# Chrono Trigger Session 15 — Continuation Notes 32

## Block closed: C5:F000..C5:F9FF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C5:F000 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=5 on a high-noise page (`raw=14`, `xref=18`) |
| C5:F100 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | weak/suspect-only pair (`C5:F1A0`, `C5:F140`) with unresolved callers |
| C5:F200 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | hard_bad=1 from invalid target `C5:F2FA` |
| C5:F300 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | hard_bad=3 with invalid zero-start targets (`C5:F380`, `C5:F3A0`, `C5:F3CF`) |
| C5:F400 | dead_zero_field | dead_lane_reject | freeze | dead zero field, hard_bad=2 (`C5:F400`, `C5:F409` invalid) |
| C5:F500 | dead_zero_field | dead_lane_reject | freeze | dead zero field (no targets/xrefs, non-executable dead lane) |
| C5:F600 | dead_zero_field | dead_lane_reject | freeze | dead zero field, hard_bad=2 (`C5:F609`, `C5:F6E3` invalid) |
| C5:F700 | dead_zero_field | dead_lane_reject | freeze | dead zero field, hard_bad=2 (`C5:F700`, `C5:F748` invalid) |
| C5:F800 | dead_zero_field | dead_lane_reject | freeze | dead zero field, hard_bad=6 (multiple invalid starts including `C5:F810`) |
| C5:F900 | dead_zero_field | dead_lane_reject | freeze | dead zero field, hard_bad=3 (`C5:F920`, `C5:F986`, `C5:F9CE` invalid) |

---

## Manual-owner pages (anchor detail)

### C5:F100..F1FF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C5:F140 (suspect, caller C5:B32E)
- C5:F1A0 (weak, caller C5:E026)

Backtrack scan (`reports/c5_f100_f1ff_backtrack.json`):
- C5:F13F->F140 score=4, start=0x22
- C5:F1A0->F1A0 score=1, start=0x21

Anchor reports:
- C5:F140: strong=0, weak=1, invalid=3
- C5:F1A0: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:F140 = `50 30 06 22 B4 14 56 55 73 7F 13 7B`
- C5:F1A0 = `21 00 2F 40 DA 01 9A 02 90 80 00 A2`

Verdict: weak/suspect-only ownership and non-prologue starts keep this page frozen.

---

## Reject/dead-lane notes

- C5:F000: rejected on heavy hard_bad contamination (invalid starts include `C5:F001`, `C5:F00C`, `C5:F0F0`), despite multiple weak hits.
  - C5:F000 = `13 03 2B 04 3F 37 B6 00 00 0F 01 0F`
  - C5:F001 = `03 2B 04 3F 37 B6 00 00 0F 01 0F 02`
  - C5:F0F0 = `00 08 42 00 81 59 50 22 F7 82 E3 10`
- C5:F200: rejected on invalid boundary-adjacent target `C5:F2FA` in repetitive `F0/01` control pattern.
- C5:F300: mixed-command reject with three invalid zero starts (`C5:F380`, `C5:F3A0`, `C5:F3CF`).
- C5:F400..F9FF: classified as `dead_zero_field`/`dead_lane_reject`; bytes are overwhelmingly zeroed and non-promotable.
  - C5:F400 = `00 00 00 00 00 00 00 00 00 00 00 00`
  - C5:F609 = `00 00 00 00 00 00 00 00 00 00 00 00`
  - C5:F810 = `00 00 00 00 00 00 00 00 00 00 00 00`
  - C5:F920 = `00 00 00 00 00 00 00 00 00 00 00 00`

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
- C5:F000..F9FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c5_f000_f9ff_seam_block.json`
- `reports/c5_f000_f9ff_seam_block.md`
- `reports/c5_f100_f1ff_backtrack.json`
- `reports/C5_F140_anchor.json`
- `reports/C5_F1A0_anchor.json`
- `reports/c5_f100_f1ff_flow.json` (manual-page extraction)
- `reports/c5_f000_f0ff_flow.json` (reject-page support)
- `reports/c5_f200_f2ff_flow.json` (reject-page support)
- `reports/c5_f300_f3ff_flow.json` (reject-page support)

---

## New live seam: C5:FA00..

Next unprocessed block starts at **C5:FA00** (crosses into bank C6 within 10 pages).

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C5:FA00 --pages 10 --json > reports/c5_fa00_c6_03ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c5_fa00_c6_03ff_seam_block.json --output reports/c5_fa00_c6_03ff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_33.
