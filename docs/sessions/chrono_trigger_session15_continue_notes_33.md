# Chrono Trigger Session 15 — Continuation Notes 33

## Block closed: C5:FA00..C6:03FF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C5:FA00 | dead_zero_field | dead_lane_reject | freeze | dead-lane page with zero ownership evidence |
| C5:FB00 | dead_zero_field | dead_lane_reject | freeze | hard_bad=3 on zero field (`FB00/FB04/FBE2` invalid) |
| C5:FC00 | dead_zero_field | dead_lane_reject | freeze | hard_bad=4 on zero field (`FC20/FC58/FCC3` etc.) |
| C5:FD00 | dead_zero_field | dead_lane_reject | freeze | hard_bad=6 on zero field |
| C5:FE00 | dead_zero_field | dead_lane_reject | freeze | hard_bad=10 on zero field |
| C5:FF00 | dead_zero_field | dead_lane_reject | freeze | hard_bad=44 (`FFF0` heavily hit invalid target) |
| C6:0000 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | extreme noise (`raw=55`, `xref=82`, soft_bad=33, hard_bad=3) |
| C6:0100 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=7 with mixed invalid/suspect crowding |
| C6:0200 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | hard_bad=1 (`C6:02A5` invalid) despite multiple weak hits |
| C6:0300 | candidate_code_lane | manual_owner_boundary_review | freeze | weak/suspect-only targets and unresolved caller quality |

---

## Manual-owner pages (anchor detail)

### C6:0300..03FF
Summary: raw_targets=4, xref_hits=4, strong_or_weak=3, hard_bad=0, soft_bad=0

Targets:
- C6:0301 (weak, caller C6:91D1)
- C6:0310 (weak, caller C6:E726)
- C6:0378 (suspect, caller C6:2F2F)
- C6:03EE (weak, caller C6:5BFC)

Backtrack scan (`reports/c6_0300_03ff_backtrack.json`):
- C6:036F->0378 score=6, start=0x20
- C6:030B->0310 score=4, start=0x18
- C6:03E8->03EE score=4, start=0x93
- C6:0301->0301 score=1, start=0xE7

Anchor reports:
- C6:0301: strong=0, weak=1, invalid=19
- C6:0310: strong=0, weak=1, invalid=34
- C6:0378: strong=0, weak=1, invalid=3
- C6:03EE: strong=0, weak=1, invalid=0

ROM-byte check:
- C6:0301 = `E7 27 A7 93 3F 93 3F 61 00 80 18 E0`
- C6:0310 = `F0 80 00 78 E0 18 D0 00 D0 00 BF 00`
- C6:0378 = `66 13 E8 12 3F 07 33 00 0F 98 CB 84`
- C6:03EE = `7F 00 0A 9F 60 43 11 3C C0 8E 00 70`

Verdict: even with score-6 backtrack at C6:036F, all targets remain weak/suspect-only and are surrounded by high invalid-anchor noise; no promotable boundary.

---

## Reject/dead-lane notes

- C5:FA00..C5:FFFF are dead-lane pages; bytes are zero-filled and ownership is non-promotable.
  - C5:FB00 = `00 00 00 00 00 00 00 00 00 00 00 00`
  - C5:FBE2 = `00 00 00 00 00 00 00 00 00 00 00 00`
  - C5:FC20 = `00 00 00 00 00 00 00 00 00 00 00 00`
  - C5:FFF0 = `00 00 00 00 00 00 00 00 00 00 00 00`
- C6:0000: high-noise mixed-command reject (`raw=55`, `xref=82`, `hard_bad=3`, `soft_bad=33`).
  - Notable invalid starts include `C6:0003`; weak hits (e.g., `C6:0080`, `C6:00E2`) are drowned by suspect/invalid traffic.
- C6:0100: reject with `hard_bad=7`, `soft_bad=2`; invalid concentration at `C6:0111`, `C6:016B`, `C6:01B1`, `C6:01B3`, `C6:01E6`.
- C6:0200: reject with `hard_bad=1` (`C6:02A5` invalid) despite weak starts (`C6:0200`, `C6:0202`).

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
- C5:FA00..C6:03FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c5_fa00_c6_03ff_seam_block.json`
- `reports/c5_fa00_c6_03ff_seam_block.md`
- `reports/c6_0300_03ff_backtrack.json`
- `reports/C6_0301_anchor.json`
- `reports/C6_0310_anchor.json`
- `reports/C6_0378_anchor.json`
- `reports/C6_03EE_anchor.json`
- `reports/c6_0300_03ff_flow.json` (manual-page extraction)
- `reports/c6_0000_00ff_flow.json` (reject-page support)
- `reports/c6_0100_01ff_flow.json` (reject-page support)
- `reports/c6_0200_02ff_flow.json` (reject-page support)

---

## New live seam: C6:0400..

Next unprocessed block starts at **C6:0400**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:0400 --pages 10 --json > reports/c6_0400_0dff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_0400_0dff_seam_block.json --output reports/c6_0400_0dff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_34.
