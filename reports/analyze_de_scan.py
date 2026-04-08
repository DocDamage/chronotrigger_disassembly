#!/usr/bin/env python3
import json

regions = [
    ('DE:0000-4000', 'reports/de_0000_4000_backtrack.json'),
    ('DE:4000-8000', 'reports/de_4000_8000_backtrack.json'),
    ('DE:8000-C000', 'reports/de_8000_c000_backtrack.json'),
    ('DE:C000-FFFF', 'reports/de_c000_ffff_backtrack.json'),
]

print("=" * 70)
print("BANK DE DEEP SCAN - HIGH SCORE CANDIDATES (score-6+)")
print("=" * 70)

all_high_scores = []
for name, path in regions:
    try:
        with open(path) as f:
            d = json.load(f)
        candidates = [x for x in d['candidates'] if x['score'] >= 6]
        all_high_scores.extend([(name, x) for x in candidates])
        print(f'\n{name}: {len(candidates)} score-6+ candidates')
        for x in sorted(candidates, key=lambda x: -x['score'])[:15]:
            print(f"  score={x['score']:2d} {x['candidate_start']} -> target={x['target']}")
    except Exception as e:
        print(f'{name}: ERROR - {e}')

# Score 10+ summary
print("\n" + "=" * 70)
print("SCORE-10+ ELITE CANDIDATES (All)")
print("=" * 70)
score_10_plus = [(r, x) for r, x in all_high_scores if x['score'] >= 10]
for region, x in sorted(score_10_plus, key=lambda x: -x[1]['score']):
    print(f"  score={x['score']:2d} [{region}] {x['candidate_start']} -> target={x['target']}")

print(f"\nTotal score-10+ functions found: {len(score_10_plus)}")

# Score 6+ summary
print("\n" + "=" * 70)
print("SCORE-6+ SUMMARY BY REGION")
print("=" * 70)
for name, path in regions:
    try:
        with open(path) as f:
            d = json.load(f)
        score_6_9 = len([x for x in d['candidates'] if 6 <= x['score'] <= 9])
        score_10_plus = len([x for x in d['candidates'] if x['score'] >= 10])
        print(f"  {name}: {score_6_9} score-6-9, {score_10_plus} score-10+")
    except:
        pass
