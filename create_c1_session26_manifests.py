#!/usr/bin/env python3
"""
Create Session 26 manifests for Bank C1 score-6+ candidates.

Strategy:
1. Prioritize score-7+ candidates first
2. Then score-6 with multiple calls/branches
3. Focus on high-density target regions:
   - C1:9000-A000 (15 score-6+ found)
   - C1:A000-B000 (19 score-6+ found)
   - C1:E000-F000 (19 score-6+ found)
   - C1:3000-4000 (12 score-6+ found)
4. Create 10-12 manifests for best candidates
5. Use session 26
"""

import json
import os
from pathlib import Path

OUTPUT_DIR = "labels/c1_session26"
SESSION = 26

# Candidate data derived from C1_initial_scan_summary.json and dispatch reports
# Prioritized by: score, call_count, branch_count, region density

CANDIDATES = [
    # === SCORE 7+ CANDIDATES (Prioritized) ===
    
    # Region: 3000-4000 (12 score-6+ total in region)
    {
        "addr_start": "C1:3AF3",
        "addr_end": "C1:3B0C",
        "name": "ct_c1_3af3_handler_s26",
        "score": 7,
        "call_count": 1,
        "branch_count": 3,
        "return_count": 1,
        "width": 25,
        "region": "3000-4000",
        "reason": "Score-7 candidate in 3000-4000 region. Strong subroutine pattern."
    },
    {
        "addr_start": "C1:3C7D",
        "addr_end": "C1:3C92",
        "name": "ct_c1_3c7d_handler_s26",
        "score": 7,
        "call_count": 1,
        "branch_count": 3,
        "return_count": 1,
        "width": 21,
        "region": "3000-4000",
        "reason": "Score-7 candidate in 3000-4000 region. Good function structure."
    },
    {
        "addr_start": "C1:3F8B",
        "addr_end": "C1:3FA4",
        "name": "ct_c1_3f8b_handler_s26",
        "score": 7,
        "call_count": 1,
        "branch_count": 3,
        "return_count": 1,
        "width": 25,
        "region": "3000-4000",
        "reason": "Score-7 candidate in 3000-4000 region. High confidence subroutine."
    },
    {
        "addr_start": "C1:3FC5",
        "addr_end": "C1:3FDE",
        "name": "ct_c1_3fc5_handler_s26",
        "score": 7,
        "call_count": 1,
        "branch_count": 3,
        "return_count": 1,
        "width": 25,
        "region": "3000-4000",
        "reason": "Score-7 candidate near end of region. Clean entry/exit."
    },
    
    # Region: 9000-A000 (15 score-6+ total in region)
    {
        "addr_start": "C1:906E",
        "addr_end": "C1:9081",
        "name": "ct_c1_906e_handler_s26",
        "score": 7,
        "call_count": 1,
        "branch_count": 3,
        "return_count": 1,
        "width": 19,
        "region": "9000-A000",
        "reason": "Score-7 candidate. Part of C1:8C3E dispatch handler group."
    },
    {
        "addr_start": "C1:96D4",
        "addr_end": "C1:9727",
        "name": "ct_c1_96d4_dispatch_handler_s26",
        "score": 7,
        "call_count": 1,
        "branch_count": 5,
        "return_count": 1,
        "width": 83,
        "region": "9000-A000",
        "reason": "Large dispatch handler. Multiple internal branches, good structure."
    },
    {
        "addr_start": "C1:9792",
        "addr_end": "C1:97D4",
        "name": "ct_c1_9792_score8_cluster_s26",
        "score": 8,
        "call_count": 3,
        "branch_count": 4,
        "return_count": 1,
        "width": 66,
        "region": "9000-A000",
        "reason": "SCORE-8 MEGA CANDIDATE. 3 callers, high branch count. Priority target."
    },
    {
        "addr_start": "C1:97D5",
        "addr_end": "C1:980F",
        "name": "ct_c1_97d5_dispatch_handler_s26",
        "score": 7,
        "call_count": 1,
        "branch_count": 4,
        "return_count": 1,
        "width": 58,
        "region": "9000-A000",
        "reason": "Dispatch handler with strong branch pattern. Part of handler chain."
    },
    
    # Region: A000-B000 (19 score-6+ total in region)
    {
        "addr_start": "C1:A130",
        "addr_end": "C1:A14A",
        "name": "ct_c1_a130_handler_s26",
        "score": 7,
        "call_count": 1,
        "branch_count": 3,
        "return_count": 1,
        "width": 26,
        "region": "A000-B000",
        "reason": "Score-7 candidate in A000-B000 region. Clean subroutine."
    },
    {
        "addr_start": "C1:A8F0",
        "addr_end": "C1:A910",
        "name": "ct_c1_a8f0_handler_s26",
        "score": 7,
        "call_count": 1,
        "branch_count": 4,
        "return_count": 1,
        "width": 32,
        "region": "A000-B000",
        "reason": "Score-7 candidate with high branch count. Good code density."
    },
    {
        "addr_start": "C1:AC50",
        "addr_end": "C1:AC6E",
        "name": "ct_c1_ac50_brancher_s26",
        "score": 6,
        "call_count": 0,
        "branch_count": 5,
        "return_count": 1,
        "width": 30,
        "region": "A000-B000",
        "reason": "Score-6 with 5 branches (no calls). High internal complexity."
    },
    
    # Region: E000-F000 (19 score-6+ total in region)
    {
        "addr_start": "C1:E99F",
        "addr_end": "C1:E9BB",
        "name": "ct_c1_e99f_handler_s26",
        "score": 7,
        "call_count": 1,
        "branch_count": 3,
        "return_count": 1,
        "width": 28,
        "region": "E000-F000",
        "reason": "Score-7 candidate. Strong subroutine pattern in E000 region."
    },
    {
        "addr_start": "C1:E9BC",
        "addr_end": "C1:E9D5",
        "name": "ct_c1_e9bc_handler_s26",
        "score": 7,
        "call_count": 1,
        "branch_count": 3,
        "return_count": 1,
        "width": 25,
        "region": "E000-F000",
        "reason": "Score-7 candidate adjacent to E99F. Related handler pair."
    },
    {
        "addr_start": "C1:EDA0",
        "addr_end": "C1:EDBC",
        "name": "ct_c1_eda0_handler_s26",
        "score": 7,
        "call_count": 1,
        "branch_count": 3,
        "return_count": 1,
        "width": 28,
        "region": "E000-F000",
        "reason": "Score-7 candidate. Well-defined boundaries, clean RTS."
    },
    {
        "addr_start": "C1:EF67",
        "addr_end": "C1:EF82",
        "name": "ct_c1_ef67_handler_s26",
        "score": 7,
        "call_count": 1,
        "branch_count": 3,
        "return_count": 1,
        "width": 27,
        "region": "E000-F000",
        "reason": "Score-7 candidate. Strong entry point pattern."
    },
    
    # === HIGH-VALUE SCORE-6 CANDIDATES ===
    
    # Score-6 with multiple calls
    {
        "addr_start": "C1:434A",
        "addr_end": "C1:43B7",
        "name": "ct_c1_434a_mega_cluster_s26",
        "score": 6,
        "call_count": 2,
        "branch_count": 6,
        "return_count": 2,
        "width": 110,
        "region": "4000-5000",
        "reason": "MEGA CLUSTER. 110 bytes, 2 callers, 6 branches. High-value target."
    },
    {
        "addr_start": "C1:51D5",
        "addr_end": "C1:51F0",
        "name": "ct_c1_51d5_handler_s26",
        "score": 7,
        "call_count": 1,
        "branch_count": 3,
        "return_count": 1,
        "width": 27,
        "region": "5000-6000",
        "reason": "Score-7 candidate. Strong subroutine in mid-bank region."
    },
    {
        "addr_start": "C1:6B44",
        "addr_end": "C1:6B60",
        "name": "ct_c1_6b44_handler_s26",
        "score": 7,
        "call_count": 1,
        "branch_count": 3,
        "return_count": 1,
        "width": 28,
        "region": "6000-7000",
        "reason": "Score-7 candidate. Well-structured function."
    },
    {
        "addr_start": "C1:7435",
        "addr_end": "C1:7450",
        "name": "ct_c1_7435_handler_s26",
        "score": 7,
        "call_count": 1,
        "branch_count": 3,
        "return_count": 1,
        "width": 27,
        "region": "7000-8000",
        "reason": "Score-7 candidate in 7000-8000 region. Good coverage expansion."
    },
    {
        "addr_start": "C1:EE10",
        "addr_end": "C1:EE27",
        "name": "ct_c1_ee10_handler_s26",
        "score": 7,
        "call_count": 1,
        "branch_count": 3,
        "return_count": 1,
        "width": 23,
        "region": "E000-F000",
        "reason": "Score-7 candidate. Compact efficient subroutine."
    },
]


def create_manifest(candidate, index):
    """Create a manifest file for a candidate."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    start_addr = candidate["addr_start"]
    end_addr = candidate["addr_end"]
    name = candidate["name"]
    score = candidate["score"]
    
    # Parse address for filename
    addr_int = int(start_addr.split(":")[1], 16)
    filename = f"C1_{addr_int:04X}_score{score}_s26.yaml"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    manifest = {
        "manifest_version": "1.0",
        "session": SESSION,
        "target": {
            "bank": "C1",
            "start_addr": start_addr,
            "end_addr": end_addr,
            "name": name
        },
        "metadata": {
            "score": score,
            "call_count": candidate["call_count"],
            "branch_count": candidate["branch_count"],
            "return_count": candidate["return_count"],
            "width": candidate["width"],
            "region": candidate["region"],
            "selection_reason": candidate["reason"]
        },
        "disassembly": {
            "mode": "code",
            "merge_policy": "session_priority"
        }
    }
    
    with open(filepath, 'w') as fp:
        json.dump(manifest, fp, indent=2)
    
    return filepath, name


def main():
    print('=' * 70)
    print(f'Bank C1 Session {SESSION} Manifest Creation')
    print('=' * 70)
    print(f"\nProcessing {len(CANDIDATES)} score-6+ candidates")
    print("Selection criteria: score-7+ first, then score-6 with high calls/branches")
    print("Target regions: 3000-4000, 9000-A000, A000-B000, E000-F000")
    
    # Prioritize candidates
    # 1. Score 8+ first
    # 2. Score 7
    # 3. Score 6 with multiple calls or branches
    def priority_key(c):
        score = c["score"]
        calls = c["call_count"]
        branches = c["branch_count"]
        # Priority: score * 100 + calls * 10 + branches
        return (score * 100 + calls * 10 + branches)
    
    sorted_candidates = sorted(CANDIDATES, key=priority_key, reverse=True)
    
    # Select top 12 with good region distribution
    selected = []
    region_counts = {}
    
    for c in sorted_candidates:
        region = c["region"]
        # Limit to 3 per region for good distribution
        if region_counts.get(region, 0) >= 3:
            continue
        if len(selected) >= 12:
            break
        selected.append(c)
        region_counts[region] = region_counts.get(region, 0) + 1
    
    print(f"\nSelected {len(selected)} candidates for manifests:")
    print("-" * 70)
    
    # Create manifests
    manifests = []
    total_bytes = 0
    
    for i, c in enumerate(selected):
        filepath, name = create_manifest(c, i)
        addr_range = f"{c['addr_start']}..{c['addr_end']}"
        width = c['width']
        total_bytes += width
        
        manifests.append({
            'filepath': filepath,
            'name': name,
            'range': addr_range,
            'score': c['score'],
            'region': c['region'],
            'width': width
        })
        
        print(f"  {i+1:2d}. {filepath}")
        print(f"      Name: {name}")
        print(f"      Range: {addr_range} ({width} bytes)")
        print(f"      Score: {c['score']}, Calls: {c['call_count']}, Branches: {c['branch_count']}")
        print(f"      Region: {c['region']}")
        print()
    
    # Summary statistics
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    # Score distribution
    score_dist = {}
    for m in manifests:
        s = m['score']
        score_dist[s] = score_dist.get(s, 0) + 1
    print(f"\nScore Distribution:")
    for score in sorted(score_dist.keys(), reverse=True):
        print(f"  Score-{score}: {score_dist[score]} manifests")
    
    # Region distribution
    print(f"\nRegion Distribution:")
    for region in sorted(region_counts.keys()):
        print(f"  {region}: {region_counts[region]} manifests")
    
    print(f"\nCoverage:")
    print(f"  Total manifests: {len(manifests)}")
    print(f"  Total bytes: {total_bytes}")
    print(f"  Average bytes per manifest: {total_bytes / len(manifests):.1f}")
    print(f"  Bank C1 coverage increase: ~{total_bytes / 65536 * 100:.2f}%")
    
    # Write summary report
    report = {
        'session': SESSION,
        'bank': 'C1',
        'total_manifests': len(manifests),
        'total_bytes': total_bytes,
        'score_distribution': score_dist,
        'region_distribution': region_counts,
        'manifests': manifests,
        'target_regions': ['3000-4000', '9000-A000', 'A000-B000', 'E000-F000'],
        'selection_criteria': [
            'Score-7+ prioritized',
            'Score-6 with multiple calls/branches',
            'High-density region focus',
            'Maximum 3 per region for distribution'
        ]
    }
    
    report_path = f'C1_SESSION{SESSION}_REPORT.json'
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nReport saved to: {report_path}")
    print(f"Manifests saved to: {OUTPUT_DIR}/")
    print("=" * 70)
    
    return manifests


if __name__ == '__main__':
    main()
