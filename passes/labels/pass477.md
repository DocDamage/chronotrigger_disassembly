# Pass 477: C0:7F62..C0:7F7A (Graphics Handler - 7 CALLERS)

**Label:** `CT_C0_7F62_GFX_HANDLER_7CALLERS`

**Address:** $C0:7F62

**Verification:**
- Score: 4
- Start byte: 48 (PHA)
- Target: C0:7F62
- Range: C0:7F61..C0:7F7A (26 bytes)
- **Callers: 7**
  - C0:0A9F, C0:0AC0, C0:0AED
  - C0:EAE1, C0:EB01, C0:EB21, C0:EB38

**Evidence:**
- **HIGH-CALLER** Graphics/Scroll utility
- 7 callers from both C0:0000 and C0:EA00+ regions
- Stack preservation entry (PHA)
- Critical scroll/GFX register handler

**Confidence:** Very High

**Function Type:** Graphics/Scroll Utility (High-Caller)
