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
    ap = argparse.ArgumentParser(description='One-shot C3 seam triage flow with page-level mixedness and owner-boundary risk layering')
    ap.add_argument('--rom', required=True)
    ap.add_argument('--range', dest='range_text', required=True)
    ap.add_argument('--format', choices=['json', 'text'], default='json')
    args = ap.parse_args()

    mixed = run_json('page_range_mixedness_v1.py', '--rom', args.rom, '--range', args.range_text)
    boundary = run_json('score_owner_boundary_risk_v1.py', '--rom', args.rom, '--range', args.range_text)
    batch = {
        'range': args.range_text,
        'page_mixedness': mixed,
        'owner_boundary': boundary,
        'summary': {
            'page_count': mixed.get('page_count', 0),
            'labels': [p['label'] for p in mixed.get('pages', [])],
            'total_hits': sum(p.get('hit_count', 0) for p in boundary.get('pages', [])),
            'total_islands': sum(p.get('island_count', 0) for p in boundary.get('pages', [])),
        },
    }
    if args.format == 'json':
        print(json.dumps(batch, indent=2))
    else:
        print(f"range: {args.range_text}")
        print(f"page_count: {batch['summary']['page_count']}")
        print(f"labels: {', '.join(batch['summary']['labels'])}")
        print(f"total_hits: {batch['summary']['total_hits']}")
        print(f"total_islands: {batch['summary']['total_islands']}")
        for mp, bp in zip(mixed.get('pages', []), boundary.get('pages', [])):
            print(f"  {mp['range']}: label={mp['label']} hits={bp['hit_count']} islands={bp['island_count']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
