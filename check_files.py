import json
import os

files = [
    'c4_s26_candidates.json',
    'c4_7000_8000_top_candidates.json',
    'c4_islands_4000.json',
    'c4_islands_c000.json',
    'c4_4000_5000_scan_session21.json',
    'c4_5000_6000_scan_session21.json',
    'c4_6000_7000_scan_session21.json',
    'c4_7000_8000_scan_session21.json'
]

for f in files:
    if os.path.exists(f):
        size = os.path.getsize(f)
        print(f'{f}: {size} bytes')
        if size > 0:
            try:
                with open(f) as file:
                    data = json.load(file)
                    if isinstance(data, list):
                        print(f'  -> List with {len(data)} items')
                    elif isinstance(data, dict):
                        print(f'  -> Dict with keys: {list(data.keys())[:5]}')
            except Exception as e:
                print(f'  -> Error: {e}')
        else:
            print('  -> EMPTY FILE')
    else:
        print(f'{f}: MISSING')
