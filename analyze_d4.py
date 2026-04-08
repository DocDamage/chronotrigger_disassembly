#!/usr/bin/env python3
import json

# Process all backtrack files
files = {
    '0000-4000': 'reports/d4_0000_4000_backtrack.json',
    '6000-8000': 'reports/d4_6000_8000_backtrack.json', 
    '8000-C000': 'reports/d4_8000_c000_backtrack.json',
    'C000-FFFF': 'reports/d4_c000_ffff_backtrack.json',
    '4000-6000': 'reports/d4_4000_5fff_backtrack.json'
}

all_candidates = []
for region, path in files.items():
    try:
        with open(path) as f:
            data = json.load(f)
        for c in data.get('candidates', []):
            c['region'] = region
            all_candidates.append(c)
    except Exception as e:
        print(f"Error loading {path}: {e}")

# Filter for score-6+ and dedupe by candidate_start
seen = set()
unique = []
for c in sorted(all_candidates, key=lambda x: (-x['score'], x['candidate_start'])):
    key = c['candidate_start']
    if key not in seen:
        seen.add(key)
        unique.append(c)

# Show top 30
print("Top 30 unique score-6+ candidates:")
for c in unique[:30]:
    print(f"{c['candidate_start']} | Score: {c['score']} | Start: {c['start_byte']} | Region: {c['region']} | ASCII: {c['ascii_ratio']}")

# Summary by score
print("\n--- Summary ---")
for score in [9, 8, 7, 6]:
    count = len([c for c in unique if c['score'] == score])
    print(f"Score-{score}: {count} candidates")

# Save detailed list
with open('reports/d4_score6_candidates.json', 'w') as f:
    json.dump(unique, f, indent=2)
print("\nSaved to reports/d4_score6_candidates.json")
