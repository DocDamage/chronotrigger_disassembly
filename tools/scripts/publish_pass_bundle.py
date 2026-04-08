#!/usr/bin/env python3
from __future__ import annotations

import argparse

from toolkit_compat import delegate_to

def main() -> int:
    parser = argparse.ArgumentParser(description='Publish a Chrono Trigger disassembly pass bundle')
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--repo-root', default='.')
    parser.add_argument('--note', default='')
    args = parser.parse_args()

    return delegate_to(
        'publish_pass_bundle_v2.py',
        ['--manifest', args.manifest, '--repo-root', args.repo_root, '--note', args.note],
    )

if __name__ == '__main__':
    raise SystemExit(main())
