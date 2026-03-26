#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml

def main() -> int:
    parser = argparse.ArgumentParser(description='Find the next callable lane')
    parser.add_argument('--config', default='tools/config/next_target_scoring.yaml')
    parser.add_argument('--bank-progress', default='tools/config/bank_c3_progress.json')
    args = parser.parse_args()
    config = yaml.safe_load(Path(args.config).read_text(encoding='utf-8'))
    progress = json.loads(Path(args.bank_progress).read_text(encoding='utf-8'))
    print(config['weights'])
    print(progress.get('open_lanes', []))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
