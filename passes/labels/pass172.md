# Pass 172 — New Labels

- `ct_c3_inline_mixed_control_dispatch_and_dma_setup_blob_preceding_tiny_eb7b_wrapper`
  - Range: `C3:1318..C3:13F7`
  - Kind: `data`
  - Confidence: `medium`
  - Notes: intentionally conservative mixed-content closure; structure is stronger than semantics

- `ct_c3_tiny_local_wrapper_calling_eb7b_then_returning`
  - Range: `C3:13F8..C3:13FB`
  - Kind: `veneer`
  - Confidence: `high`
  - Notes: resolves cleanly as `JSR $EB7B ; RTS`
