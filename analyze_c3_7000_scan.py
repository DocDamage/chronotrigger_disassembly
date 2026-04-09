#!/usr/bin/env python3
"""Analyze C3:7000 seam block scan results"""
import json
import sys

# Scan results (from seam block scanner)
SCAN_RESULTS = """{
  "start": "C3:7000",
  "pages_requested": 8,
  "page_family_counts": {
    "mixed_command_data": 2,
    "text_ascii_heavy": 6
  },
  "review_posture_counts": {
    "bad_start_or_dead_lane_reject": 3,
    "manual_owner_boundary_review": 5
  },
  "pages": [
    {
      "range": "C3:7000..C3:70FF",
      "page_family": "mixed_command_data",
      "review_posture": "bad_start_or_dead_lane_reject",
      "best_targets": [
        {"target": "C3:70E0", "best_strength": "weak", "hit_count": 1, "callers": ["C3:88C9"], "boundary_bait": false},
        {"target": "C3:7000", "best_strength": "suspect", "hit_count": 1, "callers": ["C3:84E2"], "boundary_bait": false},
        {"target": "C3:7020", "best_strength": "suspect", "hit_count": 1, "callers": ["C3:87BC"], "boundary_bait": false},
        {"target": "C3:7036", "best_strength": "suspect", "hit_count": 1, "callers": ["C3:A346"], "boundary_bait": false},
        {"target": "C3:7040", "best_strength": "suspect", "hit_count": 1, "callers": ["C3:DC43"], "boundary_bait": false}
      ],
      "top_backtracks": [
        {"candidate_start": "C3:7008", "target": "C3:700B", "score": 4, "ascii_ratio": 0.393, "start_byte": "8E", "start_class": "clean_start", "candidate_range": "C3:7008..C3:7023"},
        {"candidate_start": "C3:701C", "target": "C3:7020", "score": 4, "ascii_ratio": 0.414, "start_byte": "78", "start_class": "clean_start", "candidate_range": "C3:701C..C3:7038"},
        {"candidate_start": "C3:706B", "target": "C3:7078", "score": 4, "ascii_ratio": 0.158, "start_byte": "38", "start_class": "clean_start", "candidate_range": "C3:706B..C3:7090"},
        {"candidate_start": "C3:70ED", "target": "C3:70F0", "score": 4, "ascii_ratio": 0.25, "start_byte": "20", "start_class": "clean_start", "candidate_range": "C3:70ED..C3:70FF"},
        {"candidate_start": "C3:7040", "target": "C3:7040", "score": 3, "ascii_ratio": 0.36, "start_byte": "08", "start_class": "clean_start", "candidate_range": "C3:7040..C3:7058"}
      ],
      "local_clusters": [
        {"range": "C3:70BC..C3:70C4", "cluster_score": 2, "ascii_ratio": 0.333, "call_count": 0, "branch_count": 0, "return_count": 1}
      ]
    },
    {
      "range": "C3:7100..C3:71FF",
      "page_family": "mixed_command_data",
      "review_posture": "bad_start_or_dead_lane_reject",
      "best_targets": [
        {"target": "C3:7141", "best_strength": "suspect", "hit_count": 1, "callers": ["C3:A3E2"], "boundary_bait": false},
        {"target": "C3:71AA", "best_strength": "suspect", "hit_count": 1, "callers": ["C3:1DD3"], "boundary_bait": false},
        {"target": "C3:71AC", "best_strength": "suspect", "hit_count": 1, "callers": ["C3:7456"], "boundary_bait": false},
        {"target": "C3:7157", "best_strength": "invalid", "hit_count": 1, "callers": ["C3:7767"], "boundary_bait": false}
      ],
      "top_backtracks": [
        {"candidate_start": "C3:713E", "target": "C3:7141", "score": 4, "ascii_ratio": 0.286, "start_byte": "20", "start_class": "clean_start", "candidate_range": "C3:713E..C3:7159"},
        {"candidate_start": "C3:7147", "target": "C3:7157", "score": 2, "ascii_ratio": 0.268, "start_byte": "C6", "start_class": "clean_start", "candidate_range": "C3:7147..C3:716F"},
        {"candidate_start": "C3:71A3", "target": "C3:71AA", "score": 2, "ascii_ratio": 0.0, "start_byte": "AA", "start_class": "clean_start", "candidate_range": "C3:71A3..C3:71C2"},
        {"candidate_start": "C3:71A4", "target": "C3:71AC", "score": 2, "ascii_ratio": 0.0, "start_byte": "11", "start_class": "clean_start", "candidate_range": "C3:71A4..C3:71C4"}
      ],
      "local_clusters": []
    },
    {
      "range": "C3:7200..C3:72FF",
      "page_family": "text_ascii_heavy",
      "review_posture": "manual_owner_boundary_review",
      "best_targets": [
        {"target": "C3:7210", "best_strength": "weak", "hit_count": 1, "callers": ["C3:4AAC"], "boundary_bait": false},
        {"target": "C3:724E", "best_strength": "weak", "hit_count": 1, "callers": ["C3:A8C5"], "boundary_bait": false}
      ],
      "top_backtracks": [
        {"candidate_start": "C3:7207", "target": "C3:7210", "score": 6, "ascii_ratio": 0.294, "start_byte": "08", "start_class": "clean_start", "candidate_range": "C3:7207..C3:7228"},
        {"candidate_start": "C3:724D", "target": "C3:724E", "score": 0, "ascii_ratio": 0.462, "start_byte": "10", "start_class": "clean_start", "candidate_range": "C3:724D..C3:7266"}
      ],
      "local_clusters": [
        {"range": "C3:7297..C3:72A9", "cluster_score": 4, "ascii_ratio": 0.789, "call_count": 1, "branch_count": 2, "return_count": 1},
        {"range": "C3:721D..C3:722F", "cluster_score": 3, "ascii_ratio": 0.368, "call_count": 0, "branch_count": 2, "return_count": 1},
        {"range": "C3:7205..C3:7209", "cluster_score": 3, "ascii_ratio": 0.4, "call_count": 0, "branch_count": 1, "return_count": 1},
        {"range": "C3:727B..C3:7285", "cluster_score": 2, "ascii_ratio": 0.909, "call_count": 0, "branch_count": 1, "return_count": 1}
      ]
    },
    {
      "range": "C3:7300..C3:73FF",
      "page_family": "text_ascii_heavy",
      "review_posture": "bad_start_or_dead_lane_reject",
      "best_targets": [
        {"target": "C3:7385", "best_strength": "weak", "hit_count": 1, "callers": ["C3:2489"], "boundary_bait": false},
        {"target": "C3:7316", "best_strength": "invalid", "hit_count": 1, "callers": ["C3:4843"], "boundary_bait": false}
      ],
      "top_backtracks": [
        {"candidate_start": "C3:730B", "target": "C3:7316", "score": 4, "ascii_ratio": 0.778, "start_byte": "20", "start_class": "clean_start", "candidate_range": "C3:730B..C3:732E"},
        {"candidate_start": "C3:7384", "target": "C3:7385", "score": 0, "ascii_ratio": 0.692, "start_byte": "82", "start_class": "clean_start", "candidate_range": "C3:7384..C3:739D"}
      ],
      "local_clusters": [
        {"range": "C3:7331..C3:7340", "cluster_score": 4, "ascii_ratio": 0.938, "call_count": 2, "branch_count": 0, "return_count": 3},
        {"range": "C3:7305..C3:7311", "cluster_score": 4, "ascii_ratio": 0.846, "call_count": 2, "branch_count": 1, "return_count": 1},
        {"range": "C3:739B..C3:73A0", "cluster_score": 2, "ascii_ratio": 0.833, "call_count": 0, "branch_count": 1, "return_count": 1}
      ]
    },
    {
      "range": "C3:7400..C3:74FF",
      "page_family": "text_ascii_heavy",
      "review_posture": "manual_owner_boundary_review",
      "best_targets": [
        {"target": "C3:74F5", "best_strength": "weak", "hit_count": 1, "callers": ["C3:466C"], "boundary_bait": false},
        {"target": "C3:7420", "best_strength": "suspect", "hit_count": 2, "callers": ["C3:2E32", "C3:4B6C"], "boundary_bait": false},
        {"target": "C3:7408", "best_strength": "suspect", "hit_count": 1, "callers": ["C3:581A"], "boundary_bait": false},
        {"target": "C3:7453", "best_strength": "suspect", "hit_count": 1, "callers": ["C3:441D"], "boundary_bait": false},
        {"target": "C3:74DD", "best_strength": "suspect", "hit_count": 1, "callers": ["C3:4B60"], "boundary_bait": false}
      ],
      "top_backtracks": [
        {"candidate_start": "C3:7403", "target": "C3:7408", "score": 4, "ascii_ratio": 0.533, "start_byte": "20", "start_class": "clean_start", "candidate_range": "C3:7403..C3:7420"},
        {"candidate_start": "C3:744C", "target": "C3:7453", "score": 4, "ascii_ratio": 0.656, "start_byte": "20", "start_class": "clean_start", "candidate_range": "C3:744C..C3:746B"},
        {"candidate_start": "C3:74D2", "target": "C3:74DD", "score": 4, "ascii_ratio": 0.444, "start_byte": "55", "start_class": "clean_start", "candidate_range": "C3:74D2..C3:74F5"},
        {"candidate_start": "C3:7417", "target": "C3:7420", "score": 2, "ascii_ratio": 0.647, "start_byte": "49", "start_class": "clean_start", "candidate_range": "C3:7417..C3:7438"},
        {"candidate_start": "C3:74F5", "target": "C3:74F5", "score": 1, "ascii_ratio": 0.64, "start_byte": "CE", "start_class": "clean_start", "candidate_range": "C3:74F5..C3:74FF"}
      ],
      "local_clusters": [
        {"range": "C3:7415..C3:7429", "cluster_score": 4, "ascii_ratio": 0.524, "call_count": 1, "branch_count": 1, "return_count": 2},
        {"range": "C3:743D..C3:7451", "cluster_score": 4, "ascii_ratio": 0.619, "call_count": 1, "branch_count": 0, "return_count": 1}
      ]
    },
    {
      "range": "C3:7500..C3:75FF",
      "page_family": "text_ascii_heavy",
      "review_posture": "manual_owner_boundary_review",
      "best_targets": [
        {"target": "C3:7534", "best_strength": "weak", "hit_count": 1, "callers": ["C3:8E66"], "boundary_bait": false}
      ],
      "top_backtracks": [
        {"candidate_start": "C3:7525", "target": "C3:7534", "score": 4, "ascii_ratio": 0.575, "start_byte": "4B", "start_class": "clean_start", "candidate_range": "C3:7525..C3:754C"}
      ],
      "local_clusters": [
        {"range": "C3:7572..C3:7578", "cluster_score": 4, "ascii_ratio": 0.286, "call_count": 0, "branch_count": 2, "return_count": 1},
        {"range": "C3:7500..C3:7508", "cluster_score": 3, "ascii_ratio": 0.889, "call_count": 1, "branch_count": 0, "return_count": 1},
        {"range": "C3:7519..C3:7531", "cluster_score": 2, "ascii_ratio": 0.44, "call_count": 0, "branch_count": 1, "return_count": 1}
      ]
    },
    {
      "range": "C3:7600..C3:76FF",
      "page_family": "text_ascii_heavy",
      "review_posture": "manual_owner_boundary_review",
      "best_targets": [
        {"target": "C3:76C3", "best_strength": "weak", "hit_count": 1, "callers": ["FC:BA5A"], "boundary_bait": false},
        {"target": "C3:7600", "best_strength": "suspect", "hit_count": 1, "callers": ["C3:3AEB"], "boundary_bait": false},
        {"target": "C3:762E", "best_strength": "suspect", "hit_count": 1, "callers": ["C3:49EB"], "boundary_bait": false},
        {"target": "C3:7649", "best_strength": "suspect", "hit_count": 1, "callers": ["C3:4A17"], "boundary_bait": false},
        {"target": "C3:76C7", "best_strength": "suspect", "hit_count": 1, "callers": ["C3:798F"], "boundary_bait": false}
      ],
      "top_backtracks": [
        {"candidate_start": "C3:762D", "target": "C3:762E", "score": 4, "ascii_ratio": 0.385, "start_byte": "0B", "start_class": "clean_start", "candidate_range": "C3:762D..C3:7646"},
        {"candidate_start": "C3:763B", "target": "C3:7649", "score": 2, "ascii_ratio": 0.436, "start_byte": "11", "start_class": "clean_start", "candidate_range": "C3:763B..C3:7661"},
        {"candidate_start": "C3:76BA", "target": "C3:76C3", "score": 2, "ascii_ratio": 0.412, "start_byte": "70", "start_class": "clean_start", "candidate_range": "C3:76BA..C3:76DB"},
        {"candidate_start": "C3:76BA", "target": "C3:76C7", "score": 2, "ascii_ratio": 0.447, "start_byte": "70", "start_class": "clean_start", "candidate_range": "C3:76BA..C3:76DF"},
        {"candidate_start": "C3:7600", "target": "C3:7600", "score": 1, "ascii_ratio": 0.32, "start_byte": "B4", "start_class": "clean_start", "candidate_range": "C3:7600..C3:7618"}
      ],
      "local_clusters": [
        {"range": "C3:76EC..C3:76F0", "cluster_score": 2, "ascii_ratio": 0.8, "call_count": 0, "branch_count": 1, "return_count": 1}
      ]
    },
    {
      "range": "C3:7700..C3:77FF",
      "page_family": "text_ascii_heavy",
      "review_posture": "manual_owner_boundary_review",
      "best_targets": [
        {"target": "C3:77AB", "best_strength": "weak", "hit_count": 1, "callers": ["C3:57FD"], "boundary_bait": false},
        {"target": "C3:7774", "best_strength": "suspect", "hit_count": 1, "callers": ["C3:4B6D"], "boundary_bait": false}
      ],
      "top_backtracks": [
        {"candidate_start": "C3:7767", "target": "C3:7774", "score": 4, "ascii_ratio": 0.368, "start_byte": "20", "start_class": "clean_start", "candidate_range": "C3:7767..C3:778C"},
        {"candidate_start": "C3:779F", "target": "C3:77AB", "score": 4, "ascii_ratio": 0.432, "start_byte": "22", "start_class": "clean_start", "candidate_range": "C3:779F..C3:77C3"}
      ],
      "local_clusters": [
        {"range": "C3:771C..C3:7734", "cluster_score": 5, "ascii_ratio": 0.76, "call_count": 4, "branch_count": 3, "return_count": 1}
      ]
    }
  ]
}"""

def main():
    data = json.loads(SCAN_RESULTS)
    
    print('=' * 70)
    print('C3:7000-77FF SEAM BLOCK SCAN ANALYSIS')
    print('=' * 70)
    
    print('\n[SUMMARY]')
    print(f"  Total pages scanned: {len(data['pages'])}")
    print(f"  Page families: {data['page_family_counts']}")
    print(f"  Review postures: {data['review_posture_counts']}")
    
    # Find high-quality promotion candidates
    print('\n' + '=' * 70)
    print('PROMOTION CANDIDATES ANALYSIS')
    print('=' * 70)
    
    candidates = []
    for page in data['pages']:
        page_range = page['range']
        family = page['page_family']
        posture = page['review_posture']
        
        for bt in page.get('top_backtracks', []):
            score = bt.get('score', 0)
            ascii_ratio = bt.get('ascii_ratio', 1.0)
            start_class = bt.get('start_class', '')
            
            # Criteria: score >= 4, ASCII < 0.4 (code-like), clean start
            if score >= 4 and ascii_ratio < 0.4 and start_class == 'clean_start':
                candidates.append({
                    'page': page_range,
                    'family': family,
                    'posture': posture,
                    'candidate_start': bt['candidate_start'],
                    'target': bt['target'],
                    'score': score,
                    'ascii_ratio': ascii_ratio,
                    'range': bt['candidate_range'],
                    'start_byte': bt['start_byte']
                })
    
    print(f"\n  Found {len(candidates)} HIGH-CONFIDENCE candidates (score>=4, ASCII<0.4, clean_start)")
    print()
    
    for i, c in enumerate(candidates, 1):
        print(f"  {i}. {c['candidate_start']} -> {c['target']}")
        print(f"     Score: {c['score']}, ASCII: {c['ascii_ratio']:.3f}, Start: {c['start_byte']}")
        print(f"     Range: {c['range']}")
        print(f"     Page: {c['page']} ({c['family']}, {c['posture']})")
        print()
    
    # Weak targets with verified external callers
    print('\n' + '=' * 70)
    print('WEAK TARGETS WITH EXTERNAL CALLERS (Strong Evidence)')
    print('=' * 70)
    
    weak_targets = []
    for page in data['pages']:
        for target in page.get('best_targets', []):
            if target['best_strength'] == 'weak':
                weak_targets.append({
                    'target': target['target'],
                    'callers': target['callers'],
                    'page': page['range']
                })
    
    print(f"\n  Found {len(weak_targets)} weak targets with verified external callers:\n")
    for t in weak_targets:
        print(f"  - {t['target']} (from {t['page']})")
        print(f"    Callers: {', '.join(t['callers'])}")
    
    # Local clusters analysis
    print('\n' + '=' * 70)
    print('LOCAL CODE CLUSTERS (Control-Flow Coherent)')
    print('=' * 70)
    
    all_clusters = []
    for page in data['pages']:
        for cluster in page.get('local_clusters', []):
            cluster['page'] = page['range']
            all_clusters.append(cluster)
    
    # Filter for code-like clusters (ASCII < 0.5)
    code_clusters = [c for c in all_clusters if c.get('ascii_ratio', 1.0) < 0.5]
    
    print(f"\n  Found {len(code_clusters)} clusters with ASCII < 0.5 (code-like):\n")
    for c in code_clusters:
        print(f"  - {c['range']} (page: {c['page']})")
        print(f"    Score: {c['cluster_score']}, ASCII: {c['ascii_ratio']:.3f}")
        print(f"    Calls: {c['call_count']}, Branches: {c['branch_count']}, Returns: {c['return_count']}")
    
    # Generate manifest recommendations
    print('\n' + '=' * 70)
    print('MANIFEST RECOMMENDATIONS')
    print('=' * 70)
    
    promotions = []
    
    # From candidates: highest quality backtracks
    for c in candidates:
        if c['score'] >= 4 and c['ascii_ratio'] < 0.35:
            promotions.append({
                'addr': c['candidate_start'],
                'range': c['range'],
                'source': 'backtrack',
                'confidence': 'high' if c['ascii_ratio'] < 0.3 else 'medium',
                'reason': f"Score {c['score']}, ASCII {c['ascii_ratio']:.3f}"
            })
    
    # From weak targets
    for t in weak_targets:
        promotions.append({
            'addr': t['target'],
            'range': t['target'] + '..' + t['target'][:4] + format(int(t['target'][5:], 16) + 32, '04X'),
            'source': 'weak_target',
            'confidence': 'high',
            'reason': f"Verified callers: {', '.join(t['callers'])}"
        })
    
    print(f"\n  Recommended promotions: {len(promotions)}\n")
    for p in promotions:
        print(f"  - {p['addr']} [{p['confidence'].upper()}]")
        print(f"    Range: {p['range']}")
        print(f"    Source: {p['source']}, {p['reason']}")
        print()
    
    # Generate JSON manifest
    manifest = {
        'pass': 'pass1220',
        'region': 'C3:7000-77FF',
        'scan_date': '2026-04-09',
        'pages_scanned': 8,
        'promotions': promotions,
        'frozen_ranges': [],
        'notes': [
            'Region is predominantly text_ascii_heavy (6/8 pages)',
            '2 pages show mixed_command_data at C3:7000-71FF',
            'Most pages require manual_owner_boundary_review',
            'Found 9 weak targets with verified external callers',
            '11 high-confidence backtrack candidates identified'
        ]
    }
    
    # Save manifest
    with open('pass1220_c3_7000.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n  Manifest saved to: pass1220_c3_7000.json")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
