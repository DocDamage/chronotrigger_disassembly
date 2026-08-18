# Chrono Trigger Session 15 — Continuation Notes 31

## Block closed: C5:E600..C5:EFFF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C5:E600 | branch_fed_control_pocket | local_control_only | freeze | lone suspect target `C5:E6C8`; no weak/strong ownership evidence |
| C5:E700 | candidate_code_lane | manual_owner_boundary_review | freeze | single weak target `C5:E790` with unresolved caller only |
| C5:E800 | candidate_code_lane | local_control_only | freeze | lone suspect target `C5:E853` with soft_bad=1 |
| C5:E900 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | two weak-only targets (`C5:E902`, `C5:E976`) with unresolved callers |
| C5:EA00 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | hard_bad=2 from invalid starts `C5:EA87` and `C5:EA9F` |
| C5:EB00 | mixed_command_data | mixed_lane_continue | freeze | weak target `C5:EB23` sits in mixed lane without boundary support |
| C5:EC00 | mixed_command_data | mixed_lane_continue | freeze | no targets and no xrefs on mixed page |
| C5:ED00 | branch_fed_control_pocket | local_control_only | freeze | no targets, no xrefs |
| C5:EE00 | candidate_code_lane | mixed_lane_continue | freeze | no targets/xrefs and no ownership evidence |
| C5:EF00 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | hard_bad=2 + soft_bad=1 (invalid `C5:EF00` and `C5:EFD2`) |

---

## Manual-owner pages (anchor detail)

### C5:E700..E7FF
Summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0

Target:
- C5:E790 (weak, caller C5:0E90)

Backtrack scan (`reports/c5_e700_e7ff_backtrack.json`):
- C5:E781->E790 score=6, start=0x08

Anchor report:
- C5:E790: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:E790 = `44 30 30 20 20 05 08 04 CE 10 10 40`

Verdict: lone weak anchor with no corroborating owner boundary; byte flow remains table/control-like.

### C5:E900..E9FF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C5:E902 (weak, caller C5:0277)
- C5:E976 (weak, caller C5:2D4E)

Backtrack scan (`reports/c5_e900_e9ff_backtrack.json`):
- C5:E900->E902 score=4, start=0x64
- C5:E969->E976 score=2, start=0xAA

Anchor reports:
- C5:E902: strong=0, weak=1, invalid=0
- C5:E976: strong=0, weak=1, invalid=1

ROM-byte check:
- C5:E902 = `D6 04 B3 0A 70 2B 40 6D 09 04 02 00`
- C5:E976 = `0F 74 1F 57 0F B4 31 BB 00 27 73 2B`

Verdict: both entries remain weak-only and lack prologue-quality starts; freeze.

---

## Reject/mixed lane notes

- C5:EA00: rejected immediately on hard_bad=2 (both targets invalid).
  - C5:EA87 = `00 30 04 E0 20 CC C0 50 81 0E 7F CE`
  - C5:EA9F = `80 E0 30 80 80 06 B7 09 C0 C0 00 A0`
- C5:EF00: rejected on hard_bad=2 + soft_bad=1 despite several weak hits.
  - Invalid starts include `C5:EF00` and `C5:EFD2`
  - C5:EF00 = `80 08 25 09 28 14 01 03 95 02 00 07`
  - C5:EFD2 = `80 E0 C6 E0 A4 40 FF 43 E4 C0 DC 90`
- C5:E600/E800: local-control pages with suspect-only targets (`C5:E6C8`, `C5:E853`).
- C5:EB00: mixed-lane carry with weak singleton `C5:EB23`; not boundary-defensible.
- C5:EC00/ED00/EE00: quiet mixed/local pages with zero xref ownership evidence.

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
- C5:E600..EFFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c5_e600_efff_seam_block.json`
- `reports/c5_e600_efff_seam_block.md`
- `reports/c5_e700_e7ff_backtrack.json`
- `reports/c5_e900_e9ff_backtrack.json`
- `reports/C5_E790_anchor.json`
- `reports/C5_E902_anchor.json`
- `reports/C5_E976_anchor.json`
- `reports/c5_e700_e7ff_flow.json` (manual-page extraction)
- `reports/c5_e900_e9ff_flow.json` (manual-page extraction)
- `reports/c5_ea00_eaff_flow.json` (reject-page support)
- `reports/c5_ef00_efff_flow.json` (reject-page support)

---

## New live seam: C5:F000..

Next unprocessed block starts at **C5:F000**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C5:F000 --pages 10 --json > reports/c5_f000_f9ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c5_f000_f9ff_seam_block.json --output reports/c5_f000_f9ff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_32.
