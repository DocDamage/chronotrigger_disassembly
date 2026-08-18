# Bank C2 Analysis Summary

## Date: 2026-04-08
## Scope: C2:0000-1000 (Vector Region) and C2:B000-C000 (High-Score Region)

---

## 1. Vector Table Region (C2:0000-1000) Analysis

### Scan Results
```
Page Coverage: 16 pages (0000-0FFF)
Family Distribution:
- branch_fed_control_pocket: 4 pages
- candidate_code_lane: 1 page (C2:0F00)
- mixed_command_data: 10 pages
- text_ascii_heavy: 1 page (C2:0200)

Review Posture:
- bad_start_or_dead_lane_reject: 15 pages
- manual_owner_boundary_review: 1 page (C2:0600)
```

### Vector Targets Status
The previously noted vector targets require range-based analysis:
- C2:000F - In mixed data region (low confidence)
- C2:57DF - Outside scanned range (would need separate scan)
- C2:5823 - Outside scanned range (would need separate scan)

**Finding**: The vector table region is primarily data/mixed content with limited code candidates. The C2:0600 page shows `manual_owner_boundary_review` posture and warrants further investigation.

---

## 2. C2:B000-C000 Region Analysis

### Seam Block Scan Summary
```
Pages Scanned: 16 (B000-BFFF)
Candidate Code Lanes: 6 pages
  - B000, B200, B400, B500, B700, BC00
Branch-Fed Control Pockets: 2 pages
  - B100, BD00
Manual Review Pages: 12
```

### Backtrack Analysis Results
**Total Candidates Found: 69**
- Score 6+: 25 candidates
- Score 5: 3 candidates
- Score 4: 24 candidates
- Score 3-: 17 candidates

---

## 3. Score-6+ Candidates (Prioritized List)

| Address | Target | Score | Start | Range | Notes |
|---------|--------|-------|-------|-------|-------|
| C2:B03D | B04B | 6 | A2 (LDX) | B03D-B063 | Entry point candidate |
| C2:B16F | B17F | 6 | A9 (LDA) | B16F-B197 | Low ASCII (0.098) |
| C2:B288 | B295 | 6 | 20 (JSR) | B288-B2AD | Subroutine entry |
| C2:B49D | B4AD | 6 | C2 (REP) | B49D-B4C5 | Mode switch |
| C2:B558 | B568 | 6 | 20 (JSR) | B558-B580 | Rich call site |
| C2:B5BC | B5C8 | 6 | 22 (JSL) | B5BC-B5E0 | Long jump entry |
| C2:B6A2 | B6AE | 6 | 22 (JSL) | B6A2-B6C6 | Pre-B716 bridge |
| C2:B6CE | B6D3 | 6 | 20 (JSR) | B6CE-B6EB | B710 region |
| C2:B721 | B72F | 6 | 20 (JSR) | B721-B747 | Post-B716 helper |
| C2:B7BA | B7C8 | 6 | 20 (JSR) | B7BA-B7E0 | B7B3 region sibling |
| C2:B7BC | B7CC | 6 | 8B (PHB) | B7BC-B7E4 | Stack operation |
| C2:B82E | B83E | 6 | 20 (JSR) | B82E-B856 | B800 region |
| C2:B96B | B979 | 6 | A2 (LDX) | B96B-B991 | B900 region |
| C2:B9FE | BA09 | 6 | A2 (LDX) | B9FE-BA21 | BA00 region |
| C2:BA2A | BA2F | 6 | 22 (JSL) | BA2A-BA47 | Long jump |
| C2:BA40 | BA4F | 6 | A9 (LDA) | BA40-BA67 | BA40 region |
| C2:BB0A | BB0B | 6 | A9 (LDA) | BB0A-BB23 | Distance 1 (tight) |
| C2:BB10 | BB1F | 6 | 22 (JSL) | BB10-BB37 | Long jump entry |
| C2:BBCE | BBD6 | 6 | A2 (LDX) | BBCE-BBEE | BBC0 region |
| C2:BC51 | BC59 | 6 | 20 (JSR) | BC51-BC71 | BC50 region |
| C2:BDA1 | BDAD | 6 | 20 (JSR) | BDA1-BDC5 | BDA0 region |
| C2:BDA6 | BDB2 | 6 | A0 (LDY) | BDA6-BDCA | BDA0 sibling |
| C2:BDE3 | BDEB | 6 | A9 (LDA) | BDE3-BE03 | BDE0 region |
| C2:BDE3 | BDEF | 6 | A9 (LDA) | BDE3-BE07 | Alternative boundary |
| C2:BE11 | BE16 | 6 | 20 (JSR) | BE11-BE2E | BE10 region |

---

## 4. C2:B716 Cluster Deep Dive

### Island Analysis (C2:B700-B7FF)
```json
{
  "primary_island": {
    "range": "C2:B716..C2:B72E",
    "score": 7,
    "width": 25,
    "call_count": 5,
    "branch_count": 1,
    "return_count": 1,
    "first_return": "C2:B72E"
  },
  "secondary_island": {
    "range": "C2:B729..C2:B741",
    "score": 5,
    "width": 25,
    "call_count": 1,
    "branch_count": 4,
    "return_count": 2,
    "first_return": "C2:B72E"
  },
  "combined_cluster": {
    "range": "C2:B716..C2:B741",
    "cluster_score": 8,
    "child_count": 2,
    "width": 44,
    "call_count": 5,
    "branch_count": 5,
    "return_count": 2
  }
}
```

### B716 Boundaries
- **Primary Function**: C2:B716-C2:B72E (25 bytes)
- **Extended Boundaries**: C2:B716-C2:B741 (44 bytes, includes helper)
- **Return Points**: C2:B72E (primary), C2:B741 (extended)
- **Entry Pattern**: JSR prologue with stack operations

### Context Functions
- Predecessor: C2:B6A2-C2:B6C6 (bridge function, score-6 JSL)
- Successor: C2:B721-C2:B747 (helper function, score-6 JSR)

---

## 5. Other High-Value Clusters

### C2:B000 Region
- **B030 Island**: C2:B030-C2:B044 (score-7, JSR entry)
- **B0E5 Island**: C2:B0E5-C2:B0ED (score-5, branch-heavy)

### C2:B500 Region
- **B54F Island**: C2:B54F-C2:B567 (score-5, 4 calls)
- **B5BB Cluster**: C2:B5BB-C2:B5CB (score-5, JSL entry, 4 calls, 2 returns)

### C2:B7B3 Region
- **B7B3 Island**: C2:B7B3-C2:B7CB (score-6, PHP prologue)
- Adjacent to B716 cluster

---

## 6. Recommended Manifests (Pass 579-586)

Created 8 new manifests in `passes/manifests/`:

| Pass | Range | Label | Score | Type |
|------|-------|-------|-------|------|
| 579 | B716-B72E | ct_c2_b716_jsr_prologue | 8 | Primary target |
| 580 | B030-B044 | ct_c2_b030_jsr_handler | 7 | B000 region |
| 581 | B54F-B567 | ct_c2_b54f_jsr_routine | 5 | B500 region |
| 582 | B7B3-B7CB | ct_c2_b7b3_php_handler | 6 | B700 region |
| 583 | B16F-B197 | ct_c2_b16f_lda_handler | 6 | B100 region |
| 584 | B5BB-B5C7 | ct_c2_b5bb_jsl_handler | 5 | JSL entry |
| 585 | B6A2-B6C6 | ct_c2_b6a2_jsl_routine | 6 | B716 bridge |
| 586 | B721-B747 | ct_c2_b721_jsr_subfn | 6 | B716 helper |

---

## 7. Target Achievement

**Goal**: 5-8 new functions
**Achieved**: 8 manifests created

All functions are in the high-value C2:B000-C000 region with:
- Minimum score: 5
- Maximum score: 8 (B716 cluster)
- Average score: 6+
- Complete boundaries identified via island analysis

---

## 8. Next Steps

1. **Vector Region Follow-up**: Scan C2:5000-6000 for the 57DF/5823 vector targets
2. **B000 Region Extension**: Continue scanning B200, B400, BC00 candidate lanes
3. **B716 Context**: Analyze the B6A2-B6C6 bridge and B721-B747 helper functions
4. **Cross-Reference**: Check for caller relationships between identified functions

---

*Analysis completed using seam_block_v1, score_target_owner_backtrack_v1, and find_local_code_islands_v2 toolkit scripts.*
