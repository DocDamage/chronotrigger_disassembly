# Seam shape triage upgrade 4

## Why this upgrade exists
Recent continuation passes exposed the same bottleneck over and over:
- the seam workflow kept rescanning the whole ROM for raw callers on every page
- local workspace runs did not always have the full manifest history mirrored
- block sweeps were being done by hand because the one-page flow was fine semantically but slow operationally

This upgrade focuses on **throughput without relaxing standards**.

## New scripts
- `tools/scripts/xref_index_utils_v1.py`
- `tools/scripts/build_raw_xref_index_v1.py`
- `tools/scripts/export_closed_ranges_snapshot_v1.py`
- `tools/scripts/scan_range_entry_callers_v3.py`
- `tools/scripts/score_raw_xref_context_v3.py`
- `tools/scripts/run_c3_candidate_flow_v7.py`

## What changed
### 1) Reusable raw xref index
`build_raw_xref_index_v1.py` scans the ROM once and writes a reusable caller index.

This means local seam passes stop paying the full-ROM scan cost every single page.

Example:
```bash
python tools/scripts/build_raw_xref_index_v1.py \
  --rom "Chrono Trigger (USA).sfc" \
  --output tools/cache/chrono_trigger_raw_xref_index_v1.json
```

### 2) Closed-range snapshot export
`export_closed_ranges_snapshot_v1.py` collapses all manifest closed ranges into one compact snapshot file.

This is useful when the local environment has the manifest tree available once, but future runs should avoid reopening every manifest repeatedly.

Example:
```bash
python tools/scripts/export_closed_ranges_snapshot_v1.py \
  --manifests-dir passes/manifests \
  --output tools/cache/closed_ranges_snapshot_v1.json
```

### 3) Xref-aware v3 scanners
`scan_range_entry_callers_v3.py` and `score_raw_xref_context_v3.py` now accept:
- `--xref-index`
- `--closed-ranges-snapshot`

They still fall back to the older behavior when those files are not present.

### 4) v7 one-page flow
`run_c3_candidate_flow_v7.py` is the corrected successor to v5 for local seam work.

It preserves the same semantics but can reuse:
- raw xref index
- closed-range snapshot

Example:
```bash
python tools/scripts/run_c3_candidate_flow_v7.py \
  --rom "Chrono Trigger (USA).sfc" \
  --range C3:FB00..C3:FBFF \
  --manifests-dir passes/manifests \
  --closed-ranges-snapshot tools/cache/closed_ranges_snapshot_v1.json \
  --xref-index tools/cache/chrono_trigger_raw_xref_index_v1.json \
  --dead-ranges-config tools/config/c3_dead_ranges_v1.json \
  --json
```

## Practical impact
This upgrade is about **speeding honest rejection**:
- hard-bad pages get rejected faster
- repeated-hit near-miss pages get summarized faster
- local-control-only pages get identified faster
- block-level continuation notes become easier to generate without relaxing promotion standards

## What this upgrade does not change
It does **not** loosen the seam rules:
- caller quality still matters
- target start quality still matters
- local structure still does not equal ownership
- repeated weak hits are still only near-misses until a real owner boundary holds
