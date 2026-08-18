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

documented_addrs = set(start for f, start, end in c3_manifests)

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
            
            # Get size from file if possible
            size = 0
            try:
                with open(os.path.join(c3_labels_dir, f)) as fp:
                    content = fp.read()
                    # Try to extract size
                    size_match = re.search(r'Size:\s*(\d+)\s*bytes', content, re.I)
                    if size_match:
                        size = int(size_match.group(1))
                    else:
                        range_match = re.search(r'Range:\s*C3:[0-9A-F]{4}\.\.C3:([0-9A-F]{4})', content, re.I)
                        if range_match:
                            end_addr = int(range_match.group(1), 16)
                            size = end_addr - addr + 1
            except:
                pass
            
            candidates.append((addr, score, f, size))

# Sort by address
candidates.sort()

# Find undocumented candidates
undocumented = [(a, s, f, sz) for a, s, f, sz in candidates if a not in documented_addrs]

print(f'=== Undocumented Score-6+ Candidates: {len(undocumented)} ===')
total_bytes = 0
for a, s, f, sz in undocumented:
    total_bytes += sz
    print(f"  C3:{a:04X} - score {s} - {sz} bytes - {f}")

print(f"\nTotal undocumented bytes: {total_bytes}")

# Current coverage
total_c3 = 65536
current = len(c3_bytes)
percent = (current / total_c3) * 100

print(f"\nCurrent coverage: {current} bytes ({percent:.2f}%)")
print(f"After documenting all remaining: {current + total_bytes} bytes ({((current + total_bytes)/total_c3)*100:.2f}%)")

# Check for 3700-4300 candidates
region_3700 = [(a, s, f, sz) for a, s, f, sz in candidates if 0x3700 <= a <= 0x4300 and a not in documented_addrs]
print(f"\n=== C3:3700-4300 Region Undocumented: {len(region_3700)} ===")
for a, s, f, sz in region_3700:
    print(f"  C3:{a:04X} - score {s} - {sz} bytes")

# Check flow analysis files for more candidates
print("\n=== Checking flow analysis files ===")
flow_files = [
    'reports/c3_3761_3c7f_flow.json',
    'reports/c3_30b1_34ff_flow.json'
]
for ff in flow_files:
    if os.path.exists(ff):
        print(f"Found: {ff}")
