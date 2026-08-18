# Chrono Trigger Session 15 — Continuation Notes 45

## Block closed: C6:7200..C6:7BFF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:7200 | mixed_command_data | local_control_only | freeze | suspect-only targets (`C6:7200`, `C6:7230`) |
| C6:7300 | mixed_command_data | mixed_lane_continue | freeze | lone weak target `C6:73C4` |
| C6:7400 | mixed_command_data | local_control_only | freeze | lone suspect target `C6:7473` |
| C6:7500 | mixed_command_data | mixed_lane_continue | freeze | empty mixed lane (`raw=0`, `xref=0`) |
| C6:7600 | mixed_command_data | local_control_only | freeze | suspect-only target `C6:76A9` |
| C6:7700 | mixed_command_data | mixed_lane_continue | freeze | lone suspect target `C6:7707` |
| C6:7800 | mixed_command_data | manual_owner_boundary_review | freeze | weak/suspect-only ownership with no strong anchors |
| C6:7900 | mixed_command_data | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:7A00 | mixed_command_data | local_control_only | freeze | lone suspect target `C6:7A08` |
| C6:7B00 | candidate_code_lane | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |

---

## Manual-owner page (anchor detail)

### C6:7800..78FF
Summary: raw_targets=4, xref_hits=9, strong_or_weak=5, hard_bad=0, soft_bad=0

Targets:
- C6:78C4 (weak, callers CA:9DB9, CB:238C, CB:4CED, CB:8C39, CB:A5E5)
- C6:7818 (weak, caller C6:4B4F)
- C6:7801 (suspect, callers C6:8A3D and C6:9B21)
- C6:786A (suspect, caller C6:D8E2)

Backtrack scan (`reports/c6_7800_78ff_backtrack.json`):
- C6:786A->786A score=5, start=0x20
- C6:78B4->78C4 score=4, start=0x62
- C6:7814->7818 score=2, start=0x79
- C6:7801->7801 score=1, start=0x23

Anchor reports:
- C6:78C4: strong=0, weak=5, invalid=11
- C6:7818: strong=0, weak=1, invalid=3
- C6:7801: strong=0, weak=2, invalid=11
- C6:786A: strong=0, weak=1, invalid=0

ROM-byte check:
- C6:78C4 = `08 88 79 5E 44 04 99 23 23 97 9E 99`
- C6:7818 = `9A 05 01 AB 01 FC FD FF 35 3C 54 55`
- C6:7801 = `23 CD 0A E3 11 79 23 4E 93 09 7B 7C`
- C6:786A = `20 C1 B2 16 8A 9A DF ED 77 DB 03 E7`

Verdict: no strong anchors and heavy invalid overlap on key weak/suspect entries (`78C4`, `7801`); freeze.

---

## Reject/mixed lane notes

- C6:7300 remains mixed-lane carry on weak `C6:73C4` (2 hits).
- C6:7500 remains empty mixed lane (`raw=0`, `xref=0`).
- C6:7700 remains mixed-lane carry with suspect-only `C6:7707`.
- No page in this block triggered hard-bad reject posture; the block is dominated by local-control and mixed-lane pages.

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
- C6:7200..7BFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_7200_7bff_seam_block.json`
- `reports/c6_7200_7bff_seam_block.md`
- `reports/c6_7800_78ff_backtrack.json`
- `reports/c6_7800_78ff_flow.json` (manual-page extraction)
- `reports/C6_78C4_anchor.json`
- `reports/C6_7818_anchor.json`
- `reports/C6_7801_anchor.json`
- `reports/C6_786A_anchor.json`

---

## New live seam: C6:7C00..

Next unprocessed block starts at **C6:7C00**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:7C00 --pages 10 --json > reports/c6_7c00_85ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_7c00_85ff_seam_block.json --output reports/c6_7c00_85ff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_46.
