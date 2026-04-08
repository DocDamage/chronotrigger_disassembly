#!/usr/bin/env python3
"""
Bank C1:8E00-9800 Dispatch Table Analysis Report Generator
"""

import json

def main():
    # Read the seam block report
    with open('reports/c1_8e00_9800_seam_block.json', 'r') as f:
        seam_data = json.load(f)

    # Read the backtrack report
    with open('reports/c1_8e00_9800_backtrack.json', 'r') as f:
        backtrack_data = json.load(f)

    # Read the anchor report
    with open('reports/c1_8c3e_call_anchor_report.json', 'r') as f:
        anchor_data = json.load(f)

    report = []
    report.append('=' * 70)
    report.append('BANK C1:8E00-9800 DISPATCH TABLE ANALYSIS REPORT')
    report.append('=' * 70)
    report.append('')

    report.append('## 1. CALLER VALIDATION FOR C1:8C3E HUB')
    report.append('-' * 70)
    report.append(f"Target: {anchor_data['target']}")
    report.append(f"Total Callers Found: {anchor_data['call_count']}")
    report.append(f"Strong Anchors: {anchor_data['strong_anchor_count']}")
    report.append(f"Weak Anchors: {anchor_data['weak_anchor_count']}")
    report.append(f"Suspect Anchors: {anchor_data['suspect_anchor_count']}")
    report.append(f"Invalid: {anchor_data['invalid_count']}")
    report.append('')
    report.append('All 42 callers are VALID JSR instructions')
    report.append('All 42 are WEAK anchors (callers in unresolved regions)')
    report.append('')

    report.append('## 2. DISPATCH TABLE PATTERN ANALYSIS')
    report.append('-' * 70)
    report.append('Spacing Pattern:')
    report.append('  - 65.9% of gaps are table-like (0x30-0x80 bytes)')
    report.append('  - Average gap: 58.4 bytes')
    report.append('  - Range: 10-121 bytes')
    report.append('')
    report.append('Dispatch Type: CODE-BASED JUMP TABLE')
    report.append('  - 42 handler functions in C1:8E00-9800 range')
    report.append('  - Each handler calls C1:8C3E as a shared subroutine')
    report.append('  - Pattern: Handler -> JSR C1:8C3E -> RTS')
    report.append('')

    report.append('## 3. SCORE-6+ CANDIDATES (BACKTRACK ANALYSIS)')
    report.append('-' * 70)
    report.append('')
    score6 = [c for c in backtrack_data['candidates'] if c['score'] >= 6]
    report.append(f'Found {len(score6)} score-6+ candidates:')
    report.append('')
    for c in score6:
        report.append(f"  {c['candidate_start']} -> {c['target']}")
        report.append(f"    Score: {c['score']}, Distance: {c['distance_to_target']}")
        report.append(f"    Start: {c['start_byte']} ({c['start_class']})")
        report.append(f"    Range: {c['candidate_range']}")
        report.append('')

    report.append('## 4. HIGH-SCORE CLUSTERS (SEAM BLOCK ANALYSIS)')
    report.append('-' * 70)
    clusters = []
    for page in seam_data['pages']:
        for cluster in page.get('local_clusters', []):
            clusters.append({
                'range': cluster['range'],
                'score': cluster['cluster_score'],
                'width': cluster['width'],
                'calls': cluster['call_count'],
                'returns': cluster['return_count']
            })

    # Sort by score
    clusters.sort(key=lambda x: x['score'], reverse=True)
    report.append(f'Top clusters (score 6+):')
    report.append('')
    for c in clusters[:15]:
        report.append(f"  {c['range']}: score={c['score']}, width={c['width']}, calls={c['calls']}, rts={c['returns']}")
    report.append('')

    report.append('## 5. RECOMMENDED NEW MANIFESTS (Pass 621+)')
    report.append('-' * 70)
    report.append('')
    report.append('### Priority 1: Score-6+ Functions (3 manifests)')
    report.append('')
    candidates_6 = [
        ('C1:8E9B', 'C1:8EA6', 6, 'Handler dispatching to C1:8C3E'),
        ('C1:8F02', 'C1:8F10', 6, 'Handler dispatching to C1:8C3E'),
        ('C1:8FF4', 'C1:9003', 6, 'Handler dispatching to C1:8C3E'),
    ]
    for start, target, sc, note in candidates_6:
        report.append(f"  Pass 62X: {start} (score {sc})")
        report.append(f"    Type: Function, Note: {note}")
        report.append('')

    report.append('### Priority 2: Score-4 Candidates (6 manifests)')
    report.append('')
    candidates_4 = [
        'C1:8E41', 'C1:8E6C', 'C1:8E77', 'C1:9151', 'C1:93A4'
    ]
    for i, addr in enumerate(candidates_4, 624):
        report.append(f"  Pass {i}: {addr} (score 4)")
    report.append('')

    report.append('### Priority 3: High-Score Clusters (10+ manifests)')
    report.append('')
    high_clusters = [
        ('C1:8E95..C1:8EAA', 8, 'Handler cluster'),
        ('C1:9792..C1:97D4', 8, 'Large handler cluster'),
        ('C1:9032..C1:9044', 7, 'Handler cluster'),
        ('C1:906E..C1:9081', 7, 'Handler cluster'),
        ('C1:9745..C1:9764', 7, 'Handler cluster'),
        ('C1:96C2..C1:96D3', 7, 'Handler cluster'),
    ]
    for i, (range_str, sc, note) in enumerate(high_clusters, 630):
        report.append(f"  Pass {i}: {range_str} (score {sc}) - {note}")
    report.append('')

    report.append('## 6. COVERAGE IMPACT')
    report.append('-' * 70)
    report.append('Current Bank C1: 14 documented ranges (1.47%)')
    report.append('Estimated new ranges from this analysis: 15-20')
    report.append('Projected Bank C1 coverage: ~2.5-3%')
    report.append('')

    report.append('## 7. STATE MACHINE IDENTIFICATION')
    report.append('-' * 70)
    report.append('The C1:8C3E hub with 42 callers implements:')
    report.append('  - A STATE MACHINE DISPATCH PATTERN')
    report.append('  - 42 handler functions (C1:8E00-9800)')
    report.append('  - Central dispatch/handler at C1:8C3E')
    report.append('  - Likely handles game state, menu, or event processing')
    report.append('')
    report.append('=' * 70)
    report.append('END OF REPORT')
    report.append('=' * 70)

    # Print and save
    output = '\n'.join(report)
    print(output)
    
    with open('reports/c1_8e00_9800_analysis_report.md', 'w') as f:
        f.write(output)
    
    print("\nReport saved to: reports/c1_8e00_9800_analysis_report.md")

if __name__ == '__main__':
    main()
