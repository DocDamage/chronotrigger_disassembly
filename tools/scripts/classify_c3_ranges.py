#!/usr/bin/env python3
from __future__ import annotations
import argparse

def main() -> int:
    parser = argparse.ArgumentParser(description='Classify candidate C3 ranges')
    parser.add_argument('--range', required=True)
    args = parser.parse_args()
    print(f'[stub] classify {args.range} as code/data/text/padding candidate')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
