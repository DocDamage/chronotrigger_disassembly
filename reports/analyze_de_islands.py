#!/usr/bin/env python3
import json
import sys

regions = [
    ('DE:0000-4000', 'reports/de_0000_4000_islands.json'),
    ('DE:4000-8000', 'reports/de_4000_8000_islands.json'),
    ('DE:8000-C000', 'reports/de_8000_c000_islands.json'),
    ('DE:C000-FFFF', 'reports/de_c000_ffff_islands.json'),
]

print("=" * 80)
print("BANK DE DEEP SCAN - LOCAL CODE ISLANDS (Score-6+ Clusters)")
print("=" * 80)

all_clusters = []
score_10_plus = []
score_6_to_9 = []

for region_name, path in regions:
    print(f"\n{'='*40}")
    print(f"REGION: {region_name}")
    print('='*40)
    
    try:
        with open(path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        
        clusters = data.get('clusters', [])
        print(f"Total clusters: {len(clusters)}")
        
        high_clusters = [c for c in clusters if c.get('cluster_score', 0) >= 6]
        print(f"Score-6+ clusters: {len(high_clusters)}")
        
        for c in high_clusters:
            c['region'] = region_name
            all_clusters.append(c)
            if c['cluster_score'] >= 10:
                score_10_plus.append(c)
            else:
                score_6_to_9.append(c)
        
        # Show top clusters
        for c in sorted(high_clusters, key=lambda x: -x['cluster_score'])[:10]:
            flags = f" [flags={c['data_misread_flags']}]" if c.get('data_misread_flags') else ""
            print(f"  score={c['cluster_score']:2d} {c['range']:22s} width={c['width']:3d} children={c['child_count']}{flags}")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

# Summary
print("\n" + "=" * 80)
print("SUMMARY - ALL SCORE-10+ ELITE CLUSTERS (PRIORITY TARGETS)")
print("=" * 80)
for c in sorted(score_10_plus, key=lambda x: -x['cluster_score']):
    flags = f" [flags={c['data_misread_flags']}]" if c.get('data_misread_flags') else ""
    print(f"  score={c['cluster_score']:2d} {c['range']:22s} [{c['region']}] width={c['width']:3d}{flags}")

print(f"\nTotal score-10+ clusters: {len(score_10_plus)}")
print(f"Total score-6-9 clusters: {len(score_6_to_9)}")
print(f"Total score-6+ clusters: {len(all_clusters)}")

# Recommendations
print("\n" + "=" * 80)
print("RECOMMENDED MANIFEST TARGETS (15-20 functions)")
print("=" * 80)

# Sort all by score and pick best ones
top_targets = sorted(all_clusters, key=lambda x: (-x['cluster_score'], -x['width']))[:25]
for i, c in enumerate(top_targets, 1):
    flags = " [DATA-MISREAD]" if c.get('data_misread_flags') else ""
    print(f"  {i:2d}. score={c['cluster_score']:2d} {c['range']:22s} [{c['region']}] width={c['width']:3d}{flags}")

# Save full report
report = {
    'bank': 'DE',
    'summary': {
        'total_score_10_plus': len(score_10_plus),
        'total_score_6_to_9': len(score_6_to_9),
        'total_score_6_plus': len(all_clusters),
    },
    'score_10_plus_clusters': score_10_plus,
    'score_6_to_9_clusters': score_6_to_9,
    'recommended_targets': top_targets[:20],
}

with open('reports/de_deep_scan_summary.json', 'w') as f:
    json.dump(report, f, indent=2)

print("\n" + "=" * 80)
print("Full report saved to: reports/de_deep_scan_summary.json")
print("=" * 80)
