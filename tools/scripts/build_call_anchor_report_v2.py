#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from snes_utils import format_offset_as_snes, iter_all_call_patterns, parse_snes_address


def main() -> int:
    parser = argparse.ArgumentParser(description='Build a call-anchor report from raw ROM bytes')
    parser.add_argument('--rom', required=True)
    parser.add_argument('--target', required=True, help='Exact entry address like C3:1025')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    bank, addr = parse_snes_address(args.target)
    rom_bytes = Path(args.rom).read_bytes()
    hits = []
    for kind, offset in iter_all_call_patterns(rom_bytes, bank, addr):
        hits.append({'kind': kind, 'call_site': format_offset_as_snes(offset)})

    result = {'target': args.target, 'call_count': len(hits), 'calls': hits[:500]}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"target: {args.target}")
        print(f"call_count: {len(hits)}")
        for item in hits[:100]:
            print(f"  {item['kind']} from {item['call_site']}")
        if len(hits) > 100:
            print(f"  ... truncated {len(hits) - 100} additional hits")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
