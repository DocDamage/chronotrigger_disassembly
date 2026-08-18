# Pass 182 — New Labels

- `ct_c3_inline_mixed_control_table_false_entry_and_false_wrapper_cluster_before_2000_candidate`
  - Range: `C3:1C00..C3:1FFF`
  - Kind: `data`
  - Confidence: `medium-high`
  - Notes: conservative upgraded-flow freeze; `1C00` looks cleaner than the previous lead-in but still does not earn an owner claim, the `1DDF..1DE2` wrapper shape is false because it targets frozen post-marker data at `C3:1150`, the `1DFD..1E01` long-wrapper shape is also rejected, and the apparent `1E29` low-bank caller story collapses under byte-level inspection, leaving `2000` as the next cleaner seam
