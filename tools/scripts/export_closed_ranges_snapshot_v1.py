#!/usr/bin/env python3
from __future__ import annotations

import argparse

from xref_index_utils_v1 import export_closed_ranges_snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description='Export effective closed ranges from manifests plus continuation-note closures into one compact snapshot file')
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--sessions-dir', default='docs/sessions')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    payload = export_closed_ranges_snapshot(args.output, args.manifests_dir, args.sessions_dir)
    print(f'output: {args.output}')
    print(f'range_count: {payload["range_count"]}')
    print(f'manifest_range_count: {payload.get("manifest_range_count", 0)}')
    print(f'continuation_range_count: {payload.get("continuation_range_count", 0)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
