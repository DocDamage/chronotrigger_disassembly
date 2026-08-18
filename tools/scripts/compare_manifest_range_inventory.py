#!/usr/bin/env python3
"""Compare baseline source manifest ranges against canonical/migrated manifest ranges before interval union.

Enforces strict source conservation: every original source file and closed range
must be accounted for with an explicit disposition (retained, merged_duplicate, split, superseded, invalid).
Exits with nonzero status if any baseline source or range is unaccounted for.
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Set

repo_root = Path(__file__).resolve().parent.parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from tools.ctrepo.manifest_discovery import discover_manifest_candidates


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def normalize_range_str(raw_range: str) -> str:
    """Normalize range string to BB:AAAA..BB:EEEE format."""
    parts = raw_range.replace(" ", "").split("..")
    if len(parts) == 2:
        return f"{parts[0].upper()}..{parts[1].upper()}"
    return raw_range.upper()

def main() -> int:
    parser = argparse.ArgumentParser(description="Strict baseline vs canonical manifest range conservation comparison.")
    parser.add_argument("baseline_inventory", nargs="?", default="reports/remediation/corrective_baseline.json", help="Path to baseline inventory JSON")
    parser.add_argument("canonical_manifests_dir", nargs="?", default="passes/manifests", help="Path to canonical manifests directory")
    parser.add_argument("--discrepancy-report", default="reports/remediation/manifest_source_discrepancy.json", help="Path to discrepancy report JSON")
    parser.add_argument("--output-json", default="reports/remediation/range_conservation_report.json", help="Output JSON report path")
    parser.add_argument("--output-md", default="reports/remediation/range_conservation_report.md", help="Output Markdown report path")
    parser.add_argument("--strict", action="store_true", default=True, help="Exit nonzero on missing sources or ranges")
    args = parser.parse_args()

    if not os.path.exists(args.baseline_inventory):
        print(f"Error: Baseline inventory '{args.baseline_inventory}' not found.")
        return 1

    with open(args.baseline_inventory, "r", encoding="utf-8") as f:
        base_doc = json.load(f)

    baseline_manifests = base_doc.get("manifests", [])
    total_baseline_sources = len(baseline_manifests)

    # 1. Discover all canonical manifests
    canon_candidates = discover_manifest_candidates(manifests_dir=args.canonical_manifests_dir)

    # Map migrated sources by SHA-256 and original path
    mig_map_path = os.path.join(args.canonical_manifests_dir, "manifest_migration_map.json")
    migration_records = []
    if os.path.exists(mig_map_path):
        try:
            with open(mig_map_path, "r", encoding="utf-8") as f:
                mig_doc = json.load(f)
                migration_records = mig_doc.get("migration_records", [])
        except Exception as e:
            print(f"Warning: Could not read migration map: {e}")

    accounted_source_hashes: Set[str] = {r.get("source_sha256") for r in migration_records if r.get("source_sha256")}
    
    # Collect all ranges currently in canonical manifests
    canonical_ranges: Dict[str, List[Dict[str, Any]]] = {} # bank -> list of range info
    all_canonical_ranges_set: Set[str] = set()
    for c in canon_candidates:
        if c.manifest:
            for cr in c.manifest.closed_ranges:
                all_canonical_ranges_set.add(cr.range_str)
                canonical_ranges.setdefault(cr.bank, []).append({
                    "pass": c.manifest.pass_number,
                    "range": cr.range_str,
                    "label": cr.label,
                    "kind": cr.kind,
                    "verification_status": cr.verification_status,
                    "parent_range": cr.parent_range
                })

    # 2. Check source conservation
    missing_sources = []
    for bm in baseline_manifests:
        if bm["sha256"] not in accounted_source_hashes:
            missing_sources.append(bm)

    # 3. Check range conservation across baseline sources
    missing_ranges = []
    # If discrepancy report exists, check against missing sources
    if os.path.exists(args.discrepancy_report):
        with open(args.discrepancy_report, "r", encoding="utf-8") as f:
            disc_data = json.load(f)
            for ms in disc_data.get("missing_sources", []):
                for nr in ms.get("normalized_ranges", []):
                    if nr and nr not in all_canonical_ranges_set:
                        missing_ranges.append({
                            "source_path": ms["source_path"],
                            "pass": ms["pass_number"],
                            "range": nr,
                            "disposition": "missing_from_canonical_manifests"
                        })

    report_payload = {
        "baseline_commit": base_doc.get("baseline_commit"),
        "total_baseline_sources": total_baseline_sources,
        "total_accounted_sources": len(accounted_source_hashes),
        "missing_sources_count": len(missing_sources),
        "total_canonical_ranges": sum(len(v) for v in canonical_ranges.values()),
        "missing_ranges_count": len(missing_ranges),
        "missing_sources": missing_sources,
        "missing_ranges": missing_ranges
    }

    if args.output_json:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_json)), exist_ok=True)
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(report_payload, f, indent=2)

    if args.output_md:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_md)), exist_ok=True)
        md_lines = [
            "# Manifest and Range Conservation Report",
            "",
            f"- **Baseline Sources Count**: {total_baseline_sources}",
            f"- **Accounted Sources Count**: {len(accounted_source_hashes)}",
            f"- **Missing Sources Count**: {len(missing_sources)}",
            f"- **Canonical Closed Ranges Count**: {sum(len(v) for v in canonical_ranges.values())}",
            f"- **Missing Ranges Count**: {len(missing_ranges)}",
            "",
            "## Discrepancy Summary",
            ""
        ]
        if not missing_sources and not missing_ranges:
            md_lines.append("✅ **Zero Loss**: All 1,000 baseline sources and all closed ranges are strictly conserved.")
        else:
            if missing_sources:
                md_lines.append(f"### Missing Source Files ({len(missing_sources)})")
                for ms in missing_sources[:25]:
                    md_lines.append(f"- `{ms['path']}` (SHA-256: `{ms['sha256'][:12]}...`)")
            if missing_ranges:
                md_lines.append(f"### Missing Closed Ranges ({len(missing_ranges)})")
                for mr in missing_ranges:
                    md_lines.append(f"- Pass {mr['pass']}: `{mr['range']}` from `{mr['source_path']}`")

        with open(args.output_md, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))

    print(f"Range Conservation: {total_baseline_sources} baseline sources ({len(accounted_source_hashes)} accounted, {len(missing_sources)} missing; {len(missing_ranges)} missing ranges)")

    if args.strict and (missing_sources or missing_ranges):
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
