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
    parser = argparse.ArgumentParser(
        description='One-shot C3 seam triage flow with xref-context scoring, local-island detection, and page-ownership classification'
    )
    parser.add_argument('--rom', required=True)
    parser.add_argument('--range', dest='range_text', required=True)
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    v2 = run_json(
        'run_c3_candidate_flow_v2.py',
        '--rom', args.rom,
        '--range', args.range_text,
        '--manifests-dir', args.manifests_dir,
    )
    ownership = run_json(
        'score_seam_page_ownership_v1.py',
        '--rom', args.rom,
        '--range', args.range_text,
        '--manifests-dir', args.manifests_dir,
    )

    result = {
        'range': args.range_text,
        'candidate_flow_v2': v2,
        'page_ownership': ownership,
        'summary': {
            **v2.get('summary', {}),
            **ownership.get('summary', {}),
        },
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"range: {args.range_text}")
        for key, value in result['summary'].items():
            print(f"{key}: {value}")
        if ownership.get('hits'):
            print('top ownership hits:')
            for hit in ownership['hits'][:10]:
                reasons = ','.join(hit['ownership_reasons'])
                print(
                    f"  {hit['caller']} {hit['kind']} -> {hit['target']} | "
                    f"score={hit['ownership_score']} reasons={reasons}"
                )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
