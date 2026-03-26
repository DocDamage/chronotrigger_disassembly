# Chrono Trigger Labels — Pass 163

## Strong labels

### C3:01E4..C3:02DC  ct_c3_selected_7e7f_224_byte_band_initializer_and_32_step_saturating_add_or_subtract_wram_stream_worker   [strong structural]
- Saves exact `B/D/P/A/X/Y` and installs exact direct page `0300`.
- Exact mode byte `50 == 0` clears exact `50/51` and exits through exact shared epilogue `01BD..01C5`.
- Exact phase byte `51 == 0` triggers one exact first-activation seed stage.
- On that first activation:
  - exact mode `01` seeds exact byte `F0 = 00`
  - other surviving nonzero modes seed exact byte `F0 = FF`
  - exact `X = 52 + 01C0`
  - exact low bit of exact byte `54` selects exact bank `7E` vs exact bank `7F`
  - exact overlapping same-bank `MVN` with exact `A = 00DE` propagates the seed across one exact selected-bank band of exact length `00E0` bytes.
- Exact phase byte `51` is incremented once per call and compared against exact `20`; when the exact phase reaches `20`, the owner clears exact `51` and exact `50` and exits.
- For each active step:
  - exact long pointer bytes `56/57` are seeded to exact `FE/C0`
  - exact helper `C3:02DD` returns one exact mixed byte which is stored into exact `55`
  - exact source span is rebuilt as exact `X = 52 + 01C0` through exact end word `F4 = 52 + 02A0`
  - exact WRAM destination address is loaded through exact `$2181/$2183` from exact `52` plus one exact parity-dependent `+00E0` adjustment and exact bank byte `54`
  - exact bank byte `54` is also loaded into exact data bank via `PHA ; PLB`
- Exact inner byte-walk uses exact long indirect `[55]`, so with exact `56/57 = FE/C0` it walks one exact chained ROM-byte source in exact bank `C0:FE??`.
- Exact bias derivation uses two successive exact chained bytes:
  - one exact `AND #1F ; ADC #03` lane feeding exact countdown `Y`
  - one exact `AND #03 ; ADC #08` lane feeding exact bias byte `F2`
- Exact arithmetic split:
  - exact mode `50 == 02` enters one exact subtract-and-clamp-to-zero loop
  - all other surviving nonzero modes enter one exact add-and-clamp-to-FF loop
- Exact clamped result is written both to exact WRAM port `$2180` and back to exact selected-bank source `0000,X`.
- Strongest safe reading: exact selected-`7E/7F` `0xE0`-byte band initializer and one exact 32-step saturating add/subtract WRAM stream worker, likely one exact brighten/darken ramp family or equivalent paired rendering effect.

### C3:02DD..C3:0306  ct_c3_external_byte_mix_helper_updating_0386_and_returning_start_byte_for_c0_fe_chained_table_walk   [strong structural]
- Exact standalone callable helper reached by exact `JSL C3:02DD` and exiting exact `RTL`.
- Exact body updates exact state rooted at exact `0386`.
- Exact mix inputs include exact `X`, exact `0008`, exact `F0`, exact `F2`, exact `F4`, and exact reads from exact PPU registers `2137 / 213C / 213D`.
- Returns the final exact mixed byte in exact accumulator and stores it back into exact `0386`.
- Exact caller `C3:01E4` stores the returned exact byte into exact `55` while exact `56/57 = FE/C0`, proving the helper feeds the exact low byte of one exact long indirect pointer into exact chained ROM table space `C0:FE??`.
- Exact second direct caller at exact `C3:15E4` proves this helper is externally callable and not merely one exact private tail.
- Strongest safe reading: exact externally callable byte-mix helper updating exact `0386` and returning one exact start byte for the exact `C0:FE??` chained-table walk used by the selected-band stream worker.

## Provisional labels
- none

## Alias / wrapper / caution labels
- none
