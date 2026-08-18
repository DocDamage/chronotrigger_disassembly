#!/usr/bin/env python3
"""Regenerate canonical reports in isolation and compare deterministic payloads."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from tools.ctrepo.policy_validation import validate_report_provenance


def _run(command: List[str]) -> None:
    result = subprocess.run(command, cwd=repo_root, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(
            f"command failed ({result.returncode}): {' '.join(command)}\n{result.stdout}\n{result.stderr}"
        )


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _semantic_payload(document: Dict[str, Any]) -> Dict[str, Any]:
    payload = copy.deepcopy(document)
    payload.pop("provenance", None)
    return payload


def _semantic_markdown(text: str) -> str:
    return "\n".join(
        line for line in text.replace("\r\n", "\n").splitlines()
        if not line.startswith("- **Generated**:")
    ).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Check generated report drift without modifying tracked files")
    parser.add_argument("--require-clean-provenance", action="store_true")
    args = parser.parse_args()
    errors: List[str] = []

    with tempfile.TemporaryDirectory(prefix="ct-report-drift-") as temp_name:
        temp = Path(temp_name)
        outputs = {
            "coverage": (
                repo_root / "reports" / "coverage.json",
                temp / "coverage.json",
            ),
            "doctor": (
                repo_root / "reports" / "toolkit_doctor.json",
                temp / "doctor.json",
            ),
            "range_ownership": (
                repo_root / "reports" / "range_ownership.json",
                temp / "range_ownership.json",
            ),
        }
        markdown_outputs = {
            "coverage": (repo_root / "reports" / "coverage.md", temp / "coverage.md"),
            "doctor": (repo_root / "reports" / "toolkit_doctor.md", temp / "doctor.md"),
            "range_ownership": (repo_root / "reports" / "range_ownership.md", temp / "range_ownership.md"),
        }

        _run([
            sys.executable, "tools/scripts/generate_coverage.py", "--strict",
            "--output-json", str(outputs["coverage"][1]),
            "--output-md", str(temp / "coverage.md"),
        ])
        _run([
            sys.executable, "tools/scripts/toolkit_doctor.py", "--strict",
            "--output-json", str(outputs["doctor"][1]),
            "--output-md", str(temp / "doctor.md"),
        ])
        _run([
            sys.executable, "tools/scripts/validate_range_ownership.py", "--strict",
            "--output-json", str(outputs["range_ownership"][1]),
            "--output-md", str(temp / "range_ownership.md"),
        ])

        for name, (committed_path, fresh_path) in outputs.items():
            if not committed_path.exists():
                errors.append(f"{name}: missing committed report {committed_path}")
                continue
            committed = _load(committed_path)
            fresh = _load(fresh_path)
            committed_provenance = committed.get("provenance", {})
            fresh_provenance = fresh.get("provenance", {})
            errors.extend(
                f"{name} committed provenance: {error}"
                for error in validate_report_provenance(committed_provenance)
            )
            if _semantic_payload(committed) != _semantic_payload(fresh):
                errors.append(f"{name}: deterministic report payload differs from fresh generation")
            if committed_provenance.get("manifest_set_digest") != fresh_provenance.get("manifest_set_digest"):
                errors.append(f"{name}: manifest_set_digest is stale")
            if committed_provenance.get("generator_source_digest") != fresh_provenance.get("generator_source_digest"):
                errors.append(f"{name}: generator_source_digest is stale")
            if args.require_clean_provenance and not committed_provenance.get("worktree_clean_before_generation"):
                errors.append(f"{name}: committed report was not generated from a clean worktree")

        for name, (committed_path, fresh_path) in markdown_outputs.items():
            if not committed_path.exists():
                errors.append(f"{name}: missing committed Markdown report {committed_path}")
                continue
            committed = _semantic_markdown(committed_path.read_text(encoding="utf-8"))
            fresh = _semantic_markdown(fresh_path.read_text(encoding="utf-8"))
            if committed != fresh:
                errors.append(f"{name}: deterministic Markdown payload differs from fresh generation")

    if errors:
        print("Report drift/provenance errors:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Report drift: deterministic payloads and provenance are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
