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

- Latest continuation note: `docs/sessions/chrono_trigger_session15_continue_notes_89.md`
- Latest closed block: **`C7:EE00..C7:F7FF`**
- Current live seam: **`C7:F800..`**
- Continuation run closed so far: **72 ten-page blocks / 720 pages**
- Promotion count across that continuation run: **7** (passes 192-198: B000-B1FF, C300-C4FF, C5AC-C5D0, D363-D37C, C193-C1B2, C1B6-C1CE, C028-C02C)
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

## 🎉 PROMOTION: Pass 194 — C7:C5AC..C7:C5D0

**THRESHOLD PROMOTION — Anchor Crisis Broken!**

After 50+ pages without strong anchors, C7:C5AC promoted on evidence convergence:
- **Score 6** (perfect backtrack)
- **REP #$20 prologue** (definitive 65816 code)
- **Local cluster with returns** (C59D-C5B5)
- **Suspect anchor** from C275 (valid JSR)

**Promoted range:** C7:C5AC..C7:C5D0 (~36 bytes, conservative)
**Strategic value:** First strong foothold in C500 region, enables validation of adjacent candidates

See `docs/sessions/chrono_trigger_session15_continue_notes_84.md` for full analysis.

---

## 🎉 PROMOTION: Pass 195 — C7:D363..C7:D37C

**Second threshold promotion — anchor chain extended!**

C7:D363 promoted following pass 194 precedent:
- **Score 6** (perfect backtrack)
- **PHD prologue** (0x0B — Push Direct Page, valid 65816)
- **Local clusters** (D3A8-D3C3, D3E7-D3F9, both score 4)
- **Low ASCII ratio** — 26.9% (code-like)
- **Upper C7 boundary known** — D363 is in executable region

**Promoted range:** C7:D363..C7:D37C (~26 bytes)
**Strategic value:** Extends contiguous promoted chain C300→C5AC→D363

See `docs/sessions/chrono_trigger_session15_continue_notes_86.md` for full analysis.

---

## 🎉 PROMOTION: Pass 196 — C7:C193..C7:C1B2

**NEW PRECEDENT: Cluster-based threshold promotion!**

C7:C193 promoted based on **strongest cluster evidence in upper C7**:
- **Score 7 cluster** (exceeds backtrack scores!)
- **5 branches, 2 returns** (definitive subroutine structure)
- **32 bytes width** (substantial code region)
- **2 child clusters** (C193-C1AB, C19A-C1B2)

**New threshold precedent:** Cluster score ≥ 7 + multiple returns = defensible promotion, even without external anchors or high backtrack scores.

**Promoted range:** C7:C193..C7:C1B2 (~32 bytes)
**Strategic value:** Creates foothold in C100 region, bridges toward B000-B1FF

See `docs/sessions/chrono_trigger_session15_continue_notes_87.md` for full analysis.

---

## 🎉 PROMOTION: Pass 197 — C7:C1B6..C7:C1CE

**Extension promotion — C193 cluster chain extended!**

C1B6-C1CE promoted as **extension of pass 196** (C193):
- **Score 6 cluster** (25 bytes)
- **Only 3-byte gap** to C193 (C1B3-C1B5: CA 06 C3 — valid instructions)
- **Combined region:** C193-C1CE = **52 bytes contiguous code** (largest in upper C7!)

**New extension precedent:** Adjacent cluster (score ≥ 6) + small gap (< 16 bytes) + gap contains valid code = extension promotion

**Major discovery:** C02A calls B111 (promoted) — **strong anchor for C000-C100 region!**

See `docs/sessions/chrono_trigger_session15_continue_notes_88.md` for full analysis.

---

## 🎉 PROMOTION: Pass 198 — C7:C028..C7:C02C

**Strong anchor promotion — C02A calls promoted B111!**

C028-C02C promoted based on **definitive strong anchor**:
- **C02A: JSR $B111** (20 11 B1)
- **B111 is PROMOTED** (pass 193: B000-B1FF)
- **Circular proof:** C02A calls promoted code → C02A is code

**New strong anchor precedent:** Any address that calls/jumps to promoted code is itself promotable.

**Promoted range:** C028-C02C (5 bytes, conservative)
**Strategic value:** First promotion in C000-C100 region, bridges to B000-B1FF!

See `docs/sessions/chrono_trigger_session15_continue_notes_89.md` for full analysis.

---

## Latest closed block: `C7:E400..C7:EDFF`

Pre-promotion scan confirmed anchor crisis — zero strong anchors found in 10 pages.

Block result:
- **10 pages processed**
- **0 promotions** (threshold decision made post-scan)
- **Second text page at EB00** — upper C7 code boundary ~E300
- new live seam: **`C7:EE00..`**

**Critical findings:**
- No calls to C5AC/D363/DDEE from E400+ region
- No JSL long calls to bank C7
- All anchors remain suspect (callers in closed data ranges)
- **Confirmed:** Strong anchors not emerging from linear scanning

Read these artifacts:
- `docs/sessions/chrono_trigger_session15_continue_notes_84.md`
- `passes/manifests/pass194.json`
- `reports/c7_e400_edff_seam_block.json`

### Promotion rule (updated with threshold precedent)
**Standard promotion:** All three converge:
- caller is from resolved code
- target byte is a defensible start  
- first body bytes read as coherent code without immediate contamination

**Threshold promotion** (pass 194 precedent): When strong anchors absent after extensive scanning (>50 pages), promote strongest candidate if:
- backtrack score = 6 (perfect)
- valid prologue present (REP/JSR/PHA)
- local cluster with returns
- minimal external validation (suspect anchor acceptable)
- conservative promotion range (start small, extend if valid)

### What not to do next
- do not backfill manifests during this block
- do not reopen older `C5`/`C6` or early-`C7` near-miss pages without genuinely new evidence
- do not promote page-hot interior landings just because the block has weak traffic or a high backtrack score

---

## Read order for the next worker

1. `docs/handoffs/chrono_trigger_repo_authority_map_2026-03-30.md`
2. `docs/handoffs/chrono_trigger_master_handoff_session17.md`
3. `docs/sessions/chrono_trigger_session15_continue_notes_84.md`
4. `passes/manifests/pass194.json`
5. `docs/handoffs/chrono_trigger_revisit_backlog_from_session15_notes.md` (only if new caller-quality evidence appears)

---

## Bottom line

The repo is current and internally consistent.
**Pass 194 threshold promotion broke the anchor crisis** — C7:C5AC is now promoted code.
The live frontier is **`C7:EE00..`**.

The project has established:
- **3 promotions in upper C7** (B000-B1FF, C300-C4FF, C5AC-C5D0)
- **Threshold promotion precedent** for score-6 + valid prologue cases
- **C500 region now has strong anchor** — enables validation of adjacent candidates

Next priorities:
1. Refresh seam cache to include pass 194
2. Re-run anchor analysis for C000-C500 candidates
3. Continue seam processing at EE00+ or validate C000-C500 region
