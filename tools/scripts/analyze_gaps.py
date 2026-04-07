#!/usr/bin/env python3
"""Analyze coverage gaps in Bank C0"""
import os, json
from pathlib import Path

MANIFESTS_DIR = Path("../../passes/manifests")

def parse_range(rstr):
    if rstr.startswith("C0:"):
        parts = rstr.split("..")
        if len(parts) == 2:
            start = int(parts[0].split(":")[1], 16)
            end = int(parts[1].split(":")[1], 16)
            return (start, end)
    return None

def main():
    # Collect all C0 ranges
    ranges = []
    for fname in os.listdir(MANIFESTS_DIR):
        if fname.startswith("pass") and fname.endswith(".json"):
            with open(MANIFESTS_DIR / fname) as f:
                try:
                    data = json.load(f)
                    for cr in data.get("closed_ranges", []):
                        r = parse_range(cr.get("range", ""))
                        if r:
                            ranges.append((r[0], r[1], fname, cr.get("label", "")))
                except:
                    pass
    
    if not ranges:
        print("No C0 ranges found")
        return
    
    # Sort by start
    ranges.sort()
    
    # Calculate coverage
    total_bytes = sum(end - start for start, end, _, _ in ranges)
    
    # Find gaps
    gaps = []
    end_marker = 0x0000
    
    for start, end, fname, label in ranges:
        if start > end_marker:
            gaps.append((end_marker, start))
        end_marker = max(end_marker, end)
    
    # Check for gap at end
    if end_marker < 0xFFFF:
        gaps.append((end_marker, 0xFFFF))
    
    print(f"=== Bank C0 Coverage ===")
    print(f"Total functions: {len(ranges)}")
    print(f"Total bytes covered: {total_bytes} ({100*total_bytes/65536:.1f}%)")
    print()
    
    # Show gaps > 256 bytes
    print(f"=== Gaps > 256 bytes ===")
    for gap_start, gap_end in gaps:
        size = gap_end - gap_start
        if size > 256:
            print(f"  C0:{gap_start:04X}..C0:{gap_end:04X}: {size} bytes")
    
    print()
    print(f"=== Top 10 gaps ===")
    gaps_sorted = sorted(gaps, key=lambda x: x[1]-x[0], reverse=True)[:10]
    for gap_start, gap_end in gaps_sorted:
        size = gap_end - gap_start
        print(f"  C0:{gap_start:04X}..C0:{gap_end:04X}: {size} bytes")
    
    # Show coverage by 4KB region
    print()
    print(f"=== Coverage by 4KB region ===")
    for region in range(0x0, 0x10000, 0x1000):
        region_ranges = [(s, e) for s, e, _, _ in ranges if s >= region and s < region + 0x1000]
        region_coverage = sum(e - s for s, e in region_ranges)
        pct = 100 * region_coverage / 0x1000
        print(f"  C0:{region:04X}-{region+0xFFF:04X}: {pct:.1f}%")

if __name__ == "__main__":
    main()
