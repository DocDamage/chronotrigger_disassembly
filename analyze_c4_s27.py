#!/usr/bin/env python3
"""Analyze C4 coverage and identify high-value targets for session 27"""

import json
import os
import struct

def load_json(filepath):
    """Load JSON file if it exists and is valid"""
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        try:
            with open(filepath) as f:
                return json.load(f)
        except:
            return None
    return None

def parse_islands_binary(filepath):
    """Try to parse islands file which may be binary or have non-JSON content"""
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
            # Try to decode as JSON with error handling
            try:
                return json.loads(content.decode('utf-8', errors='ignore'))
            except:
                return None
    except:
        return None

def extract_clusters_from_scan(data):
    """Extract high-scoring clusters from scan data"""
    clusters = data.get('clusters', [])
    high_clusters = []
    for c in clusters:
        if c.get('score', 0) >= 5:
            high_clusters.append({
                'addr': c.get('start'),
                'start': c.get('start'),
                'range': c.get('range'),
                'score': c.get('score'),
                'calls': c.get('calls', c.get('call_count', 0)),
                'branches': c.get('branches', c.get('branch_count', 0)),
                'width': c.get('width', 0),
                'source': 'scan-cluster'
            })
    return high_clusters

def main():
    all_candidates = []
    
    # Load session 26 candidates
    data = load_json('c4_s26_candidates.json')
    if data:
        for c in data:
            c['source'] = 's26'
            all_candidates.append(c)
    
    # Load 7000-8000 top candidates
    data = load_json('c4_7000_8000_top_candidates.json')
    if data:
        for c in data:
            c['source'] = '7000-8000'
            c['addr'] = c.get('range', '').split('..')[0] if 'range' in c else None
            c['start'] = c['addr']
            c['calls'] = c.get('call_count', 0)
            c['branches'] = c.get('branch_count', 0)
            all_candidates.append(c)
    
    # Load scan files and extract clusters
    scan_files = [
        ('c4_4000_5000_scan_session21.json', '4000-5000'),
        ('c4_5000_6000_scan_session21.json', '5000-6000'),
        ('c4_6000_7000_scan_session21.json', '6000-7000'),
        ('c4_7000_8000_scan_session21.json', '7000-8000'),
    ]
    
    for filepath, region in scan_files:
        data = load_json(filepath)
        if data:
            clusters = extract_clusters_from_scan(data)
            for c in clusters:
                c['source'] = region
                all_candidates.append(c)
            
            # Also extract high-scoring islands
            islands = data.get('islands', [])
            for i in islands:
                if i.get('score', 0) >= 5:
                    i['source'] = f'{region}-island'
                    i['addr'] = i.get('range', '').split('..')[0] if 'range' in i else None
                    i['start'] = i['addr']
                    i['calls'] = i.get('call_count', 0)
                    i['branches'] = i.get('branch_count', 0)
                    all_candidates.append(i)
    
    # Filter score 5+ and remove duplicates by address
    seen = set()
    unique_candidates = []
    for c in all_candidates:
        addr = c.get('addr') or c.get('start')
        if addr and addr not in seen:
            seen.add(addr)
            if c.get('score', 0) >= 5:
                unique_candidates.append(c)
    
    # Sort by score (desc), calls (desc), branches (desc)
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
    
    print("=" * 60)
    print("TOP CANDIDATES FOR SESSION 27 MANIFESTS")
    print("=" * 60)
    print()
    
    for c in unique_candidates[:30]:
        addr = c.get('addr') or c.get('start', 'unknown')
        score = c.get('score', 0)
        calls = c.get('calls', 0)
        branches = c.get('branches', 0)
        width = c.get('width', 0)
        src = c.get('source', 'unknown')
        rng = c.get('range', '')
        print(f"{addr} score={score} calls={calls} branches={branches} width={width:2} [{src}]")
        if rng:
            print(f"           Range: {rng}")
    
    # Save full list for manifest creation
    with open('c4_s27_candidates.json', 'w') as f:
        json.dump(unique_candidates, f, indent=2)
    
    print()
    print(f"Saved {len(unique_candidates)} candidates to c4_s27_candidates.json")
    
    # Return top candidates for manifest creation
    return unique_candidates[:15]

if __name__ == '__main__':
    main()
