import json, glob, os

manifests_dir = '../../passes/manifests/'
targets = [
    ('C0:CB3A', 4), ('C0:CBAD', 2), ('C0:8D7F', 9), ('C0:67E3', 4),
    ('C0:67A2', 2), ('C0:6918', 2), ('C0:B309', 2), ('C0:B3A6', 1)
]

def addr_to_int(a):
    bank, addr = a.split(':')
    return int(bank, 16) * 0x10000 + int(addr, 16)

def in_range(target, range_str):
    t = addr_to_int(target)
    start, end = range_str.split('..')
    s = addr_to_int(start)
    e = addr_to_int(end)
    return s <= t <= e

covered = {t[0]: [] for t in targets}

for mf in glob.glob(manifests_dir + 'pass*.json'):
    try:
        with open(mf) as f:
            data = json.load(f)
        for r in data.get('closed_ranges', []):
            for t, _ in targets:
                if in_range(t, r['range']):
                    covered[t].append((os.path.basename(mf), r['range']))
    except:
        pass

print("Target coverage check:")
for t, callers in targets:
    if covered[t]:
        print(f"  {t} ({callers} callers): COVERED by {covered[t]}")
    else:
        print(f"  {t} ({callers} callers): NOT COVERED - PROMOTE!")
