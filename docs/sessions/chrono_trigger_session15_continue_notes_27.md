# Chrono Trigger Session 15 — Continuation Notes 27

## Block closed: C5:BE00..C5:C7FF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C5:BE00 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | two weak + one suspect target, all unresolved caller evidence |
| C5:BF00 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=1 (`C5:BF40`) plus soft_bad=1 contamination |
| C5:C000 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=1 (`C5:C00F`) on a high-noise page (16 raw / 18 xref) |
| C5:C100 | mixed_command_data | manual_owner_boundary_review | freeze | weak/suspect-only targets, including boundary-bait `C5:C1FF` |
| C5:C200 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | 6-target mesh with one suspect endpoint (`C5:C2FD`) and no strong anchors |
| C5:C300 | candidate_code_lane | manual_owner_boundary_review | freeze | lone weak boundary-bait target `C5:C3FE` only |
| C5:C400 | branch_fed_control_pocket | local_control_only | freeze | only suspect target `C5:C430` (soft_bad=1), no weak/strong support |
| C5:C500 | branch_fed_control_pocket | mixed_lane_continue | freeze | weak `C5:C500` + suspect `C5:C5F0` in mixed lane; no boundary proof |
| C5:C600 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | three weak targets but two backtracks collapse to score 0 |
| C5:C700 | candidate_code_lane | mixed_lane_continue | freeze | lone weak target `C5:C7B9`; mixed-lane carry only |

---

## Manual-owner pages (anchor detail)

### C5:BE00..BEFF
Summary: raw_targets=3, xref_hits=3, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C5:BE12 (suspect, caller C5:D647)
- C5:BE7F (weak, caller C5:37E4)
- C5:BE8C (weak, caller C5:DFF7)

Backtrack scan (`reports/c5_be00_beff_backtrack.json`):
- C5:BE09->BE12 score=4, start=0x93
- C5:BE7D->BE7F score=4, start=0x2F
- C5:BE7D->BE8C score=4, start=0x2F

Anchor reports:
- C5:BE12: strong=0, weak=1, invalid=0
- C5:BE7F: strong=0, weak=1, invalid=0
- C5:BE8C: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:BE12 = `0F 80 01 F0 01 F0 01 F0 01 F0 DF 01`
- C5:BE7F = `2F 12 04 F7 09 3A 60 11 10 09 10 0A`
- C5:BE8C = `08 15 3D 01 7D 06 FD 22 00 2F 50 1F`

Verdict: caller evidence stays weak/suspect only, and candidate starts are data-like control fragments rather than callable prologues.

### C5:C100..C1FF
Summary: raw_targets=4, xref_hits=4, strong_or_weak=3, hard_bad=0, soft_bad=0

Targets:
- C5:C130 (suspect, caller C5:C4EB)
- C5:C180 (weak, caller C5:9D75)
- C5:C1EF (weak, caller C5:1370)
- C5:C1FF (weak, caller C5:79DB, boundary_bait)

Backtrack scan (`reports/c5_c100_c1ff_backtrack.json`):
- C5:C1E6->C1EF score=6, start=0x20
- C5:C129->C130 score=4, start=0x50
- C5:C179->C180 score=2, start=0xE0
- C5:C1F9->C1FF score=2, start=0x17

Anchor reports:
- C5:C130: strong=0, weak=1, invalid=1
- C5:C180: strong=0, weak=1, invalid=3
- C5:C1EF: strong=0, weak=1, invalid=4
- C5:C1FF: strong=0, weak=1, invalid=2

ROM-byte check:
- C5:C130 = `38 D4 AF D0 CB 0E 16 6B 20 2F E0 E8`
- C5:C180 = `0C 04 82 82 E1 C1 F1 E1 02 80 67 0A`
- C5:C1EF = `E0 A8 68 A8 68 03 3A 14 00 1C 17 16`
- C5:C1FF = `04 3F 56 4B 14 01 01 16 17 28 80 3F`

Verdict: boundary-bait and weak-only anchors dominate; no callable entry signature survives manual review.

### C5:C200..C2FF
Summary: raw_targets=6, xref_hits=6, strong_or_weak=5, hard_bad=0, soft_bad=0

Targets:
- C5:C200 (weak, caller C5:3191)
- C5:C223 (weak, caller C5:9D14)
- C5:C2B0 (weak, caller C5:296C)
- C5:C2CB (weak, caller FC:CA93)
- C5:C2F9 (weak, caller C5:979E)
- C5:C2FD (suspect, caller C5:6FCE)

Backtrack scan (`reports/c5_c200_c2ff_backtrack.json`):
- C5:C2FD->C2FD score=5, start=0x0B
- C5:C2A9->C2B0 score=4, start=0x8B
- C5:C2C5->C2CB score=4, start=0xC1
- C5:C2F4->C2F9 score=4, start=0x78
- C5:C222->C223 score=2, start=0x90
- C5:C200->C200 score=1, start=0x3F

Anchor reports:
- C5:C200: strong=0, weak=1, invalid=6
- C5:C223: strong=0, weak=1, invalid=0
- C5:C2B0: strong=0, weak=1, invalid=0
- C5:C2CB: strong=0, weak=1, invalid=0
- C5:C2F9: strong=0, weak=1, invalid=0
- C5:C2FD: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:C200 = `3F 56 4B 14 01 01 16 17 28 80 3F 41`
- C5:C223 = `70 F4 05 04 FE 29 F8 A8 71 55 9B E0`
- C5:C2B0 = `18 C0 EE 1E CC 38 30 F0 D6 39 43 0D`
- C5:C2CB = `33 0C 3D 67 80 41 49 1F 02 04 7F 4A`
- C5:C2F9 = `3F 1F 40 05 0B 00 DF 41 9B CF 0E 87`
- C5:C2FD = `0B 00 DF 41 9B CF 0E 87 00 44 82 80`

Verdict: despite multiple medium backtracks, all anchors are weak-only and start bytes remain non-prologue/data-like; freeze.

### C5:C300..C3FF
Summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0

Target:
- C5:C3FE (weak, caller C5:64FD, boundary_bait)

Backtrack scan (`reports/c5_c300_c3ff_backtrack.json`):
- C5:C3FD->C3FE score=4, start=0xC0

Anchor report:
- C5:C3FE: strong=0, weak=1, invalid=1

ROM-byte check:
- C5:C3FE = `CD 3E F9 18 11 10 10 AA 00 78 39 2D`

Verdict: lone boundary-edge weak anchor with no prologue-quality start; freeze.

### C5:C600..C6FF
Summary: raw_targets=3, xref_hits=3, strong_or_weak=3, hard_bad=0, soft_bad=0

Targets:
- C5:C61F (weak, caller C5:62A6)
- C5:C670 (weak, caller C5:DB6D)
- C5:C67D (weak, caller C5:4E33)

Backtrack scan (`reports/c5_c600_c6ff_backtrack.json`):
- C5:C617->C61F score=4, start=0x20
- C5:C66F->C670 score=0, start=0x8E
- C5:C677->C67D score=0, start=0xF0

Anchor reports:
- C5:C61F: strong=0, weak=1, invalid=0
- C5:C670: strong=0, weak=1, invalid=0
- C5:C67D: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:C61F = `98 44 04 00 DC 4E 10 DE DE C2 C2 DE`
- C5:C670 = `E0 10 B0 01 F0 FF 01 F0 01 F0 01 F0`
- C5:C67D = `F0 01 F0 01 F0 01 F0 01 F0 FF 01 F0`

Verdict: two score-0 backtracks and repetitive control bytes keep this page non-promotable.

---

## Reject/mixed lane notes

- C5:BF00: rejected with `hard_bad=1`, `soft_bad=1`; invalid target `C5:BF40` plus mixed weak/suspect chatter across 10 xref hits.
  - C5:BF00 = `06 3D 84 3F 88 35 80 00 6F 00 F0 0A`
  - C5:BFCB = `11 41 0C 21 00 10 09 00 03 7C 1B E4`
- C5:C000: rejected with `hard_bad=1` on high target density (`raw=16`, `xref=18`), including invalid `C5:C00F`.
  - C5:C000 = `FB 05 19 03 E0 20 E5 0C FD 00 08 7F`
  - C5:C0C0 = `05 5E 01 F0 40 C2 FF 20 32 E1 1E 66`
  - C5:C0E0 = `44 22 80 C3 66 84 80 05 06 07 08 1F`
- C5:C400: local-control only; lone suspect `C5:C430` (`soft_bad=1`) without weak/strong support.
- C5:C500 and C5:C700: mixed-lane carry pages with weak-only singletons (`C5:C500`, `C5:C7B9`) and no caller-backed boundary promotion.

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
- C5:BE00..C7FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c5_be00_c7ff_seam_block.json`
- `reports/c5_be00_c7ff_seam_block.md`
- `reports/c5_be00_beff_backtrack.json`
- `reports/c5_c100_c1ff_backtrack.json`
- `reports/c5_c200_c2ff_backtrack.json`
- `reports/c5_c300_c3ff_backtrack.json`
- `reports/c5_c600_c6ff_backtrack.json`
- `reports/C5_BE12_anchor.json`
- `reports/C5_BE7F_anchor.json`
- `reports/C5_BE8C_anchor.json`
- `reports/C5_C130_anchor.json`
- `reports/C5_C180_anchor.json`
- `reports/C5_C1EF_anchor.json`
- `reports/C5_C1FF_anchor.json`
- `reports/C5_C200_anchor.json`
- `reports/C5_C223_anchor.json`
- `reports/C5_C2B0_anchor.json`
- `reports/C5_C2CB_anchor.json`
- `reports/C5_C2F9_anchor.json`
- `reports/C5_C2FD_anchor.json`
- `reports/C5_C3FE_anchor.json`
- `reports/C5_C61F_anchor.json`
- `reports/C5_C670_anchor.json`
- `reports/C5_C67D_anchor.json`
- `reports/c5_be00_beff_flow.json` (supporting extraction)
- `reports/c5_c100_c1ff_flow.json` (supporting extraction)
- `reports/c5_c200_c2ff_flow.json` (supporting extraction)
- `reports/c5_c300_c3ff_flow.json` (supporting extraction)
- `reports/c5_c600_c6ff_flow.json` (supporting extraction)
- `reports/c5_bf00_bfff_flow.json` (reject-page support)
- `reports/c5_c000_c0ff_flow.json` (reject-page support)
- `reports/c5_c400_c4ff_flow.json` (mixed-page support)
- `reports/c5_c500_c5ff_flow.json` (mixed-page support)
- `reports/c5_c700_c7ff_flow.json` (mixed-page support)

---

## New live seam: C5:C800..

Next unprocessed block starts at **C5:C800**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C5:C800 --pages 10 --json > reports/c5_c800_d1ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c5_c800_d1ff_seam_block.json --output reports/c5_c800_d1ff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_28.
