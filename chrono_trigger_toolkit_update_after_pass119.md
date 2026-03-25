# Chrono Trigger Toolkit Update After Pass 119

This focused toolkit update hardens the workflow before pass 120.

## What was patched

- Header-aware HiROM mapper support in `scripts/ct_common.py`
- Payload-vs-raw offset reporting in `scripts/ct_addr.py` and `scripts/ct_dump_range.py`
- Bank-local absolute `JSR/JMP` resolution in `scripts/ct_xrefs.py`
- Versioned xref cache rebuild logic in `scripts/ct_build_xref_cache.py`
- Automatic xref-cache freshness checks in `scripts/ct_resume_workspace.py`
- Mapper/header/xref freshness doctor checks in `scripts/ct_toolkit_doctor.py`
- `ct_dump_range.py` now supports `--end` and `--bank-relative`

## Workspace state refreshed

- Label DB rebuilt from the shipped pass corpus
- Workspace state synced to pass 119
- Xref cache rebuilt with `schema_version = 2` and `xref_resolution_version = bank_local_v2`
- Toolkit doctor rerun successfully

## Current synced state

- latest pass: **119**
- completion estimate: **67.7%**
- workspace root: **ct_pass119_toolkit_v6_work**
- xref cache header size: **0x0**
- ROM payload size: **0x400000**

## Spot-checks performed

- `python3 scripts/ct_addr.py C2:8820 --rom "Chrono Trigger (USA).sfc"`
- `python3 scripts/ct_dump_range.py C2:8820 --end C2:8830 --rom "Chrono Trigger (USA).sfc" --bank-relative`
- `python3 scripts/ct_xrefs.py C2:8820 --mode calls --bank C2 --rom "Chrono Trigger (USA).sfc" --limit 5`

These checks confirmed the corrected bank-local caller resolution for the `C2:8820` settlement/search owner band and the new mapper/raw-offset reporting.
