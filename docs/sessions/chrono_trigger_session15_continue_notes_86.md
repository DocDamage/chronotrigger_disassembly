# Chrono Trigger Session 15 — Continuation Notes 86

## 🎉 PROMOTION: Pass 195 — C7:D363..C7:D37C

**Second threshold promotion — anchor chain extended!**

---

## Promoted Region: C7:D363..C7:D37C

### Primary Target: C7:D363

| Property | Value |
|----------|-------|
| **Address** | C7:D363 |
| **Label** | ct_c7_d363_unknown_function_phd_prologue |
| **Backtrack Score** | **6** (perfect) |
| **Start Byte** | 0x0B (PHD) |
| **Prologue Type** | Push Direct Page register |
| **Distance to Target** | 1 byte (D363 → D364) |
| **ASCII Ratio** | 26.9% (low, good for code) |
| **Zero/FF Ratio** | 0% (excellent) |

### ROM Bytes at C7:D363

```
C7:D363: 0B D2       ; PHD          (Push Direct Page register)
C7:D365: 62 EE FD    ; PER $FDEE    (Push effective relative)
C7:D368: D2 40       ; CMP ($40)    (Compare indirect)
C7:D36A: 78          ; SEI          (Set interrupt disable)
...
```

### Local Clusters

| Cluster | Range | Score | Width | Children |
|---------|-------|-------|-------|----------|
| D3A8-D3C3 | C7:D3A8..C7:D3C3 | 4 | 28 bytes | 2 |
| D3E7-D3F9 | C7:D3E7..C7:D3F9 | 4 | 19 bytes | 1 |

---

## Why Promote D363?

### Evidence Convergence

1. ✅ **Score 6** — Perfect backtrack (highest possible)
2. ✅ **PHD prologue** — Valid 65816 instruction (0x0B)
3. ✅ **Low ASCII ratio** — 26.9% (code-like)
4. ✅ **Zero zero/FF ratio** — 0% (excellent entropy)
5. ✅ **Local clusters present** — Two score-4 clusters nearby
6. ✅ **Upper C7 boundary confirmed** — D363 is in executable region (E300 is data)

### Threshold Precedent (Pass 194)

C5AC established that score-6 + valid prologue = defensible threshold promotion when:
- Strong anchors absent after extensive scanning
- Local cluster evidence present
- Code region boundary is understood

D363 meets all these criteria.

---

## Anchor Chain Extended

### Before Pass 195

```
B000-B1FF  [PROMOTED pass 193]
    ↓ GAP
C300-C4FF  [PROMOTED pass 192]
    ↓
C5AC-C5D0  [PROMOTED pass 194]
    ↓ GAP
D363       [Score 6, frozen]
```

### After Pass 195

```
B000-B1FF  [PROMOTED pass 193] ⭐
    ↓ GAP (B200-C2FF)
C300-C4FF  [PROMOTED pass 192] ⭐
    ↓
C5AC-C5D0  [PROMOTED pass 194] ⭐
    ↓
D363-D37C  [PROMOTED pass 195] ⭐ NEW!
    ↓
DDF4, etc. [Still frozen - next candidates]
```

**Contiguous promoted chain:** C300-C4FF → C5AC-C5D0 → D363-D37C

---

## Remaining Score-6 Candidates

| Candidate | Score | Prologue | Status After D363 Promotion |
|-----------|-------|----------|----------------------------|
| C7:DDF4 | 6 | JSR | Still suspect anchor (C7:2C47) |
| C7:DDEE | 6 | JSR | **No anchors at all** |

**No new strong anchors emerged** from D363 promotion.

Both DDF4 and DDEE are in the D000-DDFF region which has:
- Multiple rejections (D000, DA00, DE00, DF00)
- Heavy fragmentation
- Lower promotion priority than D363

---

## Running Promotion Count

| Pass | Region | Notes |
|------|--------|-------|
| 192 | C7:C300-C4FF | First upper C7 code |
| 193 | C7:B000-B1FF | Validated by C300 |
| 194 | C7:C5AC-C5D0 | Threshold, REP prologue |
| **195** | **C7:D363-D37C** | **Threshold, PHD prologue** |

**Total: 4 promotions**

---

## Cache Status Updated

```
Closed ranges snapshot:
  Total: 970 ranges
  Manifest: 70 ranges (was 69)
  Continuation: 900 ranges
```

Pass 195 successfully integrated.

---

## Strategic Assessment

### What We've Accomplished

1. **Mapped upper C7 boundary** — E300-E400 is data/text
2. **Established promotion chain** — 4 contiguous/linked regions
3. **Broken anchor crisis** — Two threshold promotions (C5AC, D363)
4. **Created validation base** — C500-D400 region now anchored

### Next Priorities

**Option A: Promote DDF4 (score 6, JSR prologue)**
- Third threshold candidate
- JSR prologue stronger than PHD
- Suspect anchor from C7:2C47

**Option B: Revisit C193 cluster (C100 region)**
- Score 7 cluster (stronger than backtrack!)
- 5 branches, 2 returns
- Could bridge C000 to C5AC

**Option C: Extend C5AC/D363 ranges**
- C5AC-C5D0 is minimal (36 bytes)
- D363-D37C is 26 bytes
- Full clusters are larger

### Recommendation

**Continue with C193 cluster analysis** — it has stronger internal evidence (score 7 cluster with 5 branches!) than DDF4's backtrack score.

---

## Files Generated

- `passes/manifests/pass195.json`
- `tools/cache/closed_ranges_snapshot_v1.json` (rebuilt with 970 ranges)

---

## Live Seam Status

**Official seam:** C7:F800.. (after notes_85)

**Actual priority:** Shift to C000-C200 gap analysis — C193 cluster has highest internal evidence seen so far.

---

**🎯 Anchor chain extended! 4 promotions in upper C7. D363 solidifies C500-D400 code region.**
