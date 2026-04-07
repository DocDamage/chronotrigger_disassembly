# Pass 452: C0:E5A5..C0:E5BD (REGISTER SAVE - 6 CALLERS)

**Label:** `ct_c0_e5a5_register_save_score6`

**Address:** $C0:E5A5

**Verification:**
- Score: 6
- Start byte: 8D (STA abs)
- Target: C0:E5A5
- Range: C0:E5A5..C0:E5BD (25 bytes)
- **Callers: 6** (weak)

**Evidence:**
- Register preservation helper
- Called from multiple locations in main code
- Part of E500 utility block

**Confidence:** High

**Function Type:** Register Preservation Helper
