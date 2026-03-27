# Pass 190 — New Labels

- `ct_c3_inline_branch_heavy_mixed_control_arithmetic_blob_with_false_data_side_2709_target_and_no_caller_backed_true_start_before_2800_candidate`
  - Range: `C3:2700..C3:27FF`
  - Kind: `data`
  - Confidence: `medium-high`
  - Notes: conservative upgraded-flow freeze; the only visible raw hit is `C3:A1B7 -> C3:2709`, but the caller sits in obvious byte-soup / inline-data material and is not trustworthy, the veneer scan only finds unsupported `BRA` signatures at `2714`, `2771`, `2787`, `27A8`, and `27BF`, there is no clean wrapper or return stub inside the page, and the denser control-looking middle/late bytes still never produce a caller-backed true start
