# Bank C4:0000-1000 Gap Analysis Report

**Date:** 2026-04-08
**Region:** C4:0000-1000 (First 4KB of Bank C4)
**Previous Coverage:** 9 manifests (641-649)
**New Discoveries:** 5 score-6+ candidates, 7 code islands

---

## Summary

This analysis focused on mapping the gaps in Bank C4:0000-1000 using backtrack analysis from the 192 previously identified candidates. The region was found to contain significant initialization and utility code similar to patterns seen in Bank C0.

### Results
- **5 new score-6+ function candidates identified**
- **7 code islands discovered in gaps**
- **10 gaps analyzed covering ~3.8KB of unmapped space**
- **Recommended 8 new manifests (650-657)**

---

## Existing Coverage (Manifests 641-649)

| Pass | Range | Label | Pattern |
|------|-------|-------|---------|
| 641 | C4:01D2..C4:01EB | ct_c4_01d2_jsr_handler | JSR prologue |
| 642 | C4:02BB..C4:02D8 | ct_c4_02bb_phb_handler | PHB prologue |
| 643 | C4:0347..C4:0369 | ct_c4_0347_dual_target | JSR dual-target |
| 644 | C4:049D..C4:04BC | ct_c4_049d_ldy_init | LDY# initialization |
| 645 | C4:0617..C4:0637 | ct_c4_0617_jsr_util | JSR utility |
| 646 | C4:0810..C4:082A | ct_c4_0810_jsr_dispatch | JSR dispatcher |
| 647 | C4:085E..C4:0877 | ct_c4_085e_ldy_handler | LDY# handler |
| 648 | C4:08B7..C4:08D5 | ct_c4_08b7_jsr_routine | JSR routine |
| 649 | C4:0A54..C4:0A73 | ct_c4_0a54_jsr_entry | JSR entry point |

**Coverage:** 9 ranges = ~390 bytes (9.5% of 4KB region)

---

## Gap Analysis

### Identified Gaps

| Gap | Range | Size | Status |
|-----|-------|------|--------|
| 1 | C4:0000..C4:01D1 | 466 bytes | **NEW CANDIDATES FOUND** |
| 2 | C4:01EC..C4:02BA | 207 bytes | No high-score candidates |
| 3 | C4:02D9..C4:0346 | 110 bytes | No high-score candidates |
| 4 | C4:036A..C4:049C | 307 bytes | No high-score candidates |
| 5 | C4:04BD..C4:0616 | 346 bytes | Score-4 candidates only |
| 6 | C4:0638..C4:080F | 472 bytes | Code island found |
| 7 | C4:082B..C4:085D | 51 bytes | Too small |
| 8 | C4:0878..C4:08B6 | 63 bytes | Too small |
| 9 | C4:08D6..C4:0A53 | 382 bytes | No high-score candidates |
| 10 | C4:0A74..C4:0FFF | 1420 bytes | **NEW CANDIDATES FOUND** |

---

## New Score-6+ Candidates

### Gap 1: C4:0000-01D1

| Address | Target | Score | Prologue | Type |
|---------|--------|-------|----------|------|
| C4:007B | C4:007C | 6 | JSR ($20) | Utility function |
| C4:00F9 | C4:00FC | 6 | JSL ($22) | Long call handler |

**Analysis:** 
- C4:007B: Clean JSR entry with 34-byte estimated range. Appears to be an early utility function in the bank header region.
- C4:00F9: JSL (long jump) entry point, suggesting cross-bank functionality. 36-byte estimated range.

### Gap 10: C4:0A74-0FFF

| Address | Target | Score | Prologue | Type |
|---------|--------|-------|----------|------|
| C4:0A99 | C4:0AA0 | 6 | JSL ($22) | Long call handler |
| C4:0ADB | C4:0AE0 | 6 | JSL ($22) | Long call handler |
| C4:0E8C | C4:0EA0 | 6 | PHP ($08) | State preservation |

**Analysis:**
- C4:0A99: JSL entry with 40-byte range. Positioned after manifest 649 (C4:0A54), suggesting related functionality.
- C4:0ADB: Second JSL entry, 38-byte range. Multiple JSL targets in this region suggest jump table or dispatch pattern.
- C4:0E8C: PHP prologue indicates state-preserving function. 53-byte range suggests substantial logic.

---

## Code Islands Found

Code islands are return-anchored code sequences that form valid subroutines:

### High-Score Islands (Score 5+)

| Range | Score | Width | Returns | Location |
|-------|-------|-------|---------|----------|
| C4:0E7A..C4:0E96 | 7 | 29 bytes | 3 | Gap 10 |
| C4:0AFE..C4:0B12 | 5 | 21 bytes | 1 | Gap 10 |
| C4:0B32..C4:0B44 | 5 | 19 bytes | 1 | Gap 10 |

### Additional Islands

| Range | Score | Width | Returns | Location |
|-------|-------|-------|---------|----------|
| C4:0BCE..C4:0BE7 | 4 | 26 bytes | 3 | Gap 10 |
| C4:073C..C4:074C | 3 | 17 bytes | 1 | Gap 6 |
| C4:0E53..C4:0E6B | 3 | 25 bytes | 2 | Gap 10 |
| C4:0DF4..C4:0E09 | 3 | 22 bytes | 1 | Gap 10 |

---

## Entry Point Patterns Discovered

### Prologue Distribution

| Prologue Type | Count | Description |
|---------------|-------|-------------|
| JSR ($20) | 7 | Standard subroutine calls |
| JSL ($22) | 4 | Long/cross-bank calls |
| LDY#/LDX# (A0/A2) | 2 | Index register initialization |
| PHP ($08) | 1 | State preservation |
| PHB ($8B) | 1 | Data bank preservation |

### Pattern Analysis

1. **JSL Cluster at C4:0A99/0ADB**: Two JSL entries within 64 bytes suggests a jump table pattern or related cross-bank utilities.

2. **PHP Handler at C4:0E8C**: State-preserving function likely called during interrupts or mode switches.

3. **Early Bank Functions (C4:007B/00F9)**: Positioned in the first 256 bytes, suggesting initialization or bank-header utilities.

---

## Recommended New Manifests

### From Backtrack Analysis (Score-6+)

```json
// Pass 650
{
  "pass_number": 650,
  "closed_ranges": [{
    "range": "C4:007B..C4:009C",
    "kind": "owner",
    "label": "ct_c4_007b_jsr_handler",
    "confidence": "high"
  }],
  "promotion_reason": "Score-6 cluster, JSR prologue. Target C4:007C. Gap fill in C4:0000-01D1."
}

// Pass 651
{
  "pass_number": 651,
  "closed_ranges": [{
    "range": "C4:00F9..C4:011C",
    "kind": "owner",
    "label": "ct_c4_00f9_jsl_handler",
    "confidence": "high"
  }],
  "promotion_reason": "Score-6 cluster, JSL prologue. Target C4:00FC. Long-call handler in bank header."
}

// Pass 652
{
  "pass_number": 652,
  "closed_ranges": [{
    "range": "C4:0A99..C4:0AC0",
    "kind": "owner",
    "label": "ct_c4_0a99_jsl_handler",
    "confidence": "high"
  }],
  "promotion_reason": "Score-6 cluster, JSL prologue. Target C4:0AA0. Post-manifest-649 gap fill."
}

// Pass 653
{
  "pass_number": 653,
  "closed_ranges": [{
    "range": "C4:0ADB..C4:0B00",
    "kind": "owner",
    "label": "ct_c4_0adb_jsl_handler",
    "confidence": "high"
  }],
  "promotion_reason": "Score-6 cluster, JSL prologue. Target C4:0AE0. JSL cluster pattern."
}

// Pass 654
{
  "pass_number": 654,
  "closed_ranges": [{
    "range": "C4:0E8C..C4:0EC0",
    "kind": "owner",
    "label": "ct_c4_0e8c_php_handler",
    "confidence": "high"
  }],
  "promotion_reason": "Score-6 cluster, PHP prologue. Target C4:0EA0. State preservation function."
}
```

### From Code Island Analysis

```json
// Pass 655 (High-score island)
{
  "pass_number": 655,
  "closed_ranges": [{
    "range": "C4:0E7A..C4:0E96",
    "kind": "owner",
    "label": "ct_c4_0e7a_island_score7",
    "confidence": "high"
  }],
  "promotion_reason": "Code island score-7, 3 returns, 29 bytes. High-confidence subroutine."
}

// Pass 656
{
  "pass_number": 656,
  "closed_ranges": [{
    "range": "C4:0AFE..C4:0B12",
    "kind": "owner",
    "label": "ct_c4_0afe_island_score5",
    "confidence": "high"
  }],
  "promotion_reason": "Code island score-5, 1 return, 21 bytes. 2 calls, 2 branches."
}

// Pass 657
{
  "pass_number": 657,
  "closed_ranges": [{
    "range": "C4:0B32..C4:0B44",
    "kind": "owner",
    "label": "ct_c4_0b32_island_score5",
    "confidence": "high"
  }],
  "promotion_reason": "Code island score-5, 1 return, 19 bytes. 2 calls, 1 branch."
}
```

---

## Coverage Improvement

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Manifests | 9 | 17 (+8) | +89% |
| Documented ranges | 9 | 17 | +8 ranges |
| Bytes covered | ~390 | ~720 | +330 bytes |
| Coverage % | 9.5% | 17.6% | +8.1% |

---

## Next Steps

1. **Apply manifests 650-657** to close the identified gaps
2. **Continue gap analysis** on C4:1000-FFFF (remaining 60KB)
3. **Cross-reference with C0 patterns** - many C4 functions appear similar to C0 utilities
4. **Investigate score-4 candidates** in gaps 5 and 6 for potential promotion
5. **Analyze jump table patterns** around C4:0A99/0ADB

---

## Appendix: Score-4 Candidates for Future Analysis

### Gap 5 (C4:04BD-0616)
- C4:04DB -> C4:04DF (score=4, LDY# prologue)
- C4:054D -> C4:0551 (score=4)
- C4:0575 -> C4:057A/0582 (score=4)
- C4:060A -> C4:060B (score=4)

### Gap 6 (C4:0638-080F)
- C4:064E -> C4:0650 (score=4, PHP prologue)
- C4:073D -> C4:0745 (score=4)
- C4:075B -> C4:0760 (score=4)
- C4:0800 -> C4:0808 (score=4)

These may be promoted upon further analysis of their calling contexts.
