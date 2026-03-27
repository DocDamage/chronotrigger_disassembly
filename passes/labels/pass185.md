# Pass 185 — New Labels

- `ct_c3_inline_mixed_false_target_cluster_with_brk_heavy_lead_in_and_unsupported_226f_helper_pocket_before_2300_candidate`
  - Range: `C3:2200..C3:22FF`
  - Kind: `data`
  - Confidence: `medium-high`
  - Notes: conservative upgraded-flow freeze; the page has many raw targets, but several of the visible callers sit in obvious text/table/script-like data neighborhoods, the remaining more code-like callers into `2200` and `2210` still land on BRK/COP-heavy mixed bytes, and the cleanest local pocket at `226F..227B` stays unsupported because the only nearby visible target is the interior `RTS` at `227B`
