#!/usr/bin/env python3
import json
import os

os.chdir(r'c:\Users\Doc\Desktop\chronotrigger_disassembly')

# Load island data
regions = [
    ('D6:0000-6000', r'reports\D6_0000_6000_islands.json'),
    ('D6:7000-8000', r'reports\D6_7000_8000_islands.json'),
    ('D6:8000-C000', r'reports\D6_8000_C000_islands.json'),
    ('D6:C000-FFFF', r'reports\D6_C000_FFFF_islands.json'),
]

all_clusters = []
for region_name, path in regions:
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    for cluster in data.get('clusters', []):
        cluster['region'] = region_name
        all_clusters.append(cluster)

# Filter score 6+ and sort by score
high_score = [c for c in all_clusters if c.get('cluster_score', 0) >= 6]
high_score.sort(key=lambda x: (-x['cluster_score'], x['range']))

print('=== D6 Bank - Score 6+ Code Clusters ===')
print(f'Total clusters found: {len(all_clusters)}')
print(f'Score 6+ clusters: {len(high_score)}')
print()

for i, c in enumerate(high_score, 1):
    flags = ','.join(c.get('data_misread_flags', [])) if c.get('data_misread_flags') else 'none'
    print(f"{i}. Region: {c['region']}")
    print(f"   Range: {c['range']}")
    print(f"   Score: {c['cluster_score']} (children: {c['child_count']})")
    print(f"   Size: {c['width']} bytes, Calls: {c['call_count']}, Returns: {c['return_count']}")
    print(f"   Flags: {flags}")
    print()

# Also process caller data
print('\n=== D6 Bank - Cross-Bank Caller Analysis ===')
caller_regions = [
    ('D6:0000-6000', r'reports\D6_0000_6000_callers.json'),
    ('D6:7000-8000', r'reports\D6_7000_8000_callers.json'),
    ('D6:8000-C000', r'reports\D6_8000_C000_callers.json'),
    ('D6:C000-FFFF', r'reports\D6_C000_FFFF_callers.json'),
]

all_callers = []
for region_name, path in caller_regions:
    try:
        with open(path, encoding='utf-8-sig') as f:
            data = json.load(f)
        for cand in data.get('candidates', []):
            cand['region'] = region_name
            all_callers.append(cand)
    except Exception as e:
        print(f"Error loading {path}: {e}")

# Filter score 6+ callers
high_caller_score = [c for c in all_callers if c.get('score', 0) >= 6]
high_caller_score.sort(key=lambda x: (-x['score'], x['candidate_start']))

print(f'Total caller candidates: {len(all_callers)}')
print(f'Score 6+ caller candidates: {len(high_caller_score)}')
print()

# Group by candidate_start to find unique function entry points
from collections import defaultdict
entry_points = defaultdict(list)
for c in high_caller_score:
    entry_points[c['candidate_start']].append(c)

print(f'Unique high-score entry points: {len(entry_points)}')
print()

# Show top entry points
for start, targets in sorted(entry_points.items(), key=lambda x: -len(x[1]))[:20]:
    print(f"Entry: {start} - {len(targets)} cross-bank references")
