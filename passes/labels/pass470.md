# Pass 470: C0:75E9..C0:75FF (Graphics Handler - 6 CALLERS)

**Label:** `CT_C0_75E9_GFX_HANDLER_6CALLERS`

**Address:** $C0:75E9

**Verification:**
- Score: 6
- Start byte: 20 (JSR)
- Target: C0:75E9
- Range: C0:75E7..C0:75FF (25 bytes)
- **Callers: 6** (C0:17A9, C0:17FE, C0:183E, C0:2617, C0:2658, C0:0A96)

**Evidence:**
- **HIGH-CALLER** Graphics/Scroll handler
- 6 callers from scroll/map system
- Score 6 backtrack with JSR entry
- Major utility in C0:7500 region

**Confidence:** Very High

**Function Type:** Graphics/Scroll Utility (High-Caller)
