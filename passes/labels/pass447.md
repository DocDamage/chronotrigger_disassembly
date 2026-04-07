# Pass 447: C0:E687..C0:E69C (STATE LOADER - 15 CALLERS)

**Label:** `ct_c0_e687_state_loader_score6`

**Address:** $C0:E687

**Verification:**
- Score: 6 (backtrack from target E687, candidate start at E682 with C2 20 - REP #$20)
- Actual function starts at E687
- Target: C0:E687
- Range: C0:E687..C0:E69C (22 bytes)
- **Callers: 15** (weak) - HIGH CALLER COUNT

**Evidence:**
- High caller target with 15 cross-references
- State loading/initialization pattern
- RTS at E69C confirms function boundary
- Pass353 covers E682-E686 (REP #$20 setup stub), this is the main function

**Confidence:** High

**Function Type:** State Loading / Initialization

**Notes:**
This is the main state loading function at E687. The preceding bytes at E682-E686 form a small setup stub (REP #$20 / RTS) covered by pass353. This function is called from 15 locations, indicating it's a core state management routine.

**Callers include:**
- C0:CC64, C0:CF84, C0:D2F0, C0:D35C, C0:D5AC, C0:D5EB, C0:D66E, C0:D6DC, C0:D71B, C0:D789, C0:D7C8, C0:D834, C0:DAB8, C0:DAF3, C0:E182
