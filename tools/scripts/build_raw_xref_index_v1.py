#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from xref_index_utils_v1 import build_xref_entries, write_xref_index


def main() -> int:
    parser = argparse.ArgumentParser(description='Build a reusable raw caller/xref index for the ROM so seam scans stop rescanning the whole image every page')
    parser.add_argument('--rom', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    rom_bytes = Path(args.rom).read_bytes()
    entries = build_xref_entries(rom_bytes)
    write_xref_index(args.output, rom_bytes, entries)
    print(f'output: {args.output}')
    print(f'entry_count: {len(entries)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
