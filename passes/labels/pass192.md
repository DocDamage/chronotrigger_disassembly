# Pass 192 — New Labels (Session 32, C3 Low-Bank Forward Seam)

- `ct_c3_2900_frozen_mixed_data_19_brk_no_xref_targets`
  - Range: `C3:2900..C3:29FF`
  - Kind: `data`
  - Confidence: `high`
  - Notes: 19 BRK opcodes in 256 bytes (7.4% density), no xref targets, no PHP/PHB/PHD prologue patterns, incoherent control flow with branches targeting mid-instruction offsets. Frozen as mixed data/content page.

- `ct_c3_2a00_frozen_mixed_data_17_brk_6_unsupported_rts`
  - Range: `C3:2A00..C3:2AFF`
  - Kind: `data`
  - Confidence: `high`
  - Notes: 17 BRK opcodes, 6 RTS bytes but none has a caller-backed true start. Hardware register access at $4206/$4214 suggests division code is embedded but misaligned. Frozen as mixed data with embedded code fragments.

- `ct_c3_2b00_branch_fed_arithmetic_pocket_hw_div_mul_3_rtl_9_jsr`
  - Range: `C3:2B00..C3:2BFF`
  - Kind: `owner`
  - Confidence: `medium-high`
  - Notes: Branch-fed control pocket with code score 52. Contains hardware division unit access (`STA $4204` at C3:2B7A), possible multiplication setup (`STA $4202` at C3:2BF2), cross-bank JSL to C3:0E29, 9 JSR calls to C3 low-bank utilities ($00E2, $021B, $0C0A, $10C2, $1310, $16B8, $8017, $F4AC), table-driven computation at $00A9+Y/$1446+Y/$0E40+X/$8290+X, long data access from bank $FE:A531+X. DP variable map spans $04-$FE. BMI $2C01 at C3:2BF9 confirms cross-page flow into C3:2C00.
