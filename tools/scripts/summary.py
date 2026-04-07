#!/usr/bin/env python3
import os, json, re
from pathlib import Path

MANIFESTS_DIR = Path('../../passes/manifests')

# Collect all C0 passes
c0_passes = []
for fname in os.listdir(MANIFESTS_DIR):
    if fname.startswith('pass') and fname.endswith('.json'):
        with open(MANIFESTS_DIR / fname) as f:
            try:
                data = json.load(f)
                for r in data.get('closed_ranges', []):
                    if r.get('range', '').startswith('C0:'):
                        reason = data.get('promotion_reason', '')
                        m = re.search(r'(\d+) callers', reason.lower())
                        callers = int(m.group(1)) if m else 0
                        c0_passes.append({
                            'pass': fname.replace('.json', ''),
                            'range': r['range'],
                            'label': r.get('label', ''),
                            'callers': callers,
                            'reason': reason
                        })
            except:
                pass

# Sort by caller count
c0_passes.sort(key=lambda x: x['callers'], reverse=True)

print(f'=== Bank C0 Summary ===')
print(f'Total C0 functions: {len(c0_passes)}')
print()
print('=== Top 15 by caller count ===')
for p in c0_passes[:15]:
    print(f"  {p['range']}: {p['callers']} callers - {p['label'][:50]}")

# Calculate coverage
ranges = []
for p in c0_passes:
    parts = p['range'].split('..')
    if len(parts) == 2:
        start = int(parts[0].split(':')[1], 16)
        end = int(parts[1].split(':')[1], 16)
        ranges.append((start, end))

total = sum(e-s for s, e in ranges)
print()
print(f'=== Coverage ===')
print(f'Total bytes covered: {total} ({100*total/65536:.1f}% of Bank C0)')
