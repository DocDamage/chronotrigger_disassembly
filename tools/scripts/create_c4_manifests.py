#!/usr/bin/env python3
"""Create manifest files for C4:0000-1000 score-6+ candidates."""
import json
import os
import sys

def main():
    # Create manifests for score-6+ candidates
    manifests = [
        {
            'pass_number': 641,
            'closed_ranges': [{'range': 'C4:01D2..C4:01EB', 'kind': 'owner', 'label': 'ct_c4_01d2_jsr_handler', 'confidence': 'high'}],
            'promotion_reason': 'Score-6 cluster, JSR prologue. Called from C4:0480, C4:C84C. Target C4:01D3.'
        },
        {
            'pass_number': 642,
            'closed_ranges': [{'range': 'C4:02BB..C4:02D8', 'kind': 'owner', 'label': 'ct_c4_02bb_phb_handler', 'confidence': 'high'}],
            'promotion_reason': 'Score-6 cluster, PHB prologue (data bank push). Bank register management.'
        },
        {
            'pass_number': 643,
            'closed_ranges': [{'range': 'C4:0347..C4:0369', 'kind': 'owner', 'label': 'ct_c4_0347_dual_target', 'confidence': 'high'}],
            'promotion_reason': 'Score-6 cluster, JSR prologue. Dual-target: C4:0351, C4:0355. Multi-entry function.'
        },
        {
            'pass_number': 644,
            'closed_ranges': [{'range': 'C4:049D..C4:04BC', 'kind': 'owner', 'label': 'ct_c4_049d_ldy_init', 'confidence': 'high'}],
            'promotion_reason': 'Score-6 cluster, LDY# prologue. Initialization with index register setup.'
        },
        {
            'pass_number': 645,
            'closed_ranges': [{'range': 'C4:0617..C4:0637', 'kind': 'owner', 'label': 'ct_c4_0617_jsr_util', 'confidence': 'high'}],
            'promotion_reason': 'Score-6 cluster, JSR prologue. Target C4:061F. Utility function.'
        },
        {
            'pass_number': 646,
            'closed_ranges': [{'range': 'C4:0810..C4:082A', 'kind': 'owner', 'label': 'ct_c4_0810_jsr_dispatch', 'confidence': 'high'}],
            'promotion_reason': 'Score-6 cluster, JSR prologue. Dual-target: C4:0812, C4:0818. Dispatcher pattern.'
        },
        {
            'pass_number': 647,
            'closed_ranges': [{'range': 'C4:085E..C4:0877', 'kind': 'owner', 'label': 'ct_c4_085e_ldy_handler', 'confidence': 'high'}],
            'promotion_reason': 'Score-6 cluster, LDY# prologue. Target C4:085F. Index-based operation.'
        },
        {
            'pass_number': 648,
            'closed_ranges': [{'range': 'C4:08B7..C4:08D5', 'kind': 'owner', 'label': 'ct_c4_08b7_jsr_routine', 'confidence': 'high'}],
            'promotion_reason': 'Score-6 cluster, JSR prologue. Dual-target: C4:08BD, C4:08C1. Branching function.'
        },
        {
            'pass_number': 649,
            'closed_ranges': [{'range': 'C4:0A54..C4:0A73', 'kind': 'owner', 'label': 'ct_c4_0a54_jsr_entry', 'confidence': 'high'}],
            'promotion_reason': 'Score-6 cluster, JSR prologue. Target C4:0A5B. Entry point handler.'
        },
        {
            'pass_number': 650,
            'closed_ranges': [{'range': 'C4:0A99..C4:0AB8', 'kind': 'owner', 'label': 'ct_c4_0a99_jsl_longcall', 'confidence': 'high'}],
            'promotion_reason': 'Score-6 cluster, JSL prologue. Long call cross-bank entry point. Target C4:0AA0.'
        },
        {
            'pass_number': 651,
            'closed_ranges': [{'range': 'C4:0ADB..C4:0AF8', 'kind': 'owner', 'label': 'ct_c4_0adb_jsl_crossbank', 'confidence': 'high'}],
            'promotion_reason': 'Score-6 cluster, JSL prologue. Cross-bank long call handler. Target C4:0AE0.'
        },
        {
            'pass_number': 652,
            'closed_ranges': [{'range': 'C4:0E8C..C4:0EB8', 'kind': 'owner', 'label': 'ct_c4_0e8c_php_stackframe', 'confidence': 'high'}],
            'promotion_reason': 'Score-6 cluster, PHP prologue. Stack frame setup with processor status save. Target C4:0EA0.'
        },
        # Additional clusters
        {
            'pass_number': 653,
            'closed_ranges': [{'range': 'C4:0E7A..C4:0E96', 'kind': 'owner', 'label': 'ct_c4_0e7a_cluster7', 'confidence': 'medium'}],
            'promotion_reason': 'Score-7 cluster. Width 29, 1 call, 3 returns. High-confidence code island.'
        },
        {
            'pass_number': 654,
            'closed_ranges': [{'range': 'C4:08FA..C4:0906', 'kind': 'owner', 'label': 'ct_c4_08fa_cluster6', 'confidence': 'medium'}],
            'promotion_reason': 'Score-6 cluster. Width 13, 1 call, 3 returns. Nested function cluster.'
        },
        {
            'pass_number': 655,
            'closed_ranges': [{'range': 'C4:0AFE..C4:0B12', 'kind': 'owner', 'label': 'ct_c4_0afe_cluster5', 'confidence': 'medium'}],
            'promotion_reason': 'Score-5 cluster. Width 21, 2 calls, 2 branches. Complex control flow.'
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
    return 0

if __name__ == '__main__':
    sys.exit(main())
