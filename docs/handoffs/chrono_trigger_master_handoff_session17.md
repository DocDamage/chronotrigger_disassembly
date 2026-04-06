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

- Latest continuation note: `docs/sessions/chrono_trigger_session15_continue_notes_82.md`
- Latest closed block: **`C7:D000..C7:D9FF`**
- Current live seam: **`C7:DA00..`**
- Continuation run closed so far: **69 ten-page blocks / 690 pages**
- Promotion count across that continuation run: **2** (passes 192-193: C7:B000-B1FF, C7:C300-C4FF)
- Effective closed-range snapshot after refresh: **967 ranges** = **67** manifest-backed + **900** note-backed frozen pages across `C3/C4/C5/C6/C7`

That remains harsh, but it is still the correct read.
The repo has continued to preserve a noisy seam honestly instead of polluting the label set with caller-backed bait entries.

---

## What changed since Session 16 handoff

Session 16 handoff ended with:
- live seam **`C7:0800..`**
- latest continuation note **`59`**

**MAJOR BREAKTHROUGH: First C7 bank promotions after 170+ pages!**

Since then, the repo has closed **notes 60 through 80**:
- **21 additional ten-page seam blocks**
- range covered: **`C7:0800..C7:C5FF`**
- net result: **2 promotions** (passes 192-193) — historic first code in C7 bank

**Historic structural events:**

### 1. **PASS 192: C7:C300..C7:C4FF promoted** 🎉
- **Strategic jump success**: Skipped from `C7:B200` directly to `C7:C300`
- **4 targets promoted**: C7:C3AE, C7:C388, C7:C31D, C7:C4AA
- **Evidence**: 8 prologues, multiple RTS/RTL, cross-bank calls from 10 banks
- **Status**: First code promotion in upper C7 bank after 170+ pages

### 2. **PASS 193: C7:B000..C7:B1FF promoted** 🎉
- **Validates C7:C300**: Strong anchors from C7:C000..C7:C2FF and C7:7400..C7:74FF
- **8 targets promoted**: B111, B188, B0B4, B0DF, B09E, B0F2, B115, B195
- **Circular dependency broken**: C7:C300 promotion provided strong anchors to validate C7:B100

### 3. **Bridge Region Analysis: C7:B200..C7:B9FF**
- Identified **C7:B961** (JSR $D0A0, score 4) as strong bridge candidate
- **C7:BC00..C7:C5FF block** reached the promoted C7:C300 region
- **Strongest candidate yet**: C7:C5AC with **score 6** — highest backtrack score in C7 bank!

### 4. **Orphan Block Identified: C7:C200-C2FF**
- Region shows code-like patterns but **NO external anchors**
- Blocking contiguous C000-C500 promotion
- Resolution path: promote adjacent regions (C100 or C500) first

---

## What the latest work proves

### 1. The early `C7` tail is now stronger negative evidence, not weaker
From `C7:0800` through `C7:39FF`, the project still has not found one candidate where:
- caller quality held up
- start-byte quality held up
- local body structure held up

That is no longer “maybe the next block opens up.”
It is now repeated evidence across dead-zero fields, mixed patterned tables, and branch-fed/control pockets.

### 2. **BREAKTHROUGH: C7 bank contains significant code in upper region**
- `C7:0E00..C7:1BFF` is confirmed dead-zero / low-ingress corridor
- **Upper C7 discovered**: `C7:B000..C7:C500` contains active executable code
- **Promoted regions**: B000-B1FF (512 bytes), C300-C4FF (512 bytes)
- **Gap remains**: B200-C2FF contains code-like patterns but needs validation

### 3. Score-6 backtracks can indicate real code with strong anchors
**C7:C5AC is the strongest candidate yet:**
- **Score 6** with `REP #$20` prologue
- Connected to local cluster C7:C59D-C7:C5B5 (score 4, 2 calls, 4 branches, 1 return)
- Weak anchor from C7:C275 (currently unresolved)

**Historical note**: Early C7 score-6 candidates (2DE6, 2F33, 32CE) failed because they lacked:
- Strong caller chains from resolved code
- Cross-bank validation
- Prologue evidence (PHP/PHB/REP)

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

## Latest closed block: `C7:D000..C7:D9FF`

Extended C7 coverage through D9FF, found **third score-6 candidate** and **JSR prologue pattern**!

Block result:
- **10 pages processed**
- **0 promotions**
- new live seam: **`C7:DA00..`**

**Major findings:**
- **C7:D363**: Score-6 candidate (0x0B = PHD start) — third score-6 in upper C7!
- **C7:D1ED**: Score-4 candidate with **JSR prologue** (0x20) — subroutine call structure
- **C7:D000**: Rejected despite **19 xref hits** — structure validation failure

**Score-6 Candidates in Upper C7:**
| Address | Score | Start Byte | Instruction | Anchor |
|---------|-------|------------|-------------|--------|
| C7:C5AC | **6** | 0xC2 | REP #$20 | Weak |
| C7:D363 | **6** | 0x0B | PHD | Suspect |

**JSR Prologue Discovery:**
- C7:D1DF starts with `JSR $15EE` (0x20 0xEE 0x15)
- Indicates callable subroutine structure
- Suspect anchor from C7:985A (closed data range)

**Contiguity status:**
- D000: **REJECTED** (19 hits but bad structure) — another gap
- D100-D3FF: Strong candidates but suspect anchors
- D400-D9FF: Mixed/control pockets

Read these artifacts:
- `docs/sessions/chrono_trigger_session15_continue_notes_82.md`
- `reports/c7_d000_d9ff_seam_block.json`
- `reports/c7_d300_d3ff_backtrack.json`

---

## What to do next

### Immediate next block
Process exactly one ten-page seam block:
- **`C7:DA00..C7:E3FF`**

Start with:
```bash
python tools/scripts/audit_branch_state_v1.py
python tools/scripts/audit_pass_manifests_v1.py
python tools/scripts/ensure_seam_cache_v1.py --rom 'rom/Chrono Trigger (USA).sfc'
python tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:DA00 --pages 10 --json > reports/c7_da00_e3ff_seam_block.json
python tools/scripts/render_seam_block_report_v1.py --input reports/c7_da00_e3ff_seam_block.json --output reports/c7_da00_e3ff_seam_block.md
```

Then:
1. Read the rendered block report
2. Identify pages marked `manual_owner_boundary_review`
3. Run owner-backtrack scans for those pages
4. Run anchor reports for targets worth defending
5. Look for **strong anchors** to backlog candidates: C5AC, D363, D1ED, CEEB
6. Write `docs/sessions/chrono_trigger_session15_continue_notes_83.md`

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
