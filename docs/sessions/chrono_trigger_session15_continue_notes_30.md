# Chrono Trigger Session 15 — Continuation Notes 30

## Block closed: C5:DC00..C5:E5FF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C5:DC00 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | hard_bad=1 from invalid start `C5:DC00` |
| C5:DD00 | candidate_code_lane | manual_owner_boundary_review | freeze | two weak-only targets (`C5:DD0F`, `C5:DD1F`) with unresolved callers |
| C5:DE00 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | one suspect + two weak targets, no strong-anchor ownership |
| C5:DF00 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | hard_bad=1 plus soft_bad=2 contamination |
| C5:E000 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | high-noise page with hard_bad=1 (`raw=10`, `xref=15`) |
| C5:E100 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | hard_bad=2 (`C5:E132`, `C5:E1E0` invalid) |
| C5:E200 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=1 from invalid target `C5:E2F3` |
| C5:E300 | candidate_code_lane | mixed_lane_continue | freeze | lone weak target `C5:E3B8`; no boundary-backed ownership |
| C5:E400 | candidate_code_lane | manual_owner_boundary_review | freeze | two weak-only targets with unresolved callers |
| C5:E500 | candidate_code_lane | local_control_only | freeze | no targets, no xrefs |

---

## Manual-owner pages (anchor detail)

### C5:DD00..DDFF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C5:DD0F (weak, caller C5:10EE)
- C5:DD1F (weak, caller C5:BF94)

Backtrack scan (`reports/c5_dd00_ddff_backtrack.json`):
- C5:DD0F->DD0F score=3, start=0x11
- C5:DD1F->DD1F score=3, start=0x04

Anchor reports:
- C5:DD0F: strong=0, weak=1, invalid=4
- C5:DD1F: strong=0, weak=1, invalid=1

ROM-byte check:
- C5:DD0F = `11 00 86 55 02 00 40 70 55 EE FF AA`
- C5:DD1F = `04 F1 0E 40 F0 40 90 C2 3D 80 10 13`

Verdict: both targets are weak-only with substantial invalid companion callers; no defensible callable boundary.

### C5:DE00..DEFF
Summary: raw_targets=3, xref_hits=3, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C5:DE02 (suspect, caller E0:A124)
- C5:DE1C (weak, caller C5:3BA1)
- C5:DEA2 (weak, caller C5:C950)

Backtrack scan (`reports/c5_de00_deff_backtrack.json`):
- C5:DE00->DE02 score=4, start=0x53
- C5:DE19->DE1C score=2, start=0x04
- C5:DE99->DEA2 score=2, start=0x18

Anchor reports:
- C5:DE02: strong=0, weak=1, invalid=3
- C5:DE1C: strong=0, weak=1, invalid=0
- C5:DEA2: strong=0, weak=1, invalid=1

ROM-byte check:
- C5:DE02 = `11 55 00 BB 36 AA 40 60 F4 11 AA 5A`
- C5:DE1C = `F7 28 4E FD 42 78 05 48 C0 53 11 00`
- C5:DEA2 = `3F 20 F0 20 F0 20 F0 20 20 01 F0 02`

Verdict: suspect/weak-only ownership with data-like byte runs prevents promotion.

### C5:E400..E4FF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C5:E43B (weak, caller C5:396C)
- C5:E4F0 (weak, caller C5:E135)

Backtrack scan (`reports/c5_e400_e4ff_backtrack.json`):
- C5:E4E6->E4F0 score=6, start=0xA0
- C5:E43A->E43B score=2, start=0xC0

Anchor reports:
- C5:E43B: strong=0, weak=1, invalid=0
- C5:E4F0: strong=0, weak=1, invalid=3

ROM-byte check:
- C5:E43B = `54 80 25 85 4E 00 0E 3A 53 5E 01 FE`
- C5:E4F0 = `1A 15 9F 14 FF 1F 02 40 7F EB 21 B8`

Verdict: even with a score-6 backtrack, all caller evidence remains weak-only and target bytes stay non-prologue.

---

## Reject/mixed lane notes

- C5:DC00: rejected on hard_bad=1 from invalid `C5:DC00`; weak `C5:DCBC` does not rescue page.
  - C5:DC00 = `00 8F 0A 8B 02 12 FD 11 DF F6 11 4A`
  - C5:DCBC = `A0 52 60 9F 20 13 23 00 AB 03 02 00`
- C5:DF00: rejected with hard_bad=1 and soft_bad=2 (invalid `C5:DF25`, plus suspect contamination).
  - C5:DF00 = `01 F0 01 F0 FF 01 F0 01 F0 0E 10 A0`
  - C5:DF25 = `00 00 18 08 38 18 00 30 30 20 20 7C`
  - C5:DF71 = `C2 71 60 20 30 32 06 07 03 1E 1B 01`
- C5:E000: high-noise reject (`raw_targets=10`, `xref_hits=15`) with invalid anchor at `C5:E070`.
  - C5:E000 = `E0 E0 F8 FC B0 BE 73 FE F0 76 66 07`
  - C5:E01F = `C1 42 60 1C 1C 10 10 20 A0 F1 1C 6A`
  - C5:E020 = `42 60 1C 1C 10 10 20 A0 F1 1C 6A 0C`
  - C5:E070 = `00 C0 04 F0 F0 F8 F8 41 0D FC FC FE`
- C5:E100: rejected immediately on hard_bad=2 (invalid `C5:E132`, `C5:E1E0`).
- C5:E200: rejected on hard_bad=1 (`C5:E2F3` invalid) despite weak `C5:E2C0`.
- C5:E300: mixed-lane carry only (`C5:E3B8` weak, score=2); not promotable.

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
- C5:DC00..E5FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c5_dc00_e5ff_seam_block.json`
- `reports/c5_dc00_e5ff_seam_block.md`
- `reports/c5_dd00_ddff_backtrack.json`
- `reports/c5_de00_deff_backtrack.json`
- `reports/c5_e400_e4ff_backtrack.json`
- `reports/C5_DD0F_anchor.json`
- `reports/C5_DD1F_anchor.json`
- `reports/C5_DE02_anchor.json`
- `reports/C5_DE1C_anchor.json`
- `reports/C5_DEA2_anchor.json`
- `reports/C5_E43B_anchor.json`
- `reports/C5_E4F0_anchor.json`
- `reports/c5_dd00_ddff_flow.json` (manual-page extraction)
- `reports/c5_de00_deff_flow.json` (manual-page extraction)
- `reports/c5_e400_e4ff_flow.json` (manual-page extraction)
- `reports/c5_dc00_dcff_flow.json` (reject-page support)
- `reports/c5_df00_dfff_flow.json` (reject-page support)
- `reports/c5_e000_e0ff_flow.json` (reject-page support)
- `reports/c5_e100_e1ff_flow.json` (reject-page support)
- `reports/c5_e200_e2ff_flow.json` (reject-page support)

---

## New live seam: C5:E600..

Next unprocessed block starts at **C5:E600**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C5:E600 --pages 10 --json > reports/c5_e600_efff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c5_e600_efff_seam_block.json --output reports/c5_e600_efff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_31.
