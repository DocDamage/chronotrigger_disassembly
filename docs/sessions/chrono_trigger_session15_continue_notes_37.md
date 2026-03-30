# Chrono Trigger Session 15 — Continuation Notes 37

## Block closed: C6:2200..C6:2BFF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:2200 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | heavy soft-bad contamination (`soft_bad=10`) plus `hard_bad=1` |
| C6:2300 | mixed_command_data | mixed_lane_continue | freeze | mixed carry lane (`soft_bad=6`) with only one weak target |
| C6:2400 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | explicit invalid entries (`C6:2480`, `C6:24DB`) with `hard_bad=2` |
| C6:2500 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | weak/suspect-only ownership, all callers unresolved |
| C6:2600 | mixed_command_data | local_control_only | freeze | suspect-only local control (`C6:2617`, `C6:2621`) |
| C6:2700 | candidate_code_lane | local_control_only | freeze | suspect-only branch pocket (`C6:2726`, `C6:2750`, `C6:2780`) |
| C6:2800 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | strong contamination (`hard_bad=10`, `soft_bad=2`) |
| C6:2900 | mixed_command_data | local_control_only | freeze | no incoming targets (`raw=0`, `xref=0`) |
| C6:2A00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | invalid-only targets (`C6:2A28`, `C6:2A4D`) |
| C6:2B00 | mixed_command_data | mixed_lane_continue | freeze | lone weak target `C6:2BCD` with unresolved ownership |

---

## Manual-owner page (anchor detail)

### C6:2500..25FF
Summary: raw_targets=4, xref_hits=4, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C6:254D (weak, caller C6:89CD)
- C6:25BF (weak, caller C6:E8E9)
- C6:2514 (suspect, caller C6:B7C2)
- C6:2533 (suspect, caller C6:94EA)

Backtrack scan (`reports/c6_2500_25ff_backtrack.json`):
- C6:2548->254D score=4, start=0x20
- C6:2533->2533 score=3, start=0xCE
- C6:2512->2514 score=2, start=0x3C
- C6:25B6->25BF score=2, start=0xAC

Anchor reports:
- C6:2514: strong=0, weak=1, invalid=0
- C6:2533: strong=0, weak=1, invalid=1
- C6:254D: strong=0, weak=1, invalid=7
- C6:25BF: strong=0, weak=1, invalid=1

ROM-byte check:
- C6:2514 = `35 02 00 3D 08 14 3C C9 34 55 3E 00`
- C6:2533 = `CE 09 16 40 08 08 1D 2A 98 CB 30 96`
- C6:254D = `9A 0F 18 21 9A 2A 12 18 21 94 F5 30`
- C6:25BF = `50 21 BC 57 31 00 C0 2E 15 3F 08 0A`

Verdict: page remains weak/suspect-only with unresolved caller ownership and no strong anchors; freeze.

---

## Reject/mixed lane notes

- C6:2200 rejected for combined contamination (`hard_bad=1`, `soft_bad=10`) despite one weak target (`C6:2221`).
- C6:2300 remains mixed-lane carry (`soft_bad=6`) with only one weak candidate (`C6:23C4`).
- C6:2400 rejected on explicit invalid starts (`C6:2480`, `C6:24DB`).
- C6:2800 is the most contaminated page in this block (`xref=21`, `hard_bad=10`, `soft_bad=2`), so weak `C6:2809` is insufficient.
- C6:2A00 is invalid-only (`C6:2A28`, `C6:2A4D`) and remains hard reject.
- C6:2B00 stays mixed-lane carry with a single unresolved weak target (`C6:2BCD`).

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
- C6:2200..2BFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_2200_2bff_seam_block.json`
- `reports/c6_2200_2bff_seam_block.md`
- `reports/c6_2500_25ff_backtrack.json`
- `reports/c6_2500_25ff_flow.json` (manual-page extraction)
- `reports/C6_2514_anchor.json`
- `reports/C6_2533_anchor.json`
- `reports/C6_254D_anchor.json`
- `reports/C6_25BF_anchor.json`

---

## New live seam: C6:2C00..

Next unprocessed block starts at **C6:2C00**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:2C00 --pages 10 --json > reports/c6_2c00_35ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_2c00_35ff_seam_block.json --output reports/c6_2c00_35ff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_38.
