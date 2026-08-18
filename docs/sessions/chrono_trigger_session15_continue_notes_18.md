# Chrono Trigger Session 15 — Continuation Notes 18

## Block closed: C5:6300..C5:6CFF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes still active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C5:6300 | candidate_code_lane | local_control_only | freeze | no xref hits; local clusters only |
| C5:6400 | candidate_code_lane | mixed_lane_continue | freeze | weak-only callers (unresolved) and top starts are `0xCD` / `0xF0` |
| C5:6500 | branch_fed_control_pocket | local_control_only | freeze | lone suspect target with one weak unresolved caller |
| C5:6600 | mixed_command_data | local_control_only | freeze | no targets, no xrefs |
| C5:6700 | candidate_code_lane | mixed_lane_continue | freeze | weak/suspect targets only; top starts `0x7F` / `0x63` |
| C5:6800 | candidate_code_lane | local_control_only | freeze | no xref hits; local cluster only |
| C5:6900 | candidate_code_lane | local_control_only | freeze | zero external xref despite dense local clusters |
| C5:6A00 | candidate_code_lane | local_control_only | freeze | suspect target C5:6A3E only; weak unresolved caller; start `0x8F` |
| C5:6B00 | mixed_command_data | mixed_lane_continue | freeze | zero targets, zero xrefs |
| C5:6C00 | candidate_code_lane | local_control_only | freeze | suspect target C5:6C30 only; weak unresolved caller; start `0xFE` |

---

## Anchor and backtrack detail (caller-backed targets)

No page in this block reached `manual_owner_boundary_review`; validation was done anyway for all caller-backed targets.

### C5:6400..64FF
Targets: C5:6440 (weak, hits=1), C5:64B0 (weak, hits=1)

- C5:64B0 backtrack: C5:64AE -> C5:64B0, score=2, start_byte=0xCD (`CMP abs`)
- C5:6440 backtrack: C5:6440 -> C5:6440, score=-1, start_byte=0xF0 (`BEQ rel`)
- Anchor reports: both targets have **0 strong**, **1 weak**, caller status unresolved
- Additional noise: each target also has invalid same-bank mismatch hits from other banks
- Verdict: no promotable owner boundary

### C5:6500..65FF
Target: C5:6576 (suspect, hits=1)

- Backtrack: C5:6576 -> C5:6576, score=3, start_byte=0x20 (`JSR abs`)
- Anchor report: **0 strong**, **1 weak** (caller C5:C537 unresolved)
- Page family is `branch_fed_control_pocket`
- Verdict: unresolved caller quality and branch-fed family; freeze

### C5:6700..67FF
Targets: C5:67B5 (weak, hits=1), C5:6747 (suspect, hits=1)

- C5:6747 backtrack: C5:6743 -> C5:6747, score=2, start_byte=0x7F (`ADC long,X`)
- C5:67B5 backtrack: C5:67B1 -> C5:67B5, score=2, start_byte=0x63 (`ADC sr,S`)
- Anchor reports: both targets **0 strong**, **1 weak**, callers unresolved
- Verdict: starts are arithmetic opcodes, not defensive function entries; freeze

### C5:6A00..6AFF
Target: C5:6A3E (suspect, hits=1)

- Backtrack: C5:6A3B -> C5:6A3E, score=4, start_byte=0x8F (`STA long`)
- Anchor report: **0 strong**, **1 weak** (caller C5:EADF unresolved)
- Verdict: single unresolved weak caller and non-prologue start opcode; freeze

### C5:6C00..6CFF
Target: C5:6C30 (suspect, hits=1)

- Backtrack: C5:6C2B -> C5:6C30, score=2, start_byte=0xFE (`INC abs,X`)
- Anchor report: **0 strong**, **1 weak** (caller C5:92CC unresolved), plus 4 invalid bank-mismatch hits
- Verdict: valid evidence remains weak-only and target start byte is non-prologue; freeze

---

## Structural takeaways from this block

1. No `manual_owner_boundary_review` pages appeared in this 10-page sweep.
2. All caller-backed targets remained weak/unresolved; no resolved caller evidence surfaced.
3. Best backtrack score was only 4 (C5:6A3E) and still failed start-byte quality.
4. This stretch looks like continuation dead-lane/mixed-lane territory rather than callable function boundary territory.

---

## Running promotion count

- C5:3B00..44FF: 0 promotions (notes_14)
- C5:4500..4EFF: 0 promotions (notes_15)
- C5:4F00..58FF: 0 promotions (notes_16)
- C5:5900..62FF: 0 promotions (notes_17)
- C5:6300..6CFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c5_6300_6cff_seam_block.json`
- `reports/c5_6300_6cff_seam_block.md`
- `reports/c5_6400_64ff_backtrack.json`
- `reports/c5_6500_65ff_backtrack.json`
- `reports/c5_6700_67ff_backtrack.json`
- `reports/c5_6a00_6aff_backtrack.json`
- `reports/c5_6c00_6cff_backtrack.json`
- `reports/c5_6440_anchor.json`
- `reports/c5_64b0_anchor.json`
- `reports/c5_6576_anchor.json`
- `reports/c5_6747_anchor.json`
- `reports/c5_67b5_anchor.json`
- `reports/c5_6a3e_anchor.json`
- `reports/c5_6c30_anchor.json`

---

## New live seam: C5:6D00..

Next unprocessed block starts at **C5:6D00**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C5:6D00 --pages 10 --json > reports/c5_6d00_76ff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c5_6d00_76ff_seam_block.json --output reports/c5_6d00_76ff_seam_block.md`
3. Run owner-backtrack scans only for pages that land in `manual_owner_boundary_review`; otherwise freeze and advance.
