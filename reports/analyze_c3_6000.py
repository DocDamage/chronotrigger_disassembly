#!/usr/bin/env python3
import json

# Load backtrack results (handle UTF-16)
with open('reports/c3_6000_6fff_backtrack.json', 'r', encoding='utf-16') as f:
    backtrack = json.load(f)

# Load seam block results (handle UTF-16)
with open('reports/c3_6000_6fff_seam_block.json', 'r', encoding='utf-16') as f:
    seam_block = json.load(f)

# Extract score-6+ candidates
score_6_plus = [c for c in backtrack['candidates'] if c['score'] >= 6]
score_4_plus = [c for c in backtrack['candidates'] if c['score'] >= 4 and c['score'] < 6]

print('=' * 70)
print('BANK C3:6000-6FFF ANALYSIS REPORT')
print('High-Density Region Discovery')
print('=' * 70)
print()

print('## SCORE-6+ CANDIDATES (Strong Function Evidence)')
print(f'Found {len(score_6_plus)} candidates with score >= 6:')
print()
for c in score_6_plus:
    start = c['candidate_start']
    target = c['target']
    score = c['score']
    start_byte = c['start_byte']
    print(f'  {start} -> target {target} | score={score} | start_byte=0x{start_byte}')
print()

print('## SCORE-4 CANDIDATES (Moderate Function Evidence)')
print(f'Found {len(score_4_plus)} candidates with score >= 4:')
print()
for c in score_4_plus:
    start = c['candidate_start']
    target = c['target']
    score = c['score']
    start_byte = c['start_byte']
    print(f'  {start} -> target {target} | score={score} | start_byte=0x{start_byte}')
print()

print('## SEAM BLOCK PAGE FAMILY SUMMARY')
print(f'Total pages scanned: {len(seam_block["pages"])}')
print()
family_counts = seam_block['page_family_counts']
for family, count in sorted(family_counts.items()):
    print(f'  {family}: {count} pages')
print()

print('## REVIEW POSTURE SUMMARY')
posture_counts = seam_block['review_posture_counts']
for posture, count in sorted(posture_counts.items()):
    print(f'  {posture}: {count} pages')
print()

print('## EXISTING DOCUMENTATION IN REGION')
print('  C3:65AB..C3:65C8 - ct_c3_65ab_gap_handler (pass 713)')
print('  C3:6643..C3:6660 - ct_c3_6643_gap_handler (pass 714)')
print()

print('## NEW HIGH-VALUE CANDIDATES FOR DOCUMENTATION')
print('Based on score-6+ analysis:')
print()

# Filter out already documented
documented = ['C3:65AB', 'C3:6643']
new_score_6 = [c for c in score_6_plus if c['candidate_start'] not in documented]
for i, c in enumerate(new_score_6, 1):
    start = c['candidate_start']
    target = c['target']
    score = c['score']
    start_byte = c['start_byte']
    byte_name = {'0B': 'PHD', 'A9': 'LDA#', '20': 'JSR', '08': 'PHP', '22': 'JSL'}.get(start_byte, start_byte)
    print(f'{i}. {start} (target: {target}) - score {score}, prologue: {byte_name}')
print()

print('## RECOMMENDED NEW MANIFESTS (Score-6+)')
print('These functions should be documented with high priority:')
print()
for i, c in enumerate(new_score_6, 716):
    start = c['candidate_start']
    print(f'  pass{i}_c3_{start.lower().replace("c3:", "")}_gap.json')
print()

print('## ADDITIONAL CANDIDATES (Score-4)')
print('These may be functions or helpers with moderate confidence:')
print()
count = 0
for c in score_4_plus[:15]:  # Top 15
    if c['score'] >= 4:
        count += 1
        start = c['candidate_start']
        target = c['target']
        score = c['score']
        start_byte = c['start_byte']
        byte_name = {'0B': 'PHD', 'A9': 'LDA#', '20': 'JSR', '08': 'PHP', '22': 'JSL', 'CE': 'DEC'}.get(start_byte, start_byte)
        print(f'  {start} (target: {target}) - score {score}, start: {byte_name}')
print()

print('## COVERAGE IMPACT')
print(f'  Region size: 4096 bytes (0x1000)')
print(f'  Currently documented: ~46 bytes (C3:65AB-65C8 + C3:6643-6660)')
print(f'  Coverage: ~1.1%')
print(f'  Potential new coverage: ~800-1200 bytes with score-4+ candidates')
print()

# Extract local clusters with high scores
print('## LOCAL CODE CLUSTERS (Islands with RTS evidence)')
clusters = []
for page in seam_block['pages']:
    for cluster in page.get('local_clusters', []):
        if cluster.get('cluster_score', 0) >= 4:
            clusters.append({
                'range': cluster['range'],
                'score': cluster['cluster_score'],
                'width': cluster['width'],
                'call_count': cluster['call_count'],
                'return_count': cluster['return_count']
            })

clusters.sort(key=lambda x: -x['score'])
print(f'Found {len(clusters)} clusters with score >= 4:')
print()
for c in clusters[:15]:
    print(f"  {c['range']} - score {c['score']}, width {c['width']}, calls={c['call_count']}, returns={c['return_count']}")
print()

print('=' * 70)
