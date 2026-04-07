# Extract backtrack data from scan results
targets = {
    'C0:CB3A': {'callers': 4, 'backtrack': 'C0:CB35', 'score': 2},
    'C0:8D7F': {'callers': 9, 'backtrack': 'C0:8D7E', 'score': 4},
    'C0:67E3': {'callers': 4, 'backtrack': 'C0:67D7', 'score': 6},
    'C0:67A2': {'callers': 2, 'backtrack': 'C0:679D', 'score': 4},
    'C0:6918': {'callers': 2, 'backtrack': 'C0:690F', 'score': 4},
    'C0:B309': {'callers': 2, 'backtrack': 'C0:B309', 'score': 5},
}

for addr, info in targets.items():
    bank, start = info['backtrack'].split(':')
    start_int = int(start, 16)
    end_int = start_int + 35  # Estimate ~35 bytes per function
    print(f"{addr}: {info['backtrack']}..C0:{end_int:04X} ({info['callers']} callers, score {info['score']})")
