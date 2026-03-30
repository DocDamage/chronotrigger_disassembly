# Chrono Trigger Session 15 — Continuation Notes 21

## Block closed: C5:8100..C5:8AFF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C5:8100 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | only target is invalid (C5:8140) with hard_bad=1 |
| C5:8200 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=2; page contains invalid starts C5:8204/C5:8206 |
| C5:8300 | candidate_code_lane | local_control_only | freeze | lone suspect target C5:830F; no strong/weak caller support |
| C5:8400 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | two weak targets, both unresolved caller evidence only |
| C5:8500 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=2 with invalid C5:8500 and boundary-bait invalid C5:85FF |
| C5:8600 | mixed_command_data | mixed_lane_continue | freeze | single weak target in mixed-command lane; no boundary evidence |
| C5:8700 | mixed_command_data | manual_owner_boundary_review | freeze | lone weak target C5:8712 with unresolved caller only |
| C5:8800 | mixed_command_data | mixed_lane_continue | freeze | weak hits present but mixed-command page and no defensible entry start |
| C5:8900 | candidate_code_lane | local_control_only | freeze | zero targets, zero xrefs |
| C5:8A00 | branch_fed_control_pocket | local_control_only | freeze | zero targets, zero xrefs |

---

## Manual-owner pages (anchor detail)

### C5:8400..84FF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C5:8498 (weak, caller C5:F02E)
- C5:84CF (weak, caller C5:4683)

Backtrack scan (`reports/c5_8400_84ff_backtrack.json`):
- C5:8494->8498 score=4, start=0x0D
- C5:84CE->84CF score=4, start=0x4A

Anchor reports:
- C5:8498: strong=0, weak=1, invalid=1
- C5:84CF: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:8498 = `5C 12 13 03 50 40 60 40 10 00 F0 40`
- C5:84CF = `10 40 30 00 30 1C 1C 0E 0E 07 07 03`

Verdict: both candidates remain weak-only with non-prologue starts in a branch-fed pocket; freeze.

### C5:8700..87FF
Summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0

Target:
- C5:8712 (weak, caller C5:CFB6)

Backtrack scan (`reports/c5_8700_87ff_backtrack.json`):
- C5:870D->8712 score=4, start=0x08

Anchor report:
- C5:8712: strong=0, weak=1, invalid=1

ROM-byte check:
- C5:8712 = `69 02 00 B9 B0 0F 20 DB B0 7C 10 00`

Verdict: caller quality stays unresolved; target body remains mixed/data-like and non-promotable.

---

## Reject lanes and mixed-lane carry pages

- C5:8100, C5:8200, C5:8500 were auto-rejected on hard_bad evidence (invalid starts and/or boundary-bait invalid target).
- C5:8600 and C5:8800 remain mixed-command lanes with weak traffic only; no callable boundary established.
- C5:8900 and C5:8A00 are silent local-control pages (no targets/xrefs).

---

## Running promotion count

- C5:3B00..44FF: 0 promotions (notes_14)
- C5:4500..4EFF: 0 promotions (notes_15)
- C5:4F00..58FF: 0 promotions (notes_16)
- C5:5900..62FF: 0 promotions (notes_17)
- C5:6300..6CFF: 0 promotions (notes_18)
- C5:6D00..76FF: 0 promotions (notes_19)
- C5:7700..80FF: 0 promotions (notes_20)
- C5:8100..8AFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c5_8100_8aff_seam_block.json`
- `reports/c5_8100_8aff_seam_block.md`
- `reports/c5_8400_84ff_backtrack.json`
- `reports/c5_8700_87ff_backtrack.json`
- `reports/C5_8498_anchor.json`
- `reports/C5_84CF_anchor.json`
- `reports/C5_8712_anchor.json`

---

## New live seam: C5:8B00..

Next unprocessed block starts at **C5:8B00**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C5:8B00 --pages 10 --json > reports/c5_8b00_94ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c5_8b00_94ff_seam_block.json --output reports/c5_8b00_94ff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_22.
