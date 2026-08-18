# Chrono Trigger Session 15 — Continuation Notes 28

## Block closed: C5:C800..C5:D1FF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C5:C800 | candidate_code_lane | local_control_only | freeze | no targets, no xrefs |
| C5:C900 | candidate_code_lane | local_control_only | freeze | lone suspect boundary-bait target `C5:C9FF` only |
| C5:CA00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | hard_bad=2 from invalid targets `C5:CA23` and `C5:CAF3` |
| C5:CB00 | candidate_code_lane | manual_owner_boundary_review | freeze | two weak-only targets (`C5:CB02`, `C5:CB2F`) with unresolved callers |
| C5:CC00 | candidate_code_lane | mixed_lane_continue | freeze | lone weak target `C5:CCC0`; no boundary-backed ownership |
| C5:CD00 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | single weak target `C5:CD33` still unresolved |
| C5:CE00 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | hard_bad=1 from invalid target `C5:CEDF` |
| C5:CF00 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=1 from invalid start at `C5:CF00` |
| C5:D000 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | hard_bad=1 from invalid target `C5:D0DC` |
| C5:D100 | candidate_code_lane | mixed_lane_continue | freeze | weak `C5:D100` + suspect `C5:D1C0`; no promotable boundary |

---

## Manual-owner pages (anchor detail)

### C5:CB00..CBFF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C5:CB02 (weak, caller C5:0531)
- C5:CB2F (weak, caller C5:6FDC)

Backtrack scan (`reports/c5_cb00_cbff_backtrack.json`):
- C5:CB2B->CB2F score=4, start=0x39
- C5:CB00->CB02 score=2, start=0xE0

Anchor reports:
- C5:CB02: strong=0, weak=1, invalid=0
- C5:CB2F: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:CB02 = `70 8F F1 00 0E F0 0F F1 0E FF 03 E7`
- C5:CB2F = `BF 00 EF 00 A0 F7 F1 FE 60 FF 20 FF`

Verdict: both anchors remain weak-only and target bytes look table/control-like, not callable entry prologues.

### C5:CD00..CDFF
Summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0

Target:
- C5:CD33 (weak, caller C5:758B)

Backtrack scan (`reports/c5_cd00_cdff_backtrack.json`):
- C5:CD33->CD33 score=5, start=0xA0

Anchor report:
- C5:CD33: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:CD33 = `A0 40 D0 30 18 E0 00 01 03 04 0F 10`

Verdict: lone unresolved weak anchor and non-prologue start byte keep page frozen.

---

## Reject/mixed lane notes

- C5:CA00: rejected immediately on hard_bad=2 (invalid starts at `C5:CA23`, `C5:CAF3`).
  - C5:CA23 = `FF 00 B7 53 00 F9 18 DF 69 FF 0C FF`
  - C5:CAF3 = `00 E0 FF F0 FF 01 1F E0 2F 00 C0 46`
- C5:CE00: hard_bad=1 from invalid `C5:CEDF` despite one weak hit at `C5:CEBF`.
- C5:CF00: hard_bad=1 from invalid self-start `C5:CF00` with weak `C5:CF2E` nearby.
- C5:D000: hard_bad=1 from invalid `C5:D0DC`; weak `C5:D000` does not override reject posture.
- C5:CC00 and C5:D100 remain mixed-lane carry pages with weak/suspect targets only (`C5:CCC0`, `C5:D100`, `C5:D1C0`).

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
- C5:C800..D1FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c5_c800_d1ff_seam_block.json`
- `reports/c5_c800_d1ff_seam_block.md`
- `reports/c5_cb00_cbff_backtrack.json`
- `reports/c5_cd00_cdff_backtrack.json`
- `reports/C5_CB02_anchor.json`
- `reports/C5_CB2F_anchor.json`
- `reports/C5_CD33_anchor.json`
- `reports/c5_cb00_cbff_flow.json` (supporting extraction)
- `reports/c5_cd00_cdff_flow.json` (supporting extraction)

---

## New live seam: C5:D200..

Next unprocessed block starts at **C5:D200**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C5:D200 --pages 10 --json > reports/c5_d200_dbff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c5_d200_dbff_seam_block.json --output reports/c5_d200_dbff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_29.
