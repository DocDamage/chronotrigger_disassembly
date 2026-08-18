# Chrono Trigger Session 15 — Continuation Notes 52

## Block closed: C6:B800..C6:C1FF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:B800 | mixed_command_data | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:B900 | mixed_command_data | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:BA00 | mixed_command_data | manual_owner_boundary_review | freeze | `BA60/BA7C` stay weak-only unresolved-caller landings; `BA76` is suspect-only from frozen data |
| C6:BB00 | mixed_command_data | local_control_only | freeze | lone suspect target `C6:BB06` plus soft-bad page pressure |
| C6:BC00 | mixed_command_data | local_control_only | freeze | lone suspect target `C6:BC4D` with no strong/weak support |
| C6:BD00 | mixed_command_data | manual_owner_boundary_review | freeze | `BD7D` is the strongest near-miss, but caller quality remains weak-only unresolved |
| C6:BE00 | mixed_command_data | local_control_only | freeze | suspect-only `BE15/BE43` targets, no strong/weak support |
| C6:BF00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | weak `BF02` cannot overcome invalid companion targets and hard-bad pressure |
| C6:C000 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | busiest reject page in block, but all traffic stays suspect-only under a hard-bad gate |
| C6:C100 | mixed_command_data | local_control_only | freeze | suspect-only `C109/C115` targets, no strong/weak support |

---

## Manual-owner page detail

### C6:BA00..BAFF
Summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:BA60 (1 weak caller from unresolved `C6:D46E`, downgraded to suspect effective strength)
- C6:BA76 (1 suspect `JMP` caller from frozen `C6:8A00` data page)
- C6:BA7C (1 weak caller from unresolved `C6:E7B6`)

Backtrack scan (`reports/c6_ba00_baff_backtrack.json`):
- C6:BA72->BA76 score=4, start=0x21
- C6:BA72->BA7C score=4, start=0x21
- C6:BA50->BA60 score=2, start=0x41

Anchor reports:
- C6:BA60: strong=0, weak=1, invalid=0
- C6:BA76: strong=0, weak=0, suspect=1, invalid=0
- C6:BA7C: strong=0, weak=1, invalid=0

ROM-byte check:
- C6:BA50 = `41 C7 03 AA AB CE 9B 75 66 EE 29 BD`
- C6:BA60 = `0A F1 1A 39 91 02 4A 5A 74 0F D2 9F`
- C6:BA72 = `21 E6 26 27 1A 1B AA CF D7 03 ED 0B`
- C6:BA76 = `1A 1B AA CF D7 03 ED 0B 40 AF E1 0E`
- C6:BA7C = `ED 0B 40 AF E1 0E 38 39 EE 0A F1 1A`

Verdict:
- `BA7C` is the only target that survives as weak effective strength.
- `BA60` downgrades to suspect under xref-context scoring.
- `BA76` never gets beyond suspect because its only caller lives in a closed data page.
- No target reaches resolved-code caller quality, so the page still freezes.

**Frozen.**

### C6:BD00..BDFF
Summary: raw_targets=2, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:BD44 (1 weak caller from unresolved `C6:D96F`, downgraded to suspect effective strength)
- C6:BD7D (2 weak `JML` callers from unresolved `CC:2B10` and `CC:2CA2`)

Backtrack scan (`reports/c6_bd00_bdff_backtrack.json`):
- C6:BD6F->BD7D score=6, start=0x0B
- C6:BD3E->BD44 score=2, start=0xF8

Anchor reports:
- C6:BD44: strong=0, weak=1, invalid=0
- C6:BD7D: strong=0, weak=2, invalid=0

ROM-byte check:
- C6:BD3E = `F8 01 F8 01 F8 01 F8 01 F8 01 F8 32`
- C6:BD44 = `F8 01 F8 01 F8 32 FE 3B 01 F8 D2 FD`
- C6:BD6F = `0B 05 9F 4D FC BB 01 F8 6E C5 AF 5F`
- C6:BD7D = `F8 16 48 7B 01 60 44 AE AF 02 10 AE`

Verdict:
- `BD7D` is the strongest honest near-miss page in the block: two valid weak callers and the only score-6 backtrack that survived manual review.
- That still is not enough. Both callers remain unresolved, so the target fails the caller-quality rule.
- `BD44` is weaker and clearly contaminated by repeated `F8 01` patterning.

**Frozen.**

---

## Reject-heavy page note

### C6:C000..C0FF
Summary: raw_targets=5, xref_hits=8, strong_or_weak=0, hard_bad=1, soft_bad=0

Targets:
- C6:C0C0 (3 suspect callers from `C6:0DFC`, `C6:1441`, `D1:2691`)
- C6:C020 (2 suspect callers from `C6:0E54` and `C6:1CC5`)
- C6:C00E (1 suspect caller from `C6:D330`)
- C6:C0A1 (1 suspect caller from `C6:A527`)
- C6:C021 (invalid companion target from `C6:C72F`)

Backtrack scan from block report:
- C6:C010->C020 score=4
- C6:C011->C021 score=4
- C6:C00E->C00E score=3
- C6:C0A1->C0A1 score=3
- C6:C0BC->C0C0 score=2

ROM-byte check:
- C6:C00E = `12 24 26 27 59 05 C0 F8 F7 40 95 04`
- C6:C010 = `26 27 59 05 C0 F8 F7 40 95 04 2B C6`
- C6:C020 = `94 02 56 03 F5 02 00 23 24 24 15 62`
- C6:C021 = `02 56 03 F5 02 00 23 24 24 15 62 12`
- C6:C0C0 = `34 33 34 BE 13 9C 15 C0 F8 80 77 5A`

Verdict:
- `C000` is the busiest reject page in the block by far.
- None of that traffic survives into even weak effective strength; every caller-backed lane stays suspect-only.
- The invalid companion target plus the page’s hard-bad posture keep the whole page frozen.

**Frozen.**

---

## Block read

- **Strongest honest near-miss page**: **`C6:BD00..BDFF`** — `BD7D` kept two weak callers and a score-6 backtrack, but still failed on unresolved caller quality.
- **Strongest reject signal**: **`C6:C000..C0FF`** — the busiest reject page in the block, with five targets in play and zero surviving strong/weak effective hits.
- `C6:BA00..BAFF` also forced manual review, but `BA60/BA7C` never got past weak-or-suspect caller quality and `BA76` stayed data-backed suspect only.

---

## Running promotion count

- C5:3B00..44FF: 0 promotions (notes_14)
- C5:4500..4EFF: 0 promotions (notes_15)
- C5:4F00..58FF: 0 promotions (notes_16)
- C5:5900..62FF: 0 promotions (notes_17)
- C5:6300..6CFF: 0 promotions (notes_18)
- C5:6D00..76FF: 0 promotions (notes_19)
- C5:7700..80FF: 0 promotions (notes_20)
- C5:8100..8AFF: 0 promotions (notes_21)
- C5:8B00..94FF: 0 promotions (notes_22)
- C5:9500..9EFF: 0 promotions (notes_23)
- C5:A000..A9FF: 0 promotions (notes_24)
- C5:AA00..B3FF: 0 promotions (notes_25)
- C5:B400..BDFF: 0 promotions (notes_26)
- C5:BE00..C7FF: 0 promotions (notes_27)
- C5:C800..D1FF: 0 promotions (notes_28)
- C5:D200..DBFF: 0 promotions (notes_29)
- C5:DC00..E5FF: 0 promotions (notes_30)
- C5:E600..EFFF: 0 promotions (notes_31)
- C5:F000..F9FF: 0 promotions (notes_32)
- C5:FA00..C6:03FF: 0 promotions (notes_33)
- C6:0400..0DFF: 0 promotions (notes_34)
- C6:0E00..17FF: 0 promotions (notes_35)
- C6:1800..21FF: 0 promotions (notes_36)
- C6:2200..2BFF: 0 promotions (notes_37)
- C6:2C00..35FF: 0 promotions (notes_38)
- C6:3600..3FFF: 0 promotions (notes_39)
- C6:4000..49FF: 0 promotions (notes_40)
- C6:4A00..53FF: 0 promotions (notes_41)
- C6:5400..5DFF: 0 promotions (notes_42)
- C6:5E00..67FF: 0 promotions (notes_43)
- C6:6800..71FF: 0 promotions (notes_44)
- C6:7200..7BFF: 0 promotions (notes_45)
- C6:7C00..85FF: 0 promotions (notes_46)
- C6:8600..8FFF: 0 promotions (notes_47)
- C6:9000..99FF: 0 promotions (notes_48)
- C6:9A00..A3FF: 0 promotions (notes_49)
- C6:A400..ADFF: 0 promotions (notes_50)
- C6:AE00..B7FF: 0 promotions (notes_51)
- C6:B800..C1FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_b800_c1ff_seam_block.json`
- `reports/c6_b800_c1ff_seam_block.md`
- `reports/c6_ba00_baff_flow.json`
- `reports/c6_ba00_baff_backtrack.json`
- `reports/c6_bd00_bdff_flow.json`
- `reports/c6_bd00_bdff_backtrack.json`
- `reports/C6_BA60_anchor.json`
- `reports/C6_BA76_anchor.json`
- `reports/C6_BA7C_anchor.json`
- `reports/C6_BD44_anchor.json`
- `reports/C6_BD7D_anchor.json`

---

## New live seam: C6:C200..

Next unprocessed block starts at **C6:C200**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:C200 --pages 10 --json > reports/c6_c200_cbff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_c200_cbff_seam_block.json --output reports/c6_c200_cbff_seam_block.md`
3. Run owner-backtrack scans only for pages that still land in `manual_owner_boundary_review`, then write notes_53.
