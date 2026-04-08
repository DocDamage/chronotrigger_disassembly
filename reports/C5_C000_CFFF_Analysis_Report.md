# Bank C5:C000-CFFF Analysis Report

## Executive Summary

Analysis of Bank C5:C000-CFFF (16 pages, 0x1000 bytes) - a rich code region identified as high priority. This region shows significant code density with multiple score-6+ function entry points.

## Current State

### Existing Manifests for C5
| Pass | Range | Label | Confidence |
|------|-------|-------|------------|
| 576 | C5:4206-4280 | ct_c5_4206_php_prologue | high |
| 577 | C5:C030-C0A0 | ct_c5_c030_c000_region | high |
| 578 | C5:C0B7-C130 | ct_c5_c0b7_jsl_prologue | high |
| 579 | C5:4206-4280 | ct_c5_4206_php_prologue | high |
| 580 | C5:4FBD-4FC4 | ct_c5_4fbd_return_anchored | high |
| 581 | C5:4805-481D | ct_c5_4805_phd_prologue | medium |
| 582 | C5:44D6-44E1 | ct_c5_44d6_score5_island | medium |
| 619 | C5:4767-476F | ct_c5_4767_call_anchor | medium |
| 620 | C5:4A00-4A17 | ct_c5_4a00_branch_handler | medium |

### C5 Coverage Stats
- 9 documented ranges
- 0.85% coverage (very low - high opportunity)
- C5:4000-4FFF previously deep scanned (high code density found)

---

## Seam Block Analysis Results (C5:C000-CFFF)

### Page Family Distribution
| Family | Count | Pages |
|--------|-------|-------|
| candidate_code_lane | 8 | C000, C300, C700, C800, C900, CB00, CC00, CF00 |
| branch_fed_control_pocket | 6 | C200, C400, C500, C600, CD00, CE00 |
| mixed_command_data | 2 | C100, CA00 |

### Review Posture Distribution
| Posture | Count | Description |
|---------|-------|-------------|
| local_control_only | 10 | Internal control flow (branches only) |
| bad_start_or_dead_lane_reject | 4 | Bad start bytes or dead lanes |
| manual_owner_boundary_review | 1 | Needs manual review (C200) |
| mixed_lane_continue | 1 | Mixed content (C700) |

---

## Score-6+ Candidates Found

### Score-6 Candidates (High Confidence)

| # | Address | Prologue | Target | Distance | Notes |
|---|---------|----------|--------|----------|-------|
| 1 | **C5:C030** | PHP (08) | C5:C034 | 4 | **EXISTING (Pass 577)** |
| 2 | **C5:C036** | JSR (20) | C5:C038 | 2 | **NEW** - Near C030 |
| 3 | **C5:C0B7** | JSL (22) | C5:C0C0 | 9 | **EXISTING (Pass 578)** - Cross-bank call |
| 4 | **C5:C0EA** | PHP (08) | C5:C0F4 | 10 | **NEW** - High confidence PHP prologue |
| 5 | **C5:C1E6** | JSR (20) | C5:C1EF | 9 | **NEW** - Score-6 JSR prologue |
| 6 | **C5:CEF2** | PHP (08) | C5:CF00 | 14 | **NEW** - End of region PHP prologue |

**Score-6 Summary:** 6 total candidates, 2 existing, **4 NEW high-confidence candidates**

### Score-5 Candidates (Medium-High Confidence)

| # | Address | Prologue | Target | Distance | Notes |
|---|---------|----------|--------|----------|-------|
| 7 | C5:C2FD | PHD (0B) | C5:C2FD | 0 | Stack frame setup |
| 8 | C5:CD33 | LDY# (A0) | C5:CD33 | 0 | Register init |

### Score-4 Candidates (Medium Confidence)

| # | Address | Prologue | Target | Notes |
|---|---------|----------|--------|-------|
| 9 | C5:C00C | PHP (08) | C5:C00D | Near C000 |
| 10 | C5:C129 | BVC (50) | C5:C130 | Branch target |
| 11 | C5:C3FD | CPY# (C0) | C5:C3FE | Near boundary |
| 12 | C5:C4FA | PHP (08) | C5:C500 | Score-4 PHP |
| 13 | C5:C617 | JSR (20) | C5:C61F | JSR prologue |
| 14 | C5:CB2B | AND (39) | C5:CB2F | Page CB |
| 15 | C5:C2A9 | PHB (8B) | C5:C2B0 | Stack push |

---

## Recommended New Manifests

### High Priority (Score-6)

#### Manifest 1: C5:C036 JSR Prologue
```json
{
  "pass_number": TBD,
  "closed_ranges": [
    {
      "range": "C5:C036..C5:C050",
      "kind": "owner",
      "label": "ct_c5_c036_jsr_prologue",
      "confidence": "high"
    }
  ],
  "promotion_reason": "Score-6 cluster, JSR prologue (20). Part of C5:C000 region code cluster. Adjacent to C5:C030."
}
```

#### Manifest 2: C5:C0EA PHP Prologue
```json
{
  "pass_number": TBD,
  "closed_ranges": [
    {
      "range": "C5:C0EA..C5:C10C",
      "kind": "owner",
      "label": "ct_c5_c0ea_php_prologue",
      "confidence": "high"
    }
  ],
  "promotion_reason": "Score-6 cluster, PHP prologue (08). High confidence function entry."
}
```

#### Manifest 3: C5:C1E6 JSR Prologue
```json
{
  "pass_number": TBD,
  "closed_ranges": [
    {
      "range": "C5:C1E6..C5:C207",
      "kind": "owner",
      "label": "ct_c5_c1e6_jsr_prologue",
      "confidence": "high"
    }
  ],
  "promotion_reason": "Score-6 cluster, JSR prologue (20). Candidate triage seed."
}
```

#### Manifest 4: C5:CEF2 PHP Prologue
```json
{
  "pass_number": TBD,
  "closed_ranges": [
    {
      "range": "C5:CEF2..C5:CF18",
      "kind": "owner",
      "label": "ct_c5_cef2_php_prologue",
      "confidence": "high"
    }
  ],
  "promotion_reason": "Score-6 cluster, PHP prologue (08). End of C5:CF00 region."
}
```

### Medium Priority (Score-5)

#### Manifest 5: C5:C2FD PHD Prologue
```json
{
  "pass_number": TBD,
  "closed_ranges": [
    {
      "range": "C5:C2FD..C5:C315",
      "kind": "owner",
      "label": "ct_c5_c2fd_phd_prologue",
      "confidence": "medium"
    }
  ],
  "promotion_reason": "Score-5 cluster, PHD prologue (0B). Stack frame setup."
}
```

#### Manifest 6: C5:CD33 LDY# Prologue
```json
{
  "pass_number": TBD,
  "closed_ranges": [
    {
      "range": "C5:CD33..C5:CD4B",
      "kind": "owner",
      "label": "ct_c5_cd33_ldy_prologue",
      "confidence": "medium"
    }
  ],
  "promotion_reason": "Score-5 cluster, LDY# prologue (A0). Register initialization."
}
```

### Lower Priority (Score-4) - Additional 7 Candidates

7. C5:C00C - PHP prologue (score-4)
8. C5:C129 - BVC control flow (score-4)
9. C5:C3FD - CPY# prologue (score-4)
10. C5:C4FA - PHP prologue (score-4)
11. C5:C617 - JSR prologue (score-4)
12. C5:CB2B - AND op (score-4)
13. C5:C2A9 - PHB prologue (score-4)

**Total Recommended: 13 new function ranges (4 score-6, 2 score-5, 7 score-4)**

---

## Comparison: C5:C000-CFFF vs C5:4000-4FFF

| Metric | C5:4000-4FFF | C5:C000-CFFF | Analysis |
|--------|--------------|--------------|----------|
| **Size** | 0x1000 (16 pages) | 0x1000 (16 pages) | Same size |
| **Score-6+ candidates** | ~4-5 | **6** | C000-CFFF higher density |
| **Existing manifests** | 5 (576,579,580,581,582) | 2 (577,578) | C000-CFFF less explored |
| **Page families** | Mixed | 8 candidate_code_lane | C000-CFFF more uniform |
| **Coverage** | ~5% | ~1% | C000-CFFF more opportunity |

### Key Differences

**C5:4000-4FFF:**
- Previously deep scanned
- More scattered code pockets
- Several small islands (44D6, 4805, 4A00, 4FBD)
- Mix of PHP, PHD, and return-anchored functions

**C5:C000-CFFF:**
- Higher density of PHP/JSR prologues
- More uniform page families (8 candidate_code_lane)
- Less explored - only 2 existing manifests
- Clustered entry points (C030-C0EA region has 4 score-6 candidates in ~200 bytes)
- Strong cross-bank call target (C0B7 JSL)

### Code Density Assessment

**C5:C000-C0FF:** Very High Density
- 4 score-6 candidates in first 256 bytes
- Multiple PHP/JSR/JSL prologues
- Active cross-bank calls

**C5:C100-CFFF:** Medium-High Density
- Score-6 at C1E6
- Score-5 at C2FD, CD33
- Score-6 at CEF2 (end of region)
- Several score-4 candidates throughout

---

## Prologue Type Analysis

| Prologue Type | Count | Addresses |
|---------------|-------|-----------|
| PHP (08) | 4 | C030, C00C, C0EA, CEF2, C4FA |
| JSR (20) | 2 | C036, C1E6 |
| JSL (22) | 1 | C0B7 |
| PHD (0B) | 1 | C2FD |
| LDY# (A0) | 1 | CD33 |
| PHB (8B) | 1 | C2A9 |
| CPY# (C0) | 1 | C3FD |

**Most common:** PHP prologues (save processor status) - typical for interrupt handlers and important functions

---

## Cross-Bank Call Analysis

High-value targets called from outside C5:
- C5:C0C0 - called from C5:81A8, C5:D675 (internal)
- C5:C0B7 - **JSL target** - cross-bank long jump
- C5:C2CB - called from FC:CA93 (far bank)

---

## Local Code Islands

Significant internal clusters found:
- C5:C0B6..C5:C0C4 (cluster score 5)
- C5:C034..C5:C03A (cluster score 4)
- C5:C1E2..C5:C1E8 (cluster score 6)
- C5:C2D9..C5:C2E7 (cluster score 5)
- C5:CB70..C5:CB7A (cluster score 7)
- C5:C947..C5:C95F (cluster score 6)

---

## Action Items

1. **Immediate:** Create manifests for 4 score-6 candidates (C036, C0EA, C1E6, CEF2)
2. **Short-term:** Create manifests for 2 score-5 candidates (C2FD, CD33)
3. **Medium-term:** Evaluate 7 score-4 candidates for promotion
4. **Investigation:** Determine boundaries for C5:C000 region (may be larger than currently mapped)
5. **Cross-bank:** Analyze C5:C0B7 JSL target callers (may reveal related functions)

---

## Conclusion

C5:C000-CFFF is confirmed as a **rich code region** with:
- **6 score-6+ function entry points** (4 new)
- **8 score-5+ candidates**
- **Higher code density than C5:4000-4FFF**
- **More uniform structure** (mostly candidate_code_lane pages)
- **Lower current coverage** (opportunity for discovery)

**Recommendation:** Prioritize C5:C000-CFFF for continued disassembly. The region shows characteristics of a major code hub with multiple utility functions and cross-bank entry points.

---

*Report generated: 2026-04-08*
*Region: C5:C000-CFFF (16 pages)*
*Analysis tools: run_seam_block_v1.py, score_target_owner_backtrack_v1.py*
