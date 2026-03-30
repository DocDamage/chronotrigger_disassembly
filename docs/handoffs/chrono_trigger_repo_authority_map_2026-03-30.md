# Chrono Trigger Repo Authority Map — 2026-03-30

## Purpose
This is the current repo-status index for active disassembly work.

Use it to answer:
- what is authoritative right now
- what is only historical reference
- what should be treated as archive material
- which old files are most likely to confuse the next worker

This file is current for the live seam at `C7:3A00..`.

---

## Active sources of truth

Read these first for any new seam session:
- `README.md`
- `docs/handoffs/chrono_trigger_master_handoff_session17.md`
- `docs/handoffs/chrono_trigger_resume_checklist_c7_3a00_43ff.md`
- `docs/sessions/chrono_trigger_session15_continue_notes_64.md`
- `tools/`
- `reports/` for the current block and manual-page artifacts

Active machine-readable state:
- `passes/manifests/` — canonical manifest-backed state through pass `191`
- `passes/disasm/` — active pass notes for manifest-backed work after the repo-first transition
- `passes/labels/` — active label notes for manifest-backed work after the repo-first transition
- `tools/cache/closed_ranges_snapshot_v1.json` — effective seam snapshot rebuilt from manifests plus frozen continuation-note pages

Active seam rule:
- pass manifests remain canonical only through pass `191`
- continuation notes are the operative state-of-record after pass `191`
- seam tooling now bridges that gap through the effective closed-range snapshot layer

---

## Historical Reference

These files are useful context, but they are not the current start point:

### `docs/handoffs/`
- older session handoffs are historical state captures
- `chrono_trigger_master_index_handoff.md` is an early-session topical index centered on pass-61-era work
- the `archive/` subtree is explicitly historical

### `docs/sessions/`
- session 13 and session 14 continuation notes remain valuable for earlier frontier history
- older `chrono_trigger_session15_continue_notes_*.md` files are the note-backed seam history behind the current frontier
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
- `toolkits/` — historical zip bundles only; use `tools/` for active tooling
- `emulators/bsnes-windows.zip` — convenience archive, not repo state
- `docs/rom_analysis/` — imported external dump material and assets

---

## High-Confusion Areas

These are the files or directories most likely to waste time if treated as current:

1. `docs/handoffs/chrono_trigger_master_index_handoff.md`
- important historical index
- not a current master handoff
- its “mandatory starting context” section reflects an early-session research posture, not the current seam workflow

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
- `passes/`: `71` files
- `docs/handoffs/`: `35` files
- `docs/sessions/`: `111` files
- `toolkits/`: `81` files

Interpretation:
- the repo contains a large amount of valuable history
- only a small subset is actually on the critical path for the next seam block

---

## Practical Read Order

If the next worker wants the minimum correct context:
1. `README.md`
2. `docs/handoffs/chrono_trigger_master_handoff_session17.md`
3. `docs/handoffs/chrono_trigger_resume_checklist_c7_3a00_43ff.md`
4. `docs/handoffs/chrono_trigger_revisit_backlog_from_session15_notes.md`
5. `docs/sessions/chrono_trigger_session15_continue_notes_64.md`

If the next worker needs historical context after that:
1. older `docs/sessions/chrono_trigger_session15_continue_notes_*.md`
2. earlier `docs/handoffs/chrono_trigger_master_handoff_session*.md`
3. `repo_sync/`
4. `disassembly/` and `labels/`

---

## Bottom Line

The repo does not need a blanket reread before continuing.

The correct working posture is:
- use the current handoff + checklist + continuation notes as the live lane
- treat older mirrors and sync packets as historical reference only
- treat toolkit zip archives and imported external dumps as archive material
