#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from seam_triage_utils_v1 import (
    parse_snes_range,
    format_snes_range,
    printable_ascii_ratio,
    zero_ff_ratio,
    repeated_pair_score,
    classify_start_byte,
    BARRIERS,
    RETURNS,
)
from manifest_xref_utils import iter_raw_callers

LIKELY_PROLOG = {0xA9, 0xA2, 0xA0, 0x08, 0x48, 0xDA, 0x5A, 0x20, 0x22}

def score_candidate(blob: bytes, start_byte: int, target_inside_offset: int) -> int:
    score = 0
    start_class, _ = classify_start_byte(start_byte)
    if start_class == 'hard_bad_start':
        score -= 4
    elif start_class == 'soft_bad_start':
        score -= 2
    else:
        score += 1
    if start_byte in LIKELY_PROLOG:
        score += 2
    if any(b in RETURNS for b in blob):
        score += 2
    if printable_ascii_ratio(blob) >= 0.45:
        score -= 2
    if zero_ff_ratio(blob) >= 0.25:
        score -= 2
    if repeated_pair_score(blob) >= 0.35:
        score -= 2
    if target_inside_offset > 0:
        score += 1
    return score

def main() -> int:
    parser = argparse.ArgumentParser(description='Backtrack from hot raw targets to the nearest plausible owner boundary candidates')
    parser.add_argument('--rom', required=True)
    parser.add_argument('--range', dest='range_text', required=True)
    parser.add_argument('--max-back', type=int, default=16)
    parser.add_argument('--lookahead', type=int, default=24)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    bank, start, end = parse_snes_range(args.range_text)
    rom_bytes = Path(args.rom).read_bytes()

    seen_targets = set()
    targets = []
    for item in iter_raw_callers(rom_bytes):
        if item['target_bank'] != bank or not (start <= item['target_addr'] <= end):
            continue
        if item['target'] in seen_targets:
            continue
        seen_targets.add(item['target'])
        targets.append(item['target'])

    out = []
    for target_text in sorted(targets):
        _, target_addr = target_text.split(':')
        target_addr = int(target_addr, 16)
        target_off = (bank - 0xC0) * 0x10000 + target_addr
        best = None
        for delta in range(0, args.max_back + 1):
            cand_addr = target_addr - delta
            if cand_addr < start:
                break
            if delta > 0 and rom_bytes[(bank - 0xC0) * 0x10000 + cand_addr - 1] in BARRIERS:
                break
            cand_off = (bank - 0xC0) * 0x10000 + cand_addr
            blob = rom_bytes[cand_off:min(len(rom_bytes), target_off + args.lookahead + 1)]
            score = score_candidate(blob, rom_bytes[cand_off], target_addr - cand_addr)
            item = {
                'candidate_start': f'{bank:02X}:{cand_addr:04X}',
                'target': f'{bank:02X}:{target_addr:04X}',
                'score': score,
                'distance_to_target': target_addr - cand_addr,
                'start_byte': f'{rom_bytes[cand_off]:02X}',
                'start_class': classify_start_byte(rom_bytes[cand_off])[0],
                'ascii_ratio': round(printable_ascii_ratio(blob), 3),
                'zero_ff_ratio': round(zero_ff_ratio(blob), 3),
                'repeated_pair_score': round(repeated_pair_score(blob), 3),
                'candidate_range': format_snes_range(bank, cand_addr, min(end, target_addr + args.lookahead)),
            }
            if best is None or item['score'] > best['score'] or (item['score'] == best['score'] and item['distance_to_target'] > best['distance_to_target']):
                best = item
        if best:
            out.append(best)

    out.sort(key=lambda item: (-int(item['score']), item['target']))
    result = {'range': args.range_text, 'candidate_count': len(out), 'candidates': out}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f'range: {args.range_text}')
        print(f'candidate_count: {len(out)}')
        for item in out:
            print(f"  {item['target']} -> best_start={item['candidate_start']} score={item['score']} distance={item['distance_to_target']} start={item['start_byte']} {item['start_class']}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
