#!/usr/bin/env python3
"""Analyze remaining C1 candidates"""
import json

# Load the initial scan
with open('reports/C1_initial_scan_summary.json', 'r') as f:
    data = json.load(f)

# Build list of all candidates from the summary
all_candidates = []
for region, info in data.get('score_6_plus_summary', {}).items():
    for c in info.get('top_clusters', []):
        if 'addr' in c:
            # Skip range addresses like C1:434A..C1:43B7
            addr = c['addr']
            if '..' in addr:
                continue
            all_candidates.append({
                'addr': addr,
                'score': c.get('score', 6),
                'width': c.get('width', 25),
                'type': c.get('type', 'subroutine')
            })

print(f'Total top clusters found: {len(all_candidates)}')
print()

# Load processed manifests from session reports
processed = set()
for session in [25, 26, 27, 28]:
    try:
        with open(f'C1_SESSION{session}_REPORT.json', 'r') as f:
            sdata = json.load(f)
            for m in sdata.get('manifests', []):
                processed.add(m['addr'])
    except Exception as e:
        print(f"Error loading session {session}: {e}")

# Also check labels directory for any C1 manifests
import os
labels_dir = 'labels'
if os.path.exists(labels_dir):
    for root, dirs, files in os.walk(labels_dir):
        for f in files:
            if f.startswith('C1_') and f.endswith('.yaml'):
                # Extract address from filename
                parts = f.split('_')
                if len(parts) >= 2:
                    addr = 'C1:' + parts[1].upper()
                    processed.add(addr)

print(f'Processed candidates: {len(processed)}')

# Find remaining
remaining = [c for c in all_candidates if c['addr'] not in processed]
print(f'Remaining candidates: {len(remaining)}')
print()

# Group by score
score7 = [c for c in remaining if c['score'] == 7]
score6 = [c for c in remaining if c['score'] == 6]
print(f'Score 7 remaining: {len(score7)}')
print(f'Score 6 remaining: {len(score6)}')
print()

# Group by region
by_region = {}
for c in remaining:
    addr_int = int(c['addr'].split(':')[1], 16)
    region = f'{addr_int//0x1000:01X}000-{addr_int//0x1000+1:01X}FFF'
    if region not in by_region:
        by_region[region] = []
    by_region[region].append(c)

print('Remaining by region:')
for region in sorted(by_region.keys()):
    print(f'  C1:{region}: {len(by_region[region])} candidates')

print()
print('=== DETAILED REMAINING CANDIDATES ===')
for c in sorted(remaining, key=lambda x: (x['score'], x['addr']), reverse=True):
    print(f"{c['addr']} - score {c['score']} - {c['width']} bytes - {c['type']}")

# Save to file
with open('c1_remaining_candidates.json', 'w') as f:
    json.dump(remaining, f, indent=2)
print()
print('Saved to c1_remaining_candidates.json')
