# Pass 474: C0:7BA0..C0:7BC1 (Graphics Handler - Score 6)

**Label:** `CT_C0_7BA0_GFX_HANDLER_SC6`

**Address:** $C0:7BA0

**Verification:**
- Score: 6
- Start byte: 20 (JSR)
- Target: C0:7BA9
- Range: C0:7BA0..C0:7BC1 (34 bytes)
- **Callers: 4** (C0:837D, C0:839D, C0:83FD, C0:841D)

**Evidence:**
- Graphics/Scroll handler with multiple callers
- Part of C0:7B00 scroll control region
- Called from C0:8300+ dispatch routines

**Confidence:** High

**Function Type:** Graphics/Scroll Handler
