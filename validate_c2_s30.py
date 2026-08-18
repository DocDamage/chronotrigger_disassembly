#!/usr/bin/env python3
"""Validate Session 30 C2 manifests for overlaps"""

import json
import os
import re

# Load session 30 manifests
with open('C2_SESSION_30_MANIFESTS.json', 'r') as f:
    s30_data = json.load(f)

s30_manifests = s30_data['manifests']

# Parse range strings
def parse_range(range_str):
    """Parse 'C2:8CAB-C2:8D11' into (0x8CAB, 0x8D11)"""
    match = re.match(r'C2:([0-9A-F]+)-C2:([0-9A-F]+)', range_str)
    if match:
        return int(match.group(1), 16), int(match.group(2), 16)
    return None, None

# Check for overlaps within S30 manifests
print("=" * 70)
print("VALIDATING SESSION 30 MANIFESTS")
print("=" * 70)

print("\n1. Checking for internal overlaps...")
s30_ranges = []
for m in s30_manifests:
    start, end = parse_range(m['range'])
    s30_ranges.append((start, end, m['label'], m['pass']))

overlaps_found = False
for i, (s1, e1, l1, p1) in enumerate(s30_ranges):
    for j, (s2, e2, l2, p2) in enumerate(s30_ranges):
        if i < j:  # Only check each pair once
            if not (e1 <= s2 or e2 <= s1):
                print(f"  OVERLAP: Pass {p1} ({l1}) overlaps Pass {p2} ({l2})")
                print(f"           C2:{s1:04X}-C2:{e1:04X} vs C2:{s2:04X}-C2:{e2:04X}")
                overlaps_found = True

if not overlaps_found:
    print("  [OK] No internal overlaps found")

# Check against existing C2 manifests
print("\n2. Checking against existing C2 manifests...")

# Load existing manifests from passes/manifests
existing_ranges = []
manifest_files = [f for f in os.listdir('passes/manifests') if f.startswith('pass_') and f.endswith('.yaml')]

for mf in manifest_files:
    # Skip S30 manifests
    if '_c2_8' in mf and any(str(p) in mf for p in [str(m['pass']) for m in s30_manifests]):
        continue
    
    with open(f'passes/manifests/{mf}', 'r') as f:
        content = f.read()
        # Extract range
        range_match = re.search(r'range:\s*C2:([0-9A-F]+)-C2:([0-9A-F]+)', content)
        if range_match:
            start = int(range_match.group(1), 16)
            end = int(range_match.group(2), 16)
            existing_ranges.append((start, end, mf))

# Also add known S28/S29 manifests from earlier
existing_ranges.extend([
    (0x8006, 0x8090, "pass_1103_c2_8006.yaml"),
    (0x8249, 0x82D5, "pass_1104_c2_8249.yaml"),
    (0x9F1C, 0x9F49, "pass_1090_c2_9f1c.yaml"),
    (0x9F4A, 0x9F8C, "pass_1111_c2_9f4a.yaml"),
])

overlap_with_existing = False
for s1, e1, l1, p1 in s30_ranges:
    for s2, e2, name2 in existing_ranges:
        if not (e1 <= s2 or e2 <= s1):
            print(f"  OVERLAP: Pass {p1} ({l1}) overlaps {name2}")
            print(f"           C2:{s1:04X}-C2:{e1:04X} vs C2:{s2:04X}-C2:{e2:04X}")
            overlap_with_existing = True

if not overlap_with_existing:
    print("  [OK] No overlaps with existing manifests")

# Summary
print("\n" + "=" * 70)
print("VALIDATION SUMMARY")
print("=" * 70)
print(f"Session 30 manifests: {len(s30_manifests)}")
print(f"Internal overlaps: {'YES' if overlaps_found else 'NONE'}")
print(f"External overlaps: {'YES' if overlap_with_existing else 'NONE'}")
print(f"Status: {'VALID' if not overlaps_found and not overlap_with_existing else 'INVALID'}")

# Region coverage analysis
print("\n3. Region coverage...")
regions = {
    '8100-8200': (0x8100, 0x8200),
    '8600-8700': (0x8600, 0x8700),
    '8700-8800': (0x8700, 0x8800),
    '8800-8900': (0x8800, 0x8900),
    '8900-8A00': (0x8900, 0x8A00),
    '8B00-8C00': (0x8B00, 0x8C00),
    '8C00-8D00': (0x8C00, 0x8D00),
    '8D00-8E00': (0x8D00, 0x8E00),
    '8E00-8F00': (0x8E00, 0x8F00),
    '8F00-9000': (0x8F00, 0x9000),
}

for reg_name, (reg_start, reg_end) in regions.items():
    covered = 0
    for s, e, l, p in s30_ranges:
        overlap_start = max(s, reg_start)
        overlap_end = min(e, reg_end)
        if overlap_end > overlap_start:
            covered += overlap_end - overlap_start
    pct = (covered / (reg_end - reg_start)) * 100
    status = "[X]" if covered > 0 else "[ ]"
    print(f"  {status} {reg_name}: {covered:3d}/{reg_end-reg_start:3d} bytes ({pct:.0f}%)")

print("\n" + "=" * 70)
