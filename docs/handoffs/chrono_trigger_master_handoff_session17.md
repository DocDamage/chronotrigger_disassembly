# Chrono Trigger Disassembly — Master Handoff Session 17

## Repo / branch / ROM
- Repo: `DocDamage/chronotrigger_disassembly`
- Working branch: `live-work-from-pass166`
- ROM: `rom/Chrono Trigger (USA).sfc`
- Manifest-backed canonical state: still stops at **pass 191**
- Operative state beyond pass 191: **continuation notes** under `docs/sessions/`
- Effective seam cache state: `tools/cache/closed_ranges_snapshot_v1.json` now auto-bridges manifests plus frozen continuation-note pages

---

## Current top-line state

- Latest continuation note: `docs/sessions/chrono_trigger_session15_continue_notes_64.md`
- Latest closed block: **`C7:3000..C7:39FF`**
- Current live seam: **`C7:3A00..`**
- Continuation run closed so far: **51 ten-page blocks / 510 pages**
- Promotion count across that continuation run: **0**
- Effective closed-range snapshot after refresh: **815 ranges** = **65** manifest-backed + **750** note-backed frozen pages across `C3/C4/C5/C6/C7`

That remains harsh, but it is still the correct read.
The repo has continued to preserve a noisy seam honestly instead of polluting the label set with caller-backed bait entries.

---

## What changed since Session 16 handoff

Session 16 handoff ended with:
- live seam **`C7:0800..`**
- latest continuation note **`59`**

Since then, the repo has closed **notes 60 through 64**:
- **5 additional ten-page seam blocks**
- range covered: **`C7:0800..C7:39FF`**
- net result: **zero promotions**

Important structural events in that run:
1. `C7:0E00..C7:1BFF` resolved into an extended dead-zero / low-ingress corridor rather than a hidden executable lane.
2. `C7:1C00..C7:25FF` produced only one manual-review page, and it still collapsed on table-like byte structure before anchor follow-up.
3. `C7:2600..C7:2FFF` was the busiest late-session flare-up, with five manual-review pages and multiple score-6 backtracks, but every defended target still failed on local byte quality.
4. `C7:3000..C7:39FF` cooled again; the only anchor-worthy target in that stretch was `C7:3120`, and it still remained just **weak / unresolved**.

---

## What the latest work proves

### 1. The early `C7` tail is now stronger negative evidence, not weaker
From `C7:0800` through `C7:39FF`, the project still has not found one candidate where:
- caller quality held up
- start-byte quality held up
- local body structure held up

That is no longer “maybe the next block opens up.”
It is now repeated evidence across dead-zero fields, mixed patterned tables, and branch-fed/control pockets.

### 2. The dead-zero corridor extends much deeper into `C7` than the Session 16 handoff captured
The session now materially strengthens the read that:
- `C7:0E00..C7:1BFF` is a dead-zero / low-ingress corridor
- later `C7` pages may look more active, but they still do not resolve into owner-worthy code

### 3. Score-6 backtracks are still not enough
The recent notes keep repeating the same lesson:
- a high backtrack score only says the bytes *before* the target can be partitioned into instruction boundaries
- it does **not** prove the target byte is a defensible owner start

Recent examples:
- `C7:2DE6`
- `C7:2F33`
- `C7:32CE`

All of them looked arguable until the actual bytes were read.

### 4. The repaired snapshot layer is still doing real work
The new `C7` pages reinforce the value of the note-backed closed-range snapshot:
- callers from already frozen pages continue to downgrade to **suspect / resolved_data**
- they no longer inflate page heat into fake weak-owner support

Recent example:
- `C7:2C90` drew the busiest support in its page, but all of it came from already frozen pages behind the seam

### 5. Manifest backfill is still a separate task
The manifest layer still remains frozen at pass `191`.
But active seam truth continues to live in:
- the continuation notes
- the seam-block reports
- page-specific backtrack / anchor artifacts
- the rebuilt effective closed-range snapshot in `tools/cache/closed_ranges_snapshot_v1.json`

Do not pretend the pass-manifest layer is current until a dedicated reconciliation pass happens.
Use the repaired snapshot layer for seam and anchor work meanwhile.

---

## Latest closed block: `C7:3000..C7:39FF`

This is the current frontier block from `docs/sessions/chrono_trigger_session15_continue_notes_64.md`.

Block result:
- **10 pages processed**
- **0 promotions**
- new live seam: **`C7:3A00..`**

Most important page outcomes:
- `C7:3100` was the strongest honest near-miss in the block because `C7:3120` survived long enough to justify anchor follow-up, but it still remained only **weak / unresolved**
- `C7:3200` carried the strongest reject signal because it combined real ingress and good backtracks with branch-fed/control-pocket structure, yet still failed under reject-heavy byte quality
- two pages in this block reached `manual_owner_boundary_review`, and both collapsed before any promotion case could form

Read these artifacts first if you need the exact evidence:
- `docs/sessions/chrono_trigger_session15_continue_notes_64.md`
- `reports/c7_3000_39ff_seam_block.json`
- `reports/c7_3000_39ff_seam_block.md`

---

## What to do next

### Immediate next block
Process exactly one ten-page seam block:
- **`C7:3A00..C7:43FF`**

Start with:
```bash
python3 tools/scripts/audit_branch_state_v1.py
python3 tools/scripts/audit_pass_manifests_v1.py
python3 tools/scripts/ensure_seam_cache_v1.py --rom 'rom/Chrono Trigger (USA).sfc'
python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:3A00 --pages 10 --json > reports/c7_3a00_43ff_seam_block.json
python3 tools/scripts/render_seam_block_report_v1.py --input reports/c7_3a00_43ff_seam_block.json --output reports/c7_3a00_43ff_seam_block.md
```

Then:
1. read the rendered block report
2. identify only the pages marked `manual_owner_boundary_review`
3. run owner-backtrack scans for those pages
4. run anchor reports only for targets that still look worth defending after byte review; `build_call_anchor_report_v3.py` now uses the rebuilt `tools/cache/closed_ranges_snapshot_v1.json` by default
5. write `docs/sessions/chrono_trigger_session15_continue_notes_65.md`

### Promotion rule
Only promote if all three converge:
- caller is from resolved code
- target byte is a defensible start
- first body bytes read as coherent code without immediate contamination

If any of those fail, freeze and advance the seam.

### What not to do next
- do not backfill manifests during this block
- do not reopen older `C5`/`C6` or early-`C7` near-miss pages without genuinely new evidence
- do not promote page-hot interior landings just because the block has weak traffic or a high backtrack score

---

## Read order for the next worker

1. `docs/handoffs/chrono_trigger_repo_authority_map_2026-03-30.md`
2. `docs/handoffs/chrono_trigger_master_handoff_session17.md`
3. `docs/sessions/chrono_trigger_session15_continue_notes_64.md`
4. `docs/handoffs/chrono_trigger_resume_checklist_c7_3a00_43ff.md`
5. `docs/handoffs/chrono_trigger_revisit_backlog_from_session15_notes.md` (only if new caller-quality evidence appears)
6. `reports/c7_3000_39ff_seam_block.md`

---

## Bottom line

The repo is current and internally consistent.
The live frontier is **`C7:3A00..`**.
The honest interpretation of the last 510 seam pages is still: **zero safe promotions, increasing negative evidence, keep moving conservatively**.
The new nuance is that the project is now seeing both:
- a confirmed dead-zero corridor in early `C7`
- later patterned mixed-content/control pockets that still fail even when they look more executable on first pass
