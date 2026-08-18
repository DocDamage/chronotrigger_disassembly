# Chrono Trigger continuation notes after Session 15 handoff — pass set 15

## What was done
- Resumed at the live seam **`C5:4500..`**.
- Swept one additional 10-page ROM-first seam block:
  - `C5:4500..C5:4EFF`
- Kept the same conservative rule: no code promotion without caller quality, start-byte quality, and local structure all converging.
- Result: **no new promotions**. All ten pages closed honestly.

## Method note
- Manifest-backed canonical state still stops at pass 191, so this continuation remains note-backed.
- Used:
  - `reports/c5_4500_4eff_seam_block.json`
  - `reports/c5_4500_4eff_seam_block.md`
  - Targeted `build_call_anchor_report_v3.py` checks for all eleven candidate entries across the block:
    - C5:4C00, C5:4CDF, C5:4CFF, C5:4E00, C5:4E20, C5:4E30, C5:4805, C5:481E, C5:4603, C5:46C0, C5:4728
    - All eleven returned `weak / unresolved`. Zero resolved or strong callers in the entire block.
  - Direct ROM byte read for C5:4C00..4CFF and C5:4E00..4EFF (the two `manual_owner_boundary_review` pages).
  - Targeted spot checks: C5:4800..483F (hard-bad page), C5:4603, C5:46C0, C5:4728, C5:4D3F, C5:4DC1.

## Anchor report result
Zero strong or resolved callers across all eleven checked targets.
Every anchor was `weak / unresolved`.
This removed all elevated-quality caller support before manual byte review.

## Why this block did not promote code

### `C5:4C00..4CFF` — freeze (strongest near-miss, `branch_fed_control_pocket` family)
- Posture: `manual_owner_boundary_review`. Family: `branch_fed_control_pocket` — no hard-bad, no soft-bad, zero local clusters. Score-3 backtrack at C5:4C00. This was the cleanest-looking page by metrics in the block.
- C5:4C00 bytes: `62 91 7B 7B 9F FF 72 71 40 60 90...`
  - `62 91 7B` = PER (Push Effective PC-Relative Address, 3 bytes). PER as a function entry is unusual — it pushes a computed stack address without any prior PHP/PHD/REP setup.
  - Offset 8: `40` = RTI.
  - Offset 9: `60` = RTS.
  - Two return instructions (RTI then RTS) within the first 9 bytes of the supposed function entry is a data-misread signature. Real function bodies do not contain both RTI and RTS in their opening bytes.
- C5:4CDF = `C3 B6` = CMP ($B6,S),Y (stack-relative indirect indexed). Stack-relative CMP without any PHK/PHP/REP setup is not a function entry.
- C5:4CFF = `E8` = INX. INX alone at an entry point is not a function entry.
- The page was flagged `branch_fed_control_pocket` because its traffic arrives via branch instructions, not direct calls. Branch traffic establishes that execution enters the page through control flow continuations — it does not establish callable function boundaries.
- **Frozen.**

### `C5:4E00..4EFF` — freeze (hottest trap page)
- Posture: `manual_owner_boundary_review`. Score-4 backtrack at C5:4E00, score-3 at C5:4E20. Two weak JSR callers plus one JMP.
- C5:4E00 byte: `2B` = PLD (Pull Direct Register from Stack). PLD is a function **epilogue** instruction — it restores the D register that was saved by PHD at function entry. Having PLD as the very first instruction means execution either started mid-body (PHD happened earlier in a longer enclosing function) or this is data. Either disqualifies a promotion.
- C5:4E20 byte: `43` = EOR (sr,S),Y (stack-relative indirect indexed). Not a function entry.
- C5:4E30 byte: `10 00` = BPL +0 (branch to next instruction regardless of N flag = a 2-byte no-op). The caller into 4E30 is a JMP (not JSR), further weakening the function-boundary argument.
- C5:4E04..4E0A cluster: TDC, STA long ($EEBDF7), STY dp,X. Three mid-body store instructions. No return instruction within cluster bounds.
- C5:4E85..4E8C cluster (ends in RTL at 4E8C): contains BPL at 4E87 that branches to C5:4EC8 (far outside the cluster). A cluster whose control flow exits before reaching its RTL is mid-body flow, not a standalone callable body.
- **Frozen.**

### `C5:4800..48FF` — freeze (bad-start page with notable unsupported island)
- Posture: `bad_start_or_dead_lane_reject`. hard_bad=1. Score-4 backtrack at C5:4805 with one weak caller (C5:EFF9, unresolved).
- C5:4805 byte: `0B` = PHD (Push Direct Register). PHD is a legitimate function prologue opcode. This is the only page in the block where a caller-backed target begins with a real prologue instruction. However: the single caller from C5:EFF9 is unresolved, and the page-level hard_bad=1 flag means another xref into this page points at a known-bad byte. The hard-bad pressure prevents promotion without resolved caller support.
- C5:4821..482A cluster: `08 76 18 33 FB 25 66 9F 10 60` — PHP + body + RTS at 482A (10 bytes). Structurally resembles a tiny helper. No external caller support into 4821 (the page's caller-backed targets are 4805, 481E, 48C0 — not 4821). An island with no external caller cannot be promoted.
- **Frozen.** The 4821..482A island is the most structurally honest-looking unsupported pocket in this block.

### `C5:4600..46FF` and `C5:4700..47FF` — no promotion (mixed-lane carry-forward)
- C5:4600: `branch_fed` traffic opens with `F8` = SED (Set Decimal Mode) at page-top. SED is a 6502-era BCD instruction almost never used in SNES 65816 production code. Its presence at page-top is a data indicator.
- C5:4603 = `FE 03 00` = INC $0003,X (increment absolute indexed). Not a function entry.
- C5:46C0 = `D6 F3` = DEC $F3,X (decrement dp,X). Not a function entry.
- C5:4728 = `04 00` = TSB $00 (Test and Set Bits, direct page). Not a function entry.
- All three candidates: score-2 backtracks, single weak/unresolved caller each.
- **No promotions.**

### `C5:4500..45FF` — freeze (bad-start page)
- hard_bad=1. Only target (C5:45BA) is classified `invalid`. Score-2 backtrack only. Freeze immediately.

### `C5:4900..49FF`, `C5:4A00..4AFF`, `C5:4B00..4BFF` — freeze (dead-quiet belt)
- Three consecutive pages with **zero xref hits** each. No raw targets, no backtracks, no local clusters (except one each).
- C5:4900 is `mixed_command_data` family — structural content classification, not code.
- C5:4A00 and C5:4B00 have one local cluster each (C5:4A00..4A17; C5:4BEF..4BFF) but no external caller support.
- **All three frozen without extended analysis.**

### `C5:4D00..4DFF` — freeze (local control with false score-4 bait)
- Posture: `local_control_only`. 0 strong_or_weak external xrefs. Two suspect-only targets with score-4 backtracks.
- C5:4D3F = `F9 00 EF` = SBC $EF00,Y (absolute indexed). SBC as a function entry without prior SEC/CLC is not a function entry.
- C5:4DC1 = `F1 0E` = SBC ($0E),Y (direct page indirect indexed). Same problem.
- Score-4 backtracks are the highest in the block for this page but the backtrack tool is picking up instruction-boundary plausibility, not actual caller evidence. With zero external xrefs, these score-4 values are false positives.
- **Frozen.**

## Most important near-miss / trap pages
- **Strongest honest near-miss**: **`C5:4C00..4CFF`** — `branch_fed_control_pocket`, no bad starts, no local clusters, score-3 at page-top. Failed because RTI+RTS appear within the first 9 bytes. Worth revisiting if a resolved branch-side caller ever surfaces.
- **Hottest trap page**: **`C5:4E00..4EFF`** — score-4 backtrack, two weak JSR callers, three detected clusters. Failed because C5:4E00=PLD (an epilogue opcode, not a prologue), and the 4E85 cluster's BPL exits far outside the cluster bounds.
- **Most interesting unsupported island**: **C5:4821..482A** — PHP + body + RTS (10 bytes, structurally correct). No external caller support. The adjacent target at 4805=PHD also has a legitimate prologue byte but is stuck behind a single weak unresolved caller and a page-level hard-bad flag.
- **Quietest dead stretch**: **C5:4900..4BFF** — three pages in a row with zero xref hits. Most silent stretch since the C3 bank dead zones.

## Seam movement
- Previous live seam: `C5:4500..`
- Newly swept through: `C5:4500..C5:4EFF`
- New live seam: **`C5:4F00..`**

## Pass / completion estimate
- Previous latest completed pass estimate: **731**
- New latest completed pass estimate: **741** (estimated)
- Completion estimate: **do not treat the old coarse metric as reliable without rescoping**

## Recommended next move
1. Resume at **`C5:4F00..`**.
2. Preserve `C5:4C00..4CFF` as reference territory — `branch_fed_control_pocket` clean metrics are notable even though the byte evidence failed; future branch-side resolution could change the picture.
3. Preserve `C5:4E00..4EFF` as reference territory — score-4 backtrack plus two JSR callers is the highest-quality failed candidate in this block.
4. Note `C5:4821..482A` (PHP+body+RTS island) as a potential unsupported helper pocket; if a resolved caller from within C5 later targets a nearby byte, reconsider.
5. Do not let the dead quiet of `C5:4900..4BFF` cause false optimism about the territory after `C5:4F00..` — dead zones can resume hot suddenly.
