# Pass 446: C0:E534..C0:E54B (DATA HANDLER - 15 CALLERS)

**Label:** `ct_c0_e534_data_handler_score6`

**Address:** $C0:E534

**Verification:**
- Score: 6 (backtrack from target)
- Start byte: 0E (ASL abs)
- Target: C0:E534
- Range: C0:E534..C0:E54B (24 bytes)
- **Callers: 15** (weak) - HIGH CALLER COUNT

**Evidence:**
- High caller target with 15 cross-references
- Data processing pattern in E500 region
- RTS at E54B confirms function boundary
- Located in NMI/IRQ handler region (E000-F000)

**Confidence:** High

**Function Type:** Data Processing Helper

**Notes:**
This function is part of the E500 region handler block. With 15 callers, it's a frequently-used utility function likely involved in data manipulation or state management during interrupt processing.

**Callers include:**
- C0:CC6F, C0:CF8F, C0:D2FB, C0:D367, C0:D5B7, C0:D5F6, C0:D679, C0:D6E7, C0:D726, C0:D794, C0:D7D3, C0:D83F, C0:DAC3, C0:DAFE, C0:E18D
