# Pass 429: C0:F41D..C0:F445

**Label:** `ct_c0_f41d_score6`

**Address:** $C0:F41D

**Verification:**
- Score: 6 (high confidence)
- Start byte: 0B (PHD - clean start)
- Target: C0:F42D
- Range: C0:F41D..C0:F445 (41 bytes)

**Evidence:**
- Clean instruction start (PHD - push direct page register)
- ASCII ratio: 0.39 (moderate)
- Called from C7:BF6A
- Verified through owner backtrack analysis

**Confidence:** High
