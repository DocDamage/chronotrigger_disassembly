#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from snes_utils import ascii_ratio, opcode_hint_score, parse_snes_range, slice_rom_range, unique_ratio, zero_ratio


def classify(data: bytes) -> tuple[str, dict[str, float | int]]:
    zr = zero_ratio(data)
    ar = ascii_ratio(data)
    ur = unique_ratio(data)
    oh = opcode_hint_score(data)
    metrics = {
        'length': len(data),
        'zero_ratio': round(zr, 4),
        'ascii_ratio': round(ar, 4),
        'unique_ratio': round(ur, 4),
        'opcode_hint_score': oh,
    }
    if zr >= 0.70:
        return 'padding_or_sparse_data', metrics
    if ar >= 0.70 and zr <= 0.10:
        return 'inline_text_or_marker', metrics
    if oh >= max(8, len(data) // 12) and zr < 0.35:
        return 'executable_candidate', metrics
    if ur < 0.25:
        return 'table_or_control_data', metrics
    return 'mixed_or_uncertain', metrics


def main() -> int:
    parser = argparse.ArgumentParser(description='Classify candidate C3 ranges from ROM bytes')
    parser.add_argument('--rom', required=True)
    parser.add_argument('--range', dest='range_text', required=True)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    bank, _, _ = parse_snes_range(args.range_text)
    if bank != 0xC3:
        print(f'warning: script tuned for C3, got bank {bank:02X}')

    data = slice_rom_range(Path(args.rom).read_bytes(), args.range_text)
    label, metrics = classify(data)
    result = {'range': args.range_text, 'classification': label, 'metrics': metrics}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{args.range_text}: {label}")
        for k, v in metrics.items():
            print(f"  {k}: {v}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
