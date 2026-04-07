import json, glob, os

manifests_dir = '../../passes/manifests/'

# Targets worth promoting (2+ callers)
targets = [
    ('C0:14BD', 4, 'C0:14AD', 'weak', 2),   # 4 callers
    ('C0:14AD', 2, 'C0:14A4', 'weak', 4),   # 2 callers  
    ('C0:D6A7', 2, 'C0:D6A1', 'weak', 2),   # 2 callers
    ('C0:1220', 2, 'C0:1219', 'weak', 4),   # 2 callers
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
            for t, _, _, _, _ in targets:
                if in_range(t, r['range']):
                    covered[t].append((os.path.basename(mf), r['range']))
    except:
        pass

print("Target coverage check:")
for t, callers, start, strength, score in targets:
    if covered[t]:
        print(f"  {t} ({callers} callers): COVERED by {covered[t]}")
    else:
        print(f"  {t} ({callers} callers): NOT COVERED - PROMOTE!")
        bank, addr = start.split(':')
        start_int = int(addr, 16)
        end_int = start_int + 35
        print(f"    Proposed: {start}..C0:{end_int:04X}")
