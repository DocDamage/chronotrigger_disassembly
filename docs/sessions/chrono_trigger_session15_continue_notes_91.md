# Chrono Trigger Session 15 — Continuation Notes 91

## 🎉🎉🎉 MILESTONE: Pass 200! — C7:3C00..C7:3C16

**200th pass! Dual evidence promotion continues the spree!**

---

## Promoted Region: C7:3C00..C7:3C16

### The 200th Pass Milestone

**Pass 200!** A major milestone in the Chrono Trigger disassembly project.

| Property | Value |
|----------|-------|
| **Pass** | **200** |
| **Address** | C7:3C00..C7:3C16 |
| **Label** | ct_c7_3c00_unknown_function_cluster_jsr_c4f3 |
| **Type** | Dual evidence (cluster + strong anchor) |

### Evidence Convergence

| Evidence | Finding |
|----------|---------|
| **Cluster** | 3C00-3C16 (score 4, 23 bytes) |
| **Strong anchor** | 3C04 calls C4F3 |
| **Anchor target** | C4F3 (promoted C300-C4FF) |
| **Instruction** | JSR $C4F3 (20 F3 C4) |

### ROM Verification

```
C7:3C00: 3F 53 07 D5    ; AND $D507,X
C7:3C04: 20 F3 C4       ; **JSR $C4F3** ← CALLS PROMOTED!
C7:3C07: 9B             ; TXY
C7:3C08: 3F 53 07 D5    ; AND $D507,X
...
```

**3C04: JSR $C4F3** — C4F3 is in promoted C300-C4FF (pass 192).

---

## Session 18: The Promotion Spree Summary

| Pass | Region | Type | Notes |
|------|--------|------|-------|
| 194 | C5AC-C5D0 | Threshold | REP prologue |
| 195 | D363-D37C | Threshold | PHD prologue |
| 196 | C193-C1B2 | Cluster | Score 7 |
| 197 | C1B6-C1CE | Extension | Adjacent to C193 |
| 198 | C028-C02C | Strong anchor | Calls B111 |
| 199 | 924D-9265 | Dual evidence | Score 7 + anchor |
| **200** | **3C00-3C16** | **Dual evidence** | **Score 4 + anchor** |

**7 promotions in one session!** (passes 194-200)

**9 total promotions in upper C7!**

---

## Upper C7 Status: 9 Promotions!

```
C028-C02C  [PROMOTED pass 198] ⭐
    ↓ GAP: C02D-C192
C193-C1CE  [PROMOTED pass 196+197] ⭐ 52 bytes
    ↓ GAP: C1CF-C2FF
C300-C4FF  [PROMOTED pass 192] ⭐
    ↑ 3C04 calls C4F3
    ↑ 9258 calls C3FA
C3C00-3C16 [PROMOTED pass 200] ⭐ NEW!
C924D-9265 [PROMOTED pass 199] ⭐
    ↓
C5AC-C5D0  [PROMOTED pass 194] ⭐
    ↓
D363-D37C  [PROMOTED pass 195] ⭐
    ↓
B000-B1FF  [PROMOTED pass 193] ⭐
```

---

## Remaining Strong Anchor Candidates

After pass 200, still **6 strong anchors** to promote:

| Address | Cluster | Target | Priority |
|---------|---------|--------|----------|
| 4A6A | None | C4EB | Medium |
| 7488 | None | B188 | Low (no cluster) |
| AEDE | None | C302 | High (calls C300) |
| BD2D | Score 2 | D364 | Medium |
| C275 | None | C5B0 | High (near C5AC) |
| CB1A | Near CBAF | B01F | Medium |

---

## Cache Status

```
Closed ranges snapshot:
  Total: 975 ranges
  Manifest: 75 ranges
  Continuation: 900 ranges
```

---

## Next: Pass 201+

Continue promoting strong anchors:
1. **AEDE** — calls C302 (promoted), high priority
2. **C275** — calls C5B0 (promoted), near C5AC
3. **CB1A** — near CBAF cluster
4. **BD2D** — weak cluster but calls D364

---

**🎉🎉🎉 PASS 200 MILESTONE! 9 promotions in upper C7, 7 in this session!** 🚀🚀🚀
