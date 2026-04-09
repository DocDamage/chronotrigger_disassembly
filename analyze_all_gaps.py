#!/usr/bin/env python3
import json
import os

# Load all candidates
with open('c0_all_score6_candidates_v2.json', 'r') as f:
    candidates = json.load(f)

# Priority gaps
gaps = [
    (0x3224, 0x34ED, "3224-34ED (714 bytes) - C0:3000-4000"),
    (0x3DA9, 0x407B, "3DA9-407B (723 bytes) - C0:3000-4000"),
    (0xAD37, 0xAFFF, "AD37-AFFF (713 bytes) - C0:A000-B000"),
    (0xD6C5, 0xD975, "D6C5-D975 (689 bytes) - C0:D000-E000"),
    (0xED15, 0xEFCA, "ED15-EFCA (694 bytes) - C0:E000-F000"),
]

def addr_to_int(addr_str):
    if isinstance(addr_str, str):
        if ':' in addr_str:
            addr_str = addr_str.split(':')[1]
        addr_str = addr_str.replace('0x', '')
        return int(addr_str, 16)
    return addr_str

print("=== Candidates in Priority Gaps ===\n")

all_gap_candidates = []
for start, end, name in gaps:
    gap_candidates = []
    for c in candidates:
        addr = addr_to_int(c.get('addr', '0'))
        if start <= addr <= end:
            gap_candidates.append((addr, c))
    
    gap_candidates.sort()
    all_gap_candidates.extend(gap_candidates)
    
    print(f"{name}:")
    print(f"  {len(gap_candidates)} candidates")
    for addr, c in gap_candidates:
        score = c.get('score', 0)
        target = c.get('target', 'N/A')
        print(f"    C0:{addr:04X} score={score} target={target}")
    print()

# Check existing manifests in c0_new_candidates
print("=== Existing Manifests in Priority Gaps ===\n")
manifest_dir = 'labels/c0_new_candidates'
for start, end, name in gaps:
    gap_manifests = []
    for f in os.listdir(manifest_dir):
        if f.endswith('.json'):
            try:
                with open(os.path.join(manifest_dir, f), 'r') as mf:
                    m = json.load(mf)
                    addr = addr_to_int(m.get('address', '0'))
                    if start <= addr <= end:
                        gap_manifests.append((addr, m, f))
            except:
                pass
    
    if gap_manifests:
        print(f"{name}:")
        for addr, m, f in sorted(gap_manifests):
            print(f"  C0:{addr:04X} - {m.get('label')} ({f})")
        print()

# Check existing label files (YAML)
print("=== Existing Label Files in Priority Gaps ===\n")
label_dir = 'labels'
for start, end, name in gaps:
    gap_labels = []
    for f in os.listdir(label_dir):
        if f.startswith('bank_C0_') and f.endswith('.yaml'):
            # Extract address from filename
            parts = f.split('_')
            if len(parts) >= 3:
                try:
                    addr = int(parts[2], 16)
                    if start <= addr <= end:
                        gap_labels.append((addr, f))
                except:
                    pass
    
    if gap_labels:
        print(f"{name}:")
        for addr, f in sorted(gap_labels):
            print(f"  C0:{addr:04X} - {f}")
        print()
