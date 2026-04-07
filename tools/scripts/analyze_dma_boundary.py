#!/usr/bin/env python3
"""Analyze DMA function boundaries for potential pass adjustments"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from snes_utils_hirom_v2 import hirom_to_file_offset

rom_path = '../../rom/Chrono Trigger (USA).sfc'

def read_bytes_at(addr, length=256):
    """Read bytes from ROM at SNES address"""
    offset = hirom_to_file_offset(0xC0, addr)
    with open(rom_path, 'rb') as f:
        f.seek(offset)
        return f.read(length)

# Analyze the DMA function at 8085/808D
print("=" * 70)
print("DMA FUNCTION BOUNDARY ANALYSIS")
print("=" * 70)

# C0:8085 analysis
print("\n--- C0:8085 DMA Function Analysis ---")
data_8085 = read_bytes_at(0x8085, 256)

# Find all RTS positions
rts_positions = [i for i, b in enumerate(data_8085) if b == 0x60]
print(f"All RTS positions from C0:8085: {[f'C0:{0x8085+i:04X} (+{i})' for i in rts_positions[:5]]}")

# Check what's at 80BD (start of pass454)
print(f"\nBytes at C0:80BD (pass454 start):")
offset_80bd = 0x80BD - 0x8085
hex_str = ' '.join(f"{b:02X}" for b in data_8085[offset_80bd:offset_80bd+16])
print(f"  {hex_str}")

# Check byte BEFORE 80BD to see if it's mid-instruction
print(f"\nBytes at C0:80BA (3 bytes before pass454):")
offset_80ba = 0x80BA - 0x8085
hex_str = ' '.join(f"{b:02X}" for b in data_8085[offset_80ba:offset_80ba+8])
print(f"  {hex_str}")

# C0:8500 analysis
print("\n" + "=" * 70)
print("--- C0:8500 DMA Function Analysis ---")
data_8500 = read_bytes_at(0x8500, 256)

rts_positions_8500 = [i for i, b in enumerate(data_8500) if b == 0x60]
print(f"All RTS positions from C0:8500: {[f'C0:{0x8500+i:04X} (+{i})' for i in rts_positions_8500[:5]]}")

# Check what's at 851E (start of pass312)
print(f"\nBytes at C0:851E (pass312 start):")
offset_851e = 0x851E - 0x8500
hex_str = ' '.join(f"{b:02X}" for b in data_8500[offset_851e:offset_851e+8])
print(f"  {hex_str}")

# Check what's at 8522 (end of pass312)
print(f"\nBytes at C0:8522 (pass312 end):")
offset_8522 = 0x8522 - 0x8500
hex_str = ' '.join(f"{b:02X}" for b in data_8500[offset_8522:offset_8522+8])
print(f"  {hex_str}")

# Check if 851E is a valid entry point
print("\n" + "=" * 70)
print("BOUNDARY RECOMMENDATIONS")
print("=" * 70)

print("""
C0:8085/C0:808D DMA Function:
- Current pass454 starts at C0:80BD but the function starts at C0:8085
- C0:8085 has 28 callers, C0:808D has 32 callers
- These are ENTRY POINTS into the same shared function body
- Recommendation: Extend pass454 range to C0:8085..C0:813C

C0:8500 DMA Setup:
- Current pass312 covers C0:851E..C0:8522 (tiny wrapper)
- C0:8500 has RTS at +34 (C0:8522) and is the main entry
- Recommendation: Create new pass for C0:8500..C0:8522
- Note: pass312's C0:851E may be part of this same function
""")
