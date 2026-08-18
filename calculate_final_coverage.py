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

print(f'========================================')
print(f'  BANK C3 FINAL COVERAGE REPORT')
print(f'========================================')
print(f'')
print(f'C3 manifests found: {len(c3_manifests)}')
print(f'Current documented bytes: {current}')
print(f'Current coverage: {percent:.2f}%')
print(f'')
print(f'Target for 30%: {needed_30} bytes')
print(f'Gap to 30%: {gap} bytes')
print(f'')

if percent >= 30.0:
    print(f'*** SUCCESS! 30% MILESTONE ACHIEVED! ***')
    print(f'   Coverage: {percent:.2f}% (Target: 30.00%)')
    print(f'   Exceeded by: {current - needed_30} bytes')
else:
    print(f'Progress toward 30%:')
    print(f'   Current: {percent:.2f}%')
    print(f'   Remaining: {gap} bytes')

print(f'')
print(f'========================================')
print(f'  Session 28 Manifests (pass992-1005)')
print(f'========================================')

session_28_manifests = [m for m in c3_manifests if 'session28' in m[0]]
print(f'New manifests created: {len(session_28_manifests)}')
for m in sorted(session_28_manifests, key=lambda x: x[1]):
    size = m[2] - m[1] + 1
    print(f'  {m[0]}: C3:{m[1]:04X}..C3:{m[2]:04X} ({size} bytes)')

# Calculate coverage by region
regions = [
    ('0000-1FFF', 0x0000, 0x1FFF),
    ('2000-3FFF', 0x2000, 0x3FFF),
    ('4000-5FFF', 0x4000, 0x5FFF),
    ('6000-7FFF', 0x6000, 0x7FFF),
    ('8000-9FFF', 0x8000, 0x9FFF),
    ('A000-BFFF', 0xA000, 0xBFFF),
    ('C000-DFFF', 0xC000, 0xDFFF),
    ('E000-FFFF', 0xE000, 0xFFFF),
]

print(f'')
print(f'========================================')
print(f'  Coverage by Region')
print(f'========================================')
for name, start, end in regions:
    region_bytes = set(i for i in c3_bytes if start <= i <= end)
    region_size = end - start + 1
    region_percent = (len(region_bytes) / region_size) * 100
    print(f'  C3:{name}: {len(region_bytes):5d} bytes ({region_percent:5.2f}%)')

print(f'')
print(f'========================================')
