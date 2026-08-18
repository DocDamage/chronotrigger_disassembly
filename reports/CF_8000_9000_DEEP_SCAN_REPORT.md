# Bank CF:8000-9000 Deep Scan Report

**Date:** 2026-04-08  
**Status:** COMPLETE - Deep Analysis  
**Region:** CF:8000..CF:9000 + Full Bank CF Backtrack Analysis  

---

## Executive Summary

Bank CF is a **major unexplored code bank** with significant function density in the upper half (CF:8000-FFFF). The CF:8000-9000 region, while initially flagged as a "dispatch table" with score 134, shows **17 primary entry points** with moderate caller density. The true high-density code regions are in **CF:E000-FFFF** with 69+ score-6+ clusters.

---

## CF:8000-9000 Region Analysis (Original Target)

### Seam Block Scan Results (16 pages)

| Page Range | Page Family | Review Posture |
|------------|-------------|----------------|
| CF:8000-80FF | text_ascii_heavy | bad_start_or_dead_lane_reject |
| CF:8100-81FF | text_ascii_heavy | local_control_only |
| CF:8200-82FF | text_ascii_heavy | mixed_lane_continue |
| CF:8300-83FF | text_ascii_heavy | mixed_lane_continue |
| CF:8400-84FF | text_ascii_heavy | local_control_only |
| CF:8500-85FF | text_ascii_heavy | mixed_lane_continue |
| CF:8600-86FF | text_ascii_heavy | local_control_only |
| CF:8700-87FF | mixed_command_data | mixed_lane_continue |
| CF:8800-88FF | text_ascii_heavy | local_control_only |
| CF:8900-89FF | text_ascii_heavy | local_control_only |
| CF:8A00-8AFF | text_ascii_heavy | manual_owner_boundary_review |
| CF:8B00-8BFF | text_ascii_heavy | mixed_lane_continue |
| CF:8C00-8CFF | text_ascii_heavy | local_control_only |
| CF:8D00-8DFF | text_ascii_heavy | local_control_only |
| CF:8E00-8EFF | text_ascii_heavy | local_control_only |
| CF:8F00-8FFF | text_ascii_heavy | local_control_only |

**Page Family Summary:**
- text_ascii_heavy: 15 pages
- mixed_command_data: 1 page

**Review Posture Summary:**
- local_control_only: 9 pages
- mixed_lane_continue: 5 pages
- manual_owner_boundary_review: 1 page
- bad_start_or_dead_lane_reject: 1 page

### Raw XRef Context Analysis

| Metric | Count |
|--------|-------|
| Total Hits | 17 |
| Hard Bad Start Suppressed | 1 (CF:8000) |
| Valid Entry Points | 16 |
| Cross-Bank (JML/JSL) | 1 (CA:1C69 → CF:8AC1) |

**Entry Points Found:**
- CF:80A9 (4 same-bank JSR callers: CF:E43E, CF:E470, CF:E550, CF:E582)
- CF:80D8 (1 JSR caller: CF:4FFA)
- CF:80E0 (2 JSR callers: CF:78D4, CF:7F8C)
- CF:827F (1 JMP caller: CF:74EB)
- CF:837C (1 JSR caller: CF:4ECF)
- CF:83FF (1 JMP caller: CF:1EE9)
- CF:846B (1 JMP caller: CF:9282)
- CF:8500 (1 JSR caller: CF:E69E)
- CF:850A (1 JSR caller: CF:E677)
- CF:8AC1 (1 JML cross-bank: CA:1C69)
- CF:8BAD (1 JSR caller: CF:E633)
- CF:8DAC (1 JMP caller: CF:FA48)

### Backtrack Analysis Results

| Candidate | Best Start | Score | Distance | Start Byte | Type |
|-----------|------------|-------|----------|------------|------|
| CF:80A9 | CF:804F | 4 | 90 | 20 | JSR prologue |
| CF:80D8 | CF:8059 | 4 | 127 | 20 | JSR prologue |
| CF:80E0 | CF:8061 | 4 | 127 | 20 | JSR prologue |
| CF:827F | CF:81FF | 4 | 128 | 20 | JSR prologue |
| CF:83FF | CF:839B | 4 | 100 | 22 | JSL prologue |
| CF:8500 | CF:84CF | 4 | 49 | 20 | JSR prologue |
| CF:850A | CF:84CF | 4 | 59 | 20 | JSR prologue |
| CF:8AC1 | CF:8ABA | 4 | 7 | 48 | PHA prologue |
| CF:837C | CF:8353 | 2 | 41 | 22 | JSL prologue |
| CF:846B | CF:83EB | 2 | 128 | 22 | JSL prologue |
| CF:8BAD | CF:8B39 | 2 | 116 | 20 | JSR prologue |
| CF:8DAC | CF:8D9E | 2 | 14 | 08 | PHP prologue |
| CF:8000 | CF:8000 | -6 | 0 | 00 | BRK (bad start) |

**Note:** No score-6+ clusters found in CF:8000-9000. Highest score is 4.

---

## Full Bank CF Score-6+ Analysis

### CF:9000-A000 (11 candidates, max score 4)

| Candidate | Best Start | Score | Distance | Start Byte |
|-----------|------------|-------|----------|------------|
| CF:90A9 | CF:9037 | 4 | 114 | 20 |
| CF:90BF | CF:9041 | 4 | 126 | 20 |
| CF:91F8 | CF:91EC | 4 | 12 | 5A |
| CF:929E | CF:9271 | 4 | 45 | 20 |
| CF:95F8 | CF:95AF | 4 | 73 | 20 |
| CF:9604 | CF:95AF | 4 | 85 | 20 |
| CF:998D | CF:9915 | 4 | 120 | 20 |
| CF:99A9 | CF:9932 | 4 | 119 | 48 |

### CF:A000-B000 (46 candidates, 1 score-6)

| Candidate | Best Start | Score | Distance | Start Byte |
|-----------|------------|-------|----------|------------|
| **CF:A31C** | **CF:A2B4** | **6** | 104 | 8B |
| CF:A0FF | CF:A0DD | 4 | 34 | 20 |
| CF:A163 | CF:A151 | 4 | 18 | 20 |
| CF:A17F | CF:A170 | 4 | 15 | 48 |
| CF:A1C5 | CF:A170 | 4 | 85 | 48 |
| CF:A286 | CF:A209 | 4 | 125 | 20 |
| CF:A3B7 | CF:A39B | 4 | 28 | 22 |
| CF:A433 | CF:A3E9 | 4 | 74 | 22 |
| CF:A43B | CF:A3E9 | 4 | 82 | 22 |
| CF:A471 | CF:A3F1 | 4 | 128 | 22 |
| CF:A61B | CF:A617 | 4 | 4 | 20 |
| CF:A69D | CF:A672 | 4 | 43 | 4B |
| CF:A771 | CF:A75B | 4 | 22 | 22 |
| CF:A9F4 | CF:A979 | 4 | 123 | 20 |
| CF:AA0A | CF:A991 | 4 | 121 | 20 |
| CF:AB4C | CF:AB4B | 4 | 1 | 20 |
| CF:AB6E | CF:AB4B | 4 | 35 | 20 |

### CF:B000-C000 (21 candidates, max score 4)

| Candidate | Best Start | Score | Distance | Start Byte |
|-----------|------------|-------|----------|------------|
| CF:B223 | CF:B215 | 4 | 14 | 20 |
| CF:B499 | CF:B48C | 4 | 13 | 48 |
| CF:B548 | CF:B4CD | 4 | 123 | 20 |
| CF:B54C | CF:B4CD | 4 | 127 | 20 |
| CF:B6FC | CF:B6EF | 4 | 13 | 20 |
| CF:B8B5 | CF:B89F | 4 | 22 | 20 |
| CF:B8E0 | CF:B89F | 4 | 65 | 20 |
| CF:BB28 | CF:BB24 | 4 | 4 | 0B |

### CF:C000-D000 (14 candidates, 5 score-6)

| Candidate | Best Start | Score | Distance | Start Byte |
|-----------|------------|-------|----------|------------|
| **CF:C0C0** | **CF:C06D** | **6** | 83 | 20 |
| **CF:C0E0** | **CF:C06D** | **6** | 115 | 20 |
| **CF:C6A5** | **CF:C637** | **6** | 110 | 20 |
| **CF:C6A6** | **CF:C637** | **6** | 111 | 20 |
| **CF:CF16** | **CF:CEA1** | **6** | 117 | 20 |
| CF:CAA4 | CF:CA9B | 4 | 9 | 20 |
| CF:CFEE | CF:CFEB | 4 | 3 | 20 |

### CF:D000-E000 (7 candidates, max score 4)

| Candidate | Best Start | Score | Distance | Start Byte | Caller |
|-----------|------------|-------|----------|------------|--------|
| CF:DC0F | CF:DBD1 | 4 | 62 | 20 | C9:71FB (JSL) |
| CF:DCAE | CF:DCA2 | 4 | 12 | 45 | FD:3331 (JSL) |
| CF:DCC9 | CF:DCBF | 4 | 10 | 20 | C8:8DA7 (JSL) |
| CF:D3AD | CF:D397 | 2 | 22 | 20 | CF:E66D (JSR) |
| CF:D7B5 | CF:D78F | 2 | 38 | 20 | CF:CCBE (JMP) |
| CF:DA2F | CF:D9ED | 2 | 66 | 20 | C7:E005 (JSL) |
| CF:DFA6 | CF:DF75 | 2 | 49 | 20 | FF:0C31 (JML) |

**Cross-Bank Activity in D000-E000:**
- C7:E005 → CF:DA2F (JSL)
- C9:71FB → CF:DC0F (JSL)
- FD:3331 → CF:DCAE (JSL)
- C8:8DA7 → CF:DCC9 (JSL)
- FF:0C31 → CF:DFA6 (JML)

### CF:E000-F000 (53 candidates, 16 score-6) - **RICHEST REGION**

| Candidate | Best Start | Score | Distance | Start Byte |
|-----------|------------|-------|----------|------------|
| **CF:E781** | **CF:E777** | **6** | 10 | A0 |
| **CF:E7D7** | **CF:E7D4** | **6** | 3 | 5A |
| **CF:E83A** | **CF:E837** | **6** | 3 | C2 |
| **CF:E906** | **CF:E8F1** | **6** | 21 | 20 |
| **CF:E926** | **CF:E8F1** | **6** | 53 | 20 |
| **CF:E99C** | **CF:E94D** | **6** | 79 | 20 |
| **CF:EAC5** | **CF:EAC3** | **6** | 2 | 20 |
| **CF:ECEB** | **CF:ECE0** | **6** | 11 | A2 |
| **CF:ED18** | **CF:ECE0** | **6** | 56 | A2 |
| **CF:EDB8** | **CF:EDB5** | **6** | 3 | C2 |
| **CF:EE9A** | **CF:EE99** | **6** | 1 | A0 |
| **CF:EE9F** | **CF:EE9C** | **6** | 3 | 5A |
| **CF:EEFF** | **CF:EEFD** | **6** | 2 | C2 |
| **CF:EFA9** | **CF:EF9D** | **6** | 12 | C2 |
| **CF:EFAF** | **CF:EFAC** | **6** | 3 | DA |
| CF:ECC2 | CF:ECC2 | 5 | 0 | A2 |
| CF:EEEB | CF:EEEB | 5 | 0 | A0 |

### CF:F000-FF00 (36 candidates, 29 score-6) - **HIGHEST DENSITY**

| Candidate | Best Start | Score | Distance | Start Byte |
|-----------|------------|-------|----------|------------|
| **CF:F01F** | **CF:F003** | **6** | 28 | A2 |
| **CF:F06F** | **CF:F003** | **6** | 108 | A2 |
| **CF:F18B** | **CF:F18A** | **6** | 1 | 08 |
| **CF:F193** | **CF:F18A** | **6** | 9 | 08 |
| **CF:F3BA** | **CF:F39F** | **6** | 27 | 20 |
| **CF:F423** | **CF:F3F2** | **6** | 49 | 20 |
| **CF:F522** | **CF:F4C0** | **6** | 98 | C2 |
| **CF:F530** | **CF:F4C0** | **6** | 112 | C2 |
| **CF:F548** | **CF:F4D1** | **6** | 119 | A9 |
| **CF:F54C** | **CF:F4D1** | **6** | 123 | A9 |
| **CF:F619** | **CF:F59A** | **6** | 127 | A9 |
| **CF:F61E** | **CF:F5A0** | **6** | 126 | A9 |
| **CF:F957** | **CF:F940** | **6** | 23 | C2 |
| **CF:F9D3** | **CF:F99C** | **6** | 55 | 08 |
| **CF:FA43** | **CF:FA3E** | **6** | 5 | 20 |
| **CF:FADD** | **CF:FAB9** | **6** | 36 | A9 |
| **CF:FAE2** | **CF:FAB9** | **6** | 41 | A9 |
| **CF:FB02** | **CF:FAE7** | **6** | 27 | A0 |
| **CF:FB65** | **CF:FB63** | **6** | 2 | A0 |
| **CF:FCF6** | **CF:FCEF** | **6** | 7 | C2 |
| **CF:FCFB** | **CF:FCEF** | **6** | 12 | C2 |
| **CF:FD02** | **CF:FCEF** | **6** | 19 | C2 |
| **CF:FD22** | **CF:FD1D** | **6** | 5 | A9 |
| **CF:FD36** | **CF:FD1D** | **6** | 25 | A9 |
| **CF:FD6A** | **CF:FD51** | **6** | 25 | A9 |
| **CF:FD9E** | **CF:FD85** | **6** | 25 | A9 |
| **CF:FDA9** | **CF:FD85** | **6** | 36 | A9 |
| **CF:FDAD** | **CF:FD85** | **6** | 40 | A9 |
| **CF:FE20** | **CF:FDFB** | **6** | 37 | DA |

---

## Cross-Bank Caller Validation

### True Cross-Bank Calls (JSL/JML from other banks to CF)

| Target | Caller | Kind | Validity |
|--------|--------|------|----------|
| CF:8AC1 | CA:1C69 | JML | Valid |
| CF:DA2F | C7:E005 | JSL | Valid |
| CF:DC0F | C9:71FB | JSL | Valid |
| CF:DCAE | FD:3331 | JSL | Valid |
| CF:DCC9 | C8:8DA7 | JSL | Valid |
| CF:DFA6 | FF:0C31 | JML | Valid |

### Same-Bank Callers (Internal CF)

Most high-score candidates in CF:E000-FFFF are called from within bank CF itself (same-bank JSR/JMP). These represent internal function organization rather than cross-bank dispatch.

---

## Dispatch Table Analysis

### CF:8000-9000 Assessment

The original "score 134" for CF:8000-9000 appears to have been calculated from aggregate instruction counts (208 JSR + 84 JSL within the region), not actual unique entry points. The deep scan reveals:

- **17 unique entry points** in CF:8000-9000
- Only **1 true cross-bank call** (CA:1C69 → CF:8AC1 via JML)
- Most calls are **same-bank internal** calls from unresolved CF regions
- **No score-6+ clusters** in this region

### High-Score Cluster Regions

| Region | Score-6+ Count | Best Region |
|--------|----------------|-------------|
| CF:8000-9000 | 0 | Max score 4 |
| CF:9000-A000 | 0 | Max score 4 |
| CF:A000-B000 | 1 | CF:A31C (score 6) |
| CF:B000-C000 | 0 | Max score 4 |
| CF:C000-D000 | 5 | Multiple score-6 |
| CF:D000-E000 | 0 | Max score 4 (but 5 cross-bank JSL/JML) |
| **CF:E000-F000** | **16** | **Richest region** |
| **CF:F000-FF00** | **29** | **Highest density** |

---

## Recommended New Manifests (Pass 716+)

### Priority 1: Score-6+ Clusters (18 manifests)

```yaml
# CF:A000-B000 (1 manifest)
716: CF:A2B4..CF:A31C  # score 6, LDY# prologue

# CF:C000-D000 (5 manifests)
717: CF:C06D..CF:C0C0  # score 6
718: CF:C06D..CF:C0E0  # score 6
719: CF:C637..CF:C6A5  # score 6
720: CF:C637..CF:C6A6  # score 6
721: CF:CEA1..CF:CF16  # score 6

# CF:E000-F000 (16 manifests - select top)
722: CF:E777..CF:E781  # score 6, LDY# prologue
723: CF:E8F1..CF:E906  # score 6, JSR prologue
724: CF:E8F1..CF:E926  # score 6, JSR prologue
725: CF:ECE0..CF:ECEB  # score 6, LDX# prologue
726: CF:ECE0..CF:ED18  # score 6, LDX# prologue
727: CF:F003..CF:F01F  # score 6, LDX# prologue
728: CF:F4C0..CF:F522  # score 6, REP prologue
729: CF:F4D1..CF:F548  # score 6, LDA# prologue
```

### Priority 2: Cross-Bank Entry Points (6 manifests)

```yaml
# True cross-bank targets with external JSL/JML callers
730: CF:8AB0..CF:8AC1  # CA:1C69 (JML)
731: CF:D9E0..CF:DA2F  # C7:E005 (JSL)
732: CF:DBD0..CF:DC0F  # C9:71FB (JSL)
733: CF:DCA0..CF:DCAE  # FD:3331 (JSL)
734: CF:DCB0..CF:DCC9  # C8:8DA7 (JSL)
735: CF:DF70..CF:DFA6  # FF:0C31 (JML)
```

### Priority 3: Score-4 Clusters in CF:8000-9000 (8 manifests)

```yaml
# CF:8000-9000 score-4 candidates
736: CF:804F..CF:80A9  # score 4
737: CF:84CF..CF:8500  # score 4
738: CF:84CF..CF:850A  # score 4
739: CF:8ABA..CF:8AC1  # score 4, cross-bank target
```

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| **Total Score-6+ Clusters** | **51** |
| **CF:8000-9000 Entry Points** | 17 |
| **CF:8000-9000 Score-6+** | 0 |
| **True Cross-Bank Callers** | 6 |
| **Same-Bank Internal Calls** | 200+ |
| **Recommended New Manifests** | 18+ |

---

## Key Findings

1. **CF:8000-9000 is NOT a traditional dispatch table** - it has only 17 entry points with max score 4
2. **CF:E000-FFFF is the major code region** - 45 score-6+ clusters identified
3. **Cross-bank activity is concentrated in CF:D000-E000** - 5 JSL/JML from banks C7, C8, C9, FD, FF
4. **Most CF code is internally organized** - same-bank JSR/JMP calls dominate
5. **Bank CF is a major new code bank** - 51+ score-6+ clusters need documentation

---

## Next Steps

1. Create manifests for the 18 priority score-6+ clusters
2. Document cross-bank entry points first (external API surface)
3. Focus on CF:E000-FFFF (highest function density)
4. Run full seam flow analysis on CF:E000-F000 and CF:F000-FF00
5. Investigate calling patterns from banks C7, C8, C9, FD, FF
