#!/usr/bin/env python3
"""
Validate C1 Session 26 manifests.

Checks:
1. All manifest files exist and are valid JSON
2. Address ranges are valid and non-overlapping
3. Required fields are present
4. Score values are reasonable
5. No duplicate addresses
"""

import json
import os
from pathlib import Path

OUTPUT_DIR = "labels/c1_session26"
REPORT_FILE = "C1_SESSION26_REPORT.json"

def parse_address(addr_str):
    """Parse C1:XXXX address string to integer."""
    return int(addr_str.split(':')[1], 16)

def validate_manifests():
    print('=' * 70)
    print('C1 Session 26 Manifest Validation')
    print('=' * 70)
    
    # Load report
    if not os.path.exists(REPORT_FILE):
        print(f"ERROR: Report file {REPORT_FILE} not found!")
        return False
    
    with open(REPORT_FILE) as f:
        report = json.load(f)
    
    manifests = report.get('manifests', [])
    print(f"\nValidating {len(manifests)} manifests...")
    
    all_valid = True
    errors = []
    warnings = []
    
    # Track addresses for overlap detection
    address_ranges = []
    
    for i, m in enumerate(manifests):
        filepath = m.get('filepath', '')
        name = m.get('name', 'unknown')
        
        # Check file exists
        if not os.path.exists(filepath):
            errors.append(f"File not found: {filepath}")
            all_valid = False
            continue
        
        # Load and validate JSON
        try:
            with open(filepath) as f:
                manifest_data = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON in {filepath}: {e}")
            all_valid = False
            continue
        
        # Check required fields
        required_fields = ['manifest_version', 'session', 'target', 'metadata', 'disassembly']
        for field in required_fields:
            if field not in manifest_data:
                errors.append(f"Missing field '{field}' in {filepath}")
                all_valid = False
        
        # Validate target fields
        target = manifest_data.get('target', {})
        target_fields = ['bank', 'start_addr', 'end_addr', 'name']
        for field in target_fields:
            if field not in target:
                errors.append(f"Missing target field '{field}' in {filepath}")
                all_valid = False
        
        # Validate address range
        start_addr = target.get('start_addr', '')
        end_addr = target.get('end_addr', '')
        
        if not start_addr.startswith('C1:') or not end_addr.startswith('C1:'):
            errors.append(f"Invalid address format in {filepath}")
            all_valid = False
        else:
            try:
                start_int = parse_address(start_addr)
                end_int = parse_address(end_addr)
                
                if start_int >= end_int:
                    errors.append(f"Invalid range (start >= end) in {filepath}: {start_addr}..{end_addr}")
                    all_valid = False
                
                if start_int < 0 or end_int > 0xFFFF:
                    errors.append(f"Address out of bounds in {filepath}")
                    all_valid = False
                
                # Check for overlaps
                for prev_start, prev_end, prev_name in address_ranges:
                    if not (end_int <= prev_start or start_int >= prev_end):
                        errors.append(f"Address overlap: {name} ({start_addr}..{end_addr}) overlaps with {prev_name}")
                        all_valid = False
                
                address_ranges.append((start_int, end_int, name))
                
            except ValueError as e:
                errors.append(f"Address parse error in {filepath}: {e}")
                all_valid = False
        
        # Validate metadata
        metadata = manifest_data.get('metadata', {})
        score = metadata.get('score', 0)
        if score < 6:
            warnings.append(f"Low score ({score}) in {filepath}")
        
        call_count = metadata.get('call_count', -1)
        branch_count = metadata.get('branch_count', -1)
        return_count = metadata.get('return_count', -1)
        
        if call_count < 0 or branch_count < 0 or return_count < 0:
            warnings.append(f"Missing metrics in {filepath}")
        
        # Validate session
        session = manifest_data.get('session', 0)
        if session != 26:
            warnings.append(f"Unexpected session number ({session}) in {filepath}")
        
        print(f"  [OK] {filepath}")
    
    # Print results
    print("\n" + "=" * 70)
    if all_valid and not warnings:
        print("VALIDATION PASSED - All manifests are valid!")
    elif all_valid:
        print("VALIDATION PASSED WITH WARNINGS")
    else:
        print("VALIDATION FAILED")
    print("=" * 70)
    
    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for e in errors[:10]:  # Show first 10
            print(f"  [ERR] {e}")
        if len(errors) > 10:
            print(f"  ... and {len(errors) - 10} more errors")
    
    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for w in warnings[:10]:
            print(f"  ! {w}")
        if len(warnings) > 10:
            print(f"  ... and {len(warnings) - 10} more warnings")
    
    # Coverage summary
    print(f"\nCoverage Summary:")
    total_bytes = sum(end - start for start, end, _ in address_ranges)
    print(f"  Total manifests: {len(manifests)}")
    print(f"  Total bytes covered: {total_bytes}")
    print(f"  Address ranges: {len(address_ranges)}")
    print(f"  Bank C1 coverage: ~{total_bytes / 65536 * 100:.2f}%")
    
    # Region coverage
    region_bytes = {}
    for m in manifests:
        region = m.get('region', 'unknown')
        width = m.get('width', 0)
        region_bytes[region] = region_bytes.get(region, 0) + width
    
    print(f"\nCoverage by Region:")
    for region, bytes_covered in sorted(region_bytes.items()):
        print(f"  {region}: {bytes_covered} bytes")
    
    print("=" * 70)
    
    return all_valid


if __name__ == '__main__':
    validate_manifests()
