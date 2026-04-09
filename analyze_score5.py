#!/usr/bin/env python3
import json
import os

# Load the backtrack data for score-5 candidates
with open('c4_backtrack_full.json', 'rb') as f:
    raw = f.read()
    
# Handle UTF-16 LE encoding
if raw[:2] == b'\xff\xfe':
    content = raw[2:].decode('utf-16-le', errors='ignore')
elif raw[:3] == b'\xef\xbb\xbf':
    content = raw[3:].decode('utf-8', errors='ignore')
else:
    content = raw.decode('utf-8', errors='ignore')

data = json.loads(content)

candidates = data.get('candidates', [])

# Get score-5 candidates
score_5 = [c for c in candidates if c.get('score', 0) == 5]

# Get already documented addresses
documented = set()
for root, dirs, files in os.walk('passes'):
    for fname in files:
        if fname.startswith('pass') and fname.endswith('.json'):
            path = os.path.join(root, fname)
            try:
                with open(path) as f:
                    m = json.load(f)
                    start = m.get('start', '')
                    if start.startswith('C4:'):
                        documented.add(start)
            except:
                pass

# Filter new score-5 candidates
new_5 = [c for c in score_5 if c.get('candidate_start') not in documented]

print(f'Score-5 candidates: {len(score_5)}')
print(f'New score-5 candidates: {len(new_5)}')

# Show top score-5 by region diversity
def get_region(addr):
    parts = addr.split(':')
    if len(parts) == 2:
        bank = parts[0]
        offset = int(parts[1], 16)
        region = (offset // 0x1000) * 0x1000
        return f"{bank}:{region:04X}"
    return "unknown"

# Group by region
regions = {}
for c in new_5:
    region = get_region(c.get('candidate_start', ''))
    if region not in regions:
        regions[region] = []
    regions[region].append(c)

print('\nScore-5 by region:')
for region in sorted(regions.keys()):
    print(f'  {region}: {len(regions[region])} candidates')

# Select score-5 candidates from underrepresented regions
target_regions = ['C4:2000', 'C4:3000', 'C4:4000', 'C4:5000', 'C4:9000', 'C4:A000', 'C4:B000', 'C4:C000', 'C4:E000', 'C4:F000']
selected_5 = []
for region in target_regions:
    if region in regions and regions[region]:
        selected_5.append(regions[region][0])

print(f'\nSelected {len(selected_5)} score-5 candidates for expansion:')
for c in selected_5[:10]:
    addr = c.get('candidate_start', '')
    target = c.get('target', '')
    region = get_region(addr)
    start_byte = c.get('start_byte', '')
    print(f'  {addr} -> {target} (byte={start_byte}) [{region}]')

# Save for manifest creation
with open('c4_score5_candidates.json', 'w') as f:
    json.dump(selected_5[:10], f, indent=2)
print(f'\nSaved {min(10, len(selected_5))} candidates to c4_score5_candidates.json')
