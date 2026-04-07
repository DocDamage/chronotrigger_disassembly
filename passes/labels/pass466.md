# Pass 466: C0:749B..C0:74BE (Graphics Handler - Score 6)

**Label:** `CT_C0_749B_GFX_HANDLER_SC6`

**Address:** $C0:749B

**Verification:**
- Score: 6
- Start byte: 0B (PHD)
- Targets: C0:74A5, C0:74A6 (dual target)
- Range: C0:749B..C0:74BE (36 bytes)
- **Callers: 1** (C0:0A6D)

**Evidence:**
- Graphics/Scroll handler with dual entry points
- Direct page preservation wrapper
- Part of C0:7400 scroll system

**Confidence:** High

**Function Type:** Graphics/Scroll Handler
