# Chrono Trigger Session 15 — Continuation Notes 81

## Block closed: C7:C600..C7:CFFF (10 pages)

Continued extending C7 bank coverage beyond the C500 region where we found the score-6 C5AC candidate.

---

## Summary

- **Pages processed:** 10 (C600-CFFF)
- **Promotions:** 0
- **Page families:** 8 candidate_code_lane, 2 mixed_command_data
- **Review postures:** 2 manual_owner_boundary_review, 4 local_control_only, 3 mixed_lane_continue, 1 rejected

---

## Key Findings

### Manual Review Pages

#### C7:C800 — Score-4 candidate C8B6
| Property | Value |
|----------|-------|
| **Target** | C7:C8B6 |
| **Candidate** | C7:C8AF |
| **Score** | 4 |
| **Start byte** | 0xA0 (LDY #imm) |
| **Distance** | 7 bytes |
| **Anchor** | 1 weak (JSL from CC:0D16) |

**ROM bytes at C7:C8AF:**
```
A0 FC 12 63 CE 01 26 EC 3F A0 FF 0E EE 03 23 DC D0...
```

- Clean start byte (A0 = LDY immediate)
- Local cluster at C7:C860..C7:C86D (score 2, 1 branch, 1 return)
- **Frozen:** Only weak anchor support

#### C7:CE00 — Multiple score-4 candidates

| Candidate | Target | Score | Start Byte | Class | Anchor |
|-----------|--------|-------|------------|-------|--------|
| C7:CE95 | C7:CEA0 | 4 | 0x15 (ORA dp,X) | clean | suspect (data range) |
| C7:CEA5 | C7:CEB0 | 4 | 0xF3 (SBC (S),Y) | clean | suspect (data range) |
| **C7:CEE9** | **C7:CEEB** | **4** | **0xC2 (REP #imm)** | **clean** | **weak** |
| C7:CE03 | C7:CE0E | 2 | 0xF0 (BEQ rel) | clean | — |

**Most interesting: C7:CEEB with REP prologue**
- Start byte 0xC2 = `REP #$20` — classic 65816 function prologue
- Weak anchor from C7:E32F (unresolved bytes)
- Local cluster: C7:CEB1..C7:CEBA (score 3, 1 call, 1 return)

**ROM bytes at C7:CEE9:**
```
C2 20 ...  ; REP #$20 - sets 16-bit accumulator mode
```

This is the **second REP prologue** found in upper C7 (after C5AC's score-6 candidate)!

---

## Rejected Page: C7:CD00

**Status:** `bad_start_or_dead_lane_reject`

Despite rejection, C7:CD00 showed multiple score-4 backtrack candidates:
- C7:CD09→C7:CD17 (score 4)
- C7:CD1B→C7:CD20 (score 4) 
- C7:CDE4→C7:CDEB (score 4)

**Impact on contiguity:**
- CD00 sits between CC00 (local_control_only) and CE00 (manual_review)
- If CD00 has actual code, it would bridge this region
- **Contiguity broken at CD00** — prevents C600-CFFF contiguous promotion

---

## Local Clusters Summary

| Cluster | Page | Score | Width | Calls | Branches | Returns |
|---------|------|-------|-------|-------|----------|---------|
| C7:C860..C7:C86D | C800 | 2 | 14 bytes | 0 | 1 | 1 |
| C7:CA7E..C7:CA96 | CA00 | — | — | — | — | — |
| C7:CAC1..C7:CAD9 | CA00 | — | — | — | — | — |
| C7:CBAF..C7:CBC7 | CB00 | — | — | — | — | — |
| C7:CCA3..C7:CCAD | CC00 | — | — | — | — | — |
| C7:CE1B..C7:CE33 | CE00 | 6 | 25 bytes | 2 | 0 | 1 |
| C7:CEB1..C7:CEBA | CE00 | 3 | 10 bytes | 1 | 0 | 1 |
| C7:CEA4..C7:CEAD | CE00 | 2 | 10 bytes | 0 | 1 | 1 |
| C7:CF61..C7:CF6F | CF00 | — | — | — | — | — |

**Strongest cluster: C7:CE1B** (score 6, 2 calls, 1 return) — excellent code indicators!

---

## Strategic Analysis

### Current C7 Code Map
```
B000-B1FF  [PROMOTED pass 193]
    ↓ GAP: B200-C2FF (orphan)
C300-C4FF  [PROMOTED pass 192]
    ↓
C500-C5FF  [C5AC: score-6, REP prologue]
    ↓
C600-C6FF  [mixed_command_data]
C700-C7FF  [mixed_command_data]
C800-C8FF  [C8B6: score-4, weak anchor]
C900-C9FF  [candidate_code_lane]
CA00-CAFF  [local_control_only]
CB00-CBFF  [local_control_only]
CC00-CCFF  [local_control_only]
CD00-CDFF  [REJECTED - bad_start]
CE00-CEFF  [CEEB: score-4, REP prologue]
CF00-CFFF  [local_control_only]
```

### Pattern Recognition: REP Prologues
We've now found **two REP #$20 prologues** in upper C7:
1. **C7:C5AC** (score 6) — highest backtrack score in C7 bank
2. **C7:CEE9** (score 4) — clean prologue, weak anchor

Both indicate 65816 code that sets 16-bit accumulator mode at function entry — classic subroutine structure.

### Contiguity Challenges
- **C7:CD00 rejection** breaks C600-CFFF contiguous code possibility
- **C7:C200-C2FF orphan** still unresolved between promoted regions
- **Strategy:** Need to resolve individual strong candidates rather than contiguous blocks

---

## Running promotion count

- Passes 192-193: 2 promotions (C7:B000-B1FF, C7:C300-C4FF)
- C7:BC00..C7:C5FF: 0 promotions (notes_80)
- **C7:C600..C7:CFFF: 0 promotions (this note)**

Total promotions: **2**

**Next likely promotions:**
1. C7:C5AC (score 6, REP prologue) — pending strong caller
2. C7:CEEB (score 4, REP prologue) — needs anchor validation

---

## Files generated

- `reports/c7_c600_cfff_seam_block.json`
- `reports/c7_c600_cfff_seam_block.md`
- `reports/c7_c800_c8ff_backtrack.json`
- `reports/c7_ce00_ceff_backtrack.json`
- `reports/C7_C8B6_anchor.json`
- `reports/C7_CEA0_anchor.json`
- `reports/C7_CEEB_anchor.json` (implied from analysis)

---

## New live seam: C7:D000..

Next block starts at **C7:D000**.

### Status
- Extended C7 coverage to CFFF
- Found second REP prologue (CEEB)
- Strong local clusters present
- CD00 rejection breaks contiguous promotion

### Options
1. **Continue linear** (C7:D000..) — extend coverage toward D800
2. **Promote C5AC** — strongest candidate (score 6)
3. **Revisit CD00** — check if rejection was correct

### Recommendation
**Continue linear** to build more context. The pattern of REP prologues and strong clusters suggests real code in C600-CFFF that needs validation from additional coverage.

### Next steps
1. `python tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:D000 --pages 10 --json > reports/c7_d000_d9ff_seam_block.json`
2. Look for anchors to existing candidates (C5AC, C8B6, CEEB)
3. Write `docs/sessions/chrono_trigger_session15_continue_notes_82.md`

**The C7 bank continues to show strong code indicators with REP prologues and high-scoring clusters!** 🚀
