import json, glob, os

# Proposed new ranges
new_ranges = [
    ('pass516', 'C0:14AD..C0:14D0'),
    ('pass517', 'C0:14A4..C0:14C7'),
    ('pass518', 'C0:D6A1..C0:D6C4'),
    ('pass519', 'C0:1219..C0:123C'),
]

def parse_range(r):
    start, end = r.split('..')
    bank1, addr1 = start.split(':')
    bank2, addr2 = end.split(':')
    return (bank1, int(addr1, 16), int(addr2, 16))

def overlap(r1, r2):
    b1, s1, e1 = parse_range(r1)
    b2, s2, e2 = parse_range(r2)
    if b1 != b2:
        return False  # Different banks don't overlap
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
