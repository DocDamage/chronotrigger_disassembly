#!/usr/bin/env python3
"""Deep analysis of Bank C4 7000-8000 region"""
import json

# Load combined data
with open('c4_7000_8000_combined.json') as f:
    data = json.load(f)

islands = data['islands']

# Filter for high-value candidates
score_7 = [i for i in islands if i.get('score', 0) == 7]
score_6 = [i for i in islands if i.get('score', 0) == 6]
score_5 = [i for i in islands if i.get('score', 0) == 5]
score_4_call_heavy = [i for i in islands if i.get('score', 0) == 4 and i.get('call_count', 0) >= 1]

print('=== SCORE 7 CANDIDATES ===')
for i in score_7:
    print(json.dumps(i, indent=2))

print(f'\n=== SCORE 6 CANDIDATES ({len(score_6)} found) ===')
for i in score_6:
    print(f"  {i.get('range')}: bytes={i.get('width')}, branches={i.get('branch_count')}, calls={i.get('call_count')}")

print(f'\n=== SCORE 5 CANDIDATES ({len(score_5)} found) ===')
for i in score_5:
    print(f"  {i.get('range')}: bytes={i.get('width')}, branches={i.get('branch_count')}, calls={i.get('call_count')}")

print(f'\n=== SCORE 4 with CALLS ({len(score_4_call_heavy)} found) ===')
for i in score_4_call_heavy:
    print(f"  {i.get('range')}: bytes={i.get('width')}, branches={i.get('branch_count')}, calls={i.get('call_count')}")

# Create top candidates list for manifest generation
top_candidates = []
top_candidates.extend(score_7)
top_candidates.extend(score_6)
top_candidates.extend(score_5)
top_candidates.extend(score_4_call_heavy)

# Sort by score, then by branches+calls, then by width
top_candidates.sort(key=lambda x: (x.get('score', 0), 
                                   x.get('branch_count', 0) + x.get('call_count', 0),
                                   x.get('width', 0)), reverse=True)

print('\n=== TOP 10 CANDIDATES FOR MANIFESTS ===')
for idx, i in enumerate(top_candidates[:10], 1):
    print(f"{idx}. {i.get('range')}: score={i.get('score')}, bytes={i.get('width')}, branches={i.get('branch_count')}, calls={i.get('call_count')}")

# Save top candidates
with open('c4_7000_8000_top_candidates.json', 'w') as f:
    json.dump(top_candidates[:10], f, indent=2)
print(f'\nSaved top 10 candidates to c4_7000_8000_top_candidates.json')
