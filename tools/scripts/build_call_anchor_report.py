#!/usr/bin/env python3
from __future__ import annotations

import argparse

from snes_utils import parse_snes_range
from toolkit_compat import default_rom_path, delegate_to


def main() -> int:
    parser = argparse.ArgumentParser(description='Build a call-anchor report using the current bank-aware implementation')
    parser.add_argument('--rom', default=default_rom_path())
    parser.add_argument('--target', help='Exact entry address like C3:1817')
    parser.add_argument('--range', dest='range_text', help='Legacy range input; the start address becomes the target')
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--sessions-dir', default='docs/sessions')
    parser.add_argument('--closed-ranges-snapshot', default='tools/cache/closed_ranges_snapshot_v1.json')
    parser.add_argument('--only-valid', action='store_true')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    if bool(args.target) == bool(args.range_text):
        raise SystemExit('provide exactly one of --target or --range')

    target = args.target
    if args.range_text:
        bank, start, _ = parse_snes_range(args.range_text)
        target = f'{bank:02X}:{start:04X}'

    forwarded = [
        '--rom',
        args.rom,
        '--target',
        str(target),
        '--manifests-dir',
        args.manifests_dir,
        '--sessions-dir',
        args.sessions_dir,
        '--closed-ranges-snapshot',
        args.closed_ranges_snapshot,
    ]
    if args.only_valid:
        forwarded.append('--only-valid')
    if args.json:
        forwarded.append('--json')
    return delegate_to('build_call_anchor_report_v3.py', forwarded)

if __name__ == '__main__':
    raise SystemExit(main())
