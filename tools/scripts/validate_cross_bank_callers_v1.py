#!/usr/bin/env python3
"""Validate cross-bank callers and detect fake same-bank misidentifications.

Addresses the issue found in C4:8010 where 22 "cross-bank" callers were 
actually same-bank JSR/JMP instructions that resolved to addresses in their
own bank, not C4.
"""

import argparse
import json
from pathlib import Path

def hirom_to_file_offset(bank, addr):
    """Convert HiROM SNES address to file offset."""
    return ((bank - 0xC0) * 0x10000) + addr

def file_offset_to_hirom(offset):
    """Convert file offset to HiROM SNES address."""
    bank = (offset // 0x10000) + 0xC0
    addr = offset % 0x10000
    return bank, addr

def read_byte(rom, bank, addr):
    """Read a byte from ROM at SNES address."""
    offset = hirom_to_file_offset(bank, addr)
    if offset < len(rom):
        return rom[offset]
    return None

def read_instruction(rom, bank, addr):
    """Read instruction at SNES address and return (opcode, operands, instruction_size)."""
    offset = hirom_to_file_offset(bank, addr)
    if offset >= len(rom):
        return None, None, 0
    
    opcode = rom[offset]
    
    # Single byte instructions
    if opcode in (0x60, 0x6B, 0x40, 0x00):  # RTS, RTL, RTI, BRK
        return opcode, [], 1
    
    # Two byte instructions
    if opcode in (0x20,):  # JSR abs
        if offset + 2 < len(rom):
            target = rom[offset + 1] | (rom[offset + 2] << 8)
            return opcode, [target], 3
    
    # Three byte instructions
    if opcode in (0x22,):  # JSL long
        if offset + 3 < len(rom):
            target = rom[offset + 1] | (rom[offset + 2] << 8) | (rom[offset + 3] << 16)
            return opcode, [target], 4
    
    if opcode in (0x4C, 0x5C):  # JMP abs, JML long
        if offset + 2 < len(rom):
            target = rom[offset + 1] | (rom[offset + 2] << 8)
            if opcode == 0x5C and offset + 3 < len(rom):
                target |= rom[offset + 3] << 16
                return opcode, [target], 4
            return opcode, [target], 3
    
    return opcode, None, 1

def validate_caller(rom, caller_addr, target_addr):
    """Validate if a caller actually calls the target.
    
    Returns:
        - "VALID_CROSS_BANK": True cross-bank call (JSL/JML from different bank)
        - "VALID_SAME_BANK": True same-bank call (JSR/JMP within same bank)
        - "FAKE_CROSS_BANK": Same-bank instruction misidentified as cross-bank
        - "INVALID": Not a call instruction
    """
    caller_bank = (caller_addr >> 16) & 0xFF
    target_bank = (target_addr >> 16) & 0xFF
    caller_offset = caller_addr & 0xFFFF
    
    opcode, operands, size = read_instruction(rom, caller_bank, caller_offset)
    
    if opcode is None:
        return "INVALID", "Cannot read instruction"
    
    # Check instruction type
    is_jsl = opcode == 0x22  # JSL
    is_jml = opcode == 0x5C  # JML
    is_jsr = opcode == 0x20  # JSR
    is_jmp = opcode == 0x4C  # JMP
    
    if not (is_jsl or is_jml or is_jsr or is_jmp):
        return "INVALID", f"Not a call/jump instruction (opcode: {opcode:02X})"
    
    if operands is None:
        return "INVALID", "Incomplete instruction"
    
    actual_target = operands[0]
    if is_jsl or is_jml:
        actual_target = operands[0]  # Already includes bank byte
    else:
        # JSR/JMP - add caller's bank
        actual_target = (caller_bank << 16) | operands[0]
    
    # Check if target matches
    if actual_target != target_addr:
        return "INVALID", f"Target mismatch: instruction targets {actual_target:06X}, expected {target_addr:06X}"
    
    # Determine call type
    actual_target_bank = (actual_target >> 16) & 0xFF
    
    if is_jsl or is_jml:
        if actual_target_bank != caller_bank:
            return "VALID_CROSS_BANK", f"JSL/JML to different bank {actual_target_bank:02X}"
        else:
            return "VALID_SAME_BANK", f"JSL/JML within same bank {actual_target_bank:02X}"
    else:
        if actual_target_bank != caller_bank:
            # This shouldn't happen for JSR/JMP - they can't specify different banks
            return "FAKE_CROSS_BANK", f"JSR/JMP cannot target different bank - likely data misread"
        else:
            return "VALID_SAME_BANK", f"JSR/JMP within same bank {actual_target_bank:02X}"

def main():
    parser = argparse.ArgumentParser(description='Validate cross-bank callers')
    parser.add_argument('--rom', required=True, help='Path to ROM file')
    parser.add_argument('--target', required=True, help='Target address (e.g., C4:8010)')
    parser.add_argument('--callers', nargs='+', help='Caller addresses to validate')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    
    args = parser.parse_args()
    
    # Parse target
    target_parts = args.target.replace(':', '').split(':')
    if len(target_parts) == 1:
        target_addr = int(target_parts[0], 16)
    else:
        target_addr = (int(target_parts[0], 16) << 16) | int(target_parts[1], 16)
    
    rom = Path(args.rom).read_bytes()
    
    results = []
    
    print(f"Validating callers to {args.target} ({target_addr:06X}):")
    print("=" * 60)
    
    for caller in args.callers or []:
        caller_addr = int(caller.replace(':', ''), 16)
        status, reason = validate_caller(rom, caller_addr, target_addr)
        
        results.append({
            'caller': caller,
            'caller_addr': caller_addr,
            'status': status,
            'reason': reason
        })
        
        status_icon = "✓" if status.startswith("VALID") else "✗" if status == "INVALID" else "⚠"
        print(f"{status_icon} {caller}: {status}")
        print(f"   {reason}")
        print()
    
    # Summary
    valid_cross = sum(1 for r in results if r['status'] == 'VALID_CROSS_BANK')
    valid_same = sum(1 for r in results if r['status'] == 'VALID_SAME_BANK')
    fake = sum(1 for r in results if r['status'] == 'FAKE_CROSS_BANK')
    invalid = sum(1 for r in results if r['status'] == 'INVALID')
    
    print("=" * 60)
    print(f"Summary:")
    print(f"  Valid cross-bank: {valid_cross}")
    print(f"  Valid same-bank: {valid_same}")
    print(f"  Fake cross-bank: {fake}")
    print(f"  Invalid: {invalid}")
    
    if args.json:
        print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
