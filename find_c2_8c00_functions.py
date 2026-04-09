#!/usr/bin/env python3
"""Find function boundaries in C2:8C00-9000 gaps"""

import json

def hirom_to_file_offset(bank, addr):
    return ((bank & 0x3F) << 16) | addr

with open('rom/Chrono Trigger (USA).sfc', 'rb') as f:
    offset = hirom_to_file_offset(0xC2, 0x8C00)
    f.seek(offset)
    data = bytearray(f.read(0x400))

print("=" * 80)
print("C2:8C00-9000 FUNCTION DISCOVERY (Session 31)")
print("=" * 80)

# Prologues and epilogues
prologues = {0x08: 'PHP', 0x0B: 'PHD', 0x48: 'PHA', 0x5A: 'PHY', 0xDA: 'PHX', 
             0xC2: 'REP', 0xE2: 'SEP', 0x78: 'SEI', 0x8B: 'PHB'}
epilogues = {0x28: 'PLP', 0x2B: 'PLD', 0x68: 'PLA', 0x7A: 'PLY', 0xFA: 'PLX',
             0x60: 'RTS', 0x6B: 'RTL', 0x40: 'RTI', 0xAB: 'PLB'}

def find_calls_in_function(data, start, end):
    """Count JSR/JSL in a function"""
    calls = 0
    i = start
    while i < end - 2:
        if data[i] == 0x20:
            calls += 1
            i += 3
        elif data[i] == 0x22:
            calls += 1
            i += 4
        else:
            i += 1
    return calls

def find_branches_in_function(data, start, end):
    """Count branch instructions"""
    branches = 0
    branch_ops = {0x10, 0x30, 0x50, 0x70, 0x90, 0xB0, 0xD0, 0xF0, 0x80}  # BPL, BMI, BVC, BVS, BCC, BCS, BNE, BEQ, BRA
    for i in range(start, end):
        if data[i] in branch_ops:
            branches += 1
    return branches

def score_function(data, start, end):
    """Score a potential function"""
    score = 0
    size = end - start
    
    # Size check (too small or too large)
    if size < 8 or size > 500:
        return 0
    
    # Prologue bonus
    if data[start] in prologues:
        score += 2
    
    # Epilogue bonus (RTS/RTL at end)
    if data[end-1] in epilogues:
        score += 3
    
    # Call richness
    calls = find_calls_in_function(data, start, end)
    score += min(calls, 5)
    
    # Branch count
    branches = find_branches_in_function(data, start, end)
    score += min(branches // 2, 3)
    
    # Reasonable size bonus
    if 20 <= size <= 200:
        score += 1
    
    return score

def find_functions_in_range(data, range_start, range_end, min_score=5):
    """Find functions in a range"""
    functions = []
    rel_start = range_start - 0x8C00
    rel_end = range_end - 0x8C00
    
    # Find all potential function starts (prologues)
    starts = []
    for i in range(rel_start, rel_end):
        if data[i] in prologues:
            starts.append(i)
    
    # For each start, try to find end
    for start in starts:
        # Look for RTS/RTL within reasonable range
        for end in range(start + 8, min(start + 300, rel_end)):
            if data[end] in [0x60, 0x6B]:  # RTS, RTL
                score = score_function(data, start, end + 1)
                if score >= min_score:
                    functions.append({
                        'start': 0x8C00 + start,
                        'end': 0x8C00 + end + 1,
                        'size': end - start + 1,
                        'score': score,
                        'calls': find_calls_in_function(data, start, end + 1),
                        'prologue': prologues.get(data[start], '???'),
                    })
                break
    
    return functions

# Gaps to analyze
gaps = [
    (0x8C00, 0x8CAB, "Pre-8CAB"),
    (0x8D11, 0x8D87, "8CAB-8D87"),
    (0x8DDA, 0x8EBE, "8D87-8EBE"),
]

all_functions = []

for gap_start, gap_end, gap_name in gaps:
    print(f"\n--- Gap: C2:{gap_start:04X}-C2:{gap_end:04X} ({gap_name}) ---")
    
    funcs = find_functions_in_range(data, gap_start, gap_end, min_score=4)
    funcs.sort(key=lambda x: x['start'])
    
    print(f"Found {len(funcs)} candidate functions:")
    for f in funcs[:8]:
        print(f"  C2:{f['start']:04X}-C2:{f['end']:04X} | {f['size']:3d}b | Score: {f['score']} | Calls: {f['calls']} | {f['prologue']}")
    
    all_functions.extend(funcs)

# Filter overlapping functions
def filter_overlapping(functions):
    """Remove overlapping functions, keeping higher scores"""
    sorted_funcs = sorted(functions, key=lambda x: (-x['score'], -x['calls'], x['size']))
    filtered = []
    used_ranges = []
    
    for f in sorted_funcs:
        overlaps = False
        for start, end in used_ranges:
            if not (f['end'] <= start or f['start'] >= end):
                overlaps = True
                break
        if not overlaps:
            filtered.append(f)
            used_ranges.append((f['start'], f['end']))
    
    return sorted(filtered, key=lambda x: x['start'])

unique_functions = filter_overlapping(all_functions)

print(f"\n{'='*60}")
print("UNIQUE HIGH-VALUE FUNCTIONS (Score 5+, sorted by address)")
print(f"{'='*60}")

high_value = [f for f in unique_functions if f['score'] >= 5]
for f in high_value[:15]:
    print(f"C2:{f['start']:04X}-C2:{f['end']:04X} | {f['size']:3d}b | Score: {f['score']} | Calls: {f['calls']}")

# Also analyze the entire 8C00-9000 for any missed functions
print(f"\n{'='*60}")
print("FULL REGION SCAN (8C00-9000)")
print(f"{'='*60}")

all_region_funcs = find_functions_in_range(data, 0x8C00, 0x9000, min_score=6)
all_region_funcs = filter_overlapping(all_region_funcs)

print(f"Found {len(all_region_funcs)} score-6+ functions:")
for f in all_region_funcs:
    print(f"C2:{f['start']:04X}-C2:{f['end']:04X} | {f['size']:3d}b | Score: {f['score']} | Calls: {f['calls']}")

# Save results
with open('c2_8c00_functions.json', 'w') as f:
    json.dump({
        'gap_functions': all_functions,
        'unique_high_value': high_value,
        'all_region_score6': all_region_funcs,
    }, f, indent=2)

print(f"\n{'='*60}")
print(f"Results saved to c2_8c00_functions.json")
print(f"High-value candidates: {len(high_value)}")
print(f"Score-6+ in region: {len(all_region_funcs)}")
print(f"{'='*60}")
