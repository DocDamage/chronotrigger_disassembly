# Pass 469: C0:7546..C0:756B (Graphics Handler - Score 6)

**Label:** `CT_C0_7546_GFX_HANDLER_SC6`

**Address:** $C0:7546

**Verification:**
- Score: 6
- Start byte: 20 (JSR)
- Target: C0:7553
- Range: C0:7546..C0:756B (38 bytes)
- **Callers: 1** weak (C0:74A9)

**Evidence:**
- Graphics/Scroll handler in C0:7500 region
- JSR trampoline to target routine
- Called from C0:74A9 scroll code

**Confidence:** High

**Function Type:** Graphics/Scroll Handler
