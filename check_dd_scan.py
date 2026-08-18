#!/usr/bin/env python3
"""Check DD scan output directly"""
import json
import subprocess

def run_scan(range_text):
    cmd = [
        'python', 'tools/scripts/find_local_code_islands_v2.py',
        '--rom', 'rom/Chrono Trigger (USA).sfc',
        '--range', range_text,
        '--max-back', '48',
        '--json'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

# Scan all regions
regions = [
    'DD:0000..DD:3FFF',
    'DD:4000..DD:7FFF', 
    'DD:8000..DD:BFFF',
    'DD:C000..DD:FFFF'
]

all_clusters = []
for r in regions:
    print(f"\n=== {r} ===")
    data = run_scan(r)
    clusters = data.get('clusters', [])
    print(f"Clusters: {len(clusters)}")
    
    if clusters:
        # Sort by cluster_score
        sorted_clusters = sorted(clusters, key=lambda x: x.get('cluster_score', 0), reverse=True)
        print("Top 10 by cluster_score:")
        for c in sorted_clusters[:10]:
            print(f"  {c.get('range')}: score={c.get('cluster_score')}, width={c.get('width')}, returns={c.get('return_count')}")
        all_clusters.extend(clusters)

# Summary
print(f"\n\n=== OVERALL SUMMARY ===")
print(f"Total clusters: {len(all_clusters)}")

# Count by cluster_score
score_counts = {}
for c in all_clusters:
    s = c.get('cluster_score', 0)
    score_counts[s] = score_counts.get(s, 0) + 1

print("\nScore distribution:")
for s in sorted(score_counts.keys(), reverse=True):
    print(f"  Score {s}: {score_counts[s]} clusters")

# Show score-6+
score6_plus = [c for c in all_clusters if c.get('cluster_score', 0) >= 6]
print(f"\nScore-6+ clusters: {len(score6_plus)}")
for c in sorted(score6_plus, key=lambda x: x.get('cluster_score', 0), reverse=True):
    print(f"  {c.get('range')}: score={c.get('cluster_score')}, width={c.get('width')}, returns={c.get('return_count')}, calls={c.get('call_count')}")
