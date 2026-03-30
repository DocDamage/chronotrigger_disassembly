# Chrono Trigger Session 15 — Continuation Notes 51

## Block closed: C6:AE00..C6:B7FF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:AE00 | mixed_command_data | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:AF00 | mixed_command_data | manual_owner_boundary_review | freeze | `AF40/AFAE` are weak-only unresolved-caller landings |
| C6:B000 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | invalid `C6:B068` with hard-bad `RTS` start byte |
| C6:B100 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | invalid `C6:B140` despite score-6 backtrack |
| C6:B200 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | hard-bad pressure plus weak/suspect mix never survives |
| C6:B300 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | invalid boundary-bait `C6:B3FD` and no strong/weak survivor |
| C6:B400 | mixed_command_data | local_control_only | freeze | lone suspect boundary-bait target `C6:B4FF` |
| C6:B500 | mixed_command_data | manual_owner_boundary_review | freeze | `B569` is plausible locally, but caller quality stays weak-only |
| C6:B600 | mixed_command_data | local_control_only | freeze | only suspect `B604/B62E` targets, no strong/weak support |
| C6:B700 | mixed_command_data | mixed_lane_continue | freeze | lone suspect target `C6:B74A` with no surviving ingress support |

---

## Manual-owner page detail

### C6:AF00..AFFF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:AF40 (1 weak caller from unresolved `C6:D801`, downgraded to suspect effective strength)
- C6:AFAE (1 weak caller from unresolved `C6:BD91`)

Backtrack scan (`reports/c6_af00_afff_backtrack.json`):
- C6:AF30->AF40 score=4, start=0x41
- C6:AFAA->AFAE score=2, start=0x73

Anchor reports:
- C6:AF40: strong=0, weak=1, invalid=0
- C6:AFAE: strong=0, weak=1, invalid=0

ROM-byte check:
- C6:AF30 = `41 DD 91 0A 4C 4D 4E 07 79 01 61 A4`
- C6:AF40 = `52 55 AC 10 CC A6 10 04 BD 07 1C 00`
- C6:AFAA = `73 74 75 76 25 3A 00 16 0A 89 09 AF`
- C6:AFAE = `25 3A 00 16 0A 89 09 AF 5A CD 36 02`

Verdict:
- `AF40` and `AFAE` both remain callable enough to force manual review.
- That is still not enough to promote either one. Each target has only one unresolved weak caller.
- `AF40` degrades further to suspect effective strength under xref-context scoring.
- `AFAE` keeps weak effective strength, but the target bytes still read noisy and high-risk.

**Frozen.**

### C6:B500..B5FF
Summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:B569 (1 weak caller from unresolved `C6:BDE3`)

Backtrack scan (`reports/c6_b500_b5ff_backtrack.json`):
- C6:B55D->B569 score=4, start=0x0B

Anchor reports:
- C6:B569: strong=0, weak=1, invalid=0

ROM-byte check:
- C6:B55D = `0B A8 12 15 1E D4 2A 07 B4 0D F3 6D`
- C6:B569 = `21 5A 36 0A 0B BA BA 48 0B CD 1A AB`

Verdict:
- `B569` is the cleanest single target in the block structurally.
- It still has only one weak caller, and that caller remains unresolved.
- Promotion rule fails on caller quality before anything else can matter.

**Frozen.**

---

## Reject-heavy page note

### C6:B200..B2FF
Summary: raw_targets=4, xref_hits=4, strong_or_weak=1, hard_bad=1, soft_bad=0

Targets:
- C6:B20C (weak caller from unresolved `C6:CB33`)
- C6:B23F (suspect caller from frozen `C6:0BD1`)
- C6:B2C1 (suspect caller from frozen `C6:786A`)
- one additional invalid/unsurviving lane inside the page

Backtrack scan from block report:
- C6:B20A->B20C score=4
- C6:B22B->B239 score=4
- C6:B23B->B23F score=4

ROM-byte check:
- C6:B20A = `A0 02 34 33 FD 33 8E 00 0F 0D D8 03`
- C6:B20C = `34 33 FD 33 8E 00 0F 0D D8 03 E3 26`
- C6:B23B = `1E BF 03 03 E3 03 A6 04 44 08 02 05`
- C6:B23F = `E3 03 A6 04 44 08 02 05 01 03 34 8F`

Verdict:
- `B200` carries the strongest reject pressure in the block because it kept the most target traffic while still triggering the hard-bad gate.
- `B20C` is the only target that reaches weak strength, but the page posture is still reject-heavy and no resolved-code caller survives.
- The suspect-only companion targets do not rescue the page.

**Frozen.**

---

## Block read

- **Strongest honest near-miss page**: **`C6:B500..B5FF`** — single plausible landing at `B569`, but only one unresolved weak caller.
- **Strongest reject signal**: **`C6:B200..B2FF`** — the busiest reject page in the block, with four targets in play but no defensible survivor.
- `C6:AF00..AFFF` also forced manual review, but both `AF40` and `AFAE` fell short on caller quality before the local bytes could justify promotion.

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
- C6:AE00..B7FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_ae00_b7ff_seam_block.json`
- `reports/c6_ae00_b7ff_seam_block.md`
- `reports/c6_af00_afff_flow.json`
- `reports/c6_af00_afff_backtrack.json`
- `reports/c6_b500_b5ff_flow.json`
- `reports/c6_b500_b5ff_backtrack.json`
- `reports/C6_AF40_anchor.json`
- `reports/C6_AFAE_anchor.json`
- `reports/C6_B569_anchor.json`

---

## New live seam: C6:B800..

Next unprocessed block starts at **C6:B800**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:B800 --pages 10 --json > reports/c6_b800_c1ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_b800_c1ff_seam_block.json --output reports/c6_b800_c1ff_seam_block.md`
3. Run owner-backtrack scans only for pages that still land in `manual_owner_boundary_review`, then write notes_52.
