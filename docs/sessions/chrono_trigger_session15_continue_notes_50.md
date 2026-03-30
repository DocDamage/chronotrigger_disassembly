# Chrono Trigger Session 15 — Continuation Notes 50

## Block closed: C6:A400..C6:ADFF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:A400 | mixed_command_data | local_control_only | freeze | lone suspect target `C6:A421` with no strong/weak support |
| C6:A500 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | `A518/A538` are real near-miss starts, but every caller is weak and unresolved |
| C6:A600 | mixed_command_data | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:A700 | mixed_command_data | local_control_only | freeze | lone suspect target `C6:A77B` with no strong/weak support |
| C6:A800 | candidate_code_lane | local_control_only | freeze | candidate-code lane, but no ingress targets (`raw=0`, `xref=0`) |
| C6:A900 | mixed_command_data | manual_owner_boundary_review | freeze | soft-bad `A900` plus weak/suspect-only `A97B/A98B` pressure |
| C6:AA00 | candidate_code_lane | local_control_only | freeze | candidate-code lane, but no ingress targets (`raw=0`, `xref=0`) |
| C6:AB00 | mixed_command_data | mixed_lane_continue | freeze | no ingress targets and no surviving local cluster pressure |
| C6:AC00 | mixed_command_data | local_control_only | freeze | lone suspect target `C6:AC56` with no strong/weak support |
| C6:AD00 | mixed_command_data | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |

---

## Manual-owner page detail

### C6:A500..A5FF
Summary: raw_targets=2, xref_hits=3, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C6:A518 (2 weak callers from unresolved `C6:E624` and `C6:EDD7`)
- C6:A538 (1 weak caller from unresolved `C6:EAFC`)

Backtrack scan (`reports/c6_a500_a5ff_backtrack.json`):
- C6:A516->A518 score=6, start=0xA2
- C6:A534->A538 score=6, start=0x08

Anchor reports:
- C6:A518: strong=0, weak=2, invalid=0
- C6:A538: strong=0, weak=1, invalid=0

ROM-byte check:
- C6:A516 = `A2 71 20 03 13 40 11 0C 15 17 9C 0D`
- C6:A518 = `20 03 13 40 11 0C 15 17 9C 0D 60 78`
- C6:A534 = `08 16 05 05 20 09 C1 39 C1 C1 1C 91`
- C6:A538 = `20 09 C1 39 C1 C1 1C 91 92 9E 08 AC`

Verdict:
- `A518` and `A538` both land on plausible `JSR` starts and both keep score-6 backtracks, so this page is a real near-miss.
- That still is not enough. Every caller lives in unresolved territory, so the anchor quality never rises above weak.
- `A518` keeps one weak effective hit and one suspect downgrade under xref context; `A538` keeps only one weak effective hit.
- Promotion rule fails on caller quality. No resolved-code caller survives.

**Frozen.**

### C6:A900..A9FF
Summary: raw_targets=3, xref_hits=4, strong_or_weak=1, hard_bad=0, soft_bad=1

Targets:
- C6:A900 (suspect caller from frozen `C6:9A00` data page, but soft-bad start byte `0x09`)
- C6:A97B (1 weak caller from unresolved `C6:EB0E`)
- C6:A98B (2 weak callers from unresolved `C6:E3D7` and `C6:E500`, both downgraded to suspect effective strength)

Backtrack scan (`reports/c6_a900_a9ff_backtrack.json`):
- C6:A973->A97B score=6, start=0xA2
- C6:A98A->A98B score=6, start=0xC2
- C6:A900->A900 score=-2, start=0x09

Anchor reports:
- C6:A97B: strong=0, weak=1, invalid=0
- C6:A98B: strong=0, weak=2, invalid=0

ROM-byte check:
- C6:A900 = `09 01 F8 5F 18 74 12 C1 BC 00 92 EB`
- C6:A973 = `A2 62 A6 06 DE 6B 0C 12 12 C1 E5 03`
- C6:A97B = `12 C1 E5 03 50 A0 52 C1 A2 53 FB DE`
- C6:A98A = `C2 C2 50 51 DB C7 C8 01 5F 10 06 07`
- C6:A98B = `C2 50 51 DB C7 C8 01 5F 10 06 07 BB`

Verdict:
- `A900` itself is rejected immediately by the `ORA #imm` soft-bad start byte.
- `A97B` keeps only one weak unresolved caller.
- `A98B` keeps two weak anchor callers, but both collapse to suspect effective strength under xref-context scoring.
- No candidate reaches resolved-code caller quality, so the page does not survive manual review.

**Frozen.**

---

## Block read

- **Strongest honest near-miss page**: **`C6:A500..A5FF`** — the best page in the block, with two valid-looking `JSR` landings (`A518`, `A538`) and score-6 backtracks, but still no resolved-code caller support.
- **Strongest reject signal**: **`C6:A900..A9FF`** — mixed manual-review page where `A900` dies on a soft-bad start and the better-looking `A97B/A98B` candidates never get past weak-or-suspect caller quality.
- `C6:A800..A8FF` and `C6:AA00..AAFF` were the clearest reminder that a page can score as `candidate_code_lane` and still deserve an honest freeze when ingress stays at zero.

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
- C6:A400..ADFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_a400_adff_seam_block.json`
- `reports/c6_a400_adff_seam_block.md`
- `reports/c6_a500_a5ff_flow.json`
- `reports/c6_a500_a5ff_backtrack.json`
- `reports/c6_a900_a9ff_flow.json`
- `reports/c6_a900_a9ff_backtrack.json`
- `reports/C6_A518_anchor.json`
- `reports/C6_A538_anchor.json`
- `reports/C6_A97B_anchor.json`
- `reports/C6_A98B_anchor.json`

---

## New live seam: C6:AE00..

Next unprocessed block starts at **C6:AE00**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:AE00 --pages 10 --json > reports/c6_ae00_b7ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_ae00_b7ff_seam_block.json --output reports/c6_ae00_b7ff_seam_block.md`
3. Run owner-backtrack scans only for pages that still land in `manual_owner_boundary_review`, then write notes_51.
