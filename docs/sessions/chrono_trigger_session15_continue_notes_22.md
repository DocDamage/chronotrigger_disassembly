# Chrono Trigger Session 15 — Continuation Notes 22

## Block closed: C5:8B00..C5:94FF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C5:8B00 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | hard_bad=2 with invalid targets C5:8BBB/C5:8BC0 |
| C5:8C00 | branch_fed_control_pocket | mixed_lane_continue | freeze | no targets, no xrefs |
| C5:8D00 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | lone weak target C5:8D10 remains unresolved and non-prologue |
| C5:8E00 | branch_fed_control_pocket | mixed_lane_continue | freeze | single weak target C5:8E14 with backtrack score 0 |
| C5:8F00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | hard_bad + soft_bad + invalid target C5:8FEB |
| C5:9000 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | high weak traffic but hard_bad=1 keeps page poisoned |
| C5:9100 | candidate_code_lane | mixed_lane_continue | freeze | lone weak target C5:9113 only, no owner-boundary support |
| C5:9200 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | invalid C5:9275 plus suspect-only alternates |
| C5:9300 | candidate_code_lane | mixed_lane_continue | freeze | single weak target C5:93A0 with low backtrack confidence |
| C5:9400 | branch_fed_control_pocket | mixed_lane_continue | freeze | lone suspect target C5:9424 and soft_bad start class |

---

## Manual-owner page detail

### C5:8D00..8DFF
Summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0

Target:
- C5:8D10 (weak, hits=1, caller C5:0BD0)

Backtrack scan (`reports/c5_8d00_8dff_backtrack.json`):
- C5:8D0C->8D10 score=4, start=0xDF

Anchor report (`reports/C5_8D10_anchor.json`):
- strong=0, weak=1, invalid=4
- valid caller remains unresolved; all other hits are bank-mismatch noise

ROM-byte check:
- C5:8D10 = `C1 A7 00 60 FA 08 73 88 61 88 F3 00`

Verdict: weak-only unresolved caller and non-defensible entry bytes; freeze.

---

## Notable reject-lane evidence

- C5:8B00: branch-fed pocket with score floor hits (down to -6) and two invalid targets.
- C5:8F00: mixed-command page with both hard_bad and soft_bad start classes active.
- C5:9000: 7 weak hits but still auto-rejected because hard_bad contamination is present; high hit count did not improve owner confidence.
- C5:9200: invalid C5:9275 and only suspect alternates (C5:9264/C5:92D6).

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
- C5:8B00..94FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c5_8b00_94ff_seam_block.json`
- `reports/c5_8b00_94ff_seam_block.md`
- `reports/c5_8d00_8dff_backtrack.json`
- `reports/C5_8D10_anchor.json`

---

## New live seam: C5:9500..

Next unprocessed block starts at **C5:9500**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C5:9500 --pages 10 --json > reports/c5_9500_9eff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c5_9500_9eff_seam_block.json --output reports/c5_9500_9eff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_23.
