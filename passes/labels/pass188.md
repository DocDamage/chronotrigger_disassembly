# Pass 188 — New Labels

- `ct_c3_inline_mixed_weak_single_caller_page_with_unsupported_2523_helper_stub_and_late_pointer_table_cluster_before_2600_candidate`
  - Range: `C3:2500..C3:25FF`
  - Kind: `data`
  - Confidence: `medium-high`
  - Notes: conservative upgraded-flow freeze; only three visible raw targets appear in this page, only the `C3:5599 -> C3:2504` same-bank `JSR` looks remotely caller-trustworthy, `2504` still fails local sanity checks, the cleanest local pocket is the unsupported `2523..2529` helper-looking island ending in the page’s lone `RTS`, and the late half of the page shifts into obvious pointer/table-like material from roughly `2590` onward
