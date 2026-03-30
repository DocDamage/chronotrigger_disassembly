# Pass manifests

Each pass should have one machine-readable manifest in this folder.
Use tools/config/pass_manifest_schema.json as the schema source of truth.

Current boundary note:
- manifest-backed canonical state currently stops at pass `191`
- continuation work after pass `191` is note-backed under `docs/sessions/`
- current seam tooling bridges manifests plus frozen continuation-note pages through `tools/cache/closed_ranges_snapshot_v1.json`

Do not assume this directory alone captures the current live seam.
