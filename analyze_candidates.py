#!/usr/bin/env python3
import json
import os

def load_candidates(path):
    with open(path, 'r', encoding='utf-16') as f:
        return json.load(f)

def get_existing_c0_labels(labels_dir):
    existing = set()
    for f in os.listdir(labels_dir):
        if 'C0' in f.upper() and f.endswith('.asm'):
            # Extract address from filename like CT_C0_80BD_xxx.asm
            parts = f.upper().replace('CT_C0_', '').split('_')
            if parts:
                addr = parts[0]
                existing.add(f'C0:{addr}')
    return existing

def main():
    labels_dir = 'labels'
    existing = get_existing_c0_labels(labels_dir)
    print(f"Found {len(existing)} existing C0 labels")
    print("="*60)
    
    # Process 8000-BFFF region
    print("\n### C0:8000-BFFF Score-6+ Candidates ###")
    d1 = load_candidates('reports/c0_8000_bfff_candidates.json')
    seen = set()
    new_8000 = []
    for c in d1['candidates']:
        if c['score'] >= 6 and c['candidate_start'] not in seen:
            seen.add(c['candidate_start'])
            status = "EXISTS" if c['candidate_start'] in existing else "NEW"
            print(f"  {c['candidate_start']} score={c['score']} {status}")
            if status == "NEW":
                new_8000.append(c)
    
    print(f"\n  Total unique score-6+ in 8000-BFFF: {len(seen)}")
    print(f"  New candidates: {len(new_8000)}")
    
    # Process C000-FFFF region
    print("\n### C0:C000-FFFF Score-6+ Candidates ###")
    d2 = load_candidates('reports/c0_c000_ffff_candidates.json')
    seen2 = set()
    new_c000 = []
    for c in d2['candidates']:
        if c['score'] >= 6 and c['candidate_start'] not in seen2:
            seen2.add(c['candidate_start'])
            status = "EXISTS" if c['candidate_start'] in existing else "NEW"
            print(f"  {c['candidate_start']} score={c['score']} {status}")
            if status == "NEW":
                new_c000.append(c)
    
    print(f"\n  Total unique score-6+ in C000-FFFF: {len(seen2)}")
    print(f"  New candidates: {len(new_c000)}")
    
    print("\n" + "="*60)
    print(f"TOTAL NEW CANDIDATES: {len(new_8000) + len(new_c000)}")
    
    # Output recommendations
    print("\n### RECOMMENDED NEW FUNCTIONS ###")
    for c in new_8000[:10]:
        print(f"  {c['candidate_start']} - score {c['score']}, {c['start_byte']} start")
    for c in new_c000[:8]:
        print(f"  {c['candidate_start']} - score {c['score']}, {c['start_byte']} start")

if __name__ == '__main__':
    main()
