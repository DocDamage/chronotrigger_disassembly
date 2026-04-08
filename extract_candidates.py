#!/usr/bin/env python3
import json
import sys

def extract_high_score_candidates(filepath, min_score=6):
    with open(filepath, 'r', encoding='utf-16') as f:
        data = json.load(f)
    
    print(f"\n=== {data.get('range', 'Unknown')} Score-{min_score}+ Candidates ===")
    
    high_score = []
    if 'owner_backtrack' in data:
        for c in data['owner_backtrack'].get('candidates', []):
            if c.get('score', 0) >= min_score:
                high_score.append(c)
                start_byte = c['start_byte']
                if isinstance(start_byte, int):
                    start_byte_str = f"{start_byte:02X}"
                else:
                    start_byte_str = str(start_byte)
                print(f"  {c['target']} -> candidate_start={c['candidate_start']} score={c['score']} distance={c['distance_to_target']} start={start_byte_str}")
    
    print(f"\nFound {len(high_score)} candidates with score >= {min_score}")
    print(f"Page Family: {data.get('page_family', {}).get('page_family', 'N/A')}")
    print(f"Review Posture: {data.get('review_posture', 'N/A')}")
    
    return high_score

if __name__ == "__main__":
    files = [
        'reports/c3_2900_3058_flow.json',
        'reports/c3_30b1_34ff_flow.json',
        'reports/c3_3761_3c7f_flow.json'
    ]
    
    all_candidates = []
    for f in files:
        try:
            candidates = extract_high_score_candidates(f)
            all_candidates.extend(candidates)
        except Exception as e:
            print(f"Error processing {f}: {e}")
    
    print(f"\n\n=== TOTAL: {len(all_candidates)} high-score candidates across all gaps ===")
