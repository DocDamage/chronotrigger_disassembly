# Pass 461: C0:7077..C0:709C (Graphics Handler - Score 6)

**Label:** `CT_C0_7077_GFX_HANDLER_SC6`

**Address:** $C0:7077

**Verification:**
- Score: 6
- Start byte: 0B (PHD)
- Target: C0:7084
- Range: C0:7077..C0:709C (38 bytes)
- **Callers: 2** (C0:0100, C0:01C9)

**Evidence:**
- Graphics/Scroll handler with direct page preservation
- Multiple external callers indicates utility function
- Clean PHD entry with proper stack handling

**Confidence:** High

**Function Type:** Graphics/Scroll Handler
