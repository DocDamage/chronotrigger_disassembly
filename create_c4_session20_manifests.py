#!/usr/bin/env python3
"""Create manifest files for Bank C4 Session 20 - highest scoring candidates."""
import json
import os
import sys

def main():
    # Top candidates from Bank C4 scan (Session 20)
    manifests = [
        # C4:4000-8000 region - Score 7 (highest found)
        {
            'pass_number': 1018,
            'closed_ranges': [{'range': 'C4:7730..C4:7748', 'kind': 'owner', 'label': 'ct_c4_7730_score7_handler', 'confidence': 'high'}],
            'promotion_reason': 'Session 20 Bank C4 scan. Score-7 cluster, width 25, 1 call, 6 branches, 3 returns. Mid-bank high-confidence function.'
        },
        {
            'pass_number': 1019,
            'closed_ranges': [{'range': 'C4:5025..C4:5039', 'kind': 'owner', 'label': 'ct_c4_5025_score7_routine', 'confidence': 'high'}],
            'promotion_reason': 'Session 20 Bank C4 scan. Score-7 cluster, width 21, 2 calls, 2 branches, 1 return. Multiple caller function.'
        },
        # C4:0000-4000 region - Score 6
        {
            'pass_number': 1020,
            'closed_ranges': [{'range': 'C4:0E7A..C4:0E92', 'kind': 'owner', 'label': 'ct_c4_0e7a_score6_handler', 'confidence': 'high'}],
            'promotion_reason': 'Session 20 Bank C4 scan. Score-6 cluster, width 25, 1 call, 2 returns. Low-bank entry point.'
        },
        {
            'pass_number': 1021,
            'closed_ranges': [{'range': 'C4:3F45..C4:3F54', 'kind': 'owner', 'label': 'ct_c4_3f45_score6_routine', 'confidence': 'high'}],
            'promotion_reason': 'Session 20 Bank C4 scan. Score-6 cluster, width 16, 1 call, 3 branches, 2 returns. Near page boundary function.'
        },
        # C4:8000-C000 region - Score 6
        {
            'pass_number': 1022,
            'closed_ranges': [{'range': 'C4:9DE6..C4:9DF6', 'kind': 'owner', 'label': 'ct_c4_9de6_score6_handler', 'confidence': 'high'}],
            'promotion_reason': 'Session 20 Bank C4 scan. Score-6 cluster, width 17, 1 call, 1 branch, 1 return. High-bank utility function.'
        },
        # C4:C000-FFFF region - Score 5
        {
            'pass_number': 1023,
            'closed_ranges': [{'range': 'C4:CE33..C4:CE4B', 'kind': 'owner', 'label': 'ct_c4_ce33_score5_handler', 'confidence': 'medium'}],
            'promotion_reason': 'Session 20 Bank C4 scan. Score-5 cluster, width 25, 1 call, 1 branch, 3 returns. Upper-bank function with multiple exits.'
        },
    ]

    # Write manifests
    output_dir = 'passes/new_manifests'
    os.makedirs(output_dir, exist_ok=True)

    for m in manifests:
        filepath = os.path.join(output_dir, f"pass{m['pass_number']}.json")
        with open(filepath, 'w') as f:
            json.dump(m, f, indent=2)
        print(f"Created: {filepath}")

    print(f"\nTotal manifests created: {len(manifests)}")
    print("Session 20 Bank C4 scan complete.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
