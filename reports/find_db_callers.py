#!/usr/bin/env python3
"""Find all cross-bank callers targeting Bank DB."""
import sys
sys.path.insert(0, 'tools/scripts')

from pathlib import Path
from manifest_xref_utils import iter_raw_callers

def main():
    rom_bytes = Path('rom/Chrono Trigger (USA).sfc').read_bytes()
    
    db_callers = []
    for item in iter_raw_callers(rom_bytes):
        if item['kind'] in ('JSL', 'JML') and item['target_bank'] == 0xDB:
            db_callers.append(item)
    
    # Group by target
    from collections import defaultdict
    by_target = defaultdict(list)
    for item in db_callers:
        by_target[item['target']].append(item)
    
    print(f"Found {len(db_callers)} cross-bank calls to Bank DB")
    print(f"Targeting {len(by_target)} unique addresses")
    print()
    print("Top targets by caller count:")
    sorted_targets = sorted(by_target.items(), key=lambda x: -len(x[1]))
    for target, callers in sorted_targets[:30]:
        print(f"  {target}: {len(callers)} callers")
        for c in callers[:3]:
            print(f"    from {c['caller']} ({c['kind']})")
        if len(callers) > 3:
            print(f"    ... and {len(callers)-3} more")
    
    # Save full results
    import json
    with open('reports/db_cross_bank_callers.json', 'w') as f:
        json.dump({
            'total_calls': len(db_callers),
            'unique_targets': len(by_target),
            'targets': {t: [{'caller': c['caller'], 'kind': c['kind']} for c in callers] 
                       for t, callers in sorted_targets}
        }, f, indent=2)
    print()
    print("Full results saved to reports/db_cross_bank_callers.json")

if __name__ == '__main__':
    main()
