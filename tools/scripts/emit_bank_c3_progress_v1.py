#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from manifest_xref_utils import classify_kind, load_closed_ranges


def main() -> int:
    parser = argparse.ArgumentParser(description='Emit a current bank C3 progress snapshot from manifests')
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--bank', default='C3')
    parser.add_argument('--json-out')
    parser.add_argument('--md-out')
    args = parser.parse_args()

    bank = int(args.bank, 16)
    ranges = [item for item in load_closed_ranges(args.manifests_dir) if item.bank == bank]
    if not ranges:
        raise SystemExit(f'no ranges found for bank {args.bank}')

    latest_pass = max(item.pass_number for item in ranges)
    manifests = sorted(Path(args.manifests_dir).glob('pass*.json'))
    live_seam = ''
    completion_estimate = ''
    if manifests:
        latest_manifest = max(manifests, key=lambda path: int(path.stem.replace('pass', '')))
        data = json.loads(latest_manifest.read_text(encoding='utf-8'))
        live_seam = str(data.get('live_seam_after_pass', ''))
        completion_estimate = str(data.get('completion_estimate', ''))

    code_ranges = []
    data_ranges = []
    for item in ranges:
        bucket = code_ranges if classify_kind(item.kind) == 'code' else data_ranges
        bucket.append({'range': item.range_text, 'label': item.label, 'kind': item.kind, 'pass': item.pass_number, 'confidence': item.confidence})

    snapshot = {
        'bank': f'{bank:02X}',
        'latest_pass': latest_pass,
        'live_seam_after_pass': live_seam,
        'completion_estimate': completion_estimate,
        'closed_executable_ranges': code_ranges,
        'closed_data_ranges': data_ranges,
    }

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(snapshot, indent=2) + '\n', encoding='utf-8')
    if args.md_out:
        lines = [
            f'# Bank {bank:02X} Progress Snapshot',
            '',
            f'- latest pass: **{latest_pass}**',
            f'- live seam after pass: **`{live_seam}`**',
            f'- completion estimate: **~{completion_estimate}%**',
            '',
            '## Closed executable ranges',
        ]
        for item in code_ranges:
            lines.append(f"- `{item['range']}` — {item['label']} ({item['kind']}, pass {item['pass']}, {item['confidence']})")
        lines += ['', '## Closed data ranges']
        for item in data_ranges:
            lines.append(f"- `{item['range']}` — {item['label']} ({item['kind']}, pass {item['pass']}, {item['confidence']})")
        Path(args.md_out).write_text('\n'.join(lines) + '\n', encoding='utf-8')

    print(json.dumps(snapshot, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
