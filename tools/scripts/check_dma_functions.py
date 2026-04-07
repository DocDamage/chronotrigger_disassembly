#!/usr/bin/env python3
"""Check DMA utility functions at C0:8085, C0:808D, C0:8500"""

import sys
import os

# Read ROM
rom_path = os.path.join(os.path.dirname(__file__), '../../rom/Chrono Trigger (USA).sfc')
with open(rom_path, 'rb') as f:
    rom = f.read()

def hirom_to_file_offset(snes_addr):
    return snes_addr & 0x3FFFFF

# Target addresses to examine - check up to 256 bytes for RTS
targets = [
    (0xC08085, 'C0:8085', '28 callers - DMA utility'),
    (0xC0808D, 'C0:808D', '32 callers - DMA utility'),
    (0xC08500, 'C0:8500', '20 callers - DMA setup'),
]

for snes_addr, name, desc in targets:
    offset = hirom_to_file_offset(snes_addr)
    print(f'=== {name} ({desc}) ===')
    print(f'    SNES: 0x{snes_addr:06X} -> File: 0x{offset:06X}')
    
    # Read 256 bytes at this location
    data = rom[offset:offset+256]
    
    # Print first 16 bytes
    hex_part = ' '.join(f'{b:02X}' for b in data[:16])
    print(f'  First 16 bytes: {hex_part}')
    
    # Check for RTS (0x60), RTL (0x6B), RTI (0x40)
    rts_positions = [i for i, b in enumerate(data) if b == 0x60]
    rtl_positions = [i for i, b in enumerate(data) if b == 0x6B]
    
    print(f'  RTS at offsets: {[f"+{i} ({i:02X})" for i in rts_positions[:3]]}')
    print(f'  RTL at offsets: {[f"+{i} ({i:02X})" for i in rtl_positions[:3]]}')
    
    if rts_positions:
        first_rts = rts_positions[0]
        end_addr = snes_addr + first_rts
        print(f'  First function ends: C0:{end_addr:04X} (length {first_rts} bytes)')
    if rtl_positions:
        first_rtl = rtl_positions[0]
        end_addr = snes_addr + first_rtl
        print(f'  First RTL ends: C0:{end_addr:04X} (length {first_rtl} bytes)')
    
    print()
