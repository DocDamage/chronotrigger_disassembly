#!/usr/bin/env python3
"""Check all manifest candidates in the manifests directory using tools.ctrepo."""

import argparse
import json
import os
import sys
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from tools.ctrepo.manifest_discovery import discover_manifest_candidates
from tools.ctrepo.manifest_validation import validate_manifest

def main() -> int:
    parser = argparse.ArgumentParser(description="Check and validate all manifest files.")
    parser.add_argument("--manifests-dir", default="passes/manifests", help="Path to manifests directory")
    parser.add_argument("--allow-legacy", action="store_true", help="Allow legacy schemas and adapt them in memory")
    parser.add_argument("--strict", action="store_true", help="Enforce strict canonical schema and naming (fail on legacy)")
    parser.add_argument("--report", default=None, help="Path to write JSON validation report")
    args = parser.parse_args()

    results = discover_manifest_candidates(manifests_dir=args.manifests_dir)
    
    total = len(results)
    valid_count = 0
    errors = []
    seen_passes = {}
    duplicates = []
    non_canonical_names = []

    for r in results:
        if not r.is_canonical_filename:
            non_canonical_names.append(r.filename)
            if args.strict:
                errors.append(f"{r.source_path}: Non-canonical filename '{r.filename}'")

        if r.error:
            errors.append(f"{r.source_path}: {r.error}")
            continue

        if r.manifest is None:
            errors.append(f"{r.source_path}: Could not parse manifest")
            continue

        p_num = r.manifest.pass_number
        if p_num in seen_passes:
            duplicates.append((p_num, seen_passes[p_num], r.source_path))
            if args.strict:
                errors.append(f"Duplicate pass {p_num}: {r.source_path} collides with {seen_passes[p_num]}")
        else:
            seen_passes[p_num] = r.source_path

        is_valid, val_errs = validate_manifest(r.manifest, strict=args.strict)
        if not is_valid:
            for ve in val_errs:
                errors.append(f"{r.source_path} (pass {p_num}): {ve}")
        else:
            valid_count += 1

    report_data = {
        "manifests_dir": args.manifests_dir,
        "total_files": total,
        "valid_count": valid_count,
        "error_count": len(errors),
        "non_canonical_names_count": len(non_canonical_names),
        "duplicate_passes_count": len(duplicates),
        "errors": errors,
        "non_canonical_names": non_canonical_names,
        "duplicates": [{"pass": p, "first": f, "second": s} for p, f, s in duplicates]
    }

    if args.report:
        os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)

    print(f"Checked {total} manifest candidates: {valid_count} valid, {len(duplicates)} duplicate IDs, {len(non_canonical_names)} non-canonical names, {len(errors)} errors")

    if args.strict and errors:
        return 1
    elif not args.allow_legacy and (errors or non_canonical_names or duplicates):
        return 1

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
