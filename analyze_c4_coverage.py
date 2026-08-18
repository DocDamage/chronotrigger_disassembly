#!/usr/bin/env python3
"""Analyze C4 coverage and identify high-value targets for session 27"""

import json
import os

def load_json(filepath):
    """Load JSON file if it exists"""
    if os.path.exists(filepath):
        with open(filepath) as f:
            return json.load(f)
    return None

def main():
    all_candidates = []
    
    # Load all available scan data
    sources = [
        ('c4_s26_candidates.json', 's26'),
        ('c4_7000_8000_top_candidates.json', '7000-8000'),
        ('c4_4000_5000_scan_session21.json', '4000-5000'),
        ('c4_5000_6000_scan_session21.json', '5000-6000'),
        ('c4_6000_7000_scan_session21.json', '6000-7000'),
        ('c4_7000_8000_scan_session21.json', '7000-8000'),
    ]
    
    for filepath, source in sources:
        data = load_json(filepath)
        if data:
            if isinstance(data, list):
                candidates = data
            elif isinstance(data, dict):
                candidates = data.get('candidates', [])
            else:
                continue
                
            for c in candidates:
                c['source'] = source
                # Normalize field names
                if 'addr' not in c and 'start' in c:
                    c['addr'] = c['start']
                if 'start' not in c and 'addr' in c:
                    c['start'] = c['addr']
                if 'calls' not in c and 'call_count' in c:
                    c['calls'] = c['call_count']
                if 'branches' not in c and 'branch_count' in c:
                    c['branches'] = c['branch_count']
                all_candidates.append(c)
    
    # Load islands data
    for filepath, region in [('c4_islands_4000.json', '4000-6000'), ('c4_islands_c000.json', 'C000-FFFF')]:
        data = load_json(filepath)
        if data:
            for i in data:
                i['source'] = f'islands-{region}'
                i['island'] = True
                if 'addr' not in i:
                    i['addr'] = i['range'].split('..')[0]
                if 'start' not in i:
                    i['start'] = i['addr']
                if 'calls' not in i:
                    i['calls'] = i.get('call_count', 0)
                if 'branches' not in i:
                    i['branches'] = i.get('branch_count', 0)
                all_candidates.append(i)
    
    # Filter score 5+ and remove duplicates
    seen = set()
    unique_candidates = []
    for c in all_candidates:
        addr = c.get('addr', c.get('start', ''))
        if addr and addr not in seen:
            seen.add(addr)
            if c.get('score', 0) >= 5:
                unique_candidates.append(c)
    
    # Sort by score, calls, branches
    unique_candidates.sort(key=lambda x: (-x.get('score', 0), -x.get('calls', 0), -x.get('branches', 0)))
    
    print(f"Total unique score-5+ candidates: {len(unique_candidates)}")
    print()
    
    # Group by score
    score_7_plus = [c for c in unique_candidates if c.get('score', 0) >= 7]
    score_6 = [c for c in unique_candidates if c.get('score', 0) == 6]
    score_5 = [c for c in unique_candidates if c.get('score', 0) == 5]
    
    print(f"Score 7+: {len(score_7_plus)}")
    print(f"Score 6:  {len(score_6)}")
    print(f"Score 5:  {len(score_5)}")
    print()
    
    print("=== TOP CANDIDATES FOR SESSION 27 ===")
    print()
    
    for c in unique_candidates[:25]:
        addr = c.get('addr', c.get('start', 'unknown'))
        score = c.get('score', 0)
        calls = c.get('calls', 0)
        branches = c.get('branches', 0)
        width = c.get('width', 0)
        src = c.get('source', 'unknown')
        island = ' [ISLAND]' if c.get('island') else ''
        print(f"{addr} score={score} calls={calls} branches={branches} width={width} [{src}]{island}")
    
    # Save full list for manifest creation
    with open('c4_s27_candidates.json', 'w') as f:
        json.dump(unique_candidates, f, indent=2)
    
    print()
    print(f"Saved {len(unique_candidates)} candidates to c4_s27_candidates.json")

if __name__ == '__main__':
    main()
