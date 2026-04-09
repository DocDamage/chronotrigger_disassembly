#!/usr/bin/env python3
"""Create manifests for C1 Session 25 - covering all regions."""

import json
import os
from pathlib import Path

SCAN_FILES = {
    '2000-3000': 'c1_2000_scan.json',
    '3000-4000': 'c1_3000_scan.json',
    '8000-9000': 'c1_8000_scan.json',
    '9000-A000': 'c1_9000_scan.json',
    'A000-B000': 'c1_a000_scan.json',
    'B000-C000': 'c1_b000_scan.json',
    'C000-D000': 'c1_c000_scan.json',
    'D000-E000': 'c1_d000_scan.json',
    'E000-F000': 'c1_e000_scan.json',
    'F000-FFFF': 'c1_f000_scan.json',
}

OUTPUT_DIR = "labels/c1_session25"

def parse_address(addr_str):
    """Parse C1:XXXX address string to integer."""
    return int(addr_str.split(':')[1], 16)

def create_manifest(island, region):
    """Create a manifest file for a candidate."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    range_str = island['range']
    start_addr = range_str.split('..')[0]
    end_addr = range_str.split('..')[1]
    
    start_int = parse_address(start_addr)
    end_int = parse_address(end_addr)
    
    score = island['score']
    calls = island['call_count']
    branches = island['branch_count']
    
    # Generate a descriptive name
    if calls >= 2:
        func_type = "hub"
    elif calls == 1:
        func_type = "handler"
    elif branches >= 3:
        func_type = "brancher"
    else:
        func_type = "util"
    
    name = f"ct_c1_{start_int:04x}_{func_type}_s25"
    filename = f"C1_{start_int:04X}_score{score}_s25.yaml"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    manifest = {
        'manifest_version': '1.0',
        'session': 25,
        'target': {
            'bank': 'C1',
            'start_addr': start_addr,
            'end_addr': end_addr,
            'name': name
        },
        'metadata': {
            'score': score,
            'call_count': calls,
            'branch_count': branches,
            'return_count': island['return_count'],
            'width': island['width'],
            'ascii_ratio': island['ascii_ratio'],
            'region': region
        },
        'disassembly': {
            'mode': 'code',
            'merge_policy': 'session_priority'
        }
    }
    
    with open(filepath, 'w') as fp:
        json.dump(manifest, fp, indent=2)
    
    return filepath, name

def main():
    print('=' * 60)
    print('Creating C1 Session 25 Manifests')
    print('=' * 60)
    
    # Collect all score-7+ candidates from all regions
    all_candidates = []
    
    for region, filepath in SCAN_FILES.items():
        if os.path.exists(filepath):
            with open(filepath) as f:
                data = json.load(f)
            
            for island in data.get('islands', []):
                if island['score'] >= 7:
                    all_candidates.append({
                        'island': island,
                        'region': region,
                        'start_int': parse_address(island['range'].split('..')[0])
                    })
    
    # Sort by start address to ensure good distribution
    all_candidates.sort(key=lambda x: x['start_int'])
    
    print(f"\nFound {len(all_candidates)} score-7+ candidates")
    
    # Select candidates with good distribution across regions
    # Aim for 8-10 total, distributed across different regions
    selected = []
    used_addrs = set()
    
    # First pass: select one from each region that has candidates
    regions_covered = set()
    for c in all_candidates:
        region = c['region']
        addr = c['start_int']
        
        # Skip if too close to already selected
        too_close = any(abs(addr - used) < 64 for used in used_addrs)
        if too_close:
            continue
        
        if region not in regions_covered and len(selected) < 10:
            selected.append(c)
            used_addrs.add(addr)
            regions_covered.add(region)
    
    # Second pass: fill remaining slots with highest scores
    for c in all_candidates:
        addr = c['start_int']
        too_close = any(abs(addr - used) < 64 for used in used_addrs)
        if too_close or c in selected:
            continue
        
        if len(selected) < 10:
            selected.append(c)
            used_addrs.add(addr)
    
    # Create manifests
    print(f"\nCreating {len(selected)} manifests:")
    manifests = []
    for c in selected:
        filepath, name = create_manifest(c['island'], c['region'])
        manifests.append({
            'filepath': filepath,
            'name': name,
            'region': c['region'],
            'score': c['island']['score'],
            'range': c['island']['range']
        })
        print(f"  {filepath}: {name} (score {c['island']['score']}, {c['region']})")
    
    # Summary
    print('\n### Manifest Summary ###')
    print(f"Total manifests created: {len(manifests)}")
    
    by_region = {}
    for m in manifests:
        r = m['region']
        by_region[r] = by_region.get(r, 0) + 1
    
    print("\nBy region:")
    for r, count in sorted(by_region.items()):
        print(f"  {r}: {count}")
    
    # Write summary report
    report = {
        'session': 25,
        'bank': 'C1',
        'total_manifests': len(manifests),
        'total_candidates_analyzed': len(all_candidates),
        'regions_covered': list(by_region.keys()),
        'manifests': manifests
    }
    
    report_path = 'C1_SESSION25_REPORT.json'
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nReport saved to: {report_path}")
    
    return manifests

if __name__ == '__main__':
    main()
