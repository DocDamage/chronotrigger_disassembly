# Chrono Trigger Session 15 — Continuation Notes 44

## Block closed: C6:6800..C6:71FF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:6800 | text_ascii_heavy | mixed_lane_continue | freeze | weak/suspect text lane, no strong ownership |
| C6:6900 | text_ascii_heavy | manual_owner_boundary_review | freeze | weak-only targets with unresolved callers and no strong anchors |
| C6:6A00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | suspect-only leads plus invalid `C6:6ACA` (`hard_bad=1`) |
| C6:6B00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | invalid-only target `C6:6B00` (`hard_bad=2`) |
| C6:6C00 | mixed_command_data | manual_owner_boundary_review | freeze | weak/suspect set remains unresolved (`soft_bad=1`) |
| C6:6D00 | mixed_command_data | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:6E00 | mixed_command_data | manual_owner_boundary_review | freeze | high weak volume at `C6:6EC4`, but no strong anchors |
| C6:6F00 | mixed_command_data | mixed_lane_continue | freeze | lone weak target `C6:6F06` |
| C6:7000 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | suspect/invalid mix with `hard_bad=1` |
| C6:7100 | mixed_command_data | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |

---

## Manual-owner pages (anchor detail)

### C6:6900..69FF
Summary: raw_targets=2, xref_hits=3, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C6:6900 (weak, callers C6:424A and C6:E30F)
- C6:69C4 (weak, caller CA:E3AF)

Backtrack scan (`reports/c6_6900_69ff_backtrack.json`):
- C6:69BE->69C4 score=4, start=0x05
- C6:6900->6900 score=1, start=0xC4

Anchor reports:
- C6:6900: strong=0, weak=2, invalid=3
- C6:69C4: strong=0, weak=1, invalid=0

ROM-byte check:
- C6:6900 = `C4 21 C5 21 00 B6 21 B7 3D C6 21 C7`
- C6:69C4 = `DC 0C AC 0D F1 DC 0C 6B 2C 7D B4 16`

Verdict: both entries remain weak-only and unresolved; freeze.

### C6:6C00..6CFF
Summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=1

Targets:
- C6:6C08 (weak, caller C6:D268)
- C6:6C32 (suspect, caller C6:2AA8)
- C6:6C6B (suspect, caller C6:C5D3)

Backtrack scan (`reports/c6_6c00_6cff_backtrack.json`):
- C6:6C64->6C6B score=4, start=0x8B
- C6:6C07->6C08 score=2, start=0x4B
- C6:6C2C->6C32 score=2, start=0x3B

Anchor reports:
- C6:6C08: strong=0, weak=1, invalid=3
- C6:6C32: strong=0, weak=1, invalid=0
- C6:6C6B: strong=0, weak=1, invalid=3

ROM-byte check:
- C6:6C08 = `4C 4D 1D 1E C6 1F 4E F8 10 78 16 45`
- C6:6C32 = `F8 E6 8E 5E 80 0F 17 1C 13 01 F8 7D`
- C6:6C6B = `01 F8 8B 42 BF 77 26 27 26 FB 0D FC`

Verdict: weak/suspect-only ownership with invalid companion overlap; freeze.

### C6:6E00..6EFF
Summary: raw_targets=1, xref_hits=8, strong_or_weak=6, hard_bad=0, soft_bad=0

Targets:
- C6:6EC4 (weak, callers CA:A243, CA:BEEF, CA:E2FC, CA:F777, CB:25E7, CB:4D6F, CB:4DED, CB:F090)

Backtrack scan (`reports/c6_6e00_6eff_backtrack.json`):
- C6:6EC3->6EC4 score=4, start=0x08

Anchor reports:
- C6:6EC4: strong=0, weak=8, invalid=5

ROM-byte check:
- C6:6EC4 = `9C 11 DC 30 2A 9D 00 01 92 00 77 78`

Verdict: high weak-hit count but still no strong anchors and notable invalid overlap; freeze.

---

## Reject/mixed lane notes

- C6:6800 remains mixed-lane carry with two weak (`C6:6800`, `C6:6860`) and one suspect (`C6:6886`) target.
- C6:6A00 rejected on suspect/invalid mix (`C6:6ACA` invalid) with `hard_bad=1`.
- C6:6B00 is invalid-only (`C6:6B00` hit twice), hard reject.
- C6:6F00 remains mixed-lane carry on lone weak `C6:6F06`.
- C6:7000 rejected with suspect-heavy traffic and invalid `C6:70F2`.

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
- C6:6800..71FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_6800_71ff_seam_block.json`
- `reports/c6_6800_71ff_seam_block.md`
- `reports/c6_6900_69ff_backtrack.json`
- `reports/c6_6c00_6cff_backtrack.json`
- `reports/c6_6e00_6eff_backtrack.json`
- `reports/c6_6900_69ff_flow.json` (manual-page extraction)
- `reports/c6_6c00_6cff_flow.json` (manual-page extraction)
- `reports/c6_6e00_6eff_flow.json` (manual-page extraction)
- `reports/C6_6900_anchor.json`
- `reports/C6_69C4_anchor.json`
- `reports/C6_6C08_anchor.json`
- `reports/C6_6C32_anchor.json`
- `reports/C6_6C6B_anchor.json`
- `reports/C6_6EC4_anchor.json`

---

## New live seam: C6:7200..

Next unprocessed block starts at **C6:7200**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:7200 --pages 10 --json > reports/c6_7200_7bff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_7200_7bff_seam_block.json --output reports/c6_7200_7bff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_45.
