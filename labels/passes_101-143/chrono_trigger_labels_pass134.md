# Chrono Trigger Labels — Pass 134

## Purpose

Pass 134 closes the downstream callable refresh / packet-build seam that pass 133 left open at `C2:D36C..C2:D520`. The main structural correction here is that the seam does **not** stay one blob: it resolves cleanly into one externally-called three-slot refresh/build owner, one local selector packet, one shared row/descriptor writer, one local byte table feeding that writer, two short exact service wrappers, one local four-word dispatch table, one dispatch target wrapper, and one exact `E984`-status dispatcher.

## Strong labels

### C2:D36C..C2:D45E  ct_c2_externally_called_three_slot_refresh_owner_with_7600_seed_optional_0d77_service_refresh_d466_row_writer_and_d45f_packet   [strong structural]
- Has real outside callers at exact `C2:CFE4`, `C2:D09E`, `C2:E7AC`, and `C2:E7E8`.
- Begins `PHP ; SEP #$30`.
- Clears exact byte `0D5D`.
- Uses exact slot byte `79`.
- Immediate early exit when exact slot byte `79 == 03`.
- Immediate early exit when exact byte `0D49[79] == 00`.
- In 16-bit mode derives exact destination `X = 7600 + ((78 & FF00) >> 2)` and copies exact `0040` bytes from exact source `7E:9890` into that exact `7600`-family window.
- When exact word `0D84 == 0000`:
  - emits exact selector `C15E` through exact helper `ED31`
  - runs exact helper `F28D` with exact `X = 3310` and exact `Y = 98C9`
  - loads exact word `98C2`, halves it into the exact `FFD296` lookup index, and conditionally right-shifts the exact fetched word three more times when the original low bit was set
  - masks the exact low nibble and compares it against exact byte `0D77`
  - when that exact nibble changed, stores it into exact bytes `0D77` and `020C`, seeds exact word `0DC5 = 5E00`, seeds exact word `020D = D396`, seeds exact byte `020F = FF`, runs exact helper `F90C`, derives an exact repeat/count byte from exact byte `0234`, runs exact helper `FB97`, then emits exact local selector packet `D45F` through exact helper `8385`
- After the optional exact `0D77` refresh lane, seeds exact row base `61 = 3200`, seeds exact source pointer `02 = 9890`, and clears exact loop bytes `24/25`.
- Across three exact `0x10`-byte source slots:
  - loads exact lead byte `[02]`
  - when that exact byte is non-negative, copies exact `0009` bytes from the current exact slot into exact work window `9A90`, exact `0006` bytes into exact work window `9AE0`, mirrors the exact following word into exact `9AA2`, emits exact selector `C168` through exact helper `ED31`, then runs exact helper `D466`
  - advances exact row base `61` by exact `00C0`
  - advances exact source pointer `02` by exact `0010`
  - increments exact slot counter byte `24`
- After the exact 3-slot loop, increments exact byte `0D15` and exits `PLP ; RTS`.
- Strongest safe reading: exact externally-called three-slot refresh/build owner that validates exact slot state `79 / 0D49[79]`, seeds an exact `7600` mirror window from `9890`, optionally refreshes exact nibble/state `0D77` through the `D396/F90C/FB97/D45F` service lane, then walks three exact `9890`-family slots and uses exact helper `D466` to build/export the live exact row/descriptor outputs.

### C2:D45F..C2:D465  ct_c2_local_selector_descriptor_packet_for_d36c_changed_0d77_service_lane   [strong]
- Exact 7-byte local selector/descriptor packet used only by `D36C`.
- Exact bytes: `08 78 00 5E 7E F0 01`.
- Strongest safe reading: exact local selector descriptor packet for the changed-`0D77` service lane inside exact owner `D36C`.

### C2:D466..C2:D4B3  ct_c2_shared_three_slot_row_descriptor_writer_using_d4b4_and_ffcc84_templates   [strong structural]
- Has real caller at exact `C2:D43D`.
- Begins `PHP ; SEP #$20`.
- Uses exact row base word `61` and exact slot counter byte `24`.
- Derives exact packed lane byte `((24 << 2) | 11)` and writes that exact byte to exact row offsets `[61+005F]`, `[61+0061]`, `[61+009F]`, and `[61+00A1]`.
- Loads exact source selector byte `00` and uses it as the index into exact local byte table `D4B4`.
- Writes the exact selected base byte from `D4B4[x]` to exact row offset `[61+005E]`, then writes the next three exact incremented bytes to exact row offsets `[61+0060]`, `[61+009E]`, and `[61+00A0]`.
- In 16-bit mode derives exact source `X = FF:CC84 + (00 << 5)` and exact destination `Y = 7E:9500 + (24 << 5)`.
- Copies exact `0x20` bytes from exact source bank `FF` into the exact `9500`-family destination slot.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact shared three-slot row/descriptor writer that stamps four exact lane-tag bytes into the current `61`-based row, expands one exact base byte from local table `D4B4` into four exact neighboring row bytes, and imports one exact `0x20`-byte template from exact source family `FF:CC84` into the exact slot-selected `9500` work window.

### C2:D4B4..C2:D4BB  ct_c2_local_base_byte_table_for_d466_row_descriptor_writer   [strong]
- Exact 8-byte local table used only by `D466`.
- Exact bytes: `E0 E4 E8 EC F0 F4 F8 08`.
- Strongest safe reading: exact local base-byte table for the shared exact row/descriptor writer at `D466`.

### C2:D4BC..C2:D4D4  ct_c2_local_fc75_service_wrapper_seeding_54_03_and_0d13_75_then_fbff_emit   [strong structural]
- Begins `PHP ; SEP #$20`.
- Seeds exact byte `54 = 03`.
- Emits exact selector `C16F` through exact helper `ED31`.
- Seeds exact byte `0D13 = 75`.
- Emits exact selector `FBFF` through exact helper `8385`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact local service wrapper that seeds exact selector byte `54 = 03`, emits exact setup selector `C16F`, stamps exact service/state byte `0D13 = 75`, then exits through exact selector `FBFF`.

### C2:D4D5..C2:D4EF  ct_c2_shared_0f00_mirror_service_wrapper_seeding_0d13_59_then_fbff_emit   [strong structural]
- Has real outside callers at exact `C2:CF82` and exact `C2:CF8F`.
- Begins `PHP ; SEP #$20`.
- Emits exact selector `C191` through exact helper `ED31`.
- Seeds exact byte `0D13 = 59`.
- Mirrors exact byte `0F00 -> 54`.
- Emits exact selector `FBFF` through exact helper `8385`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact shared service wrapper that emits exact selector `C191`, mirrors exact byte `0F00` into exact selector/state byte `54`, stamps exact byte `0D13 = 59`, and then exits through exact selector `FBFF`.

### C2:D4F0..C2:D4F7  ct_c2_local_four_word_dispatch_table_for_d4f8_d506_cf61_cf92   [strong]
- Exact local 4-word dispatch table.
- Exact entries: `D4F8`, `D506`, `CF61`, `CF92`.
- Also appears as a bank-local exact word match inside the generic exact dispatcher table at `C2:82A8`.
- Strongest safe reading: exact local four-word dispatch table that groups the two newly-closed exact service targets `D4F8 / D506` with the already-frozen exact siblings `CF61 / CF92`.

### C2:D4F8..C2:D505  ct_c2_dispatch_target_wrapper_running_9aad_d065_d0e5_then_inc68_and_83b2   [strong structural]
- Reached through exact local dispatch table `D4F0`.
- Exact body runs:
  - `JSR 9AAD`
  - `JSR D065`
  - `JSR D0E5`
  - `INC 68`
  - `JMP 83B2`
- Strongest safe reading: exact dispatch-target wrapper that runs the fixed exact `9AAD -> D065 -> D0E5` service chain, increments exact byte `68`, and exits through exact jump `83B2`.

### C2:D506..C2:D519  ct_c2_e984_status_dispatcher_routing_negative_to_cf0a_nonnegative_clear_to_cfa2_and_overflow_to_82b2   [strong structural]
- Reached through exact local dispatch table `D4F0`.
- Begins `JSR E984 ; BIT 0D1D`.
- When the exact negative flag is set, exits immediately through exact jump `CF0A`.
- When the exact negative flag is clear and the exact overflow flag is clear, exits through exact jump `CFA2`.
- When the exact negative flag is clear and the exact overflow flag is set, exits through exact jump `82B2`.
- Strongest safe reading: exact `E984`-status dispatcher that routes the negative path to exact jump `CF0A`, the clean non-negative/non-overflow path to exact jump `CFA2`, and the exact overflow case to exact jump `82B2`.

## Alias / wrapper / caution labels

## Honest remaining gap

- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
- the next real code seam now moves naturally to `C2:D51A..C2:D715`
