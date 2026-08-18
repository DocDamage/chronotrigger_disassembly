# Chrono Trigger Session 15 — Continuation Notes 73

## Block closed: C7:8A00..C7:93FF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C7:8A00 | candidate_code_lane | local_control_only | freeze | local clusters only, no external xrefs |
| C7:8B00 | mixed_command_data | mixed_lane_continue | freeze | no clusters, mixed data patterns |
| C7:8C00 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:8D00 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:8E00 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:8F00 | candidate_code_lane | local_control_only | freeze | suspect target 8F91, data patterns |
| C7:9000 | candidate_code_lane | manual_owner_boundary_review | freeze | weak target, data patterns, weak callers |
| C7:9100 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:9200 | candidate_code_lane | local_control_only | freeze | 4 clusters but data patterns, no code structure |
| C7:9300 | candidate_code_lane | local_control_only | freeze | 2 tiny veneers but data patterns |

---

## Critical finding: False positive classification

### The "code-dense" block is actually DATA

Despite **90% candidate_code_lane** classification (9 of 10 pages), detailed byte analysis reveals **no actual 65816 code**:

| Indicator | Expected for Code | Actual Findings | Status |
|-----------|-------------------|-----------------|--------|
| PHP ($08) | Common (stack frame) | **0 in all pages** | ❌ Missing |
| PHA ($48) | Common (save registers) | **0 in all pages** | ❌ Missing |
| PHB ($8B) | Common (save data bank) | **0 in all pages** | ❌ Missing |
| REP/SEP ($C2/$E2) | Frequent | 0-1 per page | ❌ Rare |
| RTS per 256 bytes | Multiple | 1-2 only | ❌ Too few |
| RTI ($40) | Rare (interrupts only) | 1-3 per page | ❌ Abnormally high |

**C7:9200 sample bytes:**
```
01 C1 44 FC FD 98 12 40 EE 11 C2 00 13 2B 90 0D
DA D4 41 DE 0F 14 0B 80 C5 60 FF AD 66 ED 03 43
```

**Assessment:** Random byte distribution with no recognizable instruction sequences. Valid 65816 code would show:
- Function prologues: `PHP : PHD : PHB : REP #$30`
- Register operations: `LDA`, `STA`, `LDX`, `STX`
- Control flow: `BRA`, `BEQ`, `JSR`, `JMP`

**Conclusion:** The "candidate_code_lane" classification is a **false positive** from random byte distributions coincidentally matching opcode patterns.

**Likely content:** Graphics data (tilemaps), compressed data, or lookup tables.

---

## Manual-owner review summary

### C7:9000..C7:90FF
Summary: raw_targets=1, xref_hits=2, strong_or_weak=1, hard_bad=0, soft_bad=0

Target:
- C7:9010 (2 weak callers from `C7:ACDA`, `C7:BB34`)

Backtrack scan:
- C7:9010->9010 score=3
- Start byte: `0x22` (JSL) - but data pattern
- Candidate range: C7:9010..C7:9028 (only 25 bytes)

Anchor report:
- **Classification: valid / weak / unresolved**
- Both callers from **unresolved regions**

ROM-byte check:
- **No standard function prologues** (PHP, PHB, PHD absent)
- Byte distribution: 46% entropy (suggests data/tables)
- Only 2 zero bytes, 3 FF bytes (low padding - data characteristic)
- 1 repeated pair (BD 94) - table-like pattern

Verdict:
- Score-3 backtrack is borderline-low
- Start byte 0x22 (JSL) but following bytes don't form valid long address
- **Likely jump table or data table** with bytes interpreted as JSL opcodes
- Both callers weak/unresolved

**Frozen.**

---

## "Tiny veneers" analysis

C7:9300 was flagged with "2 tiny veneers" - small code stubs that typically:
1. Set up bank register: `PHB : LDA #bank : PHA : PLB`
2. Jump to implementation: `JMP/JML target`
3. Size: typically 3-7 bytes

**Actual findings at C7:9300:**
- No JMP ($4C) or JML ($5C) instructions
- No RTL ($6B) for long-return veneers
- Random data pattern doesn't match veneer structure

**Conclusion:** Veneer detection is picking up **coincidental byte patterns**, not real code stubs.

---

## Block read

- **Critical false positive identified**: 90% candidate_code_lane classification (9 pages) appeared promising as "code-dense," but byte-level analysis revealed **zero stack operations** (PHP/PHA/PHB), **abnormal RTI frequency**, and **no coherent instruction sequences**. This is **data**, not code.

- **620-page milestone**: Seam work has now processed **62 consecutive ten-page blocks** without promotion. The streak includes correctly identifying false positive classifications like this block.

- **Classification algorithm limitation**: The seam toolkit's family detection can be fooled by random byte distributions in data regions that coincidentally match opcode patterns. Manual byte review remains essential.

- **Manual review rate normalized**: **10%** (1/10 pages) - returned to baseline after 20% in previous blocks. The single manual-review page (C7:9000) was correctly identified as data, not code.

- **Local clusters are not functions**: Pages flagged with "4 local clusters" (C7:9200) or "2 tiny veneers" (C7:9300) contain data patterns, not callable subroutines. Cluster detection is picking up coincidental branch/return byte patterns.

- **Cross-block pattern**: C7 bank continues to show data-heavy characteristics. The shift from mixed_command_data (70% in C7:8000 block) to candidate_code_lane (90% in this block) reflects different data types (pointer tables vs graphics/compressed data), not code emergence.

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
- C7:8A00..93FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c7_8a00_93ff_seam_block.json`
- `reports/c7_8a00_93ff_seam_block.md`
- `reports/c7_9000_90ff_backtrack.json`
- `reports/C7_9010_anchor.json`

---

## New live seam: C7:9400..

Next unprocessed block starts at **C7:9400**.

### 620-page milestone and critical lesson

Seam work has processed **62 consecutive ten-page blocks** without promotion. This block taught a critical lesson:

**Classification ≠ Reality**
- 90% candidate_code_lane looked promising
- Byte review revealed **zero stack operations**, **no function prologues**
- Result: **False positive** - data, not code

**Verification hierarchy:**
1. Page family (classification) - least reliable
2. Xref hits and backtrack scores - moderate reliability
3. **Byte-level review** - most reliable
4. Caller anchor quality - critical for promotion

### Remaining C7 bank

~108 pages (C7:9400..FFFF). Estimated 11 more ten-page blocks.

### Next steps

1. `python tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:9400 --pages 10 --json > reports/c7_9400_9dff_seam_block.json`
2. `python tools/scripts/render_seam_block_report_v1.py --input reports/c7_9400_9dff_seam_block.json --output reports/c7_9400_9dff_seam_block.md`
3. Run owner-backtrack and anchor reports for manual-review pages
4. Write `docs/sessions/chrono_trigger_session15_continue_notes_74.md`
