#!/usr/bin/env python3
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from snes_utils_hirom_v2 import format_offset_as_snes, hirom_to_file_offset, parse_snes_address


NOTE_NAME_RE = re.compile(r'^chrono_trigger_session15_continue_notes_(\d+)\.md$')
BLOCK_CLOSED_RE = re.compile(r'^## Block closed:\s*([0-9A-F]{2}:[0-9A-F]{4}\.\.[0-9A-F]{2}:[0-9A-F]{4})', re.MULTILINE)
SWEEP_BLOCK_RE = re.compile(r'^\s*-\s*`([0-9A-F]{2}:[0-9A-F]{4}\.\.[0-9A-F]{2}:[0-9A-F]{4})`', re.MULTILINE)
LIVE_SEAM_RE = re.compile(r'New live seam:\s*(?:\*\*)?`?([0-9A-F]{2}:[0-9A-F]{4}\.\.)`?(?:\*\*)?', re.IGNORECASE)
ZERO_PROMOTION_RE = re.compile(r'Result:\s*\*\*(?:zero|no new)\s+promotions?\*\*', re.IGNORECASE)


@dataclass(frozen=True)
class ContinuationClosedRange:
    note_number: int
    source_path: str
    range_text: str
    kind: str
    label: str
    confidence: str
    source_mode: str


@dataclass(frozen=True)
class ContinuationNoteSummary:
    note_number: int
    source_path: str
    block_ranges: tuple[str, ...]
    live_seam: str
    zero_promotions: bool
    closed_ranges: tuple[ContinuationClosedRange, ...]


def note_number_from_path(path: str | Path) -> int | None:
    match = NOTE_NAME_RE.match(Path(path).name)
    if not match:
        return None
    return int(match.group(1))


def iter_session15_note_paths(sessions_dir: str | Path) -> list[Path]:
    base = Path(sessions_dir)
    paths: list[Path] = []
    for path in base.glob('chrono_trigger_session15_continue_notes_*.md'):
        number = note_number_from_path(path)
        if number is None:
            continue
        paths.append(path)
    paths.sort(key=lambda item: note_number_from_path(item) or -1)
    return paths


def page_range_from_start(page_text: str) -> str:
    bank, addr = parse_snes_address(page_text)
    return f'{bank:02X}:{addr:04X}..{bank:02X}:{addr + 0xFF:04X}'


def slugify(value: str) -> str:
    text = value.strip().lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_') or 'unknown'


def parse_range_bounds(range_text: str) -> tuple[int, int, int, int]:
    left, right = range_text.split('..', 1)
    start_bank, start_addr = parse_snes_address(left)
    end_bank, end_addr = parse_snes_address(right)
    return start_bank, start_addr, end_bank, end_addr


def iter_pages_for_block(range_text: str) -> Iterable[str]:
    start_bank, start_addr, end_bank, end_addr = parse_range_bounds(range_text)
    start_offset = hirom_to_file_offset(start_bank, start_addr)
    end_offset = hirom_to_file_offset(end_bank, end_addr)
    if start_offset % 0x100 != 0 or end_offset % 0x100 != 0xFF:
        raise ValueError(f'block range must be page aligned: {range_text}')
    offset = start_offset
    while offset <= end_offset:
        page_start = format_offset_as_snes(offset)
        yield page_range_from_start(page_start)
        offset += 0x100


def parse_structured_page_closures(text: str, note_number: int, source_path: str) -> list[ContinuationClosedRange]:
    ranges: list[ContinuationClosedRange] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith('|'):
            continue
        if 'Page' in stripped and 'Decision' in stripped:
            continue
        if set(stripped.replace('|', '').replace('-', '').replace(' ', '')) == set():
            continue
        parts = [part.strip() for part in stripped.strip('|').split('|')]
        if len(parts) < 5:
            continue
        page_text, family, posture, decision = parts[:4]
        if not re.fullmatch(r'[0-9A-F]{2}:[0-9A-F]{4}', page_text):
            continue
        if decision.lower() != 'freeze':
            continue
        family_slug = slugify(family)
        posture_slug = slugify(posture)
        label = f'ct_note_backed_frozen_page_{page_text.lower().replace(":", "_")}_{family_slug}_{posture_slug}'
        ranges.append(
            ContinuationClosedRange(
                note_number=note_number,
                source_path=source_path,
                range_text=page_range_from_start(page_text),
                kind='data',
                label=label,
                confidence='medium-high',
                source_mode='structured_page_freeze',
            )
        )
    return ranges


def parse_coarse_block_closures(text: str, note_number: int, source_path: str) -> list[ContinuationClosedRange]:
    if not ZERO_PROMOTION_RE.search(text):
        return []
    block_ranges = [match.group(1) for match in SWEEP_BLOCK_RE.finditer(text)]
    if not block_ranges:
        block_closed = BLOCK_CLOSED_RE.search(text)
        if block_closed:
            block_ranges = [block_closed.group(1)]
    ranges: list[ContinuationClosedRange] = []
    for block_index, block_range in enumerate(block_ranges, start=1):
        for page_index, page_range in enumerate(iter_pages_for_block(block_range), start=1):
            page_start = page_range.split('..', 1)[0]
            label = (
                f'ct_note_backed_frozen_page_{page_start.lower().replace(":", "_")}'
                f'_coarse_zero_promotion_note_{note_number:02d}_block_{block_index:02d}_page_{page_index:02d}'
            )
            ranges.append(
                ContinuationClosedRange(
                    note_number=note_number,
                    source_path=source_path,
                    range_text=page_range,
                    kind='data',
                    label=label,
                    confidence='medium',
                    source_mode='coarse_zero_promotion_block',
                )
            )
    return ranges


def parse_continuation_note(path: str | Path) -> ContinuationNoteSummary:
    note_path = Path(path)
    note_number = note_number_from_path(note_path)
    if note_number is None:
        raise ValueError(f'not a session15 continuation note path: {note_path}')
    text = note_path.read_text(encoding='utf-8')

    block_ranges = [match.group(1) for match in BLOCK_CLOSED_RE.finditer(text)]
    if not block_ranges:
        block_ranges = [match.group(1) for match in SWEEP_BLOCK_RE.finditer(text)]

    live_seam_match = LIVE_SEAM_RE.search(text)
    live_seam = live_seam_match.group(1) if live_seam_match else ''

    closed_ranges = parse_structured_page_closures(text, note_number, str(note_path))
    if not closed_ranges:
        closed_ranges = parse_coarse_block_closures(text, note_number, str(note_path))

    return ContinuationNoteSummary(
        note_number=note_number,
        source_path=str(note_path),
        block_ranges=tuple(block_ranges),
        live_seam=live_seam,
        zero_promotions=bool(ZERO_PROMOTION_RE.search(text)),
        closed_ranges=tuple(closed_ranges),
    )


def load_continuation_note_closed_ranges(sessions_dir: str | Path) -> list[ContinuationClosedRange]:
    ranges: list[ContinuationClosedRange] = []
    for path in iter_session15_note_paths(sessions_dir):
        ranges.extend(parse_continuation_note(path).closed_ranges)
    return ranges


def latest_continuation_note_summary(sessions_dir: str | Path) -> ContinuationNoteSummary | None:
    paths = iter_session15_note_paths(sessions_dir)
    if not paths:
        return None
    return parse_continuation_note(paths[-1])
