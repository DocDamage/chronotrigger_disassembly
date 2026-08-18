# Pass 432: C0:F138..C0:F15A (4 CALLERS)

**Label:** `ct_c0_f138_4callers`

**Address:** $C0:F138

**Verification:**
- Score: 4
- Start byte: A2 (LDX immediate - clean start)
- Target: C0:F142
- Range: C0:F138..C0:F15A (35 bytes)
- **Callers: 4** (C0:F07C, C0:F08B, C0:F0AE, C0:F0D3)

**Evidence:**
- **HIGH CALLER TARGET** - 4 callers from F000 page functions
- Clean instruction start (LDX #imm)
- ASCII ratio: 0.2 (low - code)
- Related to F110 and F159 functions

**Confidence:** High (due to high caller count)
