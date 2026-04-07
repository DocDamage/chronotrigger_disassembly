#!/usr/bin/env python3
"""
Comprehensive pass validation tool.
Checks for overlaps, boundary issues, and suggests fixes.
"""

import json
import glob
from pathlib import Path
from typing import List, Tuple, Dict
import sys

MANIFESTS_DIR = Path('../../passes/manifests')


def addr_to_int(addr: str) -> int:
    """Convert C0:1234 to integer."""
    bank, offset = addr.split(':')
    return int(bank, 16) * 0x10000 + int(offset, 16)


def parse_range(r: str) -> Tuple[str, int, int]:
    """Parse 'C0:1234..C0:5678' into (bank, start, end)."""
    start, end = r.split('..')
    bank = start.split(':')[0]
    return (bank, addr_to_int(start), addr_to_int(end))


def ranges_overlap(r1: str, r2: str) -> Tuple[bool, str]:
    """Check if two ranges overlap. Returns (overlap, details)."""
    b1, s1, e1 = parse_range(r1)
    b2, s2, e2 = parse_range(r2)
    
    if b1 != b2:
        return (False, "Different banks")
    
    if e1 < s2 or e2 < s1:
        return (False, "No overlap")
    
    # Calculate overlap
    os_start = max(s1, s2)
    os_end = min(e1, e2)
    os_size = os_end - os_start + 1
    
    return (True, f"Overlap: {b1}:{os_start:04X}..{b1}:{os_end:04X} ({os_size} bytes)")


def load_all_passes() -> List[Tuple[str, Dict]]:
    """Load all pass manifests."""
    passes = []
    for mf in MANIFESTS_DIR.glob('pass*.json'):
        try:
            with open(mf) as f:
                data = json.load(f)
            passes.append((mf.name, data))
        except Exception as e:
            print(f"Error loading {mf.name}: {e}")
    return passes


def find_overlaps(passes: List[Tuple[str, Dict]]) -> List[Tuple[str, str, str, str]]:
    """Find all overlapping passes."""
    overlaps = []
    
    for i, (name1, data1) in enumerate(passes):
        for r1 in data1.get('closed_ranges', []):
            range1 = r1['range']
            
            for name2, data2 in passes[i+1:]:
                for r2 in data2.get('closed_ranges', []):
                    range2 = r2['range']
                    
                    is_overlap, details = ranges_overlap(range1, range2)
                    if is_overlap:
                        overlaps.append((name1, range1, name2, range2, details))
    
    return overlaps


def check_boundaries(passes: List[Tuple[str, Dict]]) -> List[Tuple[str, str, str]]:
    """Check for suspicious boundaries."""
    issues = []
    
    for name, data in passes:
        for r in data.get('closed_ranges', []):
            range_str = r['range']
            bank, start, end = parse_range(range_str)
            size = end - start + 1
            
            # Check for very small functions
            if size < 10:
                issues.append((name, range_str, f"Very small ({size} bytes)"))
            
            # Check for very large functions
            if size > 200:
                issues.append((name, range_str, f"Very large ({size} bytes)"))
            
            # Check for non-page-aligned in code regions
            # (This is a warning, not necessarily an error)
            if start % 256 != 0 and size > 50:
                issues.append((name, range_str, f"Not page-aligned (may be OK)"))
    
    return issues


def check_confidence_levels(passes: List[Tuple[str, Dict]]) -> Dict[str, int]:
    """Count passes by confidence level."""
    confidence_counts = defaultdict(int)
    
    for name, data in passes:
        for r in data.get('closed_ranges', []):
            conf = r.get('confidence', 'unknown')
            confidence_counts[conf] += 1
    
    return confidence_counts


def suggest_fixes(overlaps: List[Tuple]) -> List[Tuple[str, str, str]]:
    """Suggest fixes for overlaps."""
    suggestions = []
    
    for name1, range1, name2, range2, details in overlaps:
        b, s1, e1 = parse_range(range1)
        _, s2, e2 = parse_range(range2)
        
        # Suggest shrinking the smaller range
        size1 = e1 - s1 + 1
        size2 = e2 - s2 + 1
        
        if size1 <= size2:
            # Shrink range1
            if s1 < s2:
                new_end = s2 - 1
                new_range = f"{b}:{s1:04X}..{b}:{new_end:04X}"
                suggestions.append((name1, range1, f"Change to {new_range}"))
            else:
                new_start = e2 + 1
                new_range = f"{b}:{new_start:04X}..{b}:{e1:04X}"
                suggestions.append((name1, range1, f"Change to {new_range}"))
        else:
            # Shrink range2
            if s2 < s1:
                new_end = s1 - 1
                new_range = f"{b}:{s2:04X}..{b}:{new_end:04X}"
                suggestions.append((name2, range2, f"Change to {new_range}"))
            else:
                new_start = e1 + 1
                new_range = f"{b}:{new_start:04X}..{b}:{e2:04X}"
                suggestions.append((name2, range2, f"Change to {new_range}"))
    
    return suggestions


def main():
    print("=" * 70)
    print("PASS VALIDATION REPORT")
    print("=" * 70)
    
    passes = load_all_passes()
    print(f"\nLoaded {len(passes)} pass manifests")
    
    # Check overlaps
    print("\n" + "=" * 70)
    print("OVERLAP CHECK")
    print("=" * 70)
    
    overlaps = find_overlaps(passes)
    
    if overlaps:
        print(f"\n[FAIL] Found {len(overlaps)} overlap(s):\n")
        for name1, range1, name2, range2, details in overlaps:
            print(f"  {name1}: {range1}")
            print(f"    vs")
            print(f"  {name2}: {range2}")
            print(f"  -> {details}\n")
        
        # Suggest fixes
        print("-" * 70)
        print("SUGGESTED FIXES:")
        print("-" * 70)
        suggestions = suggest_fixes(overlaps)
        for name, old_range, suggestion in suggestions:
            print(f"  {name}: {old_range}")
            print(f"    -> {suggestion}")
    else:
        print("\n[OK] No overlaps found")
    
    # Check boundaries
    print("\n" + "=" * 70)
    print("BOUNDARY CHECK")
    print("=" * 70)
    
    boundary_issues = check_boundaries(passes)
    
    if boundary_issues:
        print(f"\n[WARN]  Found {len(boundary_issues)} boundary issue(s):\n")
        for name, range_str, issue in boundary_issues:
            print(f"  {name}: {range_str}")
            print(f"    -> {issue}")
    else:
        print("\n[OK] No boundary issues found")
    
    # Confidence summary
    print("\n" + "=" * 70)
    print("CONFIDENCE LEVELS")
    print("=" * 70)
    
    confidence = check_confidence_levels(passes)
    total = sum(confidence.values())
    
    for level in ['high', 'medium', 'low', 'unknown']:
        count = confidence.get(level, 0)
        pct = (count / total * 100) if total > 0 else 0
        bar = '#' * int(pct / 5)
        print(f"  {level:10}: {count:3} ({pct:5.1f}%) {bar}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    total_ranges = sum(len(d.get('closed_ranges', [])) for _, d in passes)
    print(f"Total passes: {len(passes)}")
    print(f"Total ranges: {total_ranges}")
    print(f"Overlaps: {len(overlaps)}")
    print(f"Boundary issues: {len(boundary_issues)}")
    
    if overlaps:
        print("\n[FAIL] Validation FAILED - fix overlaps before continuing")
        sys.exit(1)
    else:
        print("\n[OK] Validation PASSED")
        sys.exit(0)


if __name__ == '__main__':
    from collections import defaultdict
    main()
