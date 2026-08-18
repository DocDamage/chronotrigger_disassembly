# Chrono Trigger Session 15 — Continuation Notes 25

## Block closed: C5:AA00..C5:B3FF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C5:AA00 | candidate_code_lane | manual_owner_boundary_review | freeze | weak+suspect-only targets (`C5:AA20`, `C5:AAFC`) with unresolved callers |
| C5:AB00 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=1 from invalid target `C5:AB56` |
| C5:AC00 | branch_fed_control_pocket | local_control_only | freeze | no targets, no xrefs |
| C5:AD00 | branch_fed_control_pocket | local_control_only | freeze | no targets, no xrefs |
| C5:AE00 | mixed_command_data | mixed_lane_continue | freeze | mixed-command page with no ownership evidence |
| C5:AF00 | candidate_code_lane | local_control_only | freeze | no targets, no xrefs |
| C5:B000 | candidate_code_lane | manual_owner_boundary_review | freeze | dense weak-only target mesh (8 targets / 9 hits), all unresolved callers |
| C5:B100 | branch_fed_control_pocket | mixed_lane_continue | freeze | lone weak target `C5:B1B6` only; no caller-backed boundary |
| C5:B200 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | one weak + two suspect targets, no promotable entry signature |
| C5:B300 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | hard_bad=1 from invalid target `C5:B367` |

---

## Manual-owner pages (anchor detail)

### C5:AA00..AAFF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C5:AA20 (weak, caller C5:DD4C)
- C5:AAFC (suspect, caller C5:4A78)

Backtrack scan (`reports/c5_aa00_aaff_backtrack.json`):
- C5:AA1C->AA20 score=4, start=0x1C
- C5:AAF9->AAFC score=2, start=0x2A

Anchor reports:
- C5:AA20: strong=0, weak=1, invalid=5
- C5:AAFC: strong=0, weak=1, invalid=1

ROM-byte check:
- C5:AA20 = `0F 0E 05 B0 01 0B 01 05 44 02 FE 15`
- C5:AAFC = `0E E0 FC 24 80 C0 3F 07 11 10 0B 14`

Verdict: both candidate starts remain weak/suspect only and land in arithmetic/data-like byte flow, so freeze.

### C5:B000..B0FF
Summary: raw_targets=8, xref_hits=9, strong_or_weak=8, hard_bad=0, soft_bad=0

Targets:
- C5:B00F (weak, caller C5:8116)
- C5:B03E (weak, caller C5:CEBA)
- C5:B040 (weak, caller C5:7D49)
- C5:B04F (weak, caller C5:3112)
- C5:B098 (weak, callers C5:A2D0, C5:B0A8)
- C5:B0B4 (weak, caller C5:8FA1)
- C5:B0C0 (weak, caller C5:2A69)
- C5:B0DB (suspect, caller C5:8718)

Backtrack scan (`reports/c5_b000_b0ff_backtrack.json`):
- C5:B03F->B040 score=6, start=0x20
- C5:B03F->B04F score=6, start=0x20
- C5:B097->B098 score=6, start=0xC2
- C5:B0D5->B0DB score=6, start=0xA0
- C5:B00D->B00F score=4, start=0xA0
- C5:B02E->B03E score=4, start=0x06
- C5:B0B3->B0B4 score=2, start=0xC2
- C5:B0C0->B0C0 score=1, start=0xBF

Anchor reports:
- C5:B00F: strong=0, weak=1, invalid=0
- C5:B03E: strong=0, weak=1, invalid=0
- C5:B040: strong=0, weak=1, invalid=6
- C5:B04F: strong=0, weak=1, invalid=1
- C5:B098: strong=0, weak=2, invalid=0
- C5:B0B4: strong=0, weak=1, invalid=1
- C5:B0C0: strong=0, weak=1, invalid=4
- C5:B0DB: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:B00F = `3A C0 0C 08 C0 F3 C0 F3 C0 F3 C0 83`
- C5:B03E = `C8 20 E0 80 30 B0 E0 F0 20 90 60 3F`
- C5:B040 = `E0 80 30 B0 E0 F0 20 90 60 3F 1C 57`
- C5:B04F = `18 08 19 40 A4 1E 04 F8 01 06 00 07`
- C5:B098 = `0B 07 74 11 FE 36 82 32 C8 70 C4 78`
- C5:B0B4 = `18 F0 8A 0F 00 FF 00 FF 00 FF 1F 00`
- C5:B0C0 = `BF C0 FC C0 FC C0 FC C0 7C 0A 0B 05`
- C5:B0DB = `B6 1C 02 3A 0E 8A 1A C6 0B 30 40 06`

Verdict: despite several score-6 backtracks, anchors stay weak-only/unresolved and byte patterns remain table-like or mixed-control; freeze.

### C5:B200..B2FF
Summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C5:B26A (weak, caller C5:6E1E)
- C5:B23F (suspect, caller C5:9920)
- C5:B2E8 (suspect, caller C5:D54F)

Backtrack scan (`reports/c5_b200_b2ff_backtrack.json`):
- C5:B23F->B23F score=5, start=0x0B
- C5:B2E7->B2E8 score=4, start=0x04
- C5:B266->B26A score=2, start=0x69

Anchor reports:
- C5:B23F: strong=0, weak=1, invalid=1
- C5:B26A: strong=0, weak=1, invalid=0
- C5:B2E8: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:B23F = `0B 17 13 63 01 40 10 7F 69 7F 60 2F`
- C5:B26A = `1D 3F 0D 01 80 90 01 03 04 0C 10 30`
- C5:B2E8 = `FC 1F E8 3F D1 00 3F F3 DF 37 EF 97`

Verdict: weak/suspect-only caller evidence and non-prologue starts (`0x0B`, `0x1D`, `0xFC`) keep this page frozen.

---

## Reject/mixed lane notes

- C5:AB00: rejected on hard_bad=1 (`C5:AB56` invalid). Byte sample: `60 A0 C6 00 C0 00 FE 21 C4 30 C8 3F`.
- C5:B300: rejected on hard_bad=1 (`C5:B367` invalid) even with two weak hits. Byte sample: `00 FF 6A FF 3F 6A 0F 3A 03 82 0E 1D`.
- C5:B100: mixed-lane carry only; lone weak target `C5:B1B6` (`0F FE 0E F4 3C 86 80 DA 92 B0 1E DA`) is not boundary-defensible.
- C5:AC00/C5:AD00/C5:AF00: quiet local-control pages with zero targets/xrefs.

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
- C5:AA00..B3FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c5_aa00_b3ff_seam_block.json`
- `reports/c5_aa00_b3ff_seam_block.md`
- `reports/c5_aa00_aaff_backtrack.json`
- `reports/c5_b000_b0ff_backtrack.json`
- `reports/c5_b200_b2ff_backtrack.json`
- `reports/C5_AA20_anchor.json`
- `reports/C5_AAFC_anchor.json`
- `reports/C5_B00F_anchor.json`
- `reports/C5_B03E_anchor.json`
- `reports/C5_B040_anchor.json`
- `reports/C5_B04F_anchor.json`
- `reports/C5_B098_anchor.json`
- `reports/C5_B0B4_anchor.json`
- `reports/C5_B0C0_anchor.json`
- `reports/C5_B0DB_anchor.json`
- `reports/C5_B23F_anchor.json`
- `reports/C5_B26A_anchor.json`
- `reports/C5_B2E8_anchor.json`
- `reports/c5_aa00_aaff_flow.json` (supporting extraction)
- `reports/c5_b000_b0ff_flow.json` (supporting extraction)
- `reports/c5_b200_b2ff_flow.json` (supporting extraction)

---

## New live seam: C5:B400..

Next unprocessed block starts at **C5:B400**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C5:B400 --pages 10 --json > reports/c5_b400_bdff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c5_b400_bdff_seam_block.json --output reports/c5_b400_bdff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_26.
