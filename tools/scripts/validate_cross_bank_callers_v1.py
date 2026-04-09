#!/usr/bin/env python3
"""Validate cross-bank callers and detect fake same-bank misidentifications."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from snes_utils import hirom_to_file_offset, parse_snes_address


def read_instruction(rom: bytes, bank: int, addr: int):
    """Read instruction at SNES address and return (opcode, operands, instruction_size)."""
    offset = hirom_to_file_offset(bank, addr)
    if offset >= len(rom):
        return None, None, 0

    opcode = rom[offset]

    if opcode in (0x60, 0x6B, 0x40, 0x00):
        return opcode, [], 1
    if opcode == 0x20 and offset + 2 < len(rom):
        target = rom[offset + 1] | (rom[offset + 2] << 8)
        return opcode, [target], 3
    if opcode == 0x22 and offset + 3 < len(rom):
        target = rom[offset + 1] | (rom[offset + 2] << 8) | (rom[offset + 3] << 16)
        return opcode, [target], 4
    if opcode in (0x4C, 0x5C) and offset + 2 < len(rom):
        target = rom[offset + 1] | (rom[offset + 2] << 8)
        if opcode == 0x5C and offset + 3 < len(rom):
            target |= rom[offset + 3] << 16
            return opcode, [target], 4
        return opcode, [target], 3

    return opcode, None, 1


def validate_caller(rom: bytes, caller_addr: int, target_addr: int):
    caller_bank = (caller_addr >> 16) & 0xFF
    caller_offset = caller_addr & 0xFFFF

    opcode, operands, _size = read_instruction(rom, caller_bank, caller_offset)
    if opcode is None:
        return "INVALID", "Cannot read instruction"

    is_jsl = opcode == 0x22
    is_jml = opcode == 0x5C
    is_jsr = opcode == 0x20
    is_jmp = opcode == 0x4C

    if not (is_jsl or is_jml or is_jsr or is_jmp):
        return "INVALID", f"Not a call/jump instruction (opcode: {opcode:02X})"
    if operands is None:
        return "INVALID", "Incomplete instruction"

    actual_target = operands[0] if (is_jsl or is_jml) else ((caller_bank << 16) | operands[0])
    if actual_target != target_addr:
        return "INVALID", f"Target mismatch: instruction targets {actual_target:06X}, expected {target_addr:06X}"

    actual_target_bank = (actual_target >> 16) & 0xFF
    if is_jsl or is_jml:
        if actual_target_bank != caller_bank:
            return "VALID_CROSS_BANK", f"JSL/JML to different bank {actual_target_bank:02X}"
        return "VALID_SAME_BANK", f"JSL/JML within same bank {actual_target_bank:02X}"
    if actual_target_bank != caller_bank:
        return "FAKE_CROSS_BANK", "JSR/JMP cannot target different bank - likely data misread"
    return "VALID_SAME_BANK", f"JSR/JMP within same bank {actual_target_bank:02X}"


def main():
    parser = argparse.ArgumentParser(description='Validate cross-bank callers')
    parser.add_argument('--rom', required=True, help='Path to ROM file')
    parser.add_argument('--target', required=True, help='Target address (e.g., C4:8010)')
    parser.add_argument('--callers', nargs='+', help='Caller addresses to validate')
    parser.add_argument('--json', action='store_true', help='Output JSON')

    args = parser.parse_args()

    target_bank, target_offset = parse_snes_address(args.target)
    target_addr = (target_bank << 16) | target_offset
    rom = Path(args.rom).read_bytes()
    results = []

    if not args.json:
        print(f"Validating callers to {args.target} ({target_addr:06X}):")
        print("=" * 60)

    for caller in args.callers or []:
        caller_bank, caller_offset = parse_snes_address(caller)
        caller_addr = (caller_bank << 16) | caller_offset
        status, reason = validate_caller(rom, caller_addr, target_addr)
        results.append(
            {
                'caller': caller,
                'caller_addr': caller_addr,
                'status': status,
                'reason': reason,
            }
        )

        if not args.json:
            status_icon = "OK" if status.startswith("VALID") else "NO" if status == "INVALID" else "WARN"
            print(f"{status_icon} {caller}: {status}")
            print(f"   {reason}")
            print()

    if args.json:
        print(json.dumps(results, indent=2))
        return

    valid_cross = sum(1 for r in results if r['status'] == 'VALID_CROSS_BANK')
    valid_same = sum(1 for r in results if r['status'] == 'VALID_SAME_BANK')
    fake = sum(1 for r in results if r['status'] == 'FAKE_CROSS_BANK')
    invalid = sum(1 for r in results if r['status'] == 'INVALID')

    print("=" * 60)
    print("Summary:")
    print(f"  Valid cross-bank: {valid_cross}")
    print(f"  Valid same-bank: {valid_same}")
    print(f"  Fake cross-bank: {fake}")
    print(f"  Invalid: {invalid}")


if __name__ == '__main__':
    main()
