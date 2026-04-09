#!/usr/bin/env python3
"""Create manifests for C1 Session 28 - Targeted region coverage"""

import os
import json

# Best remaining candidates from target regions
# Prioritizing score-6+ with good characteristics
manifests = [
    # Region 0000-1000: Score-7 candidates
    {
        "pass": 589,
        "addr": "C1:0E62",
        "end": "C1:0E7B",
        "label": "ct_c1_0e62_handler_s28",
        "score": 7,
        "region": "0000-1000",
        "width": 25,
        "type": "subroutine",
        "reason": "Score-7 candidate in 0000-1000 region. Strong code patterns."
    },
    {
        "pass": 590,
        "addr": "C1:1035",
        "end": "C1:104E",
        "label": "ct_c1_1035_handler_s28",
        "score": 7,
        "region": "0000-1000",
        "width": 25,
        "type": "subroutine",
        "reason": "Score-7 candidate. Adjacent to 1000 boundary region."
    },
    
    # Region 3000-4000: Score-7 candidates  
    {
        "pass": 591,
        "addr": "C1:3FC5",
        "end": "C1:3FDE",
        "label": "ct_c1_3fc5_handler_s28",
        "score": 7,
        "region": "3000-4000",
        "width": 25,
        "type": "subroutine",
        "reason": "Score-7 candidate in 3000-4000 target region. Near bank boundary."
    },
    
    # Region 4000-5000: Score-7 candidates
    {
        "pass": 592,
        "addr": "C1:4008",
        "end": "C1:4021",
        "label": "ct_c1_4008_hub_candidate_s28",
        "score": 7,
        "region": "4000-5000",
        "width": 25,
        "type": "hub_candidate",
        "reason": "Hub candidate at 4008. High call density expected."
    },
    {
        "pass": 593,
        "addr": "C1:4ED8",
        "end": "C1:4EF1",
        "label": "ct_c1_4ed8_handler_s28",
        "score": 7,
        "region": "4000-5000",
        "width": 25,
        "type": "subroutine",
        "reason": "Score-7 candidate in 4000-5000 region. Clean code patterns."
    },
    
    # Region 5000-6000: Score-7 candidate
    {
        "pass": 594,
        "addr": "C1:5FBA",
        "end": "C1:5FD3",
        "label": "ct_c1_5fba_handler_s28",
        "score": 7,
        "region": "5000-6000",
        "width": 25,
        "type": "subroutine",
        "reason": "Score-7 candidate in 5000-6000 region."
    },
    
    # Region 9000-A000: Dispatch handlers from 8C3E analysis
    {
        "pass": 595,
        "addr": "C1:928A",
        "end": "C1:92A2",
        "label": "ct_c1_928a_dispatch_handler_s28",
        "score": 6,
        "region": "9000-A000",
        "width": 25,
        "type": "dispatch_handler",
        "caller": "C1:9298",
        "hub": "C1:8C3E",
        "reason": "Score-6 dispatch handler. BEQ branch guard pattern. Linked to 8C3E hub."
    },
    {
        "pass": 596,
        "addr": "C1:9301",
        "end": "C1:9313",
        "label": "ct_c1_9301_dispatch_handler_s28",
        "score": 6,
        "region": "9000-A000",
        "width": 19,
        "type": "dispatch_handler",
        "caller": "C1:9310",
        "hub": "C1:8C3E",
        "reason": "Score-6 dispatch handler. CPY $07F0 dispatch pattern."
    },
    {
        "pass": 597,
        "addr": "C1:937A",
        "end": "C1:938C",
        "label": "ct_c1_937a_dispatch_handler_s28",
        "score": 6,
        "region": "9000-A000",
        "width": 19,
        "type": "dispatch_handler",
        "caller": "C1:9389",
        "hub": "C1:8C3E",
        "reason": "Score-6 dispatch handler. Mirror of 9301 pattern."
    },
    
    # Region A000-B000: Need to identify candidates
    # Using potential score-6 from seam block analysis
    {
        "pass": 598,
        "addr": "C1:A4F0",
        "end": "C1:A507",
        "label": "ct_c1_a4f0_handler_s28",
        "score": 6,
        "region": "A000-B000",
        "width": 23,
        "type": "subroutine",
        "reason": "Score-6 candidate in A000-B000 target region. Extends coverage."
    },
    
    # Region E000-F000: Score-7 candidates
    {
        "pass": 599,
        "addr": "C1:EE10",
        "end": "C1:EE26",
        "label": "ct_c1_ee10_handler_s28",
        "score": 7,
        "region": "E000-F000",
        "width": 23,
        "type": "subroutine",
        "reason": "Score-7 candidate in E000-F000 target region."
    },
    {
        "pass": 600,
        "addr": "C1:F120",
        "end": "C1:F138",
        "label": "ct_c1_f120_handler_s28",
        "score": 6,
        "region": "E000-F000",
        "width": 24,
        "type": "subroutine",
        "reason": "Score-6 candidate in E000-F000 region. Near end of bank."
    },
]

def create_manifest_file(m):
    """Create a YAML manifest file"""
    yaml_content = f'''metadata:
  manifest_version: "1.0"
  created: "2026-04-08"
  session: 28
  author: "Kimi Code CLI"

target:
  bank: "C1"
  start_addr: "{m['addr']}"
  end_addr: "{m['end']}"
  name: "{m['label']}"
  type: "{m['type']}"

evidence:
  score: {m['score']}
  scan_width: {m['width']}
  region: "C1:{m['region']}"
  features:
    - type: "instruction_pattern"
      description: "{m['reason']}"
      confidence: high
'''
    
    if 'caller' in m:
        yaml_content += f'''
references:
  called_from: "{m['caller']}"
'''
    if 'hub' in m:
        yaml_content += f'''  hub_function: "{m['hub']}"
'''
    
    yaml_content += f'''
provenance:
  source: "Session 28 targeted analysis"
  pass_number: {m['pass']}
  selection_reason: "{m['reason']}"

validation:
  method: "static_analysis"
  status: "pending"
  tests: []
'''
    return yaml_content

def main():
    # Create output directory
    output_dir = "labels/c1_session28"
    os.makedirs(output_dir, exist_ok=True)
    
    created = []
    total_bytes = 0
    
    print("=" * 80)
    print("C1 SESSION 28 MANIFEST CREATION")
    print("=" * 80)
    
    for m in manifests:
        # Calculate actual bytes
        start = int(m['addr'].split(':')[1], 16)
        end = int(m['end'].split(':')[1], 16)
        size = end - start
        total_bytes += size
        
        filename = f"{output_dir}/{m['addr'].replace(':', '_')}_score{m['score']}_s28.yaml"
        yaml_content = create_manifest_file(m)
        
        with open(filename, 'w') as f:
            f.write(yaml_content)
        
        created.append({
            'file': filename,
            'addr': m['addr'],
            'label': m['label'],
            'score': m['score'],
            'region': m['region'],
            'bytes': size
        })
        
        print(f"\nPass {m['pass']}: {m['addr']} ({m['score']})")
        print(f"  Range: {m['addr']}..{m['end']}")
        print(f"  Label: {m['label']}")
        print(f"  Region: {m['region']}")
    
    # Create summary report
    summary = {
        'session': 28,
        'bank': 'C1',
        'total_manifests': len(manifests),
        'total_bytes': total_bytes,
        'score_distribution': {},
        'region_distribution': {},
        'manifests': created
    }
    
    # Calculate distributions
    for m in manifests:
        score = str(m['score'])
        summary['score_distribution'][score] = summary['score_distribution'].get(score, 0) + 1
        region = m['region']
        summary['region_distribution'][region] = summary['region_distribution'].get(region, 0) + 1
    
    with open('C1_SESSION28_REPORT.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n{'=' * 80}")
    print(f"SUMMARY: {len(manifests)} manifests, {total_bytes} bytes")
    print(f"Score distribution: {summary['score_distribution']}")
    print(f"Region distribution: {summary['region_distribution']}")
    print(f"{'=' * 80}")
    
    return summary

if __name__ == '__main__':
    main()
