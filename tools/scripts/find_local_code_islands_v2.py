#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from seam_triage_utils_v1 import (
    parse_snes_range,
    format_snes_range,
    slice_rom_range,
    BRANCHES,
    RETURNS,
    CALLS,
    STACKISH,
    BARRIERS,
    printable_ascii_ratio,
    repeated_pair_score,
)

def score_blob(blob: bytes) -> dict[str, object]:
    branches = sum(1 for b in blob if b in BRANCHES)
    returns = [i for i, b in enumerate(blob) if b in RETURNS]
    calls = sum(1 for b in blob if b in CALLS)
    stackish = sum(1 for b in blob if b in STACKISH)
    bad = sum(1 for b in blob if b in BARRIERS)
    score = 0
    if returns:
        score += 3
    if calls:
        score += 2
    if branches >= 1:
        score += 1
    if stackish:
        score += 1
    if bad:
        score -= bad * 2
    a_ratio = printable_ascii_ratio(blob)
    r_score = repeated_pair_score(blob)
    if a_ratio >= 0.30:
        score -= 2
    if r_score >= 0.45:
        score -= 2
    return {
        'score': score,
        'branch_count': branches,
        'return_offsets': returns,
        'call_count': calls,
        'stackish_count': stackish,
        'barrier_count': bad,
        'ascii_ratio': round(a_ratio, 3),
        'repeated_pair_score': round(r_score, 3),
    }

def find_return_anchored_windows(data: bytes, max_back: int, min_width: int) -> list[tuple[int, int]]:
    windows: list[tuple[int, int]] = []
    for end, b in enumerate(data):
        if b not in RETURNS:
            continue
        start = max(0, end - max_back)
        last_barrier = None
        for i in range(start, end):
            if data[i] in BARRIERS:
                last_barrier = i
        if last_barrier is not None:
            start = last_barrier + 1
        if end - start + 1 >= min_width:
            windows.append((start, end))
    return sorted(set(windows))

def merge_windows(windows: list[tuple[int, int]], max_gap: int = 2) -> list[list[tuple[int, int]]]:
    if not windows:
        return []
    groups: list[list[tuple[int, int]]] = [[windows[0]]]
    for start, end in windows[1:]:
        g = groups[-1]
        _, prev_end = g[-1]
        if start <= prev_end + max_gap:
            g.append((start, end))
        else:
            groups.append([(start, end)])
    return groups

def main() -> int:
    parser = argparse.ArgumentParser(description='Find return-anchored local islands and merge overlapping windows into broader local clusters')
    parser.add_argument('--rom', required=True)
    parser.add_argument('--range', dest='range_text', required=True)
    parser.add_argument('--min-width', type=int, default=5)
    parser.add_argument('--max-back', type=int, default=24)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()

    bank, start, _ = parse_snes_range(args.range_text)
    data = slice_rom_range(Path(args.rom).read_bytes(), args.range_text)

    candidates = []
    raw_windows = []
    for rel_start, rel_end in find_return_anchored_windows(data, args.max_back, args.min_width):
        blob = data[rel_start:rel_end + 1]
        scored = score_blob(blob)
        if scored['score'] < 2:
            continue
        raw_windows.append((rel_start, rel_end))
        first_return = scored['return_offsets'][0] if scored['return_offsets'] else None
        candidates.append({
            'range': format_snes_range(bank, start + rel_start, start + rel_end),
            'score': scored['score'],
            'width': len(blob),
            'call_count': scored['call_count'],
            'branch_count': scored['branch_count'],
            'stackish_count': scored['stackish_count'],
            'return_count': len(scored['return_offsets']),
            'first_return_address': f'{bank:02X}:{start + rel_start + first_return:04X}' if first_return is not None else '',
            'ascii_ratio': scored['ascii_ratio'],
            'repeated_pair_score': scored['repeated_pair_score'],
            'rel_start': rel_start,
            'rel_end': rel_end,
        })

    clusters = []
    for group in merge_windows(sorted(raw_windows)):
        g_start = group[0][0]
        g_end = max(end for _, end in group)
        blob = data[g_start:g_end + 1]
        scored = score_blob(blob)
        child_ranges = [format_snes_range(bank, start + s, start + e) for s, e in group]
        cluster_score = scored['score'] + max(0, len(group) - 1)
        clusters.append({
            'range': format_snes_range(bank, start + g_start, start + g_end),
            'cluster_score': cluster_score,
            'child_count': len(group),
            'child_ranges': child_ranges,
            'width': len(blob),
            'call_count': scored['call_count'],
            'branch_count': scored['branch_count'],
            'stackish_count': scored['stackish_count'],
            'return_count': len(scored['return_offsets']),
            'ascii_ratio': scored['ascii_ratio'],
            'repeated_pair_score': scored['repeated_pair_score'],
        })

    candidates = [{k:v for k,v in item.items() if k not in {'rel_start','rel_end'}} for item in sorted(candidates, key=lambda item: (-int(item['score']), -int(item['width']), item['range']))]
    clusters.sort(key=lambda item: (-int(item['cluster_score']), -int(item['width']), item['range']))
    result = {'range': args.range_text, 'island_count': len(candidates), 'cluster_count': len(clusters), 'islands': candidates, 'clusters': clusters}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f'range: {args.range_text}')
        print(f'island_count: {len(candidates)}')
        print(f'cluster_count: {len(clusters)}')
        for item in clusters:
            print(f"  cluster {item['range']}: score={item['cluster_score']} width={item['width']} children={item['child_count']}")
            for child in item['child_ranges']:
                print(f"    child: {child}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
