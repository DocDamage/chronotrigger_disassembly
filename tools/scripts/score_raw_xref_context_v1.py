#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from manifest_xref_utils import anchor_strength, classify_caller_context, iter_raw_callers, load_closed_ranges
from snes_utils import hirom_to_file_offset, parse_snes_address, parse_snes_range


def snes_to_offset(bank: int, addr: int) -> int:
    return hirom_to_file_offset(bank, addr)


def neighborhood(rom_bytes: bytes, bank: int, addr: int, radius: int) -> bytes:
    center = snes_to_offset(bank, addr)
    start = max(0, center - radius)
    end = min(len(rom_bytes), center + radius + 1)
    return rom_bytes[start:end]


def printable_ascii_ratio(blob: bytes) -> float:
    if not blob:
        return 0.0
    hits = sum(1 for b in blob if 0x20 <= b <= 0x7E)
    return hits / len(blob)


def zero_ff_ratio(blob: bytes) -> float:
    if not blob:
        return 0.0
    hits = sum(1 for b in blob if b in (0x00, 0xFF))
    return hits / len(blob)


def branch_ratio(blob: bytes) -> float:
    branches = {0x10, 0x30, 0x50, 0x70, 0x80, 0x82, 0x90, 0xB0, 0xD0, 0xF0}
    if not blob:
        return 0.0
    hits = sum(1 for b in blob if b in branches)
    return hits / len(blob)


def return_count(blob: bytes) -> int:
    return sum(1 for b in blob if b in (0x60, 0x6B, 0x40))


def repeated_pair_score(blob: bytes) -> float:
    if len(blob) < 4:
        return 0.0
    pairs = [blob[i:i+2] for i in range(0, len(blob) - 1, 2)]
    if not pairs:
        return 0.0
    distinct = len(set(pairs))
    return 1.0 - (distinct / len(pairs))


def data_side_risk(blob: bytes) -> str:
    ascii_r = printable_ascii_ratio(blob)
    zeroff_r = zero_ff_ratio(blob)
    rep_r = repeated_pair_score(blob)
    branch_r = branch_ratio(blob)
    returns = return_count(blob)
    score = 0
    if ascii_r >= 0.35:
        score += 2
    elif ascii_r >= 0.22:
        score += 1
    if zeroff_r >= 0.35:
        score += 2
    elif zeroff_r >= 0.22:
        score += 1
    if rep_r >= 0.45:
        score += 2
    elif rep_r >= 0.30:
        score += 1
    if branch_r >= 0.18 and returns == 0:
        score += 1
    if score >= 4:
        return 'very_high'
    if score >= 2:
        return 'high'
    if score >= 1:
        return 'medium'
    return 'low'


def effective_strength(anchor: str, caller_risk: str, target_risk: str) -> str:
    rank = {'strong': 0, 'weak': 1, 'suspect': 2, 'invalid': 3}
    pos = rank.get(anchor, 3)
    if caller_risk in {'very_high', 'high'}:
        pos = max(pos, 2)
    elif caller_risk == 'medium':
        pos = max(pos, 1)
    if target_risk == 'very_high':
        pos = max(pos, 2)
    elif target_risk == 'high':
        pos = max(pos, 1)
    inv = {0: 'strong', 1: 'weak', 2: 'suspect', 3: 'invalid'}
    return inv[pos]


def main() -> int:
    parser = argparse.ArgumentParser(description='Score incoming raw xrefs into a SNES range using neighborhood heuristics for data-side caller/target risk')
    parser.add_argument('--rom', required=True)
    parser.add_argument('--range', dest='range_text', required=True)
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--radius', type=int, default=16)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    bank, start, end = parse_snes_range(args.range_text)
    rom_bytes = Path(args.rom).read_bytes()
    closed_ranges = load_closed_ranges(args.manifests_dir)

    hits: list[dict[str, object]] = []
    for item in iter_raw_callers(rom_bytes):
        if item['target_bank'] != bank or not (start <= item['target_addr'] <= end):
            continue
        validity = 'valid'
        if item['kind'] in {'JSR', 'JMP'} and item['caller_bank'] != bank:
            validity = 'invalid_bank_mismatch'
        caller_ctx = classify_caller_context(closed_ranges, str(item['caller']))
        anchor = anchor_strength(validity, str(caller_ctx['caller_status']))
        caller_bank, caller_addr = parse_snes_address(str(item['caller']))
        caller_blob = neighborhood(rom_bytes, caller_bank, caller_addr, args.radius)
        target_blob = neighborhood(rom_bytes, bank, int(item['target_addr']), args.radius)
        caller_risk = data_side_risk(caller_blob)
        target_risk = data_side_risk(target_blob)
        hits.append(
            {
                'target': item['target'],
                'caller': item['caller'],
                'kind': item['kind'],
                'validity': validity,
                'anchor_strength': anchor,
                'effective_strength': effective_strength(anchor, caller_risk, target_risk),
                'caller_risk': caller_risk,
                'target_risk': target_risk,
                'caller_ascii_ratio': round(printable_ascii_ratio(caller_blob), 3),
                'caller_zero_ff_ratio': round(zero_ff_ratio(caller_blob), 3),
                'caller_repeated_pair_score': round(repeated_pair_score(caller_blob), 3),
                'target_ascii_ratio': round(printable_ascii_ratio(target_blob), 3),
                'target_zero_ff_ratio': round(zero_ff_ratio(target_blob), 3),
                'target_repeated_pair_score': round(repeated_pair_score(target_blob), 3),
                **caller_ctx,
            }
        )

    hits.sort(key=lambda item: (str(item['target']), str(item['effective_strength']), str(item['caller'])))
    result = {'range': args.range_text, 'hit_count': len(hits), 'hits': hits}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f'range: {args.range_text}')
        print(f'hit_count: {len(hits)}')
        for hit in hits:
            print(f"  {hit['caller']} {hit['kind']} -> {hit['target']} | anchor={hit['anchor_strength']} effective={hit['effective_strength']} caller_risk={hit['caller_risk']} target_risk={hit['target_risk']}")
            if hit['caller_range']:
                print(f"    caller_range: {hit['caller_range']} ({hit['caller_label']})")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
