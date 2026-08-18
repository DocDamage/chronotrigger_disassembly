# Chrono Trigger Session 15 — Continuation Notes 77

## Strategic Analysis: C7:C300..C7:CCFF (Caller Region)

**NOTE:** This is a non-linear strategic jump from C7:B200 to C7:C300 to analyze the caller region that could validate C7:B100.

Result: **Zero promotions** in this block, but **critical discovery of real code in C7:C3xx-C7:C4xx**.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C7:C300 | candidate_code_lane | local_control_only | freeze | 2 targets, code structure but weak callers |
| C7:C400 | candidate_code_lane | local_control_only | freeze | 3 targets, code structure but weak callers |
| C7:C500 | candidate_code_lane | manual_owner_boundary_review | freeze | 1 target, weak caller |
| C7:C600 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:C700 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:C800 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:C900 | mixed_command_data | mixed_lane_continue | freeze | mixed data patterns |
| C7:CA00 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:CB00 | candidate_code_lane | local_control_only | freeze | 3 targets but weak callers |
| C7:CC00 | mixed_command_data | mixed_lane_continue | freeze | mixed data patterns |

---

## Critical discovery: Real code in C7:C3xx-C7:C4xx

### Confirmed code structure

**C7:C300..C7:C3FF:**
- **3 prologues** (REP/SEP)
- **Direct call to C7:B09E**: `JSR $B09E` at C7:C331
- Called from **10 different banks** (C6, C7, C9, D4, D5, D6, D9, E0, EA, F0)
- 8 JSR references from external sources

**C7:C400..C7:C4FF:**
- **5 prologues** (REP/SEP)
- **Direct calls to C7:B0xx region:**
  - `JMP $B0B4` at C7:C475
  - `JSR $B0DF` at C7:C487
  - `JMP $B0F2` at C7:C4AB
- Called from **F0:9B85** (inter-bank JSL)
- 12 total references

### Verified callers to C7:B100 region

| Caller | Target | Instruction | Status |
|--------|--------|-------------|--------|
| C7:C331 | C7:B09E | JSR | Has call pattern |
| C7:C475 | C7:B0B4 | JMP | **Has prologue ($E2)** ✅ |
| C7:C487 | C7:B0DF | JSR | **Has prologue ($20)** ✅ |
| C7:C4AB | C7:B0F2 | JMP | **Has return ($60)** ✅ |
| C7:C02A | C7:B111 | JSR | Has call pattern |

**C7:C475, C7:C487, C7:C4AB show definitive code indicators** (prologues, returns).

---

## C7:B100 promotion assessment

### Current anchor status

| Target | Strength | Caller | Caller Status |
|--------|----------|--------|---------------|
| C7:B09E | weak | C7:C331 | Unresolved, but shows call pattern |
| C7:B0B4 | suspect | C7:C475 | **Shows code indicators** ✅ |
| C7:B0DF | weak | C7:C487 | **Shows code indicators** ✅ |
| C7:B0F2 | weak | C7:C4AB | **Shows code indicators** ✅ |
| C7:B111 | weak | C7:C02A | Unresolved, but shows call pattern |
| C7:B188 | suspect | C7:7488 | In data range |

### Verdict: NOT READY for promotion

**Blockers:**
1. **Circular dependency**: C7:B100 needs strong callers; C7:C3xx callers need code confirmation
2. **Caller classification lag**: C7:C475/C487/C4AB show code structure but classified as "suspect" because they sit in regions marked as data
3. **No STRONG anchors yet**: All callers still weak/suspect in the anchor reports

**Progress:**
- ✅ C7:C3xx-C7:C4xx confirmed as real code (prologues, returns, cross-bank calls)
- ✅ Direct calls from C7:C3xx to C7:B0xx verified
- ⚠️ Caller chain needs formal promotion before B100 can be validated

---

## Strategic implications

### The C7 code discovery

**First confirmed real code in upper C7 bank** (above C3 threshold):
- C7:C300-C7:C4xx contains executable functions
- Cross-bank activity (10 banks call into this region)
- This validates the hypothesis that C7 bank contains code above C3

### Path to C7:B100 promotion

**Required steps:**
1. **Promote C7:C300-C7:C4xx as code** (strong structural evidence)
2. **Re-run anchor reports** for C7:B100 targets (callers will be "strong" once C3xx is promoted)
3. **Promote C7:B100** once callers are validated

**Alternative:**
- Continue linear progression (C7:B200..) to find entry points
- Backfill C7:C300 validation once anchor chain is complete

### 170-page streak status

The streak **C7:0000..C7:A7FF as data** remains intact.

C7:C300+ represents **new code territory** not yet in closed ranges.

---

## Block read

- **Strategic jump successful**: C7:C300-C7:C4xx confirmed as **real code** with prologues, returns, and cross-bank call activity. This is the first confirmed code in upper C7 bank.

- **Circular dependency identified**: C7:B100 needs strong callers; C7:C3xx callers show code structure but need formal promotion before they can validate B100.

- **Direct calls verified**: C7:C475→B0B4, C7:C487→B0DF, C7:C4AB→B0F2, C7:C331→B09E. The caller chain exists but needs formal validation.

- **Cross-bank activity**: C7:C3xx-C7:C4xx is called from 10 different banks, indicating this is significant shared code, not local utilities.

- **Promotion blocked by classification lag**: C7:C475/C487/C4AB show code indicators (prologues, returns) but are classified as "suspect" because they sit in data-flagged regions. Formal promotion of C3xx region is needed.

- **Strategic recommendation**: Process C7:C300..C7:C4FF for promotion first, then use those as strong anchors for C7:B100 validation.

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
- C7:A800..C7:B1FF: 0 promotions (notes_76)
- C7:C300..C7:CCFF: 0 promotions (this note)

Total promotions since seam work began: **0**

---

## Files generated for this block

- `reports/c7_c300_ccff_seam_block.json`
- `reports/c7_c300_ccff_seam_block.md`
- `reports/c7_c300_c3ff_backtrack.json`
- `reports/c7_c400_c4ff_backtrack.json`
- `reports/C7_B111_anchor_v2.json`
- `reports/C7_B188_anchor_v2.json`

---

## Strategic decision point

### Current state

**Seam:** C7:B200 (unchanged - strategic jump, not linear progression)
**Discovery:** C7:C300-C7:C4xx is **real code**
**Blocker:** Circular dependency (B100 needs C3xx promotion; C3xx needs formal validation)

### Options

**Option A: Promote C7:C300-C7:C4xx now**
- Strong structural evidence (prologues, returns, cross-bank calls)
- Would provide strong anchors for C7:B100
- Risk: Promoting without full block analysis

**Option B: Return to linear progression (C7:B200..)**
- Find entry points leading to C3xx
- Build anchor chain naturally
- Lower risk, slower progress

**Option C: Process C7:C200..C7:C2FF (gap region)**
- Analyze the skipped region
- May contain entry points to C3xx
- Bridge the gap in coverage

### Recommendation

**Option A (promote C7:C300-C7:C4xx)** is justified because:
1. Definitive code indicators (returns, prologues)
2. Cross-bank call activity confirms significance
3. Direct callers to B100 region identified
4. Structural evidence stronger than most promoted code in project

### Next steps

If promoting C7:C300-C7:C4xx:
1. Create pass manifest for C7:C300..C7:C4FF as code
2. Update closed ranges snapshot
3. Re-run anchor reports for C7:B100
4. Promote C7:B100 if callers now "strong"

If continuing linear:
1. `python tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:B200 --pages 10 --json > reports/c7_b200_bbff_seam_block.json`
2. Process normally

Write `docs/sessions/chrono_trigger_session15_continue_notes_78.md`
