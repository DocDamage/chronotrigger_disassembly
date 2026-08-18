# Chrono Trigger Session 15 — Continuation Notes 83

## Block closed: C7:DA00..C7:E3FF (10 pages)

Fourth block of Session 18, continuing through upper C7 bank.

---

## Summary

- **Pages processed:** 10 (DA00-E3FF)
- **Promotions:** 0
- **Page families:** 7 mixed_command_data, 1 branch_fed_control_pocket, 1 candidate_code_lane, **1 text_ascii_heavy**
- **Review postures:** 3 manual_owner_boundary_review, 3 mixed_lane_continue, 3 rejected, 1 local_control_only

---

## 🎯 Key Finding: Fourth Score-6 Candidate!

### C7:DDEE → DDF4

| Property | Value |
|----------|-------|
| **Candidate** | C7:DDEE |
| **Target** | C7:DDF4 |
| **Score** | **6** |
| **Start byte** | **0x20 (JSR!)** |
| **Distance** | 6 bytes |
| **Anchor** | suspect (caller in closed data range) |

**ROM bytes at C7:DDEE:**
```
20 FC DC FD EE 00 33 32 28 40 0E BB CF 0E FE 21
```

**Disassembly:**
```asm
C7:DDEE: 20 FC DC    ; JSR $DCFC
C7:DDF1: FD EE 00    ; SBC $00EE,X
...
```

This is the **fourth score-6 candidate** in upper C7 and the **second with JSR prologue**!

---

## Score-6 Candidates Summary (Upper C7)

| Address | Score | Start | Instruction | Prologue Type | Anchor |
|---------|-------|-------|-------------|---------------|--------|
| C7:C5AC | **6** | 0xC2 | REP #$20 | 65816 setup | Weak |
| C7:D363 | **6** | 0x0B | PHD | Stack setup | Suspect |
| C7:DDEE | **6** | **0x20** | **JSR $DCFC** | **Subroutine call** | Suspect |

**Pattern:** All three have valid code prologues but lack strong (resolved code) anchors.

---

## Other Notable Findings

### C7:E200 — Text/ASCII Heavy Page

**First text-like page encountered in upper C7!**

ROM bytes at C7:E200:
```
43 21 10 78 00 FE CC CD CC E1 23 45 78 55 21 11...
ASCII: C!.x......#ExU!...
```

This page contains ASCII-like patterns interspersed with code-like bytes. Likely contains:
- Dialogue text fragments
- String data
- Mixed text/code regions

**Status:** `mixed_lane_continue` — not a pure code page.

---

### Manual Review Pages

#### C7:DC00 — Multiple score-4 candidates

| Candidate | Target | Score | Start | Byte |
|-----------|--------|-------|-------|------|
| C7:DC07 | C7:DC13 | 4 | 0x48 (PHA) | 12 bytes |
| C7:DC34 | C7:DC40 | 4 | 0x48 (PHA) | 12 bytes |
| C7:DCC4 | C7:DCD4 | 4 | 0x48 (PHA) | 16 bytes |

**Pattern:** Multiple PHA (push accumulator) prologues — classic function entry pattern!

All have **suspect anchors** from closed data ranges.

#### C7:E000 — High activity (14 xref hits)

| Candidate | Target | Score | Note |
|-----------|--------|-------|------|
| C7:E005 | C7:E008 | 4 | — |
| C7:E005 | C7:E00D | 4 | Same start, different targets |

**Activity:** 10 raw targets, 14 xref hits — busy page but suspect anchors only.

#### C7:E100 — Weak target E198

- Score-4 candidate: C7:E188 → E198
- Weak anchor from unresolved code
- Boundary bait at E1FF

---

### Rejected Pages

| Page | Reason | Note |
|------|--------|------|
| C7:DA00 | bad_start_or_dead_lane | 4 targets, hard_bad=1 |
| C7:DE00 | bad_start_or_dead_lane | candidate_code_lane family but rejected |
| C7:DF00 | bad_start_or_dead_lane | branch_fed_control_pocket |

**Impact:** Multiple rejections create gaps in potential D000-E000 code region.

---

## The Anchor Crisis

**Critical observation:** We now have **three score-6 candidates** in upper C7:
- C5AC: REP #$20 prologue
- D363: PHD prologue  
- DDEE: JSR prologue

**All share the same problem:** Callers are in **closed data ranges** or **unresolved bytes**.

**What we need:** Anchors from **promoted code regions** (C7:B000-B1FF or C7:C300-C4FF) to validate these candidates.

**Hypothesis:** The promoted regions (B000-B1FF, C300-C4FF) may contain callers to these upper addresses, but:
1. The callers haven't been disassembled far enough to reveal the JSR/JSL instructions
2. The caller addresses are in gaps between promoted regions (B200-C2FF)

---

## Strategic Analysis

### C7 Bank Status (DA00-E3FF region)

```
DA00-DAFF  [REJECTED]
DB00-DBFF  [mixed_continue]
DC00-DCFF  [manual_review] - 3x PHA prologues (score 4)
DD00-DDFF  [local_control] - DDEE: score-6, JSR prologue ⭐
DE00-DEFF  [REJECTED]
DF00-DFFF  [REJECTED]
E000-E0FF  [manual_review] - 14 hits
E100-E1FF  [manual_review] - weak targets
E200-E2FF  [text_ascii] - First text page!
E300-E3FF  [mixed_continue]
```

### Key Gaps
- **DA00, DE00, DF00 rejected** — fragmentation in D000-E000 region
- **E200 text page** — transition from code to data?

### Contiguity Status
Upper C7 is increasingly fragmented:
- Promoted: B000-B1FF, C300-C4FF
- Candidates: C5AC, D363, DDF4, CEEB, DC13, DC40, DCD4...
- Gaps: CD00, D000, DA00, DE00, DF00 (all rejected)

**Conclusion:** Contiguous code region unlikely. Need **strong anchor validation** for individual promotions.

---

## Running promotion count

- Passes 192-193: 2 promotions
- Notes 80-82: 0 promotions
- **Notes 83: 0 promotions (this note)**

Total promotions: **2**

**Candidate backlog (score ≥6):**
1. C7:C5AC (score 6, REP) — strongest
2. C7:D363 (score 6, PHD) — suspect anchor
3. C7:DDEE (score 6, JSR) — suspect anchor

---

## Files generated

- `reports/c7_da00_e3ff_seam_block.json`
- `reports/c7_da00_e3ff_seam_block.md`
- `reports/c7_dc00_dcff_backtrack.json`
- `reports/c7_dd00_ddff_backtrack.json`
- `reports/c7_e000_e0ff_backtrack.json`
- `reports/c7_e100_e1ff_backtrack.json`

---

## New live seam: C7:E400..

Next block starts at **C7:E400**.

### Status
- Extended C7 coverage through E3FF
- Found **fourth score-6 candidate** (DDF4) with JSR prologue
- First text page at E200
- Multiple rejections fragment D000-E000 region
- **Anchor crisis:** All strong candidates lack resolved code anchors

### Options

1. **Continue linear** (E400+) — extend coverage, hope for strong anchors
2. **Revisit B200-C2FF gap** — the orphan region between promotions
3. **Promote C5AC on threshold** — score 6 + REP prologue = compelling despite weak anchor

### Recommendation

**Continue linear to E400+** but with shifted focus:
- Look specifically for **resolved code anchors** (from C7:B000-B1FF or C7:C300-C4FF)
- If found, they could validate the backlog of score-6 candidates
- The E200 text page suggests we may be approaching data regions

### Next steps

1. `python tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:E400 --pages 10 --json > reports/c7_e400_edff_seam_block.json`
2. Prioritize anchor analysis — look for strong (resolved code) anchors
3. Consider strategic promotion if strong anchor found
4. Write `docs/sessions/chrono_trigger_session15_continue_notes_84.md`

**Three score-6 candidates with valid prologues — we need just one strong anchor to unlock promotions!** 🎯
