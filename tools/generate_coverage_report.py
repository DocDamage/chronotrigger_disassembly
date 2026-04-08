#!/usr/bin/env python3
"""Generate coverage report for all banks based on manifest data."""

import json
import os
import re
from pathlib import Path
from collections import defaultdict

def parse_range(range_str):
    """Parse a range string like 'C0:DA52..C0:DA68' into (bank, start, end)."""
    match = re.match(r'([A-F0-9]+):([A-F0-9]+)\.\.\1:([A-F0-9]+)', range_str)
    if match:
        bank = match.group(1)
        start = int(match.group(2), 16)
        end = int(match.group(3), 16)
        return bank, start, end
    return None, None, None


def load_manifests(manifests_dir='passes/manifests'):
    """Load all pass manifests and extract bank coverage info."""
    manifests_path = Path(manifests_dir)
    bank_ranges = defaultdict(list)
    
    for manifest_file in sorted(manifests_path.glob('pass*.json')):
        try:
            with open(manifest_file, 'r') as f:
                data = json.load(f)
            
            # Extract address ranges from closed_ranges
            if 'closed_ranges' in data:
                for closed_range in data['closed_ranges']:
                    range_str = closed_range.get('range', '')
                    bank, start, end = parse_range(range_str)
                    if bank:
                        bank_ranges[bank].append({
                            'range': (start, end),
                            'pass': manifest_file.stem,
                            'label': closed_range.get('label', 'unknown'),
                            'kind': closed_range.get('kind', 'unknown'),
                            'confidence': closed_range.get('confidence', 'unknown')
                        })
        except Exception as e:
            pass  # Skip problematic files
    
    return bank_ranges


def find_gaps(bank, ranges, bank_size=0x10000):
    """Find gaps in bank coverage."""
    if not ranges:
        return [(0, bank_size - 1)]
    
    # Sort by start address
    sorted_ranges = sorted(ranges, key=lambda x: x['range'][0])
    
    gaps = []
    current_end = 0
    
    for item in sorted_ranges:
        start, end = item['range']
        if start > current_end:
            gaps.append((current_end, start - 1))
        current_end = max(current_end, end + 1)
    
    if current_end < bank_size:
        gaps.append((current_end, bank_size - 1))
    
    return gaps


def generate_report():
    """Generate comprehensive coverage report."""
    bank_ranges = load_manifests()
    
    print("=" * 70)
    print("CHRONO TRIGGER DISASSEMBLY - BANK COVERAGE REPORT")
    print("=" * 70)
    print()
    
    total_coverage = 0
    total_size = 0
    
    for bank in sorted(bank_ranges.keys()):
        ranges = bank_ranges[bank]
        covered_bytes = sum(r['range'][1] - r['range'][0] + 1 for r in ranges)
        coverage_pct = (covered_bytes / 0x10000) * 100
        total_coverage += covered_bytes
        total_size += 0x10000
        
        print(f"\nBank {bank}: {len(ranges)} ranges, {covered_bytes} bytes ({coverage_pct:.2f}%)")
        print("-" * 50)
        
        gaps = find_gaps(bank, ranges)
        if gaps:
            print(f"  Gaps ({len(gaps)}):")
            for gap_start, gap_end in gaps[:10]:  # Limit to first 10 gaps
                size = gap_end - gap_start + 1
                print(f"    {bank}:{gap_start:04X}-{bank}:{gap_end:04X} ({size} bytes, {size/256:.1f} pages)")
            if len(gaps) > 10:
                print(f"    ... and {len(gaps) - 10} more gaps")
    
    print("\n" + "=" * 70)
    print(f"TOTAL: {total_coverage} / {total_size} bytes ({(total_coverage/total_size)*100:.2f}%)")
    print("=" * 70)
    
    # Return bank info for agent tasking
    return {
        bank: {
            'ranges': ranges,
            'gaps': find_gaps(bank, ranges),
            'coverage_bytes': sum(r['range'][1] - r['range'][0] + 1 for r in ranges)
        }
        for bank, ranges in bank_ranges.items()
    }


if __name__ == '__main__':
    generate_report()
