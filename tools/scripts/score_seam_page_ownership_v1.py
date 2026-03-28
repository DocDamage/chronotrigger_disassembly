#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DIRECT_KINDS = {'JSR', 'JMP', 'JSL', 'JML'}
BRANCH_KINDS = {
    'BRA', 'BRL', 'BCC', 'BCS', 'BEQ', 'BMI', 'BNE', 'BPL', 'BVC', 'BVS',
    'PER'
}
RETURN_SUFFIXES = ('RTS', 'RTL', 'RTI')


def run_json(script_name: str, *extra_args: str) -> dict:
    script_path = SCRIPT_DIR / script_name
    proc = subprocess.run(
        [sys.executable, str(script_path), *extra_args, '--json'],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def parse_snes_address(text: str) -> tuple[int, int]:
    bank_s, addr_s = text.split(':')
    return int(bank_s, 16), int(addr_s, 16)


def page_base(addr: int) -> int:
    return addr & 0xFF00


def page_offset(addr: int) -> int:
    return addr & 0x00FF


def parse_island_range(text: str) -> tuple[int, int, int]:
    left, right = text.split('..')
    bank_s, start_s = left.split(':')
    _, end_s = right.split(':')
    return int(bank_s, 16), int(start_s, 16), int(end_s, 16)


def risk_penalty(risk: str) -> int:
    return {
        'low': 0,
        'medium': 1,
        'high': 2,
        'very_high': 3,
    }.get(risk, 3)


def strength_bonus(strength: str) -> int:
    return {
        'strong': 4,
        'weak': 2,
        'suspect': 0,
        'invalid': -4,
    }.get(strength, -4)


def classify_hit(hit: dict, target_bank: int) -> dict:
    caller_bank, caller_addr = parse_snes_address(hit['caller'])
    _, target_addr = parse_snes_address(hit['target'])
    kind = str(hit.get('kind', ''))
    caller_page = page_base(caller_addr)
    target_page = page_base(target_addr)
    same_page = caller_bank == target_bank and caller_page == target_page
    same_bank = caller_bank == target_bank
    is_direct = kind in DIRECT_KINDS
    is_branch = kind in BRANCH_KINDS
    return {
        'caller_bank': caller_bank,
        'caller_addr': caller_addr,
        'target_addr': target_addr,
        'same_bank': same_bank,
        'same_page': same_page,
        'is_direct': is_direct,
        'is_branch': is_branch,
        'is_external': not same_page,
        'is_page_top': page_offset(target_addr) <= 0x10,
    }


def island_lookup(islands: list[dict]) -> list[tuple[int, int, dict]]:
    out = []
    for island in islands:
        bank, start, end = parse_island_range(island['range'])
        out.append((start, end, island))
    return out


def interior_island_penalty(target_addr: int, islands_info: list[tuple[int, int, dict]]) -> tuple[int, str]:
    for start, end, island in islands_info:
        if start <= target_addr <= end:
            if target_addr == start:
                return 0, ''
            score = int(island.get('score', 0))
            penalty = 3 if score >= 5 else 2
            return penalty, island['range']
    return 0, ''


def score_hit(hit: dict, target_bank: int, islands_info: list[tuple[int, int, dict]]) -> dict:
    shape = classify_hit(hit, target_bank)
    score = 0

    score += strength_bonus(str(hit.get('effective_strength', 'invalid')))
    score -= risk_penalty(str(hit.get('caller_risk', 'very_high')))
    score -= risk_penalty(str(hit.get('target_risk', 'very_high')))

    if shape['is_direct']:
        score += 2
    if shape['is_external']:
        score += 2
    if shape['is_branch']:
        score -= 1
    if shape['same_page']:
        score -= 2
    if shape['is_page_top']:
        score += 2

    penalty, island_range = interior_island_penalty(shape['target_addr'], islands_info)
    score -= penalty

    reasons = []
    if shape['is_direct']:
        reasons.append('direct')
    if shape['is_external']:
        reasons.append('external')
    if shape['same_page']:
        reasons.append('same_page')
    if shape['is_branch']:
        reasons.append('branch_fed')
    if shape['is_page_top']:
        reasons.append('page_top')
    if island_range:
        reasons.append(f'interior_of_{island_range}')

    return {
        **hit,
        **shape,
        'ownership_score': score,
        'ownership_reasons': reasons,
        'interior_island_range': island_range,
    }


def page_class(summary: dict) -> str:
    if summary['best_external_direct_score'] >= 8 and summary['external_direct_hit_count'] >= 2:
        return 'high_attention_external_owner_candidate'
    if summary['best_external_direct_score'] >= 5:
        return 'medium_attention_external_owner_candidate'
    if summary['local_branch_hit_count'] >= max(3, summary['external_direct_hit_count'] + 2):
        return 'local_control_blob'
    if summary['interior_island_hit_count'] >= 2:
        return 'interior_landing_bait'
    return 'mixed_no_owner'


def build_summary(scored_hits: list[dict], islands: list[dict]) -> dict:
    external_direct = [
        hit for hit in scored_hits
        if hit['is_external'] and hit['is_direct']
    ]
    local_branch = [
        hit for hit in scored_hits
        if hit['same_page'] and hit['is_branch']
    ]
    page_top = [hit for hit in scored_hits if hit['is_page_top']]
    interior = [hit for hit in scored_hits if hit['interior_island_range']]
    best_hit = max(scored_hits, key=lambda item: item['ownership_score']) if scored_hits else None
    best_external = max(external_direct, key=lambda item: item['ownership_score']) if external_direct else None

    summary = {
        'scored_hit_count': len(scored_hits),
        'external_direct_hit_count': len(external_direct),
        'local_branch_hit_count': len(local_branch),
        'page_top_hit_count': len(page_top),
        'interior_island_hit_count': len(interior),
        'local_island_count': len(islands),
        'best_hit_score': int(best_hit['ownership_score']) if best_hit else None,
        'best_hit_target': best_hit['target'] if best_hit else '',
        'best_external_direct_score': int(best_external['ownership_score']) if best_external else None,
        'best_external_direct_target': best_external['target'] if best_external else '',
    }
    summary['page_class'] = page_class(summary)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Score page-level ownership signal for a C3 seam by separating external direct callers from local branch-fed control noise'
    )
    parser.add_argument('--rom', required=True)
    parser.add_argument('--range', dest='range_text', required=True)
    parser.add_argument('--manifests-dir', default='passes/manifests')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    flow = run_json(
        'run_c3_candidate_flow_v2.py',
        '--rom', args.rom,
        '--range', args.range_text,
        '--manifests-dir', args.manifests_dir,
    )
    bank_s, _ = args.range_text.split(':', 1)
    target_bank = int(bank_s, 16)

    islands = list(flow.get('local_islands', {}).get('islands', []))
    islands_info = island_lookup(islands)
    hits = list(flow.get('xref_context', {}).get('hits', []))
    scored_hits = [score_hit(hit, target_bank, islands_info) for hit in hits]
    scored_hits.sort(
        key=lambda item: (-int(item['ownership_score']), item['target'], item['caller'])
    )

    result = {
        'range': args.range_text,
        'summary': build_summary(scored_hits, islands),
        'hits': scored_hits,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"range: {args.range_text}")
        for key, value in result['summary'].items():
            print(f"{key}: {value}")
        if scored_hits:
            print('top ownership hits:')
            for hit in scored_hits[:10]:
                reasons = ','.join(hit['ownership_reasons'])
                print(
                    f"  {hit['caller']} {hit['kind']} -> {hit['target']} | "
                    f"score={hit['ownership_score']} effective={hit['effective_strength']} "
                    f"caller_risk={hit['caller_risk']} target_risk={hit['target_risk']} "
                    f"reasons={reasons}"
                )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
