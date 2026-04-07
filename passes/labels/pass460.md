# Pass 460: C0:704B..C0:706E (Graphics Handler - Score 6)

**Label:** `CT_C0_704B_GFX_HANDLER_SC6`

**Address:** $C0:704B

**Verification:**
- Score: 6
- Start byte: 20 (JSR)
- Target: C0:7056
- Range: C0:704B..C0:706E (36 bytes)
- **Callers: 1** (suspect)

**Evidence:**
- Graphics/Scroll handler in C0:7000 region
- Clean JSR entry point
- Part of scroll control system

**Confidence:** High

**Function Type:** Graphics/Scroll Handler
