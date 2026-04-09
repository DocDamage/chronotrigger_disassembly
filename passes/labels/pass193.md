# Pass 193 — New Labels (Session 32, C3 Low-Bank Forward Seam)

- `ct_c3_2c00_frozen_mixed_data_0_rts_rtl_7_brk_invalid_jml_a6`
  - Range: `C3:2C00..C3:2CFF`
  - Kind: `data`
  - Confidence: `high`
  - Notes: Mixed control/data blob with 0 RTS/RTL subroutine returns, 7 BRK opcodes, 4 COP opcodes, 6 JSR calls to unknown targets ($5100, $5116, $F0AD, $0671, $9A70, $05C0), JML to invalid bank $A6:109F, long addresses to atypical banks ($50, $07, $09, $53, $5D). The BMI $2C01 target from C3:2BF9 resolved to data.

- `ct_c3_2d00_frozen_data_32_brk_inflated_score_byte_coincidences`
  - Range: `C3:2D00..C3:2DFF`
  - Kind: `data`
  - Confidence: `high`
  - Notes: Data page with 32 BRK bytes (12.5% density). Apparent RTL at $2D09 and RTS at $2D3A are byte coincidences — $6B is the high byte of ROL $6B0A operand, $60 is the DP operand of ORA [$60],Y. Score of 54 is entirely inflated by coincidences.

- `ct_c3_2e00_frozen_structured_data_tables_42_brk_14_rti_coincidences`
  - Range: `C3:2E00..C3:2EFF`
  - Kind: `data`
  - Confidence: `high`
  - Notes: Structured data/table region with 42 BRK bytes (16.4%), 14 RTI byte coincidences (impossible in real code), repeating `00 XX 00 XX` patterns at $2E88-$2EBF indicating 16-bit lookup table or coordinate pair array. 9 PHD ($0B) byte coincidences.

- `ct_c3_2f00_frozen_structured_data_continuation_40_brk_tabular_patterns`
  - Range: `C3:2F00..C3:2FFF`
  - Kind: `data`
  - Confidence: `high`
  - Notes: Continuation of structured data from C3:2E00. 40 BRK bytes (15.6%), `30 XX 30 YY` and `3A XX 3A YY` patterns indicating tilemap/frame data continuation. 1 isolated RTS at $2FC3 but without defendable entry. 18 JSR byte coincidences from frequent $20 values in data.
