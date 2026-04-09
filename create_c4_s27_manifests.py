#!/usr/bin/env python3
"""Create manifests for Bank C4 Session 27 to push coverage toward 8%"""

import json
import os

# Manifest template
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

# Top candidates for Session 27 (10-12 manifests)
# Selected based on: score, calls, branches, and coverage potential
CANDIDATES = [
    {
        "addr": "C4:7730",
        "end": "C4:7748", 
        "score": 7,
        "calls": 1,
        "branches": 6,
        "width": 25,
        "label": "ct_c4_7730_supercluster",
        "reason": "Score-7 supercluster, 6 branches, 1 call. High-density code region."
    },
    {
        "addr": "C4:5025",
        "end": "C4:5039",
        "score": 7,
        "calls": 2,
        "branches": 2,
        "width": 21,
        "label": "ct_c4_5025_call_heavy",
        "reason": "Score-7 island, 2 calls, 2 branches. Call-heavy function."
    },
    {
        "addr": "C4:46B7",
        "end": "C4:46CF",
        "score": 6,
        "calls": 1,
        "branches": 3,
        "width": 25,
        "label": "ct_c4_46b7_branch_handler",
        "reason": "Score-6 cluster, 3 branches. Branch-heavy handler in 4000-5000 region."
    },
    {
        "addr": "C4:1701",
        "end": "C4:1708",
        "score": 6,
        "calls": 1,
        "branches": 2,
        "width": 8,
        "label": "ct_c4_1701_dual_branch",
        "reason": "Score-6 cluster, 2 branches. Early bank function."
    },
    {
        "addr": "C4:9E50",
        "end": "C4:9E56",
        "score": 6,
        "calls": 1,
        "branches": 2,
        "width": 7,
        "label": "ct_c4_9e50_handler",
        "reason": "Score-6 cluster in 8000-C000 region, 2 branches."
    },
    {
        "addr": "C4:607A",
        "end": "C4:6085",
        "score": 6,
        "calls": 1,
        "branches": 1,
        "width": 12,
        "label": "ct_c4_607a_subroutine",
        "reason": "Score-6 cluster in 6000-7000 region."
    },
    {
        "addr": "C4:9DE6",
        "end": "C4:9DF6",
        "score": 6,
        "calls": 1,
        "branches": 1,
        "width": 17,
        "label": "ct_c4_9de6_handler",
        "reason": "Score-6 cluster in 8000-C000 region."
    },
    {
        "addr": "C4:C771",
        "end": "C4:C77C",
        "score": 6,
        "calls": 1,
        "branches": 1,
        "width": 12,
        "label": "ct_c4_c771_c000_handler",
        "reason": "Score-6 cluster in C000-FFFF region. Cross-bank candidate."
    },
    {
        "addr": "C4:7980",
        "end": "C4:7992",
        "score": 5,
        "calls": 3,
        "branches": 4,
        "width": 19,
        "label": "ct_c4_7980_call_dense",
        "reason": "Score-5, 3 calls, 4 branches. Call-dense function."
    },
    {
        "addr": "C4:752A",
        "end": "C4:753C",
        "score": 5,
        "calls": 3,
        "branches": 1,
        "width": 19,
        "label": "ct_c4_752a_call_triple",
        "reason": "Score-5, 3 calls. Call-heavy in 7000-8000 region."
    },
    {
        "addr": "C4:7F8F",
        "end": "C4:7FA7",
        "score": 5,
        "calls": 0,
        "branches": 6,
        "width": 25,
        "label": "ct_c4_7f8f_branch_heavy",
        "reason": "Score-5, 6 branches. Branch-heavy handler."
    },
]

def create_manifest(pass_num, candidate):
    """Create a manifest for a candidate"""
    manifest = json.loads(json.dumps(MANIFEST_TEMPLATE))
    manifest["disassembly"]["pass"] = pass_num
    manifest["disassembly"]["target"]["address"] = candidate["addr"]
    manifest["disassembly"]["target"]["label"] = candidate["label"]
    manifest["disassembly"]["target"]["reason"] = candidate["reason"]
    manifest["disassembly"]["closure"]["expected_length"] = candidate["width"]
    return manifest

def main():
    # Find next pass number
    passes_dir = "passes/new_manifests"
    existing_passes = []
    if os.path.exists(passes_dir):
        for f in os.listdir(passes_dir):
            if f.startswith("pass") and f.endswith(".json"):
                try:
                    # Extract number from pass123_name.json
                    num = int(f[4:].split("_")[0])
                    existing_passes.append(num)
                except:
                    pass
    
    next_pass = max(existing_passes) + 1 if existing_passes else 953
    print(f"Starting at pass {next_pass}")
    print()
    
    created_manifests = []
    total_bytes = 0
    
    for i, candidate in enumerate(CANDIDATES):
        pass_num = next_pass + i
        manifest = create_manifest(pass_num, candidate)
        
        filename = f"pass{pass_num}_{candidate['label']}.json"
        filepath = os.path.join(passes_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        created_manifests.append({
            "pass": pass_num,
            "file": filename,
            "addr": candidate["addr"],
            "label": candidate["label"],
            "score": candidate["score"],
            "bytes": candidate["width"]
        })
        
        total_bytes += candidate["width"]
        print(f"Pass {pass_num}: {candidate['addr']} -> {candidate['label']} (score={candidate['score']}, {candidate['width']} bytes)")
    
    # Save summary
    summary = {
        "session": 27,
        "bank": "C4",
        "manifest_count": len(CANDIDATES),
        "pass_range": f"{next_pass}-{next_pass + len(CANDIDATES) - 1}",
        "total_bytes": total_bytes,
        "coverage_increase_percent": round((total_bytes / 65536) * 100, 2),
        "manifests": created_manifests
    }
    
    with open('c4_s27_manifests_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print()
    print("=" * 60)
    print("SESSION 27 SUMMARY")
    print("=" * 60)
    print(f"Manifests created: {len(CANDIDATES)}")
    print(f"Pass range: {next_pass}-{next_pass + len(CANDIDATES) - 1}")
    print(f"Total bytes: {total_bytes}")
    print(f"Coverage increase: +{summary['coverage_increase_percent']:.2f}%")
    print()
    print("Score distribution:")
    score_7 = len([c for c in CANDIDATES if c['score'] >= 7])
    score_6 = len([c for c in CANDIDATES if c['score'] == 6])
    score_5 = len([c for c in CANDIDATES if c['score'] == 5])
    print(f"  Score 7+: {score_7}")
    print(f"  Score 6:  {score_6}")
    print(f"  Score 5:  {score_5}")

if __name__ == '__main__':
    main()
