#!/usr/bin/env python3
"""Deep dive analysis of C1 hub function regions - v2"""

import sys
sys.path.insert(0, 'tools/scripts')
from snes_utils_hirom_v2 import hirom_to_file_offset, parse_snes_address

def load_rom(path):
    with open(path, 'rb') as f:
        return f.read()

rom = load_rom('rom/Chrono Trigger (USA).sfc')

# 65816 instruction lengths (simplified)
INSTR_LEN = {
    0x60: 1,  # RTS
    0x6B: 1,  # RTL
    0x40: 1,  # RTI
    0x48: 1,  # PHA
    0x68: 1,  # PLA
    0xDA: 1,  # PHX
    0xFA: 1,  # PLX
    0x5A: 1,  # PHY
    0x7A: 1,  # PLY
    0x8A: 1,  # TXA
    0x98: 1,  # TYA
    0xAA: 1,  # TAX
    0xA8: 1,  # TAY
    0xBA: 1,  # TSX
    0x9A: 1,  # TXS
    0x18: 1,  # CLC
    0x38: 1,  # SEC
    0x58: 1,  # CLI
    0x78: 1,  # SEI
    0xB8: 1,  # CLV
    0xC8: 1,  # INY
    0xCA: 1,  # DEX
    0xE8: 1,  # INX
    0x88: 1,  # DEY
    0x1B: 1,  # TCS
    0x3B: 1,  # TSC
    0x7B: 1,  # TDC
    0x8B: 1,  # PHB
    0xAB: 1,  # PLB
    0x0B: 1,  # PHD
    0x2B: 1,  # PLD
    0x4B: 1,  # PHK
    0x5B: 1,  # TCD
    0x9B: 1,  # TXY
    0xBB: 1,  # TYX
    0xCB: 1,  # WAI
    0xDB: 1,  # STP
    0xEA: 1,  # NOP
    0xEB: 1,  # XBA
    0xFB: 1,  # XCE
}

def get_instr_length(opcode, rom_data, offset):
    if opcode in INSTR_LEN:
        return INSTR_LEN[opcode]
    # Implied/single byte
    if opcode in [0x1A, 0x3A]:  # INC A, DEC A
        return 1
    # Immediate (2 bytes)
    if opcode in [0x09, 0x29, 0x49, 0x69, 0x89, 0xA0, 0xA2, 0xA9, 0xC0, 0xC9, 0xE0, 0xE9]:
        return 2
    # Direct page (2 bytes)
    if opcode in [0x05, 0x24, 0x25, 0x45, 0x65, 0x85, 0xA4, 0xA5, 0xA6, 0xC4, 0xC5, 0xE4, 0xE5]:
        return 2
    # Absolute (3 bytes)
    if opcode in [0x0D, 0x0C, 0x0E, 0x0F, 0x20, 0x4C, 0x8C, 0x8D, 0x8E, 0x8F, 0x9C, 0x9D, 0x9E, 0x9F,
                  0x0C, 0x2C, 0x4D, 0x6D, 0x8C, 0xAC, 0xAD, 0xAE, 0xAF, 0xCC, 0xCD, 0xCE, 0xCF, 0xEC, 0xED, 0xEE, 0xEF]:
        return 3
    # Long (4 bytes)
    if opcode in [0x22, 0x5C, 0x8F, 0x9F, 0xCF, 0xDF, 0xEF, 0xFC]:
        return 4
    # Branches (2 bytes with relative offset)
    if opcode in [0x10, 0x30, 0x50, 0x70, 0x90, 0xB0, 0xD0, 0xF0, 0x80]:
        return 2
    # Default
    return 1

def disasm_at(rom, addr_str, max_bytes=128):
    bank, addr = parse_snes_address(addr_str)
    offset = hirom_to_file_offset(bank, addr)
    
    instrs = []
    pos = 0
    while pos < max_bytes:
        if offset + pos >= len(rom):
            break
        opcode = rom[offset + pos]
        curr_addr = addr + pos
        
        length = get_instr_length(opcode, rom, offset + pos)
        remaining = len(rom) - (offset + pos)
        actual_len = min(length, remaining)
        data = rom[offset + pos:offset + pos + actual_len]
        
        # Format instruction
        if opcode == 0x60:
            text = "RTS"
        elif opcode == 0x6B:
            text = "RTL"
        elif opcode == 0x40:
            text = "RTI"
        elif opcode == 0x20:
            target = data[1] | (data[2] << 8)
            text = f"JSR ${target:04X}"
        elif opcode == 0x4C:
            target = data[1] | (data[2] << 8)
            text = f"JMP ${target:04X}"
        elif opcode == 0x22:
            target = data[1] | (data[2] << 8) | (data[3] << 16)
            text = f"JSL ${target:06X}"
        elif opcode == 0x5C:
            target = data[1] | (data[2] << 8) | (data[3] << 16)
            text = f"JML ${target:06X}"
        elif opcode == 0xA9:
            text = f"LDA #${data[1]:02X}"
        elif opcode == 0xA5:
            text = f"LDA ${data[1]:02X}"
        elif opcode == 0xAD:
            target = data[1] | (data[2] << 8)
            text = f"LDA ${target:04X}"
        elif opcode == 0x85:
            text = f"STA ${data[1]:02X}"
        elif opcode == 0x8D:
            target = data[1] | (data[2] << 8)
            text = f"STA ${target:04X}"
        elif opcode == 0x9C:
            target = data[1] | (data[2] << 8)
            text = f"STZ ${target:04X}"
        elif opcode == 0x64:
            text = f"STZ ${data[1]:02X}"
        elif opcode == 0x48:
            text = "PHA"
        elif opcode == 0x68:
            text = "PLA"
        elif opcode == 0xDA:
            text = "PHX"
        elif opcode == 0xFA:
            text = "PLX"
        elif opcode == 0x5A:
            text = "PHY"
        elif opcode == 0x7A:
            text = "PLY"
        elif opcode == 0x18:
            text = "CLC"
        elif opcode == 0x38:
            text = "SEC"
        elif opcode == 0x69:
            text = f"ADC #${data[1]:02X}"
        elif opcode == 0xE9:
            text = f"SBC #${data[1]:02X}"
        elif opcode == 0xC9:
            text = f"CMP #${data[1]:02X}"
        elif opcode == 0x10:
            off = data[1] if data[1] < 128 else data[1] - 256
            text = f"BPL ${off:+d}"
        elif opcode == 0x30:
            off = data[1] if data[1] < 128 else data[1] - 256
            text = f"BMI ${off:+d}"
        elif opcode == 0x50:
            off = data[1] if data[1] < 128 else data[1] - 256
            text = f"BVC ${off:+d}"
        elif opcode == 0x70:
            off = data[1] if data[1] < 128 else data[1] - 256
            text = f"BVS ${off:+d}"
        elif opcode == 0x90:
            off = data[1] if data[1] < 128 else data[1] - 256
            text = f"BCC ${off:+d}"
        elif opcode == 0xB0:
            off = data[1] if data[1] < 128 else data[1] - 256
            text = f"BCS ${off:+d}"
        elif opcode == 0xD0:
            off = data[1] if data[1] < 128 else data[1] - 256
            text = f"BNE ${off:+d}"
        elif opcode == 0xF0:
            off = data[1] if data[1] < 128 else data[1] - 256
            text = f"BEQ ${off:+d}"
        elif opcode == 0x80:
            off = data[1] if data[1] < 128 else data[1] - 256
            text = f"BRA ${off:+d}"
        elif opcode == 0xAA:
            text = "TAX"
        elif opcode == 0xA8:
            text = "TAY"
        elif opcode == 0x8A:
            text = "TXA"
        elif opcode == 0x98:
            text = "TYA"
        elif opcode == 0xE2:
            text = f"SEP #${data[1]:02X}"
        elif opcode == 0xC2:
            text = f"REP #${data[1]:02X}"
        elif opcode == 0x29:
            text = f"AND #${data[1]:02X}"
        elif opcode == 0x05:
            text = f"ORA ${data[1]:02X}"
        elif opcode == 0x1A:
            text = "INC A"
        elif opcode == 0x3A:
            text = "DEC A"
        elif opcode == 0xE6:
            text = f"INC ${data[1]:02X}"
        elif opcode == 0xC6:
            text = f"DEC ${data[1]:02X}"
        elif opcode == 0xEE:
            target = data[1] | (data[2] << 8)
            text = f"INC ${target:04X}"
        elif opcode == 0xBD:
            target = data[1] | (data[2] << 8)
            text = f"LDA ${target:04X},X"
        elif opcode == 0x9D:
            target = data[1] | (data[2] << 8)
            text = f"STA ${target:04X},X"
        elif opcode == 0xB9:
            target = data[1] | (data[2] << 8)
            text = f"LDA ${target:04X},Y"
        elif opcode == 0x99:
            target = data[1] | (data[2] << 8)
            text = f"STA ${target:04X},Y"
        elif opcode == 0xBC:
            target = data[1] | (data[2] << 8)
            text = f"LDY ${target:04X}"
        else:
            text = f"db ${opcode:02X}"
        
        instrs.append((f"{bank:02X}:{curr_addr:04X}", opcode, data.hex().upper(), text))
        
        # Stop at return instructions
        if opcode in (0x60, 0x6B, 0x40, 0x4C, 0x5C):
            if opcode == 0x4C or opcode == 0x5C:  # JMP/JML - continue for jump table analysis
                pass
            else:
                pos += length
                break
        
        pos += length
    
    return instrs

def find_function_end(rom, start_addr, max_scan=256):
    """Find function end by scanning for RTS/RTL/RTI"""
    bank, addr = parse_snes_address(start_addr)
    offset = hirom_to_file_offset(bank, addr)
    
    pos = 0
    while pos < max_scan:
        if offset + pos >= len(rom):
            break
        opcode = rom[offset + pos]
        
        length = get_instr_length(opcode, rom, offset + pos)
        
        if opcode in (0x60, 0x6B, 0x40):  # RTS, RTL, RTI
            return addr + pos + length - 1
        
        # Long jumps usually end functions
        if opcode in (0x4C, 0x5C, 0x6C, 0x7C, 0xDC, 0xFC):
            if opcode == 0x4C:  # JMP - check if followed by code or data
                return addr + pos + length - 1
        
        pos += length
    
    return addr + pos

# Analyze each region
print("=" * 80)
print("C1 HUB FUNCTION BOUNDARY ANALYSIS")
print("=" * 80)

# Region 1: C1:179C Dispatch Hub
print("\n" + "=" * 80)
print("REGION 1: C1:179C DISPATCH HUB (25 callers)")
print("=" * 80)

print("\n--- C1:178E (Score-6 start, hub entry) ---")
instrs = disasm_at(rom, "C1:178E", 64)
for addr, opc, data, text in instrs[:16]:
    marker = " <<< HUB C1:179C" if "179C" in addr else ""
    print(f"  {addr}: {data:<12} {text}{marker}")

# The hub functions we found
hub_targets = [
    ("C1:179C", "Hub entry (dispatch)"),
    ("C1:17B3", "Score-6 sub-function"),
    ("C1:17BF", "Score-6 sub-function"),
    ("C1:17DD", "Score-6 sub-function"),
]

print("\n--- Function Boundaries ---")
for addr, desc in hub_targets:
    end = find_function_end(rom, addr, 128)
    print(f"  {addr}..{end:04X} : {desc}")

# Region 2: C1:1B55 Utility Hub
print("\n" + "=" * 80)
print("REGION 2: C1:1B55 UTILITY HUB (29 callers)")
print("=" * 80)

print("\n--- C1:1B06 (Score-6 start, LDA# prologue) ---")
instrs = disasm_at(rom, "C1:1B06", 64)
for addr, opc, data, text in instrs[:12]:
    marker = " <<< HUB C1:1B55" if "1B55" in addr else ""
    print(f"  {addr}: {data:<12} {text}{marker}")

print("\n--- C1:1B9B (Score-6 candidate C1:1BAA) ---")
instrs = disasm_at(rom, "C1:1B9B", 32)
for addr, opc, data, text in instrs[:8]:
    marker = " <<< ENTRY C1:1BAA" if "1BAA" in addr else ""
    print(f"  {addr}: {data:<12} {text}{marker}")

# Region 3: C1:4AEB Library Hub
print("\n" + "=" * 80)
print("REGION 3: C1:4AEB LIBRARY HUB (27 callers)")
print("=" * 80)

print("\n--- C1:4A6B (Score-6 start) ---")
instrs = disasm_at(rom, "C1:4A6B", 64)
for addr, opc, data, text in instrs[:12]:
    marker = ""
    if "4A71" in addr:
        marker = " <<< ENTRY C1:4A71"
    elif "4A7B" in addr:
        marker = " <<< Secondary entry"
    print(f"  {addr}: {data:<12} {text}{marker}")

print("\n--- C1:4AEB (Hub entry point) ---")
instrs = disasm_at(rom, "C1:4ADB", 64)
for addr, opc, data, text in instrs[:12]:
    marker = " <<< HUB C1:4AEB" if "4AEB" in addr else ""
    print(f"  {addr}: {data:<12} {text}{marker}")

# Summary
print("\n" + "=" * 80)
print("FUNCTION BOUNDARY SUMMARY")
print("=" * 80)

all_funcs = [
    ("C1:178E", "Dispatch Hub Main", 25, "high"),
    ("C1:17A5", "Dispatch Handler 1", 0, "medium"),
    ("C1:17BC", "Dispatch Handler 2", 0, "medium"),
    ("C1:17DA", "Dispatch Handler 3", 0, "medium"),
    ("C1:1B06", "Utility Hub Main", 29, "high"),
    ("C1:1B9B", "Utility Handler", 0, "medium"),
    ("C1:4A6B", "Library Init", 1, "high"),
    ("C1:4A9F", "Library Handler 1", 0, "medium"),
    ("C1:4ADB", "Library Hub Main", 27, "high"),
]

for start, desc, callers, conf in all_funcs:
    bank, addr = parse_snes_address(start)
    offset = hirom_to_file_offset(bank, addr)
    end = find_function_end(rom, start, 128)
    size = end - addr + 1
    print(f"  {start}..{bank}:{end:04X} ({size:3d} bytes) | {desc:25s} | Callers: {callers:2d} | {conf}")
