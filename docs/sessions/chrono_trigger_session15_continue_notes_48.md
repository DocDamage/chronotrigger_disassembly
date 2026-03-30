# Chrono Trigger Session 15 — Continuation Notes 48

## Block closed: C6:9000..C6:99FF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:9000 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | suspect pair plus invalid `C6:908C` (`hard_bad=1`, `soft_bad=1`) |
| C6:9100 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | invalid companion target `C6:910C` (`hard_bad=1`) despite weak hits |
| C6:9200 | mixed_command_data | manual_owner_boundary_review | freeze | weak-only target with unresolved ownership and no strong anchors |
| C6:9300 | mixed_command_data | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:9400 | mixed_command_data | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:9500 | mixed_command_data | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:9600 | mixed_command_data | manual_owner_boundary_review | freeze | weak/suspect mix across four targets with unresolved ownership |
| C6:9700 | mixed_command_data | manual_owner_boundary_review | freeze | lone weak target with no strong support |
| C6:9800 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | invalid companion target `C6:985B` (`hard_bad=1`) in mixed weak/suspect lane |
| C6:9900 | mixed_command_data | mixed_lane_continue | freeze | no ingress targets and no local clusters |

---

## Manual-owner pages (anchor detail)

### C6:9200..92FF
Summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:9231 (weak, caller C6:D959)

Backtrack scan (`reports/c6_9200_92ff_backtrack.json`):
- C6:9221->9231 score=4, start=0x79

Anchor reports:
- C6:9231: strong=0, weak=1, invalid=0

ROM-byte check:
- C6:9231 = `58 00 E4 00 00 29 01 01 F8 15 50 89`

Verdict: lone weak unresolved anchor, no strong support; freeze.

### C6:9600..96FF
Summary: raw_targets=4, xref_hits=4, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C6:9600 (weak, caller C6:41E2)
- C6:9622 (weak, caller C6:2BE9)
- C6:9621 (suspect, caller C6:B811)
- C6:9651 (suspect, caller C6:71F0)

Backtrack scan (`reports/c6_9600_96ff_backtrack.json`):
- C6:9619->9621 score=6, start=0x08
- C6:9619->9622 score=6, start=0x08
- C6:9651->9651 score=3, start=0x8B
- C6:9600->9600 score=-1, start=0x23

Anchor reports:
- C6:9600: strong=0, weak=1, invalid=13
- C6:9622: strong=0, weak=1, invalid=2
- C6:9621: strong=0, weak=1, invalid=0
- C6:9651: strong=0, weak=1, invalid=0

ROM-byte check:
- C6:9600 = `23 03 01 00 B7 00 E5 FC 3D 35 44 43`
- C6:9622 = `FA 21 DF F3 9C 04 05 38 21 2F 02 EF`
- C6:9621 = `47 FA 21 DF F3 9C 04 05 38 21 2F 02`
- C6:9651 = `8B 23 8D 61 4F 03 FC FC 24 23 AF FB`

Verdict: mixed weak/suspect entries remain unresolved and no strong ownership anchors emerged; freeze.

### C6:9700..97FF
Summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:9721 (weak, caller C6:6F38)

Backtrack scan (`reports/c6_9700_97ff_backtrack.json`):
- C6:971D->9721 score=6, start=0x20

Anchor reports:
- C6:9721: strong=0, weak=1, invalid=1

ROM-byte check:
- C6:9721 = `F9 FD E0 01 23 23 60 34 35 44 44 45`

Verdict: single weak unresolved anchor with invalid overlap and no strong support; freeze.

---

## Reject/mixed lane notes

- C6:9000 rejected on invalid `C6:908C` plus suspect companions (`hard_bad=1`, `soft_bad=1`).
- C6:9100 rejected despite two weak hits (`C6:9100`, `C6:9124`) because invalid `C6:910C` keeps `hard_bad=1`.
- C6:9800 rejected due to invalid target `C6:985B` while other entries stay weak/suspect-only.
- C6:9900 remains mixed-lane carry with no ingress and no local code islands.

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
- C6:7C00..85FF: 0 promotions (notes_46)
- C6:8600..8FFF: 0 promotions (notes_47)
- C6:9000..99FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_9000_99ff_seam_block.json`
- `reports/c6_9000_99ff_seam_block.md`
- `reports/c6_9200_92ff_backtrack.json`
- `reports/c6_9600_96ff_backtrack.json`
- `reports/c6_9700_97ff_backtrack.json`
- `reports/c6_9200_92ff_flow.json` (manual-page extraction)
- `reports/c6_9600_96ff_flow.json` (manual-page extraction)
- `reports/c6_9700_97ff_flow.json` (manual-page extraction)
- `reports/C6_9231_anchor.json`
- `reports/C6_9600_anchor.json`
- `reports/C6_9622_anchor.json`
- `reports/C6_9621_anchor.json`
- `reports/C6_9651_anchor.json`
- `reports/C6_9721_anchor.json`

---

## New live seam: C6:9A00..

Next unprocessed block starts at **C6:9A00**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:9A00 --pages 10 --json > reports/c6_9a00_a3ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_9a00_a3ff_seam_block.json --output reports/c6_9a00_a3ff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_49.
