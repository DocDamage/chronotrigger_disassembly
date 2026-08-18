#!/usr/bin/env python3
"""Create Session 30 manifests for C2:8000-9000 deep dive"""

import json
import os

# Selected 12 best candidates for Session 30
# Prioritizing: score 9 first, then call-rich, distributed across regions
manifests = [
    # Score 9 candidates (highest priority)
    {
        "pass": 1200,
        "address": 0x028CAB,  # C2:8CAB
        "bank": 2,
        "label": "ct_c2_8cab_handler_s30",
        "range": "C2:8CAB-C2:8D11",
        "score": 9,
        "width": 102,
        "call_count": 7,
        "branch_count": 5,
        "stackish_count": 2,
        "return_count": 1,
        "session": 30,
        "rationale": "Score-9 function in 8C00-9000 region. 102 bytes, 7 internal calls. High-value handler."
    },
    {
        "pass": 1201,
        "address": 0x028D87,  # C2:8D87
        "bank": 2,
        "label": "ct_c2_8d87_service_s30",
        "range": "C2:8D87-C2:8DDA",
        "score": 9,
        "width": 83,
        "call_count": 4,
        "branch_count": 3,
        "stackish_count": 2,
        "return_count": 1,
        "session": 30,
        "rationale": "Score-9 service function. 83 bytes, 4 calls. Strong boundaries."
    },
    {
        "pass": 1202,
        "address": 0x028EBE,  # C2:8EBE
        "bank": 2,
        "label": "ct_c2_8ebe_handler_s30",
        "range": "C2:8EBE-C2:8F30",
        "score": 9,
        "width": 114,
        "call_count": 7,
        "branch_count": 4,
        "stackish_count": 3,
        "return_count": 1,
        "session": 30,
        "rationale": "Score-9 handler in 8E00-9000 region. 114 bytes, 7 calls."
    },
    {
        "pass": 1203,
        "address": 0x028F30,  # C2:8F30
        "bank": 2,
        "label": "ct_c2_8f30_routine_s30",
        "range": "C2:8F30-C2:8F8E",
        "score": 9,
        "width": 94,
        "call_count": 6,
        "branch_count": 4,
        "stackish_count": 2,
        "return_count": 1,
        "session": 30,
        "rationale": "Score-9 routine. 94 bytes, 6 calls. Part of 8F00 hub network."
    },
    {
        "pass": 1204,
        "address": 0x028F8E,  # C2:8F8E
        "bank": 2,
        "label": "ct_c2_8f8e_service_s30",
        "range": "C2:8F8E-C2:8FF9",
        "score": 9,
        "width": 107,
        "call_count": 5,
        "branch_count": 4,
        "stackish_count": 2,
        "return_count": 1,
        "session": 30,
        "rationale": "Score-9 service. 107 bytes, 5 calls. Near bank boundary."
    },
    # Score 7 candidates with high call counts
    {
        "pass": 1205,
        "address": 0x0281A2,  # C2:81A2
        "bank": 2,
        "label": "ct_c2_81a2_interrupt_s30",
        "range": "C2:81A2-C2:81EF",
        "score": 7,
        "width": 77,
        "call_count": 9,
        "branch_count": 6,
        "stackish_count": 2,
        "return_count": 1,
        "session": 30,
        "rationale": "Score-7 interrupt handler. 77 bytes, 9 calls, RTI return. 8100 region."
    },
    {
        "pass": 1206,
        "address": 0x0286F0,  # C2:86F0
        "bank": 2,
        "label": "ct_c2_86f0_handler_s30",
        "range": "C2:86F0-C2:875B",
        "score": 7,
        "width": 107,
        "call_count": 9,
        "branch_count": 5,
        "stackish_count": 3,
        "return_count": 1,
        "session": 30,
        "rationale": "Score-7 handler. 107 bytes, 9 calls. Rich subroutine."
    },
    {
        "pass": 1207,
        "address": 0x028910,  # C2:8910
        "bank": 2,
        "label": "ct_c2_8910_mega_handler_s30",
        "range": "C2:8910-C2:89B9",
        "score": 7,
        "width": 169,
        "call_count": 12,
        "branch_count": 8,
        "stackish_count": 4,
        "return_count": 1,
        "session": 30,
        "rationale": "Score-7 mega-handler. 169 bytes, 12 calls! Largest in session. 8900 region."
    },
    {
        "pass": 1208,
        "address": 0x028B36,  # C2:8B36
        "bank": 2,
        "label": "ct_c2_8b36_complex_s30",
        "range": "C2:8B36-C2:8CA7",
        "score": 7,
        "width": 369,
        "call_count": 15,
        "branch_count": 12,
        "stackish_count": 5,
        "return_count": 1,
        "session": 30,
        "rationale": "Score-7 complex function. 369 bytes, 15 calls! Massive handler. 8B00 region."
    },
    # Remaining score 7 candidates for coverage
    {
        "pass": 1209,
        "address": 0x028775,  # C2:8775
        "bank": 2,
        "label": "ct_c2_8775_service_s30",
        "range": "C2:8775-C2:87B9",
        "score": 7,
        "width": 68,
        "call_count": 4,
        "branch_count": 3,
        "stackish_count": 2,
        "return_count": 1,
        "session": 30,
        "rationale": "Score-7 service function. 68 bytes, 4 calls. 8700 region coverage."
    },
    {
        "pass": 1210,
        "address": 0x0287B9,  # C2:87B9
        "bank": 2,
        "label": "ct_c2_87b9_helper_s30",
        "range": "C2:87B9-C2:8805",
        "score": 7,
        "width": 76,
        "call_count": 4,
        "branch_count": 3,
        "stackish_count": 2,
        "return_count": 1,
        "session": 30,
        "rationale": "Score-7 helper function. 76 bytes, 4 calls. 87B0-8800 region."
    },
    {
        "pass": 1211,
        "address": 0x028805,  # C2:8805
        "bank": 2,
        "label": "ct_c2_8805_routine_s30",
        "range": "C2:8805-C2:8851",
        "score": 7,
        "width": 76,
        "call_count": 4,
        "branch_count": 3,
        "stackish_count": 2,
        "return_count": 1,
        "session": 30,
        "rationale": "Score-7 routine. 76 bytes, 4 calls. 8800-8900 transition region."
    },
]

# Create manifest YAML files
manifests_dir = "passes/manifests"
os.makedirs(manifests_dir, exist_ok=True)

for m in manifests:
    filename = f"{manifests_dir}/pass_{m['pass']}_c2_{m['address'] & 0xFFFF:04x}.yaml"
    with open(filename, 'w') as f:
        f.write(f"pass: {m['pass']}\n")
        f.write(f"address: {m['address']:06X}\n")
        f.write(f"bank: {m['bank']}\n")
        f.write(f"label: {m['label']}\n")
        f.write(f"range: {m['range']}\n")
        f.write(f"score: {m['score']}\n")
        f.write(f"width: {m['width']}\n")
        f.write(f"call_count: {m['call_count']}\n")
        f.write(f"branch_count: {m['branch_count']}\n")
        f.write(f"stackish_count: {m['stackish_count']}\n")
        f.write(f"return_count: {m['return_count']}\n")
        f.write(f"session: {m['session']}\n")
        f.write(f"rationale: {m['rationale']}\n")
    print(f"Created: {filename}")

# Create ASM label files
labels_dir = "labels"
for m in manifests:
    addr = m['address'] & 0xFFFF
    filename = f"{labels_dir}/CT_C2_{addr:04X}_HUB_S30.asm"
    with open(filename, 'w') as f:
        f.write(f"; {m['range']} - {m['label']}\n")
        f.write(f"; Score: {m['score']}\n")
        f.write(f"; Size: {m['width']} bytes\n")
        f.write(f"; Session: 30\n")
        f.write(f";\n")
        f.write(f"; C2:8000-9000 hub region expansion\n")
        f.write(f"; {m['call_count']} internal calls\n")
        f.write(f";\n")
        f.write(f"; Characteristics:\n")
        f.write(f"; - Part of 8000-region service network\n")
        f.write(f"; - Strong function boundaries\n")
        f.write(f"; - Call-rich handler\n")
        f.write(f"\n")
        f.write(f"{m['label']}:\n")
        f.write(f"    ; Function entry point\n")
        f.write(f"    .addr ${addr:04X}\n")
        f.write(f"\n")
        f.write(f"{m['label']}_end:\n")
        f.write(f"    ; Function boundary end\n")
        end_addr = (m['address'] & 0xFFFF) + m['width'] - 1
        f.write(f"    .addr ${end_addr:04X}\n")
    print(f"Created: {filename}")

print(f"\nTotal manifests created: {len(manifests)}")

# Calculate coverage stats
total_bytes = sum(m['width'] for m in manifests)
print(f"Total new coverage: {total_bytes} bytes")
print(f"Average score: {sum(m['score'] for m in manifests) / len(manifests):.1f}")
print(f"Total calls documented: {sum(m['call_count'] for m in manifests)}")

# Save summary
with open('C2_SESSION_30_MANIFESTS.json', 'w') as f:
    json.dump({
        'session': 30,
        'region': 'C2:8000-9000',
        'manifests': manifests,
        'total_bytes': total_bytes,
        'manifest_count': len(manifests),
        'score_9_count': sum(1 for m in manifests if m['score'] == 9),
        'score_7_count': sum(1 for m in manifests if m['score'] == 7),
    }, f, indent=2)
print("\nSummary saved to C2_SESSION_30_MANIFESTS.json")
