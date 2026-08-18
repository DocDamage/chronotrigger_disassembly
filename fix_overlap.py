#!/usr/bin/env python3
import json

# Load manifest
with open('passes/session30_c4/pass0763.json') as f:
    m = json.load(f)

# Check what Pass 750 covers
with open('passes/pass0750.json') as f:
    p750 = json.load(f)

print(f"Pass 750: {p750['start']}..{p750['end']} (size={p750['size']})")
print(f"Pass 763: {m['start']}..{m['end']} (size={m['size']})")

# Adjust Pass 763 to start after 0E96
m['start'] = 'C4:0E97'
m['end'] = 'C4:0EBE'
m['size'] = 39  # Keep same size
m['label'] = 'ct_c4_0e97_php_handler_s30'
m['target'] = 'C4:0EA0'

print(f"\nAdjusted Pass 763: {m['start']}..{m['end']} (size={m['size']})")

# Save
with open('passes/session30_c4/pass0763.json', 'w') as f:
    json.dump(m, f, indent=2)

# Update combined file
with open('passes/session30_c4/c4_session30_manifests.json') as f:
    manifests = json.load(f)

for i, man in enumerate(manifests):
    if man['pass'] == 763:
        manifests[i] = m
        break

with open('passes/session30_c4/c4_session30_manifests.json', 'w') as f:
    json.dump(manifests, f, indent=2)

print('Updated!')
