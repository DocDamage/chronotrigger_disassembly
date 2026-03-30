# Chrono Trigger Session 15 — Continuation Notes 19

## Block closed: C5:6D00..C5:76FF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C5:6D00 | candidate_code_lane | local_control_only | freeze | no xref hits; local clusters only |
| C5:6E00 | mixed_command_data | local_control_only | freeze | no targets, no xrefs |
| C5:6F00 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad + soft_bad + boundary_bait targets at C5:6FFE/C5:6FFF |
| C5:7000 | mixed_command_data | manual_owner_boundary_review | freeze | 11 raw targets but all caller evidence remains weak/unresolved |
| C5:7100 | candidate_code_lane | manual_owner_boundary_review | freeze | one weak + three suspect targets; starts are non-prologue bytes |
| C5:7200 | candidate_code_lane | manual_owner_boundary_review | freeze | score-6 near-miss at C5:7297 fails at target byte quality |
| C5:7300 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | hard_bad target C5:7397=0x00 (invalid) |
| C5:7400 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad target C5:747F=0x00 and no weak/strong carry through |
| C5:7500 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | hard_bad target C5:7506=0x00 poisons page |
| C5:7600 | candidate_code_lane | local_control_only | freeze | lone suspect target C5:76DE with no weak/strong caller support |

---

## Manual-owner pages (anchor detail)

### C5:7000..70FF
Summary: raw_targets=11, xref_hits=11, strong_or_weak=6, soft_bad=1, clusters=2

Best targets:
- C5:7000 (weak, hits=1, caller C5:A2A1)
- C5:7001 (weak, hits=1, caller C5:52F0)
- C5:7041 (weak, hits=1, caller C5:9038)
- C5:7080 (weak, hits=1, caller C5:3DCC)
- C5:70AA (weak, hits=1, caller C5:A5DD)

Backtrack scan (`reports/c5_7000_70ff_backtrack.json`):
- best structural candidates are C5:70D6->70E1 (score=4, start=0xBB) and C5:70EE->70F4 (score=4, start=0x07)
- target C5:7000 starts at 0x07, C5:7001 starts at 0x9D

Anchor reports:
- C5:7000: strong=0, weak=1, invalid=40
- C5:7001: strong=0, weak=1, invalid=8
- C5:7041: strong=0, weak=1, invalid=1
- C5:7080: strong=0, weak=1, invalid=15
- C5:70AA: strong=0, weak=1, invalid=0

ROM-byte check (first 12 bytes):
- C5:7000 = `07 9D 91 96 CE 6D DE 00 2E BE E1 FD`
- C5:7080 = `F8 86 F9 A7 D8 00 96 E9 4A F5 9C 63`
- C5:70AA = `54 FC 00 84 F8 BC F2 FE FE FE F9 01`

Page remains mixed-command; no defensible callable entry.

### C5:7100..71FF
Summary: raw_targets=4, xref_hits=4, strong_or_weak=1, hard_bad=0, soft_bad=0

Best targets:
- C5:71BC (weak, caller C5:0F67)
- C5:7117 (suspect, caller C5:CDC6)
- C5:7142 (suspect, caller C5:68E8)
- C5:71D0 (suspect, caller C5:AD0A)

Backtrack scan (`reports/c5_7100_71ff_backtrack.json`):
- C5:7114->7117 score=4, start=0xDA
- C5:7140->7142 score=4, start=0x1E
- C5:71BC->71BC score=3, start=0x14

Anchor reports (all unresolved):
- C5:71BC: strong=0, weak=1, invalid=1
- C5:7117: strong=0, weak=1, invalid=1
- C5:7142: strong=0, weak=1, invalid=0
- C5:71D0: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:71BC = `14 6B 14 00 75 A1 0F 91 E8 C8 EF DB`
- C5:7117 = `31 1B 63 2B 73 31 FB 78 73 FD FB C6`
- C5:7142 = `3F C0 35 CA 33 05 AB 0B E0 CC 22 DD`
- C5:71D0 = `5B 00 DE 08 FE 08 3F 18 7D 64 10 FF`

No start byte in this page is a defensible prologue for promotion.

### C5:7200..72FF
Summary: raw_targets=6, xref_hits=7, strong_or_weak=5, soft_bad=1, clusters=2

Best targets:
- C5:7202 (weak, hits=2; callers C5:DA46 and C5:DE60)
- C5:7216 (weak, hits=1)
- C5:726F (weak, hits=1)
- C5:728D (weak, hits=1)
- C5:7297 (suspect, hits=1)

Backtrack scan (`reports/c5_7200_72ff_backtrack.json`):
- C5:728F->7297 score=6 (highest in block), start=0x20
- C5:7265->726F score=4, start=0xC0
- C5:728C->728D score=4, start=0x9F

Anchor reports:
- C5:7202: strong=0, weak=2, invalid=4
- C5:7216: strong=0, weak=1, invalid=1
- C5:726F: strong=0, weak=1, invalid=0
- C5:728D: strong=0, weak=1, invalid=1
- C5:7297: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:7202 = `76 89 74 8B 30 BC 00 79 17 F5 1F 08`
- C5:7216 = `F0 DD B8 47 00 19 E6 19 E6 18 E7 1A`
- C5:726F = `9F EF 7F 77 FF 01 10 00 BF BF 5B 9F`
- C5:728D = `FB 1E 20 05 60 7F 20 50 19 28 30 80`
- C5:7297 = `30 80 FF 3F 01 03 40 40 80 80 08 00`

Key trap: score-6 boundary alignment at C5:7297 still lands on `0x30` (BMI branch opcode), not a function-entry byte.

---

## Bad-start reject pages (quick close)

- C5:6F00: hard_bad=1, soft_bad=1, includes boundary_bait targets C5:6FFE/C5:6FFF.
- C5:7300: hard_bad at C5:7397 (0x00).
- C5:7400: hard_bad at C5:747F (0x00).
- C5:7500: hard_bad at C5:7506 (0x00).

These pages stay frozen without promotion review.

---

## Running promotion count

- C5:3B00..44FF: 0 promotions (notes_14)
- C5:4500..4EFF: 0 promotions (notes_15)
- C5:4F00..58FF: 0 promotions (notes_16)
- C5:5900..62FF: 0 promotions (notes_17)
- C5:6300..6CFF: 0 promotions (notes_18)
- C5:6D00..76FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c5_6d00_76ff_seam_block.json`
- `reports/c5_6d00_76ff_seam_block.md`
- `reports/c5_7000_70ff_backtrack.json`
- `reports/c5_7100_71ff_backtrack.json`
- `reports/c5_7200_72ff_backtrack.json`
- `reports/C5_7000_anchor.json`
- `reports/C5_7001_anchor.json`
- `reports/C5_7041_anchor.json`
- `reports/C5_7080_anchor.json`
- `reports/C5_70AA_anchor.json`
- `reports/C5_7117_anchor.json`
- `reports/C5_7142_anchor.json`
- `reports/C5_71BC_anchor.json`
- `reports/C5_71D0_anchor.json`
- `reports/C5_7202_anchor.json`
- `reports/C5_7216_anchor.json`
- `reports/C5_726F_anchor.json`
- `reports/C5_728D_anchor.json`
- `reports/C5_7297_anchor.json`

---

## New live seam: C5:7700..

Next unprocessed block starts at **C5:7700**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C5:7700 --pages 10 --json > reports/c5_7700_80ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c5_7700_80ff_seam_block.json --output reports/c5_7700_80ff_seam_block.md`
3. Run `score_target_owner_backtrack_v1.py` only on pages that land in `manual_owner_boundary_review`, then write notes_20.
