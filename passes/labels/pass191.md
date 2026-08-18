# Pass 191 — New Labels

- `ct_c3_inline_branch_heavy_mixed_control_blob_with_double_low_bank_2809_hits_but_no_defendable_true_start_before_2900_candidate`
  - Range: `C3:2800..C3:28FF`
  - Kind: `data`
  - Confidence: `medium-high`
  - Notes: conservative upgraded-flow freeze; the page's strongest visible support is the double low-bank same-bank `JSR` pressure into `2809` from `C3:0CC9` and `C3:0CF4`, but that target still opens into a branch-heavy mixed control blob rather than a defendable true start, while the other visible targets are caller-invalid or structurally weaker and the lone return-looking bytes at `285A`, `286D`, and `287C` remain unsupported interior splinters
