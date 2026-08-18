#!/usr/bin/env python3
"""Comprehensive repository health doctor and test suite runner."""

from __future__ import annotations

import argparse
import json
import os
import py_compile
import re

import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from tools.ctrepo.provenance import create_provenance_header
from tools.ctrepo.manifest_discovery import discover_manifest_candidates
from tools.ctrepo.manifest_validation import validate_manifest
from tools.ctrepo.policy_validation import validate_all_policy_registries, validate_waiver_registry
from tools.ctrepo.range_model import detect_range_conflicts


def stable_pytest_summary(output: str) -> str:
    """Remove wall-clock timing from pytest's otherwise deterministic summary."""
    summary = output.strip().splitlines()[-1] if output.strip() else ""
    return re.sub(r"\s+in\s+\d+(?:\.\d+)?s$", "", summary)

def run_doctor(strict: bool = False) -> Tuple[Dict[str, Any], bool]:
    root = repo_root
    checks: List[Dict[str, Any]] = []
    has_failures = False
    has_warnings = False

    # 1. Compile Check on all tracked python files
    py_files = []
    py_failures = []
    for p in root.rglob("*.py"):
        if ".git" in str(p) or ".venv" in str(p):
            continue
        rel = str(p.relative_to(root)).replace("\\", "/")
        py_files.append(rel)
        try:
            py_compile.compile(str(p), doraise=True)
        except Exception as e:
            py_failures.append({"path": rel, "error": str(e)})

    check_ok = len(py_failures) == 0
    if not check_ok:
        has_failures = True
    checks.append({
        "name": "python_compilation",
        "status": "pass" if check_ok else "fail",
        "total_files": len(py_files),
        "failures": py_failures
    })

    # 2. Pyflakes static analysis check
    try:
        res = subprocess.run(
            [sys.executable, "-m", "pyflakes", "tools", "tests"],
            cwd=str(root), capture_output=True, text=True
        )
        flake_output = (res.stdout + res.stderr).strip()
        flake_ok = (res.returncode == 0) and len(flake_output) == 0
        if not flake_ok:
            has_failures = True
        checks.append({
            "name": "static_analysis_pyflakes",
            "status": "pass" if flake_ok else "fail",
            "returncode": res.returncode,
            "output": flake_output
        })
    except Exception as e:
        has_failures = True
        checks.append({
            "name": "static_analysis_pyflakes",
            "status": "fail",
            "reason": str(e)
        })

    # 3. Canonical Manifest Integrity Check
    manifest_candidates = discover_manifest_candidates(manifests_dir=str(root / "passes/manifests"))
    manifest_errors = []
    duplicate_passes = {}
    seen_passes = {}
    for c in manifest_candidates:
        if not c.is_canonical_filename:
            manifest_errors.append(f"{c.source_path}: non-canonical filename '{c.filename}'")
        if c.error:
            manifest_errors.append(f"{c.source_path}: {c.error}")
        elif c.manifest:
            p_num = c.manifest.pass_number
            if p_num in seen_passes:
                duplicate_passes[p_num] = [seen_passes[p_num], c.source_path]
                manifest_errors.append(f"Duplicate pass {p_num}")
            else:
                seen_passes[p_num] = c.source_path
            is_valid, errs = validate_manifest(c.manifest, strict=True)
            if not is_valid:
                for err in errs:
                    manifest_errors.append(f"{c.source_path}: {err}")

    manifest_ok = len(manifest_errors) == 0
    if not manifest_ok:
        has_failures = True
    checks.append({
        "name": "canonical_manifest_integrity",
        "status": "pass" if manifest_ok else "fail",
        "manifest_count": len(manifest_candidates),
        "errors": manifest_errors[:20]
    })

    # 4. Range Ownership & Conflict Check
    ranges_with_meta = []
    for c in manifest_candidates:
        if c.manifest:
            for r in c.manifest.closed_ranges:
                ranges_with_meta.append((r, c.manifest.pass_number, c.source_path))

    waivers_file = root / "tools/config/range_overlap_waivers.json"
    waiver_cids = set()
    waiver_errors = validate_waiver_registry(waivers_file)
    if not waiver_errors:
        w_doc = json.loads(waivers_file.read_text(encoding="utf-8"))
        waiver_cids = {w["conflict_id"] for w in w_doc.get("waivers", [])}

    all_conflicts = detect_range_conflicts(ranges_with_meta)
    unresolved_conflicts = [c for c in all_conflicts if c.conflict_id not in waiver_cids]
    range_ok = not waiver_errors and len(unresolved_conflicts) == 0
    if not range_ok:
        has_failures = True
    checks.append({
        "name": "range_ownership_conflicts",
        "status": "pass" if range_ok else "fail",
        "total_conflicts": len(all_conflicts),
        "unresolved_conflicts_count": len(unresolved_conflicts),
        "waived_conflicts_count": len(all_conflicts) - len(unresolved_conflicts),
        "waiver_registry_errors": waiver_errors,
    })

    # 5. Branch State & Gaps Check
    try:
        res = subprocess.run(
            [sys.executable, str(root / "tools/scripts/audit_branch_state_v1.py"), "--strict-gaps"],
            cwd=str(root), capture_output=True, text=True
        )
        branch_ok = (res.returncode == 0)
        if not branch_ok:
            has_failures = True
        checks.append({
            "name": "branch_state_audit",
            "status": "pass" if branch_ok else "fail",
            "output": res.stdout.strip()
        })
    except Exception as e:
        has_failures = True
        checks.append({
            "name": "branch_state_audit",
            "status": "fail",
            "error": str(e)
        })

    # 6. Policy registries and their evidence
    policy_errors = validate_all_policy_registries()
    policy_ok = not policy_errors
    if not policy_ok:
        has_failures = True
    checks.append({
        "name": "policy_registries",
        "status": "pass" if policy_ok else "fail",
        "errors": policy_errors,
    })

    # 7. Pytest Unit Tests
    try:
        res = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=str(root), capture_output=True, text=True
        )
        test_ok = (res.returncode == 0)
        if not test_ok:
            has_failures = True
        checks.append({
            "name": "unit_tests",
            "status": "pass" if test_ok else "fail",
            "summary": stable_pytest_summary(res.stdout)
        })
    except Exception as e:
        has_failures = True
        checks.append({
            "name": "unit_tests",
            "status": "fail",
            "error": str(e)
        })

    # 8. Prohibited binaries and generated caches in Git tracking
    try:
        res = subprocess.run(
            [sys.executable, str(root / "tools/scripts/validate_binary_policy.py")],
            cwd=str(root), capture_output=True, text=True
        )
        binary_ok = res.returncode == 0
        if not binary_ok:
            has_failures = True
        checks.append({
            "name": "binary_and_cache_policy",
            "status": "pass" if binary_ok else "fail",
            "output": (res.stdout + res.stderr).strip(),
        })
    except Exception as exc:
        has_failures = True
        checks.append({
            "name": "binary_and_cache_policy",
            "status": "fail",
            "error": str(exc),
        })

    # Overall report
    overall_status = "fail" if has_failures else ("warn" if has_warnings else "pass")
    
    provenance = create_provenance_header("toolkit_doctor.py")
    report = {
        "provenance": provenance,
        "overall_status": overall_status,
        "strict_mode": strict,
        "total_checks": len(checks),
        "passed_checks": sum(1 for c in checks if c["status"] == "pass"),
        "failed_checks": sum(1 for c in checks if c["status"] == "fail"),
        "warned_checks": sum(1 for c in checks if c["status"] == "warn"),
        "checks": checks
    }

    return report, (not has_failures)


def main() -> int:
    parser = argparse.ArgumentParser(description="Repository health doctor.")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings as well as errors")
    parser.add_argument("--output-json", default="reports/toolkit_doctor.json")
    parser.add_argument("--output-md", default="reports/toolkit_doctor.md")
    args = parser.parse_args()

    report, success = run_doctor(strict=args.strict)

    if args.output_json:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_json)), exist_ok=True)
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

    if args.output_md:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_md)), exist_ok=True)
        md_lines = [
            "# Toolkit Doctor — Repository Health Report",
            "",
            f"- **Overall Status**: `{report['overall_status'].upper()}`",
            f"- **Passed Checks**: {report['passed_checks']} / {report['total_checks']}",
            f"- **Failed Checks**: {report['failed_checks']}",
            f"- **Warnings**: {report['warned_checks']}",
            "",
            "## Check Details",
            "",
            "| Check Name | Status | Details |",
            "|---|---|---|"
        ]
        for c in report["checks"]:
            md_lines.append(f"| `{c['name']}` | **{c['status'].upper()}** | {json.dumps(c.get('details') or c.get('summary') or c.get('failures') or c.get('unresolved_conflicts_count') or c.get('output') or 'OK')} |")

        with open(args.output_md, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))

    print(f"Toolkit Doctor: {report['overall_status'].upper()} ({report['passed_checks']}/{report['total_checks']} checks passed)")
    
    if args.output_json:
        print(f"Wrote {args.output_json}")
    if args.output_md:
        print(f"Wrote {args.output_md}")

    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
