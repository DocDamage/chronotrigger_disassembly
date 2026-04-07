# Pass 449: C0:E2AA..C0:E2C2 (MODE SETUP - 4 CALLERS)

**Label:** `ct_c0_e2aa_mode_setup_score6`

**Address:** $C0:E2AA

**Verification:**
- Score: 6
- Start byte: A9 (LDA immediate)
- Target: C0:E2AA
- Range: C0:E2AA..C0:E2C2 (25 bytes)
- **Callers: 4** (weak)

**Evidence:**
- Processor mode setup with REP/SEP pattern
- RTS at E2C2 confirms function boundary
- Part of E200 utility function block

**Confidence:** High

**Function Type:** Processor Mode Setup

**Notes:**
Utility function for setting processor flags and modes. Called from 4 locations in the main codebase.
