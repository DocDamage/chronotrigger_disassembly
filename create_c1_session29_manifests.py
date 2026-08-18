#!/usr/bin/env python3
"""Create manifests for C1 Session 29"""
import json
import os
from datetime import datetime

# Load candidates
with open('c1_session29_candidates.json', 'r') as f:
    candidates = json.load(f)

# Check which were already processed
processed = set()
for session in [25, 26, 27, 28]:
    try:
        with open(f'C1_SESSION{session}_REPORT.json', 'r') as f:
            sdata = json.load(f)
            for m in sdata.get('manifests', []):
                range_str = m.get('range', '')
                if range_str:
                    addr = range_str.split('..')[0]
                    processed.add(addr)
    except:
        pass

# Filter out already processed
final_candidates = [c for c in candidates if c['addr'] not in processed]
print(f"Candidates after filtering processed: {len(final_candidates)}")

# Replace with new candidates if needed
remaining = []
with open('c1_all_candidates.json', 'r') as f:
    all_data = json.load(f)
    remaining = [c for c in all_data['remaining'] if c['addr'] not in processed and c['addr'] not in [x['addr'] for x in final_candidates]]

# Sort remaining by score
remaining.sort(key=lambda x: (-x['score'], x['addr']))

# Fill up to 12
while len(final_candidates) < 12 and remaining:
    final_candidates.append(remaining.pop(0))

print(f"Final candidates for session 29: {len(final_candidates)}")

# Get next pass number
import glob
manifest_files = glob.glob('passes/manifests/pass*.json')
max_pass = 1009  # From session 28
for mf in manifest_files:
    try:
        pass_num = int(os.path.basename(mf).split('_')[0].replace('pass', ''))
        max_pass = max(max_pass, pass_num)
    except:
        pass

start_pass = max_pass + 1
print(f"Starting at pass {start_pass}")

# Create manifests
session_manifests = []
for i, c in enumerate(final_candidates):
    pass_num = start_pass + i
    addr = c['addr']
    addr_clean = addr.replace(':', '_').replace('..', '_')
    bank = addr.split(':')[0]
    addr_int = int(addr.split(':')[1], 16)
    end_int = addr_int + c['width']
    end_addr = f"{bank}:{end_int:04X}"
    region_int = addr_int // 0x1000
    region = f"{region_int:01X}000-{(region_int+1):01X}FFF"
    
    score = c['score']
    label = f"ct_{addr_clean.lower()}_score{score}_s29"
    
    # Create YAML label file
    yaml_content = f"""metadata:
  manifest_version: "1.0"
  created: "{datetime.now().strftime('%Y-%m-%d')}"
  session: 29
  author: "Kimi Code CLI"

target:
  bank: "{bank}"
  start_addr: "{addr}"
  end_addr: "{end_addr}"
  name: "{label}"
  type: "{c['type']}"

evidence:
  score: {score}
  scan_width: {c['width']}
  region: "{bank}:{region}"
  features:
    - type: "instruction_pattern"
      description: "Score-{score} candidate in {region} region. {c['type'].replace('_', ' ').title()}."
      confidence: {'high' if score >= 7 else 'medium'}

provenance:
  source: "Session 29 analysis"
  pass_number: {pass_num}
  selection_reason: "Score-{score} candidate from {c['source']}."

validation:
  method: "static_analysis"
  status: "pending"
  tests: []
"""
    
    yaml_file = f"labels/c1_session29/{addr_clean}_score{score}_s29.yaml"
    with open(yaml_file, 'w') as f:
        f.write(yaml_content)
    
    # Create JSON manifest
    manifest = {
        "pass": pass_num,
        "label": label,
        "bank": bank,
        "addr": addr,
        "end": end_addr,
        "size": c['width'],
        "score": score,
        "type": c['type'],
        "region": region,
        "session": 29,
        "yaml_file": yaml_file
    }
    
    manifest_file = f"passes/manifests/pass{pass_num}_c1_session29.json"
    with open(manifest_file, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    session_manifests.append({
        "pass": pass_num,
        "filepath": yaml_file,
        "name": label,
        "range": f"{addr}..{end_addr}",
        "score": score,
        "region": region.replace('000-', '000-').split('-')[0] + '00-' + region.split('-')[1][:1] + 'FF',
        "width": c['width']
    })
    
    print(f"Pass {pass_num}: {addr} ({score}) - {c['width']} bytes")

# Create session report
report = {
    "session": 29,
    "bank": "C1",
    "total_manifests": len(session_manifests),
    "total_bytes": sum(m['width'] for m in session_manifests),
    "score_distribution": {},
    "region_distribution": {},
    "manifests": session_manifests,
    "target_regions": ["3000-4000", "6000-7000", "9000-A000", "D000-E000", "E000-F000"],
    "selection_criteria": [
        "Score-7+ prioritized",
        "Score-6 with high value for coverage",
        "Spread across target regions",
        "Max 12 candidates for focused session"
    ]
}

# Calculate distributions
for m in session_manifests:
    score = str(m['score'])
    report['score_distribution'][score] = report['score_distribution'].get(score, 0) + 1
    
    region_key = m['region'][:2] + '00-' + m['region'][6:8] + 'FF'
    report['region_distribution'][region_key] = report['region_distribution'].get(region_key, 0) + 1

with open('C1_SESSION29_REPORT.json', 'w') as f:
    json.dump(report, f, indent=2)

print(f"\nSession 29 complete!")
print(f"Total manifests: {len(session_manifests)}")
print(f"Total bytes: {report['total_bytes']}")
print(f"Score distribution: {report['score_distribution']}")
print(f"Region distribution: {report['region_distribution']}")
