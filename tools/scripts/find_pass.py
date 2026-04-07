import json, os, sys
from pathlib import Path

MANIFESTS_DIR = Path('../../passes/manifests')

# Find passes with overlapping ranges
targets = sys.argv[1:]

for target in targets:
    s = int(target, 16)
    for fname in sorted(os.listdir(MANIFESTS_DIR)):
        if fname.startswith('pass') and fname.endswith('.json'):
            with open(MANIFESTS_DIR / fname) as f:
                try:
                    data = json.load(f)
                    for r in data.get('closed_ranges', []):
                        rng = r['range']
                        if rng.startswith('C0:'):
                            parts = rng.split('..')
                            rs = int(parts[0].replace('C0:', ''), 16)
                            re = int(parts[1].replace('C0:', ''), 16)
                            if rs <= s <= re:
                                label = r.get('label', '')
                                print(f'{fname}: {rng} - {label}')
                except:
                    pass
