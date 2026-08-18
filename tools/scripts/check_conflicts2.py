import json, glob, os

# Proposed new ranges (using next pass numbers 510-515)
new_ranges = [
    ('pass510', 'C0:CB35..C0:CB58'),
    ('pass511', 'C0:8D7E..C0:8DA1'),
    ('pass512', 'C0:67D7..C0:67FA'),
    ('pass513', 'C0:679D..C0:67C0'),
    ('pass514', 'C0:690F..C0:6932'),
    ('pass515', 'C0:B309..C0:B32C'),
]

def parse_range(r):
    start, end = r.split('..')
    bank1, addr1 = start.split(':')
    bank2, addr2 = end.split(':')
    return (int(addr1, 16), int(addr2, 16))

def overlap(r1, r2):
    s1, e1 = parse_range(r1)
    s2, e2 = parse_range(r2)
    return not (e1 < s2 or e2 < s1)

# Load all existing passes
existing = []
for mf in glob.glob('../../passes/manifests/pass*.json'):
    try:
        with open(mf) as f:
            data = json.load(f)
        for r in data.get('closed_ranges', []):
            existing.append((os.path.basename(mf), r['range']))
    except:
        pass

print("Checking for overlaps...")
for name, new_r in new_ranges:
    conflicts = []
    for existing_name, existing_r in existing:
        if overlap(new_r, existing_r):
            conflicts.append(f"  {existing_name}: {existing_r}")
    if conflicts:
        print(f"{name} ({new_r}):")
        for c in conflicts:
            print(c)
    else:
        print(f"{name} ({new_r}): NO CONFLICTS")
