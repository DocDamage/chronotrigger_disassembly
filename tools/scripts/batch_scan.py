#!/usr/bin/env python3
"""
Batch scan multiple Bank C0 regions and auto-promote high-caller targets.
"""

import json
import subprocess
import os
import sys
import argparse
from pathlib import Path
from typing import List, Tuple
import tempfile

# Priority regions to scan (from coverage analysis)
DEFAULT_REGIONS = [
    ("C0:CF00", 7),  # 1792 bytes - largest gap
    ("C0:B400", 5),  # 1280 bytes
    ("C0:F900", 5),  # 1280 bytes
    ("C0:3100", 4),  # 1024 bytes
    ("C0:4700", 4),  # 1024 bytes
]


def run_scan(start: str, pages: int, rom_path: str) -> dict:
    """Run seam block scan and return JSON data."""
    cmd = [
        'python', 'run_seam_block_v1.py',
        '--rom', rom_path,
        '--start', start,
        '--pages', str(pages),
        '--json'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd='.')
    
    if result.returncode != 0:
        print(f"Error scanning {start}: {result.stderr}")
        return None
    
    try:
        # Find JSON output (may be mixed with other output)
        output = result.stdout
        # Find the start of JSON
        json_start = output.find('{')
        if json_start >= 0:
            return json.loads(output[json_start:])
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON for {start}: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='Batch scan Bank C0 regions')
    parser.add_argument('--rom', '-r', default='../../rom/Chrono Trigger (USA).sfc',
                        help='Path to ROM file')
    parser.add_argument('--regions', nargs='+', help='Custom regions to scan (e.g., C0:1000:4)')
    parser.add_argument('--min-callers', '-c', type=int, default=2,
                        help='Minimum caller count for promotion')
    parser.add_argument('--auto-promote', '-a', action='store_true',
                        help='Auto-promote targets after scanning')
    parser.add_argument('--output-dir', '-o', default='../../scans',
                        help='Directory to save scan results')
    
    args = parser.parse_args()
    
    # Determine regions to scan
    if args.regions:
        regions = []
        for r in args.regions:
            parts = r.split(':')
            if len(parts) >= 3:
                regions.append((f"{parts[0]}:{parts[1]}", int(parts[2])))
    else:
        regions = DEFAULT_REGIONS
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_targets = []
    
    print("=" * 70)
    print("BANK C0 BATCH SCAN")
    print("=" * 70)
    print(f"Scanning {len(regions)} regions...\n")
    
    for start, pages in regions:
        print(f"\nScanning {start} ({pages} pages)...")
        print("-" * 70)
        
        scan_data = run_scan(start, pages, args.rom)
        
        if not scan_data:
            print(f"  ❌ Failed to scan {start}")
            continue
        
        # Save scan result
        output_file = output_dir / f"scan_{start.replace(':', '_')}_{pages}p.json"
        with open(output_file, 'w') as f:
            json.dump(scan_data, f, indent=2)
        print(f"  ✓ Saved to {output_file}")
        
        # Extract targets
        from auto_promote import extract_targets_from_scan
        targets = extract_targets_from_scan(scan_data)
        high_callers = [t for t in targets if t['caller_count'] >= args.min_callers]
        
        print(f"  Found {len(targets)} targets, {len(high_callers)} with {args.min_callers}+ callers")
        
        if high_callers:
            print(f"\n  High-caller targets:")
            for t in sorted(high_callers, key=lambda x: -x['caller_count']):
                status = "✓" if t['strength'] == 'weak' else "?"
                print(f"    {status} {t['target']}: {t['caller_count']} callers ({t['strength']})")
        
        all_targets.extend(high_callers)
    
    # Summary
    print("\n" + "=" * 70)
    print("BATCH SCAN COMPLETE")
    print("=" * 70)
    print(f"Total regions scanned: {len(regions)}")
    print(f"Total high-caller targets: {len(all_targets)}")
    
    if all_targets and args.auto_promote:
        print("\n" + "=" * 70)
        print("AUTO-PROMOTING TARGETS")
        print("=" * 70)
        
        # Create combined scan file for auto_promote
        combined = {'pages': []}
        for start, pages in regions:
            scan_file = output_dir / f"scan_{start.replace(':', '_')}_{pages}p.json"
            if scan_file.exists():
                with open(scan_file) as f:
                    data = json.load(f)
                    combined['pages'].extend(data.get('pages', []))
        
        combined_file = output_dir / 'combined_scan.json'
        with open(combined_file, 'w') as f:
            json.dump(combined, f, indent=2)
        
        # Run auto-promote
        subprocess.run([
            'python', 'auto_promote.py',
            '--scan-file', str(combined_file),
            '--min-callers', str(args.min_callers),
            '--auto-fix'
        ])
    elif all_targets:
        print("\nTo auto-promote these targets, run:")
        print(f"  python auto_promote.py --scan-file {output_dir}/combined_scan.json --auto-fix")


if __name__ == '__main__':
    main()
