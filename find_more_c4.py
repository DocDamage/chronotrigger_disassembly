#!/usr/bin/env python3
"""Find additional C4 candidates for expanded coverage"""

import json
import os

def load_json(filepath):
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        try:
            with open(filepath) as f:
                return json.load(f)
        except:
            return None
    return None

def main():
    all_candidates = []
    
    # Load session 27 candidates (already used)
    s27 = load_json('c4_s27_candidates.json')
    used_addrs = set()
    if s27:
        for c in s27[:11]:  # First 11 were used
            addr = c.get('addr') or c.get('start')
            if addr:
                used_addrs.add(addr)
    
    print(f"Already used: {len(used_addrs)} addresses")
    print()
    
    # Load scan files and get ALL clusters/islands with score 5+
    scan_files = [
        ('c4_4000_5000_scan_session21.json', '4000-5000'),
        ('c4_5000_6000_scan_session21.json', '5000-6000'),
        ('c4_6000_7000_scan_session21.json', '6000-7000'),
        ('c4_7000_8000_scan_session21.json', '7000-8000'),
    ]
    
    for filepath, region in scan_files:
        data = load_json(filepath)
        if not data:
            continue
            
        # Get all islands
        islands = data.get('islands', [])
        for i in islands:
            addr = i.get('range', '').split('..')[0] if 'range' in i else None
            if addr and addr not in used_addrs and i.get('score', 0) >= 5:
                i['addr'] = addr
                i['source'] = region
                i['type'] = 'island'
                all_candidates.append(i)
        
        # Get all clusters
        clusters = data.get('clusters', [])
        for c in clusters:
            addr = c.get('start')
            if addr and addr not in used_addrs and c.get('score', 0) >= 5:
                c['addr'] = addr
                c['source'] = region
                c['type'] = 'cluster'
                c['width'] = c.get('width', 0)
                c['calls'] = c.get('calls', c.get('call_count', 0))
                c['branches'] = c.get('branches', c.get('branch_count', 0))
                all_candidates.append(c)
    
    # Add remaining s27 candidates not yet used
    if s27:
        for c in s27[11:]:
            addr = c.get('addr') or c.get('start')
            if addr and addr not in used_addrs:
                c['type'] = 's27_remaining'
                all_candidates.append(c)
    
    # Remove duplicates and sort
    seen = set()
    unique = []
    for c in all_candidates:
        addr = c.get('addr')
        if addr and addr not in seen:
            seen.add(addr)
            unique.append(c)
    
    unique.sort(key=lambda x: (-x.get('score', 0), -x.get('calls', 0), -x.get('branches', 0)))
    
    print(f"Additional score-5+ candidates: {len(unique)}")
    print()
    
    # Show top candidates
    print("=" * 60)
    print("TOP ADDITIONAL CANDIDATES")
    print("=" * 60)
    print()
    
    total_bytes = 0
    for c in unique[:20]:
        addr = c.get('addr', 'unknown')
        score = c.get('score', 0)
        calls = c.get('calls', c.get('call_count', 0))
        branches = c.get('branches', c.get('branch_count', 0))
        width = c.get('width', 0)
        src = c.get('source', c.get('type', 'unknown'))
        rng = c.get('range', '')
        total_bytes += width
        print(f"{addr} score={score} calls={calls} branches={branches} width={width:2} [{src}]")
        if rng:
            print(f"           {rng}")
    
    print()
    print(f"Top 20 total bytes: {total_bytes}")
    print(f"Estimated coverage: +{(total_bytes/65536)*100:.2f}%")
    
    # Save for manifest creation
    with open('c4_s27_additional.json', 'w') as f:
        json.dump(unique, f, indent=2)

if __name__ == '__main__':
    main()
