#!/usr/bin/env python3
"""Generate coverage report for all banks based on manifest data. v2 - Fixed overlap handling."""

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


def merge_ranges(ranges):
    """Merge overlapping and adjacent ranges."""
    if not ranges:
        return []
    
    # Sort by start address
    sorted_ranges = sorted(ranges, key=lambda x: x['range'][0])
    
    merged = [sorted_ranges[0]]
    
    for current in sorted_ranges[1:]:
        last = merged[-1]
        last_start, last_end = last['range']
        curr_start, curr_end = current['range']
        
        # Check for overlap or adjacency (within 1 byte)
        if curr_start <= last_end + 1:
            # Merge ranges
            new_end = max(last_end, curr_end)
            merged[-1] = {
                'range': (last_start, new_end),
                'pass': last['pass'] + '+' + current['pass'],
                'label': last['label'] + '/merged',
                'kind': last['kind'],
                'confidence': last['confidence']
            }
        else:
            merged.append(current)
    
    return merged


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
                    if bank and start is not None and end is not None:
                        bank_ranges[bank].append({
                            'range': (start, end),
                            'pass': manifest_file.stem,
                            'label': closed_range.get('label', 'unknown'),
                            'kind': closed_range.get('kind', 'unknown'),
                            'confidence': closed_range.get('confidence', 'unknown')
                        })
        except Exception as e:
            pass  # Skip problematic files
    
    # Merge overlapping ranges for each bank
    for bank in bank_ranges:
        bank_ranges[bank] = merge_ranges(bank_ranges[bank])
    
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


def detect_overlaps(ranges):
    """Detect overlapping ranges for diagnostic purposes."""
    overlaps = []
    sorted_ranges = sorted(ranges, key=lambda x: x['range'][0])
    
    for i in range(len(sorted_ranges)):
        for j in range(i + 1, len(sorted_ranges)):
            start1, end1 = sorted_ranges[i]['range']
            start2, end2 = sorted_ranges[j]['range']
            
            if start2 <= end1:
                overlaps.append((
                    sorted_ranges[i]['pass'], 
                    sorted_ranges[j]['pass'],
                    f"Overlap: {start2:04X}-{min(end1, end2):04X}"
                ))
            else:
                break  # No more overlaps possible
    
    return overlaps


def generate_report():
    """Generate comprehensive coverage report."""
    bank_ranges = load_manifests()
    
    print("=" * 70)
    print("CHRONO TRIGGER DISASSEMBLY - BANK COVERAGE REPORT v2")
    print("=" * 70)
    print()
    
    total_coverage = 0
    total_size = 0
    total_overlaps = 0
    
    for bank in sorted(bank_ranges.keys()):
        ranges = bank_ranges[bank]
        
        # Check for overlaps before merging
        overlaps = detect_overlaps(ranges)
        if overlaps:
            total_overlaps += len(overlaps)
        
        covered_bytes = sum(r['range'][1] - r['range'][0] + 1 for r in ranges)
        coverage_pct = (covered_bytes / 0x10000) * 100
        total_coverage += covered_bytes
        total_size += 0x10000
        
        overlap_str = f" [⚠️ {len(overlaps)} overlaps]" if overlaps else ""
        print(f"\nBank {bank}: {len(ranges)} ranges, {covered_bytes} bytes ({coverage_pct:.2f}%){overlap_str}")
        print("-" * 50)
        
        if overlaps:
            print(f"  Overlaps detected:")
            for pass1, pass2, desc in overlaps[:5]:
                print(f"    {pass1} ↔ {pass2}: {desc}")
            if len(overlaps) > 5:
                print(f"    ... and {len(overlaps) - 5} more")
        
        gaps = find_gaps(bank, ranges)
        if gaps:
            print(f"  Gaps ({len(gaps)}):")
            for gap_start, gap_end in gaps[:10]:
                size = gap_end - gap_start + 1
                print(f"    {bank}:{gap_start:04X}-{bank}:{gap_end:04X} ({size} bytes, {size/256:.1f} pages)")
            if len(gaps) > 10:
                print(f"    ... and {len(gaps) - 10} more gaps")
    
    print("\n" + "=" * 70)
    print(f"TOTAL: {total_coverage} / {total_size} bytes ({(total_coverage/total_size)*100:.2f}%)")
    if total_overlaps > 0:
        print(f"⚠️  {total_overlaps} overlapping ranges detected - run conflict resolution")
    print("=" * 70)
    
    return {
        bank: {
            'ranges': ranges,
            'gaps': find_gaps(bank, ranges),
            'coverage_bytes': sum(r['range'][1] - r['range'][0] + 1 for r in ranges),
            'overlaps': detect_overlaps(ranges)
        }
        for bank, ranges in bank_ranges.items()
    }


if __name__ == '__main__':
    generate_report()
