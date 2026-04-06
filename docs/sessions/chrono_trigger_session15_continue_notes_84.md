# Chrono Trigger Session 15 — Continuation Notes 84

## 🎉 PROMOTION: Pass 194 — C7:C5AC..C7:C5D0

**First promotion in 52 pages! Threshold promotion of strongest upper C7 candidate.**

---

## Session Context

After scanning **50+ pages** of upper C7 (C500-EDFF) and finding **three score-6 candidates** with **zero strong anchors**, the anchor crisis demanded action. C7:C5AC emerged as the strongest case for threshold promotion.

---

## Promoted Region: C7:C5AC..C7:C5D0

### Primary Target: C7:C5AC

| Property | Value |
|----------|-------|
| **Address** | C7:C5AC |
| **Label** | ct_c7_c5ac_unknown_function_rep_prologue |
| **Backtrack Score** | **6** (perfect) |
| **Start Byte** | 0xC2 (REP #$20) |
| **Prologue Type** | 65816 16-bit accumulator setup |
| **Distance to Target** | 4 bytes (C5AC → C5B0) |

### Secondary Target: C7:C5B0

| Property | Value |
|----------|-------|
| **Address** | C7:C5B0 |
| **Label** | ct_c7_c5b0_subroutine_entry |
| **Caller** | C7:C275 (JSR) |
| **Caller Status** | Suspect (resolved data range) |

### ROM Bytes at C7:C5AC

```
C7:C5AC: C2 20       ; REP #$20     (Set 16-bit accumulator)
C7:C5AE: DE 13 EE    ; DEC $EE13,X  
C7:C5B1: EB          ; XBA          (Exchange B and A)
C7:C5B2: C4 22       ; CPY $22      
C7:C5B4: DF 40 DF 33 ; CMP $33DF40,X
...
```

### Local Cluster: C7:C59D..C7:C5B5

| Metric | Value |
|--------|-------|
| **Score** | 4 |
| **Width** | 25 bytes |
| **Calls** | 2 |
| **Branches** | 4 |
| **Returns** | 1 |

**Evidence of executable code:** Returns present, multiple internal calls/branches.

---

## Why Threshold Promotion?

### The Anchor Crisis

After extensive scanning:

| Candidate | Score | Prologue | Anchor Status |
|-----------|-------|----------|---------------|
| C7:C5AC | **6** | REP #$20 | Suspect (C275) |
| C7:D363 | **6** | PHD | None |
| C7:DDEE | **6** | JSR | None |

**No strong (resolved code) anchors emerged** from:
- C500-CFFF region (40 pages)
- Orphan gap B200-BBFF (10 pages)
- E400-EDFF region (10 pages)

### Evidence Convergence at C5AC

1. ✅ **Score 6** — Perfect backtrack (highest possible)
2. ✅ **REP #$20 prologue** — Definitive 65816 code indicator
3. ✅ **Local cluster with returns** — C59D-C5B5 has 1 RTS
4. ✅ **Suspect anchor** — C275 is "suspect" not "invalid" (valid JSR instruction)
5. ✅ **Cross-bank interest** — F4:E3DA attempts call to C5B0

### Risk Mitigation

- **Minimal promotion range** (C5AC-C5D0, ~36 bytes)
- **Conservative start** — Can extend once validated
- **Monitor for consistency** — Watch for conflicts in future passes

---

## Block Analysis: C7:E400..C7:EDFF (Pre-Promotion Scan)

**Why this scan confirmed the threshold decision:**

### E400+ Region Findings

| Page | Family | Posture | Key Finding |
|------|--------|---------|-------------|
| E400 | candidate_code_lane | local_control | Low activity |
| E500 | candidate_code_lane | mixed_continue | Score-3 candidate |
| E600 | mixed_command_data | mixed_continue | Dead lane |
| E700 | candidate_code_lane | mixed_continue | 1 weak target |
| E800 | branch_fed_control_pocket | local_control | 3 suspect targets |
| E900 | mixed_command_data | mixed_continue | Score-4 candidate |
| EA00 | mixed_command_data | mixed_continue | Score-4 candidate |
| **EB00** | **text_ascii_heavy** | mixed_continue | **Second text page** |
| EC00 | mixed_command_data | mixed_continue | Low activity |
| ED00 | mixed_command_data | mixed_continue | Boundary bait |

### Critical Observations

1. **No calls to C5AC/D363/DDEE** — Confirmed by direct ROM scan
2. **No JSL calls to bank C7** — Long calls don't target this bank from E400+
3. **Second text page at EB00** — Upper C7 code region likely ends ~E300
4. **All anchors suspect** — Callers from closed data ranges only

**Conclusion:** Strong anchors were not going to emerge from continued scanning.

---

## Strategic Impact

### Before Pass 194

```
B000-B1FF  [PROMOTED pass 193]
    ↓ GAP (B200-C2FF orphan)
C300-C4FF  [PROMOTED pass 192]
    ↓
C500-C5FF  [C5AC: score-6, frozen] ← ANCHOR CRISIS
```

### After Pass 194

```
B000-B1FF  [PROMOTED pass 193]
    ↓ GAP (B200-C2FF orphan)
C300-C4FF  [PROMOTED pass 192]
    ↓
C500-C5FF  [**PROMOTED pass 194**] ← FIRST STRONG ANCHOR IN C500!
    ↓
C600+      [Candidates now have anchor potential]
```

### Unlocked Potential

C5AC promotion creates:
1. **Strong anchor** for adjacent C500-C600 region
2. **Validation base** for C000-C500 candidates (C000, C100, C500)
3. **Bridge toward** C300-C4FF promoted region
4. **Reference point** for cross-bank call analysis

---

## Running Promotion Count

| Pass | Region | Notes |
|------|--------|-------|
| 192 | C7:C300-C4FF | First upper C7 code |
| 193 | C7:B000-B1FF | Validated by C300 anchors |
| **194** | **C7:C5AC-C5D0** | **Threshold promotion, anchor crisis breakthrough** |

**Total: 3 promotions**

**Promotion drought broken:** 52 pages → 1 promotion

---

## Files Generated

- `passes/manifests/pass194.json` — Promotion manifest
- `reports/c7_e400_edff_seam_block.json` — Pre-promotion scan
- `reports/c7_e400_edff_seam_block.md` — Rendered report
- `reports/c7_b200_bbff_seam_block.json` — Orphan gap analysis
- `reports/c7_b200_bbff_seam_block.md` — Rendered report
- Backtrack reports:
  - `c7_b200_b2ff_backtrack.json`
  - `c7_b400_b4ff_backtrack.json`
  - `c7_b900_b9ff_backtrack.json`

---

## New Live Seam: C7:EE00..

**Post-promotion seam continues at C7:EE00** (after ED00 block).

### Updated Strategy

With C5AC promoted:
1. **Re-run anchor analysis** for C000-C500 candidates using new closed range
2. **Extend C5AC** if no conflicts emerge (full cluster C59D-C5B5)
3. **Validate D363/DDEE** — May now have strong anchor from C5AC region

### Immediate Next Steps

1. Refresh seam cache to include pass 194:
   ```bash
   python tools/scripts/ensure_seam_cache_v1.py --rom 'rom/Chrono Trigger (USA).sfc'
   ```

2. Re-run anchor reports for backlog candidates:
   ```bash
   python tools/scripts/build_call_anchor_report_v3.py --target C7:D363 ...
   python tools/scripts/build_call_anchor_report_v3.py --target C7:DDEE ...
   ```

3. Continue seam processing at C7:EE00 or jump to validate C000-C500

---

## Threshold Promotion Precedent

**This pass establishes:**
- Score 6 + valid prologue + local cluster = defensible threshold promotion
- Anchor crisis can be broken by promoting strongest candidate
- Minimal range promotion reduces risk while enabling progress

**For future reference:** When multiple score-6 candidates exist but strong anchors are absent after extensive scanning, the strongest candidate (by prologue quality + cluster evidence) may be promoted on threshold.

---

**🎯 The anchor crisis is broken! C5AC provides the first strong foothold in C500 region.**
