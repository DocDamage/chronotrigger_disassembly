#!/usr/bin/env python3
from __future__ import annotations

import argparse

from toolkit_compat import delegate_to


def main() -> int:
    parser = argparse.ArgumentParser(description='Update bank progress from manifests')
    parser.add_argument('--bank', default='C3')
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--out')
    args = parser.parse_args()

    out = args.out or f"tools/config/bank_{args.bank.lower()}_progress.generated.json"
    return delegate_to(
        'update_bank_progress_v2.py',
        ['--bank', args.bank, '--manifests-dir', args.manifests_dir, '--out', out],
    )

if __name__ == '__main__':
    raise SystemExit(main())
