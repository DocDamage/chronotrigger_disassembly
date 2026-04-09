#!/usr/bin/env python3
"""Create YAML manifest files for C4:7000-8000 deep dive (Session 22)"""

import json
import os

# Load top candidates
with open('c4_7000_8000_top_candidates.json') as f:
    candidates = json.load(f)

# Session 22 manifests
start_pass = 631
session = 22

# Ensure manifests directory exists
os.makedirs('passes/manifests', exist_ok=True)

created = []
for idx, c in enumerate(candidates[:10]):
    range_str = c['range']
    # Parse range C4:7730..C4:7748
    start, end = range_str.split('..')
    start_addr = start.replace('C4:', '')
    end_addr = end.replace('C4:', '')
    bank = 4
    
    # Create full address (bank + offset)
    address = f"04{start_addr}"
    
    score = c['score']
    width = c['width']
    branches = c['branch_count']
    calls = c['call_count']
    rets = c['return_count']
    stackish = c.get('stackish_count', 0)
    
    pass_num = start_pass + idx
    
    # Create label
    label = f"ct_c4_{start_addr.lower()}_score{score}"
    
    # Create filename
    filename = f"pass_{pass_num}_c4_{start_addr.lower()}.yaml"
    filepath = f"passes/manifests/{filename}"
    
    # Create rationale
    rationale = f"Score {score} candidate from C4:7000-8000 deep scan. {width} bytes with {rets} returns"
    if branches > 0:
        rationale += f", {branches} branches"
    if calls > 0:
        rationale += f", {calls} calls"
    rationale += "."
    if score >= 7:
        rationale += " HIGH PRIORITY - exceptional code density."
    
    # Create YAML content
    yaml_content = f"""pass: {pass_num}
address: {address}
bank: {bank}
label: {label}
range: C4:{start_addr}-C4:{end_addr}
score: {score}
width: {width}
call_count: {calls}
branch_count: {branches}
stackish_count: {stackish}
return_count: {rets}
session: {session}
rationale: {rationale}
"""
    
    with open(filepath, 'w') as f:
        f.write(yaml_content)
    
    created.append({
        'pass': pass_num,
        'file': filename,
        'label': label,
        'range': f"C4:{start_addr}-C4:{end_addr}",
        'score': score,
        'bytes': width
    })
    print(f"Created {filepath}")

print(f"\n{'='*60}")
print(f"Created {len(created)} manifests for Session {session}")
print(f"Passes: {created[0]['pass']} - {created[-1]['pass']}")
total_bytes = sum(c['bytes'] for c in created)
print(f"Total bytes: {total_bytes}")
print(f"{'='*60}")

# Save manifest index
with open('c4_7000_8000_manifest_index.json', 'w') as f:
    json.dump(created, f, indent=2)
print(f"\nSaved manifest index to c4_7000_8000_manifest_index.json")
