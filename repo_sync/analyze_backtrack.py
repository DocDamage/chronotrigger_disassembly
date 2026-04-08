#!/usr/bin/env python3
import json
from collections import defaultdict

with open('repo_sync/backtrack_c0_7800_e900.json', 'r', encoding='utf-16') as f:
    data = json.load(f)

candidates = data['candidates']
score_6_plus = [c for c in candidates if c['score'] >= 6]
score_7_plus = [c for c in candidates if c['score'] >= 7]

print('=== Backtrack Analysis Summary ===')
print(f'Total candidates: {len(candidates)}')
print(f'Score >= 6: {len(score_6_plus)}')
print(f'Score >= 7: {len(score_7_plus)}')

# Group by start address to find clusters
start_clusters = defaultdict(list)
for c in score_6_plus:
    start_clusters[c['candidate_start']].append(c)

print()
print('=== Score-6 Clusters by Start Address (Top 25) ===')
for start, items in sorted(start_clusters.items(), key=lambda x: int(x[0].replace('C0:', ''), 16))[:25]:
    targets = [i['target'] for i in items]
    print(f"{start}: {len(items)} targets, start_byte={items[0]['start_byte']}, targets={targets[:3]}")

# Find distinct function ranges
print()
print('=== Distinct High-Value Ranges (Score >= 6) ===')
unique_ranges = {}
for c in sorted(score_6_plus, key=lambda x: int(x['candidate_start'].replace('C0:', ''), 16)):
    start = c['candidate_start']
    if start not in unique_ranges:
        unique_ranges[start] = c

for addr, c in list(sorted(unique_ranges.items(), key=lambda x: int(x[0].replace('C0:', ''), 16)))[:30]:
    print(f"{addr}: range={c['candidate_range']}, byte={c['start_byte']}, score={c['score']}")
