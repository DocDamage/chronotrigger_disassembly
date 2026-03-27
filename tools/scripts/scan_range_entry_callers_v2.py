#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from snes_utils_hirom_v2 import parse_snes_range
from manifest_xref_utils import anchor_strength, classify_caller_context, iter_raw_callers, load_closed_ranges


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Scan a SNES range for incoming raw call/jump targets with bank-aware caller scoring (fixed summary counters)'
    )
    parser.add_argument('--rom', required=True)
    parser.add_argument('--range', dest='range_text', required=True)
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--min-strength', choices=['strong', 'weak', 'suspect', 'invalid', 'any'], default='any')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    bank, start, end = parse_snes_range(args.range_text)
    rom_bytes = Path(args.rom).read_bytes()
    closed_ranges = load_closed_ranges(args.manifests_dir)

    rank = {'strong': 0, 'weak': 1, 'suspect': 2, 'invalid': 3}
    ceiling = 99 if args.min_strength == 'any' else rank[args.min_strength]

    hits: list[dict[str, object]] = []
    for item in iter_raw_callers(rom_bytes):
        if item['target_bank'] != bank or not (start <= item['target_addr'] <= end):
            continue
        caller_ctx = classify_caller_context(closed_ranges, str(item['caller']))
        validity = 'valid'
        if item['kind'] in {'JSR', 'JMP'} and item['caller_bank'] != bank:
            validity = 'invalid_bank_mismatch'
        strength = anchor_strength(validity, caller_ctx['caller_status'])
        if rank.get(strength, 99) > ceiling:
            continue
        hits.append(
            {
                'target': item['target'],
                'kind': item['kind'],
                'caller': item['caller'],
                'validity': validity,
                'anchor_strength': strength,
                **caller_ctx,
            }
        )

    hits.sort(key=lambda item: (str(item['target']), rank.get(str(item['anchor_strength']), 9), str(item['caller'])))
    grouped: dict[str, dict[str, object]] = {}
    counter_map = {
        'strong': 'strong_anchor_count',
        'weak': 'weak_anchor_count',
        'suspect': 'suspect_anchor_count',
        'invalid': 'invalid_count',
    }
    for hit in hits:
        bucket = grouped.setdefault(
            str(hit['target']),
            {
                'target': hit['target'],
                'strong_anchor_count': 0,
                'weak_anchor_count': 0,
                'suspect_anchor_count': 0,
                'invalid_count': 0,
                'hits': [],
            },
        )
        counter_key = counter_map.get(str(hit['anchor_strength']))
        if counter_key:
            bucket[counter_key] += 1
        bucket['hits'].append(hit)

    result = {
        'range': args.range_text,
        'target_count': len(grouped),
        'targets': list(grouped.values()),
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"range: {args.range_text}")
        print(f"target_count: {result['target_count']}")
        for target in result['targets'][:100]:
            print(
                f"  {target['target']}: strong={target['strong_anchor_count']} weak={target['weak_anchor_count']} suspect={target['suspect_anchor_count']} invalid={target['invalid_count']}"
            )
            for hit in target['hits'][:10]:
                print(
                    f"    {hit['kind']} from {hit['caller']} -> {hit['anchor_strength']} ({hit['caller_status']})"
                )
                if hit['caller_range']:
                    print(f"      caller_range: {hit['caller_range']} ({hit['caller_label']})")
            if len(target['hits']) > 10:
                print(f"      ... truncated {len(target['hits']) - 10} additional hits")
        if len(result['targets']) > 100:
            print(f"... truncated {len(result['targets']) - 100} additional targets")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
