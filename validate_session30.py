#!/usr/bin/env python3
"""Validate Session 30 manifests for Bank C0"""

import json
import os
import sys

def main():
    manifests = []
    manifest_dir = 'labels/c0_session30'
    
    if not os.path.exists(manifest_dir):
        print(f"ERROR: Directory {manifest_dir} does not exist")
        return 1
    
    for f in os.listdir(manifest_dir):
        if f.endswith('.json'):
            with open(f'{manifest_dir}/{f}', 'r') as fp:
                try:
                    m = json.load(fp)
                    manifests.append(m)
                except json.JSONDecodeError as e:
                    print(f"ERROR: Invalid JSON in {f}: {e}")
                    return 1

    # Sort by pass number
    manifests.sort(key=lambda x: x['pass'])

    print('=' * 70)
    print('SESSION 30 MANIFEST VALIDATION REPORT')
    print('=' * 70)
    print(f'\nTotal Manifests Created: {len(manifests)}')
    print()

    # Validate each manifest
    errors = []
    warnings = []
    total_bytes = 0

    for m in manifests:
        # Check required fields
        required = ['pass', 'label', 'address', 'snes_address', 'score', 'type', 'status', 'session']
        for r in required:
            if r not in m:
                errors.append(f"{m.get('label', 'unknown')}: Missing required field '{r}'")
        
        # Check score range
        if 'score' in m and not (6 <= m['score'] <= 10):
            warnings.append(f"{m.get('label', 'unknown')}: Score {m['score']} outside normal range")
        
        # Check session
        if 'session' in m and m['session'] != 30:
            warnings.append(f"{m.get('label', 'unknown')}: Session should be 30")
        
        # Accumulate size
        total_bytes += m.get('size', 30)

    print(f'Validation Results:')
    print(f'  - Errors: {len(errors)}')
    print(f'  - Warnings: {len(warnings)}')
    print(f'  - Total Estimated Bytes: {total_bytes}')
    print()

    if errors:
        print('ERRORS:')
        for e in errors:
            print(f'  ! {e}')
        print()

    if warnings:
        print('WARNINGS:')
        for w in warnings:
            print(f'  * {w}')
        print()

    # Summary table
    print('=' * 70)
    print('MANIFEST SUMMARY')
    print('=' * 70)
    print(f'{"Pass":<6} {"Address":<12} {"Score":<6} {"Size":<6} {"Label":<40}')
    print('-' * 70)
    for m in manifests:
        print(f"{m['pass']:<6} {m['address']:<12} {m['score']:<6} {m.get('size', 30):<6} {m['label']:<40}")

    print()
    print('=' * 70)
    print('COVERAGE IMPACT ESTIMATE')
    print('=' * 70)
    current_coverage = 23.8
    current_bytes = 15571
    new_bytes = total_bytes
    new_total = current_bytes + new_bytes
    new_coverage = (new_total / 65536) * 100
    improvement = new_coverage - current_coverage

    print(f'  Current Coverage: {current_coverage:.1f}% ({current_bytes} bytes)')
    print(f'  New Bytes Added:  {new_bytes} bytes')
    print(f'  Projected Total:  {new_coverage:.2f}% ({new_total} bytes)')
    print(f'  Improvement:      +{improvement:.2f}%')
    print()

    # Group by region
    by_region = {}
    for m in manifests:
        r = m.get('region', 'unknown')
        if r not in by_region:
            by_region[r] = []
        by_region[r].append(m)

    print('=' * 70)
    print('DISTRIBUTION BY REGION')
    print('=' * 70)
    for region, items in sorted(by_region.items()):
        print(f'  {region}: {len(items)} manifests')
    
    print()
    print('=' * 70)
    print('DISCOVERIES & HIGHLIGHTS')
    print('=' * 70)
    
    # Find score 7+ manifests
    high_score = [m for m in manifests if m['score'] >= 7]
    print(f'\nHigh-Score Functions (Score 7+): {len(high_score)}')
    for m in high_score:
        print(f"  - {m['address']}: {m['label']} (score {m['score']})")
    
    # Find audio-related functions
    audio_funcs = [m for m in manifests if m.get('features', {}).get('category') == 'audio']
    print(f'\nAudio System Functions: {len(audio_funcs)}')
    for m in audio_funcs:
        print(f"  - {m['address']}: {m['label']}")
    
    print()
    return 0 if len(errors) == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
