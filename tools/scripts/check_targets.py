import json

# From scan results - extract backtrack data for targets
targets = {
    'C0:A9CD': {'callers': 8, 'backtrack_start': 'C0:A9C1', 'score': 6},
    'C0:AA7F': {'callers': 39, 'backtrack_start': 'C0:AA6F', 'score': 4, 'strength': 'invalid'},
    'C0:ABA2': {'callers': 11, 'backtrack_start': 'C0:ABA0', 'score': 6},
}

for addr, info in targets.items():
    print(f"{addr}: {info['callers']} callers, start={info.get('backtrack_start', 'unknown')}, score={info.get('score', '?')}, strength={info.get('strength', 'weak')}")
    
    # Calculate range
    bank, start = addr.split(':')
    start_int = int(start, 16)
    
    # For boundary, use backtrack or target
    if 'backtrack_start' in info:
        bt_bank, bt_start = info['backtrack_start'].split(':')
        start_int = int(bt_start, 16)
    
    # Estimate end (assume ~30-50 bytes for functions with these caller counts)
    if info.get('strength') == 'invalid':
        end_int = start_int + 15  # Data table entries are short
    else:
        end_int = start_int + 35  # Regular function
    
    print(f"  Proposed range: C0:{start_int:04X}..C0:{end_int:04X}")
    print()
