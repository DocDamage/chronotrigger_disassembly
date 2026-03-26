#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

REQUIRED_TOP = {
    'pass_number', 'branch', 'toolkit_version', 'live_seam_after_pass',
    'completion_estimate', 'closed_ranges', 'new_labels', 'confidence', 'notes'
}
REQUIRED_CLOSED = {'range', 'kind', 'label', 'confidence'}
REQUIRED_CONF = {'structural', 'semantic', 'rebuild'}


def main() -> int:
    parser = argparse.ArgumentParser(description='Lightweight pass manifest checker')
    parser.add_argument('--manifest', required=True)
    args = parser.parse_args()

    data = json.loads(Path(args.manifest).read_text(encoding='utf-8'))
    missing = REQUIRED_TOP - set(data)
    if missing:
        print(f'missing top-level keys: {sorted(missing)}')
        return 1
    for idx, item in enumerate(data['closed_ranges']):
        cmissing = REQUIRED_CLOSED - set(item)
        if cmissing:
            print(f'closed_ranges[{idx}] missing keys: {sorted(cmissing)}')
            return 1
    conf_missing = REQUIRED_CONF - set(data['confidence'])
    if conf_missing:
        print(f'confidence missing keys: {sorted(conf_missing)}')
        return 1
    print(f"manifest ok: pass {data['pass_number']}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
