#!/usr/bin/env python3
"""Deep dive analysis of C2:8000-9000 hub region"""

import struct

def snes_to_file_addr(bank, addr):
    """Convert SNES LoROM address to file offset"""
    # LoROM: Bank * 0x8000 + (addr & 0x7FFF) + 0x200 (header)
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

# Read C2:8000-9000
with open('rom/Chrono Trigger (USA).sfc', 'rb') as f:
    offset = snes_to_file_addr(0xC2, 0x8000)
    f.seek(offset)
    data = bytearray(f.read(0x1000))

print("=" * 80)
print("BANK C2: 8000-9000 DEEP DIVE ANALYSIS")
print("=" * 80)

# Look for function prologues and epilogues
prologue_patterns = {
    0x08: "PHP",      # Push P
    0x0B: "PHD",      # Push D
    0x48: "PHA",      # Push A
    0x5A: "PHY",      # Push Y
    0xDA: "PHX",      # Push X
    0xC2: "REP",      # Reset status bits
    0xE2: "SEP",      # Set status bits
    0x78: "SEI",      # Set interrupt disable
    0x20: "JSR",      # JSR (could be function entry)
    0x22: "JSL",      # JSL (long call)
}

epilogue_patterns = {
    0x28: "PLP",      # Pull P
    0x2B: "PLD",      # Pull D
    0x68: "PLA",      # Pull A
    0x7A: "PLY",      # Pull Y
    0xFA: "PLX",      # Pull X
    0x60: "RTS",      # Return
    0x6B: "RTL",      # Return long
    0x40: "RTI",      # Return from interrupt
}

# JSR/JSL targets for call counting
def find_jsr_jsl_in_range(data, start, end):
    """Find all JSR/JSL calls in a range"""
    calls = []
    i = start
    while i < min(end, len(data)):
        if data[i] == 0x20 and i + 2 < len(data):  # JSR abs
            target = data[i+1] | (data[i+2] << 8)
            calls.append(('JSR', i, target))
            i += 3
        elif data[i] == 0x22 and i + 3 < len(data):  # JSL long
            target = data[i+1] | (data[i+2] << 8) | (data[i+3] << 16)
            calls.append(('JSL', i, target))
            i += 4
        elif data[i] in [0xFC, 0xF4]:  # JSR/JSL (indirect)
            i += 3
        else:
            i += 1
    return calls

def score_function(data, start, end):
    """Score a potential function range"""
    score = 0
    if start >= len(data) or end > len(data):
        return 0
    
    func_data = data[start:end]
    size = end - start
    
    # Clean start bonus
    first_byte = func_data[0]
    if first_byte in prologue_patterns:
        score += 2
    elif is_valid_code_byte(first_byte):
        score += 1
    
    # Clean end bonus (RTS/RTL/RTI)
    last_byte = func_data[-1]
    if last_byte in epilogue_patterns:
        score += 3
    
    # Count calls
    calls = find_jsr_jsl_in_range(data, start, end)
    score += min(len(calls), 4)  # Max 4 points for calls
    
    # Penalty for odd sizes
    if size < 4 or size > 500:
        score -= 2
    
    return score

# Known existing manifests in 8000-9000
existing_manifests = [
    (0x8006, 0x8090, "C2:8006 Hub Entry (S29)"),
    (0x8249, 0x82D5, "C2:8249 Sweep Service (S29)"),
    (0x9F1C, 0x9F49, "C2:9F1C Complex Hub (S28)"),
    (0x9F4A, 0x9F8C, "C2:9F4A Hub Extension (S29)"),
]

# Analyze each sub-region
regions = [
    (0x8000, 0x8400, "8000-8400 (Hub Context)"),
    (0x8400, 0x8800, "8400-8800"),
    (0x8800, 0x8C00, "8800-8C00"),
    (0x8C00, 0x9000, "8C00-9000"),
]

candidates = []

for region_start, region_end, region_name in regions:
    print(f"\n{'='*60}")
    print(f"REGION: C2:{region_name}")
    print(f"{'='*60}")
    
    # Look for function boundaries
    region_candidates = []
    
    # Scan for potential function starts
    i = region_start - 0x8000
    region_data_start = i
    region_data_end = min(region_end - 0x8000, len(data))
    
    while i < region_data_end:
        byte = data[i]
        
        # Check for function prologue
        is_prologue = byte in prologue_patterns
        
        # Look for JSR targets (20 XX YY pattern just before)
        is_jsr_target = False
        if i >= 3:
            if data[i-3] == 0x20:  # JSR just before could mean we're a target
                target = data[i-2] | (data[i-1] << 8)
                if target == (i + 0x8000) & 0xFFFF:
                    is_jsr_target = True
        
        if is_prologue or is_jsr_target:
            # Try to find function end (look for RTS/RTL/RTI)
            j = i + 1
            while j < min(i + 300, region_data_end, len(data)):
                if data[j] in epilogue_patterns:
                    # Found potential end
                    start_addr = i + 0x8000
                    end_addr = j + 0x8000 + 1
                    size = j - i + 1
                    
                    # Score this function
                    score = score_function(data, i, j + 1)
                    calls = find_jsr_jsl_in_range(data, i, j + 1)
                    
                    if score >= 4:  # Minimum threshold
                        region_candidates.append({
                            'start': start_addr,
                            'end': end_addr,
                            'size': size,
                            'score': score,
                            'calls': len(calls),
                            'call_list': calls
                        })
                    break
                j += 1
        
        i += 1
    
    # Display candidates
    print(f"Found {len(region_candidates)} score-4+ candidates:")
    for c in sorted(region_candidates, key=lambda x: x['score'], reverse=True)[:10]:
        print(f"  C2:{c['start']:04X}-C2:{c['end']:04X} | Size: {c['size']:3d} | Score: {c['score']} | Calls: {c['calls']}")
    
    candidates.extend(region_candidates)

# Filter candidates that don't overlap with existing manifests
def overlaps_existing(start, end):
    for estart, eend, _ in existing_manifests:
        if not (end <= estart or start >= eend):
            return True
    return False

print(f"\n{'='*60}")
print("NEW HIGH-VALUE CANDIDATES (Score 6+, 3+ calls)")
print(f"{'='*60}")

new_candidates = []
for c in candidates:
    if c['score'] >= 6 and c['calls'] >= 3 and not overlaps_existing(c['start'], c['end']):
        new_candidates.append(c)
        print(f"C2:{c['start']:04X}-C2:{c['end']:04X} | {c['size']:3d}b | Score: {c['score']} | Calls: {c['calls']}")

print(f"\nTotal new candidates: {len(new_candidates)}")

# Save candidates to JSON for manifest creation
import json
with open('c2_8000_candidates.json', 'w') as f:
    json.dump({
        'all_candidates': candidates,
        'high_value_candidates': new_candidates,
        'existing_manifests': [
            {'start': s, 'end': e, 'name': n} for s, e, n in existing_manifests
        ]
    }, f, indent=2)

print("\nResults saved to c2_8000_candidates.json")
