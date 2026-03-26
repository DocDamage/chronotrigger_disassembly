#!/usr/bin/env python3
from __future__ import annotations
import argparse

def main() -> int:
    parser = argparse.ArgumentParser(description='Build a call-anchor report')
    parser.add_argument('--range', required=True)
    args = parser.parse_args()
    print(f'[stub] build xref/call-anchor report for {args.range}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
