#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from snes_utils_hirom_v2 import format_offset_as_snes, hirom_to_file_offset, parse_snes_address

SCRIPT_DIR = Path(__file__).resolve().parent

STRENGTH_RANK = {'strong': 0, 'weak': 1, 'suspect': 2, 'invalid': 3}


def run_json(script_name: str, *extra_args: str) -> dict:
    script_path = SCRIPT_DIR / script_name
    proc = subprocess.run(
        [sys.executable, str(script_path), *extra_args, '--json'],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def page_range_from_offset(offset: int) -> str:
    start = format_offset_as_snes(offset)
    end = format_offset_as_snes(offset + 0xFF)
    start_bank, start_addr = parse_snes_address(start)
    end_bank, end_addr = parse_snes_address(end)
    if start_bank != end_bank:
        raise ValueError('page crossed bank boundary unexpectedly')
    return f'{start_bank:02X}:{start_addr:04X}..{end_bank:02X}:{end_addr:04X}'


def best_targets(xref_hits: list[dict[str, object]], limit: int = 5) -> list[dict[str, object]]:
    grouped: dict[str, dict[str, object]] = {}
    for hit in xref_hits:
        target = str(hit['target'])
        bucket = grouped.setdefault(target, {'target': target, 'best_strength': 'invalid', 'hit_count': 0, 'callers': []})
        bucket['hit_count'] += 1
        bucket['callers'].append(str(hit['caller']))
        if STRENGTH_RANK[str(hit['effective_strength'])] < STRENGTH_RANK[str(bucket['best_strength'])]:
            bucket['best_strength'] = str(hit['effective_strength'])
    for bucket in grouped.values():
        # flag targets in the last 3 bytes of their page — instruction would span the page boundary
        _, addr_hex = str(bucket['target']).split(':')
        bucket['boundary_bait'] = (int(addr_hex, 16) & 0xFF) >= 0xFD
    items = list(grouped.values())
    items.sort(key=lambda item: (STRENGTH_RANK[str(item['best_strength'])], -int(item['hit_count']), str(item['target'])))
    return items[:limit]


def top_backtracks(candidates: list[dict[str, object]], limit: int = 5) -> list[dict[str, object]]:
    ranked = sorted(candidates, key=lambda item: (-int(item.get('score', 0)), str(item.get('owner_start', ''))))
    return ranked[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(description='Run the seam page flow over a contiguous block of pages with reusable caches.')
    parser.add_argument('--rom', required=True)
    parser.add_argument('--start', required=True, help='Page-aligned SNES address like C4:2300')
    parser.add_argument('--pages', type=int, default=10)
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--sessions-dir', default='docs/sessions')
    parser.add_argument('--cache-dir', default='tools/cache')
    parser.add_argument('--dead-ranges-config', default='tools/config/c3_dead_ranges_v1.json')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    start_bank, start_addr = parse_snes_address(args.start)
    if start_addr & 0xFF:
        raise ValueError('start address must be page aligned')
    start_offset = hirom_to_file_offset(start_bank, start_addr)

    cache = run_json(
        'ensure_seam_cache_v1.py',
        '--rom', args.rom,
        '--manifests-dir', args.manifests_dir,
        '--sessions-dir', args.sessions_dir,
        '--cache-dir', args.cache_dir,
    )
    xref_index = str(cache['xref_index_path'])
    snapshot = str(cache['closed_ranges_snapshot_path'])

    pages: list[dict[str, object]] = []
    posture_counts: dict[str, int] = {}
    family_counts: dict[str, int] = {}

    for idx in range(args.pages):
        offset = start_offset + idx * 0x100
        range_text = page_range_from_offset(offset)
        result = run_json(
            'run_c3_candidate_flow_v7.py',
            '--rom', args.rom,
            '--range', range_text,
            '--manifests-dir', args.manifests_dir,
            '--closed-ranges-snapshot', snapshot,
            '--xref-index', xref_index,
            '--dead-ranges-config', args.dead_ranges_config,
        )
        page_family = str(result['page_family']['page_family'])
        posture = str(result['summary']['review_posture'])
        family_counts[page_family] = family_counts.get(page_family, 0) + 1
        posture_counts[posture] = posture_counts.get(posture, 0) + 1
        pages.append(
            {
                'range': range_text,
                'page_family': page_family,
                'review_posture': posture,
                'summary': result['summary'],
                'best_targets': best_targets(result['xref_context']['hits']),
                'top_backtracks': top_backtracks(result['owner_backtrack']['candidates']),
                'local_clusters': result['local_islands'].get('clusters', []),
            }
        )

    result = {
        'start': args.start,
        'pages_requested': args.pages,
        'cache': cache,
        'page_family_counts': family_counts,
        'review_posture_counts': posture_counts,
        'pages': pages,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f'start: {args.start}')
        print(f'pages_requested: {args.pages}')
        print(f'page_family_counts: {json.dumps(family_counts, sort_keys=True)}')
        print(f'review_posture_counts: {json.dumps(posture_counts, sort_keys=True)}')
        for page in pages:
            print(f"{page['range']}: {page['page_family']} / {page['review_posture']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
