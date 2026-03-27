# Pass 189 — New Labels

- `ct_c3_inline_mixed_multi_target_page_with_false_text_table_callers_and_unsupported_late_rts_island_before_2700_candidate`
  - Range: `C3:2600..C3:26FF`
  - Kind: `data`
  - Confidence: `medium-high`
  - Notes: conservative upgraded-flow freeze; the page has several visible raw targets, but `C3:0EBA -> C3:2620` is clearly a text-region false hit, multiple higher-bank-looking callers into `2625`, `263F`, `265D`, and `26A5` read like table/script-style inline data, the more trustworthy low-bank callers into `2600`, `2629`, and `26D0` still land on structurally bad targets, and the strongest late local island at `2678..268F` ends in the page's lone `RTS` without a caller-backed true start
