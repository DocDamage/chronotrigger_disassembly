#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from snes_utils_hirom_v2 import format_offset_as_snes, iter_all_call_patterns, parse_snes_address

from manifest_xref_utils import anchor_strength, classify_caller_context
from xref_index_utils_v1 import choose_closed_ranges


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Build a bank-aware call-anchor report with caller-confidence scoring'
    )
    parser.add_argument('--rom', required=True)
    parser.add_argument('--target', required=True, help='Exact entry address like C3:1817')
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--sessions-dir', default='docs/sessions')
    parser.add_argument('--closed-ranges-snapshot', default='tools/cache/closed_ranges_snapshot_v1.json')
    parser.add_argument('--only-valid', action='store_true')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    bank, addr = parse_snes_address(args.target)
    rom_bytes = Path(args.rom).read_bytes()
    closed_ranges = choose_closed_ranges(args.manifests_dir, args.closed_ranges_snapshot, args.sessions_dir)

    hits: list[dict[str, object]] = []
    for kind, offset in iter_all_call_patterns(rom_bytes, bank, addr):
        caller_text = format_offset_as_snes(offset)
        caller_bank = parse_snes_address(caller_text)[0]
        notes: list[str] = []
        validity = 'valid'
        if kind in {'JSR', 'JMP'} and caller_bank != bank:
            validity = 'invalid_bank_mismatch'
            notes.append(
                f'same-bank {kind} at {caller_text} resolves to {caller_bank:02X}:{addr:04X}, not {bank:02X}:{addr:04X}'
            )

        caller_ctx = classify_caller_context(closed_ranges, caller_text)
        strength = anchor_strength(validity, caller_ctx['caller_status'])
        if validity == 'valid' and caller_ctx['caller_status'] == 'unresolved':
            notes.append('caller lives in unresolved bytes, so this is weak anchor evidence')
        elif validity == 'valid' and caller_ctx['caller_status'] == 'resolved_data':
            notes.append('caller sits inside a closed data range, so this hit is suspect')
        elif validity == 'valid' and caller_ctx['caller_status'] == 'resolved_code':
            notes.append('caller sits inside a resolved executable range')

        item = {
            'kind': kind,
            'caller': caller_text,
            'target': args.target,
            'validity': validity,
            'anchor_strength': strength,
            **caller_ctx,
            'notes': notes,
        }
        if args.only_valid and validity != 'valid':
            continue
        hits.append(item)

    rank = {'strong': 0, 'weak': 1, 'suspect': 2, 'invalid': 3}
    hits.sort(key=lambda item: (rank.get(str(item['anchor_strength']), 9), str(item['caller'])))

    result = {
        'target': args.target,
        'call_count': len(hits),
        'strong_anchor_count': sum(1 for item in hits if item['anchor_strength'] == 'strong'),
        'weak_anchor_count': sum(1 for item in hits if item['anchor_strength'] == 'weak'),
        'suspect_anchor_count': sum(1 for item in hits if item['anchor_strength'] == 'suspect'),
        'invalid_count': sum(1 for item in hits if item['anchor_strength'] == 'invalid'),
        'hits': hits[:500],
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"target: {args.target}")
        print(f"call_count: {result['call_count']}")
        print(
            'strong={strong_anchor_count} weak={weak_anchor_count} suspect={suspect_anchor_count} invalid={invalid_count}'.format(
                **result
            )
        )
        for item in hits[:100]:
            print(
                f"  {item['kind']} from {item['caller']} -> {item['validity']} / {item['anchor_strength']} / {item['caller_status']}"
            )
            if item['caller_range']:
                print(f"    caller_range: {item['caller_range']} ({item['caller_label']})")
            for note in item['notes']:
                print(f"    note: {note}")
        if len(hits) > 100:
            print(f"  ... truncated {len(hits) - 100} additional hits")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
