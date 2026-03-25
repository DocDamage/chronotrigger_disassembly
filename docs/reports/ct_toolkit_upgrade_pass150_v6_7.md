# Toolkit Upgrade — Pass 150 / v6.7

## What changed
- refreshed the packaged toolkit forward from the old pass-145 release state to the current **pass 150** workspace state
- bumped the toolkit version to **v6.7**
- added a new handoff-generation lane:
  - `scripts/ct_generate_master_handoff.py`
  - `windows/run_generate_master_handoff.bat`
- updated README and manifest docs for the new handoff lane
- updated doctor wrapper coverage so the new handoff wrapper is part of the checked toolkit surface
- regenerated toolkit doctor, smoke, and release-audit outputs against the current pass-150 seam

## Why this upgrade matters
The static disassembly moved five more passes after the last packaged toolkit refresh, which meant the downloadable toolkit had drifted behind the real workspace.

This upgrade fixes that drift and makes full-session restart packets easier to generate from inside the toolkit itself.

## Current released state
- latest pass: **150**
- toolkit version: **v6.7**
- live seam: **`C2:F2F3..C2:F360`**
- toolkit doctor: **100.0%**
- release audit: **100.0%**

## Packaged release
- `ct_disasm_toolkit_v6_7_pass150_upgraded.zip`
