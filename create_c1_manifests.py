#!/usr/bin/env python3
"""Create the C1 hub function manifests"""

import json
import os

manifests = [
    {'pass': 579, 'range': 'C1:179C..C1:17A0', 'label': 'ct_c1_179c_dispatch_hub', 'conf': 'high', 'reason': 'Primary dispatch hub. Score-6 cluster with 25 callers via JMP. STZ/STZ/RTS pattern. 5 bytes.'},
    {'pass': 580, 'range': 'C1:178E..C1:17A0', 'label': 'ct_c1_178e_dispatch_prologue', 'conf': 'high', 'reason': 'LDA# prologue leading to dispatch hub. Score-6 clean start. 19 bytes.'},
    {'pass': 581, 'range': 'C1:17A5..C1:17BE', 'label': 'ct_c1_17a5_dispatch_handler_dec', 'conf': 'medium', 'reason': 'Score-6 candidate. Handler for decrement operation. 26 bytes.'},
    {'pass': 582, 'range': 'C1:17BC..C1:17DC', 'label': 'ct_c1_17bc_dispatch_handler_inc', 'conf': 'medium', 'reason': 'Score-6 candidate. Handler for increment operation. 33 bytes.'},
    {'pass': 583, 'range': 'C1:1B55..C1:1B66', 'label': 'ct_c1_1b55_utility_hub', 'conf': 'high', 'reason': 'Primary utility hub. Score-6 cluster with 29 callers via JSR. JSL to C7:0004. 18 bytes.'},
    {'pass': 584, 'range': 'C1:1B06..C1:1B18', 'label': 'ct_c1_1b06_utility_prologue', 'conf': 'high', 'reason': 'LDA# F0 prologue. Score-6 clean start. 19 bytes.'},
    {'pass': 585, 'range': 'C1:1B9B..C1:1BAB', 'label': 'ct_c1_1b9b_utility_handler', 'conf': 'medium', 'reason': 'Score-6 candidate. Secondary utility handler. 17 bytes.'},
    {'pass': 586, 'range': 'C1:4AEB..C1:4B17', 'label': 'ct_c1_4aeb_library_hub', 'conf': 'high', 'reason': 'Primary library hub. Score-6 cluster with 27 callers. Array/table processing. 45 bytes.'},
    {'pass': 587, 'range': 'C1:4A6B..C1:4A70', 'label': 'ct_c1_4a6b_library_init', 'conf': 'medium', 'reason': 'Library init stub. LDA# 01 / STA / RTS. 6 bytes.'},
    {'pass': 588, 'range': 'C1:4A71..C1:4AA7', 'label': 'ct_c1_4a71_library_calc_xy', 'conf': 'medium', 'reason': 'Score-6 candidate. X/Y coordinate calculation. 55 bytes.'},
]

output_dir = 'passes/manifests'
os.makedirs(output_dir, exist_ok=True)

for m in manifests:
    data = {
        'pass_number': m['pass'],
        'closed_ranges': [{
            'range': m['range'],
            'kind': 'owner',
            'label': m['label'],
            'confidence': m['conf']
        }],
        'promotion_reason': m['reason']
    }
    filename = os.path.join(output_dir, f"pass{m['pass']}.json")
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Created {filename}: {m['range']} - {m['label']}")

print(f"\nTotal: {len(manifests)} manifests created in {output_dir}/")
