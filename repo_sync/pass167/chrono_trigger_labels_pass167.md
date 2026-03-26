# Chrono Trigger Labels — Pass 167

## Strong labels
- `C3:0EFA..C3:1024` — `ct_c3_selected_bank_four_edge_scanline_owner_ordering_four_xy_pairs_and_materializing_row_spans_to_7e_or_7f`
- `C3:1025..C3:10BF` — `ct_c3_selected_bank_edge_rasterizer_storing_one_x_intercept_byte_per_scanline_with_common_epilogue`
- `C3:10C0..C3:10CF` — `ct_c3_inline_ascii_code_end_c3_marker`

## Notes
- exact `C3:0011` still proves the real external entry into the owner at exact `C3:0EFA`
- exact `C3:1025` is a real helper split because it has its own full prologue and shared epilogue
- bank-`C3` low-bank executable flow now reaches the exact `CODE END C3` marker cleanly
