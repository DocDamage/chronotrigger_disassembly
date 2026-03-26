# Chrono Trigger Disassembly — Pass 167

## Scope
Pass 167 closes the direct-entry worker anchored by the exact low-bank veneer `C3:0011 -> JMP $0EFA` and the immediately following helper with the common exact epilogue.

## Closed spans
- `C3:0EFA..C3:1024` — selected-bank four-edge scanline owner that orders four exact `(x,y)` pairs, dispatches the edge helper four times, then materializes row spans through exact `7E/7F` copy/write paths
- `C3:1025..C3:10BF` — selected-bank edge rasterizer helper storing one exact x-intercept byte per scanline and returning through the common exact `PLP/PLB/PLD/RTL` epilogue
- `C3:10C0..C3:10CF` — inline ASCII marker `CODE END C3`

## Why the split is real
- exact `C3:1025` begins with a full prologue (`PHD ; PHB ; PHP ; SEP #$20 ; PEA $0300 ; PLD`) and ends at the shared exact epilogue `C3:10BA..10BF`
- the exact owner at `0EFA` reaches the helper through exact `JSL C3:1025`
- exact `0EFA` is externally anchored by the proven low-bank entry veneer at exact `C3:0011`
- exact `10C0` is plain readable marker text, not executable flow

## Findings

### `C3:0EFA..C3:1024`
This owner installs exact direct page `0300`, clears exact local byte `69`, and compares the four exact y-like inputs at `61/63/65/67` to choose one of four exact setup blocks at `0F35 / 0F48 / 0F5B / 0F6E`.

Each setup block loads one ordered `(x1,y1,x2,y2)` pair into exact locals `53/55/57/59` and calls exact helper `0F83`.
The four exact pair selections are:
- `60,61 -> 62,63`
- `62,63 -> 64,65`
- `64,65 -> 66,67`
- `66,67 -> 60,61`

So the owner is walking the four edges of one closed four-point shape.

The exact helper gate at `0F83` compares `59` vs `55`, conditionally seeds exact `6A`, exact `50`, and exact `F6`, then calls exact edge helper `C3:1025`.

After the edge work, the owner uses exact `52` to choose bank-sensitive exact `7E` vs `7F` paths, updates exact long-pointer state through exact local `50`, writes exact row bytes either directly with exact `STA $7E0000,X` / `STA $7F0000,X` or through exact same-bank `MVN 7E,7E` / `MVN 7F,7F`, and loops through the exact shared materialization path before jumping to the common exact epilogue.

Strongest safe reading: one selected-bank four-edge scanline owner that builds row/edge state for one four-point shape and then materializes the resulting row spans into exact `7E` or exact `7F` WRAM.

### `C3:1025..C3:10BF`
This helper begins with its own full prologue and sets exact DB from exact byte `52`.
It compares `59 - 55` and swaps exact endpoint pairs when needed so the edge is processed in one consistent y-direction.

Then it derives:
- exact row count / delta from `59 - 55`
- exact starting row index from exact `55*2 + 50`
- exact x delta from `57 - 53`

The inner loops repeatedly adjust the exact x accumulator and store one exact x byte per scanline via exact `STA $0000,Y`, advancing exact `Y` by two each row.
That is exact scanline edge-table population behavior, not one generic math helper.

The helper exits through exact shared epilogue:
- `C3:10BA  TDC`
- `C3:10BB  XBA`
- `C3:10BC  PLP`
- `C3:10BD  PLB`
- `C3:10BE  PLD`
- `C3:10BF  RTL`

Strongest safe reading: one selected-bank edge rasterizer that stores one exact x-intercept byte per scanline for one line segment and returns through the shared exact bank-head epilogue.

### `C3:10C0..C3:10CF`
Readable ASCII marker:
- `CODE END C3`

This is data / marker text, not executable logic.

## Strong labels added
- `C3:0EFA..C3:1024` — `ct_c3_selected_bank_four_edge_scanline_owner_ordering_four_xy_pairs_and_materializing_row_spans_to_7e_or_7f`
- `C3:1025..C3:10BF` — `ct_c3_selected_bank_edge_rasterizer_storing_one_x_intercept_byte_per_scanline_with_common_epilogue`
- `C3:10C0..C3:10CF` — `ct_c3_inline_ascii_code_end_c3_marker`

## Resulting state
- low-bank direct-entry worker anchored by exact veneer `C3:0011` is now honestly closed
- the low-bank executable cluster now runs cleanly into the exact `CODE END C3` marker
- next bank-`C3` target should move to the next higher unresolved callable region rather than pretending more low-bank code continues past the marker

## Completion snapshot after pass 167
- overall completion estimate: **~71.3%**
- exact label rows: **1342**
- exact strong labels: **1024**
