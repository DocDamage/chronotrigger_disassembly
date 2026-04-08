#!/usr/bin/env python3
import json

regions = [
    ('DE:0000-4000', 'reports/de_0000_4000_islands.json'),
    ('DE:4000-8000', 'reports/de_4000_8000_islands.json'),
    ('DE:8000-C000', 'reports/de_8000_c000_islands.json'),
    ('DE:C000-FFFF', 'reports/de_c000_ffff_islands.json'),
]

print("=" * 80)
print("BANK DE EXTENDED SCAN - ALL CANDIDATES (Score-4+)")
print("=" * 80)

all_clusters = []

for region_name, path in regions:
    try:
        with open(path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        
        clusters = data.get('clusters', [])
        for c in clusters:
            c['region'] = region_name
            all_clusters.append(c)
            
    except Exception as e:
        print(f"ERROR: {e}")

# Group by score
score_10_plus = [c for c in all_clusters if c['cluster_score'] >= 10]
score_6_to_9 = [c for c in all_clusters if 6 <= c['cluster_score'] <= 9]
score_4_to_5 = [c for c in all_clusters if 4 <= c['cluster_score'] <= 5]

print(f"\nScore 10+ clusters: {len(score_10_plus)}")
print(f"Score 6-9 clusters: {len(score_6_to_9)}")
print(f"Score 4-5 clusters: {len(score_4_to_5)}")
print(f"Total score-4+ clusters: {len(score_10_plus) + len(score_6_to_9) + len(score_4_to_5)}")

# Show all score-6+
print("\n" + "=" * 80)
print("ALL SCORE-6+ CLUSTERS (8 functions)")
print("=" * 80)
score_6_plus = sorted([c for c in all_clusters if c['cluster_score'] >= 6], key=lambda x: -x['cluster_score'])
for i, c in enumerate(score_6_plus, 1):
    print(f"  {i:2d}. score={c['cluster_score']:2d} {c['range']:22s} [{c['region']}] width={c['width']:3d}")

# Show best score-4-5 to reach 15-20
print("\n" + "=" * 80)
print("BEST SCORE-4-5 CLUSTERS (to reach 15-20 targets)")
print("=" * 80)
score_4_5_sorted = sorted(score_4_to_5, key=lambda x: (-x['cluster_score'], -x['width']))
for i, c in enumerate(score_4_5_sorted[:15], 1):
    print(f"  {i:2d}. score={c['cluster_score']:2d} {c['range']:22s} [{c['region']}] width={c['width']:3d}")

# Final recommendation (15-20 functions)
print("\n" + "=" * 80)
print("FINAL RECOMMENDATION: 20 MANIFEST TARGETS (prioritized)")
print("=" * 80)

# Combine all, sort by score
top_20 = sorted(all_clusters, key=lambda x: (-x['cluster_score'], -x['width']))[:20]
for i, c in enumerate(top_20, 1):
    flags = " [DATA-MISREAD]" if c.get('data_misread_flags') else ""
    note = ""
    if c['cluster_score'] >= 10:
        note = " <- ELITE"
    elif c['cluster_score'] >= 6:
        note = " <- HIGH"
    print(f"  {i:2d}. score={c['cluster_score']:2d} {c['range']:22s} [{c['region']}] width={c['width']:3d}{flags}{note}")

# Save extended report
report = {
    'bank': 'DE',
    'summary': {
        'total_score_10_plus': len(score_10_plus),
        'total_score_6_to_9': len(score_6_to_9),
        'total_score_4_to_5': len(score_4_to_5),
        'total_score_4_plus': len(score_10_plus) + len(score_6_to_9) + len(score_4_to_5),
    },
    'score_10_plus': sorted(score_10_plus, key=lambda x: -x['cluster_score']),
    'score_6_to_9': sorted(score_6_to_9, key=lambda x: -x['cluster_score']),
    'score_4_to_5': sorted(score_4_5_sorted, key=lambda x: -x['cluster_score']),
    'recommended_20_manifests': top_20,
}

with open('reports/de_extended_scan.json', 'w') as f:
    json.dump(report, f, indent=2)

print("\n" + "=" * 80)
print("Extended report saved to: reports/de_extended_scan.json")
print("=" * 80)
