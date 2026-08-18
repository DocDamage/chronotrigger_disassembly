# Chrono Trigger Session 15 — Continuation Notes 24

## Block closed: C5:A000..C5:A9FF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C5:A000 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=3 despite multiple weak hits; page poisoned |
| C5:A100 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | invalid target C5:A100 (hard_bad=1) dominates page |
| C5:A200 | candidate_code_lane | local_control_only | freeze | no targets, no xrefs |
| C5:A300 | mixed_command_data | local_control_only | freeze | no targets, no xrefs |
| C5:A400 | branch_fed_control_pocket | local_control_only | freeze | no targets, no xrefs |
| C5:A500 | mixed_command_data | local_control_only | freeze | no targets, no xrefs |
| C5:A600 | branch_fed_control_pocket | local_control_only | freeze | no targets, no xrefs |
| C5:A700 | candidate_code_lane | local_control_only | freeze | no targets, no xrefs |
| C5:A800 | branch_fed_control_pocket | bad_start_or_dead_lane_reject | freeze | weak C5:A8E0 present, but invalid C5:A820 forces reject |
| C5:A900 | candidate_code_lane | local_control_only | freeze | no targets, no xrefs |

---

## Block observations

1. This 10-page sweep produced **no** `manual_owner_boundary_review` pages.
2. No owner/backtrack deep-dive runs were required beyond seam-block output.
3. Rejections were concentrated in three pages with hard_bad contamination:
   - C5:A000 (`hard_bad=3`, raw_targets=12, xref_hits=16)
   - C5:A100 (`hard_bad=1`, includes invalid target C5:A100)
   - C5:A800 (`hard_bad=1`, includes invalid target C5:A820)
4. The remaining seven pages are quiet local-control territory with zero caller-backed ownership evidence.

---

## Byte-level sanity checks (reject pages)

- C5:A010 = `7E 06 0B 7C 27 02 46 25 C5 40 01 20`
- C5:A050 = `F0 60 48 B0 60 9C F0 F8 40 48 3C 07`
- C5:A0E0 = `D0 20 50 80 B0 F8 90 F0 60 8C 02 82`
- C5:A100 = `00 C5 02 BE 26 05 7E 21 42 18 C0 15` (invalid start)
- C5:A110 = `07 BF 02 CC 05 BE 24 BE 16 C2 37 01`
- C5:A820 = `00 FF 48 0D 50 1F 1F 1F 3B 3F 80 73` (invalid start)
- C5:A8E0 = `DC 00 C4 74 48 1A 98 94 0A 1C 7C 48`

These bytes are consistent with the page-level hard_bad decisions.

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
- C5:A000..A9FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c5_a000_a9ff_seam_block.json`
- `reports/c5_a000_a9ff_seam_block.md`

---

## New live seam: C5:AA00..

Next unprocessed block starts at **C5:AA00**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C5:AA00 --pages 10 --json > reports/c5_aa00_b3ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c5_aa00_b3ff_seam_block.json --output reports/c5_aa00_b3ff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_25.
