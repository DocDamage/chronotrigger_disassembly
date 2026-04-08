#!/usr/bin/env python3
import json
from pathlib import Path

files = [
    ('0000-4000', 'reports/d4_0000_4000_backtrack.json'),
    ('6000-8000', 'reports/d4_6000_8000_backtrack.json'),
    ('8000-C000', 'reports/d4_8000_c000_backtrack.json'),
    ('C000-FFFF', 'reports/d4_c000_ffff_backtrack.json'),
    ('4000-6000', 'reports/d4_4000_5fff_backtrack.json')
]

all_candidates = []
for region, path in files:
    p = Path(path)
    if not p.exists():
        print('Missing: ' + path)
        continue
    try:
        with open(p) as f:
            data = json.load(f)
        for c in data.get('candidates', []):
            c['region'] = region
            all_candidates.append(c)
        print(region + ': ' + str(len(data.get('candidates', []))) + ' candidates')
    except Exception as e:
        print('Error ' + path + ': ' + str(e))

print('Total: ' + str(len(all_candidates)))

# Dedupe
seen = set()
unique = []
for c in sorted(all_candidates, key=lambda x: (-x['score'], x['candidate_start'])):
    key = c['candidate_start']
    if key not in seen:
        seen.add(key)
        unique.append(c)

# Show top 30
print('\nTop 30 unique score-6+ candidates:')
for c in unique[:30]:
    print('  ' + c['candidate_start'] + ' | Score: ' + str(c['score']) + ' | Start: ' + c['start_byte'] + ' | Region: ' + c['region'])

# Summary
print('\n--- Summary by Score ---')
for score in [9, 8, 7, 6]:
    count = len([c for c in unique if c['score'] == score])
    items = [c['candidate_start'] for c in unique if c['score'] == score]
    print('Score-' + str(score) + ': ' + str(count) + ' candidates')
    for i in items[:10]:
        print('  - ' + i)

# Save
Path('reports/d4_score6_candidates.json').write_text(json.dumps(unique, indent=2))
print('\nSaved to reports/d4_score6_candidates.json')
