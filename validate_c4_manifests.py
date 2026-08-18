#!/usr/bin/env python3
"""Validate C4:7000-8000 manifests"""

import json
import yaml
import os

# Load manifest index
with open('c4_7000_8000_manifest_index.json') as f:
    manifests = json.load(f)

print('=== VALIDATING MANIFESTS ===')
score_7_count = 0
score_6_count = 0
score_5_count = 0
score_4_count = 0
total_bytes = 0

for m in manifests:
    filepath = f"passes/manifests/{m['file']}"
    if os.path.exists(filepath):
        with open(filepath) as f:
            content = yaml.safe_load(f)
        score = content.get('score')
        if score == 7:
            score_7_count += 1
        elif score == 6:
            score_6_count += 1
        elif score == 5:
            score_5_count += 1
        elif score == 4:
            score_4_count += 1
        total_bytes += content.get('width', 0)
        print(f"[OK] Pass {m['pass']}: {content.get('label')} - Score {score}")
    else:
        print(f"[MISSING] Pass {m['pass']}: {filepath} NOT FOUND")

print(f'\n{"="*60}')
print(f'VALIDATION SUMMARY')
print(f'{"="*60}')
print(f'Total manifests: {len(manifests)}')
print(f'  Score 7: {score_7_count}')
print(f'  Score 6: {score_6_count}')
print(f'  Score 5: {score_5_count}')
print(f'  Score 4: {score_4_count}')
print(f'Total bytes: {total_bytes}')
print(f'Passes: {manifests[0]["pass"]} - {manifests[-1]["pass"]}')
print(f'{"="*60}')
