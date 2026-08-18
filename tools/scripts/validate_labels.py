#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from toolkit_compat import delegate_to

def main() -> int:
    parser = argparse.ArgumentParser(description='Validate Chrono Trigger manifests for overlap and confidence issues')
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--rules', default='tools/config/label_validation_rules.yaml')
    parser.add_argument('--strict-rules', action='store_true', help='Fail if the rules file is missing')
    parser.add_argument('--strict-overlaps', action='store_true', help='Fail when overlap warnings are present')
    args = parser.parse_args()

    if args.strict_rules and not Path(args.rules).exists():
        raise SystemExit(f'rules file not found: {args.rules}')
    forwarded = ['--manifests-dir', args.manifests_dir]
    if args.strict_overlaps:
        forwarded.append('--strict-overlaps')
    return delegate_to('validate_labels_v2.py', forwarded)

if __name__ == '__main__':
    raise SystemExit(main())
