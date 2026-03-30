# Chrono Trigger Session 15 — Continuation Notes 34

## Block closed: C6:0400..C6:0DFF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C6:0400 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=3 on dense mixed target traffic |
| C6:0500 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=2 (`C6:0560`, `C6:05E4` invalid) |
| C6:0600 | candidate_code_lane | mixed_lane_continue | freeze | weak hits present but soft_bad=1 and no boundary ownership |
| C6:0700 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | hard_bad=4, strong_or_weak=0 (suspect/invalid-only lane) |
| C6:0800 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=12 + soft_bad=2 (page heavily poisoned) |
| C6:0900 | candidate_code_lane | local_control_only | freeze | suspect-only targets (`C6:0901`, `C6:0945`, `C6:09AF`) |
| C6:0A00 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | hard_bad=1 from invalid target `C6:0A1D` |
| C6:0B00 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=2 (`C6:0B10`, `C6:0B18` invalid) |
| C6:0C00 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=3 (invalids at `C6:0C05`, `C6:0C0B`, `C6:0CE2`) |
| C6:0D00 | branch_fed_control_pocket | local_control_only | freeze | suspect-only targets, no weak/strong ownership evidence |

---

## Manual-owner pages (anchor detail)

### C6:0300..03FF (boundary carry from this 10-page sweep)
Summary: raw_targets=4, xref_hits=4, strong_or_weak=3, hard_bad=0, soft_bad=0

Targets:
- C6:0301 (weak, caller C6:91D1)
- C6:0310 (weak, caller C6:E726)
- C6:0378 (suspect, caller C6:2F2F)
- C6:03EE (weak, caller C6:5BFC)

Backtrack scan (`reports/c6_0300_03ff_backtrack.json`):
- C6:036F->0378 score=6, start=0x20
- C6:030B->0310 score=4, start=0x18
- C6:03E8->03EE score=4, start=0x93
- C6:0301->0301 score=1, start=0xE7

Anchor reports:
- C6:0301: strong=0, weak=1, invalid=19
- C6:0310: strong=0, weak=1, invalid=34
- C6:0378: strong=0, weak=1, invalid=3
- C6:03EE: strong=0, weak=1, invalid=0

ROM-byte check:
- C6:0301 = `E7 27 A7 93 3F 93 3F 61 00 80 18 E0`
- C6:0310 = `F0 80 00 78 E0 18 D0 00 D0 00 BF 00`
- C6:0378 = `66 13 E8 12 3F 07 33 00 0F 98 CB 84`
- C6:03EE = `7F 00 0A 9F 60 43 11 3C C0 8E 00 70`

Verdict: all targets stay weak/suspect-only with heavy invalid-anchor noise; freeze.

---

## Reject/mixed lane notes

- C6:0400: rejected with hard_bad=3 (invalid starts include `C6:041E`, `C6:042F`, `C6:044C`).
- C6:0500: rejected with hard_bad=2 (`C6:0560`, `C6:05E4` invalid) despite two weak targets.
- C6:0700: mixed-command reject (`hard_bad=4`, no weak/strong effective starts).
- C6:0800: highest local contamination in block (`hard_bad=12`, `soft_bad=2`, 25 xref hits).
  - Invalid examples: `C6:0802`, `C6:0810`, `C6:0814`, `C6:0820`, `C6:0849`
- C6:0A00/0B00/0C00: all reject on explicit invalid targets:
  - C6:0A1D, C6:0B10, C6:0B18, C6:0C05, C6:0C0B, C6:0CE2
- C6:0600 remains mixed-lane carry (weak hits at `0603/060C/06A0` with soft_bad=1); C6:0900 and C6:0D00 remain suspect-only local-control pages.

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
- C6:0400..0DFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c6_0400_0dff_seam_block.json`
- `reports/c6_0400_0dff_seam_block.md`
- `reports/c6_0300_03ff_backtrack.json` (manual carry verification)
- `reports/C6_0301_anchor.json`
- `reports/C6_0310_anchor.json`
- `reports/C6_0378_anchor.json`
- `reports/C6_03EE_anchor.json`
- `reports/c6_0300_03ff_flow.json` (manual-page extraction)
- `reports/c6_0400_04ff_flow.json` (reject-page support)
- `reports/c6_0500_05ff_flow.json` (reject-page support)
- `reports/c6_0700_07ff_flow.json` (reject-page support)
- `reports/c6_0800_08ff_flow.json` (reject-page support)
- `reports/c6_0a00_0aff_flow.json` (reject-page support)
- `reports/c6_0b00_0bff_flow.json` (reject-page support)
- `reports/c6_0c00_0cff_flow.json` (reject-page support)

---

## New live seam: C6:0E00..

Next unprocessed block starts at **C6:0E00**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C6:0E00 --pages 10 --json > reports/c6_0e00_17ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c6_0e00_17ff_seam_block.json --output reports/c6_0e00_17ff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_35.
