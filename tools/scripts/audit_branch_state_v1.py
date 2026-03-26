#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from snes_utils import iter_manifest_paths


def main() -> int:
    parser = argparse.ArgumentParser(description='Audit branch state against pass manifests and reports')
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--bank-progress', default='tools/config/bank_c3_progress.json')
    parser.add_argument('--generated-progress', default='tools/config/bank_c3_progress.generated.json')
    args = parser.parse_args()

    manifest_passes = []
    latest_seam = None
    for path in iter_manifest_paths(args.manifests_dir):
        data = json.loads(Path(path).read_text(encoding='utf-8'))
        manifest_passes.append(int(data['pass_number']))
        latest_seam = data.get('live_seam_after_pass', latest_seam)

    issues = []
    if not manifest_passes:
        issues.append('no manifests found')
    else:
        expected = list(range(min(manifest_passes), max(manifest_passes) + 1))
        missing = sorted(set(expected) - set(manifest_passes))
        if missing:
            issues.append(f'missing manifest pass numbers: {missing}')

    static_progress = Path(args.bank_progress)
    generated_progress = Path(args.generated_progress)
    if static_progress.exists() and generated_progress.exists():
        gen_data = json.loads(generated_progress.read_text(encoding='utf-8'))
        if gen_data.get('latest_live_seam') and latest_seam and gen_data['latest_live_seam'] != latest_seam:
            issues.append('generated progress latest seam differs from latest manifest seam')

    print(f'latest manifest seam: {latest_seam}')
    if issues:
        print('issues found:')
        for issue in issues:
            print(f'  - {issue}')
        return 1
    print('branch state audit ok')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
