#!/usr/bin/env python3
import json
import os

# Check the actual created manifests
manifests = []
for f in os.listdir('passes/manifests'):
    if f.startswith('pass101') and 'c1_session29' in f:
        with open(f'passes/manifests/{f}') as fp:
            m = json.load(fp)
            manifests.append(m)

print(f"Total manifests created: {len(manifests)}")
total_bytes = sum(m['size'] for m in manifests)
print(f"Total bytes: {total_bytes}")

scores = {}
for m in manifests:
    s = str(m['score'])
    scores[s] = scores.get(s, 0) + 1
print(f"Score distribution: {scores}")

# Update the report
with open('C1_SESSION29_REPORT.json', 'r') as f:
    report = json.load(f)

report['total_manifests'] = len(manifests)
report['total_bytes'] = total_bytes
report['score_distribution'] = {int(k): v for k, v in scores.items()}
report['manifests'] = sorted([{
    "pass": m['pass'],
    "filepath": m['yaml_file'],
    "name": m['label'],
    "range": f"{m['addr']}..{m['end']}",
    "score": m['score'],
    "region": m['region'],
    "width": m['size']
} for m in manifests], key=lambda x: x['pass'])

with open('C1_SESSION29_REPORT.json', 'w') as f:
    json.dump(report, f, indent=2)

print()
print("Created manifests:")
for m in sorted(manifests, key=lambda x: x['pass']):
    print(f"  Pass {m['pass']}: {m['addr']} - score {m['score']} - {m['size']} bytes")

print("\nReport updated!")
