# Chrono Trigger Labels — Pass 162

## Purpose

Pass 162 freezes the exact first real downstream worker reached by exact low-bank veneer `C3:0008`, plus the exact local repeated-`0001` fill helper immediately after it.

## What this pass closes

### C3:0077..C3:01C5  ct_c3_selected_7e7f_row_pair_midpoint_circle_span_builder_from_center_radius_inputs   [strong structural]
- Saves exact `B/D/P/A/X/Y`, masks the incoming exact accumulator down to one exact low-byte mode/control word, and installs exact direct page `0300`.
- Clears exact local lanes `51 / 53 / 55`.
- Chooses exact data bank `7E` vs exact `7F` from exact low bit of exact byte `58`.
- Treats exact words/bytes rooted at exact `50 / 52 / 54 / 56 / 58` as the exact active input set.
- Exact zero-radius path `54 == 0000` loads exact fill count `01C0`, calls exact helper `01C6`, and returns.
- Nonzero path seeds one exact midpoint-circle-style decision/error word, sets exact `X = radius`, exact `Y = 0`, and derives exact symmetric row slots from exact `52/56`.
- Exact main loop writes clamped exact byte pairs around the exact horizontal center byte `50` into two exact symmetric row slots.
- Exact negative vs nonnegative update split matches one exact midpoint-circle step family:
  - exact negative lane adds exact `4*x + 6`
  - exact nonnegative lane decrements the exact outer extent and adds the exact `4*(x-y) + 10` style update
- After the raster loop, restores the saved exact low-byte mode/control word and branches on exact `A & 007F`.
- Exact low-7-bits `== 0` enters one exact copy/densify lane.
- Exact low-7-bits `== 1` enters one exact earlier copy/densify lane and may also enter the second exact copy lane.
- Exact bit `0x80` suppresses the downstream exact leading/trailing repeated-`0001` fill stage.
- Strongest safe reading: exact selected-`7E/7F` row-pair midpoint-circle/span builder that materializes clamped left/right byte pairs around one exact center/radius input set rooted at exact `50/52/54/56/58`, with exact post-raster mode gates controlling downstream densify/fill behavior.

### C3:01C6..C3:01E3  ct_c3_selected_7e7f_row_pair_fill_helper_seeding_0001_and_propagating_it_forward_from_56   [strong structural]
- Stores the incoming exact 16-bit fill-count into exact word `F0`.
- Loads exact base pointer `56 -> X`.
- Derives exact `Y = X + 2`.
- Writes exact word `0001 -> 0000,X`.
- Chooses exact bank `7E` vs exact `7F` from exact low bit of exact byte `58`.
- Loads exact count from exact `F0` and performs one exact overlapping same-bank `MVN`:
  - exact `MVN 7E,7E`, or
  - exact `MVN 7F,7F`
- Because the move is overlapping and exact destination begins at `X + 2`, the helper propagates the seeded exact word `0001` forward across the downstream selected row-pair band.
- Strongest safe reading: exact selected-`7E/7F` row-pair fill helper that seeds exact word `0001` at the exact `56`-selected base and propagates that exact fill forward with one exact overlapping same-bank move.

## Alias / wrapper / caution labels

### C3:01CA..C3:01E3  ct_c3_overlapping_selected_7e7f_row_pair_fill_late_entry_reusing_preseeded_x_and_f0   [strong structural]
- Exact overlapping callable late entry.
- Begins after exact `X` and exact fill-count `F0` have already been staged by the caller.
- Rejoins the exact shared `TXY / INY / INY / LDA #0001 / STA 0000,X / bank-select / MVN / RTS` tail.
- Strongest safe reading: exact overlapping late entry into the shared exact selected-row-pair fill helper.

## Honest remaining gap

- the exact worker reached by exact veneer `C3:0008` is now closed more honestly as one exact owner plus one exact local helper
- the next exact downstream anchored worker is the one reached by exact veneer `C3:000E`
- exact next manual/raw seam: `C3:01E4..C3:0306`
