#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def run_json(script_name: str, *extra_args: str) -> dict:
    script_path = SCRIPT_DIR / script_name
    proc = subprocess.run(
        [sys.executable, str(script_path), *extra_args, '--json'],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def format_page_range(bank: int, start: int) -> str:
    return f'{bank:02X}:{start:04X}..{bank:02X}:{start + 0xFF:04X}'


def iter_page_ranges(range_text: str) -> list[str]:
    left, right = range_text.split('..')
    bank_s, start_s = left.split(':')
    _, end_s = right.split(':')
    bank = int(bank_s, 16)
    start = int(start_s, 16) & 0xFF00
    end = int(end_s, 16) & 0xFF00
    ranges = []
    addr = start
    while addr <= end:
        ranges.append(format_page_range(bank, addr))
        addr += 0x100
    return ranges


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Batch-run page ownership triage across a consecutive C3 seam block'
    )
    parser.add_argument('--rom', required=True)
    parser.add_argument('--range', dest='range_text', required=True)
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    page_results = []
    for page_range in iter_page_ranges(args.range_text):
        page = run_json(
            'score_seam_page_ownership_v1.py',
            '--rom', args.rom,
            '--range', page_range,
            '--manifests-dir', args.manifests_dir,
        )
        summary = dict(page['summary'])
        summary['range'] = page_range
        page_results.append(summary)

    ranked_by_external = sorted(
        page_results,
        key=lambda item: (
            -(item.get('best_external_direct_score') or -999),
            -(item.get('external_direct_hit_count') or 0),
            item['range'],
        ),
    )
    ranked_by_local = sorted(
        page_results,
        key=lambda item: (
            -(item.get('local_branch_hit_count') or 0),
            -(item.get('local_island_count') or 0),
            item['range'],
        ),
    )

    result = {
        'range': args.range_text,
        'page_count': len(page_results),
        'pages': page_results,
        'top_external_owner_candidates': ranked_by_external[:10],
        'top_local_control_blobs': ranked_by_local[:10],
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"range: {args.range_text}")
        print(f"page_count: {len(page_results)}")
        print('top external owner candidates:')
        for item in result['top_external_owner_candidates']:
            print(
                f"  {item['range']} | class={item['page_class']} "
                f"best_external_direct_score={item['best_external_direct_score']} "
                f"external_direct_hit_count={item['external_direct_hit_count']}"
            )
        print('top local control blobs:')
        for item in result['top_local_control_blobs']:
            print(
                f"  {item['range']} | class={item['page_class']} "
                f"local_branch_hit_count={item['local_branch_hit_count']} "
                f"local_island_count={item['local_island_count']}"
            )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
