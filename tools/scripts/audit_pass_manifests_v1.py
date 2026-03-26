#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from snes_utils import iter_manifest_paths


def main() -> int:
    parser = argparse.ArgumentParser(description='Audit pass manifests for revisit candidates')
    parser.add_argument('--manifests-dir', default='passes/manifests')
    args = parser.parse_args()

    revisit: list[str] = []
    for path in iter_manifest_paths(args.manifests_dir):
        data = json.loads(path.read_text(encoding='utf-8'))
        pn = data['pass_number']
        for item in data.get('closed_ranges', []):
            kind = item['kind']
            conf = item['confidence']
            label = item['label']
            if kind == 'tail_fragment':
                revisit.append(f'pass {pn}: tail fragment needs eventual reattachment -> {item["range"]}')
            elif conf in {'low', 'medium'}:
                revisit.append(f'pass {pn}: medium/low confidence review candidate -> {item["range"]} :: {label}')
            elif 'runtime_code_emitter' in label or 'interpreter' in label:
                revisit.append(f'pass {pn}: high-impact complex routine worth spot audit -> {item["range"]} :: {label}')

    if revisit:
        print('revisit candidates:')
        for line in revisit:
            print(f'  - {line}')
    else:
        print('no revisit candidates found')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
