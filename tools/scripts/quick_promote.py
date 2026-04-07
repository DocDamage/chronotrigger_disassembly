#!/usr/bin/env python3
"""
Quick promote a single target with automatic boundary suggestion and conflict checking.
Usage: python quick_promote.py C0:1234 --callers 5
"""

import json
import argparse
import sys
from pathlib import Path

MANIFESTS_DIR = Path('../../passes/manifests')


def find_next_pass_number() -> int:
    """Find the next available pass number."""
    max_num = 0
    for mf in MANIFESTS_DIR.glob('pass*.json'):
        try:
            num = int(mf.stem.replace('pass', ''))
            max_num = max(max_num, num)
        except:
            pass
    return max_num + 1


def addr_to_int(addr: str) -> int:
    bank, offset = addr.split(':')
    return int(bank, 16) * 0x10000 + int(offset, 16)


def int_to_addr(val: int) -> str:
    bank = val // 0x10000
    offset = val % 0x10000
    return f"C{bank}:{offset:04X}"


def check_conflicts(start: str, end: str) -> list:
    """Check for conflicts with existing passes."""
    conflicts = []
    bank = start.split(':')[0]
    s = addr_to_int(start)
    e = addr_to_int(end)
    
    for mf in MANIFESTS_DIR.glob('pass*.json'):
        try:
            with open(mf) as f:
                data = json.load(f)
            for r in data.get('closed_ranges', []):
                range_str = r['range']
                rs, re = range_str.split('..')
                if not rs.startswith(f'{bank}:'):
                    continue
                rs_int = addr_to_int(rs)
                re_int = addr_to_int(re)
                
                if not (e < rs_int or re_int < s):
                    conflicts.append((mf.name, range_str))
        except:
            pass
    
    return conflicts


def main():
    parser = argparse.ArgumentParser(description='Quick promote a target')
    parser.add_argument('target', help='Target address (e.g., C0:1234)')
    parser.add_argument('--start', '-s', help='Start address (default: target)')
    parser.add_argument('--size', '-z', type=int, default=30, help='Function size (default: 30)')
    parser.add_argument('--callers', '-c', type=int, required=True, help='Number of callers')
    parser.add_argument('--strength', '-t', default='weak', choices=['weak', 'strong', 'suspect'],
                        help='Target strength')
    parser.add_argument('--label', '-l', help='Custom label')
    parser.add_argument('--confidence', '-f', default='medium', choices=['high', 'medium', 'low'],
                        help='Confidence level')
    parser.add_argument('--reason', '-r', help='Promotion reason')
    parser.add_argument('--dry-run', '-n', action='store_true', help='Dry run')
    
    args = parser.parse_args()
    
    # Calculate range
    target = args.target
    start = args.start or target
    bank = start.split(':')[0]
    start_int = addr_to_int(start)
    end_int = start_int + args.size
    end = int_to_addr(end_int)
    range_str = f"{start}..{end}"
    
    print("=" * 70)
    print("QUICK PROMOTE")
    print("=" * 70)
    print(f"Target: {target}")
    print(f"Range: {range_str}")
    print(f"Callers: {args.callers}")
    print(f"Strength: {args.strength}")
    
    # Check conflicts
    print("\nChecking for conflicts...")
    conflicts = check_conflicts(start, end)
    
    if conflicts:
        print("[FAIL] CONFLICTS FOUND:")
        for name, r in conflicts:
            print(f"  {name}: {r}")
        print("\nResolve conflicts before promoting.")
        sys.exit(1)
    else:
        print("[OK] No conflicts")
    
    # Create manifest
    label = args.label or f"ct_c0_{start.replace(':', '').lower()}_function_{args.callers}callers"
    reason = args.reason or f"{args.callers} callers ({args.strength})"
    
    manifest = {
        "pass_number": find_next_pass_number(),
        "closed_ranges": [{
            "range": range_str,
            "kind": "owner",
            "label": label,
            "confidence": args.confidence
        }],
        "promotion_reason": reason
    }
    
    print("\n" + "=" * 70)
    print("MANIFEST PREVIEW")
    print("=" * 70)
    print(json.dumps(manifest, indent=2))
    
    if not args.dry_run:
        output_file = MANIFESTS_DIR / f"pass{manifest['pass_number']}.json"
        with open(output_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        print(f"\n[OK] Created {output_file.name}")
    else:
        print(f"\n[DRY RUN] Would create pass{manifest['pass_number']}.json")


if __name__ == '__main__':
    main()
