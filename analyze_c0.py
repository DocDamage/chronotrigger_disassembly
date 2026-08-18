import os
import re
import json

# Check the JSON manifests for C0
c0_manifests = []
labels_dir = 'labels'

def parse_address(addr_str):
    """Parse address string like 'C0:0887' to integer"""
    if isinstance(addr_str, int):
        return addr_str
    if ':' in addr_str:
        parts = addr_str.split(':')
        return int(parts[1], 16)
    return int(addr_str, 0)

def get_size(data):
    """Get size from manifest, defaulting to 25"""
    size = data.get('size', 0)
    if size:
        return size
    # Estimate from end_addr - org
    org = data.get('org', 0)
    end = data.get('end_addr', 0)
    if org and end:
        return int(end, 0) - int(org, 0)
    return 25  # default

# Search all subdirectories for JSON manifests
for root, dirs, files in os.walk(labels_dir):
    for f in files:
        if f.endswith('.json') and 'C0' in f.upper():
            path = os.path.join(root, f)
            try:
                with open(path, 'r') as file:
                    data = json.load(file)
                
                # Check if it's a C0 manifest
                addr_str = data.get('address', '')
                bank = data.get('bank', '')
                
                is_c0 = False
                org = 0
                
                if addr_str and 'C0:' in addr_str.upper():
                    is_c0 = True
                    org = parse_address(addr_str)
                elif bank == 'C0':
                    is_c0 = True
                    org = int(data.get('org', '0'), 0) if isinstance(data.get('org'), str) else data.get('org', 0)
                
                if is_c0:
                    size = get_size(data)
                    end = org + size
                    c0_manifests.append({
                        'org': org,
                        'end': end,
                        'size': size,
                        'name': f,
                        'score': data.get('score', 0),
                        'type': data.get('type', 'unknown'),
                        'path': path
                    })
            except Exception as e:
                pass

# Also check passes/manifests
passes_dir = 'passes/manifests'
for f in os.listdir(passes_dir):
    if f.endswith('.json'):
        path = os.path.join(passes_dir, f)
        try:
            with open(path, 'r') as file:
                data = json.load(file)
            
            if isinstance(data, dict):
                bank = data.get('bank', '')
                if bank == 'C0':
                    org = int(data.get('org', '0'), 0) if isinstance(data.get('org'), str) else data.get('org', 0)
                    size = get_size(data)
                    end = org + size
                    c0_manifests.append({
                        'org': org,
                        'end': end,
                        'size': size,
                        'name': f,
                        'score': data.get('score', 0),
                        'type': data.get('type', 'unknown'),
                        'path': path
                    })
        except Exception as e:
            pass

# Remove duplicates based on org address
seen_orgs = {}
unique_manifests = []
for m in c0_manifests:
    if m['org'] not in seen_orgs:
        seen_orgs[m['org']] = m
        unique_manifests.append(m)

c0_manifests = unique_manifests

# Sort by address
c0_manifests.sort(key=lambda x: x['org'])

# Calculate total coverage
total_bytes = sum(m['size'] for m in c0_manifests)
print(f'C0 JSON manifests: {len(c0_manifests)}')
print(f'Total bytes from manifests: {total_bytes}')
print(f'Coverage %: {total_bytes / 65536 * 100:.2f}%')
print(f'Target 20%: {int(65536 * 0.20)} bytes')
print(f'Gap to close: {int(65536 * 0.20) - total_bytes} bytes')

# Show top 15 largest manifests
print('\nTop 15 largest C0 manifests:')
sorted_by_size = sorted(c0_manifests, key=lambda x: x['size'], reverse=True)
for m in sorted_by_size[:15]:
    print(f"  C0:{m['org']:04X}-{m['end']:04X}: {m['size']} bytes (score {m['score']}) - {m['name'][:50]}")

# Show score distribution
score_dist = {}
for m in c0_manifests:
    score = m['score']
    score_dist[score] = score_dist.get(score, 0) + 1
print(f'\nScore distribution:')
for score in sorted(score_dist.keys(), reverse=True):
    print(f'  Score {score}: {score_dist[score]} manifests')

# Find gaps in key regions
print('\n\nGap analysis for target regions:')
key_regions = [(0x4000, 0x4100), (0x5B96, 0x60AA), (0x60AC, 0x6EF8)]

for region_start, region_end in key_regions:
    print(f'\nRegion C0:{region_start:04X}-{region_end:04X}:')
    region_covered = set()
    for m in c0_manifests:
        start = m['org']
        end = m['end']
        if start < region_end and end > region_start:
            overlap_start = max(start, region_start)
            overlap_end = min(end, region_end)
            for i in range(overlap_start, overlap_end):
                region_covered.add(i)
    
    covered_in_region = len(region_covered)
    total_region = region_end - region_start
    if total_region > 0:
        print(f'  Covered: {covered_in_region}/{total_region} bytes ({covered_in_region/total_region*100:.1f}%)')
    
    # Find gaps
    gaps = []
    gap_start = None
    for i in range(region_start, region_end):
        if i not in region_covered:
            if gap_start is None:
                gap_start = i
        else:
            if gap_start is not None:
                gaps.append((gap_start, i))
                gap_start = None
    if gap_start is not None:
        gaps.append((gap_start, region_end))
    
    if gaps:
        print(f'  Gaps ({len(gaps)}):')
        for gstart, gend in gaps[:10]:
            print(f'    C0:{gstart:04X}-{gend:04X} ({gend-gstart} bytes)')

# List all manifests in target regions
print('\n\nManifests in target regions:')
for region_start, region_end in key_regions:
    print(f'\nC0:{region_start:04X}-{region_end:04X}:')
    region_manifests = [m for m in c0_manifests if m['org'] >= region_start and m['org'] < region_end]
    if region_manifests:
        for m in sorted(region_manifests, key=lambda x: x['org']):
            print(f"  C0:{m['org']:04X}-{m['end']:04X}: {m['size']} bytes (score {m['score']})")
    else:
        print('  No manifests in this region')

# Also count manifests by region
print('\n\nManifests by region:')
all_regions = [
    ('0000-1000', 0x0000, 0x1000),
    ('1000-2000', 0x1000, 0x2000),
    ('2000-3000', 0x2000, 0x3000),
    ('3000-4000', 0x3000, 0x4000),
    ('4000-5000', 0x4000, 0x5000),
    ('5000-6000', 0x5000, 0x6000),
    ('6000-7000', 0x6000, 0x7000),
    ('7000-8000', 0x7000, 0x8000),
    ('8000-9000', 0x8000, 0x9000),
    ('9000-A000', 0x9000, 0xA000),
    ('A000-B000', 0xA000, 0xB000),
    ('B000-C000', 0xB000, 0xC000),
    ('C000-D000', 0xC000, 0xD000),
    ('D000-E000', 0xD000, 0xE000),
    ('E000-F000', 0xE000, 0xF000),
]

for name, rstart, rend in all_regions:
    count = len([m for m in c0_manifests if m['org'] >= rstart and m['org'] < rend])
    bytes_in_region = sum(m['size'] for m in c0_manifests if m['org'] >= rstart and m['org'] < rend)
    print(f'  {name}: {count} manifests, {bytes_in_region} bytes')
