#!/usr/bin/env python3
"""Analyze C4 candidates for Session 30"""

import json
import os

def main():
    # Read raw bytes and decode
    with open('c4_backtrack_full.json', 'rb') as f:
        raw = f.read()

    # Skip BOM if present
    if raw[:3] == b'\xef\xbb\xbf':
        raw = raw[3:]
    elif raw[:2] == b'\xff\xfe':
        raw = raw[2:].decode('utf-16-le')
    else:
        raw = raw.decode('utf-8', errors='ignore')

    if isinstance(raw, bytes):
        content = raw.decode('utf-8', errors='ignore')
    else:
        content = raw

    data = json.loads(content)

    # Get all candidates
    candidates = data.get('candidates', [])
    print(f'Total candidates: {len(candidates)}')

    # Filter by score
    score_8 = [c for c in candidates if c.get('score', 0) >= 8]
    score_7 = [c for c in candidates if c.get('score', 0) == 7]
    score_6 = [c for c in candidates if c.get('score', 0) == 6]
    score_5 = [c for c in candidates if c.get('score', 0) == 5]

    print(f'\nScore 8+: {len(score_8)}')
    print(f'Score 7: {len(score_7)}')
    print(f'Score 6: {len(score_6)}')
    print(f'Score 5: {len(score_5)}')

    # Get already documented addresses
    documented = set()
    for root, dirs, files in os.walk('passes'):
        for fname in files:
            if fname.startswith('pass') and fname.endswith('.json'):
                path = os.path.join(root, fname)
                try:
                    with open(path) as f:
                        m = json.load(f)
                        start = m.get('start', '')
                        if start.startswith('C4:'):
                            documented.add(start)
                except:
                    pass

    print(f'\nAlready documented: {len(documented)}')

    # Filter out already documented
    def not_documented(c):
        return c.get('candidate_start') not in documented

    new_8 = [c for c in score_8 if not_documented(c)]
    new_7 = [c for c in score_7 if not_documented(c)]
    new_6 = [c for c in score_6 if not_documented(c)]
    new_5 = [c for c in score_5 if not_documented(c)]

    print(f'\nNEW Score 8+: {len(new_8)}')
    print(f'NEW Score 7: {len(new_7)}')
    print(f'NEW Score 6: {len(new_6)}')
    print(f'NEW Score 5: {len(new_5)}')

    # Show top candidates by region
    print('\n=== Top Score 8+ Candidates ===')
    for c in new_8:
        addr = c.get('candidate_start', '')
        target = c.get('target', '')
        score = c.get('score', 0)
        start_byte = c.get('start_byte', '')
        print(f'  {addr} -> {target} (score={score}, byte={start_byte})')

    print('\n=== Top Score 7 Candidates ===')
    for c in new_7[:30]:
        addr = c.get('candidate_start', '')
        target = c.get('target', '')
        start_byte = c.get('start_byte', '')
        print(f'  {addr} -> {target} (byte={start_byte})')

    print('\n=== Top Score 6 Candidates (first 30) ===')
    for c in new_6[:30]:
        addr = c.get('candidate_start', '')
        target = c.get('target', '')
        start_byte = c.get('start_byte', '')
        print(f'  {addr} -> {target} (byte={start_byte})')

    # Save new candidates for later use
    new_candidates = new_8 + new_7 + new_6[:50]
    with open('c4_session30_candidates.json', 'w') as f:
        json.dump(new_candidates, f, indent=2)
    print(f'\nSaved {len(new_candidates)} new candidates to c4_session30_candidates.json')

if __name__ == '__main__':
    main()
