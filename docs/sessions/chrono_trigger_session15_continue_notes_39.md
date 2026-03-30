# Chrono Trigger Session 15 — Continuation Notes 39

## Block closed: C6:3600..C6:3FFF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:3600 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | suspect-only leads plus explicit invalid ingress (`hard_bad=1`) |
| C6:3700 | mixed_command_data | mixed_lane_continue | freeze | weak-only carry (`C6:37C4`, `C6:37FC`) with unresolved ownership |
| C6:3800 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | includes invalid target `C6:3801` (`hard_bad=1`) |
| C6:3900 | mixed_command_data | mixed_lane_continue | freeze | lone suspect target `C6:391C` only |
| C6:3A00 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | weak/suspect-only anchors with heavy invalid overlap on `C6:3A08` |
| C6:3B00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | invalid-only page (`C6:3B00`, `C6:3B80`) |
| C6:3C00 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | severe contamination (`hard_bad=22`, `C6:3CC4` invalid x21) |
| C6:3D00 | mixed_command_data | manual_owner_boundary_review | freeze | weak/suspect-only ownership, no strong anchors |
| C6:3E00 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | invalid companion target `C6:3E12` (`hard_bad=1`) |
| C6:3F00 | mixed_command_data | local_control_only | freeze | empty ingress page (`raw=0`, `xref=0`) |

---

## Manual-owner pages (anchor detail)

### C6:3A00..3AFF
Summary: raw_targets=4, xref_hits=4, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:3ACE (weak, caller DF:4DEE)
- C6:3A08 (suspect, caller C6:D049)
- C6:3A13 (suspect, caller C6:39AE)
- C6:3A3A (suspect, caller C6:43ED)

Backtrack scan (`reports/c6_3a00_3aff_backtrack.json`):
- C6:3A36->3A3A score=4, start=0x08
- C6:3A08->3A13 score=2, start=0x0C
- C6:3AC6->3ACE score=2, start=0x3B
- C6:3A08->3A08 score=1, start=0x0C

Anchor reports:
- C6:3ACE: strong=0, weak=1, invalid=1
- C6:3A08: strong=0, weak=1, invalid=19
- C6:3A13: strong=0, weak=1, invalid=0
- C6:3A3A: strong=0, weak=1, invalid=2

ROM-byte check:
- C6:3ACE = `05 3B 14 3B 15 3B 06 3B 80 07 3B 16`
- C6:3A08 = `0C 09 84 09 0C 09 84 09 0C 09 28 0C`
- C6:3A13 = `0C 0C 09 00 D9 16 DA 16 E9 16 EA 16`
- C6:3A3A = `84 09 12 3D 13 84 11 14 44 3D 15 84`

Verdict: no strong anchors and high invalid contamination on key suspect (`3A08`); freeze.

### C6:3D00..3DFF
Summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:3D0B (weak, caller C6:B89C)
- C6:3D1A (suspect, caller C6:594C)
- C6:3D61 (suspect, caller C6:9FBB)

Backtrack scan (`reports/c6_3d00_3dff_backtrack.json`):
- C6:3D08->3D0B score=6, start=0x08
- C6:3D61->3D61 score=3, start=0x78
- C6:3D16->3D1A score=2, start=0x7F

Anchor reports:
- C6:3D0B: strong=0, weak=1, invalid=2
- C6:3D1A: strong=0, weak=1, invalid=0
- C6:3D61: strong=0, weak=1, invalid=0

ROM-byte check:
- C6:3D0B = `08 E2 0C D4 8A 11 6F 40 6E 00 40 7F`
- C6:3D1A = `4E 00 4F 00 00 5E 00 5F 00 6E 00 6F`
- C6:3D61 = `78 20 BB 08 48 BA 48 80 0A 60 1D 61`

Verdict: all candidates remain weak/suspect-only with unresolved caller ownership; freeze.

---

## Reject/mixed lane notes

- C6:3600 rejected on `hard_bad=1` with invalid `C6:3600` and only suspect companion targets.
- C6:3700 remains mixed-lane carry: weak targets `C6:37C4` (3 hits) and `C6:37FC` (1 hit), no strong ownership evidence.
- C6:3900 remains mixed-lane carry with suspect-only `C6:391C`.
- C6:3B00 is invalid-only (`C6:3B00`, `C6:3B80`) and hard rejected.
- C6:3C00 is the most contaminated page in this block (`xref=23`, `hard_bad=22`), dominated by invalid `C6:3CC4` (21 hits).
- C6:3E00 rejected on invalid companion `C6:3E12` despite weak `C6:3E04`.
- C6:3F00 stays local-control empty page.

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
- C6:3600..3FFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_3600_3fff_seam_block.json`
- `reports/c6_3600_3fff_seam_block.md`
- `reports/c6_3a00_3aff_backtrack.json`
- `reports/c6_3d00_3dff_backtrack.json`
- `reports/c6_3a00_3aff_flow.json` (manual-page extraction)
- `reports/c6_3d00_3dff_flow.json` (manual-page extraction)
- `reports/C6_3ACE_anchor.json`
- `reports/C6_3A08_anchor.json`
- `reports/C6_3A13_anchor.json`
- `reports/C6_3A3A_anchor.json`
- `reports/C6_3D0B_anchor.json`
- `reports/C6_3D1A_anchor.json`
- `reports/C6_3D61_anchor.json`

---

## New live seam: C6:4000..

Next unprocessed block starts at **C6:4000**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:4000 --pages 10 --json > reports/c6_4000_49ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_4000_49ff_seam_block.json --output reports/c6_4000_49ff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_40.
