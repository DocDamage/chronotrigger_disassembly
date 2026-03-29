#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from seam_triage_utils_v1 import (
    parse_snes_range,
    parse_snes_address,
    neighborhood,
    printable_ascii_ratio,
    zero_ff_ratio,
    repeated_pair_score,
    classify_start_byte,
    data_side_risk,
    load_dead_ranges,
    dead_range_match,
    classify_page_family,
)
from manifest_xref_utils import classify_caller_context, anchor_strength, iter_raw_callers
from xref_index_utils_v1 import choose_closed_ranges, load_xref_index, iter_index_hits


def effective_strength(anchor: str, caller_risk: str, target_risk: str, start_class: str, dead_match: bool) -> str:
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
    if start_class == 'soft_bad_start':
        pos = max(pos, 2)
    elif start_class == 'hard_bad_start':
        pos = 3
    if dead_match:
        pos = 3
    inv = {0: 'strong', 1: 'weak', 2: 'suspect', 3: 'invalid'}
    return inv[pos]


def iter_hits(rom_bytes: bytes, range_bank: int, start: int, end: int, xref_index_path: str | None):
    if xref_index_path:
        payload = load_xref_index(xref_index_path)
        yield from iter_index_hits(payload, range_bank, start, end)
        return
    for item in iter_raw_callers(rom_bytes):
        if item['target_bank'] != range_bank or not (start <= item['target_addr'] <= end):
            continue
        yield item


def main() -> int:
    parser = argparse.ArgumentParser(description='Score incoming raw xrefs into a SNES range using caller/target context, bad-start gating, dead-lane suppression, coarse page-family tagging, and optional xref index reuse')
    parser.add_argument('--rom', required=True)
    parser.add_argument('--range', dest='range_text', required=True)
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--closed-ranges-snapshot', default='')
    parser.add_argument('--xref-index', default='')
    parser.add_argument('--dead-ranges-config', default='tools/config/c3_dead_ranges_v1.json')
    parser.add_argument('--radius', type=int, default=16)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    bank, start, end = parse_snes_range(args.range_text)
    rom_bytes = Path(args.rom).read_bytes()
    closed_ranges = choose_closed_ranges(args.manifests_dir, args.closed_ranges_snapshot)
    dead_ranges = load_dead_ranges(args.dead_ranges_config)
    page_family, page_reasons, _ = classify_page_family(rom_bytes, args.range_text)

    hits: list[dict[str, object]] = []
    dead_lane_suppressed = 0
    hard_bad_start_hits = 0
    soft_bad_start_hits = 0

    for item in iter_hits(rom_bytes, bank, start, end, args.xref_index or None):
        validity = 'valid'
        if item['kind'] in {'JSR', 'JMP'} and item['caller_bank'] != bank:
            validity = 'invalid_bank_mismatch'
        caller_ctx = classify_caller_context(closed_ranges, str(item['caller']))
        anchor = anchor_strength(validity, str(caller_ctx['caller_status']))
        caller_bank, caller_addr = parse_snes_address(str(item['caller']))
        caller_blob = neighborhood(rom_bytes, caller_bank, caller_addr, args.radius)
        target_blob = neighborhood(rom_bytes, bank, int(item['target_addr']), args.radius)
        target_offset = (bank - 0xC0) * 0x10000 + int(item['target_addr'])
        start_byte = rom_bytes[target_offset]
        start_class, start_reason = classify_start_byte(start_byte)
        dead_match = dead_range_match(dead_ranges, bank, int(item['target_addr']))
        eff = effective_strength(anchor, data_side_risk(caller_blob), data_side_risk(target_blob), start_class, dead_match is not None)
        if dead_match is not None:
            dead_lane_suppressed += 1
        if start_class == 'hard_bad_start':
            hard_bad_start_hits += 1
        elif start_class == 'soft_bad_start':
            soft_bad_start_hits += 1
        flags = []
        if dead_match is not None:
            flags.append('dead_lane_suppressed')
        if start_class != 'clean_start':
            flags.append(start_reason)
        hits.append({
            'target': item['target'],
            'caller': item['caller'],
            'kind': item['kind'],
            'validity': validity,
            'anchor_strength': anchor,
            'effective_strength': eff,
            'caller_risk': data_side_risk(caller_blob),
            'target_risk': data_side_risk(target_blob),
            'start_byte': f'{start_byte:02X}',
            'start_class': start_class,
            'start_reason': start_reason,
            'dead_range': dead_match['range'] if dead_match else '',
            'dead_range_reason': dead_match.get('reason', '') if dead_match else '',
            'flags': flags,
            'page_family': page_family,
            'page_family_reasons': page_reasons,
            'caller_ascii_ratio': round(printable_ascii_ratio(caller_blob), 3),
            'caller_zero_ff_ratio': round(zero_ff_ratio(caller_blob), 3),
            'caller_repeated_pair_score': round(repeated_pair_score(caller_blob), 3),
            'target_ascii_ratio': round(printable_ascii_ratio(target_blob), 3),
            'target_zero_ff_ratio': round(zero_ff_ratio(target_blob), 3),
            'target_repeated_pair_score': round(repeated_pair_score(target_blob), 3),
            **caller_ctx,
        })

    hits.sort(key=lambda item: (str(item['target']), str(item['effective_strength']), str(item['caller'])))
    result = {
        'range': args.range_text,
        'page_family': page_family,
        'hit_count': len(hits),
        'dead_lane_suppressed_count': dead_lane_suppressed,
        'hard_bad_start_hit_count': hard_bad_start_hits,
        'soft_bad_start_hit_count': soft_bad_start_hits,
        'hits': hits,
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f'range: {args.range_text}')
        print(f'page_family: {page_family}')
        print(f'hit_count: {len(hits)}')
        print(f'dead_lane_suppressed_count: {dead_lane_suppressed}')
        print(f'hard_bad_start_hit_count: {hard_bad_start_hits}')
        print(f'soft_bad_start_hit_count: {soft_bad_start_hits}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
