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
    proc = subprocess.run([sys.executable, str(script_path), *extra_args, '--json'], check=True, capture_output=True, text=True)
    return json.loads(proc.stdout)


def main() -> int:
    parser = argparse.ArgumentParser(description='One-shot C3 seam triage flow with optional reusable xref index and closed-range snapshot for much faster local seam work')
    parser.add_argument('--rom', required=True)
    parser.add_argument('--range', dest='range_text', required=True)
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--sessions-dir', default='docs/sessions')
    parser.add_argument('--closed-ranges-snapshot', default='')
    parser.add_argument('--xref-index', default='')
    parser.add_argument('--dead-ranges-config', default='tools/config/c3_dead_ranges_v1.json')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    callers_args = ['--rom', args.rom, '--range', args.range_text, '--manifests-dir', args.manifests_dir, '--sessions-dir', args.sessions_dir]
    xref_args = ['--rom', args.rom, '--range', args.range_text, '--manifests-dir', args.manifests_dir, '--sessions-dir', args.sessions_dir, '--dead-ranges-config', args.dead_ranges_config]
    if args.closed_ranges_snapshot:
        callers_args.extend(['--closed-ranges-snapshot', args.closed_ranges_snapshot])
        xref_args.extend(['--closed-ranges-snapshot', args.closed_ranges_snapshot])
    if args.xref_index:
        callers_args.extend(['--xref-index', args.xref_index])
        xref_args.extend(['--xref-index', args.xref_index])

    page = run_json('classify_page_family_v1.py', '--rom', args.rom, '--range', args.range_text)
    veneer = run_json('detect_tiny_veneers_v1.py', '--rom', args.rom, '--range', args.range_text)
    callers = run_json('scan_range_entry_callers_v3.py', *callers_args)
    xref = run_json('score_raw_xref_context_v3.py', *xref_args)
    backtrack = run_json('score_target_owner_backtrack_v1.py', '--rom', args.rom, '--range', args.range_text)
    islands = run_json('find_local_code_islands_v2.py', '--rom', args.rom, '--range', args.range_text)
    wrappers = run_json('detect_wrapper_target_quality_v1.py', '--rom', args.rom, '--range', args.range_text, '--dead-ranges-config', args.dead_ranges_config)

    strong_or_better = [hit for hit in xref['hits'] if hit['effective_strength'] in {'strong', 'weak'}]
    bad_backtracks = [item for item in backtrack['candidates'] if item['score'] >= 3]

    if page['page_family'] == 'dead_zero_field':
        posture = 'dead_lane_reject'
    elif xref['dead_lane_suppressed_count'] > 0 or xref['hard_bad_start_hit_count'] > 0:
        posture = 'bad_start_or_dead_lane_reject'
    elif islands['cluster_count'] > 0 and not strong_or_better:
        posture = 'local_control_only'
    elif strong_or_better and bad_backtracks:
        posture = 'manual_owner_boundary_review'
    else:
        posture = 'mixed_lane_continue'

    result = {
        'range': args.range_text,
        'page_family': page,
        'tiny_veneers': veneer,
        'entry_callers': callers,
        'xref_context': xref,
        'owner_backtrack': backtrack,
        'local_islands': islands,
        'wrapper_target_quality': wrappers,
        'summary': {
            'raw_target_count': callers.get('target_count', 0),
            'xref_hit_count': xref.get('hit_count', 0),
            'effective_strong_or_weak_hits': len(strong_or_better),
            'dead_lane_suppressed_hits': xref.get('dead_lane_suppressed_count', 0),
            'hard_bad_start_hits': xref.get('hard_bad_start_hit_count', 0),
            'soft_bad_start_hits': xref.get('soft_bad_start_hit_count', 0),
            'owner_backtrack_candidates': len(bad_backtracks),
            'local_island_count': islands.get('island_count', 0),
            'local_cluster_count': islands.get('cluster_count', 0),
            'tiny_veneer_count': veneer.get('candidate_count', 0),
            'wrapper_bad_target_count': wrappers.get('wrapper_bad_target_count', 0),
            'review_posture': posture,
        },
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f'range: {args.range_text}')
        print(f'page_family: {page["page_family"]}')
        print(f'review_posture: {posture}')
        for key, value in result['summary'].items():
            if key == 'review_posture':
                continue
            print(f'{key}: {value}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
