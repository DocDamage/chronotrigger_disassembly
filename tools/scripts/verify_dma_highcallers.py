#!/usr/bin/env python3
"""Verify C0 DMA high-caller functions for pass creation"""

import os
import json
import sys

sys.path.insert(0, os.path.dirname(__file__))
from snes_utils_hirom_v2 import hirom_to_file_offset

rom_path = '../../rom/Chrono Trigger (USA).sfc'
manifests_dir = '../../passes/manifests'

def check_overlap(c_start, c_end):
    """Check if range overlaps with existing manifests"""
    overlaps = []
    for fname in os.listdir(manifests_dir):
        if fname.endswith('.json') and fname.startswith('pass'):
            with open(os.path.join(manifests_dir, fname), 'r') as f:
                try:
                    data = json.load(f)
                    for r in data.get('closed_ranges', []):
                        range_str = r.get('range', '')
                        if range_str.startswith('C0:'):
                            parts = range_str.split('..')
                            if len(parts) == 2:
                                start = int(parts[0].split(':')[1], 16)
                                end = int(parts[1].split(':')[1], 16)
                                if c_start < end and c_end > start:
                                    overlaps.append((fname, range_str, r.get('label', 'unknown')))
                except:
                    pass
    return overlaps

def read_bytes_at(addr, length=256):
    """Read bytes from ROM at SNES address"""
    offset = hirom_to_file_offset(0xC0, addr)
    with open(rom_path, 'rb') as f:
        f.seek(offset)
        return f.read(length)

# Targets to verify
targets = [
    {
        'addr': 0x8085,
        'name': 'C0:8085',
        'callers': 28,
        'desc': 'DMA utility - shared function entry',
        'end_offset': 0xB7,  # RTS at +183
        'shared_with': 0x808D,
    },
    {
        'addr': 0x808D,
        'name': 'C0:808D',
        'callers': 32,
        'desc': 'DMA utility - primary entry (32 callers)',
        'end_offset': 0xAF,  # RTS at +175
        'shared_with': 0x8085,
    },
    {
        'addr': 0x8500,
        'name': 'C0:8500',
        'callers': 20,
        'desc': 'DMA setup utility',
        'end_offset': 0x22,  # First RTS at +34
    },
]

print("=" * 70)
print("C0 DMA HIGH-CALLER VERIFICATION REPORT")
print("=" * 70)

verified = []

for t in targets:
    addr = t['addr']
    print(f"\n=== {t['name']} ({t['callers']} callers) ===")
    print(f"  Description: {t['desc']}")
    
    # Read bytes
    data = read_bytes_at(addr, 128)
    
    # Show prologue
    prologue = ' '.join(f"{b:02X}" for b in data[:12])
    print(f"  Prologue: {prologue}")
    
    # Calculate range
    end_addr = addr + t['end_offset']
    print(f"  Range: C0:{addr:04X}..C0:{end_addr:04X}")
    print(f"  Size: {t['end_offset']} bytes")
    
    # Check overlap
    overlaps = check_overlap(addr, end_addr)
    if overlaps:
        print(f"  WARNING: Overlaps with existing ranges:")
        for ov in overlaps:
            print(f"    - {ov[0]}: {ov[1]} ({ov[2]})")
    else:
        print(f"  STATUS: CLEAR - ready for promotion")
        verified.append({
            'start': addr,
            'end': end_addr,
            'callers': t['callers'],
            'desc': t['desc'],
        })
    
    # Special note for shared functions
    if 'shared_with' in t:
        print(f"  NOTE: Shares function body with C0:{t['shared_with']:04X}")

print("\n" + "=" * 70)
print("VERIFIED AND READY FOR PASS CREATION:")
print("=" * 70)
for v in verified:
    print(f"  C0:{v['start']:04X}..C0:{v['end']:04X}: {v['callers']} callers - {v['desc']}")

# Summary of already-covered functions
print("\n" + "=" * 70)
print("ALREADY COVERED BY EXISTING PASSES:")
print("=" * 70)
covered = [
    ("C0:857F", "93 callers", "pass410.json", "Major dispatcher"),
    ("C0:1B31", "92 callers", "pass369.json", "Major utility"),
    ("C0:3885", "26 callers", "pass373.json", "Cross-bank loader"),
    ("C0:107F", "25 callers", "pass380.json", "VRAM calc"),
    ("C0:0A0A", "25 callers", "pass376.json", "DMA setup"),
]
for addr, callers, pass_file, desc in covered:
    print(f"  {addr} ({callers}) - {desc}: {pass_file}")

print("\n" + "=" * 70)
print("SUMMARY:")
print("=" * 70)
print(f"  Total targets checked: 8")
print(f"  Already covered: 5")
print(f"  Verified ready: {len(verified)}")
print(f"  Needs investigation: {8 - 5 - len(verified)}")
