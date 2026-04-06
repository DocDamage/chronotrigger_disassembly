# Chrono Trigger Session 15 — Continuation Notes 76

## Block closed: C7:A800..C7:B1FF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C7:A800 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:A900 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:AA00 | candidate_code_lane | mixed_lane_continue | freeze | 1 target, weak caller |
| C7:AB00 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:AC00 | mixed_command_data | local_control_only | freeze | local clusters only |
| C7:AD00 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:AE00 | mixed_command_data | manual_owner_boundary_review | freeze | 1 target, weak caller from unresolved |
| C7:AF00 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:B000 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | 6 targets but 0 returns, fragmented code |
| C7:B100 | mixed_command_data | manual_owner_boundary_review | freeze | 4 targets, 3 returns, but weak callers |

---

## Manual-owner review summary

### C7:AE00..C7:AEFF
Summary: raw_targets=1, xref_hits=1, strong_or_weak=1, hard_bad=0, soft_bad=0

Target:
- C7:AE84 (1 weak caller from `C7:BC04`)

Backtrack scan:
- C7:AE81->AE84 score=4
- Start byte: JSR (0x20)

Anchor report:
- Caller from **unresolved region**

Verdict:
- Score-4 backtrack with JSR prologue
- But single weak caller insufficient
- Local cluster shows code-like structure

**Frozen.**

---

### C7:B100..C7:B1FF
Summary: raw_targets=4, xref_hits=4, strong_or_weak=2, hard_bad=0, soft_bad=2

Targets:
- C7:B111 (1 weak caller from `C7:C02A`)
- C7:B195 (1 weak caller from `C7:B68A`)
- C7:B115 (1 suspect caller from `C7:A76A` - in **resolved DATA range**)
- C7:B188 (1 suspect caller from `C7:7488` - in **resolved DATA range**)

Backtrack scan:
- C7:B110->B111 score=4
- C7:B110->B115 score=4 (dual-target candidate!)
- C7:B17E->B188 score=4
- C7:B18D->B195 score=2

**Critical ROM-byte findings:**
```
Returns: 3 (RTS/RTL)
Prologues: 2 (PHP/SEP)
JSR: 6 (internal calls)
JSL: 3 (external calls)
```

**Strongest candidates:**
- **C7:B110**: Score 4, serves TWO targets (B111 and B115), starts with `JSL $5CCFE1`
- **C7:B17E**: Score 4, starts with `CMP $AFC3,X`

Anchor analysis:
- **All callers weak/unresolved** (C7:C02A, C7:B68A)
- 2 suspect callers from **resolved DATA ranges** (likely false positives)
- Callers concentrated in **C7:C3xx-C7:C4xx region** (unresolved)

Verdict:
- **Best code structure in C7 bank so far**: 3 returns, 2 prologues, 6 internal JSRs
- Score-4 candidates with JSL prologues
- **But**: All callers weak/unresolved
- **Circular dependency**: B100 needs C3xx-C4xx callers resolved; those callers need their callers resolved

**Frozen - but highest promotion potential yet.**

---

## High-activity page analysis

### C7:B000..C7:B0FF (6 targets, rejected)

Backtrack scores:
- C7:B092->B09E score=4 (JSL start)
- C7:B0DF->B0DF score=3 (JSL start)
- Others: score 2

ROM-byte check:
- **Returns: 0** - impossible for 6 subroutines
- Prologues: 3 (scattered)
- JSR: 1, JSL: 3

**Fragmented code, not coherent page.**

Individual candidates (B092, B0DF) show promise but page as a whole is data-mixed.

---

### C7:B100..C7:B1FF (4 targets, manual review)

**Most code-like page in 170+ pages of C7 analysis:**

| Metric | C7:B100 | Expected for Code | Status |
|--------|---------|-------------------|--------|
| Returns | 3 | 3-4 for 4 functions | ✅ Good |
| Prologues | 2 | 2-4 | ✅ Adequate |
| JSR internal | 6 | 4-8 | ✅ Normal |
| JSL external | 3 | 2-4 | ✅ Normal |
| Score-4 candidates | 3 | 2-4 | ✅ Excellent |

**Structural evidence strongly suggests real code.**

**Blocker: Caller quality**
- All 4 callers weak/unresolved
- Callers in C7:C3xx-C7:C4xx range not yet analyzed
- Need to resolve C3xx-C4xx region to validate B100

---

## Critical finding: C7:C3xx-C7:C4xx caller region

### Callers to B0xx/B1xx targets:

| Caller | Target | Instruction | Caller Location |
|--------|--------|-------------|-----------------|
| C7:C331 | B09E | JSR | C3xx region |
| C7:C475 | B0B4 | JMP | C3xx region |
| C7:C487 | B0DF | JSR | C3xx region |
| C7:C4AB | B0F2 | JMP | C3xx region |
| C7:C02A | B111 | JSR | C0xx region |
| C7:B68A | B195 | JSR | B6xx region |

**Pattern:** Concentrated caller cluster in **C7:C3xx-C7:C4xx** (unresolved).

**Hypothesis:** C7:C3xx-C7:C4xx contains **real code** that calls B0xx/B1xx subroutines. If C3xx-C4xx is code, B100 promotion is justified.

**Recommendation:** Analyze C7:C3xx-C7:C4xx region before next block.

---

## Block read

- **Strongest code candidate**: **C7:B100..C7:B1FF** — first page in C7 bank with **genuine code structure**: 3 returns, 2 prologues, 6 internal JSRs, 3 score-4 candidates. The dual-target candidate at C7:B110 (score 4 for both B111 and B115) is particularly strong. **But all callers weak/unresolved** — promotion blocked pending caller resolution.

- **Fragmented code**: **C7:B000..C7:B0FF** — 6 targets, 2 score-4 candidates (B092, B0DF) with JSL prologues, but **zero returns** and scattered structure. Individual candidates promising, page as a whole rejected.

- **650-page data streak intact**: Closed ranges cover C7:0000..C7:A7FF as data. C7:B100 is first page with real code structure, but not yet promoted due to weak caller chain.

- **Caller region identified**: C7:C3xx-C7:C4xx contains concentrated callers to B0xx/B1xx targets. This region likely contains the **parent code** that validates B100 as callable subroutines.

- **Manual review rate**: **20%** (2/10 pages) — normalized from 30% in previous block. Both manual-review pages (AE00, B100) show code-like structure but insufficient caller quality.

- **Code at B000 boundary**: C7:B000 (major SNES boundary) does NOT mark clean code start. B000 is fragmented; B100 shows coherent code structure ~256 bytes later.

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
- C7:9E00..C7:A7FF: 0 promotions (notes_75)
- C7:A800..C7:B1FF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c7_a800_b1ff_seam_block.json`
- `reports/c7_a800_b1ff_seam_block.md`
- `reports/c7_b000_b0ff_backtrack.json`
- `reports/c7_b100_b1ff_backtrack.json`

---

## New live seam: C7:B200..

Next unprocessed block starts at **C7:B200**.

### C7:B100 - Highest promotion candidate yet

**Structural evidence:**
- 3 returns ✅
- 2 prologues ✅
- 6 internal JSRs ✅
- 3 score-4 candidates ✅

**Blocker:**
- All callers weak/unresolved ❌
- Need C7:C3xx-C7:C4xx caller region resolved

**Path to promotion:**
1. Process C7:C300..C7:C4xx to resolve callers
2. If C3xx-C4xx is code → B100 validates as callable subroutines
3. B100 becomes first promotion in 170+ C7 pages

### Remaining C7 bank

- **Remaining**: ~78 pages (C7:B200..FFFF)
- **Estimated blocks**: ~8 more ten-page blocks
- **Bytes remaining**: 0x4E00 (19,968 bytes)

### Strategic consideration

The C7:C3xx-C7:C4xx caller region is now **high priority**. This region:
- Contains 5+ callers to B0xx/B1xx targets
- May contain the parent code that validates B100
- Could break the 170-page C7 freeze streak

**Recommended deviation:** Consider processing C7:C300..C7:C4xx before continuing linear progression, as this region is critical for validating B100.

### Next steps

**Option A (linear):**
1. `python tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:B200 --pages 10 --json > reports/c7_b200_bbff_seam_block.json`

**Option B (strategic - recommended):**
1. `python tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:C300 --pages 10 --json > reports/c7_c300_ccff_seam_block.json`
2. Analyze C7:C3xx-C7:C4xx caller region
3. If code found, return to validate B100 for promotion

Write `docs/sessions/chrono_trigger_session15_continue_notes_77.md`
