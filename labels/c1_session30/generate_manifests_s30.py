#!/usr/bin/env python3
"""Generate manifests for C1 Session 30 - Final Candidate Processing"""

import json
import os

# Session 30 manifest data
# Targeting the remaining ~21 candidates to complete the ~113 candidate pool

manifests = [
    # ==================== PRIORITY 1: Remaining Score-7 Candidates ====================
    {
        "pass_number": 1100,
        "closed_ranges": [
            {
                "range": "C1:7435..C1:744C",
                "kind": "owner",
                "label": "ct_c1_7435_score7_subroutine",
                "confidence": "high"
            }
        ],
        "promotion_reason": "Score-7 candidate. 23 bytes width. Subroutine with call and return patterns. Located in C1:7000-8000 region.",
        "metadata": {
            "session": 30,
            "score": 7,
            "source": "C1_initial_scan_summary.json",
            "region": "C1:7000-8000"
        }
    },
    {
        "pass_number": 1101,
        "closed_ranges": [
            {
                "range": "C1:798A..C1:79A1",
                "kind": "owner",
                "label": "ct_c1_798a_score7_subroutine",
                "confidence": "high"
            }
        ],
        "promotion_reason": "Score-7 candidate. 23 bytes width. Subroutine with strong prologue pattern. Located in C1:7900-7A00 region.",
        "metadata": {
            "session": 30,
            "score": 7,
            "source": "C1_initial_scan_summary.json",
            "region": "C1:7900-7A00"
        }
    },
    {
        "pass_number": 1102,
        "closed_ranges": [
            {
                "range": "C1:4ED8..C1:4EF0",
                "kind": "owner",
                "label": "ct_c1_4ed8_score7_subroutine_s30",
                "confidence": "high"
            }
        ],
        "promotion_reason": "Score-7 candidate update. 25 bytes width. Post-ecosystem region function with call, 4 branches, stack operation. Validated across sessions 24, 28.",
        "metadata": {
            "session": 30,
            "score": 7,
            "previous_sessions": [24, 28],
            "source": "C1_initial_scan_summary.json"
        }
    },
    {
        "pass_number": 1103,
        "closed_ranges": [
            {
                "range": "C1:5FBA..C1:5FD2",
                "kind": "owner",
                "label": "ct_c1_5fba_score7_subroutine_s30",
                "confidence": "high"
            }
        ],
        "promotion_reason": "Score-7 candidate update. 25 bytes width. Multiple callers (2) suggest shared utility function. Validated across sessions 24, 28.",
        "metadata": {
            "session": 30,
            "score": 7,
            "call_count": 2,
            "previous_sessions": [24, 28],
            "source": "C1_initial_scan_summary.json"
        }
    },
    {
        "pass_number": 1104,
        "closed_ranges": [
            {
                "range": "C1:CDEE..C1:CDFF",
                "kind": "owner",
                "label": "ct_c1_cdee_score7_handler_s30",
                "confidence": "high"
            }
        ],
        "promotion_reason": "Score-7 candidate update. 17 bytes width. Handler function in C1:C000-CFFF region. Validated in session 25.",
        "metadata": {
            "session": 30,
            "score": 7,
            "width": 17,
            "previous_sessions": [25],
            "source": "C1_initial_scan_summary.json"
        }
    },
    
    # ==================== PRIORITY 2: Hub Functions ====================
    {
        "pass_number": 1105,
        "closed_ranges": [
            {
                "range": "C1:178E..C1:17A0",
                "kind": "owner",
                "label": "ct_c1_178e_dispatch_hub",
                "confidence": "high"
            }
        ],
        "promotion_reason": "Hub function candidate. 25 callers via JMP dispatch. Score-6 cluster with LDA# prologue. Primary dispatch hub for C1:1700-1800 region.",
        "metadata": {
            "session": 30,
            "score": 6,
            "callers": 25,
            "hub_type": "dispatch",
            "source": "c1_hub_manifests.py"
        }
    },
    {
        "pass_number": 1106,
        "closed_ranges": [
            {
                "range": "C1:1B55..C1:1B66",
                "kind": "owner",
                "label": "ct_c1_1b55_utility_hub",
                "confidence": "high"
            }
        ],
        "promotion_reason": "Hub function candidate. 29 callers via JSR. Score-6 cluster. Primary utility hub with JSL to C7:0004. C1:1B00-1C00 region anchor.",
        "metadata": {
            "session": 30,
            "score": 6,
            "callers": 29,
            "hub_type": "utility",
            "source": "c1_hub_manifests.py"
        }
    },
    {
        "pass_number": 1107,
        "closed_ranges": [
            {
                "range": "C1:4AEB..C1:4B17",
                "kind": "owner",
                "label": "ct_c1_4aeb_library_hub",
                "confidence": "high"
            }
        ],
        "promotion_reason": "Hub function candidate. 27 callers. Score-6 cluster with array/table processing. Primary library hub for C1:4A00-4B00 region.",
        "metadata": {
            "session": 30,
            "score": 6,
            "callers": 27,
            "hub_type": "library",
            "source": "c1_hub_manifests.py"
        }
    },
    
    # ==================== PRIORITY 3: Best Score-6 Candidates ====================
    {
        "pass_number": 1108,
        "closed_ranges": [
            {
                "range": "C1:17A5..C1:17BE",
                "kind": "owner",
                "label": "ct_c1_17a5_dispatch_handler",
                "confidence": "medium"
            }
        ],
        "promotion_reason": "Score-6 candidate. Dispatch handler for decrement operation. PHD/BEQ pattern. Associated with C1:178E hub.",
        "metadata": {
            "session": 30,
            "score": 6,
            "associated_hub": "C1:178E",
            "source": "c1_hub_manifests.py"
        }
    },
    {
        "pass_number": 1109,
        "closed_ranges": [
            {
                "range": "C1:1B06..C1:1B18",
                "kind": "owner",
                "label": "ct_c1_1b06_utility_prologue",
                "confidence": "high"
            }
        ],
        "promotion_reason": "Score-6 candidate. LDA# F0 prologue. Clean entry point for utility hub. Initialization function.",
        "metadata": {
            "session": 30,
            "score": 6,
            "associated_hub": "C1:1B55",
            "source": "c1_hub_manifests.py"
        }
    },
    {
        "pass_number": 1110,
        "closed_ranges": [
            {
                "range": "C1:4A6B..C1:4A70",
                "kind": "owner",
                "label": "ct_c1_4a6b_library_init",
                "confidence": "medium"
            }
        ],
        "promotion_reason": "Score-6 candidate. Library init stub. LDA# 01 / STA $9930 / RTS pattern. Clean entry point for C1:4AEB library hub.",
        "metadata": {
            "session": 30,
            "score": 6,
            "associated_hub": "C1:4AEB",
            "source": "c1_hub_manifests.py"
        }
    },
    {
        "pass_number": 1111,
        "closed_ranges": [
            {
                "range": "C1:4A71..C1:4AA7",
                "kind": "owner",
                "label": "ct_c1_4a71_library_calc_xy",
                "confidence": "medium"
            }
        ],
        "promotion_reason": "Score-6 candidate. X/Y coordinate calculation function. TDC/TAX/TAY pattern. Associated with library hub.",
        "metadata": {
            "session": 30,
            "score": 6,
            "associated_hub": "C1:4AEB",
            "source": "c1_hub_manifests.py"
        }
    },
]

def generate_manifests():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 80)
    print("C1 SESSION 30 MANIFEST GENERATION")
    print("=" * 80)
    print(f"\nGenerating {len(manifests)} manifest files...\n")
    
    for m in manifests:
        pass_num = m["pass_number"]
        range_str = m["closed_ranges"][0]["range"].replace(":", "_").replace("..", "_")
        label = m["closed_ranges"][0]["label"]
        
        filename = f"C1_{range_str}_s30.yaml"
        filepath = os.path.join(output_dir, filename)
        
        # Create YAML content
        yaml_content = f"""# Session 30 Manifest - Pass {pass_num}
# Generated for C1 Bank Candidate Completion

manifest_version: "1.0"
session: 30
pass_number: {pass_num}

target:
  bank: "C1"
  range: "{m['closed_ranges'][0]['range']}"
  label: "{label}"
  confidence: "{m['closed_ranges'][0]['confidence']}"
  kind: "{m['closed_ranges'][0]['kind']}"

metadata:
  score: {m['metadata'].get('score', 'N/A')}
  source: "{m['metadata'].get('source', 'unknown')}"
  promotion_reason: "{m['promotion_reason'][:80]}..."
"""
        
        # Add optional metadata fields
        if 'callers' in m['metadata']:
            yaml_content += f"  callers: {m['metadata']['callers']}\n"
        if 'call_count' in m['metadata']:
            yaml_content += f"  call_count: {m['metadata']['call_count']}\n"
        if 'hub_type' in m['metadata']:
            yaml_content += f"  hub_type: {m['metadata']['hub_type']}\n"
        if 'previous_sessions' in m['metadata']:
            yaml_content += f"  previous_sessions: {m['metadata']['previous_sessions']}\n"
        if 'associated_hub' in m['metadata']:
            yaml_content += f"  associated_hub: \"{m['metadata']['associated_hub']}\"\n"
        
        yaml_content += f"""
promotion_reason: |
  {m['promotion_reason']}

disassembly:
  mode: "code"
  merge_policy: "session_priority"
"""
        
        with open(filepath, 'w') as f:
            f.write(yaml_content)
        
        print(f"  Pass {pass_num}: {filename}")
        print(f"    Label: {label}")
        print(f"    Range: {m['closed_ranges'][0]['range']}")
    
    print("\n" + "=" * 80)
    print(f"SUMMARY: {len(manifests)} manifests created in {output_dir}")
    print("=" * 80)
    
    # Also create a JSON summary
    summary = {
        "session": 30,
        "manifest_count": len(manifests),
        "manifests": [
            {
                "pass": m["pass_number"],
                "range": m["closed_ranges"][0]["range"],
                "label": m["closed_ranges"][0]["label"],
                "score": m["metadata"].get("score")
            }
            for m in manifests
        ]
    }
    
    summary_path = os.path.join(output_dir, "session30_manifest_summary.json")
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary written to: {summary_path}")

if __name__ == "__main__":
    generate_manifests()
