# Chrono Trigger Session 15 — Continuation Notes 46

## Block closed: C6:7C00..C6:85FF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:7C00 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | suspect/invalid mix with `hard_bad=1` |
| C6:7D00 | mixed_command_data | mixed_lane_continue | freeze | lone suspect target `C6:7D00` |
| C6:7E00 | mixed_command_data | manual_owner_boundary_review | freeze | weak-only target with unresolved callers and high invalid overlap |
| C6:7F00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | severe contamination (`hard_bad=8`, `soft_bad=1`) |
| C6:8000 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | many weak hits but still `hard_bad=2` |
| C6:8100 | mixed_command_data | mixed_lane_continue | freeze | lone suspect target `C6:81E2` |
| C6:8200 | mixed_command_data | manual_owner_boundary_review | freeze | weak/suspect pair remains unresolved, no strong anchors |
| C6:8300 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | invalid companion target `C6:8326` (`hard_bad=1`) |
| C6:8400 | mixed_command_data | local_control_only | freeze | suspect-only targets (`C6:8421`, `C6:846E`) |
| C6:8500 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | invalid boundary-bait target `C6:85FF` (`hard_bad=1`) |

---

## Manual-owner pages (anchor detail)

### C6:7E00..7EFF
Summary: raw_targets=1, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:7EA9 (weak, callers C6:E20E and C6:E810)

Backtrack scan (`reports/c6_7e00_7eff_backtrack.json`):
- C6:7E9C->7EA9 score=6, start=0xA0

Anchor reports:
- C6:7EA9: strong=0, weak=2, invalid=19

ROM-byte check:
- C6:7EA9 = `72 23 20 23 88 88 88 15 E8 16 20 21`

Verdict: target remains weak-only with very high invalid overlap; freeze.

### C6:8200..82FF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:826E (weak, caller C0:EABB)
- C6:8200 (suspect, caller C6:414B)

Backtrack scan (`reports/c6_8200_82ff_backtrack.json`):
- C6:826A->826E score=4, start=0x46
- C6:8200->8200 score=-1, start=0x36

Anchor reports:
- C6:826E: strong=0, weak=1, invalid=0
- C6:8200: strong=0, weak=1, invalid=27

ROM-byte check:
- C6:826E = `B6 0C FB 0A 40 02 0C 38 21 0B 19 83`
- C6:8200 = `36 25 A6 21 1F 44 07 30 65 43 43 02`

Verdict: no strong ownership, and `C6:8200` is heavily invalid-contaminated; freeze.

---

## Reject/mixed lane notes

- C6:7F00 is heavily contaminated (`hard_bad=8`, `soft_bad=1`), dominated by invalid `C6:7FC4`.
- C6:8000 rejected despite strong weak-hit volume (`sw=7`) because `hard_bad=2` remains unresolved.
- C6:7D00 and C6:8100 remain mixed-lane carries with suspect-only single targets.
- C6:8500 rejected due to invalid boundary-bait `C6:85FF`.

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
- C6:7C00..85FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_7c00_85ff_seam_block.json`
- `reports/c6_7c00_85ff_seam_block.md`
- `reports/c6_7e00_7eff_backtrack.json`
- `reports/c6_8200_82ff_backtrack.json`
- `reports/c6_7e00_7eff_flow.json` (manual-page extraction)
- `reports/c6_8200_82ff_flow.json` (manual-page extraction)
- `reports/C6_7EA9_anchor.json`
- `reports/C6_826E_anchor.json`
- `reports/C6_8200_anchor.json`

---

## New live seam: C6:8600..

Next unprocessed block starts at **C6:8600**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:8600 --pages 10 --json > reports/c6_8600_8fff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_8600_8fff_seam_block.json --output reports/c6_8600_8fff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_47.
