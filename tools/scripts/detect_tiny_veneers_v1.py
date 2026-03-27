#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from snes_utils_hirom_v2 import format_snes_range, parse_snes_range, slice_rom_range


def signed_rel8(value: int) -> int:
    return value - 0x100 if value >= 0x80 else value


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Detect tiny wrapper, landing-pad, and return-stub candidates inside a SNES range'
    )
    parser.add_argument('--rom', required=True)
    parser.add_argument('--range', dest='range_text', required=True)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    bank, start, _ = parse_snes_range(args.range_text)
    data = slice_rom_range(Path(args.rom).read_bytes(), args.range_text)
    results: list[dict[str, object]] = []

    for idx, op in enumerate(data):
        addr = start + idx
        if op == 0x20 and idx + 3 < len(data) and data[idx + 3] == 0x60:
            target = data[idx + 1] | (data[idx + 2] << 8)
            results.append(
                {
                    'range': format_snes_range(bank, addr, addr + 3),
                    'pattern': 'jsr_rts_wrapper',
                    'target': f'{bank:02X}:{target:04X}',
                    'confidence': 'high',
                }
            )
        elif op == 0x22 and idx + 4 < len(data) and data[idx + 4] == 0x60:
            target = data[idx + 1] | (data[idx + 2] << 8)
            target_bank = data[idx + 3]
            results.append(
                {
                    'range': format_snes_range(bank, addr, addr + 4),
                    'pattern': 'jsl_rts_wrapper',
                    'target': f'{target_bank:02X}:{target:04X}',
                    'confidence': 'high',
                }
            )
        elif op == 0x6B:
            results.append(
                {
                    'range': format_snes_range(bank, addr, addr),
                    'pattern': 'rtl_stub',
                    'target': '',
                    'confidence': 'high',
                }
            )
        elif op == 0x80 and idx + 1 < len(data):
            dest = addr + 2 + signed_rel8(data[idx + 1])
            results.append(
                {
                    'range': format_snes_range(bank, addr, addr + 1),
                    'pattern': 'bra_landing_pad',
                    'target': f'{bank:02X}:{dest & 0xFFFF:04X}',
                    'confidence': 'medium',
                }
            )

    result = {'range': args.range_text, 'candidate_count': len(results), 'candidates': results}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"range: {args.range_text}")
        print(f"candidate_count: {len(results)}")
        for item in results:
            target = f" -> {item['target']}" if item['target'] else ''
            print(f"  {item['range']}: {item['pattern']}{target} ({item['confidence']})")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
