# Pass 468: C0:74E2..C0:74FF (Graphics Handler - Score 6)

**Label:** `CT_C0_74E2_GFX_HANDLER_SC6`

**Address:** $C0:74E2

**Verification:**
- Score: 6
- Start byte: 20 (JSR)
- Target: C0:74E8
- Range: C0:74E2..C0:74FF (30 bytes)
- **Callers: 3** (C0:17D6, C0:1828, C0:265C)

**Evidence:**
- Graphics/Scroll handler with JSR entry
- Part of scroll update system
- Multiple map-related callers

**Confidence:** High

**Function Type:** Graphics/Scroll Handler
