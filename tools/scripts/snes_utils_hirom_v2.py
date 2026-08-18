#!/usr/bin/env python3
from __future__ import annotations

"""Compatibility shim for older toolkit scripts.

The live helper implementation now lives in `snes_utils.py`. This module keeps
the historical import path stable so older scripts and handoff notes continue
to work without carrying a second mapper implementation.
"""

from snes_utils import (
    RangeParseError,
    file_offset_to_snes,
    format_offset_as_snes,
    format_snes_range,
    hirom_to_file_offset,
    iter_all_call_patterns,
    iter_manifest_paths,
    parse_snes_address,
    parse_snes_range,
    range_file_offsets,
    slice_rom_range,
)

__all__ = [
    'RangeParseError',
    'file_offset_to_snes',
    'format_offset_as_snes',
    'format_snes_range',
    'hirom_to_file_offset',
    'iter_all_call_patterns',
    'iter_manifest_paths',
    'parse_snes_address',
    'parse_snes_range',
    'range_file_offsets',
    'slice_rom_range',
]
