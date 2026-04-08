#!/usr/bin/env python3
from __future__ import annotations

import argparse

from toolkit_compat import default_rom_path, delegate_to

def main() -> int:
    parser = argparse.ArgumentParser(description='Find the next callable lane using the current ROM-aware scorer')
    parser.add_argument('--rom', default=default_rom_path())
    parser.add_argument('--config', default='tools/config/next_target_scoring.yaml')
    parser.add_argument('--bank-progress', default='tools/config/bank_c3_progress.json')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    forwarded = [
        '--rom',
        args.rom,
        '--config',
        args.config,
        '--bank-progress',
        args.bank_progress,
    ]
    if args.json:
        forwarded.append('--json')
    return delegate_to('find_next_callable_lane_v2.py', forwarded)

if __name__ == '__main__':
    raise SystemExit(main())
