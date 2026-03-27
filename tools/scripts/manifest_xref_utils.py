#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Optional

from snes_utils_hirom_v2 import file_offset_to_snes, iter_manifest_paths, parse_snes_address, parse_snes_range


EXECUTABLE_KINDS = {
    'owner',
    'helper',
    'veneer',
    'tail_fragment',
    'stub',
    'entry_stub',
    'trampoline',
    'wrapper',
}

DATA_KINDS = {
    'data',
    'text_marker',
    'marker',
    'table',
    'padding',
    'padding_or_sparse_data',
    'inline_text_or_marker',
}


@dataclass(frozen=True)
class ClosedRange:
    bank: int
    start: int
    end: int
    kind: str
    label: str
    confidence: str
    pass_number: int

    @property
    def width(self) -> int:
        return self.end - self.start + 1

    @property
    def range_text(self) -> str:
        return f'{self.bank:02X}:{self.start:04X}..{self.bank:02X}:{self.end:04X}'

    def contains(self, bank: int, addr: int) -> bool:
        return self.bank == bank and self.start <= addr <= self.end


def classify_kind(kind: str) -> str:
    if kind in EXECUTABLE_KINDS:
        return 'code'
    if kind in DATA_KINDS:
        return 'data'
    if kind.endswith('_stub') or kind.endswith('_wrapper'):
        return 'code'
    return 'unknown'


def load_closed_ranges(manifests_dir: str | Path) -> list[ClosedRange]:
    ranges: list[ClosedRange] = []
    for path in iter_manifest_paths(manifests_dir):
        data = json.loads(Path(path).read_text(encoding='utf-8'))
        pass_number = int(data.get('pass_number', 0))
        for item in data.get('closed_ranges', []):
            bank, start, end = parse_snes_range(item['range'])
            ranges.append(
                ClosedRange(
                    bank=bank,
                    start=start,
                    end=end,
                    kind=item.get('kind', 'unknown'),
                    label=item.get('label', ''),
                    confidence=item.get('confidence', 'unknown'),
                    pass_number=pass_number,
                )
            )
    ranges.sort(key=lambda item: (item.bank, item.start, item.end, item.pass_number))
    return ranges


def find_covering_range(closed_ranges: Iterable[ClosedRange], bank: int, addr: int) -> Optional[ClosedRange]:
    matches = [item for item in closed_ranges if item.contains(bank, addr)]
    if not matches:
        return None
    matches.sort(key=lambda item: (item.width, -item.pass_number))
    return matches[0]


def classify_caller_context(closed_ranges: Iterable[ClosedRange], caller_text: str) -> dict[str, str]:
    bank, addr = parse_snes_address(caller_text)
    match = find_covering_range(closed_ranges, bank, addr)
    if match is None:
        return {
            'caller_status': 'unresolved',
            'caller_range': '',
            'caller_kind_family': 'unknown',
            'caller_label': '',
            'caller_confidence': 'unknown',
        }
    family = classify_kind(match.kind)
    if family == 'code':
        status = 'resolved_code'
    elif family == 'data':
        status = 'resolved_data'
    else:
        status = 'resolved_unknown'
    return {
        'caller_status': status,
        'caller_range': match.range_text,
        'caller_kind_family': family,
        'caller_label': match.label,
        'caller_confidence': match.confidence,
    }


def anchor_strength(validity: str, caller_status: str) -> str:
    if validity != 'valid':
        return 'invalid'
    if caller_status == 'resolved_code':
        return 'strong'
    if caller_status == 'unresolved':
        return 'weak'
    if caller_status == 'resolved_data':
        return 'suspect'
    return 'weak'


def iter_raw_callers(rom_bytes: bytes) -> Iterator[dict[str, object]]:
    limit = len(rom_bytes)
    for offset in range(limit):
        op = rom_bytes[offset]
        caller_bank, caller_addr = file_offset_to_snes(offset)
        caller_text = f'{caller_bank:02X}:{caller_addr:04X}'
        if op in (0x20, 0x4C) and offset + 2 < limit:
            target_addr = rom_bytes[offset + 1] | (rom_bytes[offset + 2] << 8)
            kind = 'JSR' if op == 0x20 else 'JMP'
            yield {
                'kind': kind,
                'caller': caller_text,
                'caller_bank': caller_bank,
                'target_bank': caller_bank,
                'target_addr': target_addr,
                'target': f'{caller_bank:02X}:{target_addr:04X}',
                'width': 3,
            }
        elif op in (0x22, 0x5C) and offset + 3 < limit:
            target_addr = rom_bytes[offset + 1] | (rom_bytes[offset + 2] << 8)
            target_bank = rom_bytes[offset + 3]
            kind = 'JSL' if op == 0x22 else 'JML'
            yield {
                'kind': kind,
                'caller': caller_text,
                'caller_bank': caller_bank,
                'target_bank': target_bank,
                'target_addr': target_addr,
                'target': f'{target_bank:02X}:{target_addr:04X}',
                'width': 4,
            }
