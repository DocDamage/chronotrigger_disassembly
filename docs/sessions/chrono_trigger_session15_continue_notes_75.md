# Chrono Trigger Session 15 — Continuation Notes 75

## Block closed: C7:9E00..C7:A7FF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C7:9E00 | candidate_code_lane | mixed_lane_continue | freeze | suspect target only |
| C7:9F00 | mixed_command_data | mixed_lane_continue | freeze | no targets |
| C7:A000 | mixed_command_data | manual_owner_boundary_review | freeze | 8 targets but data table (88% ASCII, 0 returns) |
| C7:A100 | mixed_command_data | mixed_lane_continue | freeze | no targets |
| C7:A200 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:A300 | mixed_command_data | mixed_lane_continue | freeze | no targets |
| C7:A400 | candidate_code_lane | manual_owner_boundary_review | freeze | 4 targets, weak callers, possible code but insufficient |
| C7:A500 | mixed_command_data | local_control_only | freeze | local clusters only |
| C7:A600 | candidate_code_lane | manual_owner_boundary_review | freeze | 1 target, weak caller |
| C7:A700 | branch_fed_control_pocket | local_control_only | freeze | local clusters only |

---

## Manual-owner review summary

### C7:A000..C7:A0FF
Summary: raw_targets=8, xref_hits=11, strong_or_weak=9, hard_bad=0, soft_bad=0

Targets:
- C7:A005 (3 weak callers from `DE:E8C0`, `F7:F573`, `F8:52EB`)
- C7:A00D (1 weak caller from `C7:CAD2`)
- C7:A02B (1 weak caller from `C7:C9A0`)
- C7:A069 (1 weak caller from `DA:60BB`)
- C7:A0A5 (1 weak caller from `C7:B9A8`)
- Plus 3 additional targets

Backtrack scan:
- C7:A068->A069 score=4 (best)
- C7:A095->A0A5 score=2
- Others: score 0 or 2

**Critical ROM-byte findings:**
```
A000: 33 33 34 34 43 68 23 44 43 32 33 33 44 32 68 33  3344Ch#DC233D2h3
```
- **88% ASCII ratio** - "3344Ch#DC233D2h3" pattern
- **Returns (RTS/RTL): 0** - impossible for 8 subroutines
- **Prologues (PHP/PHB/REP/SEP): 0** - no function entry points
- Start byte $33 at A000 - not valid 65816 opcode
- Repeated patterns (`33 34`, `44 32`, `68`) - tile/font data characteristic

Anchor analysis:
- All callers weak/unresolved
- Cross-bank callers (DE:E8C0, F7:F573, F8:52EB) suggest data references, not code calls

Verdict:
- **Definitive data table**, not code
- 11 xref hits are spurious references into numeric/text data
- High activity is false positive (like C7:9400 with 10 targets)

**Frozen.**

---

### C7:A400..C7:A4FF
Summary: raw_targets=4, xref_hits=4, strong_or_weak=4, hard_bad=0, soft_bad=0

Targets:
- C7:A400 (1 weak caller)
- C7:A460 (1 weak caller)
- C7:A4DD (1 weak caller)
- C7:A4F5 (1 weak caller)

Backtrack scan:
- C7:A4E5->A4F5 score=4
- Others: scores 3, 2, 1

ROM-byte check:
```
A400: C4 F4 FE 21 C3 4D 31 FE 21 B4 30 E1 B2 5C 10 5F
```
- Valid 65816 opcodes: C4 (MVN), F4 (PEA), 21 (AND), 5C (JML)
- 1 prologue (E2=SEP), 2 JSR, 1 JML
- 32% ASCII (more code-like than A000)
- 1 return detected

Verdict:
- Shows **real code structure** with prologues and returns
- But **all 4 callers weak/unresolved**
- Single return insufficient for 4 subroutines
- Possible code but insufficient anchor strength

**Frozen.**

---

### C7:A600..C7:A6FF
Summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0

Target:
- C7:A6A8 (1 weak caller)

Backtrack scan:
- C7:A69E->A6A8 score=4
- Start byte: 1C (TRB)

ROM-byte check:
- 2 prologues (E2=SEP), 1 RTI
- D0 (BNE) branches present
- 23% ASCII (code-like)

Verdict:
- Score-4 backtrack with prologues suggests possible code
- But single weak caller insufficient
- TRB start byte unusual for entry point

**Frozen.**

---

## Critical finding: A000 = definitive data

### Comparison: C7:9400 vs C7:A000 false positives

| Indicator | C7:9400 | C7:A000 | Status |
|-----------|---------|---------|--------|
| Targets | 10 | 8 | Both high |
| Xref hits | 11 | 11 | Both high |
| Returns | 0 | 0 | **❌ Zero** |
| Prologues | 0 | 0 | **❌ Zero** |
| ASCII ratio | Moderate | 88% | **❌ High** |
| Byte pattern | Random | "3344Ch#..." | **❌ Text/data** |

**Both pages definitively identified as DATA, not code.**

The pattern is clear: pages with **zero returns and zero prologues** cannot contain the claimed number of subroutines (8-10). These are data tables with coincidental opcode patterns.

---

## 30% manual review rate analysis

### Breakdown of 3 manual-review pages:

| Page | Actual Content | Verdict |
|------|----------------|---------|
| C7:A000 | **Data table** (88% ASCII) | ❌ False positive |
| C7:A400 | **Possible code** (prologues, returns) | ⚠️ Insufficient anchors |
| C7:A600 | **Possible code** (prologues, branches) | ⚠️ Insufficient anchors |

**30% rate = 1 false positive + 2 possible code pages**

The elevated rate reflects:
1. C7:A000's 11 spurious xref hits (data references misread as code calls)
2. Legitimate code-like structure in A400 and A600 requiring boundary verification

Unlike previous blocks where high activity indicated false positives, **A400 and A600 show genuine code characteristics** - just with insufficient caller quality for promotion.

---

## Block read

- **Highest activity false positive**: **C7:A000..C7:A0FF** — 8 targets, 11 xref hits at major SNES boundary (A000). Detailed analysis revealed **88% ASCII ratio**, **zero returns**, **zero prologues**, and **text-like byte patterns** ("3344Ch#..."). Definitively a **data table**, not code. 11 xref hits are references into numeric/font data, not subroutine calls.

- **Possible code pages**: **C7:A400** and **C7:A600** show genuine code structure with **prologues (E2=SEP)**, **returns (RTS/RTI)**, and **valid 65816 opcodes**. However, **all callers weak/unresolved** prevents promotion. These represent potential code islands in data region but lack anchor chain for verification.

- **640-page milestone approaching**: Seam work has processed **64 ten-page blocks** without promotion. The 640-page mark (block C7:A800..C7:AFFF) will be a significant milestone.

- **A000 boundary significance**: SNES banks often place code at $8000, $A000, $C000 boundaries. C7:A000 analysis confirms **no code start** at this boundary - it's data, not a code region entry point.

- **Data/code boundary detection**: Block shows clear progression: data (A000-A300) → possible code (A400, A600) → data (A500, A700). The toolkit correctly identified candidate_code_lane for A400/A600 despite surrounding data.

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
- C7:9400..9DFF: 0 promotions (notes_74)
- C7:9E00..C7:A7FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c7_9e00_a7ff_seam_block.json`
- `reports/c7_9e00_a7ff_seam_block.md`
- `reports/c7_a000_a0ff_backtrack.json`
- `reports/c7_a400_a4ff_backtrack.json`

---

## New live seam: C7:A800..

Next unprocessed block starts at **C7:A800**.

### 640-page milestone approaching

Seam work has processed **64 consecutive ten-page blocks** without promotion. Next block (C7:A800..C7:A7FF will be block 65) approaches 640 pages - a major milestone in conservative disassembly.

### C7 bank remaining work

- **Remaining**: ~88 pages (C7:A800..FFFF)
- **Estimated blocks**: ~9 more ten-page blocks
- **Bytes remaining**: 0x5800 (22,528 bytes)

The A000 boundary analysis confirms bank C7 contains primarily data. No code regions have emerged at expected SNES boundaries ($8000, $A000). Remaining pages likely continue data/event script patterns.

### Verification hierarchy reinforced

This block reinforced the definitive disqualifiers:

| Priority | Indicator | C7:A000 Result |
|----------|-----------|----------------|
| 1 | Returns (RTS/RTL) | **ZERO** ❌ |
| 2 | Prologues (PHP/PHB/REP) | **ZERO** ❌ |
| 3 | ASCII ratio | **88%** ❌ |
| 4 | Byte pattern | **"3344Ch#..."** ❌ |
| 5 | Xref hits | **11 (false)** |

**Zero returns + zero prologues = definitive data** regardless of xref count.

### Next steps

1. `python tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:A800 --pages 10 --json > reports/c7_a800_b1ff_seam_block.json`
2. `python tools/scripts/render_seam_block_report_v1.py --input reports/c7_a800_b1ff_seam_block.json --output reports/c7_a800_b1ff_seam_block.md`
3. Run owner-backtrack and anchor reports for manual-review pages
4. Write `docs/sessions/chrono_trigger_session15_continue_notes_76.md`
