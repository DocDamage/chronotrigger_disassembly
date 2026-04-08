#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterator

RANGE_RE = re.compile(r'^(?P<bank>[0-9A-Fa-f]{2}):(?P<start>[0-9A-Fa-f]{4})\.\.(?P=bank):(?P<end>[0-9A-Fa-f]{4})$')
ADDR_RE = re.compile(r'^(?P<bank>[0-9A-Fa-f]{2}):(?P<addr>[0-9A-Fa-f]{4})$')
OPEN_RANGE_RE = re.compile(r'^(?P<bank>[0-9A-Fa-f]{2}):(?P<start>[0-9A-Fa-f]{4})\.\.$')
CANONICAL_PASS_RE = re.compile(r'^pass\d+\.json$', re.IGNORECASE)


class RangeParseError(ValueError):
    pass


def parse_snes_address(text: str) -> tuple[int, int]:
    m = ADDR_RE.match(text.strip())
    if not m:
        raise RangeParseError(f'invalid SNES address: {text}')
    return int(m.group('bank'), 16), int(m.group('addr'), 16)


def parse_snes_range(text: str) -> tuple[int, int, int]:
    text = text.strip()
    m = RANGE_RE.match(text)
    if not m:
        open_match = OPEN_RANGE_RE.match(text)
        if open_match:
            bank = int(open_match.group('bank'), 16)
            start = int(open_match.group('start'), 16)
            return bank, start, 0xFFFF
        raise RangeParseError(f'invalid SNES range: {text}')
    bank = int(m.group('bank'), 16)
    start = int(m.group('start'), 16)
    end = int(m.group('end'), 16)
    if end < start:
        raise RangeParseError(f'range end before start: {text}')
    return bank, start, end


def format_snes_range(bank: int, start: int, end: int) -> str:
    return f'{bank:02X}:{start:04X}..{bank:02X}:{end:04X}'


def hirom_to_file_offset(bank: int, addr: int) -> int:
    if not (0 <= bank <= 0xFF and 0 <= addr <= 0xFFFF):
        raise RangeParseError(f'invalid SNES address: {bank:02X}:{addr:04X}')
    return ((bank & 0x3F) << 16) | addr


def range_file_offsets(range_text: str) -> tuple[int, int]:
    bank, start, end = parse_snes_range(range_text)
    return hirom_to_file_offset(bank, start), hirom_to_file_offset(bank, end)


def slice_rom_range(rom_bytes: bytes, range_text: str) -> bytes:
    start_off, end_off = range_file_offsets(range_text)
    return rom_bytes[start_off:end_off + 1]


def iter_manifest_paths(manifests_dir: str | Path) -> Iterator[Path]:
    for path in sorted(Path(manifests_dir).glob('pass*.json')):
        if path.is_file() and CANONICAL_PASS_RE.match(path.name):
            yield path


def file_offset_to_snes(offset: int) -> tuple[int, int]:
    bank = 0xC0 | ((offset >> 16) & 0x3F)
    addr = offset & 0xFFFF
    return bank, addr


def format_offset_as_snes(offset: int) -> str:
    bank, addr = file_offset_to_snes(offset)
    return f'{bank:02X}:{addr:04X}'


def iter_all_call_patterns(rom_bytes: bytes, target_bank: int, target_addr: int):
    jsl_pat = bytes([0x22, target_addr & 0xFF, (target_addr >> 8) & 0xFF, target_bank & 0xFF])
    jml_pat = bytes([0x5C, target_addr & 0xFF, (target_addr >> 8) & 0xFF, target_bank & 0xFF])
    jsr_pat = bytes([0x20, target_addr & 0xFF, (target_addr >> 8) & 0xFF])
    jmp_pat = bytes([0x4C, target_addr & 0xFF, (target_addr >> 8) & 0xFF])

    patterns = [('JSL', jsl_pat), ('JML', jml_pat), ('JSR', jsr_pat), ('JMP', jmp_pat)]
    for kind, pat in patterns:
        start = 0
        while True:
            idx = rom_bytes.find(pat, start)
            if idx < 0:
                break
            yield kind, idx
            start = idx + 1
