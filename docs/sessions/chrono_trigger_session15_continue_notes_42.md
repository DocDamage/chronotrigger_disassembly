# Chrono Trigger Session 15 — Continuation Notes 42

## Block closed: C6:5400..C6:5DFF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:5400 | candidate_code_lane | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:5500 | candidate_code_lane | mixed_lane_continue | freeze | single weak target (`C6:55C4`) with unresolved ownership |
| C6:5600 | mixed_command_data | mixed_lane_continue | freeze | three weak targets but `soft_bad=1` and no strong anchors |
| C6:5700 | candidate_code_lane | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:5800 | text_ascii_heavy | mixed_lane_continue | freeze | weak/suspect pair on text-heavy page, no strong anchors |
| C6:5900 | mixed_command_data | local_control_only | freeze | lone suspect target `C6:5958` |
| C6:5A00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | invalid-only traffic (`C6:5AC4` invalid x5) |
| C6:5B00 | candidate_code_lane | manual_owner_boundary_review | freeze | weak/suspect-only target set with unresolved callers |
| C6:5C00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | contains hard bad start (`hard_bad=1`) in mixed lane |
| C6:5D00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | invalid-only target `C6:5D80` |

---

## Manual-owner page (anchor detail)

### C6:5B00..5BFF
Summary: raw_targets=5, xref_hits=6, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:5B1D (weak, caller C6:4FF6)
- C6:5B00 (suspect, callers C6:321A and C6:3C28)
- C6:5B12 (suspect, caller C6:5888)
- C6:5B21 (suspect, caller C6:AF02)
- C6:5B5A (suspect, caller C6:9E0A)

Backtrack scan (`reports/c6_5b00_5bff_backtrack.json`):
- C6:5B1B->5B1D score=6, start=0x08
- C6:5B1B->5B21 score=6, start=0x08
- C6:5B00->5B00 score=3, start=0x15
- C6:5B4E->5B5A score=2, start=0x0E
- C6:5B12->5B12 score=1, start=0xF0

Anchor reports:
- C6:5B1D: strong=0, weak=1, invalid=0
- C6:5B00: strong=0, weak=2, invalid=5
- C6:5B12: strong=0, weak=1, invalid=2
- C6:5B21: strong=0, weak=1, invalid=0
- C6:5B5A: strong=0, weak=1, invalid=3

ROM-byte check:
- C6:5B1D = `B0 23 A3 08 48 38 0F AF 08 33 D2 10`
- C6:5B00 = `15 D6 01 23 F1 56 10 24 0A 16 02 00`
- C6:5B12 = `F0 86 18 87 18 F8 36 00 65 08 F0 B0`
- C6:5B21 = `48 38 0F AF 08 33 D2 10 34 78 60 01`
- C6:5B5A = `11 DE 0E BF 08 25 36 01 12 08 03 00`

Verdict: all candidates remain weak/suspect-only with no strong anchor evidence and notable invalid overlap on most entries; freeze.

---

## Reject/mixed lane notes

- C6:5500 remains mixed-lane carry on lone weak `C6:55C4` (3 hits), no strong ownership.
- C6:5600 remains mixed-lane carry (`soft_bad=1`) despite three weak hits (`C6:5621`, `C6:568E`, `C6:56C4`).
- C6:5800 stays mixed carry on text-heavy lane with one weak (`C6:58A7`) and one suspect (`C6:5856`).
- C6:5A00 hard rejected as invalid-only (`C6:5AC4`, 5 hits).
- C6:5C00 rejected with hard-bad contamination (`hard_bad=1`) despite weak `C6:5CE3`.
- C6:5D00 hard rejected on invalid-only `C6:5D80`.

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
- C6:5400..5DFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_5400_5dff_seam_block.json`
- `reports/c6_5400_5dff_seam_block.md`
- `reports/c6_5b00_5bff_backtrack.json`
- `reports/c6_5b00_5bff_flow.json` (manual-page extraction)
- `reports/C6_5B1D_anchor.json`
- `reports/C6_5B00_anchor.json`
- `reports/C6_5B12_anchor.json`
- `reports/C6_5B21_anchor.json`
- `reports/C6_5B5A_anchor.json`

---

## New live seam: C6:5E00..

Next unprocessed block starts at **C6:5E00**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:5E00 --pages 10 --json > reports/c6_5e00_67ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_5e00_67ff_seam_block.json --output reports/c6_5e00_67ff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_43.
