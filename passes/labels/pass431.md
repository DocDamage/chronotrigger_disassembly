# Pass 431: C0:F106..C0:F128 (4 CALLERS)

**Label:** `ct_c0_f106_4callers`

**Address:** $C0:F106

**Verification:**
- Score: 4
- Start byte: A2 (LDX immediate - clean start)
- Target: C0:F110
- Range: C0:F106..C0:F128 (35 bytes)
- **Callers: 4** (C0:F082, C0:F091, C0:F0D6, C0:F0F6)

**Evidence:**
- **HIGH CALLER TARGET** - 4 callers from within F000 page
- Clean instruction start (LDX #imm)
- ASCII ratio: 0.114 (low - code)
- Part of a cluster of related functions in F100 page

**Confidence:** High (due to high caller count)
