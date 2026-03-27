# Pass 177 — New Labels

- `ct_c3_tiny_branch_landing_pad_redirecting_execution_back_to_17ef`
  - Range: `C3:1817..C3:1818`
  - Kind: `veneer`
  - Confidence: `medium`
  - Notes: tiny executable landing pad `BRA $17EF`; observed long-jump pattern exists at `DF:0E55`, but caller context remains less certain than a normal strongly anchored owner

- `ct_c3_inline_mixed_control_and_code_fragments_between_branch_pad_and_rtl_stub`
  - Range: `C3:1819..C3:187F`
  - Kind: `data`
  - Confidence: `medium`
  - Notes: intentionally conservative mixed-content freeze between the branch pad and the isolated `RTL` stub

- `ct_c3_single_byte_rtl_return_stub_reached_via_local_jump`
  - Range: `C3:1880..C3:1880`
  - Kind: `veneer`
  - Confidence: `high`
  - Notes: one-byte `RTL`; directly targeted by same-bank `JMP $1880` at `C3:2936`
