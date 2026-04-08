#!/usr/bin/env python3
"""Create manifest files for C4:C000-CFFF score-6+ candidates."""
import json
import os
import sys

def main():
    # New recommended manifests based on analysis
    new_manifests = [
        {
            'pass_number': 677,
            'closed_ranges': [{'range': 'C4:C0DF..C4:C0F8', 'kind': 'owner', 'label': 'ct_c4_c0df_php_stackframe', 'confidence': 'high'}],
            'promotion_reason': 'Score-6 candidate, PHP prologue (08). Stack frame setup. Caller from C4:16FA (weak anchor).'
        },
        {
            'pass_number': 678,
            'closed_ranges': [{'range': 'C4:C600..C4:C62A', 'kind': 'owner', 'label': 'ct_c4_c600_handler', 'confidence': 'medium'}],
            'promotion_reason': 'Score-6 local cluster, width 43. 1 call, 4 branches. Code island.'
        },
        {
            'pass_number': 679,
            'closed_ranges': [{'range': 'C4:C771..C4:C77C', 'kind': 'owner', 'label': 'ct_c4_c771_handler', 'confidence': 'medium'}],
            'promotion_reason': 'Score-6 local cluster, width 12. 1 call, 1 branch. Small utility function.'
        },
        {
            'pass_number': 680,
            'closed_ranges': [{'range': 'C4:C831..C4:C849', 'kind': 'owner', 'label': 'ct_c4_c831_handler', 'confidence': 'medium'}],
            'promotion_reason': 'Score-5 candidate (borderline). Clean start (08 PHP). Monitor for promotion.'
        },
    ]

    # Write manifests
    output_dir = 'passes/new_manifests'
    os.makedirs(output_dir, exist_ok=True)

    for m in new_manifests:
        filepath = os.path.join(output_dir, f"pass{m['pass_number']}.json")
        with open(filepath, 'w') as f:
            json.dump(m, f, indent=2)
        print(f"Created: {filepath}")

    print(f"\nTotal new manifests: {len(new_manifests)}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
