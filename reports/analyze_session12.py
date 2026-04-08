import json
import sys

files = {
    'D1:1000-3FFF': 'reports/d1_1000_3fff_backtrack.json',
    'C5:9000-AFFF': 'reports/c5_9000_afff_backtrack.json',
    'CF:C000-CFFF': 'reports/cf_c000_cfff_backtrack.json',
    'D4:4000-5FFF': 'reports/d4_4000_5fff_backtrack.json',
}

for name, path in files.items():
    try:
        with open(path) as f:
            data = json.load(f)
        cands = [c for c in data.get('candidates', []) if c.get('score', 0) >= 6]
        print(f"{name}: {len(cands)} score-6+ candidates")
        for c in cands[:10]:
            print(f"  {c['candidate_start']} score={c['score']} {c['candidate_range']}")
        print()
    except Exception as e:
        print(f"{name}: Error - {e}")
