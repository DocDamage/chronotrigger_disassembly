#!/usr/bin/env python3
"""Generate manifests for C4:7000-8000 deep dive (Session 22)"""

import json

# Load top candidates
with open('c4_7000_8000_top_candidates.json') as f:
    candidates = json.load(f)

# Session 22 manifests
manifests = []
start_pass = 631  # Continue from previous session

for idx, c in enumerate(candidates[:10]):
    range_str = c['range']
    # Convert range format C4:7730..C4:7748 to extract start address
    start_addr = range_str.split('..')[0].replace('C4:', 'c4_')
    score = c['score']
    width = c['width']
    branches = c['branch_count']
    calls = c['call_count']
    rets = c['return_count']
    
    # Determine confidence based on score
    if score >= 7:
        confidence = 'very_high'
    elif score >= 5:
        confidence = 'high'
    else:
        confidence = 'medium'
    
    # Create label
    label = f"ct_{start_addr}_s{score}_b{branches}c{calls}"
    
    # Create reason
    reason_parts = [f"Score-{score} candidate"]
    if branches > 0:
        reason_parts.append(f"{branches} branches")
    if calls > 0:
        reason_parts.append(f"{calls} calls")
    if rets > 0:
        reason_parts.append(f"{rets} returns")
    
    reason = ", ".join(reason_parts)
    
    manifest = {
        'pass': start_pass + idx,
        'range': range_str,
        'label': label,
        'score': score,
        'bytes': width,
        'branches': branches,
        'calls': calls,
        'returns': rets,
        'confidence': confidence,
        'reason': reason
    }
    manifests.append(manifest)

if __name__ == '__main__':
    print('=' * 80)
    print('C4:7000-8000 DEEP DIVE MANIFESTS (Session 22, Passes 631-640)')
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
  "promotion_reason": "{m['reason']}. {m['bytes']} bytes."
}}''')
        total_bytes += m['bytes']
    
    print(f'\n{"=" * 80}')
    print(f'SUMMARY: {len(manifests)} functions, {total_bytes} bytes')
    print(f'Passes: {manifests[0]["pass"]} - {manifests[-1]["pass"]}')
    print(f'{"=" * 80}')
    
    # Save manifests
    with open('c4_7000_8000_manifests.json', 'w') as f:
        json.dump(manifests, f, indent=2)
    print(f'\nSaved manifests to c4_7000_8000_manifests.json')
