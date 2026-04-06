# Chrono Trigger Session 15 — Continuation Notes 72

## Block closed: C7:8000..C7:89FF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C7:8000 | mixed_command_data | mixed_lane_continue | freeze | suspect target only, data patterns |
| C7:8100 | mixed_command_data | local_control_only | freeze | local clusters only |
| C7:8200 | mixed_command_data | local_control_only | freeze | local clusters only |
| C7:8300 | text_ascii_heavy | mixed_lane_continue | freeze | ASCII-heavy data region |
| C7:8400 | text_ascii_heavy | manual_owner_boundary_review | freeze | 8 targets but data/pointer table, false positives |
| C7:8500 | mixed_command_data | mixed_lane_continue | freeze | suspect targets, data patterns |
| C7:8600 | mixed_command_data | local_control_only | freeze | local clusters only |
| C7:8700 | mixed_command_data | local_control_only | freeze | local clusters only |
| C7:8800 | mixed_command_data | manual_owner_boundary_review | freeze | score-6 backtrack but weak callers, data patterns |
| C7:8900 | candidate_code_lane | local_control_only | freeze | no external xrefs, local only |

---

## Manual-owner review summary

### C7:8400..C7:84FF
Summary: raw_targets=8, xref_hits=10, strong_or_weak=7, hard_bad=0, soft_bad=0

Targets:
- C7:84FF (2 weak callers from `C7:BC15`, `C7:CFDB`)
- C7:840E (1 weak caller from `C7:B124`)
- C7:842E (1 weak caller from `C7:AEFF`)
- C7:843C (1 weak caller from `C7:B055`)
- C7:84C4 (1 weak caller from `C7:AE9C`)
- C7:845E, C7:84A5, C7:84D2 (inferred targets)

Backtrack scan:
- C7:8405->840E score=4
- C7:842C->842E score=4
- C7:84CA->84D2 score=4
- Others: score 2 or 1 (self-referential)

ROM-byte check:
- **ASCII ratio: 50.4%** (129/256 bytes) - moderate, not natural text
- **Data pattern evident**: `50 FF A8 FF 55 FF AA FF 55 FF AA FF...` - alternating values
- Target bytes are data values, not opcodes:
  - C7:840E: `AA` (not a valid entry point)
  - C7:842E: `80 FF` (BRA -1 pattern, data)
  - C7:84FF: `01` (not valid opcode start)

Anchor analysis:
- **All callers from unresolved regions** (C7:B124, C7:AEFF, C7:BC15, etc.)
- Bank C7 has **no code manifests** - entire bank marked as data
- **Bank mismatch found**: CA:2B0C `JSR $CFDB` incorrectly mapped to C7:CFDB

Verdict:
- **False positive pattern**: 8 targets are data table entries, not code
- Xrefs are data references misinterpreted as code references
- Score-4 backtracks land in data patterns, not valid prologues
- High activity (10 hits) reflects data structure density, not code

**Frozen.**

---

### C7:8800..C7:88FF
Summary: raw_targets=2, xref_hits=3, strong_or_weak=2, hard_bad=0, soft_bad=0

Targets:
- C7:88AD (2 weak callers from `C7:E55A`, `C7:E671`)
- C7:88A1 (1 suspect caller from `C7:7CE5`)

Backtrack scan:
- C7:8898->88A1 score=6
- C7:88AC->88AD score=2

ROM-byte check:
- Score-6 candidate C7:8898 starts with `22` (JSL)
- But target C7:88A1 byte pattern suggests data, not code entry
- Local clusters show high ASCII ratio (85.7%) - data-like

Anchor analysis:
- **Callers from unresolved regions**
- C7:E55A, C7:E671, C7:7CE5 not in any manifest ranges

Verdict:
- Score-6 backtrack with JSL prologue initially promising
- But caller quality fails (all unresolved)
- Byte patterns confirm data region, not code

**Frozen.**

---

## Block read

- **Highest activity page**: **C7:8400..C7:84FF** — 8 targets, 10 xref hits, 7 strong/weak. Detailed analysis revealed **false positives**: target bytes are data values (AA, 80 FF, 01), not opcodes. Bank mismatch (CA:CFDB vs C7:CFDB) indicates xref detection errors. The "high activity" reflects dense pointer table structure, not code.

- **610-page streak intact**: Despite C7:8400 having the highest target count in recent blocks, analysis confirmed **data region, not code gap**. The streak measures continuous code coverage; bank C7 is legitimately data and doesn't break the streak.

- **Family distribution shift**: 70% mixed_command_data, 20% text_ascii_heavy, 10% candidate_code_lane. The 2 text_ascii_heavy pages (8300, 8400) contain pointer tables with ASCII-range values, not natural text.

- **Manual review rate**: **20%** (2/10 pages) — continues elevated pattern from previous blocks. Both manual-review pages (8400, 8800) had score-4/6 backtracks but failed caller quality review.

- **False positive lesson**: C7:8400 demonstrates that high target counts (8) and xref hits (10) can occur in data regions. Byte-level review (revealing AA, 01 data values) was essential to prevent false promotion.

- **Bank mismatch finding**: Cross-bank xref detection incorrectly mapped CA:2B0C's `JSR $CFDB` to C7:CFDB instead of CA:CFDB. This suggests potential xref index accuracy issues in data-heavy regions.

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
- C6:0400..0DFF: 0 promotions (notes_34)
- C6:0E00..17FF: 0 promotions (notes_35)
- C6:1800..21FF: 0 promotions (notes_36)
- C6:2200..2BFF: 0 promotions (notes_37)
- C6:2C00..35FF: 0 promotions (notes_38)
- C6:3600..3FFF: 0 promotions (notes_39)
- C6:4000..49FF: 0 promotions (notes_40)
- C6:4A00..53FF: 0 promotions (notes_41)
- C6:5400..5DFF: 0 promotions (notes_42)
- C6:5E00..67FF: 0 promotions (notes_43)
- C6:6800..71FF: 0 promotions (notes_44)
- C6:7200..7BFF: 0 promotions (notes_45)
- C6:7C00..85FF: 0 promotions (notes_46)
- C6:8600..8FFF: 0 promotions (notes_47)
- C6:9000..99FF: 0 promotions (notes_48)
- C6:9A00..A3FF: 0 promotions (notes_49)
- C6:A400..ADFF: 0 promotions (notes_50)
- C6:AE00..B7FF: 0 promotions (notes_51)
- C6:B800..C1FF: 0 promotions (notes_52)
- C6:C200..CBFF: 0 promotions (notes_53)
- C6:CC00..D5FF: 0 promotions (notes_54)
- C6:D600..DFFF: 0 promotions (notes_55)
- C6:E000..E9FF: 0 promotions (notes_56)
- C6:EA00..F3FF: 0 promotions (notes_57)
- C6:F400..FDFF: 0 promotions (notes_58)
- C6:FE00..C7:07FF: 0 promotions (notes_59)
- C7:0800..11FF: 0 promotions (notes_60)
- C7:1200..1BFF: 0 promotions (notes_61)
- C7:1C00..25FF: 0 promotions (notes_62)
- C7:2600..2FFF: 0 promotions (notes_63)
- C7:3000..39FF: 0 promotions (notes_64)
- C7:3A00..43FF: 0 promotions (notes_65)
- C7:4400..4DFF: 0 promotions (notes_66)
- C7:4E00..57FF: 0 promotions (notes_67)
- C7:5800..61FF: 0 promotions (notes_68)
- C7:6200..6BFF: 0 promotions (notes_69)
- C7:6C00..75FF: 0 promotions (notes_70)
- C7:7600..7FFF: 0 promotions (notes_71)
- C7:8000..89FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c7_8000_89ff_seam_block.json`
- `reports/c7_8000_89ff_seam_block.md`
- `reports/c7_8400_84ff_backtrack.json`
- `reports/c7_8800_88ff_backtrack.json`

---

## New live seam: C7:8A00..

Next unprocessed block starts at **C7:8A00**.

### Remaining C7 bank

~118 pages (C7:8A00..FFFF). Estimated 12 more ten-page blocks.

### Key findings summary

| Finding | Impact |
|---------|--------|
| 610-page streak intact | Conservative approach validated |
| C7:8400 false positives | High target count ≠ code (data patterns) |
| Bank mismatch (CA vs C7) | Xref index accuracy issues in data regions |
| 20% manual review rate continues | Consistent pattern across blocks |
| All callers from unresolved regions | Caller quality remains critical blocker |

### Next steps

1. `python tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:8A00 --pages 10 --json > reports/c7_8a00_93ff_seam_block.json`
2. `python tools/scripts/render_seam_block_report_v1.py --input reports/c7_8a00_93ff_seam_block.json --output reports/c7_8a00_93ff_seam_block.md`
3. Run owner-backtrack and anchor reports for manual-review pages
4. Write `docs/sessions/chrono_trigger_session15_continue_notes_73.md`
