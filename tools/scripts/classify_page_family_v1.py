#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from seam_triage_utils_v1 import classify_page_family

def main() -> int:
    parser = argparse.ArgumentParser(description='Classify a seam/page into a coarse family such as dead_zero_field, text_ascii_heavy, branch_fed_control_pocket, mixed_command_data, or candidate_code_lane')
    parser.add_argument('--rom', required=True)
    parser.add_argument('--range', dest='range_text', required=True)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    rom_bytes = Path(args.rom).read_bytes()
    family, reasons, metrics = classify_page_family(rom_bytes, args.range_text)
    result = {
        'range': args.range_text,
        'page_family': family,
        'reasons': reasons,
        'metrics': metrics,
    }
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"range: {args.range_text}")
        print(f"page_family: {family}")
        print("reasons: " + ", ".join(reasons))
        for key, value in metrics.items():
            print(f"{key}: {value}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
