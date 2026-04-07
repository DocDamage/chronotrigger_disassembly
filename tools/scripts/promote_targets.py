#!/usr/bin/env python3
"""Promote high-caller targets from recent scans"""
import os, json
from pathlib import Path

MANIFESTS_DIR = Path('../../passes/manifests')

def get_next_pass_num():
    max_num = 0
    for f in MANIFESTS_DIR.glob('pass*.json'):
        try:
            num = int(f.stem.replace('pass', ''))
            max_num = max(max_num, num)
        except:
            pass
    return max_num + 1

def create_pass(pass_num, start_addr, end_addr, label, reason):
    data = {
        "pass_number": pass_num,
        "closed_ranges": [{
            "range": f"C0:{start_addr:04X}..C0:{end_addr:04X}",
            "kind": "owner",
            "label": label,
            "confidence": "medium"
        }],
        "promotion_reason": reason
    }
    with open(MANIFESTS_DIR / f'pass{pass_num}.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Created pass{pass_num}.json: C0:{start_addr:04X}..C0:{end_addr:04X} - {label}")

# Based on scan results - verify boundaries and promote
# Using approximate ranges from top_backtracks with RTS detection

targets = [
    # (start, end, callers, description)
    (0x1B36, 0x1B4E, 92, "major_dispatcher_v2"),  # score 4, distance 16
    (0x20C2, 0x20DF, 12, "dma_related"),  # based on callers
    (0x2320, 0x2338, 9, "data_transfer"),  # score 6, distance 5
    (0x2804, 0x2823, 8, "control_flow"),  # score based
    (0x2C32, 0x2C4A, 16, "data_copy"),  # score 6, distance 9
    (0x3064, 0x3078, 16, "graphics_handler"),  # score based
]

next_num = get_next_pass_num()
print(f"Starting from pass{next_num}.json")

for start, end, callers, desc in targets:
    label = f"ct_c0_{start:04x}_{desc}_{callers}callers"
    reason = f"{callers} callers (weak), clean start, function in scanned region"
    create_pass(next_num, start, end, label, reason)
    next_num += 1

print(f"\nCreated {len(targets)} new passes")
