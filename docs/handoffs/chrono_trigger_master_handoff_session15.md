# Chrono Trigger Disassembly — Master Handoff Session 15

## Repo / branch / ROM
- Repo: `DocDamage/chronotrigger_disassembly`
- Working branch: `live-work-from-pass166`
- ROM: `rom/Chrono Trigger (USA).sfc`
- Manifest-backed canonical state: stops at **pass 191**
- Operative state beyond pass 191: **continuation notes** (`chrono_trigger_session15_continue_notes_*.md`)

---

## Current no-BS state

This session processed **40 pages** across four 10-page seam blocks in bank C5, plus a full toolkit upgrade cycle.

Result: **zero promotions**. All 40 pages frozen honestly.

That is not failure. The conservative standard — caller quality + start-byte quality + local structure all converging — is what keeps the label set trustworthy. The seam advanced from `C5:3B00` to `C5:6300` without polluting the repo.

---

## Progress made this session

### Seam blocks processed
| Block | Pages | Promotions | Notes file |
|-------|-------|------------|------------|
| C5:3B00..44FF | 10 | 0 | `chrono_trigger_session15_continue_notes_14.md` |
| C5:4500..4EFF | 10 | 0 | `chrono_trigger_session15_continue_notes_15.md` |
| C5:4F00..58FF | 10 | 0 | `chrono_trigger_session15_continue_notes_16.md` |
| C5:5900..62FF | 10 | 0 | `chrono_trigger_session15_continue_notes_17.md` |

### Seam movement
- Session started at: **`C5:3B00..`**
- Current live seam: **`C5:6300..`**

### Reports generated (all in `reports/`)
- `c5_3b00_44ff_seam_block.json` / `.md`
- `c5_4500_4eff_seam_block.json` / `.md`
- `c5_4f00_58ff_seam_block.json` / `.md`
- `c5_5900_62ff_seam_block.json` / `.md`

---

## Toolkit upgrades completed this session

All five upgrades are now in production. Scripts affected:

### Fix 1 — RTI → hard_bad_start (`seam_triage_utils_v1.py`)
- `0x40` (RTI) added to `BAD_START_HARD`
- Effect: RTI at a caller-backed target is now auto-classified `invalid` rather than requiring manual ROM read
- Previously discovered example: C5:550D=RTI was surfaced as `suspect`, now auto-caught

### Fix 2 — PLD/PLB → soft_bad_start (`seam_triage_utils_v1.py`)
- `0x2B` (PLD) and `0xAB` (PLB) added to `BAD_START_SOFT`
- Effect: epilogue pull-stack opcodes at function entries are auto-demoted from `weak` to `suspect`
- Previously discovered example: C5:4E00=PLD required manual inspection to identify as non-entry

### Fix 3 — Expanded LIKELY_PROLOG (`score_target_owner_backtrack_v1.py`)
- Added: PHD (0x0B), PHK (0x4B), PHB (0x8B), REP (0xC2)
- Effect: legitimate function prologues get the +2 LIKELY_PROLOG bonus in backtrack scoring
- Previously discovered example: C5:4805=PHD got score 4 before fix, 5 after

### Fix 4 — boundary_bait flag (`run_seam_block_v1.py` + `render_seam_block_report_v1.py`)
- Targets at page offset 0xFD–0xFF auto-tagged `[boundary_bait]` in rendered reports
- Effect: last-byte-of-page traps are auto-identified without manual address arithmetic
- Previously discovered example: C5:54FF appeared in rendered output without the flag

### Fix 5 — data-misread pattern detector (`seam_triage_utils_v1.py` + `find_local_code_islands_v2.py`)
- Added `check_data_misread_patterns(blob)` to `seam_triage_utils_v1.py`
- Detects: consecutive_identical_branch, consecutive_rts, rti_rts_proximity, tight_loop_branch, sed_decimal_mode
- Each flag subtracts 2 from island cluster score
- Previously discovered examples: C5:4C00 had RTI+RTS proximity (data misread), C5:405B had consecutive identical BRA

---

## Important negative evidence from this session

### What keeps rejecting candidates
The core pattern across all 40 pages:

1. **Score-6 backtracks ≠ function entry** — backtrack score measures instruction-boundary alignment before the target, not opcode quality at the target itself. C5:554D (CMP (dp),Y) and C5:5839 (ADC (dp,X)) both scored 6 and both failed at the target byte.

2. **BRK (0x00) contamination** — multiple promising candidates (C5:6107, C5:61E2) had BRK bytes within 2–4 bytes of the called target, a reliable data indicator.

3. **Non-prologue clean starts** — `ROR` (0x7E), `TRB` (0x1C), `STY dp,X` (0x94) all appear as start bytes at caller-backed targets. clean_start ≠ function_entry.

4. **Branch-fed pockets** — C5:5A00 and C5:5B00 are `branch_fed_control_pocket` family; they receive traffic via branches, not calls, so no function boundary can be established even if traffic is present.

### Most significant near-misses (in order of closeness)
1. **C5:6105** — `LDX #$FE` (LIKELY_PROLOG ✓, score=4) but BRK at C5:6109 (2 bytes into the target body) proves data contamination. Target is also `suspect`, not `weak`.
2. **C5:4200** — score-6 backtrack, C5:4208=0xF0 (BEQ, branch opcode at entry). The page's strongest candidate is still a branch landing, not a function start.
3. **C5:4805** — PHD (0x0B, LIKELY_PROLOG after Fix 3, score improved 4→5). The best structural candidate from the C5:4500..4EFF block. Still a single weak caller from an unresolved page.

### Quiet stretches confirming dead zone
- C5:5D00..5EFF: two consecutive pages with zero xref hits, zero clusters — complete dead zone
- C5:4900..4BFF: three consecutive pages with zero xref hits (noted in notes_15)

---

## Structural truths to preserve for future sessions

1. The seam advanced from `C5:3B00` to `C5:6300` without a single trustworthy owner/helper promotion.
2. The absence of promotions is honest — the lane is genuinely mixed/data-heavy in this stretch.
3. Score-6 backtrack is a signal for instruction-alignment, not function-entry quality. Always check the target byte itself.
4. Weak callers from unresolved pages are not enough alone; caller quality requires the caller to be from resolved code.
5. RTI (0x40), PLD (0x2B), PLB (0xAB) at function entries are now auto-caught by the upgraded toolkit.

---

## Recommended next-session workflow

1. Stay on `live-work-from-pass166`
2. Read this handoff and `chrono_trigger_session15_continue_notes_17.md`
3. Resume from **`C5:6300..`**
4. Run the standard preflight:
   ```bash
   python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C5:6300 --pages 10 --json > reports/c5_6300_6cff_seam_block.json
   python3 tools/scripts/render_seam_block_report_v1.py --input reports/c5_6300_6cff_seam_block.json --output reports/c5_6300_6cff_seam_block.md
   ```
5. For any `manual_owner_boundary_review` page, run:
   ```bash
   python3 tools/scripts/score_target_owner_backtrack_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --range 'C5:XXXX..C5:XXFF' --json
   ```
6. Promotion checklist (all three must hold):
   - caller is from resolved code (not weak/unresolved)
   - start byte is in LIKELY_PROLOG or is otherwise a defensible function entry
   - body reads as coherent code without BRK/data contamination in the first ~8 bytes
7. If those three disagree, freeze and advance the seam

---

## Files produced this session

### Continuation notes (operative state of record)
- `chrono_trigger_session15_continue_notes_14.md` — C5:3B00..44FF
- `chrono_trigger_session15_continue_notes_15.md` — C5:4500..4EFF
- `chrono_trigger_session15_continue_notes_16.md` — C5:4F00..58FF
- `chrono_trigger_session15_continue_notes_17.md` — C5:5900..62FF

### Seam block reports
- `reports/c5_3b00_44ff_seam_block.json` / `.md`
- `reports/c5_4500_4eff_seam_block.json` / `.md`
- `reports/c5_4f00_58ff_seam_block.json` / `.md`
- `reports/c5_5900_62ff_seam_block.json` / `.md`

### Toolkit scripts modified
- `tools/scripts/seam_triage_utils_v1.py` — Fixes 1, 2, 5
- `tools/scripts/score_target_owner_backtrack_v1.py` — Fix 3
- `tools/scripts/run_seam_block_v1.py` — Fix 4
- `tools/scripts/render_seam_block_report_v1.py` — Fix 4
- `tools/scripts/find_local_code_islands_v2.py` — Fix 5

### Docs updated
- `README.md`
- `docs/handoffs/chrono_trigger_master_handoff_session15.md` (this file)

---

## What remains before the disassembly is truly finished

### Immediate remaining work
- continue forward from `C5:6300..`
- bank C5 is mixed-content heavy; expect continued zero-promotion stretches
- keep publishing notes and block reports honestly

### Medium-term remaining work
- eventually reach a lane in bank C5 with clean external callers into defensible starts
- reconcile manifest state (frozen at pass 191) with the note-backed continuation frontier
- formalize toolkit changes in a `tools/docs/` writeup when the upgrade cycle stabilizes

### Long-term remaining work (unchanged from prior sessions)
- complete code/data separation across all banks
- build rebuildable source tree
- formalize decompressor grammar
- runtime validation with bsnes/bsnes-plus
