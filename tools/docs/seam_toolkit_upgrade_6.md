# Seam toolkit upgrade 6

## Why this upgrade exists
The previous toolkit upgrade fixed the biggest one-page bottleneck by adding a reusable raw-xref index and closed-range snapshot support.

The next practical bottleneck showed up immediately afterward:
- cache files disappear from the workspace between continuation runs
- page sweeps still require repetitive one-page orchestration by hand
- continuation notes still require extra manual stitching even when the underlying signals are already computed

This upgrade fixes the operational gap instead of touching the promotion rules.

## New scripts
- `tools/scripts/ensure_seam_cache_v1.py`
- `tools/scripts/run_seam_block_v1.py`
- `tools/scripts/render_seam_block_report_v1.py`

## What changed
### 1) Self-healing cache bootstrap
`ensure_seam_cache_v1.py` makes the seam cache reusable without assuming it already exists.

It will:
- create the cache directory if missing
- rebuild the raw-xref index if missing
- rebuild the raw-xref index if the ROM SHA changed
- create the closed-range snapshot if missing

Example:
```bash
python tools/scripts/ensure_seam_cache_v1.py \
  --rom "Chrono Trigger (USA).sfc" \
  --manifests-dir passes/manifests \
  --cache-dir tools/cache \
  --json
```

### 2) Block-level seam runner
`run_seam_block_v1.py` runs the corrected page flow over a contiguous block of pages while reusing the same cache.

This removes the need to hand-run the page flow ten times for every continuation block.

Example:
```bash
python tools/scripts/run_seam_block_v1.py \
  --rom "Chrono Trigger (USA).sfc" \
  --start C4:2D00 \
  --pages 10 \
  --manifests-dir passes/manifests \
  --cache-dir tools/cache \
  --dead-ranges-config tools/config/c3_dead_ranges_v1.json \
  --json
```

### 3) Markdown block renderer
`render_seam_block_report_v1.py` turns block JSON output into readable Markdown.

This is meant for:
- raw continuation reports
- page-by-page triage summaries
- quicker continuation-note drafting

Example:
```bash
python tools/scripts/render_seam_block_report_v1.py \
  --input tools/cache/block_c4_2d00.json \
  --output tools/cache/block_c4_2d00.md
```

## Practical impact
This upgrade is about **staying fast even after the workspace forgets the cache**.

You no longer need to manually rebuild the same seam state every time the environment drops out.

The new normal flow is:
1. ensure the cache exists
2. run one block sweep
3. render the block report
4. review only the real near-miss pages

## Recommended workflow
```bash
python tools/scripts/ensure_seam_cache_v1.py \
  --rom "Chrono Trigger (USA).sfc" \
  --manifests-dir passes/manifests \
  --cache-dir tools/cache

python tools/scripts/run_seam_block_v1.py \
  --rom "Chrono Trigger (USA).sfc" \
  --start C4:2D00 \
  --pages 10 \
  --manifests-dir passes/manifests \
  --cache-dir tools/cache \
  --dead-ranges-config tools/config/c3_dead_ranges_v1.json \
  --json > tools/cache/block_c4_2d00.json

python tools/scripts/render_seam_block_report_v1.py \
  --input tools/cache/block_c4_2d00.json \
  --output tools/cache/block_c4_2d00.md
```

## What this upgrade does not change
It does **not** loosen any seam standards:
- repeated weak hits are still only near-misses
- local structure is still not ownership
- hard-bad and soft-bad starts still matter
- no start gets promoted unless caller quality, start-byte quality, and local ownership all agree cleanly
