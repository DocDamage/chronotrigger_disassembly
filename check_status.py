#!/usr/bin/env python3
import json

# Load all candidates
with open('c1_session29_candidates.json') as f:
    candidates = json.load(f)

# Check which were processed
with open('c1_all_candidates.json') as f:
    all_data = json.load(f)
    processed = set(all_data['processed'])

# Check which candidates are in the selection
for c in candidates:
    addr = c['addr']
    status = 'PROCESSED' if addr in processed else 'NEW'
    print(f"{addr} - {status} - score {c['score']}")

print()
print(f"Candidates in list: {len(candidates)}")
new_count = len([c for c in candidates if c['addr'] not in processed])
proc_count = len([c for c in candidates if c['addr'] in processed])
print(f"Already processed: {proc_count}")
print(f"New: {new_count}")

# Get additional candidates to fill to 12
remaining = []
for c in all_data['remaining']:
    if c['addr'] not in processed and c['addr'] not in [x['addr'] for x in candidates]:
        remaining.append(c)

remaining.sort(key=lambda x: (-x['score'], x['addr']))
print(f"\nAdditional candidates available: {len(remaining)}")
for c in remaining[:5]:
    print(f"  {c['addr']} - score {c['score']} - {c['width']} bytes")
