# Chrono Trigger Disassembly — Pass 166

## Scope
Pass 166 closes the remaining live seam `C3:0A90..C3:0E38` by splitting it into one exact service owner, one exact stream-interpreter wrapper pair, a helper cluster, four exact quad-writer variants, and one short tail helper.

## Closed spans
- **`C3:0A90..C3:0AFE`** — exact NMI-gated input/display blackout check with alternating `7E:377A` service dispatch
- **`C3:0AFF..C3:0B02`** — exact `JSR 0B03 ; RTL` veneer
- **`C3:0B03..C3:0C91`** — exact stream-bytecode interpreter driving queue state, temporary command words, and APU port dispatch
- **`C3:0C92..C3:0CB0`** — exact nibble-slot update helper with pointer-advance path
- **`C3:0CB1..C3:0CB7`** — exact stream word-fetch helper advancing `(20)` and caching the fetched word in `20`
- **`C3:0CB8..C3:0CCC`** — exact first-free-slot clearer for exact table `0920`
- **`C3:0CCD..C3:0CE1`** — exact first-free-slot clearer for exact table `0940`
- **`C3:0CE2..C3:0CF7`** — exact first-free-slot writer for exact table `0920`
- **`C3:0CF8..C3:0D0C`** — exact first-free-slot writer for exact table `0940`
- **`C3:0D0D..C3:0D5B`** — exact WRAM-data quad writer to `0700` with duplicated sample bytes and right-shift decay of source table entries
- **`C3:0D5C..C3:0DBB`** — exact WRAM-data quad writer variant with clamped first coordinate and rotated decay update
- **`C3:0DBC..C3:0DF1`** — exact `7E`-pointer quad writer variant with right-shift update through `[13]`
- **`C3:0DF2..C3:0E27`** — exact `7E`-pointer quad writer variant with rotate/right update through `[13]`
- **`C3:0E2A..C3:0E37`** — exact increment/compare tail helper looping until `14 < 00F4`

## Why these splits are real
- exact `0AFE`, `0B02`, `0CB0`, `0CB7`, `0CCC`, `0CE1`, `0CF7`, `0D0C`, `0D5B`, `0DBB`, `0DF1`, `0E27`, and `0E37` are real terminal boundaries
- exact `0AFF..0B02` is a standalone veneer: `JSR $0B03 ; RTL`
- exact `0B03` is the only true owner entry for the interpreter body; the case labels from the exact jump table are internal only
- exact `0CB1` has an external caller at exact `C3:48FD`, so it must remain its own helper and not be buried inside `0C92..0CB0`

## Findings

### `C3:0A90..C3:0AFE`
This owner waits on exact `4212`, samples exact `4218`, and under the exact low-value / state-gated path can force display blackout by writing exact `80` to exact `2100`, clearing exact `4200/420C`, and jumping out through exact `JML 00:FF00`. Otherwise it checks exact state around `0390/0392/0394/0396`, alternates exact `0392`, and dispatches one of two small request blocks through exact `1E00/1E02` into exact external service `7E:377A`.

### `C3:0AFF..C3:0B02`
A trivial but real veneer: exact `JSR $0B03 ; RTL`.

### `C3:0B03..C3:0C91`
This is the main exact stream interpreter. It consumes words through exact long-indirect source `(20)`, decodes high-nibble command classes through the exact internal jump table rooted at `0B74`, updates exact queue/state tables `0920/0940`, materializes temporary command bytes in exact `1E00..1E03`, and under one path pushes those bytes to exact APU ports `2140..2143` while waiting for the port handshake to clear. The cases loop back through exact `JMP 0B03` until one exact stop/return case exits.

### `C3:0C92..C3:0CB0`
This helper updates one exact nibble-indexed slot table rooted at exact `22`, handling the exact carry / negative flag path and then advancing the source pointer / cached word state when the slot rolls over.

### `C3:0CB1..C3:0CB7`
A shared exact fetch helper: increment `(20)` twice, fetch exact `[20]`, cache it back into exact `20`, return.

### `C3:0CB8..C3:0D0C`
This block is a helper cluster for the interpreter:
- exact `0CB8..0CCC` clears the first matching / free exact word slot in exact table `0920`
- exact `0CCD..0CE1` does the same for exact table `0940`
- exact `0CE2..0CF7` writes a supplied exact word into the first free exact slot in exact table `0920`
- exact `0CF8..0D0C` writes a supplied exact word into the first free exact slot in exact table `0940`

### `C3:0D0D..C3:0E27`
These four owners all write exact 4-byte records into exact `0700,Y` while advancing exact `Y` in steps of four:
- the first two read exact source bytes through exact WRAM port `2180`
- the second two read exact source bytes through exact long pointers into exact bank `7E`
- each variant duplicates or offsets the sampled exact byte values into exact `0700..0703`
- each variant also updates one exact source-side byte / nibble state by shifting or rotating it right after emission

### `C3:0E2A..C3:0E37`
A short exact tail helper: increment exact `X`, copy exact `X -> 06`, compare exact `14` against exact `00F4`, loop while the carry path holds, then return exact `RTL`.

## Strong labels / semantics added
- `C3:0A90..C3:0AFE`  `ct_c3_nmi_gated_input_display_blackout_check_with_alternating_7e377a_service_dispatch`
- `C3:0AFF..C3:0B02`  `ct_c3_stream_interpreter_jsr_rtl_veneer`
- `C3:0B03..C3:0C91`  `ct_c3_stream_bytecode_interpreter_updating_0920_0940_and_dispatching_apu_command_words`
- `C3:0C92..C3:0CB0`  `ct_c3_nibble_slot_update_helper_with_pointer_advance_path`
- `C3:0CB1..C3:0CB7`  `ct_c3_stream_word_fetch_helper_advancing_20_and_caching_fetched_word`
- `C3:0CB8..C3:0CCC`  `ct_c3_first_free_slot_clear_helper_for_table_0920`
- `C3:0CCD..C3:0CE1`  `ct_c3_first_free_slot_clear_helper_for_table_0940`
- `C3:0CE2..C3:0CF7`  `ct_c3_first_free_slot_write_helper_for_table_0920`
- `C3:0CF8..C3:0D0C`  `ct_c3_first_free_slot_write_helper_for_table_0940`
- `C3:0D0D..C3:0D5B`  `ct_c3_wram_data_quad_writer_to_0700_with_duplicated_sample_bytes_and_shift_decay_update`
- `C3:0D5C..C3:0DBB`  `ct_c3_wram_data_quad_writer_variant_with_clamped_first_coordinate_and_rotate_decay_update`
- `C3:0DBC..C3:0DF1`  `ct_c3_7e_pointer_quad_writer_to_0700_with_shift_update_through_13`
- `C3:0DF2..C3:0E27`  `ct_c3_7e_pointer_quad_writer_to_0700_with_rotate_update_through_13`
- `C3:0E2A..C3:0E37`  `ct_c3_increment_compare_tail_helper_looping_until_14_falls_below_00f4`

## Resulting seam update
With `C3:0A90..C3:0E38` honestly closed, the next live unresolved bank-`C3` seam is now:
- **`C3:0EFA..C3:10B6`**

## Completion snapshot after pass 166
- overall completion estimate: **~71.0%**
- exact label rows: **1339**
- exact strong labels: **1021**

## Confidence
Medium-high.
The boundary work is strong because this region exposes many exact natural termini and one exact externally called mid-helper. The gameplay-facing names remain intentionally conservative; the structural behavior is what is locked here.
