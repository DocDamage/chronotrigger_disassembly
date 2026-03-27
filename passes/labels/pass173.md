# Pass 173 — New Labels

- `ct_c3_inline_mixed_control_table_and_helper_blob_before_c302dd_wrapper`
  - Range: `C3:13FC..C3:15E3`
  - Kind: `data`
  - Confidence: `medium`
  - Notes: intentionally conservative mixed-content closure; structure is stronger than semantics

- `ct_c3_tiny_long_wrapper_calling_c302dd_then_returning`
  - Range: `C3:15E4..C3:15E8`
  - Kind: `veneer`
  - Confidence: `high`
  - Notes: resolves cleanly as `JSL $C302DD ; RTS`
