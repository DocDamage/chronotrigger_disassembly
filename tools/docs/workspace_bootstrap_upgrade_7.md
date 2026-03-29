# Workspace bootstrap upgrade 7

## Goal
Stop seam sessions from silently degrading into ROM-only caller ownership when the local workspace is missing the checked-out repo manifest set.

## Problem
The current seam cache/bootstrap flow assumes `passes/manifests` already exists locally. When the workspace only has the ROM and not the full branch checkout, seam analysis can still proceed ROM-first, but caller ownership becomes weaker because the manifest-backed closed-range layer is not fully available.

## Fix strategy
Use a new first-step wrapper before seam work:

1. **Try a full local checkout/update of the repo branch**
2. If that fails, **restore `passes/manifests` from a manifest bundle/zip/directory source**
3. Only then, **ensure seam cache**
4. If neither full checkout nor manifest bootstrap succeeds, **fail fast** instead of silently accepting degraded ownership

## New script
- `tools/scripts/prepare_seam_workspace_v1.py`

## What it does
- Verifies whether `passes/manifests` exists locally and contains at least a configurable minimum number of pass manifests
- Attempts a real git checkout/update of `live-work-from-pass166`
- Falls back to restoring manifests from one or more bundle sources
- Rebuilds or verifies the raw xref index and closed-range snapshot once the workspace is ready
- Exits nonzero if the workspace is still not ready

## Supported fallback sources
The script accepts repeated `--manifest-source` arguments. Each source may be:
- a directory containing `passes/manifests`
- a directory containing a `manifests` folder somewhere inside it
- a `.zip` bundle containing `passes/manifests`
- a tar/tar.gz bundle containing `passes/manifests`

## Recommended usage
```bash
python tools/scripts/prepare_seam_workspace_v1.py \
  --repo-root . \
  --repo-url https://github.com/DocDamage/chronotrigger_disassembly.git \
  --branch live-work-from-pass166 \
  --rom "Chrono Trigger (USA).sfc" \
  --manifests-dir passes/manifests \
  --cache-dir tools/cache \
  --minimum-manifests 100 \
  --manifest-source ./bootstrap/ct_manifests_bundle.zip \
  --json
```

## After it succeeds
Run the normal seam block flow:
```bash
python tools/scripts/run_seam_block_v1.py \
  --rom "Chrono Trigger (USA).sfc" \
  --start C4:8700 \
  --pages 10 \
  --manifests-dir passes/manifests \
  --cache-dir tools/cache \
  --dead-ranges-config tools/config/c3_dead_ranges_v1.json \
  --json > tools/cache/block_c4_8700.json
```

## Why this is better
- Prefers the strongest mode every session: real local checkout
- Keeps a practical fallback when git/network/workspace state is bad
- Prevents accidental silent downgrade into weaker caller-ownership analysis
- Fits the existing seam toolkit instead of replacing it

## Operational note
This does not guarantee a remote clone is always possible in every execution environment. What it guarantees is that the workflow will **try checkout first**, **use manifest bootstrap second**, and **refuse to proceed silently** if neither works.
