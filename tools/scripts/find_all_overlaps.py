import json, glob, os

def addr_to_int(a):
    bank, addr = a.split(':')
    return int(addr, 16)

def in_range(target, range_str):
    t = addr_to_int(target)
    start, end = range_str.split('..')
    s = addr_to_int(start)
    e = addr_to_int(end)
    return s <= t <= e

# New passes to check
new_passes = [
    ('pass521', 'C0:75E7..C0:760A'),
    ('pass524', 'C0:74C7..C0:74EA'),
    ('pass525', 'C0:919F..C0:91BC'),
]

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

print("Checking new passes for overlaps:")
for name, new_r in new_passes:
    print(f"\n{name} ({new_r}):")
    conflicts = []
    for existing_name, existing_r in existing:
        if existing_name == name + '.json':
            continue
        # Check if same bank
        if new_r.startswith('C0:') and existing_r.startswith('C0:'):
            # Parse ranges
            new_start, new_end = new_r.replace('C0:', '').split('..')
            exist_start, exist_end = existing_r.replace('C0:', '').split('..')
            ns = int(new_start, 16)
            ne = int(new_end, 16)
            es = int(exist_start, 16)
            ee = int(exist_end, 16)
            if not (ne < es or ee < ns):
                conflicts.append(f"  {existing_name}: {existing_r}")
    if conflicts:
        for c in conflicts:
            print(c)
    else:
        print("  NO CONFLICTS")
