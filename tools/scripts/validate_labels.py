#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import yaml

def main() -> int:
    parser = argparse.ArgumentParser(description='Validate Chrono Trigger labels')
    parser.add_argument('--rules', default='tools/config/label_validation_rules.yaml')
    args = parser.parse_args()
    rules = yaml.safe_load(Path(args.rules).read_text(encoding='utf-8'))
    print([rule['id'] for rule in rules['rules']])
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
