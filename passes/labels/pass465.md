# Pass 465: C0:73D9..C0:73FE (Graphics Handler - Score 6)

**Label:** `CT_C0_73D9_GFX_HANDLER_SC6`

**Address:** $C0:73D9

**Verification:**
- Score: 6
- Start byte: A9 (LDA)
- Target: C0:73E6
- Range: C0:73D9..C0:73FE (38 bytes)
- **Callers: 2** (C0:4664, C0:46D8)

**Evidence:**
- Graphics/Scroll handler with immediate load pattern
- Part of C0:7300 scroll control block
- Called from C0:4600 graphics routines

**Confidence:** High

**Function Type:** Graphics/Scroll Handler
