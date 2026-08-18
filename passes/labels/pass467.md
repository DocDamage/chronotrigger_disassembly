# Pass 467: C0:74C7..C0:74EC (Graphics Handler - Score 6)

**Label:** `CT_C0_74C7_GFX_HANDLER_SC6`

**Address:** $C0:74C7

**Verification:**
- Score: 6
- Start byte: C2 (REP)
- Target: C0:74D4
- Range: C0:74C7..C0:74EC (38 bytes)
- **Callers: 4** (C0:17AD, C0:1825, C0:184C, C0:261B)

**Evidence:**
- Graphics/Scroll handler with 16-bit mode
- Multiple callers from scroll/map code
- REP #$10/$20 pattern for register width

**Confidence:** High

**Function Type:** Graphics/Scroll Handler (16-bit)
