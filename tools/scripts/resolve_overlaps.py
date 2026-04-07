#!/usr/bin/env python3
"""
Resolve overlapping pass manifests in Bank C0.
Strategy:
1. Identify exact duplicates (delete older)
2. Identify containments (keep larger/more specific)
3. Identify partial overlaps (adjust boundaries or merge)
4. Prioritize passes with: higher confidence, more callers, cleaner boundaries
"""

import json
import os
import re
from collections import defaultdict

MANIFESTS_DIR = '../../passes/manifests'

def parse_range(range_str):
    """Parse 'C0:XXXX..C0:YYYY' to (start, end)"""
    if '..' not in range_str:
        return None
    parts = range_str.split('..')
    start = int(parts[0].split(':')[1], 16)
    end = int(parts[1].split(':')[1], 16)
    return (start, end)

def load_all_passes():
    """Load all pass manifests and their C0 ranges"""
    passes = []
    for fname in sorted(os.listdir(MANIFESTS_DIR)):
        if fname.endswith('.json') and fname.startswith('pass'):
            path = os.path.join(MANIFESTS_DIR, fname)
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                pass_num = int(fname.replace('pass', '').replace('.json', ''))
                for r in data.get('closed_ranges', []):
                    rng = r.get('range', '')
                    if rng.startswith('C0:'):
                        parsed = parse_range(rng)
                        if parsed:
                            passes.append({
                                'file': fname,
                                'pass_num': pass_num,
                                'range_str': rng,
                                'start': parsed[0],
                                'end': parsed[1],
                                'label': r.get('label', ''),
                                'confidence': r.get('confidence', 'medium'),
                                'reason': data.get('promotion_reason', ''),
                                'data': data
                            })
            except Exception as e:
                print(f"Error loading {fname}: {e}")
    return passes

def find_overlaps(passes):
    """Find all overlapping pairs"""
    overlaps = []
    for i, p1 in enumerate(passes):
        for p2 in passes[i+1:]:
            # Check overlap
            if p1['start'] < p2['end'] and p1['end'] > p2['start']:
                overlaps.append((p1, p2))
    return overlaps

def analyze_overlap(p1, p2):
    """Analyze the type of overlap and recommend action"""
    # Exact duplicate
    if p1['start'] == p2['start'] and p1['end'] == p2['end']:
        return 'exact_duplicate', max(p1, p2, key=lambda x: x['pass_num'])
    
    # Containment: p1 inside p2
    if p1['start'] >= p2['start'] and p1['end'] <= p2['end']:
        return 'containment', p1
    
    # Containment: p2 inside p1
    if p2['start'] >= p1['start'] and p2['end'] <= p1['end']:
        return 'containment', p2
    
    # Partial overlap
    return 'partial', None

def extract_caller_count(reason):
    """Extract caller count from promotion reason"""
    match = re.search(r'(\d+)\s+caller', reason.lower())
    return int(match.group(1)) if match else 0

def main():
    print("=" * 70)
    print("BANK C0 OVERLAP RESOLUTION REPORT")
    print("=" * 70)
    
    passes = load_all_passes()
    print(f"\nTotal C0 ranges loaded: {len(passes)}")
    
    overlaps = find_overlaps(passes)
    print(f"Total overlaps found: {len(overlaps)}")
    
    # Categorize overlaps
    exact_duplicates = []
    containments = []
    partials = []
    
    for p1, p2 in overlaps:
        otype, to_remove = analyze_overlap(p1, p2)
        if otype == 'exact_duplicate':
            exact_duplicates.append((p1, p2, to_remove))
        elif otype == 'containment':
            containments.append((p1, p2, to_remove))
        else:
            partials.append((p1, p2))
    
    print(f"\n--- EXACT DUPLICATES ({len(exact_duplicates)}) ---")
    for p1, p2, remove in exact_duplicates:
        print(f"  {p1['range_str']} = {p2['range_str']}")
        print(f"    Keep: pass{p1['pass_num'] if remove == p2 else p2['pass_num']}.json")
        print(f"    Remove: pass{remove['pass_num']}.json")
    
    print(f"\n--- CONTAINMENTS ({len(containments)}) ---")
    for p1, p2, remove in containments:
        container = p1 if remove == p2 else p2
        print(f"  {remove['range_str']} inside {container['range_str']}")
        print(f"    Keep: pass{container['pass_num']}.json ({container['label'][:30]})")
        print(f"    Remove: pass{remove['pass_num']}.json ({remove['label'][:30]})")
    
    print(f"\n--- PARTIAL OVERLAPS ({len(partials)}) ---")
    for p1, p2 in partials:
        overlap_start = max(p1['start'], p2['start'])
        overlap_end = min(p1['end'], p2['end'])
        print(f"  {p1['range_str']} vs {p2['range_str']}")
        print(f"    Overlap: C0:{overlap_start:04X}..C0:{overlap_end:04X}")
        c1 = extract_caller_count(p1['reason'])
        c2 = extract_caller_count(p2['reason'])
        print(f"    Pass {p1['pass_num']}: {c1} callers, confidence={p1['confidence']}")
        print(f"    Pass {p2['pass_num']}: {c2} callers, confidence={p2['confidence']}")
        # Recommendation: keep the one with more callers or higher confidence
        if c1 > c2 or (c1 == c2 and p1['confidence'] == 'high'):
            print(f"    -> Recommend keeping pass{p1['pass_num']}")
        else:
            print(f"    -> Recommend keeping pass{p2['pass_num']}")
        print()
    
    # Summary of files to remove
    to_remove = set()
    for _, _, remove in exact_duplicates:
        to_remove.add(remove['file'])
    for _, _, remove in containments:
        to_remove.add(remove['file'])
    
    print(f"\n--- FILES TO REMOVE ({len(to_remove)}) ---")
    for f in sorted(to_remove):
        print(f"  {f}")
    
    return to_remove, partials

if __name__ == '__main__':
    to_remove, partials = main()
