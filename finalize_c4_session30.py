#!/usr/bin/env python3
"""Finalize Session 30 manifests for Bank C4"""

import json
import os

# Load the backtrack data
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

print(f'Already documented: {len(documented)}')

# Get new score-6 candidates
score_6 = [c for c in candidates if c.get('score', 0) == 6 and c.get('candidate_start') not in documented]

# Get new score-5 candidates  
score_5 = [c for c in candidates if c.get('score', 0) == 5 and c.get('candidate_start') not in documented]

print(f'New score-6: {len(score_6)}')
print(f'New score-5: {len(score_5)}')

# Show what's available
print('\n=== Score-6 by region ===')
def get_region(addr):
    parts = addr.split(':')
    if len(parts) == 2:
        offset = int(parts[1], 16)
        return f"C4:{(offset // 0x1000) * 0x1000:04X}"
    return "unknown"

regions_6 = {}
for c in score_6:
    region = get_region(c.get('candidate_start', ''))
    if region not in regions_6:
        regions_6[region] = []
    regions_6[region].append(c)

for region in sorted(regions_6.keys()):
    print(f'  {region}: {len(regions_6[region])} candidates')

# Select 8 score-6 and 4 score-5 for diversity
selected = []

# Pick score-6 candidates from diverse regions
regions_with_6 = list(regions_6.keys())
for i in range(min(8, len(score_6))):
    selected.append(score_6[i])

# Pick score-5 candidates from diverse regions
for i in range(min(4, len(score_5))):
    selected.append(score_5[i])

print(f'\nSelected {len(selected)} candidates for Session 30')

# Create manifests
manifests = []
start_pass = 758

prologue_names = {
    '20': 'jsr_handler',
    '22': 'jsl_handler', 
    '08': 'php_handler',
    'A0': 'ldy_init',
    'A2': 'ldx_init',
    '8B': 'phb_handler',
    '4B': 'phk_handler',
    'C2': 'rep_handler',
    '48': 'pha_handler',
    '0B': 'phd_handler'
}

for i, c in enumerate(selected):
    addr = c.get('candidate_start', '')
    target = c.get('target', '')
    score = c.get('score', 0)
    start_byte = c.get('start_byte', '')
    candidate_range = c.get('candidate_range', '')
    
    parts = addr.split(':')
    if len(parts) == 2:
        bank = parts[0]
        offset = int(parts[1], 16)
        
        # Calculate size
        if '..' in candidate_range:
            range_parts = candidate_range.split('..')
            if len(range_parts) == 2:
                try:
                    start = int(range_parts[0].split(':')[1], 16)
                    end = int(range_parts[1].split(':')[1], 16)
                    size = end - start
                except:
                    size = 25
            else:
                size = 25
        else:
            size = 25
        
        size = max(size, 15)
        end_offset = offset + size
        
        suffix = prologue_names.get(start_byte, f'byte{start_byte}_handler')
        label = f"ct_c4_{offset:04x}_{suffix}_s30"
        
        manifest = {
            "pass": start_pass + i,
            "label": label,
            "bank": bank,
            "start": addr,
            "end": f"{bank}:{end_offset:04X}",
            "score": score,
            "target": target,
            "start_byte": start_byte,
            "size": size,
            "session": 30,
            "region": get_region(addr),
            "promotion_reason": f"Score-{score} candidate, {suffix.replace('_', ' ')} prologue"
        }
        manifests.append(manifest)

# Save manifests
output_dir = 'passes/session30_c4'
os.makedirs(output_dir, exist_ok=True)

# Clear old manifests
for f in os.listdir(output_dir):
    if f.endswith('.json'):
        os.remove(os.path.join(output_dir, f))

for m in manifests:
    fname = f"{output_dir}/pass{m['pass']:04d}.json"
    with open(fname, 'w') as f:
        json.dump(m, f, indent=2)

with open(f'{output_dir}/c4_session30_manifests.json', 'w') as f:
    json.dump(manifests, f, indent=2)

print(f'\n=== Created {len(manifests)} manifests ===')
for m in manifests:
    print(f"  Pass {m['pass']}: {m['start']}..{m['end']} ({m['size']} bytes, score={m['score']})")

# Calculate totals
total_new_bytes = sum(m['size'] for m in manifests)
score_6_count = len([m for m in manifests if m['score'] == 6])
score_5_count = len([m for m in manifests if m['score'] == 5])

print(f'\nTotal new bytes: {total_new_bytes}')
print(f'Score-6: {score_6_count}, Score-5: {score_5_count}')
print(f'Estimated coverage increase: +{total_new_bytes/655.36:.2f}%')
