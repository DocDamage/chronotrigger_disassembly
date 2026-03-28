#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

BRANCHES = {0x10, 0x30, 0x50, 0x70, 0x80, 0x82, 0x90, 0xB0, 0xD0, 0xF0}
RETURNS = {0x60, 0x6B, 0x40}
CALLS = {0x20, 0x22, 0x4C, 0x5C}
BARRIERS = {0x00, 0x02, 0x42, 0xFF}


def parse_snes_range(text: str) -> tuple[int, int, int]:
    left, right = text.split('..')
    bank_s, start_s = left.split(':')
    bank2_s, end_s = right.split(':')
    if bank_s != bank2_s:
        raise ValueError('cross-bank ranges not supported')
    return int(bank_s, 16), int(start_s, 16), int(end_s, 16)


def format_snes(bank: int, addr: int) -> str:
    return f'{bank:02X}:{addr:04X}'


def snes_to_offset(bank: int, addr: int) -> int:
    if bank < 0xC0:
        raise ValueError(f'unsupported bank {bank:02X}')
    return (bank - 0xC0) * 0x10000 + addr


def file_offset_to_snes(offset: int) -> tuple[int, int]:
    bank = 0xC0 + (offset // 0x10000)
    addr = offset % 0x10000
    return bank, addr


def iter_raw_callers(rom_bytes: bytes):
    limit = len(rom_bytes)
    for offset in range(limit):
        op = rom_bytes[offset]
        caller_bank, caller_addr = file_offset_to_snes(offset)
        caller = format_snes(caller_bank, caller_addr)
        if op in (0x20, 0x4C) and offset + 2 < limit:
            target_addr = rom_bytes[offset + 1] | (rom_bytes[offset + 2] << 8)
            kind = 'JSR' if op == 0x20 else 'JMP'
            yield {
                'kind': kind,
                'caller': caller,
                'caller_bank': caller_bank,
                'target_bank': caller_bank,
                'target_addr': target_addr,
                'target': format_snes(caller_bank, target_addr),
            }
        elif op in (0x22, 0x5C) and offset + 3 < limit:
            target_addr = rom_bytes[offset + 1] | (rom_bytes[offset + 2] << 8)
            target_bank = rom_bytes[offset + 3]
            kind = 'JSL' if op == 0x22 else 'JML'
            yield {
                'kind': kind,
                'caller': caller,
                'caller_bank': caller_bank,
                'target_bank': target_bank,
                'target_addr': target_addr,
                'target': format_snes(target_bank, target_addr),
            }
        elif op in BRANCHES and offset + 1 < limit:
            disp = rom_bytes[offset + 1]
            if disp >= 0x80:
                disp -= 0x100
            target_addr = (caller_addr + 2 + disp) & 0xFFFF
            yield {
                'kind': f'BR_{op:02X}',
                'caller': caller,
                'caller_bank': caller_bank,
                'target_bank': caller_bank,
                'target_addr': target_addr,
                'target': format_snes(caller_bank, target_addr),
            }


def neighborhood(rom_bytes: bytes, bank: int, addr: int, radius: int = 16) -> bytes:
    center = snes_to_offset(bank, addr)
    start = max(0, center - radius)
    end = min(len(rom_bytes), center + radius + 1)
    return rom_bytes[start:end]


def printable_ascii_ratio(blob: bytes) -> float:
    return (sum(1 for b in blob if 0x20 <= b <= 0x7E) / len(blob)) if blob else 0.0


def zero_ff_ratio(blob: bytes) -> float:
    return (sum(1 for b in blob if b in (0x00, 0xFF)) / len(blob)) if blob else 0.0


def repeated_pair_score(blob: bytes) -> float:
    if len(blob) < 4:
        return 0.0
    pairs = [blob[i:i+2] for i in range(0, len(blob) - 1, 2)]
    if not pairs:
        return 0.0
    return 1.0 - (len(set(pairs)) / len(pairs))


def data_side_risk(blob: bytes) -> str:
    ascii_r = printable_ascii_ratio(blob)
    zeroff_r = zero_ff_ratio(blob)
    rep_r = repeated_pair_score(blob)
    score = 0
    if ascii_r >= 0.35:
        score += 2
    elif ascii_r >= 0.22:
        score += 1
    if zeroff_r >= 0.35:
        score += 2
    elif zeroff_r >= 0.22:
        score += 1
    if rep_r >= 0.45:
        score += 2
    elif rep_r >= 0.30:
        score += 1
    if score >= 4:
        return 'very_high'
    if score >= 2:
        return 'high'
    if score >= 1:
        return 'medium'
    return 'low'


def score_blob(blob: bytes) -> int:
    branches = sum(1 for b in blob if b in BRANCHES)
    returns = sum(1 for b in blob if b in RETURNS)
    calls = sum(1 for b in blob if b in CALLS)
    bad = sum(1 for b in blob if b in BARRIERS)
    score = 0
    if returns:
        score += 3
    if calls:
        score += 2
    if branches:
        score += 1
    score -= bad * 2
    if printable_ascii_ratio(blob) >= 0.30:
        score -= 2
    if repeated_pair_score(blob) >= 0.45:
        score -= 2
    return score


def find_return_anchored_windows(page: bytes, max_back: int = 24, min_width: int = 5) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for end, b in enumerate(page):
        if b not in RETURNS:
            continue
        start = max(0, end - max_back)
        last_barrier = None
        for i in range(start, end):
            if page[i] in BARRIERS:
                last_barrier = i
        if last_barrier is not None:
            start = last_barrier + 1
        if end - start + 1 >= min_width and score_blob(page[start:end+1]) >= 2:
            out.append((start, end))
    dedup = []
    seen = set()
    for item in sorted(out):
        if item not in seen:
            dedup.append(item)
            seen.add(item)
    return dedup


def classify_boundary(page_start: int, target_addr: int, islands: list[tuple[int, int]]) -> tuple[str, str]:
    rel = target_addr - page_start
    if rel < 0 or rel > 0xFF:
        return 'out_of_page', 'target_not_in_page'
    if rel <= 0x0F:
        return 'page_top', 'page_top_bait'
    if rel >= 0xE0:
        return 'late_tail', 'late_tail_bait'
    for start, end in islands:
        if start <= rel <= end:
            if rel == start:
                return 'island_start', 'island_start_candidate'
            return 'island_interior', 'interior_island_landing'
    return 'mid_blob', 'mid_blob_landing'


def risk_rank(text: str) -> int:
    return {'low': 0, 'medium': 1, 'high': 2, 'very_high': 3}.get(text, 4)


def main() -> int:
    ap = argparse.ArgumentParser(description='Score why visible targets fail owner-boundary review across a SNES range')
    ap.add_argument('--rom', required=True)
    ap.add_argument('--range', dest='range_text', required=True)
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    bank, start, end = parse_snes_range(args.range_text)
    rom_bytes = Path(args.rom).read_bytes()
    pages = []
    for page_start in range(start & 0xFF00, (end & 0xFF00) + 0x100, 0x100):
        page_end = min(page_start + 0xFF, end)
        page_blob = rom_bytes[snes_to_offset(bank, page_start):snes_to_offset(bank, page_end)+1]
        islands = find_return_anchored_windows(page_blob)
        hits = []
        for item in iter_raw_callers(rom_bytes):
            if item['target_bank'] != bank or not (page_start <= item['target_addr'] <= page_end):
                continue
            cbank = item['caller_bank']
            caddr = int(item['caller'].split(':')[1], 16)
            caller_blob = neighborhood(rom_bytes, cbank, caddr)
            target_blob = neighborhood(rom_bytes, bank, item['target_addr'])
            caller_risk = data_side_risk(caller_blob)
            target_risk = data_side_risk(target_blob)
            boundary_class, boundary_reason = classify_boundary(page_start, item['target_addr'], islands)
            hits.append({
                'target': item['target'],
                'target_addr': item['target_addr'],
                'caller': item['caller'],
                'kind': item['kind'],
                'caller_risk': caller_risk,
                'target_risk': target_risk,
                'boundary_class': boundary_class,
                'boundary_reason': boundary_reason,
                'caller_ascii_ratio': round(printable_ascii_ratio(caller_blob), 3),
                'target_ascii_ratio': round(printable_ascii_ratio(target_blob), 3),
            })
        hits.sort(key=lambda h: (risk_rank(h['caller_risk']) + risk_rank(h['target_risk']), h['boundary_class'], h['target']))
        top = hits[:12]
        pages.append({
            'range': f'{format_snes(bank, page_start)}..{format_snes(bank, page_end)}',
            'island_count': len(islands),
            'islands': [
                {
                    'range': f'{format_snes(bank, page_start+s)}..{format_snes(bank, page_start+e)}',
                    'start': page_start + s,
                    'end': page_start + e,
                } for s, e in islands
            ],
            'hit_count': len(hits),
            'top_boundary_lures': top,
        })
    out = {'range': args.range_text, 'page_count': len(pages), 'pages': pages}
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(f'range: {args.range_text}')
        for page in pages:
            print(f"{page['range']}: hits={page['hit_count']} islands={page['island_count']}")
            for hit in page['top_boundary_lures'][:5]:
                print(
                    f"  {hit['caller']} {hit['kind']} -> {hit['target']} | caller_risk={hit['caller_risk']} target_risk={hit['target_risk']} boundary={hit['boundary_reason']}"
                )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
