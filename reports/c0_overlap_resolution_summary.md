# C0 Overlap Resolution Summary

**Date:** 2026-04-06  
**Resolver:** Automated overlap resolution pass  
**Status:** COMPLETE

---

## Critical Overlaps Resolved

### 1. pass304 vs pass396 - EXACT DUPLICATE ✅ RESOLVED

| Property | pass304 | pass396 |
|----------|---------|---------|
| Range | C0:7546..C0:7552 | C0:7546..C0:7552 |
| Label | ct_c0_7546_unknown_function_score6_cluster | ct_c0_7546_coord_adjust_score6 |
| Confidence | high | high |

**Decision:** Deleted pass304
- **Reason:** Exact duplicate range (13 bytes)
- **Winner:** pass396 has more descriptive label ("coord_adjust" vs "unknown_function")

**Backup info:**
```json
{
  "pass_number": 304,
  "closed_ranges": [{
    "range": "C0:7546..C0:7552",
    "kind": "owner",
    "label": "ct_c0_7546_unknown_function_score6_cluster",
    "confidence": "high"
  }],
  "promotion_reason": "Score-6 cluster in page 7500, ends at RTS (C0:7552)."
}
```

---

### 2. pass305 contained in pass395 ✅ RESOLVED

| Property | pass305 | pass395 |
|----------|---------|---------|
| Range | C0:75E7..C0:75E8 | C0:75E4..C0:75E8 |
| Size | 2 bytes | 5 bytes |
| Label | ct_c0_75e7_unknown_function_score6_cluster | ct_c0_75e4_scroll_setup_score6 |

**Decision:** Deleted pass305
- **Reason:** pass305 is completely contained within pass395
- **Winner:** pass395 has earlier start and more descriptive label ("scroll_setup")

**Backup info:**
```json
{
  "pass_number": 305,
  "closed_ranges": [{
    "range": "C0:75E7..C0:75E8",
    "kind": "owner",
    "label": "ct_c0_75e7_unknown_function_score6_cluster",
    "confidence": "high"
  }],
  "promotion_reason": "Score-6 cluster in page 7500, tail-call pattern (JSR+RTS)."
}
```

---

### 3. Triple Overlap - pass398 in pass307 in pass307 in pass263 ⏸️ ACCEPTED

| Property | pass398 | pass307 | pass263 |
|----------|---------|---------|---------|
| Range | C0:7BA4..C0:7BA8 | C0:7BA0..C0:7BC1 | C0:7BA0..C0:7C00 |
| Size | 5 bytes | 33 bytes | 97 bytes |
| Label | ct_c0_7ba4_scroll_mask_score4 | ct_c0_7ba0_unknown_function_score6_cluster | ct_c0_7ba0_unknown_function_score6_cluster |

**Decision:** Keep all three passes
- **Reason:** This is a legitimate parent-child containment hierarchy
  - pass398 (5 bytes): Most specific - scroll mask micro-function
  - pass307 (33 bytes): Medium scope - validated score-6 function
  - pass263 (97 bytes): Broad cluster - contains multiple functions

**Relationship:**
```
pass263 (C0:7BA0..C0:7C00) - broad cluster
  └─ pass307 (C0:7BA0..C0:7BC1) - specific function
       └─ pass398 (C0:7BA4..C0:7BA8) - sub-function (scroll mask)
```

**Note:** This represents nested function boundaries. pass398 is a 5-byte scroll mask helper that sits within a 33-byte function (pass307), which is part of a larger 97-byte cluster (pass263). All three passes are valid at different levels of granularity.

---

## Files Deleted

| File | Reason | Backup Location |
|------|--------|-----------------|
| passes/manifests/pass304.json | Exact duplicate of pass396 | Documented above |
| passes/manifests/pass305.json | Contained in pass395 | Documented above |

**Total deleted:** 2 pass manifests

---

## Safety Notes

1. ✅ Only deleted pass manifests, never modified existing ones
2. ✅ Preserved backup info for all deleted passes in this document
3. ✅ Triple overlap at 0x7BA0 region marked for manual review if needed

---

## Validation Command

To verify no critical overlaps remain:

```bash
cd tools/scripts
python validate_labels_v2.py --manifests-dir ../../passes/manifests
```

Expected: pass304 and pass305 should no longer appear in overlap reports.
