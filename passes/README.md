# `passes/` Status

This directory is the active home for manifest-backed pass artifacts.

Subdirectories:
- `manifests/` — machine-readable pass manifests
- `disasm/` — manifest-backed pass disassembly notes
- `labels/` — manifest-backed pass label notes

Current boundary:
- manifest-backed canonical state stops at pass `191`
- continuation work after pass `191` lives under `docs/sessions/`
- active seam tooling bridges that gap through `tools/cache/closed_ranges_snapshot_v1.json`

Use this directory for manifest-backed history and structured pass records.
Do not assume it alone captures the current live seam.
