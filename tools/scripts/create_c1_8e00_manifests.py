#!/usr/bin/env python3
"""
Create manifest JSON files for C1:8E00-9800 analysis results.
"""

import json
import os

def main():
    # Priority 1: Score-6+ Functions
    manifests_p1 = [
        {
            'pass_number': 621,
            'label': 'CT_C1_8E9B_HANDLER_DISPATCH',
            'addr': 'C1:8E9B',
            'score': 6,
            'type': 'function',
            'note': 'Handler function dispatching to C1:8C3E hub',
            'calls_to': ['C1:8C3E'],
            'width': 0x24
        },
        {
            'pass_number': 622,
            'label': 'CT_C1_8F02_HANDLER_DISPATCH',
            'addr': 'C1:8F02',
            'score': 6,
            'type': 'function',
            'note': 'Handler function dispatching to C1:8C3E hub',
            'calls_to': ['C1:8C3E'],
            'width': 0x27
        },
        {
            'pass_number': 623,
            'label': 'CT_C1_8FF4_HANDLER_DISPATCH',
            'addr': 'C1:8FF4',
            'score': 6,
            'type': 'function',
            'note': 'Handler function dispatching to C1:8C3E hub',
            'calls_to': ['C1:8C3E'],
            'width': 0x28
        }
    ]

    # Priority 2: Score-4 Candidates
    manifests_p2 = [
        {'pass_number': 624, 'label': 'CT_C1_8E41_HANDLER', 'addr': 'C1:8E41', 'score': 4, 'type': 'function'},
        {'pass_number': 625, 'label': 'CT_C1_8E6C_HANDLER', 'addr': 'C1:8E6C', 'score': 4, 'type': 'function'},
        {'pass_number': 626, 'label': 'CT_C1_8E77_HANDLER', 'addr': 'C1:8E77', 'score': 4, 'type': 'function'},
        {'pass_number': 627, 'label': 'CT_C1_9151_HANDLER', 'addr': 'C1:9151', 'score': 4, 'type': 'function'},
        {'pass_number': 628, 'label': 'CT_C1_93A4_HANDLER', 'addr': 'C1:93A4', 'score': 4, 'type': 'function'},
    ]

    # Priority 3: High-Score Clusters
    manifests_p3 = [
        {'pass_number': 630, 'label': 'CT_C1_8E95_CLUSTER', 'addr': 'C1:8E95', 'score': 8, 'type': 'cluster', 'range': 'C1:8E95..C1:8EAA'},
        {'pass_number': 631, 'label': 'CT_C1_9792_CLUSTER', 'addr': 'C1:9792', 'score': 8, 'type': 'cluster', 'range': 'C1:9792..C1:97D4'},
        {'pass_number': 632, 'label': 'CT_C1_9032_CLUSTER', 'addr': 'C1:9032', 'score': 7, 'type': 'cluster', 'range': 'C1:9032..C1:9044'},
        {'pass_number': 633, 'label': 'CT_C1_906E_CLUSTER', 'addr': 'C1:906E', 'score': 7, 'type': 'cluster', 'range': 'C1:906E..C1:9081'},
        {'pass_number': 634, 'label': 'CT_C1_9745_CLUSTER', 'addr': 'C1:9745', 'score': 7, 'type': 'cluster', 'range': 'C1:9745..C1:9764'},
        {'pass_number': 635, 'label': 'CT_C1_96C2_CLUSTER', 'addr': 'C1:96C2', 'score': 7, 'type': 'cluster', 'range': 'C1:96C2..C1:96D3'},
    ]

    all_manifests = manifests_p1 + manifests_p2 + manifests_p3

    # Save manifests
    os.makedirs('passes/new_manifests', exist_ok=True)
    for m in all_manifests:
        fname = f"passes/new_manifests/pass{m['pass_number']}_c1_8e00_analysis.json"
        with open(fname, 'w') as f:
            json.dump(m, f, indent=2)
        print(f"Created: {fname}")

    print()
    print(f"Total manifests created: {len(all_manifests)}")
    print("Priority 1 (Score 6+): 3 manifests")
    print("Priority 2 (Score 4): 5 manifests")
    print("Priority 3 (Clusters): 6 manifests")

if __name__ == '__main__':
    main()
