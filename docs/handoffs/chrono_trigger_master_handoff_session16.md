# Chrono Trigger Disassembly — Master Handoff Session 16

## Repo / branch / ROM
- Repo: `DocDamage/chronotrigger_disassembly`
- Working branch: `live-work-from-pass166`
- ROM: `rom/Chrono Trigger (USA).sfc`
- Manifest-backed canonical state: still stops at **pass 191**
- Operative state beyond pass 191: **continuation notes** under `docs/sessions/`
- Effective seam cache state: `tools/cache/closed_ranges_snapshot_v1.json` now auto-bridges manifests plus frozen continuation-note pages

---

## Current top-line state

- Latest continuation note: `docs/sessions/chrono_trigger_session15_continue_notes_53.md`
- Latest closed block: **`C6:C200..C6:CBFF`**
- Current live seam: **`C6:CC00..`**
- Continuation run closed so far: **40 ten-page blocks / 400 pages**
- Promotion count across that continuation run: **0**
- Effective closed-range snapshot after repair: **705 ranges** = **65** manifest-backed + **640** note-backed frozen pages across `C3/C4/C5/C6`

That sounds harsh, but it is the correct read.
The repo has now preserved a long mixed-content corridor honestly instead of polluting the label set with caller-backed bait entries.

---

## What changed since Session 15 handoff

Session 15 handoff ended with:
- live seam **`C5:6300..`**
- latest continuation note **`17`**

Since then, the repo has closed **notes 18 through 53**:
- **36 additional ten-page seam blocks**
- range covered: **`C5:6300..C6:CBFF`**
- net result: **zero promotions**

Important structural events in that run:
1. The seam crossed the bank boundary at **`C5:FA00..C6:03FF`** without producing a clean new executable lane.
2. The later `C6` stretch kept the same pattern seen in late `C5`: weak-only anchors, invalid companion targets, and dead/no-ingress pages.
3. No later block has overturned the conservative rule set captured in Session 15 handoff. The toolkit changes held up.

---

## What the latest work proves

### 1. This is a real mixed-content dead zone, not a missed easy win
From `C5:3B00` through `C6:CBFF`, the project has not found one candidate where:
- caller quality held up
- start-byte quality held up
- local body structure held up

That is now strong negative evidence, not just temporary uncertainty.

### 2. Score-6 backtracks are still not enough
The recent `C6` notes keep repeating the same lesson:
- a high backtrack score only says the bytes *before* the target can be partitioned into instruction boundaries
- it does **not** prove the target byte is a defensible owner start

### 3. Weak-only anchors were the dominant failure mode across the run
Recent manual-review pages kept collapsing because the best target was still only backed by:
- one weak caller from unresolved territory
- invalid overlap nearby
- mixed/data-looking bytes immediately after the target

That remains true for unresolved future territory.
But the pre-seam tooling repair is now done:
- callers that sit inside already frozen note-backed pages now downgrade to **suspect / resolved_data**
- they no longer default to **weak / unresolved** just because the manifest layer stops at `191`

### 4. Manifest backfill is still a separate task
The manifest layer still remains frozen at pass `191`.
But the active seam tooling no longer depends on that frozen boundary alone.
Current seam truth lives in:
- the continuation notes
- the seam-block reports
- the anchor/backtrack/flow artifacts in `reports/`
- the rebuilt effective closed-range snapshot in `tools/cache/closed_ranges_snapshot_v1.json`

Do not pretend the pass-manifest layer is current until a dedicated reconciliation pass happens.
Use the repaired snapshot layer for seam and anchor work meanwhile.

---

## Latest closed block: `C6:C200..C6:CBFF`

This is the current frontier block from `docs/sessions/chrono_trigger_session15_continue_notes_53.md`.

Block result:
- **10 pages processed**
- **0 promotions**
- new live seam: **`C6:CC00..`**

Most important page outcomes:
- `C6:C700` was the strongest honest near-miss in the block, but `C720` still had only weak unresolved callers
- `C6:CA00` carried the strongest reject pressure in the block because hard-bad zero-start targets dominated the page
- `C6:C400` had some mixed-lane traffic, but it never escalated to manual-owner review and still froze honestly

Read these artifacts first if you need the exact evidence:
- `docs/sessions/chrono_trigger_session15_continue_notes_53.md`
- `reports/c6_c200_cbff_seam_block.json`
- `reports/c6_c200_cbff_seam_block.md`

---

## What to do next

### Immediate next block
Process exactly one ten-page seam block:
- **`C6:CC00..C6:D5FF`**

Start with:
```bash
python3 tools/scripts/audit_branch_state_v1.py
python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:CC00 --pages 10 --json > reports/c6_cc00_d5ff_seam_block.json
python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_cc00_d5ff_seam_block.json --output reports/c6_cc00_d5ff_seam_block.md
```

Then:
1. read the rendered block report
2. identify only the pages marked `manual_owner_boundary_review`
3. run owner-backtrack scans for those pages
4. run anchor reports only for targets that still look worth defending after byte review; `build_call_anchor_report_v3.py` now uses the rebuilt `tools/cache/closed_ranges_snapshot_v1.json` by default
5. write `docs/sessions/chrono_trigger_session15_continue_notes_54.md`

### Promotion rule
Only promote if all three converge:
- caller is from resolved code
- target byte is a defensible start
- first body bytes read as coherent code without immediate contamination

If any of those fail, freeze and advance the seam.

### What not to do next
- do not backfill manifests during this block
- do not reopen older `C5`/early `C6` near-miss pages without genuinely new evidence
- do not promote page-hot interior landings just because the block has weak traffic

---

## Read order for the next worker

1. `docs/handoffs/chrono_trigger_repo_authority_map_2026-03-30.md`
2. `docs/handoffs/chrono_trigger_master_handoff_session16.md`
3. `docs/sessions/chrono_trigger_session15_continue_notes_53.md`
4. `docs/handoffs/chrono_trigger_resume_checklist_c6_cc00_d5ff.md`
5. `docs/handoffs/chrono_trigger_revisit_backlog_from_session15_notes.md` (only if new caller-quality evidence appears)
6. `reports/c6_c200_cbff_seam_block.md`

---

## Bottom line

The repo is current and internally consistent.
The live frontier is **`C6:CC00..`**.
The honest interpretation of the last 400 seam pages is still: **mixed-content corridor, zero safe promotions, keep moving conservatively**.
The important difference now is that the seam tools are no longer blind to the already closed note-backed pages behind that frontier.
