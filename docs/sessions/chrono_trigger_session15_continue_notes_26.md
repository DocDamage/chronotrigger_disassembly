# Chrono Trigger Session 15 — Continuation Notes 26

## Block closed: C5:B400..C5:BDFF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C5:B400 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=1 from invalid target `C5:B463` |
| C5:B500 | candidate_code_lane | local_control_only | freeze | no targets, no xrefs |
| C5:B600 | candidate_code_lane | local_control_only | freeze | no targets, no xrefs |
| C5:B700 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | two weak-only targets (`C5:B707`, `C5:B740`) with unresolved callers |
| C5:B800 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | hard_bad=4 (invalid targets `C5:B800`, `C5:B847`, `C5:B8B1`) |
| C5:B900 | mixed_command_data | mixed_lane_continue | freeze | single weak target (`C5:B900`) but mixed-command lane, no defensible boundary |
| C5:BA00 | candidate_code_lane | local_control_only | freeze | no targets, no xrefs |
| C5:BB00 | candidate_code_lane | local_control_only | freeze | no targets, no xrefs |
| C5:BC00 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | weak-only targets (`C5:BC04`, `C5:BC08`) with unresolved callers |
| C5:BD00 | candidate_code_lane | mixed_lane_continue | freeze | lone weak target `C5:BD49`; no caller-backed promotion evidence |

---

## Manual-owner pages (anchor detail)

### C5:B700..B7FF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C5:B707 (weak, caller D6:C2C8)
- C5:B740 (weak, caller C5:04A9)

Backtrack scan (`reports/c5_b700_b7ff_backtrack.json`):
- C5:B73F->B740 score=6, start=0x20
- C5:B703->B707 score=2, start=0xCC

Anchor reports:
- C5:B707: strong=0, weak=1, invalid=1
- C5:B740: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:B707 = `FC 6E 84 00 F4 01 F0 7E 18 37 80 F0`
- C5:B740 = `CF F3 F5 06 90 01 3C 18 70 26 56 02`

Verdict: both starts remain weak-only with unresolved callers; high backtrack score at C5:B73F still lands in non-prologue data-like flow.

### C5:BC00..BCFF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C5:BC04 (weak, caller C5:0891)
- C5:BC08 (weak, caller C5:6EFD)

Backtrack scan (`reports/c5_bc00_bcff_backtrack.json`):
- C5:BC03->BC08 score=4, start=0x25
- C5:BC04->BC04 score=3, start=0x3E

Anchor reports:
- C5:BC04: strong=0, weak=1, invalid=1
- C5:BC08: strong=0, weak=1, invalid=1

ROM-byte check:
- C5:BC04 = `3E 13 11 B0 1D 02 B9 15 40 10 0C 40`
- C5:BC08 = `1D 02 B9 15 40 10 0C 40 28 D5 24 56`

Verdict: both anchors stay weak-only and backtrack starts (`0x25`, `0x3E`) are non-prologue; freeze.

---

## Reject/mixed lane notes

- C5:B400: rejected on hard_bad=1 (`C5:B463` invalid). Byte checks:
  - C5:B400 = `05 5E 11 FF CE FF 08 CF 70 00 FF 00`
  - C5:B463 = `40 C0 7C 3B 4C 27 57 00 20 01 1A 50`
- C5:B800: rejected on hard_bad=4 with invalid concentration (`C5:B800`, `C5:B847`, `C5:B8B1`). Byte checks:
  - C5:B800 = `40 99 40 AD 40 20 10 20 A0 40 91 08`
  - C5:B847 = `02 10 B3 30 40 00 00 04 69 00 40 04`
  - C5:B8B1 = `FF 10 FF 00 51 02 00 0F 00 08 02 00`
- C5:B900 and C5:BD00: mixed-lane carry pages with lone weak targets only (`C5:B900`, `C5:BD49`), not boundary-defensible.
- C5:B500/C5:B600/C5:BA00/C5:BB00: quiet local-control pages (zero targets/xrefs).

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
- C5:B400..BDFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c5_b400_bdff_seam_block.json`
- `reports/c5_b400_bdff_seam_block.md`
- `reports/c5_b700_b7ff_backtrack.json`
- `reports/c5_bc00_bcff_backtrack.json`
- `reports/C5_B707_anchor.json`
- `reports/C5_B740_anchor.json`
- `reports/C5_BC04_anchor.json`
- `reports/C5_BC08_anchor.json`
- `reports/c5_b700_b7ff_flow.json` (supporting extraction)
- `reports/c5_bc00_bcff_flow.json` (supporting extraction)

---

## New live seam: C5:BE00..

Next unprocessed block starts at **C5:BE00**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C5:BE00 --pages 10 --json > reports/c5_be00_c7ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c5_be00_c7ff_seam_block.json --output reports/c5_be00_c7ff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_27.
