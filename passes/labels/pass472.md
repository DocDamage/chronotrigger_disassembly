# Pass 472: C0:77DB..C0:77FC (Graphics Handler - Score 6)

**Label:** `CT_C0_77DB_GFX_HANDLER_SC6`

**Address:** $C0:77DB

**Verification:**
- Score: 6
- Start byte: 20 (JSR)
- Target: C0:77E4
- Range: C0:77DB..C0:77FC (34 bytes)
- **Callers: 2** weak (C0:835D, C0:83DD)

**Evidence:**
- Graphics/Scroll handler in C0:7700 region
- JSR entry with RTS exit
- Called from C0:8300+ scroll routines

**Confidence:** High

**Function Type:** Graphics/Scroll Handler
