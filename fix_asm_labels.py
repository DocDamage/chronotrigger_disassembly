#!/usr/bin/env python3
"""Fix ASM labels with correct full addresses"""

import os

# Manifest data
manifests = [
    {'range': 'C2:8C08-C2:8C5B', 'label': 'ct_c2_8c08_prelude_hub', 'score': 14, 'width': 83, 'call_count': 5},
    {'range': 'C2:8C71-C2:8CA2', 'label': 'ct_c2_8c71_handler', 'score': 10, 'width': 49, 'call_count': 1},
    {'range': 'C2:8CDF-C2:8CF7', 'label': 'ct_c2_8cdf_helper', 'score': 9, 'width': 24, 'call_count': 1},
    {'range': 'C2:8D05-C2:8D1C', 'label': 'ct_c2_8d05_service', 'score': 9, 'width': 23, 'call_count': 1},
    {'range': 'C2:8D45-C2:8D63', 'label': 'ct_c2_8d45_dispatch', 'score': 10, 'width': 30, 'call_count': 2},
    {'range': 'C2:8D66-C2:8D8F', 'label': 'ct_c2_8d66_helper', 'score': 12, 'width': 41, 'call_count': 3},
    {'range': 'C2:8DA3-C2:8E1E', 'label': 'ct_c2_8da3_mega_handler', 'score': 14, 'width': 123, 'call_count': 6},
    {'range': 'C2:8E2E-C2:8E82', 'label': 'ct_c2_8e2e_complex', 'score': 13, 'width': 84, 'call_count': 4},
    {'range': 'C2:8E83-C2:8EAB', 'label': 'ct_c2_8e83_service', 'score': 9, 'width': 40, 'call_count': 1},
    {'range': 'C2:8ECE-C2:8F55', 'label': 'ct_c2_8ece_mega_hub', 'score': 13, 'width': 135, 'call_count': 7},
    {'range': 'C2:8F56-C2:8F6C', 'label': 'ct_c2_8f56_helper', 'score': 8, 'width': 22, 'call_count': 2},
    {'range': 'C2:8F6D-C2:8FCB', 'label': 'ct_c2_8f6d_complex_handler', 'score': 14, 'width': 94, 'call_count': 8},
]

labels_dir = 'labels'

for m in manifests:
    start = m['range'].split('-')[0]  # C2:8C08
    end = m['range'].split('-')[1]    # C2:8C5B
    start_addr = start.split(':')[1]  # 8C08
    end_addr = end.split(':')[1]      # 8C5B
    end_minus_1 = f"{int(end_addr, 16) - 1:04X}"
    
    # Create proper ASM content with full addresses
    asm_content = f"; {m['range']} - {m['label']}\n"
    asm_content += f"; Score: {m['score']}\n"
    asm_content += f"; Size: {m['width']} bytes\n"
    asm_content += f"; Session: 31\n"
    asm_content += f";\n"
    asm_content += f"; C2:8C00-9000 hub region expansion\n"
    asm_content += f"; {m['call_count']} internal calls\n"
    asm_content += f";\n"
    asm_content += f"; Characteristics:\n"
    asm_content += f"; - Part of 8000-region service network\n"
    asm_content += f"; - Strong function boundaries\n"
    asm_content += f"; - Hub network connector\n"
    asm_content += f"\n"
    asm_content += f"{m['label']}:\n"
    asm_content += f"    ; Function entry point\n"
    asm_content += f"    .addr ${start_addr}\n"
    asm_content += f"\n"
    asm_content += f"{m['label']}_end:\n"
    asm_content += f"    ; Function boundary end\n"
    asm_content += f"    .addr ${end_minus_1}\n"
    
    # Determine filename from start address
    filename = f"CT_C2_{start_addr}_HUB_S31.asm"
    filepath = os.path.join(labels_dir, filename)
    
    with open(filepath, 'w') as f:
        f.write(asm_content)
    
    print(f"Fixed: {filename}")

print(f"\nAll {len(manifests)} ASM labels fixed.")
