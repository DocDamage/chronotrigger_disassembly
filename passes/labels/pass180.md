# Pass 180 — New Labels

- `ct_c3_inline_mixed_opcode_cluster_with_resolved_low_bank_call_targets_before_confirmed_0d0e_wrapper`
  - Range: `C3:1A60..C3:1AD5`
  - Kind: `data`
  - Confidence: `medium`
  - Notes: upgraded-flow conservative freeze; `1A60` and `1A7B` have better low-bank caller evidence than earlier raw targets, but the local bytes still do not stabilize into a trustworthy owner/helper split

- `ct_c3_tiny_long_wrapper_calling_c30d0e_then_returning`
  - Range: `C3:1AD6..C3:1ADA`
  - Kind: `veneer`
  - Confidence: `high`
  - Notes: confirmed `JSL $C30D0E ; RTS`; target lies inside the already closed `C3:0D0D..C3:0D5B` owner

- `ct_c3_inline_table_like_data_block_after_0d0e_wrapper_before_unproven_rtl_stub_candidate`
  - Range: `C3:1ADB..C3:1AEF`
  - Kind: `data`
  - Confidence: `medium-high`
  - Notes: immediate table-like block after the confirmed veneer; next seam reduced to the weak `RTL` candidate at `1AF0`
