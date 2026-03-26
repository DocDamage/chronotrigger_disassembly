#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from snes_utils import ascii_ratio, opcode_hint_score, slice_rom_range, zero_ratio


def score_lane(data: bytes, weights: dict[str, int]) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []
    zr = zero_ratio(data)
    ar = ascii_ratio(data)
    oh = opcode_hint_score(data)
    if oh >= max(8, len(data) // 12):
        score += weights.get('full_prologue', 0) // 2
        reasons.append('opcode-density suggests executable candidate')
    if zr >= 0.70:
        score += weights.get('zero_padding_penalty', 0)
        reasons.append('heavy zero padding penalty')
    if ar >= 0.70 and zr <= 0.10:
        score += weights.get('inline_text_penalty', 0)
        reasons.append('ascii-heavy inline text penalty')
    return score, reasons


def main() -> int:
    parser = argparse.ArgumentParser(description='Score next callable lanes from bank progress and ROM bytes')
    parser.add_argument('--rom', required=True)
    parser.add_argument('--bank-progress', default='tools/config/bank_c3_progress.json')
    parser.add_argument('--config', default='tools/config/next_target_scoring.yaml')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    progress = json.loads(Path(args.bank_progress).read_text(encoding='utf-8'))
    config = yaml.safe_load(Path(args.config).read_text(encoding='utf-8'))
    rom_bytes = Path(args.rom).read_bytes()

    results = []
    for lane in progress.get('open_lanes', []):
        range_text = lane['range']
        if '..' not in range_text:
            continue
        data = slice_rom_range(rom_bytes, range_text)
        score, reasons = score_lane(data, config.get('weights', {}))
        results.append({'range': range_text, 'score': score, 'reasons': reasons + [lane.get('reason', '')]})

    results.sort(key=lambda x: x['score'], reverse=True)
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for item in results:
            print(f"{item['range']}: score={item['score']}")
            for reason in item['reasons']:
                if reason:
                    print(f"  - {reason}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
