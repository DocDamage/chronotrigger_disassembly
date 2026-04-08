#!/usr/bin/env python3
import json
import sys

def analyze_backtrack(filename, region):
    with open(filename, encoding='utf-8-sig') as f:
        data = json.load(f)
    
    # Filter for score 6+ candidates
    high_score = [c for c in data['candidates'] if c['score'] >= 6]
    print(f'=== {region} Backtrack Analysis ===')
    print(f'Total candidates: {len(data["candidates"])}')
    print(f'Score 6+ candidates: {len(high_score)}')
    print()
    print('Score 6+ Candidates:')
    for c in high_score[:30]:
        print(f"  {c['candidate_start']} -> target={c['target']} score={c['score']} start_byte={c['start_byte']} {c['start_class']}")
    print()
    return high_score

def analyze_islands(filename, region):
    with open(filename, encoding='utf-8-sig') as f:
        data = json.load(f)
    
    # Filter for score 6+ clusters
    high_score = [c for c in data['clusters'] if c['cluster_score'] >= 6]
    print(f'=== {region} Islands Analysis ===')
    print(f'Total clusters: {len(data["clusters"])}')
    print(f'Score 6+ clusters: {len(high_score)}')
    print()
    print('Score 6+ Clusters:')
    for c in high_score[:20]:
        print(f"  {c['range']} score={c['cluster_score']} width={c['width']} returns={c['return_count']}")
    print()
    return high_score

if __name__ == '__main__':
    print("BANK DB ANALYSIS REPORT")
    print("=" * 60)
    print()
    
    bt1 = analyze_backtrack('reports/db_0000_4000_backtrack.json', 'DB:0000-4000')
    bt2 = analyze_backtrack('reports/db_4000_8000_backtrack.json', 'DB:4000-8000')
    
    is1 = analyze_islands('reports/db_0000_4000_islands.json', 'DB:0000-4000')
    is2 = analyze_islands('reports/db_4000_8000_islands.json', 'DB:4000-8000')
    
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f'DB:0000-4000: {len(bt1)} backtrack score-6+, {len(is1)} island score-6+')
    print(f'DB:4000-8000: {len(bt2)} backtrack score-6+, {len(is2)} island score-6+')
    print(f'Total score-6+ candidates: {len(bt1) + len(bt2) + len(is1) + len(is2)}')
