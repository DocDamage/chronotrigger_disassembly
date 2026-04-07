# Pass 476: C0:7F43..C0:7F60 (Graphics Handler - Score 6)

**Label:** `CT_C0_7F43_GFX_HANDLER_SC6`

**Address:** $C0:7F43

**Verification:**
- Score: 6
- Start byte: 20 (JSR)
- Targets: C0:7F48, C0:7F4C (dual)
- Range: C0:7F43..C0:7F60 (30 bytes)
- **Callers: 2** (C0:D996, C0:DC55)

**Evidence:**
- Graphics/Scroll handler in C0:7F00 region
- Dual target pattern (nearby entries)
- Called from C0:D000 and C0:DC00 range

**Confidence:** High

**Function Type:** Graphics/Scroll Handler
