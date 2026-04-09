#!/usr/bin/env python3
"""Analyze C2:8C00-9000 score-9 hub region using HiROM addressing"""

import json

def hirom_to_file_offset(bank, addr):
    """HiROM: offset = ((bank & 0x3F) << 16) | addr"""
    return ((bank & 0x3F) << 16) | addr

# Read C2:8C00-9000
with open('rom/Chrono Trigger (USA).sfc', 'rb') as f:
    offset = hirom_to_file_offset(0xC2, 0x8C00)
    f.seek(offset)
    data = bytearray(f.read(0x400))

print("=" * 80)
print("C2:8C00-9000 SCORE-9 HUB REGION EXPANSION (Session 31)")
print("=" * 80)
print(f"File offset: 0x{offset:06X}")
print(f"First 16 bytes: {' '.join(f'{b:02X}' for b in data[:16])}")

# Verify with known function C2:8CAB
verify_offset = hirom_to_file_offset(0xC2, 0x8CAB) - offset
print(f"\nVerification - C2:8CAB at relative offset 0x{verify_offset:04X}:")
print(f"  Bytes: {' '.join(f'{b:02X}' for b in data[verify_offset:verify_offset+8])}")

# Valid 65816 opcodes
valid_opcodes = set(range(256))  # Simplified - all bytes could be valid opcodes

# Prologues and epilogues
prologues = {0x08: 'PHP', 0x0B: 'PHD', 0x48: 'PHA', 0x5A: 'PHY', 0xDA: 'PHX', 
             0xC2: 'REP', 0xE2: 'SEP', 0x78: 'SEI', 0x20: 'JSR', 0x22: 'JSL',
             0xA9: 'LDA', 0xA2: 'LDX', 0xA0: 'LDY', 0x8B: 'PHB'}
epilogues = {0x28: 'PLP', 0x2B: 'PLD', 0x68: 'PLA', 0x7A: 'PLY', 0xFA: 'PLX',
             0x60: 'RTS', 0x6B: 'RTL', 0x40: 'RTI', 0xAB: 'PLB'}

# Analyze by 256-byte pages
print("\n--- Page Analysis (256-byte blocks) ---")
page_stats = []
for page in range(4):  # 8C00, 8D00, 8E00, 8F00
    base = page * 0x100
    page_data = data[base:base+0x100]
    
    prologue_count = sum(1 for b in page_data if b in prologues)
    epilogue_count = sum(1 for b in page_data if b in epilogues)
    jsr_count = page_data.count(0x20)
    jsl_count = page_data.count(0x22)
    rts_count = page_data.count(0x60)
    rtl_count = page_data.count(0x6B)
    
    # Score the page
    has_structure = prologue_count > 0 and epilogue_count > 0
    call_density = (jsr_count + jsl_count) / 256
    ret_density = (rts_count + rtl_count) / 256
    
    if has_structure and call_density > 0.02:
        status = "CODE"
    elif has_structure:
        status = "MIXED"
    elif prologue_count == 0 and epilogue_count == 0:
        status = "DATA"
    else:
        status = "UNCLEAR"
    
    page_addr = 0x8C00 + page * 0x100
    print(f"C2:{page_addr:04X}: P={prologue_count} E={epilogue_count} JSR={jsr_count} JSL={jsl_count} RTS={rts_count} RTL={rtl_count} | {status}")
    
    page_stats.append({
        'addr': page_addr,
        'prologues': prologue_count,
        'epilogues': epilogue_count,
        'jsr': jsr_count,
        'jsl': jsl_count,
        'status': status
    })

# Known manifests in this region (from labels/)
known_functions = [
    {'start': 0x8CAB, 'end': 0x8D11, 'name': 'C2:8CAB Score-9 Hub', 'score': 9},
    {'start': 0x8D87, 'end': 0x8DDA, 'name': 'C2:8D87 Score-9 Hub', 'score': 9},
    {'start': 0x8EBE, 'end': 0x8F30, 'name': 'C2:8EBE Score-9 Hub', 'score': 9},
    {'start': 0x8F30, 'end': 0x8F8E, 'name': 'C2:8F30 Score-9 Hub', 'score': 9},
    {'start': 0x8F8E, 'end': 0x8FF9, 'name': 'C2:8F8E Score-9 Hub', 'score': 9},
]

print("\n--- Gap Analysis ---")
gaps = []
prev_end = 0x8C00
for func in sorted(known_functions, key=lambda x: x['start']):
    if func['start'] > prev_end:
        gap_size = func['start'] - prev_end
        gaps.append({'start': prev_end, 'end': func['start'], 'size': gap_size})
        print(f"Gap C2:{prev_end:04X}-C2:{func['start']:04X}: {gap_size} bytes")
    prev_end = func['end']

if prev_end < 0x9000:
    gap_size = 0x9000 - prev_end
    gaps.append({'start': prev_end, 'end': 0x9000, 'size': gap_size})
    print(f"Gap C2:{prev_end:04X}-C2:9000: {gap_size} bytes")

# Analyze gaps for potential functions
def find_calls_in_range(data, start_rel, end_rel):
    """Find JSR/JSL instructions in a range"""
    calls = []
    i = start_rel
    while i < end_rel - 2:
        if data[i] == 0x20:  # JSR
            target = data[i+1] | (data[i+2] << 8)
            calls.append(('JSR', 0x8C00 + i, target))
            i += 3
        elif data[i] == 0x22:  # JSL
            target = data[i+1] | (data[i+2] << 8) | (data[i+3] << 16)
            calls.append(('JSL', 0x8C00 + i, target))
            i += 4
        else:
            i += 1
    return calls

print("\n--- Gap Contents ---")
for gap in gaps:
    start_rel = gap['start'] - 0x8C00
    end_rel = gap['end'] - 0x8C00
    gap_data = data[start_rel:end_rel]
    
    calls = find_calls_in_range(data, start_rel, end_rel)
    prologue_hits = [i for i, b in enumerate(gap_data) if b in prologues]
    epilogue_hits = [i for i, b in enumerate(gap_data) if b in epilogues]
    
    print(f"\nC2:{gap['start']:04X}-C2:{gap['end']:04X} ({gap['size']} bytes):")
    print(f"  Prologue bytes at: {[hex(gap['start'] + p) for p in prologue_hits[:5]]}")
    print(f"  Epilogue bytes at: {[hex(gap['start'] + e) for e in epilogue_hits[:5]]}")
    print(f"  Calls: {len(calls)}")
    
    # Look for patterns suggesting functions
    if len(prologue_hits) > 0 and len(epilogue_hits) > 0:
        print(f"  -> Has prologue/epilogue patterns (potential functions)")
    elif gap['size'] < 20:
        print(f"  -> Small gap (likely padding)")
    else:
        print(f"  -> Large data region or complex code")

# Save analysis
with open('c2_8c00_analysis.json', 'w') as f:
    json.dump({
        'page_stats': page_stats,
        'gaps': gaps,
        'known_functions': known_functions,
    }, f, indent=2)

print("\n" + "=" * 80)
print("Analysis complete - results in c2_8c00_analysis.json")
print("=" * 80)
