# Pass 475: C0:7D66..C0:7D7E (Graphics Handler - 7 CALLERS)

**Label:** `CT_C0_7D66_GFX_HANDLER_7CALLERS`

**Address:** $C0:7D66

**Verification:**
- Score: 4
- Start byte: 86 (STX zp)
- Target: C0:7D66
- Range: C0:7D64..C0:7D7E (27 bytes)
- **Callers: 7**
  - C0:7CDD, C0:7CF1, C0:7D19, C0:7D34, C0:7D51
  - C0:82BD, C0:833D

**Evidence:**
- **HIGH-CALLER** Graphics/Scroll utility
- 7 callers including internal C0:7C00 and external C0:8200+
- Register store pattern (STX)
- Scroll system dispatch target

**Confidence:** Very High

**Function Type:** Graphics/Scroll Utility (High-Caller)
