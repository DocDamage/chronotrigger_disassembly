# Chrono Trigger Session 15 — Continuation Notes 74

## Block closed: C7:9400..C7:9DFF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C7:9400 | candidate_code_lane | manual_owner_boundary_review | freeze | 10 targets but data misinterpretation, zero returns, weak callers |
| C7:9500 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:9600 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:9700 | branch_fed_control_pocket | local_control_only | freeze | local clusters only |
| C7:9800 | branch_fed_control_pocket | manual_owner_boundary_review | freeze | weak callers, cross-bank mismatch |
| C7:9900 | branch_fed_control_pocket | local_control_only | freeze | local clusters only |
| C7:9A00 | branch_fed_control_pocket | local_control_only | freeze | local clusters only |
| C7:9B00 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:9C00 | mixed_command_data | mixed_lane_continue | freeze | mixed data patterns |
| C7:9D00 | mixed_command_data | mixed_lane_continue | freeze | no targets |

---

## Manual-owner review summary

### C7:9400..C7:94FF
Summary: raw_targets=10, xref_hits=11, strong_or_weak=6, hard_bad=0, soft_bad=0

Targets (highest activity in project):
- C7:9401 (2 weak callers from `C7:CE10`, `C7:91BB`)
- C7:940F (1 weak caller from `C7:BAF5`)
- C7:9413 (1 weak caller from `C7:AEC0`)
- C7:94DD (1 weak caller from `C7:AD19`)
- C7:94F4 (1 weak caller from `C7:AE81`)
- Plus 5 additional targets

Backtrack scores:
- **Maximum: 4/10** (C7:94EE, C7:94F4) - below promotion threshold
- Most targets: **2/10** - poor scores
- All targets have suspicious start bytes

**Critical finding - ZERO returns:**
- **0 RTS/RTL in 256 bytes** - impossible for 10 real subroutines
- Expected: 5-10 returns for 10 functions

ROM-byte check:
- 25 branches in 256 bytes (extremely high density - suggests data misinterpretation)
- Target C7:9401 starts with `0x32` = `AND (d)` - unusual entry point
- One caller uses **JMP not JSR** (C7:BAF5 → C7:940F) - suggests jump target, not subroutine

Anchor analysis:
- **All callers weak/unresolved** (C7:CE10, C7:91BB, C7:BAF5, etc.)
- **Cross-bank mismatch**: D6:0ECB incorrectly mapped to C7:9401 (should be D6:9401)
- Caller C7:91BB in **closed data range** (suspect classification)

Verdict:
- **10 targets = data misinterpretation**, not real code
- **Zero returns** definitively proves this is not 10 subroutines
- High xref count (11) is statistical artifact from unresolved regions
- Maximum backtrack 4/10 below promotion threshold

**Frozen.**

---

### C7:9800..C7:98FF
Summary: raw_targets=2, xref_hits=3, strong_or_weak=1, hard_bad=0, soft_bad=0

Targets:
- C7:9801 (2 weak callers from `C7:7400`, `C7:CF8A`)

Backtrack scan:
- C7:9800->9801 score=4
- Start byte: `D0 0F` = `BNE $0F` (valid branch instruction)
- Target distance: 1 byte (suspicious)

Anchor analysis:
- **All callers weak/unresolved**
- Caller C7:7400 in **closed data range** (C7:7400..C7:74FF)
- Cross-bank confusion detected

Local clusters:
- C7:9800..9808: 9 bytes, 1 branch, 1 return
- C7:989D..98A1: 5 bytes, 1 call, 1 return

Verdict:
- Score-4 backtrack with valid BNE instruction initially promising
- But callers weak/unresolved
- Page-end targets suggest data structure boundary

**Frozen.**

---

## Critical finding: Highest activity = false positive

### C7:9400 statistics comparison

| Metric | C7:9400 | Expected for Real Code | Status |
|--------|---------|------------------------|--------|
| Targets | 10 | 2-3 for 256 bytes | ❌ Too high |
| Xref hits | 11 | 3-5 | ❌ Suspicious |
| Backtrack max | 4/10 | 6-10 | ❌ Below threshold |
| Returns (RTS/RTL) | 0 | 5-10 | ❌ **ZERO** |
| Prologues | 3 | 5-10 | ❌ Low |
| Branches | 25 | 10-15 | ❌ Too high |

**The 10 targets represent data misinterpretation**, not subroutines.

### Root cause analysis

1. **Zero returns**: Impossible for real code. Real subroutines require RTS/RTL.

2. **Data bytes as opcodes**: Page contains data with byte sequences that match:
   - JSR $xxxx (0x20 + 2 bytes)
   - JMP $xxxx (0x4C + 2 bytes)
   - JSL $xxxxxx (0x22 + 3 bytes)

3. **Cross-bank mismatch**: D6:0ECB `JSR $9401` incorrectly mapped to C7:9401 (should be D6:9401).

4. **Circular dependency**: All callers in unresolved regions → weak classification → no promotion.

---

## Block read

- **Highest activity false positive**: C7:9400 had unprecedented 10 targets, 11 xref hits - the highest in 63 blocks. Detailed analysis revealed **zero returns**, **maximum backtrack 4/10**, and **data misinterpretation patterns**. The high activity is statistical artifact, not real code.

- **630-page milestone**: Seam work has processed **63 consecutive ten-page blocks** without promotion. Despite multiple "high activity" pages (C7:8400 with 8 targets, C7:9400 with 10 targets), all have proven to be data regions with coincidental opcode patterns.

- **Classification reliability**: Page family (candidate_code_lane, branch_fed_control_pocket) is **not reliable** for identifying code. C7:9400 was candidate_code_lane but contained data. Verification hierarchy remains: caller quality > byte review > backtrack > family.

- **Cross-bank xref issues**: Multiple blocks show bank mismatch errors (CA:CFDB→C7:CFDB, D6:9401→C7:9401). Xref index accuracy degrades in data-heavy regions.

- **Manual review rate**: **20%** (2/10 pages) - elevated due to high xref activity. Both manual-review pages (9400, 9800) were correctly frozen after analysis.

- **Pattern boundary**: Final 2 pages (9C00, 9D00) classified as mixed_command_data with mixed_lane_continue - suggests transition to different data region.

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
- C7:8000..89FF: 0 promotions (notes_72)
- C7:8A00..93FF: 0 promotions (notes_73)
- C7:9400..9DFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c7_9400_9dff_seam_block.json`
- `reports/c7_9400_9dff_seam_block.md`
- `reports/c7_9400_94ff_backtrack.json`
- `reports/c7_9800_98ff_backtrack.json`

---

## New live seam: C7:9E00..

Next unprocessed block starts at **C7:9E00**.

### 630-page milestone and verification lessons

Seam work has processed **63 consecutive ten-page blocks** without promotion. This block taught critical lessons:

**High activity ≠ Real code**
- C7:9400: 10 targets, 11 xrefs (highest activity)
- Reality: **Zero returns**, data misinterpretation

**Definitive disqualifiers:**
1. **Zero RTS/RTL** in page with 10 "targets" → impossible for real subroutines
2. **All callers unresolved** → weak anchor chain
3. **Cross-bank mismatches** → xref index errors in data regions

**Verification hierarchy (reliable → unreliable):**
1. ✅ Returns present (RTS/RTL) - hard requirement
2. ✅ Caller from resolved code - strong anchor
3. ✅ Prologues (PHP/PHB/REP) - structural evidence
4. ⚠️ Backtrack score ≥6 - moderate reliability
5. ❌ Xref hit count - can be false positive
6. ❌ Page family - least reliable indicator

### Remaining C7 bank

~98 pages (C7:9E00..FFFF). Estimated 10 more ten-page blocks.

### Next steps

1. `python tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:9E00 --pages 10 --json > reports/c7_9e00_a7ff_seam_block.json`
2. `python tools/scripts/render_seam_block_report_v1.py --input reports/c7_9e00_a7ff_seam_block.json --output reports/c7_9e00_a7ff_seam_block.md`
3. Run owner-backtrack and anchor reports for manual-review pages
4. Write `docs/sessions/chrono_trigger_session15_continue_notes_75.md`
