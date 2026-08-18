#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from snes_utils_hirom_v2 import format_snes_range, parse_snes_range, slice_rom_range
from manifest_xref_utils import anchor_strength, classify_caller_context, iter_raw_callers, load_closed_ranges


def signed_rel8(value: int) -> int:
    return value - 0x100 if value >= 0x80 else value


def detect_tiny_candidates(bank: int, start: int, data: bytes) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for idx, op in enumerate(data):
        addr = start + idx
        if op == 0x20 and idx + 3 < len(data) and data[idx + 3] == 0x60:
            target = data[idx + 1] | (data[idx + 2] << 8)
            results.append({'range': format_snes_range(bank, addr, addr + 3), 'pattern': 'jsr_rts_wrapper', 'target': f'{bank:02X}:{target:04X}', 'confidence': 'high'})
        elif op == 0x22 and idx + 4 < len(data) and data[idx + 4] == 0x60:
            target = data[idx + 1] | (data[idx + 2] << 8)
            target_bank = data[idx + 3]
            results.append({'range': format_snes_range(bank, addr, addr + 4), 'pattern': 'jsl_rts_wrapper', 'target': f'{target_bank:02X}:{target:04X}', 'confidence': 'high'})
        elif op == 0x6B:
            results.append({'range': format_snes_range(bank, addr, addr), 'pattern': 'rtl_stub', 'target': '', 'confidence': 'high'})
        elif op == 0x80 and idx + 1 < len(data):
            dest = addr + 2 + signed_rel8(data[idx + 1])
            results.append({'range': format_snes_range(bank, addr, addr + 1), 'pattern': 'bra_landing_pad', 'target': f'{bank:02X}:{dest & 0xFFFF:04X}', 'confidence': 'medium'})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description='Run the upgraded candidate triage flow on a C3 seam')
    parser.add_argument('--rom', required=True)
    parser.add_argument('--range', dest='range_text', required=True)
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--top', type=int, default=12)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    bank, start, end = parse_snes_range(args.range_text)
    rom_bytes = Path(args.rom).read_bytes()
    data = slice_rom_range(rom_bytes, args.range_text)
    closed_ranges = load_closed_ranges(args.manifests_dir)

    tiny = detect_tiny_candidates(bank, start, data)
    rank = {'strong': 0, 'weak': 1, 'suspect': 2, 'invalid': 3}
    grouped: dict[str, dict[str, object]] = {}
    for item in iter_raw_callers(rom_bytes):
        if item['target_bank'] != bank or not (start <= item['target_addr'] <= end):
            continue
        caller_ctx = classify_caller_context(closed_ranges, str(item['caller']))
        validity = 'valid'
        if item['kind'] in {'JSR', 'JMP'} and item['caller_bank'] != bank:
            validity = 'invalid_bank_mismatch'
        strength = anchor_strength(validity, caller_ctx['caller_status'])
        bucket = grouped.setdefault(
            str(item['target']),
            {'target': item['target'], 'strong_anchor_count': 0, 'weak_anchor_count': 0, 'suspect_anchor_count': 0, 'invalid_count': 0, 'hits': []},
        )
        if strength == 'strong':
            bucket['strong_anchor_count'] += 1
        elif strength == 'weak':
            bucket['weak_anchor_count'] += 1
        elif strength == 'suspect':
            bucket['suspect_anchor_count'] += 1
        else:
            bucket['invalid_count'] += 1
        bucket['hits'].append({'kind': item['kind'], 'caller': item['caller'], 'anchor_strength': strength, **caller_ctx})

    targets = list(grouped.values())
    targets.sort(key=lambda item: (-int(item['strong_anchor_count']), -int(item['weak_anchor_count']), int(item['suspect_anchor_count']), int(item['invalid_count']), str(item['target'])))
    for item in targets:
        item['hits'].sort(key=lambda hit: (rank.get(str(hit['anchor_strength']), 9), str(hit['caller'])))

    result = {'range': args.range_text, 'tiny_candidate_count': len(tiny), 'tiny_candidates': tiny, 'target_count': len(targets), 'top_targets': targets[: args.top]}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"range: {args.range_text}")
        print(f"tiny_candidate_count: {len(tiny)}")
        for item in tiny[:20]:
            target = f" -> {item['target']}" if item['target'] else ''
            print(f"  tiny {item['range']}: {item['pattern']}{target} ({item['confidence']})")
        print(f"target_count: {len(targets)}")
        for item in targets[: args.top]:
            print(f"  {item['target']}: strong={item['strong_anchor_count']} weak={item['weak_anchor_count']} suspect={item['suspect_anchor_count']} invalid={item['invalid_count']}")
            for hit in item['hits'][:8]:
                print(f"    {hit['kind']} from {hit['caller']} -> {hit['anchor_strength']} ({hit['caller_status']})")
                if hit['caller_range']:
                    print(f"      caller_range: {hit['caller_range']} ({hit['caller_label']})")
            if len(item['hits']) > 8:
                print(f"      ... truncated {len(item['hits']) - 8} additional hits")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
