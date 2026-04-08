#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from snes_utils import iter_manifest_paths, load_manifest, manifest_pass_number, parse_snes_range


def overlaps(a: tuple[int, int, int], b: tuple[int, int, int]) -> bool:
    return a[0] == b[0] and not (a[2] < b[1] or b[2] < a[1])


def main() -> int:
    parser = argparse.ArgumentParser(description='Validate pass manifests for overlap and confidence issues')
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--strict-overlaps', action='store_true', help='Fail when overlap warnings are present')
    args = parser.parse_args()

    warnings: list[str] = []
    blocking: list[str] = []
    seen: list[tuple[tuple[int, int, int], dict]] = []
    for path in iter_manifest_paths(args.manifests_dir):
        data = load_manifest(path)
        pass_number = manifest_pass_number(data, path)
        for item in data.get('closed_ranges', []):
            rng = parse_snes_range(item['range'])
            for prev_rng, prev_item in seen:
                if overlaps(rng, prev_rng):
                    allowed = item['kind'] == 'tail_fragment' or prev_item['kind'] == 'tail_fragment'
                    if not allowed:
                        label = 'duplicate range' if rng == prev_rng else 'overlap'
                        warnings.append(
                            f"{label}: pass {pass_number} {item['range']} vs {prev_item['range']}"
                        )
            seen.append((rng, item))
            if item['confidence'] == 'low':
                blocking.append(f"low-confidence closure: pass {pass_number} {item['range']} ({item['label']})")
            if item['kind'] == 'text_marker' and 'code_end' not in item['label'] and 'text' not in item['label']:
                warnings.append(f"text marker label may be weakly named: pass {pass_number} {item['range']}")

    if warnings:
        print('warnings found:')
        for issue in warnings:
            print(f'  - {issue}')
    if blocking:
        print('blocking issues found:')
        for issue in blocking:
            print(f'  - {issue}')
        return 1
    if warnings and args.strict_overlaps:
        return 1
    print('validation ok: no blocking manifest issues found')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
