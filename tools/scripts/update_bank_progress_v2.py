#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from snes_utils import iter_manifest_paths


def main() -> int:
    parser = argparse.ArgumentParser(description='Rebuild bank progress index from pass manifests')
    parser.add_argument('--bank', default='C3')
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--out', default='tools/config/bank_c3_progress.generated.json')
    args = parser.parse_args()

    bank = args.bank.upper()
    closed_exec = []
    closed_data = []
    latest_seam = None
    latest_pass = 0

    for path in iter_manifest_paths(args.manifests_dir):
        data = json.loads(Path(path).read_text(encoding='utf-8'))
        latest_pass = max(latest_pass, int(data['pass_number']))
        latest_seam = data.get('live_seam_after_pass', latest_seam)
        for item in data.get('closed_ranges', []):
            if not item['range'].startswith(f'{bank}:'):
                continue
            entry = {
                'range': item['range'],
                'label': item['label'],
                'pass': data['pass_number'],
                'confidence': item['confidence'],
                'kind': item['kind'],
            }
            if item['kind'] in {'data', 'text_marker'}:
                closed_data.append(entry)
            else:
                closed_exec.append(entry)

    result = {
        'bank': bank,
        'latest_pass': latest_pass,
        'latest_live_seam': latest_seam,
        'closed_executable_ranges': closed_exec,
        'closed_data_ranges': closed_data,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(f'wrote {out_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
