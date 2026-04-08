#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

REQUIRED_TOP_CANONICAL = {'pass_number', 'closed_ranges'}
REQUIRED_CLOSED = {'range', 'kind', 'label', 'confidence'}
REQUIRED_CONF = {'structural', 'semantic', 'rebuild'}
REQUIRED_TOP_LEGACY = {'pass_num', 'pass_name', 'region', 'targets', 'coverage_bytes', 'notes'}
REQUIRED_TARGET_LEGACY = {'addr', 'label'}


def main() -> int:
    parser = argparse.ArgumentParser(description='Lightweight pass manifest checker')
    parser.add_argument('--manifest', required=True)
    args = parser.parse_args()

    data = json.loads(Path(args.manifest).read_text(encoding='utf-8'))
    if 'closed_ranges' in data:
        missing = REQUIRED_TOP_CANONICAL - set(data)
        if missing:
            print(f'missing canonical top-level keys: {sorted(missing)}')
            return 1
        for idx, item in enumerate(data['closed_ranges']):
            cmissing = REQUIRED_CLOSED - set(item)
            if cmissing:
                print(f'closed_ranges[{idx}] missing keys: {sorted(cmissing)}')
                return 1
        if 'confidence' in data:
            conf_missing = REQUIRED_CONF - set(data['confidence'])
            if conf_missing:
                print(f'confidence missing keys: {sorted(conf_missing)}')
                return 1
        print(f"manifest ok: canonical pass {data['pass_number']}")
        return 0

    if 'targets' in data:
        missing = REQUIRED_TOP_LEGACY - set(data)
        if missing:
            print(f'missing legacy top-level keys: {sorted(missing)}')
            return 1
        for idx, item in enumerate(data['targets']):
            tmissing = REQUIRED_TARGET_LEGACY - set(item)
            if tmissing:
                print(f'targets[{idx}] missing keys: {sorted(tmissing)}')
                return 1
        print(f"manifest ok: legacy pass {data['pass_num']}")
        return 0

    print('unknown manifest schema: expected canonical closed_ranges or legacy targets manifest')
    return 1

if __name__ == '__main__':
    raise SystemExit(main())
