#!/usr/bin/env python3
"""Analyze C1 new region scans and create manifests for score-6+ candidates."""

import json
import os
from pathlib import Path

SCAN_FILES = [
    'c1_c000_scan.json',
    'c1_d000_scan.json',
    'c1_e000_scan.json',
    'c1_f000_scan.json',
]

def load_scan_results():
    """Load and merge all scan results."""
    all_islands = []
    for f in SCAN_FILES:
        if os.path.exists(f):
            with open(f) as fp:
                data = json.load(fp)
                for island in data.get('islands', []):
                    island['source_file'] = f
                all_islands.extend(data.get('islands', []))
    return all_islands

def get_score6_plus_candidates(islands):
    """Filter for score-6+ candidates."""
    return [i for i in islands if i['score'] >= 6]

def parse_address(addr_str):
    """Parse C1:XXXX address string to integer."""
    return int(addr_str.split(':')[1], 16)

def format_address(addr):
    """Format integer address to C1:XXXX."""
    return f"C1:{addr:04X}"

def create_manifest(island, output_dir="labels/c1_session25"):
    """Create a manifest file for a candidate."""
    os.makedirs(output_dir, exist_ok=True)
    
    range_str = island['range']
    start_addr = range_str.split('..')[0]
    end_addr = range_str.split('..')[1]
    
    start_int = parse_address(start_addr)
    end_int = parse_address(end_addr)
    
    # Generate a descriptive name based on characteristics
    score = island['score']
    calls = island['call_count']
    branches = island['branch_count']
    
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
    filepath = os.path.join(output_dir, filename)
    
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
            'source_file': island.get('source_file', 'unknown')
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
    print("=" * 60)
    print("Bank C1 New Regions Analysis - Session 25")
    print("=" * 60)
    
    islands = load_scan_results()
    print(f"\nTotal islands found: {len(islands)}")
    
    candidates = get_score6_plus_candidates(islands)
    print(f"Score-6+ candidates: {len(candidates)}")
    
    # Sort by score (descending), then by start address
    candidates.sort(key=lambda x: (-x['score'], parse_address(x['range'].split('..')[0])))
    
    print("\n### Top Score-6+ Candidates ###")
    for i, c in enumerate(candidates[:20]):
        range_str = c['range']
        print(f"  {range_str}: score={c['score']}, calls={c['call_count']}, "
              f"branches={c['branch_count']}, width={c['width']}")
    
    # Create manifests for top candidates (aim for 8-10)
    print("\n### Creating Manifests ###")
    manifests_created = []
    
    # Prioritize diverse addresses and high scores
    used_addrs = set()
    for c in candidates:
        start_addr = c['range'].split('..')[0]
        addr_int = parse_address(start_addr)
        
        # Skip if too close to an already selected address
        too_close = any(abs(addr_int - used) < 32 for used in used_addrs)
        if too_close:
            continue
        
        filepath, name = create_manifest(c)
        manifests_created.append((filepath, name, c))
        used_addrs.add(addr_int)
        
        if len(manifests_created) >= 10:
            break
    
    print(f"\nCreated {len(manifests_created)} manifests:")
    for filepath, name, c in manifests_created:
        print(f"  {filepath}: {name} (score {c['score']})")
    
    print("\n### Coverage Summary ###")
    regions_covered = set()
    for c in manifests_created:
        addr = parse_address(c[2]['range'].split('..')[0])
        if 0xC000 <= addr < 0xD000:
            regions_covered.add("C000-D000")
        elif 0xD000 <= addr < 0xE000:
            regions_covered.add("D000-E000")
        elif 0xE000 <= addr < 0xF000:
            regions_covered.add("E000-F000")
        elif 0xF000 <= addr <= 0xFFFF:
            regions_covered.add("F000-FFFF")
    
    print(f"Regions covered: {sorted(regions_covered)}")
    
    return manifests_created

if __name__ == '__main__':
    main()
