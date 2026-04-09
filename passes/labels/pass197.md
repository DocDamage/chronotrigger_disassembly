# Pass 197 Labels: C3:3800-3FFF Region

## Tentative Labels (Future Reference)

| Address | Label | Type | Description |
|---------|-------|------|-------------|
| C3:3F20 | ct_c3_3f20_mode7_fragment | code | Mode 7 matrix setup fragment |
| C3:3F24 | ct_c3_3f24_stz_211b | code | Clear Mode 7 matrix register A |
| C3:3F4E | ct_c3_3f4e_rtl_return | code | RTL return point |
| C3:3F99 | ct_c3_3f99_window_mask_call | code | JSR to $36CC, window settings |
| C3:3F9E | ct_c3_3f9e_sta_2123 | code | Store to window mask register |
| C3:3FB0 | ct_c3_3fb0_wram_store | code | STA $7E6A5F long addressing |
| C3:3FB7 | ct_c3_3fb7_wram_store_2 | code | STA $7E2006 long addressing |
| C3:3FC3 | ct_c3_3fc3_sta_038c | code | Store to $038C |

## Cross-References
- C3:3F99 calls C3:36CC (known utility function)
- C3:3F90 called from C3:62A5
- C3:3FB0 called from C3:4205

## Notes
These are fragmented code snippets mixed with data. Not promoted due to insufficient caller chains and fragmented execution flow, but documented for future reference if additional context emerges.
