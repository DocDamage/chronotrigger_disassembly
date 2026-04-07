# Pass 473: C0:79CF..C0:79E7 (Graphics Handler - 10 CALLERS)

**Label:** `CT_C0_79CF_GFX_HANDLER_10CALLERS`

**Address:** $C0:79CF

**Verification:**
- Score: 4
- Start byte: 85 (STA zp)
- Target: C0:79CF
- Range: C0:79CD..C0:79E7 (27 bytes)
- **Callers: 10** - MAJOR HUB
  - C0:7925, C0:793D, C0:795A, C0:7982, C0:799D
  - C0:79BA, C0:827D, C0:829D, C0:82FD, C0:831D

**Evidence:**
- **HIGH-CALLER** Critical scroll/graphics utility
- 10 callers - most in C0:7000-8000 region
- Central dispatch/function hub
- Called from both internal and external scroll code

**Confidence:** Very High

**Function Type:** Graphics/Scroll Utility Hub (Major)
