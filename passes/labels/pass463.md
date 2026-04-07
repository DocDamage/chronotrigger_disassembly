# Pass 463: C0:7162..C0:7188 (Graphics Handler - Score 6)

**Label:** `CT_C0_7162_GFX_HANDLER_SC6`

**Address:** $C0:7162

**Verification:**
- Score: 6
- Start byte: 0B (PHD)
- Target: C0:7170
- Range: C0:7162..C0:7188 (39 bytes)
- **Callers: 2** weak (C0:A905, C0:B188)

**Evidence:**
- Graphics/Scroll handler with stack frame setup
- Multiple callers from high bank regions
- PHD/PLD wrapper pattern

**Confidence:** High

**Function Type:** Graphics/Scroll Handler
