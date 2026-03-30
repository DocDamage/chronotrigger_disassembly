# Chrono Trigger continuation notes after Session 15 handoff — pass set 16

## What was done
- Resumed at the live seam **`C5:4F00..`**.
- Swept one additional 10-page ROM-first seam block:
  - `C5:4F00..C5:58FF`
- Kept the same conservative rule: no code promotion without caller quality, start-byte quality, and local structure all converging.
- Result: **no new promotions**. All ten pages closed honestly.

## Method note
- Manifest-backed canonical state still stops at pass 191, so this continuation remains note-backed.
- Used:
  - `reports/c5_4f00_58ff_seam_block.json`
  - `reports/c5_4f00_58ff_seam_block.md`
  - Targeted `build_call_anchor_report_v3.py` for all eleven candidate entries:
    - C5:554D, C5:550D, C5:54FF, C5:54C0, C5:543F, C5:4F76, C5:5839, C5:5800, C5:51B0, C5:5360, C5:53DF
    - All eleven returned `weak / unresolved`. Zero resolved or strong callers in the entire block.
  - Direct ROM byte reads for C5:5500..55FF, C5:5400..54FF, C5:4F00..4FFF (manual review pages).
  - Targeted spot checks: C5:5800..5847, C5:5200..521F, C5:5000..5030.

## Anchor report result
Zero strong or resolved callers across all eleven checked targets.
Every anchor was `weak / unresolved`.

## Why this block did not promote code

### `C5:5500..55FF` — freeze (highest backtrack score in block, failed at byte level)
- Posture: `manual_owner_boundary_review`. Local cluster C5:5500..550D. Score-6 backtrack at C5:554D (highest in block). One weak caller from C5:29E6 (unresolved).
- C5:5500..550D cluster bytes: `F3 0C F2 CE F6 F8 7D 08 FC 3F E0 A0 08 40` — SBC (sr,S),Y, SBC (dp), INC dp,X, ADC abs,X, AND long,X, then RTI at C5:550D. Jumbled mix of subtract, increment, add, and AND with no consistent purpose, ending in RTI. This is data misread as code.
- C5:550D byte: `40` = RTI. A JSR caller into a function that starts with RTI would immediately return from interrupt — nonsensical. The seam report classifies this as suspect (not weak), confirming the byte is a poor entry candidate.
- C5:554D byte: `D1 FB` = CMP ($FB),Y (2 bytes). CMP (dp),Y as a function entry has no setup (no LDA, no load into Y, no register prep). Despite the score-6 backtrack confirming clean instruction boundaries before 554D, the actual first instruction is a compare without context — not a function entry.
- The score-6 backtrack measures instruction-boundary alignment only. It confirmed SEI + XBA + ROL abs,X cleanly precede 554D, but that is alignment evidence, not ownership evidence.
- **Frozen.**

### `C5:5400..54FF` — freeze (strongest near-miss, cleanest metrics in block)
- Posture: `manual_owner_boundary_review`. Zero hard-bad, zero soft-bad, zero local clusters. Three score-4 backtracks. This was the cleanest-looking page by metrics in the block.
- C5:54FF byte: `DD F3 0C` = CMP $0CF3,X (absolute indexed, 3 bytes). The entry point is the **last byte of the page** — the 3-byte instruction spans the page boundary into C5:5500. Page-boundary spanning is a classic backtrack-tool false positive: the instruction boundary looks clean because the prior bytes happened to align, but no real function starts at the last byte of its page.
- C5:54C0 byte: `8D 48 89` = STA $8948 (absolute). STA at function entry without any preceding LDA or REP/SEP setup is not a function prologue. One weak caller from C5:DE7C (unresolved).
- C5:543F byte: `D4 EB` = PEI ($EB) (Push Effective Indirect, 2 bytes). PEI at function entry pushes an address from an indirect pointer without establishing any registers first. The seam report classifies this as `suspect` quality (not weak), indicating the byte is a weak entry candidate. One weak caller from C5:2268 (unresolved).
- Despite the exceptional page cleanliness (zero bad starts, zero clusters, three score-4 backtracks), the actual entry bytes do not form function entries.
- **Frozen.**

### `C5:4F00..4FFF` — freeze
- Posture: `manual_owner_boundary_review`. Score-4 backtrack at C5:4F76. One caller from C5:8837 (JMP, weak/unresolved — note: JMP caller, not JSR).
- C5:4F76 bytes: `3B 60` = TSC (Transfer Stack Pointer to C Accumulator, 1 byte), then RTS (1 byte). The entire "function" is 2 bytes: copy stack pointer to A, return. A function body of TSC + RTS is meaninglessly small — it would transfer the stack pointer value into A and return, which has no purpose as a standalone callable. The JMP caller (not JSR) further weakens the boundary argument.
- C5:4FBD..4FC4 cluster: `B0 A8` = BCS -88 (branch far backward to ~4F37), `F4 E8 FA` = PEA $FAE8, then RTS at 4FC2, `96 60` = STX $60,Y, then another RTS at 4FC4. Two RTS within 2 bytes of each other is a data-misread signature. Real code does not have consecutive RTS instructions in a single path.
- **Frozen.**

### `C5:5800..58FF` — freeze (`branch_fed_control_pocket` with hard_bad)
- Posture: `bad_start_or_dead_lane_reject`. hard_bad=1 (C5:58E7 invalid). Score-6 backtrack at C5:5839 — second-highest in block.
- C5:5800 bytes: `B1 6A` = LDA ($6A),Y (2 bytes). LDA (dp),Y at function entry is not a function prologue. Two callers (JMP C5:E948, JSR C5:EAAD — both weak/unresolved).
- C5:5839 byte: `61 00` = ADC ($00,X) (2 bytes). ADC at function entry without preceding CLC is not valid — adding to an uninitialized carry state. Despite the score-6 backtrack, the opcode fails the function-entry test.
- Page is `branch_fed_control_pocket` family: traffic feeds via branch instructions, not direct calls. Hard-bad contamination from 58E7 poisons the page even for the better candidates.
- **Frozen.**

### `C5:5200..52FF` — freeze (dirtiest poison page in block)
- Posture: `bad_start_or_dead_lane_reject`. hard_bad=2. Both targets (C5:5200 and C5:5204) are classified `invalid`. Both backtracks score=-6 (strongly negative — the tool found strong evidence these are misaligned landings inside multi-byte instructions).
- C5:5200 byte: `00` = BRK (software interrupt). Functions do not start with BRK.
- C5:5204 byte: `FF E0 FF` = SBC long,X (4 bytes). High-density repeat-value pattern surrounding this target ($FF, $E0, $FF, $D8, $E7, $E0) indicates this is pattern/table data, not code.
- Score=-6 is the floor of the backtrack scale — maximum evidence of bad alignment. This page is genuinely toxic.
- **Frozen immediately.**

### `C5:5000..50FF` — freeze (adjacent-target overlapping bait)
- Posture: `bad_start_or_dead_lane_reject`. hard_bad=1. C5:5004 and C5:5005 are both caller-backed targets.
- Having two adjacent bytes (5004=`9F`, 5005=`4F`) as separate call targets is a strong overlapping-interpretation bait signature. C5:5004=`9F` = STA long,X (4 bytes), C5:5005=`4F` = EOR long (4 bytes). These likely represent different callers using the page in different CPU state interpretations — neither is the true start. Freeze.

### `C5:5100..51FF` — no promotion (mixed-lane carry-forward)
- Posture: `mixed_lane_continue`. Family: `mixed_command_data`. C5:51B0 (weak, JMP caller, score-2). JMP caller + score-2 + mixed_command_data family = no promotion. No byte review needed.

### `C5:5300..53FF` — freeze
- Posture: `bad_start_or_dead_lane_reject`. Family: `mixed_command_data`. hard_bad=1 (C5:5308 invalid). Best score=2 for the valid-looking targets (C5:5360, C5:53DF). Mixed-command-data family plus hard-bad flag = freeze without further analysis.

### `C5:5600..56FF` and `C5:5700..57FF` — freeze
- C5:5600: `local_control_only`, 0 xref hits, 0 targets. Freeze without analysis.
- C5:5700: `mixed_command_data`, `local_control_only`, 0 strong/weak external xrefs. One suspect target (C5:5727) with score-4 backtrack but zero caller support. Freeze.

## Most important near-miss / trap pages
- **Strongest honest near-miss**: **`C5:5400..54FF`** — zero bad starts, zero clusters, three score-4 backtracks. Cleanest page metrics in the block. Failed on all three candidate bytes: page-boundary bait (54FF), STA-at-entry (54C0), and suspect-quality PEI (543F).
- **Hottest trap page**: **`C5:5800..58FF`** — score-6 at C5:5839 (second-highest backtrack in block), two callers at C5:5800, `branch_fed_control_pocket` family. Poisoned by hard_bad=1 and the actual opcode at 5839 (ADC without CLC).
- **Highest score, failed at byte**: **`C5:5500..55FF`** — score-6 at C5:554D (highest in block) and score-6 at C5:5839 are the two highest backtracks seen this session. Both failed because the opcode at the target is not a function entry (CMP (dp),Y and ADC (dp,X) respectively). The score-6 backtrack is a boundary-alignment score, not a function-entry score.
- **Dirtiest poison page**: **`C5:5200..52FF`** — score=-6 on both targets, hard_bad=2. The worst-scored page encountered in this session.

## Score-6 pattern note
Two pages in this block (C5:5500 and C5:5800) had score-6 backtracks. Both failed because:
- Score-6 confirms instruction-boundary alignment before the target byte.
- Score-6 does NOT confirm the target byte itself is a function entry opcode.
- CMP (dp),Y and ADC (dp,X) are not function prologue instructions regardless of how clean the preceding alignment is.
- Future score-6 targets should still be byte-checked before any promotion decision.

## Seam movement
- Previous live seam: `C5:4F00..`
- Newly swept through: `C5:4F00..C5:58FF`
- New live seam: **`C5:5900..`**

## Pass / completion estimate
- Previous latest completed pass estimate: **741**
- New latest completed pass estimate: **751** (estimated)
- Completion estimate: **do not treat the old coarse metric as reliable without rescoping**

## Recommended next move
1. Resume at **`C5:5900..`**.
2. Preserve `C5:5400..54FF` as reference territory — cleanest page in the block; future resolved callers could unlock 54C0 or 54FF if the boundary evidence improves.
3. Do not treat score-6 backtracks as promotion signals. This session established that score-6 targets still fail at the byte level when the opcode is CMP or ADC without prior setup.
4. Watch for whether `C5:5900..` continues the dead-zone pattern from `C5:5600..5700` or returns to the hot-but-fragmented pattern.
