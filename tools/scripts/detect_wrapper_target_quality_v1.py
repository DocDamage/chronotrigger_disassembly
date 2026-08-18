#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from seam_triage_utils_v1 import parse_snes_range, classify_start_byte, load_dead_ranges, dead_range_match, classify_page_family

def detect_wrappers(data: bytes, bank: int, start: int):
    results = []
    for idx, op in enumerate(data):
        addr = start + idx
        if op == 0x20 and idx + 3 < len(data) and data[idx + 3] == 0x60:
            target = data[idx + 1] | (data[idx + 2] << 8)
            results.append({'range': f'{bank:02X}:{addr:04X}..{bank:02X}:{addr+3:04X}', 'pattern': 'jsr_rts_wrapper', 'target_bank': bank, 'target_addr': target, 'target': f'{bank:02X}:{target:04X}'})
        elif op == 0x22 and idx + 4 < len(data) and data[idx + 4] == 0x60:
            target = data[idx + 1] | (data[idx + 2] << 8)
            target_bank = data[idx + 3]
            results.append({'range': f'{bank:02X}:{addr:04X}..{bank:02X}:{addr+4:04X}', 'pattern': 'jsl_rts_wrapper', 'target_bank': target_bank, 'target_addr': target, 'target': f'{target_bank:02X}:{target:04X}'})
    return results

def main() -> int:
    parser = argparse.ArgumentParser(description='Detect tiny wrappers and score whether their targets land in dead lanes or bad-start bytes')
    parser.add_argument('--rom', required=True)
    parser.add_argument('--range', dest='range_text', required=True)
    parser.add_argument('--dead-ranges-config', default='tools/config/c3_dead_ranges_v1.json')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    bank, start, end = parse_snes_range(args.range_text)
    rom_bytes = Path(args.rom).read_bytes()
    data = rom_bytes[(bank - 0xC0) * 0x10000 + start:(bank - 0xC0) * 0x10000 + end + 1]
    dead_ranges = load_dead_ranges(args.dead_ranges_config)

    results = []
    bad_target_count = 0
    for item in detect_wrappers(data, bank, start):
        target_off = (item['target_bank'] - 0xC0) * 0x10000 + item['target_addr']
        if not (0 <= target_off < len(rom_bytes)):
            continue
        start_byte = rom_bytes[target_off]
        start_class, start_reason = classify_start_byte(start_byte)
        dead_match = dead_range_match(dead_ranges, item['target_bank'], item['target_addr'])
        if dead_match or start_class != 'clean_start':
            bad_target_count += 1
        family = ''
        family_reasons = []
        if item['target_bank'] == bank and start <= item['target_addr'] <= end:
            family, family_reasons, _ = classify_page_family(rom_bytes, args.range_text)
        results.append({
            'range': item['range'],
            'pattern': item['pattern'],
            'target': item['target'],
            'target_start_byte': f'{start_byte:02X}',
            'target_start_class': start_class,
            'target_start_reason': start_reason,
            'dead_range': dead_match['range'] if dead_match else '',
            'dead_range_reason': dead_match.get('reason', '') if dead_match else '',
            'target_page_family': family,
            'target_page_family_reasons': family_reasons,
            'target_quality': 'nonpromotable_target' if dead_match or start_class != 'clean_start' else 'mixed_or_unknown_target',
        })

    result = {'range': args.range_text, 'wrapper_count': len(results), 'wrapper_bad_target_count': bad_target_count, 'wrappers': results}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f'range: {args.range_text}')
        print(f'wrapper_count: {len(results)}')
        print(f'wrapper_bad_target_count: {bad_target_count}')
        for item in results:
            dead_text = f" dead_range={item['dead_range']}" if item['dead_range'] else ''
            print(f"  {item['range']} -> {item['target']} | start={item['target_start_byte']} {item['target_start_reason'] or item['target_start_class']}{dead_text} quality={item['target_quality']}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
