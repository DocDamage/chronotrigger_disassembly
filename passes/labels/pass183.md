# Pass 183 — New Labels

- `ct_c3_inline_mixed_control_table_and_false_low_bank_helper_cluster_before_2100_candidate`
  - Range: `C3:2000..C3:20FF`
  - Kind: `data`
  - Confidence: `medium-high`
  - Notes: conservative upgraded-flow freeze; visible same-bank caller pressure lands on `20AA`, `20B2`, and `20E6`, but each target still fails local byte-level sanity checks, `2083` also stays a false-entry pocket despite multiple callers, and no clean veneer survives before the next in-order boundary at `2100`
