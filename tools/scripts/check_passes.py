import json, sys
for pass_num in sys.argv[1:]:
    try:
        with open(f'../../passes/manifests/pass{pass_num}.json') as f:
            p = json.load(f)
        print(f'Pass {pass_num} ranges:')
        for r in p['closed_ranges']:
            label = r.get('label', 'no label')
            print(f"  {r['range']} - {label}")
    except Exception as e:
        print(f"Pass {pass_num}: {e}")
