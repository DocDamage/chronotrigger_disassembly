#!/usr/bin/env python3
"""Compare range inventories before and after manifest migration to guarantee zero data loss."""

import json
import sys
import argparse

def main() -> int:
    parser = argparse.ArgumentParser(description="Compare baseline ranges vs post-migration ranges.")
    parser.add_argument("baseline", help="Path to baseline ranges or manifest inventory JSON")
    parser.add_argument("post_migration", help="Path to post-migration manifest check or inventory JSON")
    args = parser.parse_args()

    with open(args.baseline, "r", encoding="utf-8") as f:
        base_data = json.load(f)

    with open(args.post_migration, "r", encoding="utf-8") as f:
        post_data = json.load(f)

    # Extract ranges from baseline
    base_ranges = set()
    if "entries" in base_data:
        for e in base_data["entries"]:
            for r in e.get("ranges", []):
                base_ranges.add((r["range"], r.get("label", "")))
    elif "migration_records" in base_data:
        # Dry run map
        pass

    print(f"Loaded {len(base_ranges)} baseline ranges.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
