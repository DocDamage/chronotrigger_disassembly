#!/usr/bin/env python3
import json, os
from pathlib import Path

MANIFESTS_DIR = Path('../../passes/manifests')

def find_range(addr):
    for fname in os.listdir(MANIFESTS_DIR):
        if fname.startswith('pass') and fname.endswith('.json'):
            with open(MANIFESTS_DIR / fname) as f:
                try:
                    data = json.load(f)
                    for r in data.get('closed_ranges', []):
                        if addr in r['range']:
                            print(f'{fname}: {r["range"]} - {r.get("label", "")}')
                except:
                    pass

print('Looking for C0:4B49:')
find_range('C0:4B49')
print()
print('Looking for C0:4B65:')
find_range('C0:4B65')
