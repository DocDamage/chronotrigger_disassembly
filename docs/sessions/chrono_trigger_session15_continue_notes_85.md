# Chrono Trigger Session 15 — Continuation Notes 85

## Block closed: C7:EE00..C7:F7FF (10 pages)

**Upper C7 code region boundary identified — predominantly data/text territory.**

---

## Summary

- **Pages processed:** 10 (EE00-F7FF)
- **Promotions:** 0
- **Page families:** 5 mixed_command_data, 4 text_ascii_heavy, 1 branch_fed_control_pocket
- **Review postures:** 3 rejected, 4 mixed_continue, 2 local_control_only, 1 manual_review

---

## Critical Finding: Code/Data Boundary

This block confirms the **upper boundary of executable code** in C7 bank:

### Evidence

| Indicator | Finding |
|-----------|---------|
| **Text pages** | 4 out of 10 (EE00, F000, F600, F700) |
| **Zero activity pages** | F500, F700 (0 xref hits) |
| **Rejection rate** | 3 pages rejected (EF00, F000, F100) |
| **ASCII ratio** | EE24 candidate has **77.4% ASCII** (text, not code) |

### Boundary Assessment

```
C500-C8FF  [Code candidates - C5AC promoted]
C900-CFFF  [Code candidates - clusters present]
D000-DFFF  [Mixed - fragmented but code-like]
E000-E3FF  [Transition - first text at E200]
E400-EFFF  [Data dominant - text pages]
F000-F7FF  [Data territory - zero activity]
```

**Executable code likely ends around E300-E400.**

---

## Anchor Status Update

### No New Strong Anchors Found

Scanned EE00-F7FF for calls to score-6 candidates:

| Candidate | Calls from EE00-F7FF | Status |
|-----------|---------------------|--------|
| C7:C5AC | 0 | Promoted (pass 194) |
| C7:D363 | 0 | Still frozen |
| C7:DDF4 | 0 | Still frozen |
| C7:DDEE | 0 | Still frozen |

**Linear scanning EE00+ will NOT yield anchors** to the C500-DFFF code region.

---

## Strategic Pivot Required

### What We've Learned

1. **C5AC promotion** created strong anchor in C500 region
2. **C500-E300** contains code candidates but **no cross-region callers** from E300+
3. **E300-F7FF** is predominantly data/text
4. **Strong anchors must come from within C500-E300 itself**

### Recommended Next Steps

**Option A: Promote D363 on threshold**
- Score 6 + PHD prologue + local cluster
- Second strongest candidate after C5AC
- Creates anchor chain: B000 → C300 → C5AC → D363

**Option B: Jump to C000-C200 gap**
- C193 cluster (score 6, 2 calls, 1 return) near promoted regions
- May bridge C000 to C5AC

**Option C: Continue to F800+**
- Confirm data territory extends to end of bank
- Low priority — pattern is clear

---

## Block Details

### EE00 Page — Text/Mixed

| Property | Value |
|----------|-------|
| **Family** | text_ascii_heavy |
| **Best target** | EE24 (score 4) |
| **ASCII ratio** | **77.4%** — definitively text |
| **Status** | Local control only |

### F300 Page — Best Code-Like Activity

| Candidate | Target | Score | Start | Anchor |
|-----------|--------|-------|-------|--------|
| F3BE | F3C4 | 4 | 22 (JSL) | Suspect (C7:361D) |
| F3E5 | F3EA | 4 | 22 (JSL) | Weak (C7:D039) |

**Note:** JSL (0x22) prologues suggest long jumps, but anchors are weak.

### Zero Activity Pages

- **F500**: 0 targets, 0 hits, 0 clusters
- **F700**: 0 targets, 0 hits, 0 clusters

These are definitively **data or padding** pages.

---

## Running Promotion Count

| Pass | Region | Notes |
|------|--------|-------|
| 192 | C7:C300-C4FF | First upper C7 code |
| 193 | C7:B000-B1FF | Validated by C300 |
| 194 | C7:C5AC-C5D0 | Threshold, REP prologue |
| **Pending** | C7:D363? | Score 6, PHD prologue |

**Total: 3 promotions**

---

## Files Generated

- `reports/c7_ee00_f7ff_seam_block.json`
- `reports/c7_ee00_f7ff_seam_block.md`
- `reports/c7_ee00_eeff_backtrack.json`
- `reports/c7_f300_f3ff_backtrack.json`

---

## New Live Seam: C7:F800..

**Continuing seam at F800+ is low priority** — data territory confirmed.

### Recommended Action

**Promote C7:D363 as pass 195** (threshold promotion):

| Evidence | Status |
|----------|--------|
| Score 6 | ✅ Perfect backtrack |
| PHD prologue | ✅ Valid 65816 instruction |
| Local cluster | ✅ Score 6, 2 calls, 1 return |
| Anchor | ❌ None — but C5AC now nearby |

**Rationale:**
- Second strongest candidate after C5AC
- Creates contiguous anchor chain
- PHD prologue less definitive than REP, but still valid
- Cluster has stronger internal evidence than C5AC's cluster

### Alternative: Jump to C193 Cluster

C7:C193 cluster (notes_80):
- Score 7, 1 call, 5 branches, 2 returns
- Located in C100 region
- Could bridge C000-C5AC gap

---

## Upper C7 Code Map (Final)

```
B000-B1FF  [PROMOTED pass 193] ⭐
    ↓ GAP (B200-C2FF orphan - low priority)
C300-C4FF  [PROMOTED pass 192] ⭐
    ↓
C500-C5FF  [PROMOTED pass 194] ⭐
    ↓
C600-DFFF  [Code candidates - D363 strongest] ⭐ CANDIDATE
    ↓
E000-E3FF  [Transition zone]
E400-F7FF  [DATA/TEXT - boundary confirmed]
F800-FFFF  [Likely data/padding]
```

**Next threshold promotion: D363 recommended.**

---

**🎯 Upper C7 boundary confirmed at ~E300-E400. Time to solidify the code region with D363 promotion!**
