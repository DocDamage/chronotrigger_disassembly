import json
import os

# Final 4 manifests for Session 28 - documenting remaining score-6+ candidates
manifests = [
    {
        "pass_number": 1006,
        "bank": "C3",
        "start_address": "C3:30B6",
        "end_address": "C3:30BE",
        "label": "ct_c3_30b6_score6_function",
        "kind": "owner",
        "confidence": "high",
        "source": "local_code_island",
        "target": "C3:30B6",
        "prologue_byte": "",
        "prologue_mnemonic": "",
        "score": 6,
        "promotion_reason": "Score-6 function in C3:3000 region. 9 bytes with 1 call, 1 return.",
        "notes": [
            "Compact 9-byte function",
            "Balanced call and return indicate complete function",
            "Low ASCII ratio (0.222) confirms code"
        ]
    },
    {
        "pass_number": 1007,
        "bank": "C3",
        "start_address": "C3:373D",
        "end_address": "C3:374D",
        "label": "ct_c3_373d_score6_function",
        "kind": "owner",
        "confidence": "high",
        "source": "local_code_island",
        "target": "C3:373D",
        "prologue_byte": "",
        "prologue_mnemonic": "",
        "score": 6,
        "promotion_reason": "Score-6 function in C3:3700 region. 17 bytes with 1 call, 1 return. Very low ASCII (0.176).",
        "notes": [
            "Excellent code indicators with very low ASCII ratio",
            "Standalone 17-byte function",
            "Part of C3:3700-4300 high-density region"
        ]
    },
    {
        "pass_number": 1008,
        "bank": "C3",
        "start_address": "C3:3DE2",
        "end_address": "C3:3DF0",
        "label": "ct_c3_3de2_score6_dispatch",
        "kind": "owner",
        "confidence": "high",
        "source": "local_code_island",
        "target": "C3:3DE2",
        "prologue_byte": "",
        "prologue_mnemonic": "",
        "score": 6,
        "promotion_reason": "Score-6 dispatch in C3:3D00 region. 15 bytes with 3 stackish ops, 2 returns.",
        "notes": [
            "Stack-heavy dispatch pattern (3 ops in 15 bytes)",
            "2 returns indicate multiple exit paths",
            "Possible interrupt handler or state preservation"
        ]
    },
    {
        "pass_number": 1009,
        "bank": "C3",
        "start_address": "C3:3E53",
        "end_address": "C3:3E69",
        "label": "ct_c3_3e53_score7_dispatch",
        "kind": "owner",
        "confidence": "high",
        "source": "local_code_island",
        "target": "C3:3E53",
        "prologue_byte": "",
        "prologue_mnemonic": "",
        "score": 7,
        "promotion_reason": "Score-7 HIGH VALUE dispatch in C3:3E00 region. 23 bytes with 2 calls, 3 returns.",
        "notes": [
            "HIGHEST SCORE in final batch (score-7)",
            "23-byte cluster with multiple calls and returns",
            "Child count of 3 suggests nested functions",
            "Strong code indicators with low ASCII ratio"
        ]
    },
]

# Write manifests
output_dir = 'passes/manifests'
for m in manifests:
    filepath = os.path.join(output_dir, f"pass{m['pass_number']}_c3_final.json")
    with open(filepath, 'w') as f:
        json.dump(m, f, indent=2)
    print(f"Created: {filepath}")

# Calculate total coverage
total_bytes = sum(
    int(m['end_address'].split(':')[1], 16) - int(m['start_address'].split(':')[1], 16) + 1
    for m in manifests
)
print(f"\nTotal new coverage: {total_bytes} bytes")
print(f"Manifests created: {len(manifests)}")
