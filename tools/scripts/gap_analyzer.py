#!/usr/bin/env python3
"""
Analyze Bank C0 coverage gaps and suggest next scanning priorities.
"""

import json
import glob
from pathlib import Path
from typing import List, Tuple, Dict
from collections import defaultdict

MANIFESTS_DIR = Path('../../passes/manifests')
BANK_SIZE = 0x10000  # 64KB per bank


def addr_to_int(addr: str) -> int:
    """Convert C0:1234 to integer offset."""
    bank, offset = addr.split(':')
    return int(offset, 16)


def get_coverage_map() -> List[bool]:
    """Generate a byte-level coverage map for Bank C0."""
    coverage = [False] * BANK_SIZE
    
    for mf in MANIFESTS_DIR.glob('pass*.json'):
        try:
            with open(mf) as f:
                data = json.load(f)
            for r in data.get('closed_ranges', []):
                range_str = r['range']
                start, end = range_str.split('..')
                if start.startswith('C0:'):
                    s = addr_to_int(start)
                    e = addr_to_int(end)
                    for i in range(s, min(e + 1, BANK_SIZE)):
                        coverage[i] = True
        except:
            pass
    
    return coverage


def find_gaps(coverage: List[bool], min_gap_size: int = 256) -> List[Tuple[int, int, int]]:
    """Find consecutive gaps in coverage. Returns list of (start, end, size)."""
    gaps = []
    in_gap = False
    gap_start = 0
    
    for i, covered in enumerate(coverage):
        if not covered and not in_gap:
            in_gap = True
            gap_start = i
        elif covered and in_gap:
            in_gap = False
            gap_size = i - gap_start
            if gap_size >= min_gap_size:
                gaps.append((gap_start, i - 1, gap_size))
    
    # Handle gap at end
    if in_gap:
        gap_size = BANK_SIZE - gap_start
        if gap_size >= min_gap_size:
            gaps.append((gap_start, BANK_SIZE - 1, gap_size))
    
    return sorted(gaps, key=lambda x: -x[2])


def estimate_function_count(gap_size: int) -> int:
    """Estimate number of functions in a gap based on typical function sizes."""
    # Average function size is roughly 20-40 bytes
    return max(1, gap_size // 512)  # Conservative estimate


def format_addr(offset: int) -> str:
    """Format offset as C0:XXXX."""
    return f"C0:{offset:04X}"


def analyze_gap_quality(gap_start: int, gap_end: int) -> Dict:
    """Analyze the quality of a gap (likely code vs data)."""
    # This is a heuristic based on address ranges
    # Different regions have different characteristics
    
    # Known code-heavy regions
    code_regions = [
        (0x0000, 0x2000),  # System/utility
        (0x4000, 0x8000),  # Core game logic
        (0xC000, 0xD000),  # Script engine
    ]
    
    # Known data-heavy regions
    data_regions = [
        (0xB400, 0xB800),  # Data tables
        (0xCC00, 0xD000),  # Jump tables
    ]
    
    gap_center = (gap_start + gap_end) // 2
    
    for start, end in code_regions:
        if start <= gap_center <= end:
            return {'quality': 'high', 'reason': 'Known code region'}
    
    for start, end in data_regions:
        if start <= gap_center <= end:
            return {'quality': 'low', 'reason': 'Known data region'}
    
    return {'quality': 'medium', 'reason': 'Unknown region'}


def main():
    print("=" * 70)
    print("BANK C0 GAP ANALYZER")
    print("=" * 70)
    
    # Get coverage
    coverage = get_coverage_map()
    covered_bytes = sum(coverage)
    coverage_pct = (covered_bytes / BANK_SIZE) * 100
    
    print(f"\nCurrent coverage: {covered_bytes:,} bytes ({coverage_pct:.1f}%)")
    print(f"Uncovered: {BANK_SIZE - covered_bytes:,} bytes ({100 - coverage_pct:.1f}%)")
    
    # Find gaps
    gaps = find_gaps(coverage, min_gap_size=256)
    
    print(f"\n{'=' * 70}")
    print(f"TOP 15 GAPS (sorted by size)")
    print(f"{'=' * 70}")
    print(f"{'Rank':<6} {'Start':<10} {'End':<10} {'Size':<10} {'Pages':<8} {'Est.Func':<10} {'Quality':<10}")
    print("-" * 70)
    
    for i, (start, end, size) in enumerate(gaps[:15], 1):
        pages = size // 256
        est_func = estimate_function_count(size)
        quality = analyze_gap_quality(start, end)
        
        print(f"{i:<6} {format_addr(start):<10} {format_addr(end):<10} "
              f"{size:<10} {pages:<8} {est_func:<10} {quality['quality']:<10}")
    
    # Recommendations
    print(f"\n{'=' * 70}")
    print(f"SCAN RECOMMENDATIONS")
    print(f"{'=' * 70}")
    
    high_quality_gaps = [g for g in gaps if analyze_gap_quality(g[0], g[1])['quality'] == 'high']
    
    if high_quality_gaps:
        print("\nHigh-priority code regions:")
        for start, end, size in high_quality_gaps[:5]:
            pages = (size + 255) // 256  # Round up
            print(f"  {format_addr(start)}..{format_addr(end)} ({pages} pages)")
            print(f"    Command: python batch_scan.py --regions C0:{start:04X}:{pages}")
    
    # Page-level breakdown
    print(f"\n{'=' * 70}")
    print(f"PAGE-LEVEL COVERAGE (256-byte pages)")
    print(f"{'=' * 70}")
    
    page_coverage = []
    for page in range(256):
        page_start = page * 256
        page_end = page_start + 256
        covered = sum(coverage[page_start:page_end])
        pct = (covered / 256) * 100
        page_coverage.append((page, pct))
    
    zero_pages = [p for p, pct in page_coverage if pct == 0]
    partial_pages = [(p, pct) for p, pct in page_coverage if 0 < pct < 100]
    
    print(f"\nFully covered pages: {sum(1 for _, pct in page_coverage if pct == 100)}/256")
    print(f"Partially covered: {len(partial_pages)}")
    print(f"Zero coverage: {len(zero_pages)}")
    
    if zero_pages:
        print(f"\nZero-coverage page ranges:")
        # Group consecutive pages
        ranges = []
        start = zero_pages[0]
        prev = zero_pages[0]
        
        for page in zero_pages[1:]:
            if page == prev + 1:
                prev = page
            else:
                ranges.append((start, prev))
                start = page
                prev = page
        ranges.append((start, prev))
        
        for start, end in ranges[:10]:
            if start == end:
                print(f"  C0:{start:02X}00")
            else:
                print(f"  C0:{start:02X}00-C0:{end:02X}FF ({end-start+1} pages)")


if __name__ == '__main__':
    main()
