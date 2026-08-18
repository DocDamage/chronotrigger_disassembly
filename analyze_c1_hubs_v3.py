#!/usr/bin/env python3
"""Deep dive analysis of C1 hub function regions - v3"""

import sys
sys.path.insert(0, 'tools/scripts')
from snes_utils_hirom_v2 import hirom_to_file_offset, parse_snes_address

def load_rom(path):
    with open(path, 'rb') as f:
        return f.read()

rom = load_rom('rom/Chrono Trigger (USA).sfc')

def get_byte(rom, offset, idx):
    """Safely get a byte from ROM"""
    if offset + idx < len(rom):
        return rom[offset + idx]
    return 0

def disasm_simple(rom, addr_str, count=20):
    """Simple disassembly showing first N bytes"""
    bank, addr = parse_snes_address(addr_str)
    offset = hirom_to_file_offset(bank, addr)
    
    result = []
    for i in range(count):
        if offset + i >= len(rom):
            break
        b = rom[offset + i]
        result.append(f"{b:02X}")
    
    return ' '.join(result)

def find_rts(rom, start_addr, max_scan=256):
    """Find the next RTS/RTL/RTI instruction"""
    bank, addr = parse_snes_address(start_addr)
    offset = hirom_to_file_offset(bank, addr)
    
    pos = 0
    while pos < max_scan and offset + pos < len(rom):
        opcode = rom[offset + pos]
        
        # RTS, RTL, RTI
        if opcode in (0x60, 0x6B, 0x40):
            return addr + pos
        
        # Skip instruction bytes (simplified)
        if opcode in (0x20, 0x4C, 0x8D, 0xAD, 0x9C, 0x9D, 0xBD, 0xBC, 0xEE, 0x0D, 0xAC):
            pos += 3  # 3-byte instructions
        elif opcode in (0xA9, 0xA5, 0x85, 0x64, 0xC9, 0x69, 0xE9, 0x29, 0x05, 0xE6, 0xC6):
            pos += 2  # 2-byte instructions
        elif opcode in (0x10, 0x30, 0x50, 0x70, 0x90, 0xB0, 0xD0, 0xF0, 0x80):
            pos += 2  # branches
        elif opcode == 0x22:
            pos += 4  # JSL
        else:
            pos += 1  # 1-byte or unknown
    
    return addr + pos

def analyze_function(rom, start_addr, name, caller_count=0):
    """Analyze a function and return its details"""
    bank, addr = parse_snes_address(start_addr)
    end_addr = find_rts(rom, start_addr, 256)
    size = end_addr - addr + 1
    hex_dump = disasm_simple(rom, start_addr, min(24, size))
    
    return {
        'start': start_addr,
        'end': f"{bank}:{end_addr:04X}",
        'size': size,
        'name': name,
        'callers': caller_count,
        'hex': hex_dump
    }

print("=" * 80)
print("C1 HUB FUNCTION DEEP DIVE ANALYSIS")
print("=" * 80)

# Region 1: C1:179C Dispatch Hub
print("\n" + "=" * 80)
print("REGION 1: C1:1700-1800 - DISPATCH HUB (25 callers)")
print("=" * 80)

funcs_r1 = [
    analyze_function(rom, "C1:178E", "ct_c1_178e_dispatch_init", 0),
    analyze_function(rom, "C1:179C", "ct_c1_179c_dispatch_hub", 25),
    analyze_function(rom, "C1:17A5", "ct_c1_17a5_dispatch_handler_1", 0),
    analyze_function(rom, "C1:17BC", "ct_c1_17bc_dispatch_handler_2", 0),
    analyze_function(rom, "C1:17DA", "ct_c1_17da_dispatch_handler_3", 0),
]

for f in funcs_r1:
    print(f"\n{f['start']}..{f['end']} ({f['size']:3d} bytes) - {f['name']}")
    print(f"  Callers: {f['callers']} | Hex: {f['hex'][:48]}...")

# Region 2: C1:1B55 Utility Hub
print("\n" + "=" * 80)
print("REGION 2: C1:1B00-1C00 - UTILITY HUB (29 callers)")
print("=" * 80)

funcs_r2 = [
    analyze_function(rom, "C1:1B06", "ct_c1_1b06_utility_init", 0),
    analyze_function(rom, "C1:1B14", "ct_c1_1b14_utility_handler", 0),
    analyze_function(rom, "C1:1B55", "ct_c1_1b55_utility_hub", 29),
    analyze_function(rom, "C1:1B9B", "ct_c1_1b9b_utility_handler_2", 0),
]

for f in funcs_r2:
    print(f"\n{f['start']}..{f['end']} ({f['size']:3d} bytes) - {f['name']}")
    print(f"  Callers: {f['callers']} | Hex: {f['hex'][:48]}...")

# Region 3: C1:4AEB Library Hub
print("\n" + "=" * 80)
print("REGION 3: C1:4A00-4B00 - LIBRARY HUB (27 callers)")
print("=" * 80)

funcs_r3 = [
    analyze_function(rom, "C1:4A6B", "ct_c1_4a6b_library_init", 0),
    analyze_function(rom, "C1:4A71", "ct_c1_4a71_library_handler", 0),
    analyze_function(rom, "C1:4A9F", "ct_c1_4a9f_library_handler_2", 0),
    analyze_function(rom, "C1:4ADB", "ct_c1_4adb_library_main", 0),
    analyze_function(rom, "C1:4AEB", "ct_c1_4aeb_library_hub", 27),
]

for f in funcs_r3:
    print(f"\n{f['start']}..{f['end']} ({f['size']:3d} bytes) - {f['name']}")
    print(f"  Callers: {f['callers']} | Hex: {f['hex'][:48]}...")

# Summary
print("\n" + "=" * 80)
print("MANIFEST RECOMMENDATIONS (Pass 579+)")
print("=" * 80)

all_funcs = funcs_r1 + funcs_r2 + funcs_r3
pass_num = 579

for f in all_funcs:
    if f['callers'] > 0 or f['size'] > 8:  # Promote functions with callers or substantial size
        print(f"""
Pass {pass_num}:
  Range: {f['start']}..{f['end']}
  Label: {f['name']}
  Confidence: {'high' if f['callers'] >= 20 else 'medium'}
  Reason: Score-6 candidate, {f['callers']} caller{'s' if f['callers'] != 1 else ''}, {f['size']} bytes""")
        pass_num += 1

print(f"\n\nTotal recommended functions: {pass_num - 579}")
