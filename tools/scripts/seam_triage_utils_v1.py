#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from snes_utils import file_offset_to_snes, hirom_to_file_offset, format_snes_range, parse_snes_address, parse_snes_range, slice_rom_range

BAD_START_HARD = {
    0x00: 'brk_or_barrier',
    0x02: 'cop_barrier',
    0x03: 'or_indirect_stack_start',
    0x40: 'rti_return_stub',
    0x60: 'rts_return_stub',
    0x6B: 'rtl_return_stub',
    0x80: 'bra_landing_pad',
    0xFF: 'barrier_ff',
}

BAD_START_SOFT = {
    0x01: 'ora_indirect_start',
    0x09: 'ora_immediate_start',
    0x2B: 'pld_epilogue_pull',
    0x30: 'branch_opcode_start',
    0xAB: 'plb_epilogue_pull',
}

BRANCHES = {0x10, 0x30, 0x50, 0x70, 0x80, 0x82, 0x90, 0xB0, 0xD0, 0xF0}
RETURNS = {0x60, 0x6B, 0x40}
CALLS = {0x20, 0x22, 0x4C, 0x5C}
STACKISH = {0x08, 0x28, 0x48, 0x68, 0xDA, 0xFA, 0x5A, 0x7A}
BARRIERS = {0x00, 0x02, 0x42, 0xFF}

def snes_to_offset(bank: int, addr: int) -> int:
    return hirom_to_file_offset(bank, addr)

def neighborhood(rom_bytes: bytes, bank: int, addr: int, radius: int) -> bytes:
    center = snes_to_offset(bank, addr)
    start = max(0, center - radius)
    end = min(len(rom_bytes), center + radius + 1)
    return rom_bytes[start:end]

def printable_ascii_ratio(blob: bytes) -> float:
    if not blob:
        return 0.0
    hits = sum(1 for b in blob if 0x20 <= b <= 0x7E)
    return hits / len(blob)

def zero_ratio(blob: bytes) -> float:
    if not blob:
        return 0.0
    return sum(1 for b in blob if b == 0x00) / len(blob)

def zero_ff_ratio(blob: bytes) -> float:
    if not blob:
        return 0.0
    return sum(1 for b in blob if b in (0x00, 0xFF)) / len(blob)

def branch_ratio(blob: bytes) -> float:
    if not blob:
        return 0.0
    return sum(1 for b in blob if b in BRANCHES) / len(blob)

def call_ratio(blob: bytes) -> float:
    if not blob:
        return 0.0
    return sum(1 for b in blob if b in CALLS) / len(blob)

def return_count(blob: bytes) -> int:
    return sum(1 for b in blob if b in RETURNS)

def repeated_pair_score(blob: bytes) -> float:
    if len(blob) < 4:
        return 0.0
    pairs = [blob[i:i + 2] for i in range(0, len(blob) - 1, 2)]
    if not pairs:
        return 0.0
    distinct = len(set(pairs))
    return 1.0 - (distinct / len(pairs))

def classify_start_byte(op: int) -> tuple[str, str]:
    if op in BAD_START_HARD:
        return 'hard_bad_start', BAD_START_HARD[op]
    if op in BAD_START_SOFT:
        return 'soft_bad_start', BAD_START_SOFT[op]
    return 'clean_start', ''

def data_side_risk(blob: bytes) -> str:
    ascii_r = printable_ascii_ratio(blob)
    zeroff_r = zero_ff_ratio(blob)
    rep_r = repeated_pair_score(blob)
    branch_r = branch_ratio(blob)
    returns = return_count(blob)
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
    if branch_r >= 0.18 and returns == 0:
        score += 1
    if score >= 4:
        return 'very_high'
    if score >= 2:
        return 'high'
    if score >= 1:
        return 'medium'
    return 'low'

def compute_page_metrics(blob: bytes) -> dict[str, float | int]:
    return {
        'ascii_ratio': round(printable_ascii_ratio(blob), 3),
        'zero_ratio': round(zero_ratio(blob), 3),
        'zero_ff_ratio': round(zero_ff_ratio(blob), 3),
        'repeated_pair_score': round(repeated_pair_score(blob), 3),
        'branch_ratio': round(branch_ratio(blob), 3),
        'call_ratio': round(call_ratio(blob), 3),
        'return_count': return_count(blob),
    }

def classify_page_family_from_blob(blob: bytes) -> tuple[str, list[str], dict[str, float | int]]:
    metrics = compute_page_metrics(blob)
    reasons: list[str] = []
    family = 'mixed_command_data'
    if metrics['zero_ratio'] >= 0.75 and metrics['repeated_pair_score'] >= 0.6 and metrics['ascii_ratio'] <= 0.15:
        family = 'dead_zero_field'
        reasons.extend(['zero_dominant', 'repeated_pairs_dominant'])
    elif metrics['ascii_ratio'] >= 0.45:
        family = 'text_ascii_heavy'
        reasons.append('ascii_heavy')
    elif (
        metrics['ascii_ratio'] <= 0.30
        and metrics['zero_ff_ratio'] <= 0.18
        and metrics['repeated_pair_score'] <= 0.10
        and (metrics['call_ratio'] >= 0.02 or metrics['branch_ratio'] >= 0.05)
        and metrics['return_count'] >= 1
    ):
        family = 'candidate_code_lane'
        reasons.extend(['low_data_noise', 'control_activity'])
    elif metrics['branch_ratio'] >= 0.08 and metrics['return_count'] >= 1 and metrics['ascii_ratio'] <= 0.45:
        family = 'branch_fed_control_pocket'
        reasons.extend(['branch_dense', 'return_anchored'])
    else:
        reasons.append('mixed_metrics')
    return family, reasons, metrics

def classify_page_family(rom_bytes: bytes, range_text: str) -> tuple[str, list[str], dict[str, float | int]]:
    blob = slice_rom_range(rom_bytes, range_text)
    return classify_page_family_from_blob(blob)

def load_dead_ranges(config_path: str | Path | None) -> list[dict[str, str]]:
    if not config_path:
        return []
    path = Path(config_path)
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding='utf-8'))
    return list(data.get('ranges', []))

def range_contains(range_text: str, bank: int, addr: int) -> bool:
    r_bank, start, end = parse_snes_range(range_text)
    return bank == r_bank and start <= addr <= end

def dead_range_match(dead_ranges: Iterable[dict[str, str]], bank: int, addr: int) -> dict[str, str] | None:
    for item in dead_ranges:
        if range_contains(item['range'], bank, addr):
            return item
    return None

def check_data_misread_patterns(blob: bytes) -> list[str]:
    """Return a list of data-misread signature labels found in blob.

    Patterns detected:
    - consecutive_identical_branch: same branch opcode+operand appears at offset i and i+2
    - consecutive_rts: two 0x60 bytes in a row (back-to-back RTS)
    - rti_rts_proximity: RTI (0x40) and RTS (0x60) within 3 bytes of each other
    - tight_loop_branch: any branch opcode with operand 0xFF (branch to self-minus-one)
    - sed_decimal_mode: SED (0xF8) in first 16 bytes — SNES production code never uses decimal mode
    """
    flags: list[str] = []
    n = len(blob)

    # consecutive identical branch: branch opcode at i and i+2 with same operand
    for i in range(n - 3):
        if blob[i] in BRANCHES and blob[i] == blob[i + 2] and blob[i + 1] == blob[i + 3]:
            flags.append(f'consecutive_identical_branch_at_{i:02X}')
            break

    # consecutive RTS (60 60)
    for i in range(n - 1):
        if blob[i] == 0x60 and blob[i + 1] == 0x60:
            flags.append(f'consecutive_rts_at_{i:02X}')
            break

    # RTI + RTS within 3 bytes of each other
    rti_pos = [i for i, b in enumerate(blob) if b == 0x40]
    rts_pos = [i for i, b in enumerate(blob) if b == 0x60]
    reported_proximity = False
    for ri in rti_pos:
        for si in rts_pos:
            if abs(ri - si) <= 3:
                flags.append(f'rti_rts_proximity_at_{min(ri, si):02X}')
                reported_proximity = True
                break
        if reported_proximity:
            break

    # tight-loop backward branch: branch opcode followed by 0xFF (-1 offset = branch to self-minus-one)
    for i in range(n - 1):
        if blob[i] in BRANCHES and blob[i + 1] == 0xFF:
            flags.append(f'tight_loop_branch_at_{i:02X}')
            break

    # SED (0xF8) in first 16 bytes — decimal mode never used in SNES production code
    for i in range(min(16, n)):
        if blob[i] == 0xF8:
            flags.append(f'sed_decimal_mode_at_{i:02X}')
            break

    return flags
