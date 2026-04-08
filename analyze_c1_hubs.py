#!/usr/bin/env python3
"""Deep dive analysis of C1 hub function regions"""

import sys
sys.path.insert(0, 'tools/scripts')
from snes_utils_hirom_v2 import hirom_to_file_offset, parse_snes_address

def load_rom(path):
    with open(path, 'rb') as f:
        return f.read()

rom = load_rom('rom/Chrono Trigger (USA).sfc')

def dump_region(start_str, end_str, title):
    bank_s, addr_s = parse_snes_address(start_str)
    bank_e, addr_e = parse_snes_address(end_str)
    start = hirom_to_file_offset(bank_s, addr_s)
    end = hirom_to_file_offset(bank_e, addr_e)
    data = rom[start:end]
    
    base_addr = int(start_str.split(':')[1], 16)
    bank = start_str.split(':')[0]
    
    print(f"\n=== {title} ===")
    print(f"Range: {start_str} to {end_str}")
    
    for i in range(0, len(data), 16):
        row_data = data[i:i+16]
        hex_str = ' '.join(f'{b:02X}' for b in row_data)
        addr = f"{bank}:{base_addr + i:04X}"
        
        # Try to disassemble first few bytes
        disasm = []
        j = 0
        while j < min(len(row_data), 8):  # Disasm first 8 bytes
            b = row_data[j]
            if b == 0x20:
                if j + 2 < len(row_data):
                    target = row_data[j+1] | (row_data[j+2] << 8)
                    disasm.append(f"JSR ${target:04X}")
                    j += 3
                else:
                    disasm.append(f"${b:02X}")
                    j += 1
            elif b == 0x4C:
                if j + 2 < len(row_data):
                    target = row_data[j+1] | (row_data[j+2] << 8)
                    disasm.append(f"JMP ${target:04X}")
                    j += 3
                else:
                    disasm.append(f"${b:02X}")
                    j += 1
            elif b == 0x60:
                disasm.append("RTS")
                j += 1
            elif b == 0x6B:
                disasm.append("RTL")
                j += 1
            elif b == 0xA9:
                if j + 1 < len(row_data):
                    val = row_data[j+1]
                    disasm.append(f"LDA #${val:02X}")
                    j += 2
                else:
                    disasm.append(f"${b:02X}")
                    j += 1
            elif b == 0xA5:
                if j + 1 < len(row_data):
                    val = row_data[j+1]
                    disasm.append(f"LDA ${val:02X}")
                    j += 2
                else:
                    disasm.append(f"${b:02X}")
                    j += 1
            elif b == 0x85:
                if j + 1 < len(row_data):
                    val = row_data[j+1]
                    disasm.append(f"STA ${val:02X}")
                    j += 2
                else:
                    disasm.append(f"${b:02X}")
                    j += 1
            elif b == 0x9C:
                if j + 2 < len(row_data):
                    target = row_data[j+1] | (row_data[j+2] << 8)
                    disasm.append(f"STZ ${target:04X}")
                    j += 3
                else:
                    disasm.append(f"${b:02X}")
                    j += 1
            elif b in (0x48, 0xDA, 0x5A):
                disasm.append("PHA" if b == 0x48 else ("PHX" if b == 0xDA else "PHY"))
                j += 1
            elif b in (0x68, 0xFA, 0x7A):
                disasm.append("PLA" if b == 0x68 else ("PLX" if b == 0xFA else "PLY"))
                j += 1
            elif b == 0x8D:
                if j + 2 < len(row_data):
                    target = row_data[j+1] | (row_data[j+2] << 8)
                    disasm.append(f"STA ${target:04X}")
                    j += 3
                else:
                    disasm.append(f"${b:02X}")
                    j += 1
            elif b in [0xD0, 0xF0, 0x10, 0x30, 0x50, 0x70, 0x90, 0xB0]:
                # Branch instructions
                if j + 1 < len(row_data):
                    offset = row_data[j+1]
                    if offset > 127:
                        offset -= 256
                    disasm.append(f"B{['NE','EQ','PL','MI','VC','VS','CC','CS'][[0xD0,0xF0,0x10,0x30,0x50,0x70,0x90,0xB0].index(b)]} ${offset:+d}")
                    j += 2
                else:
                    disasm.append(f"${b:02X}")
                    j += 1
            else:
                disasm.append(f"${b:02X}")
                j += 1
        
        print(f"{addr}: {hex_str:<48} | {' '.join(disasm)}")

# Analyze the three hub regions
print("=" * 80)
print("C1 HUB FUNCTION DEEP DIVE ANALYSIS")
print("=" * 80)

dump_region("C1:178E", "C1:1800", "Hub 1: C1:179C Dispatch Hub Region (25 callers)")
dump_region("C1:1B06", "C1:1B80", "Hub 2: C1:1B55 Utility Hub Region (29 callers)")
dump_region("C1:4A6B", "C1:4B00", "Hub 3: C1:4AEB Library Hub Region (27 callers)")

# Also check the score-6+ candidates we found
print("\n" + "=" * 80)
print("ADDITIONAL SCORE-6+ CANDIDATES")
print("=" * 80)

dump_region("C1:17B0", "C1:17E0", "Score-6: C1:17B3 candidate")
dump_region("C1:17BC", "C1:17C0", "Score-6: C1:17BF candidate")
dump_region("C1:17D8", "C1:17E0", "Score-6: C1:17DD candidate")
dump_region("C1:1B9B", "C1:1BB0", "Score-6: C1:1BAA candidate")
dump_region("C1:4A68", "C1:4A80", "Score-6: C1:4A71 candidate")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
