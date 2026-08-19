#!/usr/bin/env python3
"""Audit local import surfaces and smoke-test toolkit CLI entrypoints."""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS_ROOT = REPO_ROOT / "tools"


@dataclass(frozen=True)
class AuditIssue:
    path: str
    kind: str
    detail: str


def python_files(root: Path = TOOLS_ROOT) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.py")
        if "__pycache__" not in path.parts
    )


def parse_files(paths: Iterable[Path]) -> tuple[dict[Path, ast.Module], list[AuditIssue]]:
    trees: dict[Path, ast.Module] = {}
    issues: list[AuditIssue] = []
    for path in paths:
        rel = path.relative_to(REPO_ROOT).as_posix()
        try:
            trees[path] = ast.parse(path.read_text(encoding="utf-8-sig"), filename=rel)
        except (OSError, SyntaxError, UnicodeError) as exc:
            issues.append(AuditIssue(rel, "parse_error", str(exc)))
    return trees, issues


def module_exports(tree: ast.Module) -> set[str]:
    exports: set[str] = set()
    explicit_all: set[str] | None = None
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            exports.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                if alias.name != "*":
                    exports.add(alias.asname or alias.name.split(".")[0])
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    exports.add(target.id)
            if (
                isinstance(node, ast.Assign)
                and any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets)
                and isinstance(node.value, (ast.List, ast.Tuple, ast.Set))
            ):
                values = {
                    item.value
                    for item in node.value.elts
                    if isinstance(item, ast.Constant) and isinstance(item.value, str)
                }
                explicit_all = values
    return explicit_all if explicit_all is not None else exports


def resolve_local_module(source: Path, module: str | None, level: int) -> Path | None:
    parts = module.split(".") if module else []
    if level:
        base = source.parent
        for _ in range(level - 1):
            base = base.parent
        candidate = base.joinpath(*parts)
        options = (candidate.with_suffix(".py"), candidate / "__init__.py")
    else:
        options_list: list[Path] = []
        for base in (source.parent, REPO_ROOT):
            candidate = base.joinpath(*parts)
            options_list.extend((candidate.with_suffix(".py"), candidate / "__init__.py"))
        options = tuple(options_list)
    return next((path.resolve() for path in options if path.is_file()), None)


def audit_local_imports(trees: dict[Path, ast.Module]) -> list[AuditIssue]:
    issues: list[AuditIssue] = []
    exports = {path.resolve(): module_exports(tree) for path, tree in trees.items()}
    for source, tree in trees.items():
        rel = source.relative_to(REPO_ROOT).as_posix()
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            target = resolve_local_module(source, node.module, node.level)
            if target is None or target not in exports:
                continue
            available = exports[target]
            for alias in node.names:
                if alias.name == "*" or alias.name in available:
                    continue
                target_rel = target.relative_to(REPO_ROOT).as_posix()
                issues.append(
                    AuditIssue(
                        rel,
                        "missing_local_import",
                        f"line {node.lineno}: {alias.name!r} is not exported by {target_rel}",
                    )
                )
    return issues


def is_cli_entrypoint(tree: ast.Module) -> bool:
    has_argparse = any(
        isinstance(node, (ast.Import, ast.ImportFrom))
        and any(alias.name == "argparse" for alias in node.names)
        for node in tree.body
    )
    has_main_guard = any(
        isinstance(node, ast.If)
        and isinstance(node.test, ast.Compare)
        and isinstance(node.test.left, ast.Name)
        and node.test.left.id == "__name__"
        for node in tree.body
    )
    return has_argparse and has_main_guard


def smoke_cli_entrypoints(
    trees: dict[Path, ast.Module], timeout_seconds: float = 10.0
) -> tuple[list[str], list[AuditIssue]]:
    checked: list[str] = []
    issues: list[AuditIssue] = []
    for path, tree in trees.items():
        if not is_cli_entrypoint(tree):
            continue
        rel = path.relative_to(REPO_ROOT).as_posix()
        checked.append(rel)
        try:
            result = subprocess.run(
                [sys.executable, str(path), "--help"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired:
            issues.append(AuditIssue(rel, "help_timeout", f"exceeded {timeout_seconds:g}s"))
            continue
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip().splitlines()
            issues.append(
                AuditIssue(rel, "help_failure", detail[-1] if detail else f"exit {result.returncode}")
            )
    return checked, issues


def run_audit(timeout_seconds: float = 10.0) -> tuple[dict[str, object], bool]:
    paths = python_files()
    trees, issues = parse_files(paths)
    issues.extend(audit_local_imports(trees))
    checked, smoke_issues = smoke_cli_entrypoints(trees, timeout_seconds)
    issues.extend(smoke_issues)
    report: dict[str, object] = {
        "status": "pass" if not issues else "fail",
        "python_files_scanned": len(paths),
        "cli_entrypoints_smoke_tested": len(checked),
        "cli_entrypoints": checked,
        "issues": [asdict(issue) for issue in issues],
    }
    return report, not issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit toolkit-local imports and smoke-test argparse entrypoints."
    )
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--output-json", default="")
    args = parser.parse_args()

    report, success = run_audit(timeout_seconds=args.timeout)
    if args.output_json:
        output = Path(args.output_json)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
