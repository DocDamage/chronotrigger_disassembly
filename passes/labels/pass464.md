# Pass 464: C0:739B..C0:73BD (Graphics Handler - Score 6)

**Label:** `CT_C0_739B_GFX_HANDLER_SC6`

**Address:** $C0:739B

**Verification:**
- Score: 6
- Start byte: 0B (PHD)
- Target: C0:73A5
- Range: C0:739B..C0:73BD (35 bytes)
- **Callers: 2** (C0:463A, C0:4685)

**Evidence:**
- Graphics/Scroll handler in C0:7300 region
- Direct page stack operations
- Multiple callers from C0:4600 range

**Confidence:** High

**Function Type:** Graphics/Scroll Handler
