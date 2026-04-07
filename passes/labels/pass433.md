# Pass 433: C0:F14F..C0:F171 (4 CALLERS)

**Label:** `ct_c0_f14f_4callers`

**Address:** $C0:F14F

**Verification:**
- Score: 4
- Start byte: A2 (LDX immediate - clean start)
- Target: C0:F159
- Range: C0:F14F..C0:F171 (35 bytes)
- **Callers: 4** (C0:F079, C0:F0AB, C0:F0D0, C0:F0F0)

**Evidence:**
- **HIGH CALLER TARGET** - 4 callers from F000 page functions
- Clean instruction start (LDX #imm)
- ASCII ratio: 0.2 (low - code)
- Part of F100 page function cluster

**Confidence:** High (due to high caller count)
