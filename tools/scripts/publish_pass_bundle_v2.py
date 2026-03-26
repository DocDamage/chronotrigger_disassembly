#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content, encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description='Publish a pass bundle from a manifest into repo-native layout')
    parser.add_argument('--manifest', required=True)
    parser.add_argument('--repo-root', default='.')
    parser.add_argument('--note', default='')
    args = parser.parse_args()

    repo_root = Path(args.repo_root)
    manifest_path = Path(args.manifest)
    data = json.loads(manifest_path.read_text(encoding='utf-8'))
    pass_no = data['pass_number']

    manifest_dst = repo_root / 'passes' / 'manifests' / f'pass{pass_no}.json'
    ensure_dir(manifest_dst.parent)
    manifest_dst.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')

    summary_lines = [
        f"# Pass {pass_no}",
        '',
        f"- branch: **{data['branch']}**",
        f"- toolkit version: **{data['toolkit_version']}**",
        f"- live seam after pass: **`{data['live_seam_after_pass']}`**",
        f"- completion estimate: **~{data['completion_estimate']}%**",
        '',
        '## Closed ranges',
    ]
    for item in data.get('closed_ranges', []):
        summary_lines.append(f"- `{item['range']}` — {item['label']} ({item['kind']}, {item['confidence']})")
    if args.note:
        summary_lines += ['', '## Note', args.note]

    summary = '\n'.join(summary_lines) + '\n'
    write_text(repo_root / 'passes' / 'disasm' / f'pass{pass_no}.md', summary)
    write_text(repo_root / 'passes' / 'labels' / f'pass{pass_no}.md', summary)

    print(f'published pass {pass_no} bundle into {repo_root.resolve()}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
