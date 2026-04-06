# Chrono Trigger Session 15 — Continuation Notes 82

## Block closed: C7:D000..C7:D9FF (10 pages)

Third block of Session 18, extending deeper into C7 bank.

---

## Summary

- **Pages processed:** 10 (D000-D9FF)
- **Promotions:** 0
- **Page families:** 8 mixed_command_data, 1 candidate_code_lane, 1 branch_fed_control_pocket
- **Review postures:** 2 manual_owner_boundary_review, 3 local_control_only, 4 mixed_lane_continue, 1 rejected

---

## Key Findings

### Score-6 Candidate: C7:D363 → D364

| Property | Value |
|----------|-------|
| **Candidate** | C7:D363 |
| **Target** | C7:D364 |
| **Score** | **6** |
| **Start byte** | 0x0B (PHD - Push Direct Page Register) |
| **Distance** | 1 byte |
| **Anchor** | suspect (caller in closed data range) |

**ROM bytes at C7:D363:**
```
0B D2 62 EE FD D2 40 78 DE 22 0F 01 13 1E BD 04...
```

**Analysis:**
- Start byte 0x0B = `PHD` — valid 65816 instruction (pushes direct page register)
- Not a typical function prologue, but valid code
- **Suspect anchor** from C7:BD2D (caller in closed data range C7:BD00..C7:BDFF)
- **Frozen** — no strong promotion case

This is the **third score-6 candidate** found in upper C7 bank!

---

### Manual Review Pages

#### C7:D100 — Score-4 candidate D1ED

| Property | Value |
|----------|-------|
| **Candidate** | C7:D1DF |
| **Target** | C7:D1ED |
| **Score** | 4 |
| **Start byte** | **0x20 (JSR!)** |
| **Distance** | 14 bytes |

**ROM bytes at C7:D1DF:**
```
20 EE 15 4C B0 32 0E EF 78 E2 41 E2 2F ED D1 41...
```

**Analysis:**
- Start byte 0x20 = `JSR` — excellent code indicator!
- This is a subroutine call, suggesting the bytes before D1ED form a callable function
- **Suspect anchor** from C7:985A (caller in closed data range)
- **Frozen** — strong internal evidence but weak external validation

#### C7:D300 — Mixed results

- Best candidate: C7:D363→D364 (score 6, detailed above)
- Secondary: C7:D305→D30C (score 2, start 0xF0 = BEQ)
- Local clusters present but no strong anchors

---

### Rejected Page: C7:D000

**Status:** `bad_start_or_dead_lane_reject`

Despite **19 xref hits** — the highest in this block — C7:D000 was rejected.

**ROM bytes at C7:D000:**
```
CC 98 03 30 EF 00 00 10 01 DE 84 E3 63 EF 41 BC...
```

**Analysis:**
- Start byte 0xCC = `INY` (increment Y)
- Multiple score-4 backtrack candidates exist:
  - C7:D093→D0A0 (score 4)
  - C7:D0A7→D0B0 (score 4)
  - C7:D0D0→D0D4 (score 4)
- But page-level classification rejected due to overall structure

**Impact:** Another gap in potential C7 code regions.

---

## Score-6 Candidate Pattern

We've now found **three score-6 candidates** in upper C7:

| Address | Score | Start Byte | Instruction | Anchor Status |
|---------|-------|------------|-------------|---------------|
| C7:C5AC | **6** | 0xC2 | REP #$20 | Weak (unresolved) |
| C7:D363 | **6** | 0x0B | PHD | Suspect (data range) |
| C7:CE95 | 4 | 0x15 | ORA dp,X | Suspect (data range) |

**Pattern:** High backtrack scores indicate valid code structure, but:
- All lack strong (resolved code) anchors
- All are frozen pending better caller evidence

---

## Strategic Analysis

### C7 Bank Status (D000-D9FF region)

```
D000-D0FF  [REJECTED] - 19 hits but bad structure
D100-D1FF  [manual_review] - D1ED has JSR prologue!
D200-D2FF  [local_control] - clusters present
D300-D3FF  [manual_review] - D363 score-6
D400-D4FF  [mixed_continue]
D500-D5FF  [local_control] - clusters
D600-D6FF  [mixed_continue]
D700-D7FF  [control_pocket]
D800-D8FF  [local_control] - clusters
D900-D9FF  [mixed_continue]
```

### Contiguity Challenges

- **D000 rejection** breaks potential C000-DFFF contiguous code
- **CD00 rejection** (notes_81) already broke C600-CFFF
- Pattern: Even high-activity pages (19 hits at D000) can fail structure validation

### The "JSR Prologue" Discovery at D1ED

C7:D1ED is interesting because its backtrack candidate starts with **0x20 = JSR**. This means:
- The bytes at D1DF form a `JSR $15EE` instruction
- This is a **subroutine call within the candidate region**
- Suggests legitimate code structure (functions calling other functions)

Unfortunately, the anchor from C7:985A is suspect (caller in closed data range).

---

## Running promotion count

- Passes 192-193: 2 promotions (C7:B000-B1FF, C7:C300-C4FF)
- Notes 80-81: 0 promotions
- **Notes 82: 0 promotions (this note)**

Total promotions: **2**

**Candidate backlog:**
1. C7:C5AC (score 6, REP prologue) — strongest
2. C7:D363 (score 6, PHD start) — suspect anchor
3. C7:D1ED (JSR prologue) — suspect anchor
4. C7:CEEB (REP prologue) — weak anchor

---

## Files generated

- `reports/c7_d000_d9ff_seam_block.json`
- `reports/c7_d000_d9ff_seam_block.md`
- `reports/c7_d100_d1ff_backtrack.json`
- `reports/c7_d300_d3ff_backtrack.json`
- Anchor reports (stdout capture):
  - C7:D364: suspect anchor from BD2D
  - C7:D1ED: suspect anchor from 985A

---

## New live seam: C7:DA00..

Next block starts at **C7:DA00**.

### Status
- Extended C7 coverage through D9FF
- Found third score-6 candidate (D363)
- Discovered JSR prologue pattern (D1ED)
- D000 rejection creates another gap

### Upper C7 Pattern Summary

| Region | Status | Key Findings |
|--------|--------|--------------|
| C5xx | candidate | C5AC: score-6, REP prologue |
| C6xx-C8xx | mixed/candidate | C8B6: score-4 |
| C9xx-CBxx | candidate | Local clusters |
| CCxx | candidate | — |
| CDxx | **REJECTED** | Gap |
| CExx | candidate | CEEB: REP prologue |
| CFxx | candidate | — |
| D0xx | **REJECTED** | Gap (19 hits!) |
| D1xx | candidate | D1ED: JSR prologue |
| D2xx-D3xx | candidate/clusters | D363: score-6 |
| D4xx-D9xx | mixed/control | Local clusters |

### Recommendation

**Continue linear** to DA00+ to:
- Build more context for D363 and D1ED
- Look for anchors calling back into D000-D3FF region
- Potentially find connections to earlier candidates

### Next steps

1. `python tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:DA00 --pages 10 --json > reports/c7_da00_e3ff_seam_block.json`
2. Look for strong anchors to D363/D1ED
3. Write `docs/sessions/chrono_trigger_session15_continue_notes_83.md`

**Upper C7 is rich with high-scoring candidates — we need strong anchors to unlock promotions!** 🔍
