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
    
    # Score-4 candidates (for reference)
    print(f"\n--- Score-4 Candidates (top 5) ---")
    score4 = []
    if 'owner_backtrack' in data:
        for c in data['owner_backtrack'].get('candidates', []):
            if c.get('score', 0) == 4:
                score4.append(c)
        for c in score4[:5]:
            print(f"  {c['target']} -> candidate_start={c['candidate_start']} range={c.get('candidate_range', 'N/A')}")
    print(f"  Total: {len(score4)} candidates")
    
    # Local islands - top clusters by score
    print(f"\n--- Top Local Island Clusters ---")
    if 'local_islands' in data:
        islands = data['local_islands']
        print(f"Total islands: {islands.get('island_count', 0)}")
        print(f"Clusters: {islands.get('cluster_count', 0)}")
        
        # Sort by cluster_score
        clusters = sorted(islands.get('clusters', []), key=lambda x: x.get('cluster_score', 0), reverse=True)[:5]
        for i, c in enumerate(clusters):
            print(f"  {i+1}. {c['range']}: score={c['cluster_score']}, {c['width']} bytes, {c['return_count']} RTS, {c['call_count']} calls")
    
    # Tiny veneers
    print(f"\n--- Tiny Veneers ---")
    if 'tiny_veneers' in data:
        veneers = data['tiny_veneers']
        print(f"Total: {veneers.get('candidate_count', 0)} veneers")
        for v in veneers.get('candidates', [])[:5]:
            print(f"  {v['range']}: {v['pattern']} -> {v['target']} ({v['confidence']})")
    
    return high_score + score5

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
            import traceback
            print(f"Error processing {f}: {e}")
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: {len(all_candidates)} score-5+ candidates across all gaps")
    print(f"{'='*60}")
    
    # Print all candidate ranges for promotion consideration
    print(f"\n--- Candidate Ranges for Promotion ---")
    for c in sorted(all_candidates, key=lambda x: (x['score'], x['target']), reverse=True):
        print(f"  {c['candidate_start']}..{c['target']} (score={c['score']}, range={c.get('candidate_range', 'N/A')})")
