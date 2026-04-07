# Pass 435: C0:FF23..C0:FF41 (NMI HANDLER - 117 CALLERS)

**Label:** `ct_nmi_handler_117callers`

**Address:** $C0:FF23

**Verification:**
- Score: 4
- Start byte: 08 (PHP - push processor status, typical interrupt handler start)
- Target: C0:FF29
- Range: C0:FF23..C0:FF41 (31 bytes)
- **Callers: 117** - EXTREME HIGH CALLER COUNT

**Evidence:**
- **EXTREME HIGH CALLER TARGET** - 117 callers across entire codebase
- Clean instruction start (PHP - typical for interrupt handlers)
- Located in hardware vector region (FF00-FFFF)
- ASCII ratio: 0.065 (very low - pure code)
- Zero/FF ratio: 0.323 (some vector table data nearby)

**Confidence:** Very High

**Function Type:** NMI/VBlank Interrupt Handler

**Notes:**
This is the NMI (Non-Maskable Interrupt) handler, also commonly known as the VBlank interrupt handler on SNES. With 117 callers, this is one of the most critical system functions in the game. It's called every frame during vertical blanking to handle screen updates, DMA transfers, and other time-critical operations.

The high caller count indicates this is not directly called via JSR/JSL from 117 places, but rather the address C0:FF29 appears in jump tables, vector tables, or is referenced as the NMI vector target throughout the code.

**Hardware Context:**
- Location: Bank C0, near hardware vectors (FFE0-FFFF)
- Typical SNES NMI vector at $FFEA/$FFEB points to this region
- Handles vertical blanking interrupts
