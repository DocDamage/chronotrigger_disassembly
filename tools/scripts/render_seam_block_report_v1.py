#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def format_targets(targets: list[dict[str, object]]) -> str:
    if not targets:
        return 'none'
    parts = []
    for item in targets[:3]:
        tag = ' [boundary_bait]' if item.get('boundary_bait') else ''
        parts.append(f"{item['target']} ({item['best_strength']}, hits={item['hit_count']}){tag}")
    return '; '.join(parts)


def format_backtracks(items: list[dict[str, object]]) -> str:
    if not items:
        return 'none'
    parts = []
    for item in items[:3]:
        owner = item.get('owner_start', '') or item.get('range', '')
        score = item.get('score', 0)
        parts.append(f'{owner} (score={score})')
    return '; '.join(parts)


def format_clusters(clusters: list[dict[str, object]]) -> str:
    if not clusters:
        return 'none'
    parts = []
    for item in clusters[:2]:
        parts.append(str(item.get('range', '')))
    return '; '.join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description='Render a Markdown seam block report from run_seam_block_v1 JSON output.')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', default='')
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding='utf-8'))
    lines: list[str] = []
    lines.append(f"# Seam block report — {data['start']} ({data['pages_requested']} pages)")
    lines.append('')
    lines.append('## Summary')
    lines.append(f"- page families: `{json.dumps(data['page_family_counts'], sort_keys=True)}`")
    lines.append(f"- review postures: `{json.dumps(data['review_posture_counts'], sort_keys=True)}`")
    lines.append('')
    lines.append('## Page breakdown')
    lines.append('')
    for page in data['pages']:
        lines.append(f"### `{page['range']}`")
        lines.append(f"- page family: `{page['page_family']}`")
        lines.append(f"- review posture: `{page['review_posture']}`")
        summary = page['summary']
        lines.append(
            f"- summary: raw_targets={summary['raw_target_count']}, xref_hits={summary['xref_hit_count']}, "
            f"strong_or_weak={summary['effective_strong_or_weak_hits']}, hard_bad={summary['hard_bad_start_hits']}, "
            f"soft_bad={summary['soft_bad_start_hits']}, clusters={summary['local_cluster_count']}"
        )
        lines.append(f"- best targets: {format_targets(page['best_targets'])}")
        lines.append(f"- owner backtracks: {format_backtracks(page['top_backtracks'])}")
        lines.append(f"- local clusters: {format_clusters(page['local_clusters'])}")
        lines.append('')

    text = '\n'.join(lines)
    if args.output:
        Path(args.output).write_text(text, encoding='utf-8')
    else:
        print(text)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
