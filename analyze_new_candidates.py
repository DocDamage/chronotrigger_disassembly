#!/usr/bin/env python3
import json
from pathlib import Path

# Get all D4 manifests
existing_ranges = []
for f in Path('passes/manifests').glob('pass*.json'):
    try:
        data = json.loads(f.read_text())
        for r in data.get('closed_ranges', []):
            rng = r.get('range', '')
            if rng.startswith('D4:'):
                # Parse range
                parts = rng.replace('..', ':').split(':')
                if len(parts) >= 4:
                    bank = int(parts[0], 16)
                    start = int(parts[1], 16)
                    end = int(parts[2] if parts[2] else parts[3], 16)
                    existing_ranges.append((start, end, f.name, rng))
    except Exception as e:
        pass

print('Existing D4 ranges:')
for start, end, fname, rng in sorted(existing_ranges):
    print('  D4:{:04X}..D4:{:04X} ({})'.format(start, end, fname))

# Load new candidates
candidates = json.loads(Path('reports/d4_score6_candidates.json').read_text())
print('\nNew candidates found: ' + str(len(candidates)))

# Filter candidates that don't overlap with existing ranges
def overlaps_existing(start, end):
    for es, ee, _, _ in existing_ranges:
        if not (end < es or start > ee):  # Overlaps
            return True
    return False

new_candidates = []
for c in candidates:
    parts = c['candidate_start'].split(':')
    addr = int(parts[1], 16)
    # Estimate end based on candidate_range
    cr = c.get('candidate_range', '')
    cp = cr.replace('..', ':').split(':')
    if len(cp) >= 4:
        end = int(cp[3], 16) if cp[3] else addr + 32
    else:
        end = addr + 32
    if not overlaps_existing(addr, end):
        new_candidates.append(c)

print('Candidates not overlapping with existing: ' + str(len(new_candidates)))
print('\nTop 20 new candidates:')
for c in new_candidates[:20]:
    print('  ' + c['candidate_start'] + ' | Score: ' + str(c['score']) + ' | Start: ' + c['start_byte'] + ' | Region: ' + c['region'])

# Save new candidates list
Path('reports/d4_new_candidates.json').write_text(json.dumps(new_candidates, indent=2))
print('\nSaved to reports/d4_new_candidates.json')
