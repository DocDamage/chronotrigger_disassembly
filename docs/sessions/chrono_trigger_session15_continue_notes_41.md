# Chrono Trigger Session 15 — Continuation Notes 41

## Block closed: C6:4A00..C6:53FF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:4A00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | weak/suspect mix with explicit contamination (`hard_bad=1`, `soft_bad=1`) |
| C6:4B00 | candidate_code_lane | local_control_only | freeze | suspect-only targets (`C6:4B00`, `C6:4B2B`) |
| C6:4C00 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | weak hits present but `hard_bad=2`, `soft_bad=1` |
| C6:4D00 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | high-noise lane with `hard_bad=3`, `soft_bad=1` |
| C6:4E00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | severe invalid contamination (`xref=20`, `hard_bad=16`) |
| C6:4F00 | mixed_command_data | local_control_only | freeze | lone suspect target `C6:4F02` |
| C6:5000 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | extreme contamination (`xref=25`, `hard_bad=21`) |
| C6:5100 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | single weak target remains unresolved, no strong anchor |
| C6:5200 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | invalid-led page (`C6:5285` invalid x2) |
| C6:5300 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | mixed weak/invalid targets with `hard_bad=2` |

---

## Manual-owner page (anchor detail)

### C6:5100..51FF
Summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:5108 (weak, caller C6:49B4)

Backtrack scan (`reports/c6_5100_51ff_backtrack.json`):
- C6:5104->5108 score=4, start=0xF7

Anchor reports:
- C6:5108: strong=0, weak=1, invalid=1

ROM-byte check:
- C6:5108 = `1D D2 1D FB 1D F9 1E 10 00 54 00 7D`

Verdict: single weak unresolved caller plus one invalid companion caller gives no promotable ownership signal; freeze.

---

## Reject/mixed lane notes

- C6:4A00 rejected on combined bad starts (`hard_bad=1`, `soft_bad=1`) despite two weak entries (`C6:4A4A`, `C6:4AB8`).
- C6:4C00 rejected with two hard bad starts and one soft bad start even though three weak targets are present (`C6:4CC8`, `C6:4CE3`, `C6:4CE4`).
- C6:4D00 rejected on persistent contamination (`raw=11`, `xref=13`, `hard_bad=3`, `soft_bad=1`).
- C6:4E00 is one of the heaviest invalid pages so far (`hard_bad=16`; includes invalid-heavy `C6:4EA6`).
- C6:5000 is the most contaminated page in this block (`hard_bad=21` on `xref=25`).
- C6:5200 and C6:5300 both remain hard rejects due to invalid targets (`C6:5285`, `C6:5305`, `C6:5310`).

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
- C6:4A00..53FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_4a00_53ff_seam_block.json`
- `reports/c6_4a00_53ff_seam_block.md`
- `reports/c6_5100_51ff_backtrack.json`
- `reports/c6_5100_51ff_flow.json` (manual-page extraction)
- `reports/C6_5108_anchor.json`

---

## New live seam: C6:5400..

Next unprocessed block starts at **C6:5400**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:5400 --pages 10 --json > reports/c6_5400_5dff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_5400_5dff_seam_block.json --output reports/c6_5400_5dff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_42.
