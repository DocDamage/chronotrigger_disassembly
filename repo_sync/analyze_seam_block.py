#!/usr/bin/env python3
import json
import glob

# Load the seam block results
with open('repo_sync/seam_block_7800.json', 'r', encoding='utf-16') as f:
    data = json.load(f)

print('=== Seam Block Analysis: C0:7800-81FF ===')
print(f"Pages analyzed: {len(data['pages'])}")
print()

# Extract high-scoring candidates
high_score_candidates = []
for page in data['pages']:
    for bt in page.get('top_backtracks', []):
        if bt['score'] >= 6:
            high_score_candidates.append({
                'page': page['range'],
                'candidate_start': bt['candidate_start'],
                'score': bt['score'],
                'start_byte': bt['start_byte'],
                'target': bt['target'],
                'candidate_range': bt['candidate_range']
            })

print(f"Found {len(high_score_candidates)} score-6+ backtrack candidates:")
for c in sorted(high_score_candidates, key=lambda x: int(x['candidate_start'].replace('C0:', ''), 16)):
    print(f"  {c['candidate_start']} -> {c['target']} (score={c['score']}, byte={c['start_byte']})")
    print(f"    Range: {c['candidate_range']}")

# Also look at local clusters with high scores
print()
print('=== High-Value Local Clusters (score >= 5) ===')
for page in data['pages']:
    for cluster in page.get('local_clusters', []):
        if cluster['cluster_score'] >= 5:
            print(f"  {cluster['range']}: score={cluster['cluster_score']}, calls={cluster['call_count']}, returns={cluster['return_count']}, branches={cluster['branch_count']}")

# Check best targets
print()
print('=== Strong/Weak Targets ===')
for page in data['pages']:
    for target in page.get('best_targets', []):
        if target['best_strength'] in ('strong', 'weak'):
            print(f"  {target['target']} ({target['best_strength']}): {len(target['callers'])} callers")
