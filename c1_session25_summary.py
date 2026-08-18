#!/usr/bin/env python3
"""Comprehensive summary of Bank C1 Session 25 analysis."""

import json
import os

SCAN_FILES = {
    '2000-3000': 'c1_2000_scan.json',
    '3000-4000': 'c1_3000_scan.json',
    '8000-9000': 'c1_8000_scan.json',
    '9000-A000': 'c1_9000_scan.json',
    'A000-B000': 'c1_a000_scan.json',
    'B000-C000': 'c1_b000_scan.json',
    'C000-D000': 'c1_c000_scan.json',
    'D000-E000': 'c1_d000_scan.json',
    'E000-F000': 'c1_e000_scan.json',
    'F000-FFFF': 'c1_f000_scan.json',
}

def main():
    print('=' * 60)
    print('Bank C1 Remaining Regions Analysis - Session 25')
    print('=' * 60)

    total_islands = 0
    total_score6 = 0
    all_score6 = []

    for region, filepath in SCAN_FILES.items():
        if os.path.exists(filepath):
            with open(filepath) as f:
                data = json.load(f)
            islands = data.get('islands', [])
            score6 = [i for i in islands if i['score'] >= 6]
            total_islands += len(islands)
            total_score6 += len(score6)
            all_score6.extend([(region, i) for i in score6])
            print(f'{region}: {len(islands)} islands, {len(score6)} score-6+')
        else:
            print(f'{region}: FILE NOT FOUND')

    print(f'\nTotal: {total_islands} islands, {total_score6} score-6+ candidates')

    # Show top candidates by score
    print('\n### Top Score-7+ Candidates ###')
    score7 = [(r, i) for r, i in all_score6 if i['score'] >= 7]
    score7.sort(key=lambda x: -x[1]['score'])
    for region, i in score7[:20]:
        range_str = i['range']
        print(f'  {range_str} ({region}): score={i["score"]}, calls={i["call_count"]}, branches={i["branch_count"]}')
    
    print(f'\nTotal score-7+ candidates: {len(score7)}')
    
    # Coverage summary
    print('\n### Coverage by Region ###')
    for region, filepath in SCAN_FILES.items():
        if os.path.exists(filepath):
            with open(filepath) as f:
                data = json.load(f)
            islands = data.get('islands', [])
            if islands:
                addrs = [int(i['range'].split('..')[0].split(':')[1], 16) for i in islands]
                min_addr = min(addrs)
                max_addr = max(addrs)
                print(f'  {region}: 0x{min_addr:04X} - 0x{max_addr:04X}')

if __name__ == '__main__':
    main()
