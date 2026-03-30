#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from xref_index_utils_v1 import (
    build_xref_entries,
    export_closed_ranges_snapshot,
    load_xref_index,
    rom_sha256,
    write_xref_index,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Ensure reusable seam caches exist for the current ROM, manifest state, and note-backed continuation closures.'
    )
    parser.add_argument('--rom', required=True)
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--sessions-dir', default='docs/sessions')
    parser.add_argument('--cache-dir', default='tools/cache')
    parser.add_argument('--xref-index-name', default='chrono_trigger_raw_xref_index_v1.json')
    parser.add_argument('--closed-ranges-name', default='closed_ranges_snapshot_v1.json')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    rom_path = Path(args.rom)
    rom_bytes = rom_path.read_bytes()
    current_sha = rom_sha256(rom_bytes)

    cache_dir = Path(args.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    xref_index_path = cache_dir / args.xref_index_name
    closed_ranges_path = cache_dir / args.closed_ranges_name

    xref_rebuilt = False
    if xref_index_path.exists():
        try:
            payload = load_xref_index(xref_index_path)
            indexed_sha = str(payload.get('rom_sha256', ''))
            if indexed_sha != current_sha:
                raise ValueError('rom sha mismatch')
        except Exception:
            entries = build_xref_entries(rom_bytes)
            write_xref_index(xref_index_path, rom_bytes, entries)
            xref_rebuilt = True
    else:
        entries = build_xref_entries(rom_bytes)
        write_xref_index(xref_index_path, rom_bytes, entries)
        xref_rebuilt = True

    previous_snapshot = closed_ranges_path.read_text(encoding='utf-8') if closed_ranges_path.exists() else ''
    payload = export_closed_ranges_snapshot(closed_ranges_path, args.manifests_dir, args.sessions_dir)
    snapshot_rebuilt = closed_ranges_path.read_text(encoding='utf-8') != previous_snapshot

    result = {
        'rom': str(rom_path),
        'rom_sha256': current_sha,
        'cache_dir': str(cache_dir),
        'xref_index_path': str(xref_index_path),
        'closed_ranges_snapshot_path': str(closed_ranges_path),
        'xref_index_rebuilt': xref_rebuilt,
        'closed_ranges_snapshot_rebuilt': snapshot_rebuilt,
        'closed_ranges_snapshot_range_count': int(payload.get('range_count', 0)),
        'closed_ranges_snapshot_manifest_range_count': int(payload.get('manifest_range_count', 0)),
        'closed_ranges_snapshot_continuation_range_count': int(payload.get('continuation_range_count', 0)),
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for key, value in result.items():
            print(f'{key}: {value}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
