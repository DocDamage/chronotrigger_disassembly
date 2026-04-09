#!/usr/bin/env python3
"""Plan for C1 Session 29 - Process remaining score-6+ candidates"""
import json
import os

# All processed manifests from S25-S28 and C1_8C3E
processed = set()

# From session reports
for session in [25, 26, 27, 28]:
    try:
        with open(f'C1_SESSION{session}_REPORT.json', 'r') as f:
            sdata = json.load(f)
            for m in sdata.get('manifests', []):
                range_str = m.get('range', '')
                if range_str:
                    addr = range_str.split('..')[0]
                    processed.add(addr)
    except:
        pass

# From C1_8C3E new manifests
with open('reports/c1_8c3e_new_manifests.json', 'r') as f:
    data = json.load(f)
    for m in data.get('all_new_manifests', []):
        processed.add(m['addr'])

print(f"Total processed: {len(processed)}")

# All score-6+ candidates from initial scan + hub analysis
candidates = []

# From initial scan summary
with open('reports/C1_initial_scan_summary.json', 'r') as f:
    data = json.load(f)

for region, info in data.get('score_6_plus_summary', {}).items():
    for c in info.get('top_clusters', []):
        if 'addr' in c and '..' not in c['addr']:
            candidates.append({
                'addr': c['addr'],
                'score': c.get('score', 6),
                'width': c.get('width', 25),
                'type': c.get('type', 'subroutine'),
                'source': 'initial_scan'
            })

# From hub analysis report (high-score clusters)
hub_candidates = [
    {'addr': 'C1:1569', 'score': 9, 'width': 52, 'type': 'cluster', 'source': 'hub_analysis'},
    {'addr': 'C1:1183', 'score': 6, 'width': 25, 'type': 'subroutine', 'source': 'hub_analysis'},
    {'addr': 'C1:15A6', 'score': 6, 'width': 24, 'type': 'subroutine', 'source': 'hub_analysis'},
    {'addr': 'C1:1933', 'score': 6, 'width': 25, 'type': 'subroutine', 'source': 'hub_analysis'},
    {'addr': 'C1:1C3E', 'score': 8, 'width': 40, 'type': 'cluster', 'source': 'hub_analysis'},
    {'addr': 'C1:4CBD', 'score': 9, 'width': 58, 'type': 'cluster', 'source': 'hub_analysis'},
    {'addr': 'C1:492A', 'score': 6, 'width': 25, 'type': 'subroutine', 'source': 'hub_analysis'},
    {'addr': 'C1:49E6', 'score': 6, 'width': 25, 'type': 'subroutine', 'source': 'hub_analysis'},
    {'addr': 'C1:4A58', 'score': 6, 'width': 25, 'type': 'subroutine', 'source': 'hub_analysis'},
    {'addr': 'C1:83DE', 'score': 6, 'width': 17, 'type': 'subroutine', 'source': 'hub_analysis'},
    {'addr': 'C1:8E95', 'score': 8, 'width': 22, 'type': 'cluster', 'source': 'hub_analysis'},
    {'addr': 'C1:8824', 'score': 6, 'width': 25, 'type': 'subroutine', 'source': 'hub_analysis'},
    {'addr': 'C1:8EF8', 'score': 6, 'width': 25, 'type': 'subroutine', 'source': 'hub_analysis'},
    {'addr': 'C1:8D21', 'score': 6, 'width': 21, 'type': 'subroutine', 'source': 'hub_analysis'},
    {'addr': 'C1:8963', 'score': 6, 'width': 18, 'type': 'subroutine', 'source': 'hub_analysis'},
    {'addr': 'C1:9DD4', 'score': 6, 'width': 12, 'type': 'subroutine', 'source': 'hub_analysis'},
    {'addr': 'C1:B3A2', 'score': 8, 'width': 33, 'type': 'cluster', 'source': 'hub_analysis'},
    {'addr': 'C1:B2F8', 'score': 6, 'width': 10, 'type': 'subroutine', 'source': 'hub_analysis'},
    {'addr': 'C1:C011', 'score': 6, 'width': 25, 'type': 'subroutine', 'source': 'hub_analysis'},
    # Hub functions
    {'addr': 'C1:178E', 'score': 6, 'width': 30, 'type': 'hub', 'callers': 25, 'source': 'hub_analysis'},
    {'addr': 'C1:1B55', 'score': 6, 'width': 30, 'type': 'hub', 'callers': 29, 'source': 'hub_analysis'},
    {'addr': 'C1:4AEB', 'score': 6, 'width': 30, 'type': 'hub', 'callers': 27, 'source': 'hub_analysis'},
]

for c in hub_candidates:
    # Check if not already in candidates list
    if not any(x['addr'] == c['addr'] for x in candidates):
        candidates.append(c)

print(f"Total candidates: {len(candidates)}")

# Find remaining
remaining = [c for c in candidates if c['addr'] not in processed]
print(f"Remaining candidates: {len(remaining)}")

# Sort by score descending, then by address
remaining.sort(key=lambda x: (-x['score'], x['addr']))

print("\n=== REMAINING CANDIDATES ===")
score7 = [c for c in remaining if c['score'] == 7]
score6 = [c for c in remaining if c['score'] == 6]
print(f"Score 7: {len(score7)}")
print(f"Score 6: {len(score6)}")

# Group by region
by_region = {}
for c in remaining:
    addr_int = int(c['addr'].split(':')[1], 16)
    region_start = addr_int // 0x1000
    region = f'{region_start:01X}000-{(region_start+1):01X}FFF'
    if region not in by_region:
        by_region[region] = []
    by_region[region].append(c)

print("\n=== BY REGION ===")
for region in sorted(by_region.keys()):
    print(f"\nC1:{region}: {len(by_region[region])} candidates")
    for c in sorted(by_region[region], key=lambda x: -x['score']):
        print(f"  {c['addr']} - score {c['score']} - {c['width']} bytes - {c['type']}")

# Save full list
with open('c1_all_candidates.json', 'w') as f:
    json.dump({
        'processed': sorted(list(processed)),
        'remaining': remaining,
        'stats': {
            'total_processed': len(processed),
            'total_remaining': len(remaining),
            'score7_remaining': len(score7),
            'score6_remaining': len(score6)
        }
    }, f, indent=2)

# Select best 10-12 for session 29
# Target regions: 3000-4000, 6000-7000, 9000-A000, D000-E000, E000-F000
# Plus other under-covered regions

selected = []
target_regions = {'3000-3FFF', '6000-6FFF', '9000-9FFF', 'D000-DFFF', 'E000-EFFF'}
region_counts = {}

# First pass: pick score-7+ from target regions
for c in remaining:
    if c['score'] < 7:
        continue
    addr_int = int(c['addr'].split(':')[1], 16)
    region_start = addr_int // 0x1000
    region_key = f'{region_start:01X}000'
    
    if region_key in ['3000', '6000', '9000', 'D000', 'E000']:
        if region_key not in region_counts:
            region_counts[region_key] = 0
        if region_counts[region_key] < 3 and len(selected) < 12:
            selected.append(c)
            region_counts[region_key] = region_counts.get(region_key, 0) + 1

# Second pass: pick best score-6 from target regions
for c in remaining:
    if c in selected or c['score'] != 6:
        continue
    addr_int = int(c['addr'].split(':')[1], 16)
    region_start = addr_int // 0x1000
    region_key = f'{region_start:01X}000'
    
    if region_key in ['3000', '6000', '9000', 'D000', 'E000']:
        if region_key not in region_counts:
            region_counts[region_key] = 0
        if region_counts[region_key] < 3 and len(selected) < 12:
            selected.append(c)
            region_counts[region_key] = region_counts.get(region_key, 0) + 1

# Third pass: pick any remaining high scores to fill to 10-12
for c in remaining:
    if c in selected:
        continue
    if len(selected) < 12:
        selected.append(c)

print("\n=== SELECTED FOR SESSION 29 ===")
for c in selected:
    print(f"  {c['addr']} - score {c['score']} - {c['width']} bytes - {c['type']}")

# Save selection
with open('c1_session29_candidates.json', 'w') as f:
    json.dump(selected, f, indent=2)

print(f"\nTotal selected for session 29: {len(selected)}")
print("Saved to c1_session29_candidates.json")
