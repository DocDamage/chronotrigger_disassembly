#!/usr/bin/env python3
"""Check Bank C0 coverage in disassembly passes."""

import json
import glob

# Find all pass manifests
passes = glob.glob('../../passes/manifests/pass*.json')
print(f"Found {len(passes)} pass manifests")

# Track covered 256-byte pages in Bank C0
c0_pages = set()

for p in passes:
    try:
        with open(p) as f:
            data = json.load(f)
        
        for r in data.get('closed_ranges', []):
            rng = r.get('range', '')
            if rng.startswith('C0:'):
                # Extract start address
                start = rng.split('..')[0]
                addr = int(start.split(':')[1], 16)
                page = addr // 256
                c0_pages.add(page)
    except Exception as e:
        print(f"Error reading {p}: {e}")

print(f'Pages covered: {len(c0_pages)}/256')

# Find missing pages
missing = [f"C0:{i*256:04X}" for i in range(256) if i not in c0_pages]
print(f'Missing count: {len(missing)}')
if missing:
    print(f'Missing pages: {missing[:30]}')
    if len(missing) > 30:
        print(f'... and {len(missing) - 30} more')

# Save missing list for scanning
with open('missing_c0_pages.txt', 'w') as f:
    for m in missing:
        f.write(m + '\n')
print(f"Saved {len(missing)} missing pages to missing_c0_pages.txt")
