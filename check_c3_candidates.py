import json
import os
import re

# Calculate current C3 coverage from manifests
manifest_dir = 'passes/manifests'
c3_bytes = set()

c3_manifests = []
for f in os.listdir(manifest_dir):
    if f.endswith('.json'):
        filepath = os.path.join(manifest_dir, f)
        try:
            with open(filepath) as fp:
                data = json.load(fp)
                
                # Check closed_ranges
                if 'closed_ranges' in data and isinstance(data['closed_ranges'], list):
                    for cr in data['closed_ranges']:
                        if isinstance(cr, dict) and 'range' in cr:
                            range_str = cr['range']
                            m = re.match(r'C3:([0-9A-F]{4})\.\.C3:([0-9A-F]{4})', range_str, re.I)
                            if m:
                                start = int(m.group(1), 16)
                                end = int(m.group(2), 16)
                                c3_manifests.append((f, start, end))
                                for i in range(start, end + 1):
                                    c3_bytes.add(i)
                
                # Check start/end address
                if 'start_address' in data and 'end_address' in data:
                    m1 = re.match(r'C3:([0-9A-F]{4})', data['start_address'], re.I)
                    m2 = re.match(r'C3:([0-9A-F]{4})', data['end_address'], re.I)
                    if m1 and m2:
                        start = int(m1.group(1), 16)
                        end = int(m2.group(1), 16)
                        c3_manifests.append((f, start, end))
                        for i in range(start, end + 1):
                            c3_bytes.add(i)
        except Exception as e:
            pass

total_c3 = 65536
current = len(c3_bytes)
percent = (current / total_c3) * 100
needed_30 = int(0.30 * total_c3)
gap = needed_30 - current

print(f'=== C3 Coverage Summary ===')
print(f'C3 manifests found: {len(c3_manifests)}')
print(f'Current documented bytes: {current}')
print(f'Current coverage: {percent:.2f}%')
print(f'Target for 30%: {needed_30} bytes')
print(f'Gap to 30%: {gap} bytes')
print()

# Collect all score-6+ candidates from labels
candidates = []
c3_labels_dir = 'labels/c3_candidates'
for f in os.listdir(c3_labels_dir):
    if 'SCORE' in f.upper() and ('SCORE6' in f.upper() or 'SCORE7' in f.upper() or 'SCORE8' in f.upper()):
        # Extract address from filename
        m = re.search(r'C3[_:]([0-9A-F]{4})', f, re.I)
        if m:
            addr = int(m.group(1), 16)
            # Extract score
            sm = re.search(r'SCORE(\d+)', f, re.I)
            score = int(sm.group(1)) if sm else 6
            candidates.append((addr, score, f))

# Sort by address
candidates.sort()

print(f'=== Score-6+ Candidates ({len(candidates)} total) ===')
for addr, score, fname in candidates[:30]:
    print(f"  C3:{addr:04X} - score {score} - {fname}")

print()

# Find candidates in target regions
region_3700_4300 = [(a, s, f) for a, s, f in candidates if 0x3700 <= a <= 0x4300]
region_6000_6FFF = [(a, s, f) for a, s, f in candidates if 0x6000 <= a <= 0x6FFF]
region_2000_2FFF = [(a, s, f) for a, s, f in candidates if 0x2000 <= a <= 0x2FFF]

print(f'=== Candidates by Region ===')
print(f'C3:3700-4300: {len(region_3700_4300)} candidates')
for a, s, f in region_3700_4300[:10]:
    print(f"  C3:{a:04X} - score {s}")

print(f'\nC3:6000-6FFF: {len(region_6000_6FFF)} candidates')
for a, s, f in region_6000_6FFF[:10]:
    print(f"  C3:{a:04X} - score {s}")

print(f'\nC3:2000-2FFF: {len(region_2000_2FFF)} candidates')
for a, s, f in region_2000_2FFF[:10]:
    print(f"  C3:{a:04X} - score {s}")

print()

# Check which manifests already exist
documented_addrs = set()
for f, start, end in c3_manifests:
    documented_addrs.add(start)

print(f'=== Undocumented Candidates ===')
undocumented = [(a, s, f) for a, s, f in candidates if a not in documented_addrs]
print(f'Total undocumented: {len(undocumented)}')
for a, s, f in undocumented[:20]:
    print(f"  C3:{a:04X} - score {s} - {f}")
