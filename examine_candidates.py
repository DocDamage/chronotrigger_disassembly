#!/usr/bin/env python3
import json

# SNES 65816 opcodes for reference
OPCODES = {
    0x08: ("PHP", 1),
    0x0B: ("PHD", 1),
    0x18: ("CLC", 1),
    0x20: ("JSR", 3),
    0x22: ("JSL", 4),
    0x29: ("AND", 2),  # immediate
    0x38: ("SEC", 1),
    0x48: ("PHA", 1),
    0x4C: ("JMP", 3),
    0x5C: ("JML", 4),
    0x60: ("RTS", 1),
    0x6B: ("RTL", 1),
    0x78: ("SEI", 1),
    0x80: ("BRA", 2),
    0x85: ("STA", 2),  # direct page
    0x8B: ("PHB", 1),
    0x8D: ("STA", 3),  # absolute
    0x90: ("BCC", 2),
    0xA0: ("LDY", 3),  # immediate 16-bit
    0xA2: ("LDX", 3),  # immediate 16-bit
    0xA5: ("LDA", 2),  # direct page
    0xA9: ("LDA", 2),  # immediate 8-bit
    0xAD: ("LDA", 3),  # absolute
    0xB0: ("BCS", 2),
    0xC0: ("CPY", 2),  # immediate
    0xC2: ("REP", 2),
    0xC9: ("CMP", 2),  # immediate
    0xD0: ("BNE", 2),
    0xE0: ("CPX", 3),  # immediate 16-bit
    0xE2: ("SEP", 2),
    0xF0: ("BEQ", 2),
}

def hirom_to_file_offset(bank, addr):
    return ((bank & 0x3F) << 16) | addr

def disasm_simple(rom, offset, count=16):
    """Simple disassembly of bytes at offset"""
    result = []
    i = 0
    while i < count and offset + i < len(rom):
        byte = rom[offset + i]
        if byte in OPCODES:
            mnem, length = OPCODES[byte]
            if length == 1:
                result.append(f"{offset+i:06X}: {mnem}")
            elif length == 2 and offset + i + 1 < len(rom):
                operand = rom[offset + i + 1]
                result.append(f"{offset+i:06X}: {mnem} #${operand:02X}")
            elif length == 3 and offset + i + 2 < len(rom):
                operand = rom[offset + i + 1] | (rom[offset + i + 2] << 8)
                result.append(f"{offset+i:06X}: {mnem} ${operand:04X}")
            elif length == 4 and offset + i + 3 < len(rom):
                operand = rom[offset + i + 1] | (rom[offset + i + 2] << 8) | (rom[offset + i + 3] << 16)
                result.append(f"{offset+i:06X}: {mnem} ${operand:06X}")
            else:
                result.append(f"{offset+i:06X}: DB ${byte:02X}")
                i += 1
                continue
            i += length
        else:
            result.append(f"{offset+i:06X}: DB ${byte:02X}")
            i += 1
    return result

def parse_addr(addr_str):
    """Parse C3:2E31 format"""
    parts = addr_str.split(':')
    bank = int(parts[0], 16)
    addr = int(parts[1], 16)
    return bank, addr

def main():
    # Load ROM
    with open('rom/Chrono Trigger (USA).sfc', 'rb') as f:
        rom = f.read()
    
    # Candidates to examine
    candidates = [
        # (start_addr, end_addr, description)
        ("C3:2E31", "C3:2E55", "Score-6 from gap 2900-3058"),
        ("C3:3217", "C3:3234", "Score-6 from gap 30B1-34FF"),
        ("C3:3280", "C3:329A", "Score-6 from gap 30B1-34FF"),
        ("C3:34CE", "C3:34EB", "Score-6 from gap 30B1-34FF"),
        ("C3:387B", "C3:38A3", "Score-6 from gap 3761-3C7F"),
        ("C3:3C5B", "C3:3C76", "Score-6 from gap 3761-3C7F"),
    ]
    
    for start_str, end_str, desc in candidates:
        bank, start = parse_addr(start_str)
        _, end = parse_addr(end_str)
        offset = hirom_to_file_offset(bank, start)
        
        print(f"\n{'='*60}")
        print(f"Candidate: {start_str}..{end_str} ({desc})")
        print(f"File offset: {offset:06X}")
        print(f"{'='*60}")
        
        # Disassemble first 48 bytes
        lines = disasm_simple(rom, offset, 48)
        for line in lines[:16]:
            print(f"  {line}")

if __name__ == "__main__":
    main()
