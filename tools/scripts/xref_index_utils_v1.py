#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterator

from manifest_xref_utils import ClosedRange, iter_raw_callers, load_closed_ranges


def rom_sha256(rom_bytes: bytes) -> str:
    return hashlib.sha256(rom_bytes).hexdigest()


def build_xref_entries(rom_bytes: bytes) -> list[dict[str, object]]:
    return [dict(item) for item in iter_raw_callers(rom_bytes)]


def write_xref_index(path: str | Path, rom_bytes: bytes, entries: list[dict[str, object]]) -> None:
    payload = {
        'version': 1,
        'rom_sha256': rom_sha256(rom_bytes),
        'entry_count': len(entries),
        'entries': entries,
    }
    Path(path).write_text(json.dumps(payload, indent=2), encoding='utf-8')


def load_xref_index(path: str | Path) -> dict[str, object]:
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if isinstance(data, list):
        return {'version': 1, 'rom_sha256': '', 'entry_count': len(data), 'entries': data}
    if 'entries' not in data:
        raise ValueError('xref index missing entries')
    return data


def iter_index_hits(index_payload: dict[str, object], bank: int, start: int, end: int) -> Iterator[dict[str, object]]:
    for item in index_payload.get('entries', []):
        if int(item['target_bank']) != bank:
            continue
        target_addr = int(item['target_addr'])
        if start <= target_addr <= end:
            yield item


def export_closed_ranges_snapshot(snapshot_path: str | Path, manifests_dir: str | Path) -> dict[str, object]:
    ranges = load_closed_ranges(manifests_dir)
    payload = {
        'version': 1,
        'range_count': len(ranges),
        'ranges': [
            {
                'bank': item.bank,
                'start': item.start,
                'end': item.end,
                'kind': item.kind,
                'label': item.label,
                'confidence': item.confidence,
                'pass_number': item.pass_number,
            }
            for item in ranges
        ],
    }
    Path(snapshot_path).write_text(json.dumps(payload, indent=2), encoding='utf-8')
    return payload


def load_closed_ranges_snapshot(snapshot_path: str | Path) -> list[ClosedRange]:
    data = json.loads(Path(snapshot_path).read_text(encoding='utf-8'))
    out: list[ClosedRange] = []
    for item in data.get('ranges', []):
        out.append(
            ClosedRange(
                bank=int(item['bank']),
                start=int(item['start']),
                end=int(item['end']),
                kind=str(item.get('kind', 'unknown')),
                label=str(item.get('label', '')),
                confidence=str(item.get('confidence', 'unknown')),
                pass_number=int(item.get('pass_number', 0)),
            )
        )
    return out


def choose_closed_ranges(manifests_dir: str | Path | None, snapshot_path: str | Path | None) -> list[ClosedRange]:
    if snapshot_path:
        snap = Path(snapshot_path)
        if snap.exists():
            return load_closed_ranges_snapshot(snap)
    if manifests_dir:
        mdir = Path(manifests_dir)
        if mdir.exists():
            return load_closed_ranges(mdir)
    return []
