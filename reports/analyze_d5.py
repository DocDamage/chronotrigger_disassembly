#!/usr/bin/env python3
import json

with open('reports/d5_analysis.json') as f:
    data = json.load(f)

clusters = data['clusters']
score6_plus = [c for c in clusters if c['cluster_score'] >= 6]

print("=" * 60)
print("BANK D5 ANALYSIS SUMMARY")
print("=" * 60)
print(f"Total clusters found: {len(clusters)}")
print(f"Score 6+ clusters: {len(score6_plus)}")
print()

print("Top Score-6+ Function Candidates:")
print("-" * 60)
for c in sorted(score6_plus, key=lambda x: -x['cluster_score'])[:25]:
    flags = f" flags={c['data_misread_flags']}" if c['data_misread_flags'] else ""
    print(f"  {c['range']}: score={c['cluster_score']}, width={c['width']}, calls={c['call_count']}, rets={c['return_count']}{flags}")

print()
print("=" * 60)
print("SUMMARY BY REGION")
print("=" * 60)

regions = [
    (0x0000, 0x4000, "Lower"),
    (0x4000, 0x8000, "Mid"),
    (0x8000, 0xC000, "Upper"),
    (0xC000, 0xFFFF, "Bank End")
]

for start, end, name in regions:
    region_clusters = [c for c in clusters if start <= int(c['range'].split('..')[0].split(':')[1], 16) < end]
    region_score6 = [c for c in region_clusters if c['cluster_score'] >= 6]
    print(f"{name} ({start:04X}-{end:04X}): {len(region_clusters)} clusters, {len(region_score6)} score-6+")
