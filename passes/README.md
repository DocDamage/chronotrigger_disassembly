# `passes/` Status

This directory is the active home for manifest-backed pass artifacts.

Subdirectories:
- `manifests/` — canonical Schema v2 pass manifests (`pass0001.json`..`pass1229.json`) and `legacy/` historical source archive (1,000 files)
- `disasm/` — manifest-backed pass disassembly notes
- `labels/` — manifest-backed pass label notes

Current boundary:
- Canonical manifest-backed state reaches pass `1229` with 961 canonical manifests preserving all 1,105 historical claims. Ownership normalization adds 184 non-overlapping residual records, for 1,289 canonical records total (1,061 active and 228 superseded provenance records).
- Zero-loss conservation across all 1,000 baseline source files is verified and maintained by `tools/scripts/compare_manifest_range_inventory.py`.
- Unresolved range conflicts: 0.

Use this directory for manifest-backed history and structured pass records.
