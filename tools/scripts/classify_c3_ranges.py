#!/usr/bin/env python3
from __future__ import annotations

import argparse

from toolkit_compat import default_rom_path, delegate_to


def main() -> int:
    parser = argparse.ArgumentParser(description='Classify candidate C3 ranges from ROM bytes')
    parser.add_argument('--rom', default=default_rom_path())
    parser.add_argument('--range', dest='range_text', required=True)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    forwarded = ['--rom', args.rom, '--range', args.range_text]
    if args.json:
        forwarded.append('--json')
    return delegate_to('classify_c3_ranges_v2.py', forwarded)

if __name__ == '__main__':
    raise SystemExit(main())
