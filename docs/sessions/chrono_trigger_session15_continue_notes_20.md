# Chrono Trigger Session 15 — Continuation Notes 20

## Block closed: C5:7700..C5:80FF (10 pages)

Processed with the upgraded seam toolkit (all 5 fixes active).
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C5:7700 | mixed_command_data | manual_owner_boundary_review | freeze | both targets weak-only (unresolved callers); starts `0xE6` / `0x7D` |
| C5:7800 | candidate_code_lane | manual_owner_boundary_review | freeze | weak-only callers and starts `0x70` / `0x08` |
| C5:7900 | candidate_code_lane | manual_owner_boundary_review | freeze | one weak + two suspect targets; best start `0xF8` (SED) |
| C5:7A00 | candidate_code_lane | manual_owner_boundary_review | freeze | lone weak target C5:7A82 starts at `0x79` (`ADC abs,Y`) |
| C5:7B00 | candidate_code_lane | local_control_only | freeze | no targets, no xrefs |
| C5:7C00 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | hard_bad present and mixed-command page with boundary trap C5:7CFF |
| C5:7D00 | candidate_code_lane | mixed_lane_continue | freeze | weak boundary-bait target C5:7DFE plus suspect C5:7D91 |
| C5:7E00 | candidate_code_lane | local_control_only | freeze | lone suspect target C5:7EC4; no weak/strong caller support |
| C5:7F00 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | hard_bad=3 despite several weak hits; page is poisoned |
| C5:8000 | mixed_command_data | bad_start_or_dead_lane_reject | freeze | hard_bad=9 with 20 raw targets / 29 xref hits (high-noise mixed data) |

---

## Manual-owner pages (anchor detail)

### C5:7700..77FF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets and structure:
- C5:7700 (weak, hits=1, caller C5:B434)
- C5:770C (weak, hits=1, caller C5:07BE)
- Backtrack: C5:770C->770C score=3, start=0x7D
- Backtrack: C5:7700->7700 score=1, start=0xE6

Anchor reports:
- C5:7700: strong=0, weak=1, invalid=7
- C5:770C: strong=0, weak=1, invalid=1

ROM-byte check:
- C5:7700 = `E6 00 99 FE 81 FE 21 3F E0 7F 00 A0`
- C5:770C = `7D B2 FE 79 FB FD FB 31 D8 00 FF FF`

Verdict: both starts are non-prologue opcodes with unresolved caller quality; freeze.

### C5:7800..78FF
Summary: raw_targets=2, xref_hits=2, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets and structure:
- C5:7823 (weak, hits=1, caller C5:44C5)
- C5:7868 (weak, hits=1, caller C5:99D1)
- Backtrack: C5:7860->7868 score=4, start=0x08
- Backtrack: C5:7823->7823 score=1, start=0x70

Anchor reports:
- C5:7823: strong=0, weak=1, invalid=3
- C5:7868: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:7823 = `70 8F 48 B7 00 48 B7 FF EF EF E7 F7`
- C5:7868 = `3F 03 00 04 18 B9 78 7C FA FE FB 00`

Verdict: weak-only unresolved callers and no defensible entry opcode.

### C5:7900..79FF
Summary: raw_targets=3, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets and structure:
- C5:79CD (weak, hits=1, caller C5:64AD)
- C5:795F (suspect, hits=1, caller C5:29AD)
- C5:7964 (suspect, hits=1, caller C5:84B0)
- Backtrack: C5:79CA->79CD score=4, start=0xF8
- Backtracks: C5:795C->795F score=2 and C5:795C->7964 score=2, start=0x3F

Anchor reports:
- C5:79CD: strong=0, weak=1, invalid=2
- C5:795F: strong=0, weak=1, invalid=1
- C5:7964: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:79CD = `CF 65 F8 AF 10 EF 8B 89 60 14 08 60`
- C5:795F = `E0 F1 C0 E0 F0 C0 E0 80 C0 43 07 56`
- C5:7964 = `C0 E0 80 C0 43 07 56 17 80 7F 00 F1`

Verdict: high backtrack is anchored on SED/data-like flow; no promotable boundary.

### C5:7A00..7AFF
Summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0

Target and structure:
- C5:7A82 (weak, hits=1, caller C5:0271)
- Backtrack: C5:7A75->7A82 score=4, start=0x81

Anchor report:
- C5:7A82: strong=0, weak=1, invalid=0

ROM-byte check:
- C5:7A82 = `79 DE AD D1 10 BF 46 7B CF 20 42 07`

Verdict: lone unresolved weak caller and non-prologue entry byte; freeze.

---

## High-noise reject pages (quick close)

- C5:7C00: `bad_start_or_dead_lane_reject`, hard_bad=1, mixed-command page, includes boundary_bait at C5:7CFF.
- C5:7F00: `bad_start_or_dead_lane_reject`, hard_bad=3; score-6 pockets exist but page is poisoned.
- C5:8000: `bad_start_or_dead_lane_reject`, hard_bad=9 with dense mixed target traffic (20 raw targets, 29 xref hits).

These stay frozen without promotion attempts.

---

## Running promotion count

- C5:3B00..44FF: 0 promotions (notes_14)
- C5:4500..4EFF: 0 promotions (notes_15)
- C5:4F00..58FF: 0 promotions (notes_16)
- C5:5900..62FF: 0 promotions (notes_17)
- C5:6300..6CFF: 0 promotions (notes_18)
- C5:6D00..76FF: 0 promotions (notes_19)
- C5:7700..80FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c5_7700_80ff_seam_block.json`
- `reports/c5_7700_80ff_seam_block.md`
- `reports/c5_7700_77ff_backtrack.json`
- `reports/c5_7800_78ff_backtrack.json`
- `reports/c5_7900_79ff_backtrack.json`
- `reports/c5_7a00_7aff_backtrack.json`
- `reports/C5_7700_anchor.json`
- `reports/C5_770C_anchor.json`
- `reports/C5_7823_anchor.json`
- `reports/C5_7868_anchor.json`
- `reports/C5_79CD_anchor.json`
- `reports/C5_795F_anchor.json`
- `reports/C5_7964_anchor.json`
- `reports/C5_7A82_anchor.json`

---

## New live seam: C5:8100..

Next unprocessed block starts at **C5:8100**.

Recommended next move:
1. `python3 tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C5:8100 --pages 10 --json > reports/c5_8100_8aff_seam_block.json`
2. `python3 tools/scripts/render_seam_block_report_v1.py --input reports/c5_8100_8aff_seam_block.json --output reports/c5_8100_8aff_seam_block.md`
3. Run owner-backtrack scans only for pages in `manual_owner_boundary_review`, then write notes_21.
