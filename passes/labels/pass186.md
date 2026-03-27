# Pass 186 — New Labels

- `ct_c3_inline_mixed_brk_heavy_arithmetic_like_cluster_and_false_table_entry_targets_before_2400_candidate`
  - Range: `C3:2300..C3:23FF`
  - Kind: `data`
  - Confidence: `medium-high`
  - Notes: conservative upgraded-flow freeze; the visible late targets (`2380`, `2386`, `238E`, `23A3`) land inside an obvious table-like repeated-value cluster, the `C3:0B27 -> C3:2380` hit is an interior-byte false positive rather than a defendable caller, the tempting `2322` RTS does not keep a trustworthy caller after review, and the more coherent middle pocket at `2323..2376` still degrades into BRK-heavy mixed content without a caller-backed true start
