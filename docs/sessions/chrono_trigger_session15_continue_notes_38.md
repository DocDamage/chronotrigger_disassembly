# Chrono Trigger Session 15 — Continuation Notes 38

## Block closed: C6:2C00..C6:35FF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:2C00 | mixed_command_data | manual_owner_boundary_review | freeze | weak/suspect-only set led by boundary-bait `C6:2CFE`; no strong anchors |
| C6:2D00 | mixed_command_data | mixed_lane_continue | freeze | lone suspect target `C6:2D3E` with unresolved ownership |
| C6:2E00 | mixed_command_data | mixed_lane_continue | freeze | one weak + two suspect targets, no strong anchors |
| C6:2F00 | mixed_command_data | mixed_lane_continue | freeze | no incoming targets (`raw=0`, `xref=0`) |
| C6:3000 | candidate_code_lane | manual_owner_boundary_review | freeze | weak/suspect mesh with high invalid overlap in anchor reports |
| C6:3100 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | explicit contamination (`hard_bad=1`) despite two weak hits |
| C6:3200 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | heavy weak traffic but no strong anchors; key target has high invalid overlap |
| C6:3300 | mixed_command_data | local_control_only | freeze | lone suspect target `C6:3300` only |
| C6:3400 | candidate_code_lane | local_control_only | freeze | suspect-only targets (`C6:3410`, `C6:3414`, `C6:3421`) |
| C6:3500 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | weak/suspect entries remain unresolved with no strong anchors |

---

## Manual-owner pages (anchor detail)

### C6:2C00..2CFF
Summary: raw_targets=4, xref_hits=4, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:2CFE (weak, caller C6:1C8A, boundary_bait=true)
- C6:2C78 (suspect, caller C6:D778)
- C6:2CD2 (suspect, caller C6:6774)
- C6:2CD7 (suspect, caller C6:6786)

Backtrack scan (`reports/c6_2c00_2cff_backtrack.json`):
- C6:2C73->2C78 score=4, start=0x20
- C6:2CCE->2CD2 score=2, start=0x3F
- C6:2CD7->2CD7 score=1, start=0x5F
- C6:2CFE->2CFE score=-1, start=0x12

Anchor reports:
- C6:2CFE: strong=0, weak=1, invalid=0
- C6:2C78: strong=0, weak=1, invalid=1
- C6:2CD2: strong=0, weak=1, invalid=1
- C6:2CD7: strong=0, weak=1, invalid=0

ROM-byte check:
- C6:2CFE = `12 51 62 00 04 36 05 66 00 15 D2 01`
- C6:2C78 = `C8 12 00 DA 12 02 DB 6C 11 DC 12 DD`
- C6:2CD2 = `06 3D 07 00 3D 5F 3D 0B 3D 08 3D 09`
- C6:2CD7 = `5F 3D 0B 3D 08 3D 09 14 3D 0C 0A 01`

Verdict: boundary-bait weak at page end plus suspect companions remains non-promotable; freeze.

### C6:3000..30FF
Summary: raw_targets=11, xref_hits=11, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C6:3003 (weak, caller C6:D2EA)
- C6:3011 (weak, caller C6:C801)
- C6:3002 (suspect, caller C6:1304)
- C6:3021 (suspect, caller C6:BF81)
- C6:3038 (suspect, caller C6:D744)

Backtrack scan (`reports/c6_3000_30ff_backtrack.json`):
- C6:3000->3002 score=2, start=0x16
- C6:3000->3003 score=2, start=0x16
- C6:3001->3011 score=2, start=0x85
- C6:301E->3021 score=2, start=0xCD
- C6:3037->3038 score=6, start=0x08

Anchor reports:
- C6:3003: strong=0, weak=1, invalid=12
- C6:3011: strong=0, weak=1, invalid=4
- C6:3002: strong=0, weak=1, invalid=20
- C6:3021: strong=0, weak=1, invalid=8
- C6:3038: strong=0, weak=1, invalid=7

ROM-byte check:
- C6:3003 = `14 86 16 87 07 06 34 DC 0E 80 09 E2`
- C6:3011 = `16 7E 00 0D 7F 0D 8E 0D 8F 0D CC 00`
- C6:3002 = `CC 14 86 16 87 07 06 34 DC 0E 80 09`
- C6:3021 = `0D DD 0D CE 00 0D CF 0D DE 0D DF 0D`
- C6:3038 = `48 4C 17 4D 80 40 4E 17 8E 18 62 05`

Verdict: all candidates remain weak/suspect-only with heavy invalid companion-caller overlap; freeze.

### C6:3200..32FF
Summary: raw_targets=6, xref_hits=12, strong_or_weak=5, hard_bad=0, soft_bad=0

Targets:
- C6:32C4 (weak, callers CA:A3DC, CA:F33C, CA:F493, CB:7359, CB:73A2, CB:73BA)
- C6:3231 (weak, callers C6:6E6A and C6:8C31)
- C6:3232 (weak, caller C6:A9A7)
- C6:3236 (suspect, caller C6:1DE3)
- C6:32BA (suspect, caller C6:154B)

Backtrack scan (`reports/c6_3200_32ff_backtrack.json`):
- C6:3230->3231 score=2, start=0xF0
- C6:3230->3232 score=2, start=0xF0
- C6:3230->3236 score=2, start=0xF0
- C6:32C4->32C4 score=1, start=0x10
- C6:32BA->32BA score=-1, start=0x3F

Anchor reports:
- C6:32C4: strong=0, weak=6, invalid=13
- C6:3231: strong=0, weak=2, invalid=1
- C6:3232: strong=0, weak=1, invalid=2
- C6:3236: strong=0, weak=1, invalid=0
- C6:32BA: strong=0, weak=1, invalid=0

ROM-byte check:
- C6:32C4 = `10 28 00 1D FF 1C 66 56 01 4B 44 00`
- C6:3231 = `10 D8 0C D9 00 0C CA 0C CB 0C DA 0C`
- C6:3232 = `D8 0C D9 00 0C CA 0C CB 0C DA 0C 55`
- C6:3236 = `0C CA 0C CB 0C DA 0C 55 00 00 7F C0`
- C6:32BA = `3F 30 00 8A 00 99 00 9A 00 41 10 28`

Verdict: despite high weak-hit volume, no strong anchors appear and the lead target is heavily invalid-contaminated; freeze.

### C6:3500..35FF
Summary: raw_targets=3, xref_hits=5, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:3521 (weak, callers C6:6E89 and C6:8C49)
- C6:3506 (suspect, callers C6:36CD and C6:40C6)
- C6:35ED (suspect, caller C6:66D0)

Backtrack scan (`reports/c6_3500_35ff_backtrack.json`):
- C6:3501->3506 score=4, start=0x48
- C6:3513->3521 score=4, start=0x21
- C6:35EC->35ED score=4, start=0x61

Anchor reports:
- C6:3521: strong=0, weak=2, invalid=6
- C6:3506: strong=0, weak=2, invalid=0
- C6:35ED: strong=0, weak=1, invalid=0

ROM-byte check:
- C6:3521 = `11 75 9C 03 68 A0 03 E0 5E 00 08 F0`
- C6:3506 = `0B EC 0B E8 0B EC 0B FA 03 E2 00 FE`
- C6:35ED = `0E 61 4E 50 4E D0 50 0D 60 4E E0 80`

Verdict: weak/suspect-only ownership with no strong caller anchors; freeze.

---

## Reject/mixed lane notes

- C6:2D00 stays mixed-lane carry with only suspect `C6:2D3E`.
- C6:2E00 stays mixed-lane carry: one weak (`C6:2EF3`) plus suspect companions, no strong ownership.
- C6:2F00 remains mixed-lane empty page (`raw=0`, `xref=0`).
- C6:3100 is the only hard reject in this block (`hard_bad=1`) despite two weak targets (`C6:315D`, `C6:31D0`).
- C6:3300 and C6:3400 remain local-control suspect-only pages.

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
- C6:2C00..35FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_2c00_35ff_seam_block.json`
- `reports/c6_2c00_35ff_seam_block.md`
- `reports/c6_2c00_2cff_backtrack.json`
- `reports/c6_3000_30ff_backtrack.json`
- `reports/c6_3200_32ff_backtrack.json`
- `reports/c6_3500_35ff_backtrack.json`
- `reports/c6_2c00_2cff_flow.json` (manual-page extraction)
- `reports/c6_3000_30ff_flow.json` (manual-page extraction)
- `reports/c6_3200_32ff_flow.json` (manual-page extraction)
- `reports/c6_3500_35ff_flow.json` (manual-page extraction)
- `reports/C6_2CFE_anchor.json`
- `reports/C6_2C78_anchor.json`
- `reports/C6_2CD2_anchor.json`
- `reports/C6_2CD7_anchor.json`
- `reports/C6_3003_anchor.json`
- `reports/C6_3011_anchor.json`
- `reports/C6_3002_anchor.json`
- `reports/C6_3021_anchor.json`
- `reports/C6_3038_anchor.json`
- `reports/C6_32C4_anchor.json`
- `reports/C6_3231_anchor.json`
- `reports/C6_3232_anchor.json`
- `reports/C6_3236_anchor.json`
- `reports/C6_32BA_anchor.json`
- `reports/C6_3521_anchor.json`
- `reports/C6_3506_anchor.json`
- `reports/C6_35ED_anchor.json`

---

## New live seam: C6:3600..

Next unprocessed block starts at **C6:3600**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:3600 --pages 10 --json > reports/c6_3600_3fff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_3600_3fff_seam_block.json --output reports/c6_3600_3fff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_39.
