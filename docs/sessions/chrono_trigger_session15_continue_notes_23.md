# Chrono Trigger Session 15 — Continuation Notes 23

## Block closed: C5:9500..C5:9EFF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C5:9500 | branch_fed_control_pocket | mixed_lane_continue | freeze | no targets, no xrefs |
| C5:9600 | candidate_code_lane | manual_owner_boundary_review | freeze | two weak-only targets (`C5:96F2`, `C5:96F7`) with unresolved callers |
| C5:9700 | candidate_code_lane | local_control_only | freeze | no targets, no xrefs |
| C5:9800 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | hard_bad=2 (invalid `C5:9863` and `C5:9897`) |
| C5:9900 | candidate_code_lane | local_control_only | freeze | lone suspect target `C5:99DB` only |
| C5:9A00 | branch_fed_control_pocket | mixed_lane_continue | freeze | single weak target `C5:9A5F` with backtrack score 0 |
| C5:9B00 | branch_fed_control_pocket | local_control_only | freeze | no targets, no xrefs |
| C5:9C00 | candidate_code_lane | manual_owner_boundary_review | freeze | weak-only targets; score-6 near-miss still fails entry-byte quality |
| C5:9D00 | candidate_code_lane | local_control_only | freeze | no targets, no xrefs |
| C5:9E00 | candidate_code_lane | local_control_only | freeze | no targets, no xrefs |

---

## Manual-owner pages (anchor detail)

### C5:9600..96FF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C5:96F2 (weak, caller C5:51B1)
- C5:96F7 (weak, caller C5:5373)

Backtrack scan (`reports/c5_9600_96ff_backtrack.json`):
- C5:96EF->96F2 score=4, start=0x8B
- C5:96EF->96F7 score=4, start=0x8B

Anchor reports:
- C5:96F2: strong=0, weak=1, invalid=0
- C5:96F7: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:96F2 = `7E 10 1F F8 1E F9 00 11 B8 86 90 00`
- C5:96F7 = `F9 00 11 B8 86 90 00 C7 30 0E 30 8F`

Verdict: both starts are arithmetic/rotate flow in data-like context, not defensible function entries.

### C5:9C00..9CFF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C5:9C00 (weak, caller C5:2D7E)
- C5:9C34 (weak, caller C5:1ED9)

Backtrack scan (`reports/c5_9c00_9cff_backtrack.json`):
- C5:9C25->9C34 score=6, start=0x4B (PHK)
- C5:9C00->9C00 score=1, start=0x11

Anchor reports:
- C5:9C00: strong=0, weak=1, invalid=10
- C5:9C34: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:9C00 = `11 06 0B 04 0F 06 07 0F 00 07 02 09`
- C5:9C34 = `0F 05 17 00 0A 09 02 03 06 06 03 07`

Key trap: score-6 alignment at C5:9C34 comes from a plausible predecessor start (PHK), but the target byte itself is `0x0F` (`ORA long`) and the body remains table-like.

Verdict: weak-only unresolved callers and non-prologue target bytes; freeze.

---

## Reject/mixed lane notes

- C5:9800: rejected immediately on hard_bad contamination (2 invalid targets).
- C5:9A00: weak caller exists at C5:9A5F but backtrack score is 0 and page remains branch-fed.
- C5:9900/9B00/9D00/9E00: no promotable ownership evidence (local-control pages).

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
- C5:9500..9EFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c5_9500_9eff_seam_block.json`
- `reports/c5_9500_9eff_seam_block.md`
- `reports/c5_9600_96ff_backtrack.json`
- `reports/c5_9c00_9cff_backtrack.json`
- `reports/C5_96F2_anchor.json`
- `reports/C5_96F7_anchor.json`
- `reports/C5_9C00_anchor.json`
- `reports/C5_9C34_anchor.json`

---

## New live seam: C5:A000..

Next unprocessed block starts at **C5:A000**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C5:A000 --pages 10 --json > reports/c5_a000_a9ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c5_a000_a9ff_seam_block.json --output reports/c5_a000_a9ff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_24.
