#!/usr/bin/env python3
"""Validate all C4 Session 27 manifests"""

import json
import os

def main():
    passes_dir = "passes/new_manifests"
    
    # Load summary
    with open('C4_SESSION_27_FINAL_REPORT.json') as f:
        summary = json.load(f)
    
    manifests = summary['all_manifests']
    
    print("=" * 60)
    print("VALIDATING C4 SESSION 27 MANIFESTS")
    print("=" * 60)
    print()
    
    valid = 0
    invalid = 0
    errors = []
    
    for m in manifests:
        filename = m['file'] if 'file' in m else f"pass{m['pass']}_{m['label']}.json"
        filepath = os.path.join(passes_dir, filename)
        
        try:
            with open(filepath) as f:
                data = json.load(f)
                
            # Validate structure
            if 'disassembly' not in data:
                errors.append(f"{filename}: Missing 'disassembly' key")
                invalid += 1
                continue
                
            dis = data['disassembly']
            required = ['pass', 'bank', 'target', 'closure']
            for key in required:
                if key not in dis:
                    errors.append(f"{filename}: Missing 'disassembly.{key}'")
                    invalid += 1
                    break
            else:
                valid += 1
                
        except FileNotFoundError:
            errors.append(f"{filename}: File not found")
            invalid += 1
        except json.JSONDecodeError as e:
            errors.append(f"{filename}: Invalid JSON - {e}")
            invalid += 1
    
    print(f"Total manifests: {len(manifests)}")
    print(f"Valid: {valid}")
    print(f"Invalid: {invalid}")
    print()
    
    if errors:
        print("ERRORS:")
        for e in errors[:10]:
            print(f"  - {e}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more")
    else:
        print("All manifests validated successfully!")
    
    print()
    print("=" * 60)
    print("COVERAGE SUMMARY")
    print("=" * 60)
    print(f"Current C4 coverage: ~6.44%")
    print(f"New coverage added: +{summary['coverage_increase_percent']:.2f}%")
    print(f"Projected C4 coverage: ~{6.44 + summary['coverage_increase_percent']:.2f}%")
    print()
    print("Region distribution:")
    
    # Group by region
    regions = {}
    for m in manifests:
        addr = m['addr']
        # Extract offset
        offset = int(addr.split(':')[1], 16)
        
        if offset < 0x4000:
            region = "0000-3FFF"
        elif offset < 0x6000:
            region = "4000-5FFF"
        elif offset < 0x8000:
            region = "6000-7FFF"
        elif offset < 0xC000:
            region = "8000-BFFF"
        else:
            region = "C000-FFFF"
        
        if region not in regions:
            regions[region] = {"count": 0, "bytes": 0}
        regions[region]["count"] += 1
        regions[region]["bytes"] += m['bytes']
    
    for region, stats in sorted(regions.items()):
        print(f"  {region}: {stats['count']} manifests, {stats['bytes']} bytes")

if __name__ == '__main__':
    main()
