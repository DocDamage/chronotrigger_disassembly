# Pass 448: C0:E87F..C0:E886 (JUMP HANDLER - 24 CALLERS)

**Label:** `ct_c0_e87f_jump_handler_score6`

**Address:** $C0:E87F

**Verification:**
- Score: 6
- Start byte: E8 (INX)
- Target: C0:E87F
- Range: C0:E87F..C0:E886 (8 bytes)
- **Callers: 24** (weak) - HIGHEST CALLER COUNT in E-region

**Evidence:**
- EXTREME HIGH CALLER target with 24 cross-references
- Jump table handler or trampoline function
- RTS at E886 confirms function boundary
- Short 8-byte function suggests simple dispatch/translation

**Confidence:** High

**Function Type:** Jump Table Handler / Trampoline

**Notes:**
This is the highest-caller function in the E800 region with 24 callers. The very short length (8 bytes) suggests this is likely a jump table entry point, trampoline, or simple register translation function used throughout the game engine.

**Callers include:**
- C0:3719, C0:3786, C0:37B7, C0:37CD, C0:37E9, C0:37FF, C0:382D, C0:3861, C0:387A, C0:3893, C0:38C4, C0:38D9, C0:38EE, C0:391F, C0:3952, C0:3A0B, C0:3A6E, C0:3A74, C0:3CD4, C0:3F4A, C0:62FE, C0:6334, C0:638F, C0:63CE
