#!/usr/bin/env python3
"""Deep analysis of C2:8C00-9000 score-9 hub region expansion"""

import struct
import json

def snes_to_file_addr(bank, addr):
    """Convert SNES LoROM address to file offset"""
    return (bank * 0x8000) + (addr & 0x7FFF) + 0x200

def is_valid_code_byte(b):
    """Check if byte is likely valid 65816 code"""
    valid_opcodes = {
        0x08, 0x0A, 0x0B, 0x18, 0x1B, 0x20, 0x22, 0x28, 0x29, 0x2B, 0x3A, 0x3B,
        0x48, 0x4A, 0x4B, 0x4C, 0x58, 0x5A, 0x5B, 0x60, 0x68, 0x6B, 0x78, 0x7A, 0x7B,
        0x84, 0x85, 0x86, 0x87, 0x8A, 0x8B, 0x8C, 0x8D, 0x8E, 0x8F, 0x98, 0x9A, 0x9B,
        0xA2, 0xA4, 0xA5, 0xA6, 0xA8, 0xA9, 0xAA, 0xAB, 0xAC, 0xAD, 0xAE, 0xAF,
        0xB9, 0xBD, 0xC2, 0xC9, 0xCB, 0xD0, 0xDA, 0xE2, 0xE8, 0xEB, 0xF0
    }
    return b in valid_opcodes

# Read C2:8C00-9000
with open('rom/Chrono Trigger (USA).sfc', 'rb') as f:
    offset = snes_to_file_addr(0xC2, 0x8C00)
    f.seek(offset)
    data = bytearray(f.read(0x400))

print("=" * 80)
print("BANK C2: 8C00-9000 SCORE-9 HUB REGION EXPANSION")
print("Session 31 - Target: 10-12 new manifests")
print("=" * 80)

# Known existing manifests in 8C00-9000
existing_manifests = [
    (0x8CAB, 0x8D11, "C2:8CAB Score-9 Hub (S30)"),
    (0x8D87, 0x8DDA, "C2:8D87 Score-9 Hub (S30)"),
    (0x8EBE, 0x8F30, "C2:8EBE Score-9 Hub (S30)"),
    (0x8F30, 0x8F8E, "C2:8F30 Score-9 Hub (S30)"),
    (0x8F8E, 0x8FF9, "C2:8F8E Score-9 Hub (S30)"),
]

# Gaps to investigate
gaps = [
    (0x8C00, 0x8CAB, "Pre-8CAB gap"),
    (0x8D11, 0x8D87, "8CAB-8D87 gap"),
    (0x8DDA, 0x8EBE, "8D87-8EBE gap"),
    (0x8FF9, 0x9000, "Post-8F8E tail"),
]

prologue_patterns = {
    0x08: "PHP", 0x0B: "PHD", 0x48: "PHA", 0x5A: "PHY", 0xDA: "PHX",
    0xC2: "REP", 0xE2: "SEP", 0x78: "SEI", 0x20: "JSR", 0x22: "JSL",
    0xA9: "LDA", 0xA2: "LDX", 0xA0: "LDY",
}

epilogue_patterns = {
    0x28: "PLP", 0x2B: "PLD", 0x68: "PLA", 0x7A: "PLY", 0xFA: "PLX",
    0x60: "RTS", 0x6B: "RTL", 0x40: "RTI",
}

def find_jsr_jsl_in_range(data, start, end):
    """Find all JSR/JSL calls in a range"""
    calls = []
    i = start
    while i < min(end, len(data)):
        if data[i] == 0x20 and i + 2 < len(data):
            target = data[i+1] | (data[i+2] << 8)
            calls.append(('JSR', i, target))
            i += 3
        elif data[i] == 0x22 and i + 3 < len(data):
            target = data[i+1] | (data[i+2] << 8) | (data[i+3] << 16)
            calls.append(('JSL', i, target))
            i += 4
        elif data[i] in [0xFC, 0xF4]:
            i += 3
        else:
            i += 1
    return calls

def find_branches_in_range(data, start, end):
    """Find branch instructions"""
    branches = []
    i = start
    while i < min(end, len(data)):
        if data[i] in [0xD0, 0xF0, 0x10, 0x30, 0x50, 0x70, 0x90, 0xB0] and i + 1 < len(data):
            offset = data[i+1]
            if offset & 0x80:
                offset -= 256
            target = i + 2 + offset
            branches.append((data[i], i, target))
            i += 2
        elif data[i] == 0x80 and i + 1 < len(data):  # BRA
            offset = data[i+1]
            if offset & 0x80:
                offset -= 256
            target = i + 2 + offset
            branches.append((0x80, i, target))
            i += 2
        else:
            i += 1
    return branches

def score_function(data, start, end):
    """Score a potential function range"""
    score = 0
    if start >= len(data) or end > len(data):
        return 0
    
    func_data = data[start:end]
    size = end - start
    
    first_byte = func_data[0]
    if first_byte in prologue_patterns:
        score += 2
    elif is_valid_code_byte(first_byte):
        score += 1
    
    last_byte = func_data[-1]
    if last_byte in epilogue_patterns:
        score += 3
    
    calls = find_jsr_jsl_in_range(data, start, end)
    score += min(len(calls), 4)
    
    branches = find_branches_in_range(data, start, end)
    score += min(len(branches) // 2, 2)
    
    stack_ops = sum(1 for b in func_data if b in [0x08, 0x48, 0x5A, 0xDA, 0x28, 0x68, 0x7A, 0xFA])
    score += min(stack_ops // 2, 2)
    
    if size < 8 or size > 400:
        score -= 2
    
    return score

def find_functions_in_gap(data, gap_start, gap_end, gap_name):
    """Find function candidates in a gap"""
    candidates = []
    rel_start = gap_start - 0x8C00
    rel_end = gap_end - 0x8C00
    
    i = rel_start
    while i < min(rel_end, len(data)):
        byte = data[i]
        
        if byte in prologue_patterns:
            j = i + 1
            while j < min(i + 300, rel_end, len(data)):
                if data[j] in epilogue_patterns:
                    start_addr = i + 0x8C00
                    end_addr = j + 0x8C00 + 1
                    size = j - i + 1
                    
                    score = score_function(data, i, j + 1)
                    calls = find_jsr_jsl_in_range(data, i, j + 1)
                    branches = find_branches_in_range(data, i, j + 1)
                    
                    if score >= 5:
                        candidates.append({
                            'start': start_addr,
                            'end': end_addr,
                            'size': size,
                            'score': score,
                            'calls': len(calls),
                            'call_list': calls,
                            'branches': len(branches),
                            'gap': gap_name,
                            'prologue': prologue_patterns.get(byte, f"${byte:02X}"),
                            'epilogue': epilogue_patterns.get(data[j], f"${data[j]:02X}"),
                        })
                    break
                j += 1
        
        i += 1
    
    return candidates

all_candidates = []

for gap_start, gap_end, gap_name in gaps:
    print(f"\n{'='*60}")
    print(f"GAP: C2:{gap_start:04X}-C2:{gap_end:04X} ({gap_name})")
    print(f"{'='*60}")
    
    candidates = find_functions_in_gap(data, gap_start, gap_end, gap_name)
    candidates.sort(key=lambda x: (x['score'], x['calls']), reverse=True)
    
    print(f"Found {len(candidates)} score-5+ candidates:")
    for c in candidates[:8]:
        print(f"  C2:{c['start']:04X}-C2:{c['end']:04X} | {c['size']:3d}b | Score: {c['score']} | Calls: {c['calls']} | {c['prologue']}-{c['epilogue']}")
    
    all_candidates.extend(candidates)

# Filter overlapping candidates
def filter_overlapping(candidates):
    sorted_cands = sorted(candidates, key=lambda x: (x['score'], x['calls'], x['size']), reverse=True)
    filtered = []
    used_ranges = []
    
    for c in sorted_cands:
        overlaps = False
        for start, end in used_ranges:
            if not (c['end'] <= start or c['start'] >= end):
                overlaps = True
                break
        if not overlaps:
            filtered.append(c)
            used_ranges.append((c['start'], c['end']))
    
    return filtered

print(f"\n{'='*60}")
print("HIGH-VALUE CANDIDATES (Score 7+, Call-Rich, No Overlap)")
print(f"{'='*60}")

unique_candidates = filter_overlapping(all_candidates)
high_value = [c for c in unique_candidates if c['score'] >= 7 or (c['score'] >= 6 and c['calls'] >= 5)]

for c in high_value[:15]:
    print(f"C2:{c['start']:04X}-C2:{c['end']:04X} | {c['size']:3d}b | Score: {c['score']} | Calls: {c['calls']} | {c['gap']}")

# Save results
with open('c2_8c00_9000_candidates.json', 'w') as f:
    json.dump({
        'all_candidates': all_candidates,
        'high_value_candidates': high_value,
        'gaps': [{'start': s, 'end': e, 'name': n} for s, e, n in gaps],
        'existing_manifests': [{'start': s, 'end': e, 'name': n} for s, e, n in existing_manifests],
    }, f, indent=2)

print(f"\n{'='*60}")
print(f"SUMMARY: {len(high_value)} high-value candidates found")
print(f"Results saved to c2_8c00_9000_candidates.json")
print(f"{'='*60}")
