#!/usr/bin/env python3
"""Validate closed range ownership, duplicate ranges, and interval overlaps across all manifests."""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Tuple

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from tools.ctrepo.manifest_discovery import iter_canonical_manifests
from tools.ctrepo.range_model import detect_range_conflicts, compute_byte_union
from tools.ctrepo.manifest_models import ClosedRange

def main() -> int:
    parser = argparse.ArgumentParser(description="Validate range ownership and interval overlaps.")
    parser.add_argument("--manifests-dir", default="passes/manifests", help="Path to canonical manifests directory")
    parser.add_argument("--waivers-config", default="tools/config/range_overlap_waivers.json", help="Path to range overlap waivers registry")
    parser.add_argument("--strict", action="store_true", help="Exit with non-zero status if unresolved conflicts exist")
    parser.add_argument("--output-json", default="reports/range_ownership.json", help="Path to output JSON report")
    parser.add_argument("--output-md", default="reports/range_ownership.md", help="Path to output Markdown report")
    args = parser.parse_args()

    # Load waivers
    waiver_cids = set()
    if os.path.exists(args.waivers_config):
        try:
            with open(args.waivers_config, "r", encoding="utf-8") as f:
                w_data = json.load(f)
                for w in w_data.get("waivers", []):
                    if isinstance(w, dict) and "conflict_id" in w:
                        waiver_cids.add(w["conflict_id"])
                    elif isinstance(w, str):
                        waiver_cids.add(w)
        except Exception as e:
            print(f"Warning: Could not parse waivers config: {e}")

    # Collect all ranges
    all_ranges_with_meta: List[Tuple[ClosedRange, int, str]] = []
    all_manifests = []
    for m in iter_canonical_manifests(manifests_dir=args.manifests_dir, strict=False):
        all_manifests.append(m)
        src = m.source_path or f"pass{m.pass_number:04d}.json"
        for cr in m.closed_ranges:
            all_ranges_with_meta.append((cr, m.pass_number, src))

    print(f"Loaded {len(all_ranges_with_meta)} closed ranges across {len(all_manifests)} canonical manifests.")

    conflicts = detect_range_conflicts(all_ranges_with_meta)
    
    unresolved_conflicts = [c for c in conflicts if c.conflict_id not in waiver_cids]
    waived_conflicts = [c for c in conflicts if c.conflict_id in waiver_cids]

    exact_duplicates = [c for c in unresolved_conflicts if c.relationship == "exact_duplicate"]
    containments = [c for c in unresolved_conflicts if c.relationship == "containment"]
    partial_overlaps = [c for c in unresolved_conflicts if c.relationship == "partial_overlap"]
    code_data = [c for c in unresolved_conflicts if c.relationship == "code_data_overlap"]

    # Compute byte union
    all_closed_ranges = [r for r, _, _ in all_ranges_with_meta]
    coverage_res = compute_byte_union(all_closed_ranges)

    report_json_data = {
        "total_ranges": len(all_ranges_with_meta),
        "total_manifests": len(all_manifests),
        "total_conflicts": len(conflicts),
        "unresolved_conflicts_count": len(unresolved_conflicts),
        "waived_conflicts_count": len(waived_conflicts),
        "exact_duplicates_count": len(exact_duplicates),
        "containments_count": len(containments),
        "partial_overlaps_count": len(partial_overlaps),
        "code_data_count": len(code_data),
        "coverage_summary": coverage_res,
        "unresolved_conflicts": [
            {
                "conflict_id": c.conflict_id,
                "bank": c.bank,
                "overlap_range": c.overlap_range_str,
                "relationship": c.relationship,
                "left_pass": c.left_pass,
                "right_pass": c.right_pass,
                "left_range": c.left_range.range_str,
                "right_range": c.right_range.range_str,
                "left_label": c.left_range.label,
                "right_label": c.right_range.label,
                "suggested_resolution": c.suggested_resolution
            } for c in unresolved_conflicts
        ]
    }

    if args.output_json:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_json)), exist_ok=True)
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(report_json_data, f, indent=2)

    if args.output_md:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_md)), exist_ok=True)
        md_lines = [
            "# Range Ownership and Collision Audit",
            "",
            f"- **Total Closed Ranges**: {len(all_ranges_with_meta)}",
            f"- **Unresolved Conflicts**: {len(unresolved_conflicts)}",
            f"- **Exact Duplicates**: {len(exact_duplicates)}",
            f"- **Partial Overlaps**: {len(partial_overlaps)}",
            f"- **Containments**: {len(containments)}",
            f"- **Code/Data Collisions**: {len(code_data)}",
            f"- **Waived Conflicts**: {len(waived_conflicts)}",
            "",
            "## Unresolved Conflicts",
            ""
        ]
        if not unresolved_conflicts:
            md_lines.append("No unresolved range conflicts found. All closed ranges are mutually disjoint or explicitly structured.")
        else:
            md_lines.append("| Conflict ID | Bank | Overlap | Type | Left Pass/Range | Right Pass/Range | Suggestion |")
            md_lines.append("|---|---|---|---|---|---|---|")
            for c in unresolved_conflicts:
                md_lines.append(f"| `{c.conflict_id}` | `{c.bank}` | `{c.overlap_range_str}` | `{c.relationship}` | Pass {c.left_pass}: `{c.left_range.range_str}` ({c.left_range.label}) | Pass {c.right_pass}: `{c.right_range.range_range if hasattr(c.right_range, 'range_range') else c.right_range.range_str}` ({c.right_range.label}) | {c.suggested_resolution} |")

        with open(args.output_md, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))

    print(f"Range Ownership: {len(conflicts)} total conflicts ({len(unresolved_conflicts)} unresolved: {len(exact_duplicates)} exact dups, {len(partial_overlaps)} partial overlaps, {len(containments)} containments, {len(code_data)} code/data)")

    if args.strict and unresolved_conflicts:
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
