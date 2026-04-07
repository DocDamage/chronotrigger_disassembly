# Pass 451: C0:E4A9..C0:E4C1 (DMA HELPER - 3 CALLERS)

**Label:** `ct_c0_e4a9_dma_helper_score6`

**Address:** $C0:E4A9

**Verification:**
- Score: 6
- Start byte: A9 (LDA immediate)
- Target: C0:E4A9
- Range: C0:E4A9..C0:E4C1 (25 bytes)
- **Callers: 3** (weak)

**Evidence:**
- DMA transfer helper function
- RTS at E4C1 confirms function boundary
- Part of E400 utility block

**Confidence:** High

**Function Type:** DMA Transfer Helper
