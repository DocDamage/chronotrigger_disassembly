#!/usr/bin/env python3
"""Validate Session 30 C4 manifests"""

import json
import os

# Load session 30 manifests
with open('passes/session30_c4/c4_session30_manifests.json') as f:
    manifests = json.load(f)

print('=== Session 30 C4 Manifests ===')
print(f'Total: {len(manifests)} manifests')
print()

# Verify each manifest
for m in manifests:
    fname = f"passes/session30_c4/pass{m['pass']:04d}.json"
    if os.path.exists(fname):
        with open(fname) as f:
            data = json.load(f)
            if data.get('pass') == m['pass']:
                status = 'OK'
            else:
                status = 'MISMATCH'
    else:
        status = 'MISSING'
    print(f"  Pass {m['pass']}: {m['start']}..{m['end']} ({m['size']} bytes, score={m['score']}) - {status}")

# Check for overlaps with existing
print('\n=== Overlap Check ===')
existing = []
for root, dirs, files in os.walk('passes'):
    for fname in files:
        if fname.startswith('pass') and fname.endswith('.json') and 'session30' not in root:
            path = os.path.join(root, fname)
            try:
                with open(path) as f:
                    m = json.load(f)
                    if m.get('start', '').startswith('C4:'):
                        existing.append(m)
            except:
                pass

def parse_addr(addr):
    return int(addr.split(':')[1], 16)

overlaps = 0
for m in manifests:
    m_start = parse_addr(m['start'])
    m_end = parse_addr(m['end'])
    for e in existing:
        e_start = parse_addr(e['start'])
        e_end = parse_addr(e['end'])
        if m_start < e_end and m_end > e_start:
            overlaps += 1
            print(f"  OVERLAP: Pass {m['pass']} ({m['start']}) overlaps with Pass {e['pass']} ({e['start']})")

if overlaps == 0:
    print('  No overlaps detected!')

# Calculate totals
print('\n=== Coverage Summary ===')
total_bytes = sum(m['size'] for m in manifests)
existing_bytes = sum(e.get('size', 0) for e in existing)

print(f'Existing coverage: {existing_bytes} bytes ({existing_bytes/655.36:.2f}%)')
print(f'New coverage: {total_bytes} bytes ({total_bytes/655.36:.2f}%)')
print(f'Total after Session 30: {existing_bytes + total_bytes} bytes ({(existing_bytes + total_bytes)/655.36:.2f}%)')

# Region breakdown
print('\n=== Region Breakdown ===')
regions = {}
for m in manifests:
    r = m['region']
    if r not in regions:
        regions[r] = {'count': 0, 'bytes': 0}
    regions[r]['count'] += 1
    regions[r]['bytes'] += m['size']

for r in sorted(regions.keys()):
    print(f"  {r}: {regions[r]['count']} manifests, {regions[r]['bytes']} bytes")

# Score distribution
print('\n=== Score Distribution ===')
scores = {}
for m in manifests:
    s = m['score']
    if s not in scores:
        scores[s] = 0
    scores[s] += 1

for s in sorted(scores.keys(), reverse=True):
    print(f"  Score {s}: {scores[s]} manifests")

print('\n=== All Manifests Valid ===' if overlaps == 0 else '\n=== FIX OVERLAPS ===')
