#!/usr/bin/env python3
"""Analyze function boundaries in C2:8000-9000"""

# Read C2:8000-9000 region
with open('rom/Chrono Trigger (USA).sfc', 'rb') as f:
    f.seek(0x18200)
    data = bytearray(f.read(0x1000))

# Known existing manifests
existing = [
    (0x8006, 0x8090, 'S29 Hub Entry'),
    (0x8249, 0x82D5, 'S29 Sweep Service'),
    (0x9F1C, 0x9F49, 'S28 Complex Hub'),
    (0x9F4A, 0x9F8C, 'S29 Hub Extension'),
]

# Find all function boundaries (between returns)
returns = []
for i in range(len(data)):
    if data[i] in [0x60, 0x6B, 0x40]:  # RTS, RTL, RTI
        returns.append(i + 0x8000)

returns.sort()

# Analyze gaps between returns as potential functions
def find_jsr_jsl_count(start, end):
    count = 0
    i = start - 0x8000
    end_idx = min(end - 0x8000, len(data))
    while i < end_idx:
        if data[i] == 0x20:  # JSR
            count += 1
            i += 3
        elif data[i] == 0x22:  # JSL
            count += 1
            i += 4
        else:
            i += 1
    return count

# Score potential functions
print('C2:8000-9000 FUNCTION ANALYSIS')
print('=' * 70)

candidates = []
prev_end = 0x8000
for ret in returns:
    # Function likely starts after previous return
    start = prev_end
    end = ret + 1
    size = end - start
    
    if 4 <= size <= 500:  # Reasonable function size
        calls = find_jsr_jsl_count(start, end)
        
        # Score it
        score = 0
        # End with RTS/RTL/RTI
        score += 3
        # Has internal calls
        score += min(calls, 4)
        # Check start byte
        start_byte = data[start - 0x8000]
        prologues = {0x08, 0x0B, 0x48, 0x5A, 0xDA, 0xC2, 0xE2, 0x78, 0x20, 0x22}
        if start_byte in prologues:
            score += 2
        
        candidates.append({
            'start': start,
            'end': end,
            'size': size,
            'score': score,
            'calls': calls,
            'ret_type': data[ret - 0x8000]
        })
    
    prev_end = end

# Filter out existing manifests
def overlaps_existing(start, end):
    for estart, eend, _ in existing:
        if not (end <= estart or start >= eend):
            return True
    return False

new_candidates = [c for c in candidates if not overlaps_existing(c['start'], c['end'])]

print(f"\nScore 6+ Candidates (excluding existing manifests):")
print(f"{'Start':<10} {'End':<10} {'Size':<6} {'Score':<6} {'Calls':<6}")
print('-' * 50)

for c in sorted(new_candidates, key=lambda x: x['score'], reverse=True):
    if c['score'] >= 6:
        ret_str = {0x60: 'RTS', 0x6B: 'RTL', 0x40: 'RTI'}.get(c['ret_type'], '?')
        print(f"C2:{c['start']:04X}   C2:{c['end']:04X}   {c['size']:<6} {c['score']:<6} {c['calls']:<6} ({ret_str})")

print(f"\nTotal candidates: {len(new_candidates)}")
print(f"Score 6+ candidates: {sum(1 for c in new_candidates if c['score'] >= 6)}")

# Save high-value candidates for manifest creation
import json
high_value = [c for c in new_candidates if c['score'] >= 6]
with open('c2_8000_new_candidates.json', 'w') as f:
    json.dump(high_value, f, indent=2)
print(f"Saved {len(high_value)} high-value candidates to c2_8000_new_candidates.json")
