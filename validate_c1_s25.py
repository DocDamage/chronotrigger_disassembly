#!/usr/bin/env python3
"""Validate C1 Session 25 manifests."""

import json
import os

print('=' * 70)
print('Bank C1 Session 25 - Manifest Validation')
print('=' * 70)

manifest_dir = 'labels/c1_session25'
manifests = [f for f in os.listdir(manifest_dir) if f.endswith('.yaml')]

print(f'\nFound {len(manifests)} manifests:')
print('-' * 70)

all_valid = True
for m in sorted(manifests):
    filepath = os.path.join(manifest_dir, m)
    try:
        with open(filepath) as f:
            data = json.load(f)
        
        # Validate structure
        required_keys = ['manifest_version', 'session', 'target', 'metadata', 'disassembly']
        missing = [k for k in required_keys if k not in data]
        
        if missing:
            print(f'INVALID: {m} - missing keys: {missing}')
            all_valid = False
        else:
            target = data['target']
            meta = data['metadata']
            print(f'VALID: {m}')
            print(f'       {target["start_addr"]}..{target["end_addr"]} - {target["name"]}')
            print(f'       score={meta["score"]}, calls={meta["call_count"]}, branches={meta["branch_count"]}')
    except Exception as e:
        print(f'ERROR: {m} - {e}')
        all_valid = False

print('-' * 70)
result = "ALL VALID" if all_valid else "VALIDATION FAILED"
print(f'Validation result: {result}')

# Summary
if all_valid:
    print('\n### Summary Statistics ###')
    scores = []
    call_counts = []
    for m in manifests:
        with open(os.path.join(manifest_dir, m)) as f:
            data = json.load(f)
            scores.append(data['metadata']['score'])
            call_counts.append(data['metadata']['call_count'])
    
    print(f'  Total manifests: {len(manifests)}')
    print(f'  Average score: {sum(scores)/len(scores):.1f}')
    print(f'  Score distribution: 7+ = {len([s for s in scores if s >= 7])}')
    print(f'  Functions with 2+ calls (hubs): {len([c for c in call_counts if c >= 2])}')
