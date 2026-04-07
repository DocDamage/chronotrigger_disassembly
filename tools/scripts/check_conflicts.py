import json, glob, os

# Proposed new ranges
new_ranges = [
    ('pass508', 'C0:A9C1..C0:A9E4'),
    ('pass509', 'C0:AA6F..C0:AA7E'),
    ('pass510', 'C0:ABA0..C0:ABC3'),
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
