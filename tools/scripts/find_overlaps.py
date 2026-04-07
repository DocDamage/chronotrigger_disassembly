import json, glob, os

def find_passes_with_range(addr):
    results = []
    for mf in glob.glob('../../passes/manifests/pass*.json'):
        try:
            with open(mf) as f:
                data = json.load(f)
            for r in data.get('closed_ranges', []):
                if addr in r['range']:
                    results.append((os.path.basename(mf), r['range'], r.get('label', 'no label')))
        except:
            pass
    return results

for addr in ['75E7', '74C7', '919F']:
    print(f"\nSearching for {addr}:")
    results = find_passes_with_range(addr)
    for r in results:
        print(f"  {r[0]}: {r[1]} - {r[2]}")
