#!/usr/bin/env python3
"""Create additional C4 manifests to reach ~1000 bytes coverage"""

import json
import os

MANIFEST_TEMPLATE = {
    "disassembly": {
        "pass": None,
        "bank": "C4",
        "session": 27,
        "target": {
            "address": None,
            "mode": "known_code",
            "label": None,
            "reason": None
        },
        "closure": {
            "verification": "pending",
            "strategy": "score_based",
            "expected_length": None
        }
    }
}

# Additional candidates from 9000-FFFF and score-4 high-call regions
# These complement the 11 already created
ADDITIONAL_CANDIDATES = [
    # From C4:9000-FFFF analysis report - score-6 candidates
    {
        "addr": "C4:9013",
        "end": "C4:902C",
        "width": 26,
        "score": 6,
        "label": "ct_c4_9013_ldy_handler",
        "reason": "Score-6, LDY# prologue. Cross-bank caller at C4:2953."
    },
    {
        "addr": "C4:9D10",
        "end": "C4:9D2A",
        "width": 27,
        "score": 6,
        "label": "ct_c4_9d10_cluster",
        "reason": "Score-6 cluster at 9DE6 region. Strong candidate."
    },
    {
        "addr": "C4:9FEA",
        "end": "C4:9FFF",
        "width": 22,
        "score": 6,
        "label": "ct_c4_9fea_jsr_page",
        "reason": "Score-6, JSR prologue. Page boundary code."
    },
    {
        "addr": "C4:B3B1",
        "end": "C4:B3D4",
        "width": 36,
        "score": 6,
        "label": "ct_c4_b3b1_caller_heavy",
        "reason": "Score-6, strong caller from C4:09C9. High-value target."
    },
    {
        "addr": "C4:C0DF",
        "end": "C4:C0F8",
        "width": 26,
        "score": 6,
        "label": "ct_c4_c0df_cross_bank",
        "reason": "Score-6, PHP prologue. Cross-bank entries from D1:xxxx."
    },
    {
        "addr": "C4:C4DD",
        "end": "C4:C4F7",
        "width": 27,
        "score": 6,
        "label": "ct_c4_c4dd_phk_entry",
        "reason": "Score-6, PHK prologue. Bank push common pattern."
    },
    {
        "addr": "C4:C8C7",
        "end": "C4:C8E0",
        "width": 26,
        "score": 6,
        "label": "ct_c4_c8c7_rep_handler",
        "reason": "Score-6, REP prologue. Mode set function."
    },
    {
        "addr": "C4:E0EC",
        "end": "C4:E108",
        "width": 29,
        "score": 6,
        "label": "ct_c4_e0ec_multiple_callers",
        "reason": "Score-6, LDY# prologue. Multiple callers."
    },
    {
        "addr": "C4:E35E",
        "end": "C4:E37A",
        "width": 29,
        "score": 6,
        "label": "ct_c4_e35e_php_clear",
        "reason": "Score-6, PHP prologue. Clear pattern."
    },
    {
        "addr": "C4:EE00",
        "end": "C4:EE19",
        "width": 26,
        "score": 6,
        "label": "ct_c4_ee00_excellent",
        "reason": "Score-6, PHP prologue. Excellent candidate."
    },
    {
        "addr": "C4:EFD1",
        "end": "C4:EFEA",
        "width": 26,
        "score": 6,
        "label": "ct_c4_efd1_jsl_long",
        "reason": "Score-6, JSL prologue. Long jump cross-bank."
    },
    {
        "addr": "C4:F21C",
        "end": "C4:F236",
        "width": 27,
        "score": 6,
        "label": "ct_c4_f21c_rep_mode",
        "reason": "Score-6, REP prologue. Mode set."
    },
    {
        "addr": "C4:F9FA",
        "end": "C4:FA18",
        "width": 31,
        "score": 6,
        "label": "ct_c4_f9fa_ldx_init",
        "reason": "Score-6, LDX# prologue. Register init."
    },
    {
        "addr": "C4:FDB9",
        "end": "C4:FDD8",
        "width": 32,
        "score": 6,
        "label": "ct_c4_fdb9_high_page",
        "reason": "Score-6, LDX# prologue. High page candidate."
    },
    # Score-5 candidates for volume
    {
        "addr": "C4:6BDA",
        "end": "C4:6BE1",
        "width": 8,
        "score": 6,
        "label": "ct_c4_6bda_score6",
        "reason": "Score-6 cluster in 6000-7000 region."
    },
    {
        "addr": "C4:59FE",
        "end": "C4:5A07",
        "width": 10,
        "score": 5,
        "label": "ct_c4_59fe_call_triple",
        "reason": "Score-5, 3 calls. Call-dense function."
    },
    {
        "addr": "C4:772E",
        "end": "C4:7742",
        "width": 21,
        "score": 5,
        "label": "ct_c4_772e_supercluster_alt",
        "reason": "Score-5 supercluster neighbor. 4 branches."
    },
    {
        "addr": "C4:7DA7",
        "end": "C4:7DB5",
        "width": 15,
        "score": 5,
        "label": "ct_c4_7da7_branch_handler",
        "reason": "Score-5, 2 branches. Handler function."
    },
]

def create_manifest(pass_num, candidate):
    manifest = json.loads(json.dumps(MANIFEST_TEMPLATE))
    manifest["disassembly"]["pass"] = pass_num
    manifest["disassembly"]["target"]["address"] = candidate["addr"]
    manifest["disassembly"]["target"]["label"] = candidate["label"]
    manifest["disassembly"]["target"]["reason"] = candidate["reason"]
    manifest["disassembly"]["closure"]["expected_length"] = candidate["width"]
    return manifest

def main():
    passes_dir = "passes/new_manifests"
    
    # Start from pass 1126
    next_pass = 1126
    
    created = []
    total_bytes = 0
    
    for candidate in ADDITIONAL_CANDIDATES:
        pass_num = next_pass
        manifest = create_manifest(pass_num, candidate)
        
        filename = f"pass{pass_num}_{candidate['label']}.json"
        filepath = os.path.join(passes_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        created.append({
            "pass": pass_num,
            "addr": candidate["addr"],
            "label": candidate["label"],
            "score": candidate["score"],
            "bytes": candidate["width"]
        })
        
        total_bytes += candidate["width"]
        next_pass += 1
        
        print(f"Pass {pass_num}: {candidate['addr']} -> {candidate['label']} (score={candidate['score']}, {candidate['width']} bytes)")
    
    # Load existing summary and combine
    with open('c4_s27_manifests_summary.json') as f:
        summary = json.load(f)
    
    all_manifests = summary['manifests'] + created
    all_bytes = summary['total_bytes'] + total_bytes
    
    final_summary = {
        "session": 27,
        "bank": "C4",
        "manifest_count": len(all_manifests),
        "pass_range": f"{all_manifests[0]['pass']}-{all_manifests[-1]['pass']}",
        "total_bytes": all_bytes,
        "coverage_increase_percent": round((all_bytes / 65536) * 100, 2),
        "new_manifests": len(created),
        "new_bytes": total_bytes,
        "all_manifests": all_manifests
    }
    
    with open('c4_s27_manifests_final.json', 'w') as f:
        json.dump(final_summary, f, indent=2)
    
    print()
    print("=" * 60)
    print("FINAL SESSION 27 SUMMARY")
    print("=" * 60)
    print(f"Original manifests: {summary['manifest_count']}")
    print(f"New manifests: {len(created)}")
    print(f"Total manifests: {len(all_manifests)}")
    print(f"Original bytes: {summary['total_bytes']}")
    print(f"New bytes: {total_bytes}")
    print(f"Total bytes: {all_bytes}")
    print(f"Coverage increase: +{final_summary['coverage_increase_percent']:.2f}%")
    print(f"Pass range: {final_summary['pass_range']}")

if __name__ == '__main__':
    main()
