# Chrono Trigger continuation notes after Session 15 handoff — pass set 14

## What was done
- Resumed at the live seam **`C5:3B00..`**.
- Swept one additional 10-page ROM-first seam block:
  - `C5:3B00..C5:44FF`
- Kept the same conservative rule: no code promotion without caller quality, start-byte quality, and local structure all converging.
- Result: **no new promotions**. All ten pages closed honestly.

## Method note
- Manifest-backed canonical state still stops at pass 191, so this continuation remains note-backed.
- Used:
  - `reports/c5_3b00_44ff_seam_block.json`
  - `reports/c5_3b00_44ff_seam_block.md`
  - Targeted `build_call_anchor_report_v3.py` checks for the five strongest candidate entries:
    - `C5:4098` — 2 callers, both weak/unresolved
    - `C5:40F0` — 2 callers, both weak/unresolved
    - `C5:4192` — 1 caller, weak/unresolved (C5:B314)
    - `C5:4208` — 1 caller, weak/unresolved (C5:C51B)
    - `C5:43DB` — 1 caller, weak/unresolved (C5:12CC)
  - Direct ROM byte read (ExHiROM offset $54000..$544FF) for all three `manual_owner_boundary_review` pages.
- Same rule as before: weak callers from unresolved pages are not enough by themselves.

## Anchor report result
Every targeted anchor came back with zero strong or resolved callers.
All five candidates were `weak / unresolved` only.
This alone did not force a freeze, but it removed all elevated-quality caller support from the block before manual byte review began.

## Why this block did not promote code

### `C5:4200..42FF` — freeze (strongest near-miss)
- Posture: `manual_owner_boundary_review`; score-6 backtrack; 2 weak caller-backed targets.
- C5:4200 byte: `0F` = ORA long (4-byte instruction). ORA long at page-top with no prologue (no PHP, no REP, no register setup) is not a function entry.
- C5:4208 byte: `F0` = BEQ. A function that opens with a conditional branch on the Z flag inherited from the caller context is not a defensible start. The single caller from C5:C51B is unresolved.
- The score-6 backtrack lands in C5:422F..4239. The bytes there read: CLC, CMP $49C5,X, EOR dp, ADC abs,Y — an incoherent mixture without a clean top boundary.
- The BPL at C5:4285: `10 FF` = BPL -1 (branch target = self-minus-1 = C5:4286), which decodes as an apparent tight loop. This indicates the surrounding bytes are data being misread as code, not live executable flow.
- C5:42C5 = RTS ends a 5-byte pseudo-cluster (C5:42BE..42C5), but the bytes preceding it (TYA, CPX, BIT, ...) do not form a coherent function body even in any plausible m/x mode.
- **Frozen.**

### `C5:4000..40FF` — freeze (hottest trap page)
- Posture: `manual_owner_boundary_review`; 27 raw targets, 30 xref hits, 14 strong-or-weak signals; 4 soft-bad starts, 0 hard-bad. Highest activity density in the block.
- C5:4098 byte: `AF` = LDA long (4-byte instruction). LDA long as a function entry with no preceding CLC/PHP/REP/SEP is not a clean prologue. Two callers (C5:7B64, C5:A56E) are both unresolved.
- C5:40F0 bytes: `C0 C1` = CPY #$C1, then `E0 C1` = CPX #$C1 (8-bit mode) or `C0 C1 E0` = CPY #$E0C1 (16-bit). Either way, opening with CPY followed immediately by CPX comparing both registers to the same constant is not a function prologue pattern. Two callers (C5:2B69, C5:A84C) are both unresolved.
- The two local clusters at C5:405B..4063 include two consecutive identical BRA instructions (`80 DF, 80 DF`) branching to the same backward target. Two identical unconditional branches in a row is a data-misread signature, not a code signature.
- Despite the enormous signal density, no byte at any caller-backed target forms a coherent start. The page is hot but fragmented. **Frozen.**

### `C5:4100..41FF` — freeze
- Posture: `manual_owner_boundary_review`; 3 raw targets, 2 strong-or-weak, 0 hard-bad, 0 soft-bad.
- C5:4120 byte: `9F` = STA long,X (4-byte instruction). STA long,X as a function entry without any preceding load is not a function prologue. Caller from unresolved territory.
- C5:4192 byte: `7F` = ADC long,X (4-byte instruction). ADC without a preceding CLC is not a function entry. One caller (C5:B314) is unresolved.
- C5:41DF byte: `FE` = INC abs,X. INC abs,X as a first instruction is not a function entry.
- The C5:41A6..41AE cluster contains: SEI, LDA [$40],Y, STP at C5:41A9, SEC, INC abs, RTS. The STP instruction (stop processor until reset) inside a supposed code island is a strong indicator of data being misread. STP does not appear in normal callable routines.
- C5:41A0 and C5:41A8 both decode as RTI ($40) within 8 bytes of each other. Two RTI instructions in a short window is inconsistent with a single interrupt handler body — more consistent with data.
- **Frozen.**

### `C5:4300..43FF` — no promotion (carry-forward)
- Posture: `mixed_lane_continue`; 1 raw target (C5:43DB), 1 weak/unresolved caller (C5:12CC).
- C5:43DB byte: `8C` = STY abs (3-byte instruction). STY abs at a function start without a preceding LDY is not a function entry.
- The local cluster at C5:4387..438E decodes as: JSR $18F7, SBC ($1F,S),Y, ADC ($1F,X), RTS — an 8-byte sequence that structurally resembles a tiny helper. However, there is no external caller support into this pocket. The only page-level caller support points to 43DB, not 4387. An unsupported local island that is never directly called cannot be promoted.
- Kept as the least-bad carry-forward page of the block. **No promotion.**

### `C5:3B00..3BFF` and `C5:3C00..3CFF` — freeze (bad-start pages)
- C5:3B00: hard_bad=1 (C5:3BD0 still invalid). The weak caller into C5:3B7E remains unresolved. The C5:3B83..3B89 pocket opens with BMI (conditional branch) and is only 6 bytes — too small and lacks a clean top boundary. The C5:3BCD pocket starts with JSR $62FB then immediately BRA $3C08 (jumping out of page) — this reads as mid-body flow-through code, not a callable start.
- C5:3C00: hard_bad=2, soft_bad=1. All three backtracks are score-2 (weakest). Neither C5:3C10 nor C5:3C18 has been confirmed as a true start rather than a hot interior byte. The cluster at C5:3C97..3C9F remains local control only.
- **Both frozen.**

### `C5:3D00..3DFF`, `C5:3E00..3EFF`, `C5:3F00..3FFF` — freeze (local control / dead lane)
- C5:3D00: `local_control_only`. One suspect target (C5:3D96), score-2 backtrack, no resolved callers. No inspection needed beyond posture confirmation.
- C5:3E00: `local_control_only`. Two suspect targets (C5:3E00, C5:3EF9) with score-2 and score-1 backtracks. Isolated control islands at 3E09..3E13 and 3E9A..3EA1 confirmed by seam report.
- C5:3F00: `bad_start_or_dead_lane_reject`. hard_bad=1. Single weak caller into C5:3F00 (page-top bait). The C5:3FA7..3FB1 cluster is the cleanest thing on the page but has no external caller support.
- **All three frozen.**

### `C5:4400..44FF` — freeze (local control tail)
- Posture: `local_control_only`. One suspect target (C5:44C0, score-4 backtrack), no resolved callers from earlier pages (all frozen above).
- The C5:44BD..44C9 cluster contains a BRA at C5:44C8: `80 60` = BRA +$60 → target C5:452A (next page). Flow exits the page mid-cluster, consistent with mid-body pass-through code.
- The C5:44D6..44E1 cluster contains BRA at C5:44DC: `80 08` = BRA +8 → C5:44E6, which bypasses RTS at C5:44E0. A BRA that skips over an RTS means the RTS is a dead path — not the real terminator of this body. This is local-control splinter behavior, not a callable function.
- **Frozen.**

## Most important near-miss / trap pages
- **Strongest honest near-miss**: **`C5:4200..42FF`** — score-6 backtrack, two caller-backed targets, reached `manual_owner_boundary_review` posture. Failed because the byte-level start candidates (4200=ORA long, 4208=BEQ) are not function entries and the score-6 range doesn't form a coherent body.
- **Hottest trap page**: **`C5:4000..40FF`** — 27 raw targets, 30 xref hits, 14 strong/weak, highest activity of the block. Failed despite enormous signal density because no caller-backed target byte reads as a function entry.
- **Dirtiest poison page**: **`C5:3C00..3CFF`** — hard_bad=2, soft_bad=1, all backtracks score-2 only. The cleanest thing on the page (3C97..3C9F) is still local-control-only. Most contaminated early page in the block.

## Seam movement
- Previous live seam: `C5:3B00..`
- Newly swept through: `C5:3B00..C5:44FF`
- New live seam: **`C5:4500..`**

## Pass / completion estimate
- Previous latest completed pass estimate: **721**
- New latest completed pass estimate: **731** (estimated; 10 pages, ~1 pass per page forward)
- Completion estimate: **do not treat the old coarse metric as reliable without rescoping**

## Recommended next move
1. Resume at **`C5:4500..`**.
2. Preserve `C5:4200..42FF` as reference territory only — score-6 backtrack is worth revisiting if a resolved caller into 4208 or nearby ever surfaces from a later page promotion.
3. Preserve `C5:4000..40FF` as reference territory only — the traffic density is real even if no promotion earned; a future resolved promotion nearby could unlock this area retroactively.
4. Do not let heat alone force an early promotion in the next block.
5. Watch for whether the `C5:4387..438E` island (JSR+body+RTS) gets picked up by a resolved caller from within the next block — it's the only structurally coherent unsupported island in this entire sweep.
