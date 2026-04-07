# `passes/` Status

This directory is the active home for manifest-backed pass artifacts.

Subdirectories:
- `manifests/` — machine-readable pass manifests
- `disasm/` — manifest-backed pass disassembly notes
- `labels/` — manifest-backed pass label notes

Current boundary:
- manifest-backed canonical state currently reaches pass `306`
- continuation notes under `docs/sessions/` remain historical seam context, especially for the earlier C7 work summarized through note `100`
- active seam tooling still folds those frozen note-backed pages into `tools/cache/closed_ranges_snapshot_v1.json`

Use this directory for manifest-backed history and structured pass records.
For the current frontier, pair it with `README.md` and `docs/session_23_progress_report.md`.
