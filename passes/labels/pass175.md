# Pass 175 — New Labels

- `ct_c3_small_local_looping_helper_returning_after_backward_branch`
  - Range: `C3:16AC..C3:16B9`
  - Kind: `helper`
  - Confidence: `medium`
  - Notes: small self-contained code-looking loop ending in `RTS`; semantics still unclear

- `ct_c3_inline_mixed_control_table_and_code_fragments_before_externally_anchored_17bd_entry`
  - Range: `C3:16BA..C3:17BC`
  - Kind: `data`
  - Confidence: `medium`
  - Notes: intentionally conservative mixed-content closure that preserves the stronger externally anchored executable seam at `17BD`
