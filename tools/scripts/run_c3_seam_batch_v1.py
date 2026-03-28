#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def run_json(script_name: str, *extra_args: str) -> dict:
    script_path = SCRIPT_DIR / script_name
    proc = subprocess.run(
        [sys.executable, str(script_path), *extra_args, '--json'],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def top_lure(page: dict) -> dict | None:
    lures = page.get('top_boundary_lures') or []
    if not lures:
        return None
    return lures[0]


def render_markdown(range_text: str, mixed: dict, boundary: dict) -> str:
    lines: list[str] = []
    lines.append(f'# C3 seam batch report — {range_text}')
    lines.append('')
    lines.append('## Page summary')
    lines.append('')
    for mix_page, bound_page in zip(mixed['pages'], boundary['pages']):
        lure = top_lure(bound_page)
        lines.append(f"### {mix_page['range']}")
        lines.append(f"- page label: `{mix_page['label']}`")
        lines.append(
            f"- metrics: ascii={mix_page['ascii_ratio']}, zero={mix_page['zero_ratio']}, ff={mix_page['ff_ratio']}, repeated_pair={mix_page['repeated_pair_score']}"
        )
        lines.append(f"- local island count: {bound_page['island_count']}")
        lines.append(f"- visible boundary-lure count: {bound_page['hit_count']}")
        if lure:
            lines.append(
                f"- strongest visible lure: `{lure['caller']} {lure['kind']} -> {lure['target']}` | caller_risk={lure['caller_risk']} target_risk={lure['target_risk']} boundary={lure['boundary_reason']}"
            )
        else:
            lines.append('- strongest visible lure: none')
        lines.append('')
    lines.append('## Quick read')
    lines.append('')
    text_heavy = [p['range'] for p in mixed['pages'] if p['label'] in {'text_heavy_mixed', 'text_table_mixed'}]
    local_control = [p['range'] for p in mixed['pages'] if p['label'] == 'local_control_blob']
    executableish = [p['range'] for p in mixed['pages'] if p['label'] == 'mixed_executable_looking']
    lines.append(f"- text-heavy pages: {', '.join(text_heavy) if text_heavy else 'none'}")
    lines.append(f"- local-control pages: {', '.join(local_control) if local_control else 'none'}")
    lines.append(f"- executable-looking pages: {', '.join(executableish) if executableish else 'none'}")
    lines.append('')
    lines.append('## Caveat')
    lines.append('')
    lines.append('This batch report is a triage aid, not an auto-promotion engine. A clean-looking page or lure still needs caller quality and local structure to agree before it earns an owner/helper label.')
    lines.append('')
    return '\n'.join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description='Run batch seam triage across a C3 range and emit JSON or markdown')
    ap.add_argument('--rom', required=True)
    ap.add_argument('--range', dest='range_text', required=True)
    ap.add_argument('--format', choices=['json', 'markdown'], default='json')
    ap.add_argument('--output', default='')
    args = ap.parse_args()

    mixed = run_json('page_range_mixedness_v1.py', '--rom', args.rom, '--range', args.range_text)
    boundary = run_json('score_owner_boundary_risk_v1.py', '--rom', args.rom, '--range', args.range_text)

    result = {
        'range': args.range_text,
        'page_mixedness': mixed,
        'owner_boundary': boundary,
    }

    if args.format == 'json':
        rendered = json.dumps(result, indent=2)
    else:
        rendered = render_markdown(args.range_text, mixed, boundary)

    if args.output:
        Path(args.output).write_text(rendered, encoding='utf-8')
    else:
        print(rendered)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
