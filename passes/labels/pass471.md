# Pass 471: C0:7604..C0:762A (Graphics Handler - Score 6)

**Label:** `CT_C0_7604_GFX_HANDLER_SC6`

**Address:** $C0:7604

**Verification:**
- Score: 6
- Start byte: A9 (LDA)
- Target: C0:7612
- Range: C0:7604..C0:762A (39 bytes)
- **Callers: 3** (C0:7608, C0:825B, C0:82DD)

**Evidence:**
- Graphics/Scroll handler with immediate load
- Part of C0:7600 scroll control block
- Multiple callers including C0:8200+ routines

**Confidence:** High

**Function Type:** Graphics/Scroll Handler
