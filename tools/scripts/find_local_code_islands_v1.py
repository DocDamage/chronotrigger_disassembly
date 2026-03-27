#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from snes_utils_hirom_v2 import parse_snes_range, format_snes_range, slice_rom_range
except Exception:
    def parse_snes_range(text: str):
        left, right = text.split('..')
        bank_s, start_s = left.split(':')
        bank2_s, end_s = right.split(':')
        if bank_s != bank2_s:
            raise ValueError('cross-bank ranges not supported')
        return int(bank_s, 16), int(start_s, 16), int(end_s, 16)

    def format_snes_range(bank: int, start: int, end: int) -> str:
        return f'{bank:02X}:{start:04X}..{bank:02X}:{end:04X}'

    def slice_rom_range(rom_bytes: bytes, range_text: str) -> bytes:
        bank, start, end = parse_snes_range(range_text)
        if bank < 0xC0:
            raise ValueError('unsupported bank')
        base = (bank - 0xC0) * 0x10000
        return rom_bytes[base + start: base + end + 1]

BRANCHES = {0x10, 0x30, 0x50, 0x70, 0x80, 0x82, 0x90, 0xB0, 0xD0, 0xF0}
RETURNS = {0x60, 0x6B, 0x40}
CALLS = {0x20, 0x22, 0x4C, 0x5C}
STACKISH = {0x08, 0x28, 0x48, 0x68, 0xDA, 0xFA}
BARRIERS = {0x00, 0x02, 0x42, 0xFF}


def ascii_ratio(blob: bytes) -> float:
    if not blob:
        return 0.0
    return sum(1 for b in blob if 0x20 <= b <= 0x7E) / len(blob)


def repeated_pair_score(blob: bytes) -> float:
    if len(blob) < 4:
        return 0.0
    pairs = [blob[i:i+2] for i in range(0, len(blob) - 1, 2)]
    if not pairs:
        return 0.0
    return 1.0 - (len(set(pairs)) / len(pairs))


def score_blob(blob: bytes) -> dict[str, object]:
    branches = sum(1 for b in blob if b in BRANCHES)
    returns = [i for i, b in enumerate(blob) if b in RETURNS]
    calls = sum(1 for b in blob if b in CALLS)
    stackish = sum(1 for b in blob if b in STACKISH)
    bad = sum(1 for b in blob if b in BARRIERS)
    score = 0
    if returns:
        score += 3
    if calls:
        score += 2
    if branches >= 1:
        score += 1
    if stackish:
        score += 1
    if bad:
        score -= bad * 2
    a_ratio = ascii_ratio(blob)
    r_score = repeated_pair_score(blob)
    if a_ratio >= 0.30:
        score -= 2
    if r_score >= 0.45:
        score -= 2
    return {
        'score': score,
        'branch_count': branches,
        'return_offsets': returns,
        'call_count': calls,
        'stackish_count': stackish,
        'barrier_count': bad,
        'ascii_ratio': round(a_ratio, 3),
        'repeated_pair_score': round(r_score, 3),
    }


def find_return_anchored_windows(data: bytes, max_back: int, min_width: int) -> list[tuple[int, int]]:
    windows: list[tuple[int, int]] = []
    for end, b in enumerate(data):
        if b not in RETURNS:
            continue
        start = max(0, end - max_back)
        last_barrier = None
        for i in range(start, end):
            if data[i] in BARRIERS:
                last_barrier = i
        if last_barrier is not None:
            start = last_barrier + 1
        if end - start + 1 >= min_width:
            windows.append((start, end))
    return windows


def dedupe_windows(windows: list[tuple[int, int]]) -> list[tuple[int, int]]:
    seen = set()
    out = []
    for item in sorted(windows):
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description='Find unsupported code-like local islands inside a SNES range, especially return-anchored helper pockets')
    parser.add_argument('--rom', required=True)
    parser.add_argument('--range', dest='range_text', required=True)
    parser.add_argument('--min-width', type=int, default=5)
    parser.add_argument('--max-back', type=int, default=24)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    bank, start, _ = parse_snes_range(args.range_text)
    data = slice_rom_range(Path(args.rom).read_bytes(), args.range_text)

    candidates = []
    for rel_start, rel_end in dedupe_windows(find_return_anchored_windows(data, args.max_back, args.min_width)):
        blob = data[rel_start:rel_end + 1]
        scored = score_blob(blob)
        if scored['score'] < 2:
            continue
        first_return = scored['return_offsets'][0] if scored['return_offsets'] else None
        candidates.append(
            {
                'range': format_snes_range(bank, start + rel_start, start + rel_end),
                'score': scored['score'],
                'width': len(blob),
                'call_count': scored['call_count'],
                'branch_count': scored['branch_count'],
                'stackish_count': scored['stackish_count'],
                'return_count': len(scored['return_offsets']),
                'first_return_address': f'{bank:02X}:{start + rel_start + first_return:04X}' if first_return is not None else '',
                'ascii_ratio': scored['ascii_ratio'],
                'repeated_pair_score': scored['repeated_pair_score'],
            }
        )

    candidates.sort(key=lambda item: (-int(item['score']), -int(item['width']), str(item['range'])))
    result = {'range': args.range_text, 'island_count': len(candidates), 'islands': candidates}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f'range: {args.range_text}')
        print(f'island_count: {len(candidates)}')
        for item in candidates:
            rtn = f" first_return={item['first_return_address']}" if item['first_return_address'] else ''
            print(f"  {item['range']}: score={item['score']} width={item['width']} calls={item['call_count']} branches={item['branch_count']} returns={item['return_count']}{rtn}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
