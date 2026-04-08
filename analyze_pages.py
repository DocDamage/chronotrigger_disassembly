#!/usr/bin/env python3
"""Analyze code-dense pages in C7 bank"""

import sys

# Read ROM directly
with open('rom/Chrono Trigger (USA).sfc', 'rb') as f:
    rom_data = f.read()

def hirom_to_file_offset(snes_addr):
    """Convert HiROM SNES address to file offset - mask off top bit"""
    return snes_addr & 0x3FFFFF

pages = [
    (0xC79200, 'C7:9200', '4 clusters'),
    (0xC78F00, 'C7:8F00', 'suspect target 8F91'),
    (0xC79300, 'C7:9300', '2 tiny veneers'),
]

for snes_addr, name, desc in pages:
    file_offset = hirom_to_file_offset(snes_addr)
    print()
    print('=== ' + name + ' (' + desc + ') ===')
    print('    SNES: 0x' + format(snes_addr, '06X') + ' -> File: 0x' + format(file_offset, '06X'))
    
    data = rom_data[file_offset:file_offset+64]
    
    # Print hex dump in rows of 16
    for i in range(0, 64, 16):
        row = data[i:i+16]
        hex_part = ' '.join(format(b, '02X') for b in row)
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in row)
        print("  " + format(i, '04X') + ": " + hex_part + "  " + ascii_part)
    
    # Count returns and prologues
    rts = sum(1 for b in data if b == 0x60)
    rtl = sum(1 for b in data if b == 0x6B)
    php = sum(1 for b in data if b == 0x08)
    phb = sum(1 for b in data if b == 0x8B)
    rep = sum(1 for b in data if b == 0xC2)
    sep = sum(1 for b in data if b == 0xE2)
    
    print('  Opcode counts in first 64 bytes:')
    print('    RTS: ' + str(rts) + ', RTL: ' + str(rtl) + ', PHP: ' + str(php) + ', PHB: ' + str(phb) + ', REP: ' + str(rep) + ', SEP: ' + str(sep))
    
    # Extended analysis
    print('  Extended 256-byte opcode counts:')
    data256 = rom_data[file_offset:file_offset+256]
    rts256 = sum(1 for b in data256 if b == 0x60)
    rtl256 = sum(1 for b in data256 if b == 0x6B)
    rti = sum(1 for b in data256 if b == 0x40)
    pha = sum(1 for b in data256 if b == 0x48)
    lda_imm = sum(1 for i in range(len(data256)-1) if data256[i] == 0xA9)
    lda_abs = sum(1 for i in range(len(data256)-2) if data256[i] == 0xAD)
    jmp_abs = sum(1 for i in range(len(data256)-2) if data256[i] == 0x4C)
    jsl = sum(1 for i in range(len(data256)-3) if data256[i] == 0x22)
    jsr = sum(1 for i in range(len(data256)-2) if data256[i] == 0x20)
    print('    RTS: ' + str(rts256) + ', RTL: ' + str(rtl256) + ', RTI: ' + str(rti) + ', PHA: ' + str(pha))
    print('    LDA #imm: ' + str(lda_imm) + ', LDA abs: ' + str(lda_abs) + ', JMP: ' + str(jmp_abs) + ', JSL: ' + str(jsl) + ', JSR: ' + str(jsr))
    
    # Also check for common patterns
    print('  Pattern analysis:')
    
    # Check for strings of zeros (data padding)
    zero_runs = 0
    for i in range(len(data256)-4):
        if data256[i:i+4] == bytes(4):
            zero_runs += 1
    
    # Check for 0xFF (uninitialized/padding)
    ff_runs = sum(1 for i in range(len(data256)-4) if data256[i:i+4] == b'\xff\xff\xff\xff')
    
    print('    Zero runs (4+ bytes): ' + str(zero_runs))
    print('    0xFF runs (4+ bytes): ' + str(ff_runs))
