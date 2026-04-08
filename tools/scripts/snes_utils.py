from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, Iterator, Tuple
import json

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


def load_rom_bytes(rom_path: str | Path) -> bytes:
    return Path(rom_path).read_bytes()


def slice_rom_range(rom_bytes: bytes, range_text: str) -> bytes:
    start_off, end_off = range_file_offsets(range_text)
    return rom_bytes[start_off:end_off + 1]


def iter_manifest_paths(manifests_dir: str | Path) -> Iterator[Path]:
    for path in sorted(Path(manifests_dir).glob('pass*.json')):
        if path.is_file() and CANONICAL_PASS_RE.match(path.name):
            yield path


def manifest_pass_number(data: dict, path: str | Path | None = None) -> int:
    raw = data.get('pass_number', data.get('pass_num'))
    if raw is not None:
        return int(raw)
    if path is not None:
        match = re.match(r'^pass(\d+)\.json$', Path(path).name, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return 0


def load_manifest(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding='utf-8'))


def manifest_schema_name(data: dict) -> str:
    if 'closed_ranges' in data:
        return 'canonical_closed_ranges'
    if 'targets' in data:
        return 'legacy_targets'
    return 'unknown'


def manifest_live_seam(data: dict) -> str:
    return str(data.get('live_seam_after_pass') or data.get('region') or '')


def score_to_confidence(score: object) -> str:
    try:
        value = int(score)
    except Exception:
        return 'unknown'
    if value >= 8:
        return 'high'
    if value >= 6:
        return 'medium-high'
    if value >= 4:
        return 'medium'
    return 'low'


def manifest_closed_ranges(data: dict) -> list[dict]:
    closed_ranges = data.get('closed_ranges')
    if isinstance(closed_ranges, list):
        return [item for item in closed_ranges if isinstance(item, dict) and item.get('range')]

    normalized: list[dict] = []
    for item in data.get('targets', []):
        if not isinstance(item, dict):
            continue
        range_text = item.get('range')
        if not range_text:
            continue
        normalized.append(
            {
                'range': range_text,
                'kind': item.get('kind') or 'owner',
                'label': item.get('label') or data.get('pass_name') or 'legacy_target',
                'confidence': item.get('confidence') or score_to_confidence(item.get('score')),
            }
        )
    return normalized


def ascii_ratio(data: bytes) -> float:
    if not data:
        return 0.0
    count = sum(1 for b in data if b in b'\t\n\r' or 0x20 <= b <= 0x7E)
    return count / len(data)


def zero_ratio(data: bytes) -> float:
    if not data:
        return 0.0
    return data.count(0) / len(data)


def unique_ratio(data: bytes) -> float:
    if not data:
        return 0.0
    return len(set(data)) / len(data)


def opcode_hint_score(data: bytes) -> int:
    opcodes = {0x20, 0x22, 0x4C, 0x5C, 0x60, 0x6B, 0x08, 0x28, 0x2B, 0xAB, 0xC2, 0xE2, 0xA9, 0xA2, 0xA0, 0x8D, 0x9C, 0xAD}
    return sum(1 for b in data if b in opcodes)


def iter_all_call_patterns(rom_bytes: bytes, target_bank: int, target_addr: int) -> Iterator[tuple[str, int]]:
    # JSL absolute long: 22 ll hh bb
    jsl_pat = bytes([0x22, target_addr & 0xFF, (target_addr >> 8) & 0xFF, target_bank & 0xFF])
    # JML absolute long: 5C ll hh bb
    jml_pat = bytes([0x5C, target_addr & 0xFF, (target_addr >> 8) & 0xFF, target_bank & 0xFF])
    # JSR absolute: 20 ll hh (same bank only)
    jsr_pat = bytes([0x20, target_addr & 0xFF, (target_addr >> 8) & 0xFF])
    # JMP absolute: 4C ll hh (same bank only)
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


def file_offset_to_snes(offset: int) -> tuple[int, int]:
    if offset < 0:
        raise RangeParseError(f'invalid file offset: {offset}')
    bank = 0xC0 | ((offset >> 16) & 0x3F)
    addr = offset & 0xFFFF
    return bank, addr


def format_offset_as_snes(offset: int) -> str:
    bank, addr = file_offset_to_snes(offset)
    return f'{bank:02X}:{addr:04X}'
