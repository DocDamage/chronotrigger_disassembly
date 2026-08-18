#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from snes_utils import hirom_to_file_offset, parse_snes_range

BRANCHES = {0x10, 0x30, 0x50, 0x70, 0x80, 0x82, 0x90, 0xB0, 0xD0, 0xF0}
RETURNS = {0x60, 0x6B, 0x40}
CALLS = {0x20, 0x22, 0x4C, 0x5C}
STACKISH = {0x08, 0x28, 0x48, 0x68, 0xDA, 0xFA}
WRITEISH = {0x8D, 0x8F, 0x85, 0x95, 0x99, 0x9D, 0x9F}


def format_snes(bank: int, addr: int) -> str:
    return f'{bank:02X}:{addr:04X}'


def snes_to_offset(bank: int, addr: int) -> int:
    return hirom_to_file_offset(bank, addr)


def printable_ascii_ratio(blob: bytes) -> float:
    return (sum(1 for b in blob if 0x20 <= b <= 0x7E) / len(blob)) if blob else 0.0


def zero_ratio(blob: bytes) -> float:
    return (blob.count(0x00) / len(blob)) if blob else 0.0


def ff_ratio(blob: bytes) -> float:
    return (blob.count(0xFF) / len(blob)) if blob else 0.0


def zero_ff_ratio(blob: bytes) -> float:
    return (sum(1 for b in blob if b in (0x00, 0xFF)) / len(blob)) if blob else 0.0


def repeated_pair_score(blob: bytes) -> float:
    if len(blob) < 4:
        return 0.0
    pairs = [blob[i:i+2] for i in range(0, len(blob) - 1, 2)]
    if not pairs:
        return 0.0
    return 1.0 - (len(set(pairs)) / len(pairs))


def opcode_ratio(blob: bytes, ops: set[int]) -> float:
    return (sum(1 for b in blob if b in ops) / len(blob)) if blob else 0.0


def page_label(blob: bytes) -> tuple[str, list[str]]:
    ascii_r = printable_ascii_ratio(blob)
    zeroff_r = zero_ff_ratio(blob)
    rep_r = repeated_pair_score(blob)
    branch_r = opcode_ratio(blob, BRANCHES)
    ret_r = opcode_ratio(blob, RETURNS)
    call_r = opcode_ratio(blob, CALLS)
    write_r = opcode_ratio(blob, WRITEISH)
    reasons: list[str] = []

    if ascii_r >= 0.55:
        reasons.append('ascii_very_high')
        return 'text_heavy_mixed', reasons
    if ascii_r >= 0.38 and rep_r >= 0.05:
        reasons.extend(['ascii_high', 'repeated_pairs_present'])
        return 'text_table_mixed', reasons
    if rep_r >= 0.22 and zeroff_r >= 0.18:
        reasons.extend(['repeated_pairs_high', 'zero_ff_high'])
        return 'pointer_table_risk', reasons
    if branch_r >= 0.08 and ret_r >= 0.008 and call_r < 0.035 and ascii_r < 0.33:
        reasons.extend(['branches_present', 'returns_present', 'calls_light'])
        return 'local_control_blob', reasons
    if call_r >= 0.03 and branch_r >= 0.05 and ascii_r < 0.35 and rep_r < 0.15:
        reasons.extend(['calls_present', 'branches_present'])
        return 'mixed_executable_looking', reasons
    if write_r >= 0.03 and ascii_r < 0.30:
        reasons.append('write_density')
        return 'register_write_mixed', reasons
    if zeroff_r >= 0.22:
        reasons.append('zero_ff_high')
        return 'padding_or_data_mixed', reasons
    reasons.append('no_clean_owner_signal')
    return 'mixed_unknown', reasons


def iter_pages(bank: int, start: int, end: int) -> Iterable[tuple[int, int, int]]:
    page = start & 0xFF00
    final_page = end & 0xFF00
    while page <= final_page:
        yield bank, page, min(page + 0xFF, end)
        page += 0x100


def summarize_page(bank: int, page_start: int, page_end: int, rom_bytes: bytes) -> dict[str, object]:
    blob = rom_bytes[snes_to_offset(bank, page_start): snes_to_offset(bank, page_end) + 1]
    label, reasons = page_label(blob)
    return {
        'range': f'{format_snes(bank, page_start)}..{format_snes(bank, page_end)}',
        'ascii_ratio': round(printable_ascii_ratio(blob), 3),
        'zero_ratio': round(zero_ratio(blob), 3),
        'ff_ratio': round(ff_ratio(blob), 3),
        'zero_ff_ratio': round(zero_ff_ratio(blob), 3),
        'repeated_pair_score': round(repeated_pair_score(blob), 3),
        'branch_ratio': round(opcode_ratio(blob, BRANCHES), 3),
        'return_ratio': round(opcode_ratio(blob, RETURNS), 3),
        'call_ratio': round(opcode_ratio(blob, CALLS), 3),
        'stackish_ratio': round(opcode_ratio(blob, STACKISH), 3),
        'write_ratio': round(opcode_ratio(blob, WRITEISH), 3),
        'label': label,
        'reasons': reasons,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description='Score page-level mixedness across a SNES range')
    ap.add_argument('--rom', required=True)
    ap.add_argument('--range', dest='range_text', required=True)
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    bank, start, end = parse_snes_range(args.range_text)
    rom_bytes = Path(args.rom).read_bytes()
    pages = [summarize_page(b, ps, pe, rom_bytes) for b, ps, pe in iter_pages(bank, start, end)]
    out = {'range': args.range_text, 'page_count': len(pages), 'pages': pages}
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(f'range: {args.range_text}')
        for page in pages:
            print(
                f"  {page['range']}: label={page['label']} ascii={page['ascii_ratio']:.3f} zero={page['zero_ratio']:.3f} ff={page['ff_ratio']:.3f} repeated_pair={page['repeated_pair_score']:.3f}"
            )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
