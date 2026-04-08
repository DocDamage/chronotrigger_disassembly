#!/usr/bin/env python3
"""Generate recommended manifests for C1 hub functions"""

import json

manifests = [
    # Region 1: C1:1700-1800 Dispatch Hub
    {
        'pass': 579,
        'range': 'C1:179C..C1:17A0',
        'label': 'ct_c1_179c_dispatch_hub',
        'callers': 25,
        'bytes': 5,
        'confidence': 'high',
        'reason': 'Primary dispatch hub. Score-6 cluster with 25 callers via JMP. STZ/STZ/RTS pattern.'
    },
    {
        'pass': 580,
        'range': 'C1:178E..C1:17A0',
        'label': 'ct_c1_178e_dispatch_prologue',
        'callers': 0,
        'bytes': 19,
        'confidence': 'high',
        'reason': 'LDA# prologue leading to dispatch hub. Score-6 clean start.'
    },
    {
        'pass': 581,
        'range': 'C1:17A5..C1:17BE',
        'label': 'ct_c1_17a5_dispatch_handler_dec',
        'callers': 0,
        'bytes': 26,
        'confidence': 'medium',
        'reason': 'Score-6 candidate. Handler for decrement operation. PHD/BEQ pattern.'
    },
    {
        'pass': 582,
        'range': 'C1:17BC..C1:17DC',
        'label': 'ct_c1_17bc_dispatch_handler_inc',
        'callers': 0,
        'bytes': 33,
        'confidence': 'medium',
        'reason': 'Score-6 candidate. Handler for increment operation. JSR/RTS pattern.'
    },
    
    # Region 2: C1:1B00-1C00 Utility Hub  
    {
        'pass': 583,
        'range': 'C1:1B55..C1:1B66',
        'label': 'ct_c1_1b55_utility_hub',
        'callers': 29,
        'bytes': 18,
        'confidence': 'high',
        'reason': 'Primary utility hub. Score-6 cluster with 29 callers via JSR. JSL to C7:0004.'
    },
    {
        'pass': 584,
        'range': 'C1:1B06..C1:1B18',
        'label': 'ct_c1_1b06_utility_prologue',
        'callers': 0,
        'bytes': 19,
        'confidence': 'high',
        'reason': 'LDA# F0 prologue. Score-6 clean start. Initialization for utility hub.'
    },
    {
        'pass': 585,
        'range': 'C1:1B9B..C1:1BAB',
        'label': 'ct_c1_1b9b_utility_handler',
        'callers': 0,
        'bytes': 17,
        'confidence': 'medium',
        'reason': 'Score-6 candidate. PHX/STZ pattern. Secondary utility handler.'
    },
    
    # Region 3: C1:4A00-4B00 Library Hub
    {
        'pass': 586,
        'range': 'C1:4AEB..C1:4B17',
        'label': 'ct_c1_4aeb_library_hub',
        'callers': 27,
        'bytes': 45,
        'confidence': 'high',
        'reason': 'Primary library hub. Score-6 cluster with 27 callers. Array/table processing.'
    },
    {
        'pass': 587,
        'range': 'C1:4A6B..C1:4A70',
        'label': 'ct_c1_4a6b_library_init',
        'callers': 0,
        'bytes': 6,
        'confidence': 'medium',
        'reason': 'Library init stub. LDA# 01 / STA $9930 / RTS. Clean entry point.'
    },
    {
        'pass': 588,
        'range': 'C1:4A71..C1:4AA7',
        'label': 'ct_c1_4a71_library_calc_xy',
        'callers': 0,
        'bytes': 55,
        'confidence': 'medium',
        'reason': 'Score-6 candidate. TDC/TAX/TAY. X/Y coordinate calculation.'
    },
]

if __name__ == '__main__':
    print('=' * 80)
    print('RECOMMENDED MANIFESTS FOR PROMOTION (Passes 579-588)')
    print('=' * 80)

    total_bytes = 0
    for m in manifests:
        print(f'''
Pass {m['pass']}:
{{
  "pass_number": {m['pass']},
  "closed_ranges": [
    {{
      "range": "{m['range']}",
      "kind": "owner",
      "label": "{m['label']}",
      "confidence": "{m['confidence']}"
    }}
  ],
  "promotion_reason": "{m['reason']} {m['bytes']} bytes."
}}''')
        total_bytes += m['bytes']

    print(f'\n{"=" * 80}')
    print(f'SUMMARY: {len(manifests)} functions, {total_bytes} bytes')
    print(f'{"=" * 80}')
