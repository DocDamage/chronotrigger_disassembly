# Bank C3 Gap Analysis Report

## Analysis Date: 2026-04-08

## Target Gaps
1. **C3:2900-C3:3058** (1881 bytes, ~7.3 pages)
2. **C3:30B1-C3:34FF** (1103 bytes, ~4.3 pages)
3. **C3:3761-C3:3C7F** (1311 bytes, ~5.1 pages)

---

## Summary of Findings

### Overall Statistics
- Total gap bytes analyzed: 4,295 bytes
- Page family classification: `branch_fed_control_pocket` (all gaps)
- Reasons: branch_dense, return_anchored
- **High-score candidates found: 6 with score >= 6**
- Additional score-4 candidates: 23+ (potential secondary targets)

### Gap Content Analysis
All three gaps are classified as `branch_fed_control_pocket`, indicating:
- High branch instruction density (~9-11%)
- Return-anchored code structures
- Control flow oriented (conditionals, loops)
- Likely event handling or UI logic

---

## Score-6 Candidate Functions (Recommended for Promotion)

### Gap 1: C3:2900-C3:3058

#### Candidate C3:2E31 (Score-6)
- **Range**: C3:2E31..C3:2E55
- **Target entry**: C3:2E3D
- **Start byte**: $0B (PHD - Push Direct Page Register)
- **Evidence**:
  - Clean prologue: PHD instruction ($0B)
  - Distance to target: 12 bytes
  - Contains RTS at C3:2E3A
  - Local island cluster score: 5 (C3:2E6B..C3:2E87)
- **ROM Bytes**: `0B 20 74 20 ...` (PHD, JSR, etc.)
- **Status**: ✅ Strong candidate for promotion

---

### Gap 2: C3:30B1-C3:34FF

#### Candidate C3:3217 (Score-6)
- **Range**: C3:3217..C3:3234
- **Target entry**: C3:321C
- **Start byte**: $08 (PHP - Push Processor Status)
- **Evidence**:
  - Clean prologue: PHP instruction ($08)
  - Distance to target: 5 bytes
  - PPU register writes ($2120, $210D)
  - Likely video/graphics setup function
- **ROM Bytes**: `08 8D 20 21 A9 09 ...` (PHP, STA $2120, LDA #$09...)
- **Status**: ✅ Strong candidate for promotion

#### Candidate C3:3280 (Score-6)
- **Range**: C3:3280..C3:329A
- **Target entry**: C3:3282
- **Start byte**: $08 (PHP - Push Processor Status)
- **Evidence**:
  - Clean prologue: PHP instruction ($08)
  - Distance to target: 2 bytes
  - Contains RTL at C3:328D
  - JSR $2000 followed by JSL $003000
- **ROM Bytes**: `08 41 CE 08 0A 00 ...` (PHP, various ops)
- **Status**: ✅ Strong candidate for promotion

#### Candidate C3:34CE (Score-6)
- **Range**: C3:34CE..C3:34EB
- **Target entry**: C3:34D3
- **Start byte**: $20 (JSR - Jump to Subroutine)
- **Evidence**:
  - Starts with JSR instruction
  - Distance to target: 5 bytes
  - Contains RTS at C3:34DC
  - References data at $9E4E
- **ROM Bytes**: `20 3C 5E A2 4E 9E ...` (JSR $5E3C, LDX #$4E...)
- **Status**: ⚠️ Good candidate but starts with JSR not PHP

---

### Gap 3: C3:3761-C3:3C7F

#### Candidate C3:387B (Score-6)
- **Range**: C3:387B..C3:38A3
- **Target entry**: C3:388B
- **Start byte**: $20 (JSR - Jump to Subroutine)
- **Evidence**:
  - Starts with JSR instruction
  - Distance to target: 16 bytes
  - Contains REP #$21 (16-bit mode switch)
  - JMP $5420 instruction present
- **ROM Bytes**: `20 1B BC 0E B2 0C ...` (JSR $BC1B, ASL...)
- **Status**: ⚠️ Good candidate but starts with JSR not PHP

#### Candidate C3:3C5B (Score-6)
- **Range**: C3:3C5B..C3:3C76
- **Target entry**: C3:3C5E
- **Start byte**: $A2 (LDX - Load X Register)
- **Evidence**:
  - Starts with LDX #$40 (immediate load)
  - Distance to target: 3 bytes
  - Contains RTS at C3:3C70
  - JMP $39B1 (local jump)
- **ROM Bytes**: `A2 40 00 8E 01 1E ...` (LDX #$0040, STX...)
- **Status**: ⚠️ Good candidate but starts with LDX not PHP

---

## Secondary Candidates (Score-4, Review Recommended)

### From Gap C3:2900-C3:3058:
| Candidate | Target | Start Byte | Notes |
|-----------|--------|------------|-------|
| C3:291F | C3:2920 | $08 (PHP) | Clean prologue |
| C3:297D | C3:298D | $0B (PHD) | Direct page push |
| C3:2A3D | C3:2A40 | $A6 (LDX) | Variable load |
| C3:2ADD | C3:2AE0 | $48 (PHA) | Accumulator push |
| C3:2C08 | C3:2C09 | $20 (JSR) | Subroutine call |
| C3:2CA5 | C3:2CC1 | $A9 (LDA) | Immediate load |

### From Gap C3:30B1-C3:34FF:
| Candidate | Target | Start Byte | Notes |
|-----------|--------|------------|-------|
| C3:316D | C3:3170 | $55 (EOR) | Arithmetic op |
| C3:31ED | C3:3200 | $08 (PHP) | Clean prologue |

### From Gap C3:3761-C3:3C7F:
| Candidate | Target | Start Byte | Notes |
|-----------|--------|------------|-------|
| C3:37FC | C3:3800 | $C0 (CPY) | Compare op |
| C3:383B | C3:3843 | $22 (JSL) | Long subroutine call |

---

## Analysis: Why These Gaps Exist

### Page Family: `branch_fed_control_pocket`
All three gaps share this classification, indicating they contain:

1. **Control Flow Logic**: High density of branch instructions (BRA, BCC, BCS, BEQ, BNE)
2. **Return-Anchored**: Functions ending in RTS/RTL
3. **Event/State Handling**: The branch_fed pattern suggests state machines or event handlers

### Likely Purposes:
- **C3:2900-C3:3058**: ~7.3 pages of UI/graphics helper functions
- **C3:30B1-C3:34FF**: ~4.3 pages of video/PPU control functions
- **C3:3761-C3:3C7F**: ~5.1 pages of gameplay/state logic

### Tiny Veneers Found:
- 30 veneers in gap 2900-3058
- 17 veneers in gap 30B1-34FF
- 10 veneers in gap 3761-3C7F

These veneers (bra_landing_pad, rtl_stub, jsr_rts_wrapper) indicate:
- Compiler-generated jump tables
- Alignment padding
- Wrapper functions for cross-bank calls

---

## Recommended Manifests for Promotion

### Priority 1: Score-6 with Clean Prologues (PHP/PHD)

```asm
; C3:2E31..C3:2E55 - Score-6, PHD prologue
ct_c3_function_2e31_phd_prologue_score6:
    EQU $C32E31

; C3:3217..C3:3234 - Score-6, PHP prologue, PPU registers
ct_c3_ppu_setup_function_3217_score6:
    EQU $C33217

; C3:3280..C3:329A - Score-6, PHP prologue, RTL return
ct_c3_function_3280_php_rtl_score6:
    EQU $C33280
```

### Priority 2: Score-6 with JSR Prologues

```asm
; C3:34CE..C3:34EB - Score-6, JSR start, data references
ct_c3_data_handler_34ce_score6:
    EQU $C334CE

; C3:387B..C3:38A3 - Score-6, JSR start, 16-bit ops
ct_c3_wide_math_function_387b_score6:
    EQU $C3387B

; C3:3C5B..C3:3C76 - Score-6, LDX prologue
ct_c3_indexed_function_3c5b_score6:
    EQU $C33C5B
```

### Priority 3: Score-4 with Clean Prologues (Review First)

```asm
; C3:291F..C3:2938 - Score-4, PHP prologue
ct_c3_function_291f_score4:
    EQU $C3291F

; C3:297D..C3:29A5 - Score-4, PHD prologue
ct_c3_function_297d_score4:
    EQU $C3297D

; C3:31ED..C3:3200 - Score-4, PHP prologue
ct_c3_function_31ed_score4:
    EQU $C331ED
```

---

## Verification Recommendations

1. **Manual Disassembly**: Use a full 65816 disassembler on these regions
2. **XRef Analysis**: Check if any callers exist (may be table-driven)
3. **Pattern Matching**: Look for common function epilogues (RTS, RTL)
4. **Data Reference**: Check for pointers to these regions in ROM tables

---

## Conclusion

- **6 high-confidence candidates** identified with score >= 6
- **3 candidates have clean prologues** (PHP/PHD) - prioritize these
- **All gaps are code regions**, not data tables
- **Estimated new coverage**: ~450-500 bytes of documented functions
- **Remaining gap bytes**: ~3,800 bytes still to analyze (mostly control flow veneers)

Next steps:
1. Promote the 3 PHP/PHD score-6 candidates
2. Verify boundaries with manual disassembly
3. Continue analysis on remaining score-4 candidates
4. Document tiny veneers as helper functions
