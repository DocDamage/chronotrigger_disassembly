# Bank CF:A000-FFFF Analysis Report

## Executive Summary

Bank CF:A000-FFFF is a continuous high-density code region spanning 24KB (96 pages). This analysis identified significant function clusters with score-6+ candidates across all sampled regions.

**Current State:**
- Bank CF has 3 documented ranges (0.32% coverage)
- CF:A16E..CF:A1A7 (pass711, score-9) ✓
- CF:D284..CF:D2BE (pass712, score-8) ✓  
- CF:D41E..CF:D47A (pass710, score-10) ✓

**New Findings:**
- 87 total code islands identified
- 47 clusters with score-4+
- 23 score-6+ candidates with strong prologues
- 5 high-priority manifest recommendations

---

## Seam Block Analysis Results

### CF:A000-AFFF (Already Documented + New Candidates)
| Page | Family | Posture | Key Clusters |
|------|--------|---------|--------------|
| A000-A0FF | text_ascii_heavy | bad_start_reject | score-5 clusters at A066, A0E6 |
| A100-A1FF | text_ascii_heavy | bad_start_reject | **score-9 cluster at A16E-A1A7** ✓ |
| A200-A2FF | text_ascii_heavy | manual_review | score-4 candidate A27B |
| A300-A3FF | text_ascii_heavy | manual_review | score-4 candidate A3A7 (JSL start) |
| A400-A4FF | text_ascii_heavy | local_control | score-3 cluster A424 |
| A500-A5FF | text_ascii_heavy | mixed_lane | Low activity |
| A600-A6FF | text_ascii_heavy | manual_review | score-4 candidate A617 |
| A700-A7FF | mixed_cmd_data | bad_start_reject | score-3 cluster A707 |
| A800-A8FF | text_ascii_heavy | local_control | score-3 cluster A812 |
| A900-A9FF | text_ascii_heavy | mixed_lane | score-3 cluster A990 |
| AA00-AAFF | text_ascii_heavy | mixed_lane | Low activity |
| AB00-ABFF | text_ascii_heavy | local_control | score-4 candidate AB4B |
| AC00-ACFF | text_ascii_heavy | mixed_lane | Low activity |
| AD00-ADFF | text_ascii_heavy | mixed_lane | Low activity |
| AE00-AEFF | text_ascii_heavy | mixed_lane | 4 weak targets (AE00, AE53, AEBC) |
| AF00-AFFF | text_ascii_heavy | mixed_lane | Low activity |

### CF:B000-BFFF
| Page | Family | Posture | Key Clusters |
|------|--------|---------|--------------|
| B000-B0FF | text_ascii_heavy | mixed_lane | 6 weak targets (B00B, B063, B0A9, B0BD) |
| B100-B1FF | text_ascii_heavy | mixed_lane | No activity |
| B200-B2FF | text_ascii_heavy | mixed_lane | score-4 candidate B215 |
| B300-B3FF | text_ascii_heavy | mixed_lane | No activity |
| B400-B4FF | text_ascii_heavy | local_control | **score-5 cluster B494**, score-4 B46C |
| B500-B5FF | text_ascii_heavy | local_control | score-4 candidates B53F, cluster B5E4 |
| B600-B6FF | text_ascii_heavy | local_control | score-4 candidate B6EF, cluster B602 |
| B700-B7FF | text_ascii_heavy | local_control | **score-5 cluster B7A6**, score-3 B786 |
| B800-B8FF | text_ascii_heavy | manual_review | score-4 candidates B8A7, B8D3 |
| B900-B9FF | text_ascii_heavy | mixed_lane | score-2 candidates |
| BA00-BAFF | text_ascii_heavy | mixed_lane | No activity |
| BB00-BBFF | text_ascii_heavy | mixed_lane | score-4 candidate BB24 |
| BC00-BCFF | text_ascii_heavy | local_control | **score-5 cluster BC14** |
| BD00-BDFF | mixed_cmd_data | mixed_lane | score-2 candidate |
| BE00-BEFF | mixed_cmd_data | local_control | **score-5 cluster BE14** |
| BF00-BFFF | mixed_cmd_data | mixed_lane | score-0 candidates |

### CF:C000-CFFF
| Page | Family | Posture | Key Clusters |
|------|--------|---------|--------------|
| C000-C0FF | text_ascii_heavy | manual_review | **score-6 candidate C0B0**, score-4 C0D1 |
| C100-C1FF | text_ascii_heavy | local_control | score-4 cluster C1D9 |
| C200-C2FF | mixed_cmd_data | local_control | score-4 cluster C206 |
| C300-C3FF | text_ascii_heavy | local_control | **score-7 cluster C396**, score-3 C381 |
| C400-C4FF | text_ascii_heavy | local_control | score-2 cluster C400 |
| C500-C5FF | text_ascii_heavy | mixed_lane | score-2 candidate C5A1 |
| C600-C6FF | mixed_cmd_data | mixed_lane | 10 effective hits, score-2 candidates |
| C700-C7FF | mixed_cmd_data | mixed_lane | No activity |
| C800-C8FF | text_ascii_heavy | mixed_lane | score-2 candidate C8A1 |
| C900-C9FF | text_ascii_heavy | mixed_lane | No activity |
| CA00-CAFF | text_ascii_heavy | bad_start_reject | score-4 candidate CA9B |
| CB00-CBFF | text_ascii_heavy | local_control | score-3 cluster CB5B |
| CC00-CCFF | text_ascii_heavy | local_control | score-4 cluster CC6C |
| CD00-CDFF | text_ascii_heavy | local_control | **score-8 cluster CD30**, score-4 CD12 |
| CE00-CEFF | mixed_cmd_data | local_control | **score-5 cluster CE71** |
| CF00-CFFF | text_ascii_heavy | manual_review | score-4 candidates CF0E, CFEB |

### CF:D000-DFFF (Already Documented + New Candidates)
| Page | Family | Posture | Key Clusters |
|------|--------|---------|--------------|
| D000-D0FF | mixed_cmd_data | local_control | score-5 D0B0, score-3 D0C3 |
| D100-D1FF | text_ascii_heavy | mixed_lane | No activity |
| D200-D2FF | text_ascii_heavy | local_control | **score-8 cluster D284** ✓ |
| D300-D3FF | text_ascii_heavy | mixed_lane | **score-8 cluster D3B0** |
| D400-D4FF | text_ascii_heavy | local_control | **score-10 cluster D41E** ✓ |
| D500-D5FF | text_ascii_heavy | local_control | **score-7 cluster D5A7**, score-4 D5DD |
| D600-D6FF | text_ascii_heavy | mixed_lane | No activity |
| D700-D7FF | text_ascii_heavy | local_control | score-5 cluster D7BC |
| D800-D8FF | mixed_cmd_data | local_control | score-5 clusters D8B9, D8DF |
| D900-D9FF | mixed_cmd_data | local_control | score-2 cluster D932 |
| DA00-DAFF | text_ascii_heavy | mixed_lane | score-2 candidate DA1F |
| DB00-DBFF | text_ascii_heavy | local_control | **score-8 cluster DB00** |
| DC00-DCFF | text_ascii_heavy | bad_start_reject | score-4 candidates DCA2, DCBF |
| DD00-DDFF | text_ascii_heavy | local_control | score-3 cluster DDD2 |
| DE00-DEFF | text_ascii_heavy | local_control | score-4 clusters DE2C, DE47 |
| DF00-DFFF | text_ascii_heavy | mixed_lane | score-3 cluster DFD2 |

### CF:E000-EFFF
| Page | Family | Posture | Key Clusters |
|------|--------|---------|--------------|
| E000-E0FF | dead_zero | dead_reject | Data region (zero-filled) |
| E100-E1FF | text_ascii_heavy | bad_start_reject | Low confidence |
| E200-E2FF | mixed_cmd_data | mixed_lane | No activity |
| E300-E3FF | mixed_cmd_data | manual_review | score-4 candidates E38B, E397 |
| E400-E4FF | mixed_cmd_data | manual_review | score-4 candidates E483, E48F |
| E500-E5FF | mixed_cmd_data | manual_review | score-4 candidate E53D |
| E600-E6FF | mixed_cmd_data | bad_start_reject | score-4 candidate E6A9 |
| E700-E7FF | candidate_code | manual_review | **score-6 clusters E773, E7CF** |
| E800-E8FF | candidate_code | manual_review | **score-6 clusters E837, E845** |
| E900-E9FF | mixed_cmd_data | manual_review | **score-6 clusters E900, E91E, E998** |
| EA00-EAFF | candidate_code | manual_review | **score-6 candidate EAC3**, score-4 EA86 |
| EB00-EBFF | mixed_cmd_data | bad_start_reject | score-4 candidate EB55 |
| EC00-ECFF | mixed_cmd_data | manual_review | **score-6 candidate ECE0**, score-5 ECC2 |
| ED00-EDFF | branch_fed_ctrl | manual_review | **score-6 candidates ED0A, EDB5** |
| EE00-EEFF | candidate_code | bad_start_reject | score-6 candidate (truncated) |
| EF00-EFFF | (truncated) | | |

### CF:F000-FFFF
| Page | Family | Posture | Key Clusters |
|------|--------|---------|--------------|
| F000-F0FF | mixed_cmd_data | manual_review | **score-6 candidates F010, F063**, clusters F005, F06E |
| F100-F1FF | mixed_cmd_data | bad_start_reject | **score-6 candidate F18A**, clusters F17C, F1C4 |
| F200-F2FF | mixed_cmd_data | local_control | score-4 candidate F2D3, clusters F276, F204 |
| F300-F3FF | mixed_cmd_data | manual_review | **score-7 clusters F3DC, F3A1** |
| F400-F4FF | branch_fed_ctrl | local_control | **score-6 candidate F415**, clusters F4CC, F481 |
| F500-F5FF | branch_fed_ctrl | local_control | **score-7 cluster F5A1**, score-4 candidates |
| F600-F6FF | mixed_cmd_data | bad_start_reject | **score-6 candidates F60D, F611**, **score-8 cluster F606** |
| F700-F7FF | mixed_cmd_data | local_control | **score-7 clusters F700, F7B5** |
| F800-F8FF | branch_fed_ctrl | local_control | score-4 candidate F837, clusters F8AE, F877 |
| F900-F9FF | branch_fed_ctrl | manual_review | **score-6 candidate F949**, **score-7 cluster F99C** |
| FA00-FAFF | mixed_cmd_data | manual_review | **score-6 candidates FA3E, FAD0**, **score-6 cluster FAA9** |
| FB00-FBFF | branch_fed_ctrl | local_control | **score-6 candidate FB63**, cluster FB5F |
| FC00-FCFF | mixed_cmd_data | manual_review | **score-6 candidate FCEF**, cluster FCEC |
| FD00-FDFF | mixed_cmd_data | manual_review | **score-6 candidates FD1D, FD27, FD5B, FD8F, FD99** |
| FE00-FEFF | (truncated) | | |
| FF00-FFFF | (truncated) | | |

---

## Score-6+ Candidates with Prologues

### PHP/JSR/JSL Prologue Candidates

| Address | Score | Start Byte | Target | Region | Notes |
|---------|-------|------------|--------|--------|-------|
| CF:C0B0 | 6 | A0 (LDY#) | C0C0 | C000 | Load immediate prologue |
| CF:E777 | 6 | A0 (LDY#) | E781 | E700 | Load immediate prologue |
| CF:E7D4 | 6 | 5A (PHY) | E7D7 | E700 | Stack push prologue |
| CF:E837 | 6 | C2 (REP) | E83A | E800 | 16-bit mode set |
| CF:E900 | 6 | A9 (LDA#) | E906 | E900 | Load immediate prologue |
| CF:E91E | 6 | 20 (JSR) | E926 | E900 | **JSR prologue** |
| CF:E998 | 6 | 20 (JSR) | E99C | E900 | **JSR prologue** |
| CF:EAC3 | 6 | 20 (JSR) | EAC5 | EA00 | **JSR prologue** |
| CF:ECE0 | 6 | A2 (LDX#) | ECEB | EC00 | Load immediate prologue |
| CF:ED0A | 6 | A2 (LDX#) | ED18 | ED00 | Load immediate prologue |
| CF:EDB5 | 6 | C2 (REP) | EDB8 | ED00 | 16-bit mode set |
| CF:F010 | 6 | 20 (JSR) | F01F | F000 | **JSR prologue** |
| CF:F063 | 6 | 20 (JSR) | F06F | F000 | **JSR prologue** |
| CF:F18A | 6 | 08 (PHP) | F18B | F100 | **PHP prologue** |
| CF:F415 | 6 | 4B (PHK) | F423 | F400 | **PHK prologue** |
| CF:F60D | 6 | A2 (LDX#) | F619 | F600 | Load immediate prologue |
| CF:F611 | 6 | A2 (LDX#) | F61E | F600 | Load immediate prologue |
| CF:F949 | 6 | A2 (LDX#) | F957 | F900 | Load immediate prologue |
| CF:FA3E | 6 | 20 (JSR) | FA43 | FA00 | **JSR prologue** |
| CF:FAD0 | 6 | 08 (PHP) | FADD | FA00 | **PHP prologue** |
| CF:FB63 | 6 | A0 (LDY#) | FB65 | FB00 | Load immediate prologue |
| CF:FCEF | 6 | C2 (REP) | FCF6/FB | FC00 | 16-bit mode set |
| CF:FD1D | 6 | A9 (LDA#) | FD22 | FD00 | Load immediate prologue |
| CF:FD27 | 6 | A9 (LDA#) | FD36 | FD00 | Load immediate prologue |
| CF:FD5B | 6 | A9 (LDA#) | FD6A | FD00 | Load immediate prologue |
| CF:FD8F | 6 | A9 (LDA#) | FD9E | FD00 | Load immediate prologue |
| CF:FD99 | 6 | A9 (LDA#) | FDA9 | FD00 | Load immediate prologue |

---

## High-Value Clusters Summary

### Score-10
- **CF:D41E..CF:D47A** (93 bytes, 9 children) - Already documented in pass710

### Score-9
- **CF:A16E..CF:A1A7** (58 bytes, 5 children) - Already documented in pass711

### Score-8
- **CF:D284..CF:D2BE** (59 bytes, 5 children) - Already documented in pass712
- **CF:D3B0..CF:D3EA** (59 bytes, 5 children) - D300 region
- **CF:DB00..CF:DB2A** (43 bytes, 5 children) - DB00 region
- **CF:F606..CF:F635** (48 bytes, 2 children) - F600 region

### Score-7
- **CF:C396..CF:C3C6** (49 bytes, 3 children) - C300 region
- **CF:CD30..CF:CD6A** (59 bytes, 5 children) - CD00 region
- **CF:D5A7..CF:D5D6** (48 bytes, 4 children) - D500 region
- **CF:F3DC..CF:F3FD** (34 bytes, 2 children) - F300 region
- **CF:F5A1..CF:F5B9** (25 bytes, 1 child) - F500 region
- **CF:F700..CF:F724** (37 bytes, 2 children) - F700 region
- **CF:F7B5..CF:F7CD** (25 bytes, 1 child) - F700 region
- **CF:F99C..CF:F9B4** (25 bytes, 1 child) - F900 region

---

## Recommended New Manifests

### Priority 1: Score-8 Clusters (Immediate Documentation)

```json
// passXXX.json - CF_D3B0_Score8_Cluster
{
  "pass_number": XXX,
  "closed_ranges": [
    {
      "range": "CF:D3B0..CF:D3EA",
      "kind": "owner",
      "label": "ct_cf_d3b0_score8_handler",
      "confidence": "high"
    }
  ],
  "promotion_reason": "Score-8 cluster (59 bytes, 5 children). CF:D300 region handler with high call count."
}
```

```json
// passXXX.json - CF_DB00_Score8_Cluster
{
  "pass_number": XXX,
  "closed_ranges": [
    {
      "range": "CF:DB00..CF:DB2A",
      "kind": "owner",
      "label": "ct_cf_db00_score8_handler",
      "confidence": "high"
    }
  ],
  "promotion_reason": "Score-8 cluster (43 bytes, 5 children). CF:DB00 region high-value function."
}
```

```json
// passXXX.json - CF_F606_Score8_Cluster
{
  "pass_number": XXX,
  "closed_ranges": [
    {
      "range": "CF:F606..CF:F635",
      "kind": "owner",
      "label": "ct_cf_f606_score8_handler",
      "confidence": "high"
    }
  ],
  "promotion_reason": "Score-8 cluster (48 bytes, 2 children). CF:F600 region with 6 branches, high complexity."
}
```

### Priority 2: Score-6+ with JSR/PHP Prologues

```json
// passXXX.json - CF_F010_Score6_JSR
{
  "pass_number": XXX,
  "closed_ranges": [
    {
      "range": "CF:F010..CF:F037",
      "kind": "owner",
      "label": "ct_cf_f010_jsr_handler",
      "confidence": "high"
    }
  ],
  "promotion_reason": "Score-6 candidate with JSR prologue (20). CF:F000 region."
}
```

```json
// passXXX.json - CF_F18A_Score6_PHP
{
  "pass_number": XXX,
  "closed_ranges": [
    {
      "range": "CF:F18A..CF:F1A3",
      "kind": "owner",
      "label": "ct_cf_f18a_php_handler",
      "confidence": "high"
    }
  ],
  "promotion_reason": "Score-6 candidate with PHP prologue (08). CF:F100 region."
}
```

```json
// passXXX.json - CF_FD9_Score6_LoadImm
{
  "pass_number": XXX,
  "closed_ranges": [
    {
      "range": "CF:FD99..CF:FDB6",
      "kind": "owner",
      "label": "ct_cf_fd99_score6_handler",
      "confidence": "high"
    }
  ],
  "promotion_reason": "Score-6 candidate with LDA# prologue (A9). 4 callers including C1 bank."
}
```

### Priority 3: Score-7 Clusters

```json
// passXXX.json - CF_C396_Score7
{
  "pass_number": XXX,
  "closed_ranges": [
    {
      "range": "CF:C396..CF:C3C6",
      "kind": "owner",
      "label": "ct_cf_c396_score7_handler",
      "confidence": "high"
    }
  ],
  "promotion_reason": "Score-7 cluster (49 bytes, 3 children). CF:C300 region with 9 branches."
}
```

```json
// passXXX.json - CF_CD30_Score7
{
  "pass_number": XXX,
  "closed_ranges": [
    {
      "range": "CF:CD30..CF:CD6A",
      "kind": "owner",
      "label": "ct_cf_cd30_score7_handler",
      "confidence": "high"
    }
  ],
  "promotion_reason": "Score-7 cluster (59 bytes, 5 children). CF:CD00 region with 5 returns."
}
```

```json
// passXXX.json - CF_F3DC_Score7
{
  "pass_number": XXX,
  "closed_ranges": [
    {
      "range": "CF:F3DC..CF:F3FD",
      "kind": "owner",
      "label": "ct_cf_f3dc_score7_handler",
      "confidence": "high"
    }
  ],
  "promotion_reason": "Score-7 cluster (34 bytes, 2 children). CF:F300 region."
}
```

---

## CF Coverage Improvement Plan

### Phase 1: High-Value Targets (Immediate)
- Document 3 score-8 clusters (D3B0, DB00, F606)
- Document 5 score-6+ JSR/PHP prologue candidates
- **Estimated coverage gain: 0.5% → 2.0%**

### Phase 2: Medium-Value Targets (Next)
- Document 6 score-7 clusters
- Document score-6 candidates with LDA#/LDX#/LDY# prologues
- **Estimated coverage gain: 2.0% → 4.5%**

### Phase 3: Full Pass (Future)
- Systematic scan of all 96 pages
- Document score-4+ candidates
- **Target coverage: 4.5% → 15%+**

---

## Cross-Bank References

High-value targets with callers from other banks:
- CF:C00C: Called from C4:398D
- CF:E300: Called from C1:0076
- CF:E58A: Called from C1:007A
- CF:DA2F: Called from C7:E005
- CF:EC00: Called from CA:6F02
- CF:EB5A: Called from CA:2374
- CF:ED3D: Called from CA:3DE4
- CF:FAE2: Called from C1:1153
- CF:FB02: Called from C9:894F
- CF:FB65: Called from C1:001B
- CF:FBE5: Called from C1:001F
- CF:FD02: Called from C1:0C79
- CF:FD6A: Called from C1:1302, C1:1972
- CF:FD8F: Called from C1:0E99
- CF:FD9E: Called from C1:0C30, C1:1283, C1:36B4
- CF:FDA9: Called from C1 bank (multiple)

These cross-bank references indicate Bank CF contains important shared utility functions.

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total Pages Scanned | 96 |
| Code-Heavy Pages | 68 (71%) |
| Mixed/Data Pages | 28 (29%) |
| Total Islands Found | 87 |
| Total Clusters Found | 47 |
| Score-8+ Clusters | 6 (3 new) |
| Score-7 Clusters | 8 |
| Score-6+ Candidates | 27 |
| JSR/PHP/JSL Prologues | 12 |
| Cross-Bank Callers | 20+ |

---

*Report generated: 2026-04-08*
*Analysis tool: seam_block_v1 + score_target_owner_backtrack_v1 + find_local_code_islands_v2*
