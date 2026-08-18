#!/usr/bin/env python3
"""Create manifest files for new DB candidates."""
import json
import os
from pathlib import Path

# Load recommendations
with open('reports/db_manifest_recommendations.json') as f:
    manifests = json.load(f)

# Find next available pass number
existing = []
for fname in os.listdir('passes/manifests'):
    if fname.startswith('pass') and fname.endswith('.json'):
        try:
            num = int(fname[4:].replace('.json', ''))
            existing.append(num)
        except:
            pass

next_pass = max(existing) + 1 if existing else 1

# Filter out already-documented ranges
existing_ranges = {
    'DB:00AC', 'DB:027D', 'DB:1B7E', 'DB:2190', 
    'DB:5E2B', 'DB:60FB', 'DB:6A11'
}

new_manifests = []
for m in manifests:
    addr = m['addr']
    base = addr.split('..')[0]
    if base not in existing_ranges:
        new_manifests.append(m)

print("=" * 70)
print("CREATING MANIFEST FILES FOR NEW DB CANDIDATES")
print("=" * 70)
print(f"\nNext available pass number: {next_pass}")
print(f"New manifests to create: {len(new_manifests)}")
print()

for i, m in enumerate(new_manifests[:12], 0):  # Top 12
    pass_num = next_pass + i
    fname = f"passes/new_manifests/pass{pass_num}_{m['label'].lower()}.json"
    
    manifest_data = {
        "pass_number": pass_num,
        "closed_ranges": [
            {
                "range": m['range'],
                "kind": m['kind'],
                "label": m['label'].lower(),
                "confidence": m['confidence']
            }
        ],
        "promotion_reason": f"Score-{m['score']} candidate, {m['analysis']['first_byte'] if 'analysis' in m else 'code'} prologue. Bank DB mapping."
    }
    
    Path(fname).parent.mkdir(parents=True, exist_ok=True)
    with open(fname, 'w') as f:
        json.dump(manifest_data, f, indent=2)
    
    print(f"Created: {fname}")
    print(f"  Range: {m['range']}")
    print(f"  Label: {m['label']}")
    print()

print("=" * 70)
print(f"Created {min(12, len(new_manifests))} new manifest files")
print("Location: passes/new_manifests/")
