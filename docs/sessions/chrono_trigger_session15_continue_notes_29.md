# Chrono Trigger Session 15 — Continuation Notes 29

## Block closed: C5:D200..C5:DBFF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C5:D200 | candidate_code_lane | manual_owner_boundary_review | freeze | weak/suspect-only targets (`C5:D21F`, `C5:D2E0`) with unresolved caller evidence |
| C5:D300 | candidate_code_lane | local_control_only | freeze | no targets, no xrefs |
| C5:D400 | candidate_code_lane | local_control_only | freeze | lone suspect target `C5:D456` only |
| C5:D500 | branch_fed_control_pocket | local_control_only | freeze | no targets, no xrefs |
| C5:D600 | branch_fed_control_pocket | local_control_only | freeze | no targets, no xrefs |
| C5:D700 | mixed_command_data | mixed_lane_continue | freeze | lone suspect target `C5:D716` in mixed-command lane |
| C5:D800 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | hard_bad=1 from invalid `C5:D870` |
| C5:D900 | mixed_command_data | mixed_lane_continue | freeze | two suspect-only targets (`C5:D905`, `C5:D982`) |
| C5:DA00 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | hard_bad=1 from invalid `C5:DA3F` |
| C5:DB00 | branch_fed_control_pocket | local_control_only | freeze | lone suspect target `C5:DB20`; no weak/strong support |

---

## Manual-owner pages (anchor detail)

### C5:D200..D2FF
Summary: raw_targets=2, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C5:D21F (suspect, callers C5:8929 and C5:8D91)
- C5:D2E0 (weak, caller C5:B861)

Backtrack scan (`reports/c5_d200_d2ff_backtrack.json`):
- C5:D20F->D21F score=4, start=0x7E
- C5:D2DC->D2E0 score=4, start=0xC2

Anchor reports:
- C5:D21F: strong=0, weak=2, invalid=2
- C5:D2E0: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:D21F = `F0 F0 D9 38 7E 11 00 5F F0 57 F8 F7`
- C5:D2E0 = `1E A2 00 00 04 03 03 18 1D 01 01 10`

Verdict: no strong anchors, and both backtrack starts land in data-like flow; manual review fails promotion.

---

## Reject/mixed lane notes

- C5:D800: rejected on hard_bad=1; invalid target `C5:D870` plus repetitive `20/F0` table-like patterns across weak/suspect hits.
  - C5:D870 = `FF 20 F0 20 F0 20 F0 20 F0 20 F0 20`
  - C5:D8D0 = `20 F0 20 F0 20 F0 FF 20 F0 20 F0 20`
  - C5:D8FF = `20 F0 20 F0 20 F0 20 F0 20 F0 FF 20`
- C5:DA00: rejected on hard_bad=1 from invalid `C5:DA3F` despite a suspect peer target (`C5:DA12`).
  - C5:DA12 = `F0 01 F0 01 F0 01 F0 01 F0 FF 01 F0`
  - C5:DA3F = `02 12 FD 11 F6 11 2F 20 02 72 80 FE`
- C5:D700 and C5:D900 remain mixed-lane carries: only suspect traffic (`C5:D716`, `C5:D905`, `C5:D982`) with zero promotable ownership evidence.
- C5:D300/C5:D500/C5:D600 are quiet local-control pages; C5:D400/C5:DB00 have suspect-only singletons (`C5:D456`, `C5:DB20`).

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
- C5:D200..DBFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c5_d200_dbff_seam_block.json`
- `reports/c5_d200_dbff_seam_block.md`
- `reports/c5_d200_d2ff_backtrack.json`
- `reports/C5_D21F_anchor.json`
- `reports/C5_D2E0_anchor.json`
- `reports/c5_d200_d2ff_flow.json` (manual-page extraction)
- `reports/c5_d800_d8ff_flow.json` (reject-page support)
- `reports/c5_d900_d9ff_flow.json` (mixed-page support)
- `reports/c5_da00_daff_flow.json` (reject-page support)

---

## New live seam: C5:DC00..

Next unprocessed block starts at **C5:DC00**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C5:DC00 --pages 10 --json > reports/c5_dc00_e5ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c5_dc00_e5ff_seam_block.json --output reports/c5_dc00_e5ff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_30.
