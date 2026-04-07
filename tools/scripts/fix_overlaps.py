#!/usr/bin/env python3
"""
Execute overlap resolution for Bank C0.
Removes redundant passes and adjusts boundaries where needed.
"""

import json
import os
import shutil

MANIFESTS_DIR = '../../passes/manifests'
LABELS_DIR = '../../labels'
BACKUP_DIR = '../../passes/backup'

# Files to remove (containment cases)
REMOVE_FILES = [
    'pass282.json',   # C0:4098 inside pass428
    'pass307.json',   # C0:7BA0 inside pass263
    'pass316.json',   # C0:8719 inside pass273
    'pass322.json',   # C0:943C inside pass274
    'pass331.json',   # C0:A396 inside pass265
    'pass335.json',   # C0:B188 inside pass424
    'pass341.json',   # C0:BCD7 inside pass266
    'pass357.json',   # C0:EC6D inside pass356
    'pass361.json',   # C0:F0B9 inside pass278
    'pass384.json',   # C0:2C32 inside pass261
    'pass388.json',   # C0:520E inside pass284
    'pass392.json',   # C0:568B inside pass258
    'pass398.json',   # C0:7BA4 inside pass263/307
    'pass400.json',   # C0:0B75 inside pass383
    'pass425.json',   # C0:F0B9 inside pass278
    'pass312.json',   # C0:851E..C0:8522 inside pass459 (C0:8500..C0:8522)
]

# Boundary adjustments needed
ADJUSTMENTS = [
    # Adjust pass254 end to avoid overlap with pass387
    ('pass254.json', 'C0:3030..C0:3080', 'C0:3030..C0:302F'),
    
    # Adjust pass275 to avoid overlap with pass415 (A67A..A711 has 32 callers!)
    ('pass275.json', 'C0:A704..C0:A760', 'C0:A712..C0:A760'),
    
    # Adjust pass333 to avoid overlap with pass416 (A988..A9B3 has 16 callers!)
    ('pass333.json', 'C0:A979..C0:A989', 'C0:A979..C0:A987'),
    
    # Adjust pass284 to avoid overlap with pass389 (527B has 15 callers)
    ('pass284.json', 'C0:520E..C0:5280', 'C0:520E..C0:527A'),
]

def backup_and_remove():
    """Remove redundant pass files"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    
    print("=== REMOVING REDUNDANT PASSES ===")
    for fname in REMOVE_FILES:
        src = os.path.join(MANIFESTS_DIR, fname)
        dst = os.path.join(BACKUP_DIR, fname)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"  Moved {fname} to backup")
        else:
            print(f"  {fname} already removed")
    
    print(f"\nRemoved {len(REMOVE_FILES)} redundant passes")

def adjust_boundaries():
    """Adjust pass boundaries to avoid overlaps"""
    print("\n=== ADJUSTING BOUNDARIES ===")
    
    for fname, old_range, new_range in ADJUSTMENTS:
        path = os.path.join(MANIFESTS_DIR, fname)
        if not os.path.exists(path):
            print(f"  {fname} not found, skipping")
            continue
        
        with open(path, 'r') as f:
            data = json.load(f)
        
        # Update the range
        for r in data.get('closed_ranges', []):
            if r.get('range') == old_range:
                r['range'] = new_range
                # Update label to reflect new boundary
                old_label = r.get('label', '')
                # Parse addresses
                old_start = old_range.split('..')[0].split(':')[1]
                new_start = new_range.split('..')[0].split(':')[1]
                new_end = new_range.split('..')[1].split(':')[1]
                print(f"  {fname}: {old_range} -> {new_range}")
                break
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

def main():
    print("BANK C0 OVERLAP RESOLUTION")
    print("=" * 60)
    
    # First backup and remove
    backup_and_remove()
    
    # Then adjust boundaries
    adjust_boundaries()
    
    print("\n=== COMPLETE ===")
    print("Run validate_labels_v2.py to verify all overlaps are resolved")

if __name__ == '__main__':
    main()
