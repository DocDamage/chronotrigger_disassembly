#!/usr/bin/env python3
from __future__ import annotations

import argparse

from xref_index_utils_v1 import export_closed_ranges_snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description='Export all manifest closed ranges into one compact snapshot file for faster local seam scans')
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    payload = export_closed_ranges_snapshot(args.output, args.manifests_dir)
    print(f'output: {args.output}')
    print(f'range_count: {payload["range_count"]}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
