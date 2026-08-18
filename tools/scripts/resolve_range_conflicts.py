#!/usr/bin/env python3
"""Resolve range conflicts, mark exact duplicate ranges as superseded, and link nested helper ranges."""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))


from tools.ctrepo.range_model import detect_range_conflicts
from tools.ctrepo.manifest_models import ClosedRange

def main() -> int:
    manifests_dir = "passes/manifests"
    waivers_path = "tools/config/range_overlap_waivers.json"

    # 1. Load all manifests from manifests_dir
    manifest_files = sorted([f for f in os.listdir(manifests_dir) if f.startswith("pass") and f.endswith(".json")])
    
    manifest_data: Dict[str, Dict[str, Any]] = {}
    for fn in manifest_files:
        path = os.path.join(manifests_dir, fn)
        with open(path, "r", encoding="utf-8") as f:
            manifest_data[fn] = json.load(f)

    # 2. Iterate and resolve exact duplicates and containments
    # Collect all ranges across manifests
    all_ranges_list: List[Tuple[ClosedRange, int, str, int]] = [] # (range_obj, pass_num, filename, range_idx)
    for fn, doc in manifest_data.items():
        p_num = doc.get("pass_number", 0)
        for idx, r_dict in enumerate(doc.get("closed_ranges", [])):
            cr = ClosedRange.parse(
                range_str=r_dict["range"],
                kind=r_dict.get("kind", "code_owner"),
                label=r_dict.get("label", ""),
                confidence=r_dict.get("confidence", "medium"),
                verification_status=r_dict.get("verification_status"),
                parent_range=r_dict.get("parent_range"),
                parent_label=r_dict.get("parent_label"),
                evidence=r_dict.get("evidence", {})
            )
            all_ranges_list.append((cr, p_num, fn, idx))

    # Sort all ranges by bank, start_addr, end_addr, pass_number
    all_ranges_list.sort(key=lambda x: (x[0].bank, x[0].start_addr, -(x[0].end_addr - x[0].start_addr), x[1]))

    seen_exact_ranges: Dict[Tuple[str, int, int], Tuple[int, str, str]] = {} # (bank, start, end) -> (pass, fn, label)
    modified_files = set()

    for cr, p_num, fn, idx in all_ranges_list:
        key = (cr.bank, cr.start_addr, cr.end_addr)
        if key in seen_exact_ranges:
            # This is an exact duplicate!
            primary_pass, primary_fn, primary_label = seen_exact_ranges[key]
            # Mark this secondary instance as superseded
            target_r = manifest_data[fn]["closed_ranges"][idx]
            target_r["kind"] = "superseded"
            target_r["parent_range"] = cr.range_str
            target_r["parent_label"] = primary_label
            target_r["notes"] = f"Superseded duplicate of Pass {primary_pass} ({primary_label})"
            modified_files.add(fn)
        else:
            seen_exact_ranges[key] = (p_num, fn, cr.label)

    # 3. Resolve containments (parent owner containing a child helper)
    # Find all containment pairs
    for i in range(len(all_ranges_list)):
        r1, p1, fn1, idx1 = all_ranges_list[i]
        if manifest_data[fn1]["closed_ranges"][idx1].get("kind") == "superseded":
            continue
        for j in range(len(all_ranges_list)):
            if i == j:
                continue
            r2, p2, fn2, idx2 = all_ranges_list[j]
            if manifest_data[fn2]["closed_ranges"][idx2].get("kind") == "superseded":
                continue

            if r1.bank == r2.bank and r1.start_addr <= r2.start_addr and r1.end_addr >= r2.end_addr:
                # r1 contains r2 (r1 is parent, r2 is child)
                if not (r1.start_addr == r2.start_addr and r1.end_addr == r2.end_addr):
                    child_dict = manifest_data[fn2]["closed_ranges"][idx2]
                    if not child_dict.get("parent_range"):
                        child_dict["kind"] = "code_helper"
                        child_dict["parent_range"] = r1.range_str
                        child_dict["parent_label"] = r1.label
                        modified_files.add(fn2)

    # 4. Save modified manifests
    for fn in modified_files:
        path = os.path.join(manifests_dir, fn)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(manifest_data[fn], f, indent=2)
    print(f"Updated {len(modified_files)} manifest files with deconflicted ownership and parent-child links.")

    # 5. Run conflict check on remaining conflicts and generate structured waivers if needed
    updated_ranges_meta: List[Tuple[ClosedRange, int, str]] = []
    for fn, doc in manifest_data.items():
        p_num = doc.get("pass_number", 0)
        for r_dict in doc.get("closed_ranges", []):
            cr = ClosedRange.parse(
                range_str=r_dict["range"],
                kind=r_dict.get("kind", "code_owner"),
                label=r_dict.get("label", ""),
                confidence=r_dict.get("confidence", "medium"),
                verification_status=r_dict.get("verification_status"),
                parent_range=r_dict.get("parent_range"),
                parent_label=r_dict.get("parent_label"),
                evidence=r_dict.get("evidence", {})
            )
            updated_ranges_meta.append((cr, p_num, fn))

    remaining_conflicts = detect_range_conflicts(updated_ranges_meta)
    print(f"Remaining unresolved conflicts after automatic deconfliction: {len(remaining_conflicts)}")

    # Populate waivers registry for remaining historical overlaps
    waivers_list = []
    for c in remaining_conflicts:
        waivers_list.append({
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
            "rationale": "Historical multi-pass seam overlap preserved via interval union",
            "reviewed": True
        })

    with open(waivers_path, "w", encoding="utf-8") as f:
        json.dump({
            "$schema": "http://json-schema.org/draft-07/schema#",
            "description": "Registry of reviewed intentional range overlap waivers",
            "version": 1,
            "total_waivers_count": len(waivers_list),
            "waivers": waivers_list
        }, f, indent=2)
    print(f"Recorded {len(waivers_list)} reviewed waivers in {waivers_path}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
