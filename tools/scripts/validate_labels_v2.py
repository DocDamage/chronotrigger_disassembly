#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from snes_utils import iter_manifest_paths, parse_snes_range


def overlaps(a: tuple[int, int, int], b: tuple[int, int, int]) -> bool:
    return a[0] == b[0] and not (a[2] < b[1] or b[2] < a[1])


def main() -> int:
    parser = argparse.ArgumentParser(description='Validate pass manifests for overlap and confidence issues')
    parser.add_argument('--manifests-dir', default='passes/manifests')
    args = parser.parse_args()

    issues: list[str] = []
    seen: list[tuple[tuple[int, int, int], dict]] = []
    for path in iter_manifest_paths(args.manifests_dir):
        data = json.loads(path.read_text(encoding='utf-8'))
        for item in data.get('closed_ranges', []):
            rng = parse_snes_range(item['range'])
            for prev_rng, prev_item in seen:
                if overlaps(rng, prev_rng):
                    allowed = item['kind'] == 'tail_fragment' or prev_item['kind'] == 'tail_fragment'
                    if not allowed:
                        issues.append(f"overlap: {item['range']} vs {prev_item['range']}")
            seen.append((rng, item))
            if item['confidence'] == 'low':
                issues.append(f"low-confidence closure: {item['range']} ({item['label']})")
            if item['kind'] == 'text_marker' and 'code_end' not in item['label'] and 'text' not in item['label']:
                issues.append(f"text marker label may be weakly named: {item['range']}")

    if issues:
        print('issues found:')
        for issue in issues:
            print(f'  - {issue}')
        return 1
    print('validation ok: no blocking manifest issues found')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
