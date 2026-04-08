#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from continuation_note_utils_v1 import latest_continuation_note_summary
from snes_utils import iter_manifest_paths, load_manifest, manifest_live_seam, manifest_pass_number


def main() -> int:
    parser = argparse.ArgumentParser(description='Audit branch state against pass manifests and reports')
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--sessions-dir', default='docs/sessions')
    parser.add_argument('--bank-progress', default='tools/config/bank_c3_progress.json')
    parser.add_argument('--generated-progress', default='tools/config/bank_c3_progress.generated.json')
    parser.add_argument('--strict-gaps', action='store_true', help='Fail when manifest pass numbers are non-contiguous')
    args = parser.parse_args()

    manifest_passes = []
    latest_seam = None
    for path in iter_manifest_paths(args.manifests_dir):
        data = load_manifest(path)
        manifest_passes.append(manifest_pass_number(data, path))
        latest_seam = manifest_live_seam(data) or latest_seam

    warnings = []
    issues = []
    if not manifest_passes:
        issues.append('no manifests found')
    else:
        expected = list(range(min(manifest_passes), max(manifest_passes) + 1))
        missing = sorted(set(expected) - set(manifest_passes))
        if missing:
            warnings.append(f'missing manifest pass numbers: {missing}')

    latest_note = latest_continuation_note_summary(args.sessions_dir)
    effective_seam = latest_note.live_seam if latest_note and latest_note.live_seam else latest_seam

    static_progress = Path(args.bank_progress)
    generated_progress = Path(args.generated_progress)
    if static_progress.exists() and generated_progress.exists() and latest_note is None:
        gen_data = json.loads(generated_progress.read_text(encoding='utf-8'))
        if gen_data.get('latest_live_seam') and latest_seam and gen_data['latest_live_seam'] != latest_seam:
            issues.append('generated progress latest seam differs from latest manifest seam')

    print(f'latest manifest seam: {latest_seam}')
    if latest_note is not None:
        print(f'latest continuation note: {Path(latest_note.source_path).name}')
        print(f'note-backed live seam: {latest_note.live_seam or "(missing)"}')
    print(f'effective live seam: {effective_seam}')
    if warnings:
        print('warnings found:')
        for warning in warnings:
            print(f'  - {warning}')
    if issues:
        print('issues found:')
        for issue in issues:
            print(f'  - {issue}')
        return 1
    if warnings and args.strict_gaps:
        return 1
    print('branch state audit ok')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
