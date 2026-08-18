#!/usr/bin/env python3
"""Create manifests for Bank C0 score-6+ candidates."""
import json
import os
from pathlib import Path

# Selected candidates for new functions (15-18 recommended)
# Focusing on DMA/HDMA regions and clusters
SELECTED_CANDIDATES = [
    # DMA setup region cluster (near existing DMA functions)
    {"addr": "C0:8756", "score": 6, "name": "CT_C0_8756_DMA_UTIL_SCORE6", "desc": "DMA utility function near DMA setup cluster"},
    {"addr": "C0:8805", "score": 6, "name": "CT_C0_8805_GRAPHICS_INIT_SCORE6", "desc": "Graphics init with REP #$20 prologue"},
    {"addr": "C0:882B", "score": 6, "name": "CT_C0_882B_DMA_CHAIN_SCORE6", "desc": "DMA chain handler, part of DMA setup cluster"},
    
    # Graphics engine functions
    {"addr": "C0:9155", "score": 6, "name": "CT_C0_9155_SPRITE_SETUP_SCORE6", "desc": "Sprite setup with JSR chain"},
    {"addr": "C0:916C", "score": 6, "name": "CT_C0_916C_MODE_SWITCH_SCORE6", "desc": "Mode switch with REP #$20/C2 start"},
    
    # Input/Window handling
    {"addr": "C0:98A6", "score": 6, "name": "CT_C0_98A6_WINDOW_CONFIG_SCORE6", "desc": "Window configuration handler"},
    {"addr": "C0:98D7", "score": 6, "name": "CT_C0_98D7_LAYER_MASK_SCORE6", "desc": "Layer mask setup function"},
    {"addr": "C0:9908", "score": 6, "name": "CT_C0_9908_EFFECT_CTRL_SCORE6", "desc": "Effect control handler"},
    
    # Engine utility functions
    {"addr": "C0:9A29", "score": 6, "name": "CT_C0_9A29_STATE_COPY_SCORE6", "desc": "State copy with PHP/PHB prologue"},
    {"addr": "C0:9ABD", "score": 6, "name": "CT_C0_9ABD_PHA_HANDLER_SCORE6", "desc": "Stack-based handler with PHA/PHY/PHX"},
    
    # Math/Coord functions
    {"addr": "C0:A372", "score": 6, "name": "CT_C0_A372_COORD_MATH_SCORE6", "desc": "Coordinate math with JSR chain"},
    {"addr": "C0:A46C", "score": 6, "name": "CT_C0_A46C_FLAG_TEST_SCORE6", "desc": "Flag test with LDA immediate"},
    {"addr": "C0:A598", "score": 6, "name": "CT_C0_A598_DATA_OP_SCORE6", "desc": "Data operation with PLD start"},
    
    # Upper bank functions (C000+)
    {"addr": "C0:CAA1", "score": 6, "name": "CT_C0_CAA1_SCRIPT_DISPATCH_SCORE6", "desc": "Script dispatch handler with JSR chain"},
    {"addr": "C0:CBA6", "score": 6, "name": "CT_C0_CBA6_EVENT_HANDLER_SCORE6", "desc": "Event handler with PLD prologue"},
    {"addr": "C0:CE34", "score": 6, "name": "CT_C0_CE34_PHK_HANDLER_SCORE6", "desc": "Bank handling with PHK instruction"},
    
    # NMI/IRQ region functions
    {"addr": "C0:EC18", "score": 6, "name": "CT_C0_EC18_NMI_UTIL_SCORE6", "desc": "NMI utility with REP #$20"},
    
    # HDMA cluster (F800 region)
    {"addr": "C0:F860", "score": 6, "name": "CT_C0_F860_HDMA_INIT_SCORE6", "desc": "HDMA initialization with PHY/PHX"},
    {"addr": "C0:F8A2", "score": 6, "name": "CT_C0_F8A2_HDMA_TABLE_SCORE6", "desc": "HDMA table processing"},
    {"addr": "C0:F8B0", "score": 6, "name": "CT_C0_F8B0_HDMA_CHAIN_SCORE6", "desc": "HDMA chain handler with PHB"},
]

def create_label_file(candidate, labels_dir):
    """Create an .asm label file for the candidate."""
    filename = f"{candidate['name']}.asm"
    filepath = os.path.join(labels_dir, filename)
    
    # Extract hex address for EQU
    addr_hex = candidate['addr'].replace('C0:', 'C00')
    
    content = f"; {candidate['desc']}\n"
    content += f"{candidate['name']}: EQU ${addr_hex}\n"
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath

def create_manifest(candidate, manifests_dir, pass_num):
    """Create a manifest JSON for the candidate."""
    # Parse address
    addr = candidate['addr']
    bank, offset = addr.split(':')
    
    manifest = {
        "pass": pass_num,
        "label": candidate['name'],
        "address": addr,
        "snes_address": f"${bank}${offset}",
        "score": candidate['score'],
        "description": candidate['desc'],
        "type": "function",
        "status": "candidate",
        "connected_to": []
    }
    
    filename = f"pass{pass_num:03d}_{candidate['name']}.json"
    filepath = os.path.join(manifests_dir, filename)
    
    with open(filepath, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    return filepath

def main():
    labels_dir = 'labels'
    manifests_dir = 'labels/c0_new_candidates'
    
    # Create manifests directory
    os.makedirs(manifests_dir, exist_ok=True)
    
    # Starting pass number (based on existing C0 labels)
    start_pass = 250
    
    print("Creating labels and manifests for C0 candidates...")
    print("="*60)
    
    created_labels = []
    created_manifests = []
    
    for i, candidate in enumerate(SELECTED_CANDIDATES, start_pass):
        # Create label file
        label_path = create_label_file(candidate, labels_dir)
        created_labels.append(label_path)
        
        # Create manifest
        manifest_path = create_manifest(candidate, manifests_dir, i)
        created_manifests.append(manifest_path)
        
        print(f"  {candidate['addr']}: {candidate['name']} (score {candidate['score']})")
    
    print("="*60)
    print(f"Created {len(created_labels)} labels in {labels_dir}/")
    print(f"Created {len(created_manifests)} manifests in {manifests_dir}/")
    
    # Create summary report
    summary = {
        "bank": "C0",
        "region": "8000-FFFF",
        "candidates_processed": len(SELECTED_CANDIDATES),
        "focus_areas": ["DMA/HDMA", "Graphics Engine", "Input Handling", "NMI/IRQ"],
        "labels": [c['name'] for c in SELECTED_CANDIDATES],
        "estimated_coverage_increase": f"{len(SELECTED_CANDIDATES) * 0.3:.1f}%"
    }
    
    summary_path = 'reports/c0_mapping_summary.json'
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nSummary written to {summary_path}")

if __name__ == '__main__':
    main()
