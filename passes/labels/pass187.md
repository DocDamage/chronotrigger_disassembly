# Pass 187 — New Labels

- `ct_c3_inline_mixed_pointer_table_and_false_interior_target_cluster_with_unsupported_2461_helper_pocket_before_2500_candidate`
  - Range: `C3:2400..C3:24FF`
  - Kind: `data`
  - Confidence: `medium-high`
  - Notes: conservative upgraded-flow freeze; the page opens in obvious pointer/table-like material, early targets such as `2404` and `2406` land directly inside that lead-in, later targets such as `248D`, `24A4`, `24AE`, and `24F8` are unstable interior landings, and the cleanest local helper-looking pocket at `2461..2483` still lacks a caller-backed true start despite ending at a clean `RTS`
