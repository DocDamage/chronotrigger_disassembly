#!/usr/bin/env python3
import json

def analyze_gap(filepath):
    with open(filepath, 'r', encoding='utf-16') as f:
        data = json.load(f)
    
    range_name = data.get('range', 'Unknown')
    print(f"\n{'='*60}")
    print(f"GAP: {range_name}")
    print(f"{'='*60}")
    
    # Page family
    page_family = data.get('page_family', {})
    print(f"\nPage Family: {page_family.get('page_family', 'N/A')}")
    print(f"Reasons: {page_family.get('reasons', [])}")
    metrics = page_family.get('metrics', {})
    print(f"Metrics: branch_ratio={metrics.get('branch_ratio', 0):.3f}, call_ratio={metrics.get('call_ratio', 0):.3f}, returns={metrics.get('return_count', 0)}")
    
    # Score-6+ candidates from owner backtrack
    print(f"\n--- Score-6+ Owner Backtrack Candidates ---")
    high_score = []
    if 'owner_backtrack' in data:
        for c in data['owner_backtrack'].get('candidates', []):
            if c.get('score', 0) >= 6:
                high_score.append(c)
                start_byte = c['start_byte']
                if isinstance(start_byte, int):
                    start_byte_str = f"{start_byte:02X}"
                else:
                    start_byte_str = str(start_byte)
                print(f"  {c['target']} -> candidate_start={c['candidate_start']} score={c['score']} distance={c['distance_to_target']} range={c.get('candidate_range', 'N/A')}")
    print(f"  Total: {len(high_score)} candidates")
    
    # Score-5 candidates
    print(f"\n--- Score-5 Candidates ---")
    score5 = []
    if 'owner_backtrack' in data:
        for c in data['owner_backtrack'].get('candidates', []):
            if c.get('score', 0) == 5:
                score5.append(c)
                print(f"  {c['target']} -> candidate_start={c['candidate_start']} range={c.get('candidate_range', 'N/A')}")
    print(f"  Total: {len(score5)} candidates")
    
    # Local islands
    print(f"\n--- Local Islands ---")
    if 'local_islands' in data:
        islands = data['local_islands']
        print(f"Total islands: {islands.get('island_count', 0)}")
        print(f"Clusters: {islands.get('cluster_count', 0)}")
        for c in islands.get('clusters', [])[:5]:
            print(f"  Cluster {c['cluster_idx']}: {c['range']} ({c['byte_count']} bytes, {c['return_count']} RTS)")
    
    # Tiny veneers
    print(f"\n--- Tiny Veneers ---")
    if 'tiny_veneers' in data:
        veneers = data['tiny_veneers']
        print(f"Total: {veneers.get('candidate_count', 0)} veneers")
        for v in veneers.get('candidates', [])[:5]:
            print(f"  {v['range']}: {v['pattern']} -> {v['target']} ({v['confidence']})")
    
    return high_score

if __name__ == "__main__":
    files = [
        'reports/c3_2900_3058_flow.json',
        'reports/c3_30b1_34ff_flow.json',
        'reports/c3_3761_3c7f_flow.json'
    ]
    
    all_candidates = []
    for f in files:
        try:
            candidates = analyze_gap(f)
            all_candidates.extend(candidates)
        except Exception as e:
            print(f"Error processing {f}: {e}")
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: {len(all_candidates)} score-6+ candidates across all gaps")
    print(f"{'='*60}")
