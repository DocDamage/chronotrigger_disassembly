# Pass 174 — New Labels

- `ct_c3_inline_code_looking_mixed_helper_and_control_blob_before_local_2629_wrapper`
  - Range: `C3:15E9..C3:16A7`
  - Kind: `data`
  - Confidence: `medium`
  - Notes: intentionally conservative mixed-content closure; opening looks code-like but does not stabilize cleanly enough to claim as one owner/helper body

- `ct_c3_tiny_local_wrapper_calling_2629_then_returning`
  - Range: `C3:16A8..C3:16AB`
  - Kind: `veneer`
  - Confidence: `high`
  - Notes: resolves cleanly as `JSR $2629 ; RTS`
