#!/usr/bin/env python3
"""Rebuilt coverage generator using canonical manifests and interval byte unions."""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from tools.ctrepo.manifest_discovery import iter_canonical_manifests
from tools.ctrepo.range_model import compute_byte_union, detect_range_conflicts
from tools.ctrepo.provenance import create_provenance_header

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate coverage reports from canonical manifests.")
    parser.add_argument("--manifests-dir", default="passes/manifests", help="Path to manifests directory")
    parser.add_argument("--waivers-config", default="tools/config/range_overlap_waivers.json", help="Path to waivers registry")
    parser.add_argument("--output-json", default="reports/coverage.json", help="Output JSON report path")
    parser.add_argument("--output-md", default="reports/coverage.md", help="Output Markdown report path")
    parser.add_argument("--strict", action="store_true", help="Fail if unresolved conflicts or unadapted manifests exist")
    args = parser.parse_args()

    manifests = list(iter_canonical_manifests(manifests_dir=args.manifests_dir, strict=args.strict))
    
    all_ranges = []
    ranges_with_meta = []
    for m in manifests:
        for cr in m.closed_ranges:
            all_ranges.append(cr)
            ranges_with_meta.append((cr, m.pass_number, m.source_path or f"pass{m.pass_number:04d}.json"))

    # Conflict check
    waiver_cids = set()
    if os.path.exists(args.waivers_config):
        try:
            with open(args.waivers_config, "r", encoding="utf-8") as f:
                w_data = json.load(f)
                for w in w_data.get("waivers", []):
                    if isinstance(w, dict) and "conflict_id" in w:
                        waiver_cids.add(w["conflict_id"])
        except Exception:
            pass

    raw_conflicts = detect_range_conflicts(ranges_with_meta)
    unresolved_conflicts = [c for c in raw_conflicts if c.conflict_id not in waiver_cids]

    if args.strict and unresolved_conflicts:
        print(f"Error: {len(unresolved_conflicts)} unresolved range conflicts present in strict mode.")
        return 1

    # Byte union coverage
    union_res = compute_byte_union(all_ranges)

    # Denominators: SNES HiROM bank = 64 KiB (65,536 bytes)
    # Total ROM = 4 MiB (4,194,304 bytes across 64 banks C0-FF)
    BANK_SIZE = 65536
    WHOLE_ROM_SIZE = 4194304

    bank_coverage_table = {}
    for bank, covered_bytes in sorted(union_res["bank_covered_bytes"].items()):
        pct = (covered_bytes / BANK_SIZE) * 100.0
        bank_coverage_table[bank] = {
            "covered_bytes": covered_bytes,
            "bank_capacity_bytes": BANK_SIZE,
            "coverage_pct": round(pct, 2),
            "disjoint_intervals_count": len(union_res["bank_unions"].get(bank, []))
        }

    total_closed_bytes = union_res["total_covered_bytes"]
    whole_rom_pct = (total_closed_bytes / WHOLE_ROM_SIZE) * 100.0

    provenance = create_provenance_header("generate_coverage.py", manifests=manifests)

    report_payload = {
        "provenance": provenance,
        "metrics": {
            "total_manifests_count": len(manifests),
            "total_closed_ranges_count": len(all_ranges),
            "total_uniquely_closed_bytes": total_closed_bytes,
            "whole_rom_coverage_pct": round(whole_rom_pct, 4),
            "active_banks_count": len(bank_coverage_table)
        },
        "bank_coverage": bank_coverage_table,
        "bank_unions": union_res["bank_unions"]
    }

    if args.output_json:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_json)), exist_ok=True)
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(report_payload, f, indent=2)

    if args.output_md:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_md)), exist_ok=True)
        md_lines = [
            "# Chrono Trigger Disassembly — Coverage Report",
            "",
            f"- **Generated**: `{provenance['generated_at_utc']}`",
            f"- **Git Commit**: `{provenance['git_commit']}`",
            f"- **Canonical Manifests**: {len(manifests)}",
            f"- **Total Closed Ranges**: {len(all_ranges)}",
            f"- **Total Closed Bytes**: {total_closed_bytes:,} bytes",
            f"- **Whole ROM Coverage**: {whole_rom_pct:.4f}% ({total_closed_bytes:,} / {WHOLE_ROM_SIZE:,} bytes)",
            "",
            "## Bank Coverage Summary",
            "",
            "| Bank | Closed Bytes | Capacity | Coverage % | Active Intervals |",
            "|---|---|---|---|---|"
        ]
        for bank, bdata in sorted(bank_coverage_table.items()):
            md_lines.append(f"| Bank `{bank}` | {bdata['covered_bytes']:,} B | {bdata['bank_capacity_bytes']:,} B | **{bdata['coverage_pct']:.2f}%** | {bdata['disjoint_intervals_count']} |")

        with open(args.output_md, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))

    print(f"Coverage generated: {total_closed_bytes:,} bytes across {len(manifests)} manifests ({whole_rom_pct:.2f}% of whole ROM).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
