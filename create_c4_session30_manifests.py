#!/usr/bin/env python3
"""Create Session 30 manifests for Bank C4"""

import json
import os

# Read the candidates
with open('c4_session30_candidates.json') as f:
    candidates = json.load(f)

# Filter out already documented candidates
documented_starts = set()
for root, dirs, files in os.walk('passes'):
    for fname in files:
        if fname.startswith('pass') and fname.endswith('.json'):
            path = os.path.join(root, fname)
            try:
                with open(path) as f:
                    m = json.load(f)
                    start = m.get('start', '')
                    if start.startswith('C4:'):
                        documented_starts.add(start)
            except:
                pass

# Filter candidates - remove duplicates by address
seen_addrs = set()
unique_candidates = []
for c in candidates:
    addr = c.get('candidate_start', '')
    if addr not in seen_addrs and addr not in documented_starts:
        seen_addrs.add(addr)
        unique_candidates.append(c)

# Group by region
def get_region(addr):
    parts = addr.split(':')
    if len(parts) == 2:
        bank = parts[0]
        offset = int(parts[1], 16)
        region = (offset // 0x1000) * 0x1000
        return f"{bank}:{region:04X}"
    return "unknown"

regions = {}
for c in unique_candidates:
    region = get_region(c.get('candidate_start', ''))
    if region not in regions:
        regions[region] = []
    regions[region].append(c)

print("Candidates by region:")
for region in sorted(regions.keys()):
    print(f"  {region}: {len(regions[region])} candidates")

# Select top candidates - prioritize by region diversity and prologue type
prologue_priority = {'20': 5, '22': 5, '08': 4, 'A0': 3, 'A2': 3, '8B': 3, '4B': 3, 'C2': 3}

for c in unique_candidates:
    score = c.get('score', 0)
    start_byte = c.get('start_byte', '')
    region = get_region(c.get('candidate_start', ''))
    
    # Calculate priority score
    priority = score * 10
    priority += prologue_priority.get(start_byte, 0)
    
    # Boost underrepresented regions
    region_count = len(regions.get(region, []))
    if region_count < 5:
        priority += 10
    
    c['priority'] = priority

# Sort by priority
unique_candidates.sort(key=lambda x: x.get('priority', 0), reverse=True)

# Select top 12 with region diversity
selected = []
used_regions = set()
for c in unique_candidates:
    region = get_region(c.get('candidate_start', ''))
    if len(selected) < 12:
        selected.append(c)
        used_regions.add(region)

print(f"\n=== Selected {len(selected)} candidates for Session 30 ===")
for c in selected:
    addr = c.get('candidate_start', '')
    target = c.get('target', '')
    score = c.get('score', 0)
    start_byte = c.get('start_byte', '')
    priority = c.get('priority', 0)
    print(f"  {addr} -> {target} (score={score}, byte={start_byte}, prio={priority})")

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
    '48': 'pha_handler'
}

for i, c in enumerate(selected):
    addr = c.get('candidate_start', '')
    target = c.get('target', '')
    score = c.get('score', 0)
    start_byte = c.get('start_byte', '')
    candidate_range = c.get('candidate_range', '')
    
    # Parse address
    parts = addr.split(':')
    if len(parts) == 2:
        bank = parts[0]
        offset = int(parts[1], 16)
        
        # Estimate size from candidate_range or use default
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
        
        # Ensure minimum size
        size = max(size, 15)
        end_offset = offset + size
        
        # Create label
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

for m in manifests:
    fname = f"{output_dir}/pass{m['pass']:04d}.json"
    with open(fname, 'w') as f:
        json.dump(m, f, indent=2)

# Also create combined file
with open(f'{output_dir}/c4_session30_manifests.json', 'w') as f:
    json.dump(manifests, f, indent=2)

print(f"\n=== Created {len(manifests)} manifests ===")
for m in manifests:
    print(f"  Pass {m['pass']}: {m['start']}..{m['end']} ({m['size']} bytes, score={m['score']})")

# Calculate coverage increase
total_new_bytes = sum(m['size'] for m in manifests)
print(f"\nTotal new bytes: {total_new_bytes}")
print(f"Estimated coverage increase: +{total_new_bytes/655.36:.2f}%")

# Region breakdown
print("\nRegion breakdown:")
region_bytes = {}
for m in manifests:
    r = m['region']
    if r not in region_bytes:
        region_bytes[r] = 0
    region_bytes[r] += m['size']
for r in sorted(region_bytes.keys()):
    print(f"  {r}: {region_bytes[r]} bytes")
