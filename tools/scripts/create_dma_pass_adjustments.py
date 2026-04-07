#!/usr/bin/env python3
"""Create pass adjustments for DMA high-caller functions"""

import json
import os
import shutil

MANIFESTS_DIR = '../../passes/manifests'
LABELS_DIR = '../../labels'

# Backup and update pass454 to extend to C0:8085
def adjust_pass454():
    """Extend pass454 to include C0:8085/808D entry points"""
    pass_path = os.path.join(MANIFESTS_DIR, 'pass454.json')
    
    with open(pass_path, 'r') as f:
        data = json.load(f)
    
    # Update the range from C0:80BD..C0:813B to C0:8085..C0:813C
    for r in data.get('closed_ranges', []):
        if r.get('range') == 'C0:80BD..C0:813B':
            r['range'] = 'C0:8085..C0:813C'
            r['label'] = 'ct_c0_8085_dma_shared_function_60callers'
            print("Updated pass454:")
            print("  Old range: C0:80BD..C0:813B")
            print("  New range: C0:8085..C0:813C")
            print("  New label: ct_c0_8085_dma_shared_function_60callers")
            print("  Combined callers: 28 (8085) + 32 (808D) = 60")
    
    # Update promotion reason
    data['promotion_reason'] = '60 callers combined (28+32), dual-entry DMA function, RTS at C0:813C, primary entry at C0:808D'
    
    with open(pass_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print("  Saved updated pass454.json\n")

# Create new pass for C0:8500 (or extend pass312)
def create_pass459():
    """Create new pass for C0:8500 DMA setup function"""
    pass_path = os.path.join(MANIFESTS_DIR, 'pass459.json')
    
    data = {
        "pass_number": 459,
        "closed_ranges": [
            {
                "range": "C0:8500..C0:8522",
                "kind": "owner",
                "label": "ct_c0_8500_dma_setup_20callers",
                "confidence": "high"
            }
        ],
        "promotion_reason": "20 callers (strong), DMA setup function, RTS at C0:8522, 34 bytes"
    }
    
    with open(pass_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Created pass459.json:")
    print("  Range: C0:8500..C0:8522")
    print("  Label: ct_c0_8500_dma_setup_20callers")
    print("  Callers: 20")
    print("  Note: Contains pass312 range (851E..8522)")
    print()

def create_label_file():
    """Create label file for C0:8500"""
    label_path = os.path.join(LABELS_DIR, 'ct_c0_8500_dma_setup_20callers.asm')
    
    content = """; C0:8500..C0:8522 - DMA SETUP FUNCTION (20 callers)
; F0 20 C2 20 A5 E9 8D 75 43 E2 20 A6 ...
; First RTS at C0:8522 (+34 bytes)
; Multi-entry DMA utility, often called for VRAM transfer setup
"""
    
    with open(label_path, 'w') as f:
        f.write(content)
    
    print(f"Created label file: {label_path}")

def main():
    print("=" * 70)
    print("DMA HIGH-CALLER PASS ADJUSTMENTS")
    print("=" * 70)
    print()
    
    # Adjust pass454
    adjust_pass454()
    
    # Create pass459
    create_pass459()
    
    # Create label file
    create_label_file()
    
    print("=" * 70)
    print("ADJUSTMENTS COMPLETE")
    print("=" * 70)
    print()
    print("Summary:")
    print("  - pass454: Extended to C0:8085..C0:813C (covers both 8085 and 808D)")
    print("  - pass459: Created for C0:8500..C0:8522")
    print("  - Label file created for C0:8500")
    print()
    print("Note: pass312 (C0:851E..C0:8522) is now contained within pass459")
    print("      Run fix_overlaps.py to resolve this containment.")

if __name__ == '__main__':
    main()
