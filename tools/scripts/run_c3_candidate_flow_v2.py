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


def main() -> int:
    parser = argparse.ArgumentParser(description='One-shot C3 seam triage flow with xref-context scoring and local return-island detection')
    parser.add_argument('--rom', required=True)
    parser.add_argument('--range', dest='range_text', required=True)
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    veneer = run_json('detect_tiny_veneers_v1.py', '--rom', args.rom, '--range', args.range_text)
    callers = run_json('scan_range_entry_callers_v2.py', '--rom', args.rom, '--range', args.range_text, '--manifests-dir', args.manifests_dir)
    xref = run_json('score_raw_xref_context_v1.py', '--rom', args.rom, '--range', args.range_text, '--manifests-dir', args.manifests_dir)
    islands = run_json('find_local_code_islands_v1.py', '--rom', args.rom, '--range', args.range_text)

    strong_or_better = [hit for hit in xref['hits'] if hit['effective_strength'] in {'strong', 'weak'}]
    suspect_hits = [hit for hit in xref['hits'] if hit['effective_strength'] == 'suspect']

    result = {
        'range': args.range_text,
        'tiny_veneers': veneer,
        'entry_callers': callers,
        'xref_context': xref,
        'local_islands': islands,
        'summary': {
            'raw_target_count': callers.get('target_count', 0),
            'xref_hit_count': xref.get('hit_count', 0),
            'effective_strong_or_weak_hits': len(strong_or_better),
            'effective_suspect_hits': len(suspect_hits),
            'local_island_count': islands.get('island_count', 0),
            'tiny_veneer_count': veneer.get('candidate_count', 0),
        },
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"range: {args.range_text}")
        print(f"raw_target_count: {result['summary']['raw_target_count']}")
        print(f"xref_hit_count: {result['summary']['xref_hit_count']}")
        print(f"effective_strong_or_weak_hits: {result['summary']['effective_strong_or_weak_hits']}")
        print(f"effective_suspect_hits: {result['summary']['effective_suspect_hits']}")
        print(f"local_island_count: {result['summary']['local_island_count']}")
        print(f"tiny_veneer_count: {result['summary']['tiny_veneer_count']}")
        if strong_or_better:
            print('top xref-context hits:')
            for hit in strong_or_better[:10]:
                print(
                    f"  {hit['caller']} {hit['kind']} -> {hit['target']} | effective={hit['effective_strength']} caller_risk={hit['caller_risk']} target_risk={hit['target_risk']}"
                )
        if islands.get('islands'):
            print('top local islands:')
            for island in islands['islands'][:10]:
                print(
                    f"  {island['range']} | score={island['score']} width={island['width']} returns={island['return_count']} first_return={island['first_return_address']}"
                )
        if veneer.get('candidates'):
            print('tiny veneer candidates:')
            for item in veneer['candidates'][:10]:
                target = f" -> {item['target']}" if item.get('target') else ''
                print(f"  {item['range']}: {item['pattern']}{target}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
