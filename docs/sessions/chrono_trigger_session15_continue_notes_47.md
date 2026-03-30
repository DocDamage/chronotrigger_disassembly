# Chrono Trigger Session 15 — Continuation Notes 47

## Block closed: C6:8600..C6:8FFF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:8600 | mixed_command_data | mixed_lane_continue | freeze | weak/suspect pair with unresolved ownership |
| C6:8700 | mixed_command_data | manual_owner_boundary_review | freeze | weak-only target with no strong anchors |
| C6:8800 | mixed_command_data | local_control_only | freeze | suspect-only targets (`C6:8823`, `C6:8877`) |
| C6:8900 | mixed_command_data | manual_owner_boundary_review | freeze | weak-only target with unresolved caller ownership |
| C6:8A00 | mixed_command_data | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:8B00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | invalid companion target `C6:8B08` (`hard_bad=1`) |
| C6:8C00 | mixed_command_data | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:8D00 | mixed_command_data | local_control_only | freeze | lone suspect target `C6:8D8C` |
| C6:8E00 | text_ascii_heavy | local_control_only | freeze | no ingress targets (`raw=0`, `xref=0`) |
| C6:8F00 | mixed_command_data | manual_owner_boundary_review | freeze | weak/suspect pair with no strong anchor evidence |

---

## Manual-owner pages (anchor detail)

### C6:8700..87FF
Summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:8710 (weak, caller C6:25F1)

Backtrack scan (`reports/c6_8700_87ff_backtrack.json`):
- C6:8710->8710 score=3, start=0x4B

Anchor reports:
- C6:8710: strong=0, weak=1, invalid=3

ROM-byte check:
- C6:8710 = `4B 2D 87 89 23 18 F8 19 1A 25 CA 14`

Verdict: single weak unresolved anchor with invalid overlap; freeze.

### C6:8900..89FF
Summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:8988 (weak, caller C6:923D)

Backtrack scan (`reports/c6_8900_89ff_backtrack.json`):
- C6:8986->8988 score=6, start=0x48

Anchor reports:
- C6:8988: strong=0, weak=1, invalid=0

ROM-byte check:
- C6:8988 = `12 00 30 21 C0 11 20 11 12 10 12 29`

Verdict: lone weak unresolved anchor, no strong support; freeze.

### C6:8F00..8FFF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C6:8FBD (weak, caller C6:B9C3)
- C6:8F21 (suspect, caller C6:7C9B)

Backtrack scan (`reports/c6_8f00_8fff_backtrack.json`):
- C6:8FB4->8FBD score=6, start=0x08
- C6:8F21->8F21 score=3, start=0xC0

Anchor reports:
- C6:8FBD: strong=0, weak=1, invalid=0
- C6:8F21: strong=0, weak=1, invalid=1

ROM-byte check:
- C6:8FBD = `24 88 05 BD 26 6A 00 04 06 05 D9 2F`
- C6:8F21 = `C0 F8 08 B8 42 43 32 1B E2 0A 3F 02`

Verdict: both entries remain weak/suspect-only with unresolved ownership; freeze.

---

## Reject/mixed lane notes

- C6:8B00 is the only hard reject in this block (`hard_bad=1`) due to invalid `C6:8B08`.
- C6:8600 remains mixed-lane carry on weak `C6:8601` plus suspect `C6:8600`.
- Block is dominated by local-control/manual pages with low ingress volume and no strong ownership anchors.

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
- C6:8600..8FFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_8600_8fff_seam_block.json`
- `reports/c6_8600_8fff_seam_block.md`
- `reports/c6_8700_87ff_backtrack.json`
- `reports/c6_8900_89ff_backtrack.json`
- `reports/c6_8f00_8fff_backtrack.json`
- `reports/c6_8700_87ff_flow.json` (manual-page extraction)
- `reports/c6_8900_89ff_flow.json` (manual-page extraction)
- `reports/c6_8f00_8fff_flow.json` (manual-page extraction)
- `reports/C6_8710_anchor.json`
- `reports/C6_8988_anchor.json`
- `reports/C6_8FBD_anchor.json`
- `reports/C6_8F21_anchor.json`

---

## New live seam: C6:9000..

Next unprocessed block starts at **C6:9000**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:9000 --pages 10 --json > reports/c6_9000_99ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_9000_99ff_seam_block.json --output reports/c6_9000_99ff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_48.
