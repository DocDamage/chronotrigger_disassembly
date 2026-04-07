# Pass 425: C0:F0B9..C0:F0E1

**Label:** `ct_c0_f0b9_score6`

**Address:** $C0:F0B9

**Verification:**
- Score: 6 (high confidence)
- Start byte: A2 (LDX immediate - clean start)
- Target: C0:F0C9
- Range: C0:F0B9..C0:F0E1 (41 bytes)

**Evidence:**
- Clean instruction start (LDX #imm)
- ASCII ratio: 0.244 (low - likely code)
- Zero/FF ratio: 0.0 (no padding)
- Verified through owner backtrack analysis

**Confidence:** High
