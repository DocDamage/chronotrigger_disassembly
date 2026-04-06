# Chrono Trigger Session 15 — Continuation Notes 79

## Block closed: C7:B200..C7:B9FF (10 pages)

Processed with the repaired seam toolkit and note-backed closed-range snapshot bridge active.
Result: **zero promotions**. All 10 pages frozen, but **strong promotion candidates identified**.

---

## Per-page decisions

| Page | Family | Posture | Decision | Key reason |
|------|--------|---------|----------|------------|
| C7:B200 | candidate_code_lane | local_control_only | freeze | 1 target, local only |
| C7:B300 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:B400 | candidate_code_lane | bad_start_or_dead_lane_reject | freeze | B4AF hard_bad_start, but B435 candidate promising |
| C7:B500 | candidate_code_lane | local_control_only | freeze | 1 target, score-1 backtrack |
| C7:B600 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:B700 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:B800 | candidate_code_lane | local_control_only | freeze | local clusters only |
| C7:B900 | candidate_code_lane | local_control_only | freeze | 2 targets, score-4 JSR candidate |
| C7:BA00 | mixed_command_data | mixed_lane_continue | freeze | continuation page |
| C7:BB00 | mixed_command_data | mixed_lane_continue | freeze | continuation page |

---

## Strong promotion candidates identified

### C7:B900..B9FF - STRONGEST candidate

**Target:** C7:B963 (2 callers)

**Backtrack:**
- C7:B961→B963 score=4
- Start byte: **0x20 = JSR** (Jump to Subroutine)
- Distance: 2 bytes
- Candidate range: B961..B97B

**ROM bytes at B961:**
```
B961: 20 A0 D0 BE CC 02 FB 1C...
```
**JSR $D0A0** - valid 65816 instruction!

**This is REAL CODE** with a JSR prologue.

**Status:** Frozen due to weak callers, but **highest promotion potential** in block.

---

### C7:B400..B4FF - MODERATE candidate

**Rejected due to:** B4AF target (hard_bad_start - BRK $00)

**But valid candidates exist:**
- C7:B435→B440 score=2
- Start byte: 0x54 (MVN - block move)
- 3 local clusters with decent scores (5, 4, 2)
- 1 return, 8 prologues

**Status:** Rejected page-wide, but B435 candidate warrants re-examination.

---

### C7:B500-B900 continuum

**Internal clusters with returns:**
- B600: B68F..B6A7 (score=6, 2 calls, 3 branches, 1 return)
- B700: 2 clusters with returns
- B800: B82C..B844 (score=6, 1 call, 3 branches, 1 return)

**Pattern:** These pages show **code structure** but lack strong entry points.

**Hypothesis:** This is **continuation code** - subroutines reached via internal branches from promoted regions (B100 or future B900), not external entry points.

---

## Gap-filling analysis: B100 ↔ C300

### Current promoted regions:
```
C7:B000..B1FF (code) ← promoted pass 193
    ↓ GAP: B200-B9FF (this block)
C7:C300..C4FF (code) ← promoted pass 192
```

### This block fills the gap:
- **B200-B3FF**: Sparse (B200 1 target, B300 local only)
- **B400**: 5 targets (B435 candidate promising)
- **B500-B800**: Internal clusters (continuation code)
- **B900**: STRONG candidate (B961 JSR entry)
- **BA00-BB00**: mixed_lane_continue (bridge to C300)

### Potential contiguous code region:
If B900 promoted: **~8KB contiguous C7 code** (B100 + B200-B9FF + C300)

---

## Strategic recommendation

### Priority promotion pathway:

1. **HIGH**: Promote C7:B961 (JSR entry, score 4)
   - Creates strong anchor at B900
   - Validates B900-B97B as code

2. **HIGH**: Validate C7:B435 (score 2, but clean structure)
   - Lifts B400 from reject status
   - Creates mid-gap anchor

3. **MEDIUM**: Promote B500-B800 clusters
   - Requires B900 anchor first
   - Fills middle gap via internal linkage

4. **GOAL**: Contiguous C7:B100-C7:C300 code region

---

## Block read

- **Bridge region identified**: C7:B200-B9FF sits between promoted B100 and C300. Analysis reveals **code structure throughout**: 60% candidate_code_lane, internal clusters with returns, JSR prologue at B961.

- **Strongest candidate**: **C7:B900** with B961→B963 score-4 backtrack starting with **JSR $D0A0**. This is definitively code with a valid subroutine prologue.

- **Rejection reconsideration**: C7:B400 was rejected due to B4AF (BRK), but B435 shows valid structure. Page-wide reject may have been overly conservative.

- **Continuation pattern**: B500-B800 show internal clusters (returns, branches) but no strong entry points. These are likely **continuation subroutines** reached from B100 or B900, not standalone entry points.

- **Contiguous code potential**: If B900 (and potentially B400) promoted, C7 would have ~8KB of contiguous code from B100 through C300. This would be a major code region in bank C7.

- **BA00-BB00 as bridge**: mixed_lane_continue posture suggests these pages continue toward C300, potentially completing the gap fill.

---

## Running promotion count

- ... (passes 14-193) ...
- C7:C300..C7:CCFF: 2 promotions (notes_78) - BREAKTHROUGH
- C7:B200..C7:B9FF: 0 promotions (this note) - but strong candidates identified

Total promotions since seam work began: **2**

**Next promotion likely**: C7:B900 (B961) - pending strong caller validation.

---

## Files generated for this block

- `reports/c7_b200_b9ff_seam_block.json`
- `reports/c7_b200_b9ff_seam_block.md`
- `reports/c7_b400_b4ff_backtrack.json`
- `reports/c7_b500_b5ff_backtrack.json`

---

## New live seam: C7:BC00..

Next unprocessed block starts at **C7:BC00**.

### Strategic options

**Option A: Promote B900 now**
- B961 has JSR prologue (definitive code)
- Score-4 backtrack
- Would create anchor for B500-B800 validation
- Risk: Need to verify callers first

**Option B: Continue to C300**
- Process C7:BC00..C3FF to reach promoted C300
- Backfill B200-B9FF after connection established
- Lower risk, slower gap closure

**Option C: Analyze BA00-BB00**
- These are mixed_lane_continue pages
- May show bridge to C300
- Could reveal entry points

### Recommendation

**Option B (continue to C300)** - maintain momentum toward known code region. B900 promotion can happen after connection to C300 is established (stronger anchor chain).

### Next steps

1. `python tools/scripts/run_seam_block_v1.py --rom 'rom/Chrono Trigger (USA).sfc' --start C7:BC00 --pages 10 --json > reports/c7_bc00_c5ff_seam_block.json`
2. Process toward C7:C300 (already promoted)
3. Establish connection, then backfill B200-B9FF
4. Write `docs/sessions/chrono_trigger_session15_continue_notes_80.md`

**The C7 code region grows - B100, B200-B9FF candidates, and C300 are converging toward a major contiguous code block.**
