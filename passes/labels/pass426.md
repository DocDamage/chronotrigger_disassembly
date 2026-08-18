# Pass 426: C0:F11D..C0:F143

**Label:** `ct_c0_f11d_score6_4callers`

**Address:** $C0:F11D

**Verification:**
- Score: 6 (high confidence)
- Start byte: A2 (LDX immediate - clean start)
- Target: C0:F12B
- Range: C0:F11D..C0:F143 (39 bytes)
- Callers: 4 (C0:F082, C0:F091, C0:F0D6, C0:F0F6)

**Evidence:**
- High caller count (4 callers)
- Clean instruction start (LDX #imm)
- Called from multiple locations in C0:F000 page
- ASCII ratio: 0.128 (low - likely code)

**Confidence:** High
