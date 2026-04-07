# Chrono Trigger Repo Authority Map - 2026-03-30

## Purpose
This is the current repo-status index for active disassembly work.

Use it to answer:
- what is authoritative right now
- what is only historical reference
- what should be treated as archive material
- which old files are most likely to confuse the next worker

This file reflects the current repo posture after Session 23, with the active manifest-backed frontier at `C0:7800..`.

---

## Active sources of truth

Read these first for any new seam session:
- `README.md`
- `docs/session_23_progress_report.md`
- latest relevant `passes/manifests/pass*.json`
- `tools/`
- `reports/` for current generated artifacts when they support the active target bank

Active machine-readable state:
- `passes/manifests/` - canonical manifest-backed state through pass `306`
- `passes/disasm/` - active pass notes for manifest-backed work after the repo-first transition
- `passes/labels/` - active label notes for manifest-backed work after the repo-first transition
- `tools/cache/closed_ranges_snapshot_v1.json` - effective seam snapshot rebuilt from manifests plus frozen continuation-note pages for historical context and caller scoring

Active seam rule:
- pass manifests are canonical for the current frontier through pass `306`
- continuation notes remain valuable historical context, especially for the earlier C7 seam, but they are not the primary current state source
- seam tooling still bridges the older note-backed closures into the effective closed-range snapshot layer

---

## Historical Reference

These files are useful context, but they are not the current start point:

### `docs/handoffs/`
- older session handoffs are historical state captures
- `chrono_trigger_master_index_handoff.md` is an early-session topical index centered on pass-61-era work
- the `archive/` subtree is explicitly historical

### `docs/sessions/`
- session 13 and session 14 continuation notes remain valuable for earlier frontier history
- `chrono_trigger_session15_continue_notes_*.md` files are the note-backed C7 history behind the current frontier
- older `chrono_trigger_next_session_start_here_pass*.md` files are historical pass snapshots, not current launch docs

### `docs/reports/`
- toolkit doctor reports, completion reports, and old raw seam reports are reference material
- they capture what the repo believed at older passes; do not treat them as current seam instructions

### `repo_sync/`
- bootstrap and transfer snapshots from the repo-first migration phase
- useful for reconstructing how pass artifacts entered the repo
- not part of the active seam workflow

### `disassembly/` and `labels/`
- legacy pass-note mirrors grouped by pass ranges
- useful as older historical copies
- not the active path for current manifest-backed work

---

## Archive-Only Material

These should not drive current decisions:
- `toolkits/` - historical zip bundles and rebuilt release bundles; use `tools/` for active tooling and `reports/toolkit_release_manifest_*.md` for release metadata
- `emulators/bsnes-windows.zip` - convenience archive, not repo state
- `docs/rom_analysis/` - imported external dump material and assets

---

## High-Confusion Areas

These are the files or directories most likely to waste time if treated as current:

1. `docs/handoffs/chrono_trigger_master_index_handoff.md`
- important historical index
- not a current master handoff
- its "mandatory starting context" section reflects an early-session research posture, not the current seam workflow

2. `repo_sync/pass*/chrono_trigger_next_session_start_here_pass*.md`
- historical transition snapshots only
- they describe seams from passes `163..171`, not the current frontier

3. `disassembly/` and `labels/`
- older mirror trees stop at pass `163`
- current manifest-backed pass notes live under `passes/disasm/` and `passes/labels/`

4. `toolkits/*.zip`
- historical releases and working bundles
- not authoritative for current repo tooling behavior

---

## Repo Status Summary

Current directory counts from the audit:
- `repo_sync/`: `42` files
- `disassembly/`: `164` files
- `labels/`: `165` files
- `passes/`: `186` files
- `docs/handoffs/`: `35` files
- `docs/sessions/`: `147` files
- `toolkits/`: `82` files

Interpretation:
- the repo contains a large amount of valuable history
- only a small subset is actually on the critical path for the next seam block

---

## Practical Read Order

If the next worker wants the minimum correct context:
1. `README.md`
2. `docs/session_23_progress_report.md`
3. latest relevant `passes/manifests/pass*.json`
4. `tools/`
5. `reports/` that directly support the current bank/target

If the next worker needs historical context after that:
1. `docs/sessions/chrono_trigger_session15_continue_notes_*.md`
2. earlier `docs/handoffs/chrono_trigger_master_handoff_session*.md`
3. `repo_sync/`
4. `disassembly/` and `labels/`

---

## Bottom Line

The repo does not need a blanket reread before continuing.

The correct working posture is:
- use the current README + Session 23 progress report + manifest-backed pass artifacts as the live lane
- treat older mirrors and sync packets as historical reference only
- treat toolkit zip archives and imported external dumps as archive material
