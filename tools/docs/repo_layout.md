# Repo Layout Recommendation

## Source of truth
The GitHub repository is the canonical workspace.
Chat exports are snapshots, not the primary source of truth.

## Recommended top-level structure
- `tools/` — toolkit source and config
- `handoffs/` — session handoff documents
- `passes/disasm/` — per-pass narrative notes
- `passes/labels/` — per-pass label notes
- `passes/manifests/` — machine-readable pass manifests
- `reports/` — completion, validation, doctor, and progress reports
- `reference/` — stable reverse-engineering reference material
- `scratch/` — temporary/generated scratch data that can be regenerated

## Do not commit
- ROM images
- disposable extracted junk
- machine-local caches
- bulky generated outputs that have no review value
