# Chrono Trigger Labels — Pass 121

## Purpose

Pass 121 closes the exact driver/table/worker seams that were still open after pass 120:

- the higher `A886..AA30` driver above `A970`
- the `B04B` selector-gated block builder
- the `BF2F..BFFF` table-and-worker family behind the `BFD4` dispatch wrapper

## Strong labels

### C2:A886..C2:A969  ct_c2_two_phase_a970_driver_with_seeded_969a_stream_template_and_preseeded_5cc2_5d42_fills   [strong structural]
- Runs exact full-span settlement sweep `A1B2`, then exact service selectors `FBEA`, `821E`, `FC45`, and `FBE3`.
- Clears `5D40` and uses overlapping same-bank `MVN` to propagate that zero seed forward from `5D42`.
- Reruns exact helper `9E76`.
- Seeds `9694 = 969A`, `9696 = 9300`, and `9698 = 0013`.
- Copies exact `0x13` bytes from ROM root `AA06` to WRAM `969A`.
- Seeds `5CC2 = 60FF` and propagates that band fill.
- Derives a tagged `5D42` seed from the masked high-byte path of `0411` and propagates that band fill.
- Zeroes `0DAB` and `0D24`, decrements `0D9A`, and initializes the counted `A970` driver state.
- If `0412 != 0`, computes exact limit `0D25 = 8 * 0412` through hardware multiply and seeds `0DAB = 06` for the first phase.
- Repeatedly runs `821E`, increments `0D9B`, runs selector `FC45`, runs exact updater `A970`, restores `0D13 = E5`, and increments `0D24`.
- First phase continues while `0D24 < 0D25`; then the routine clears `0DAB` and continues until `0D24 == 18`.
- Strongest safe reading: exact two-phase `A970` driver that seeds the `969A` WRAM stream template, preloads the `5CC2/5D42` fill bands, and runs a counted update loop with an initial decrement-step phase followed by a zero-step tail phase up to exactly `0x18` iterations.

### C2:AA06..C2:AA18  ct_c2_nineteen_byte_rom_seed_template_copied_to_7e_969a_before_a970_stream_updates   [strong]
- Exact bytes: `10 FF FF 30 E0 01 30 D0 01 30 D0 01 30 D0 01 10 F0 01 00`
- `A886..A969` copies exactly `0x13` bytes from this ROM root into WRAM `7E:969A` using `MVN $7E,$C2` with `X = AA06`, `Y = 969A`, and `A = 0012`.
- Strongest safe reading: exact 19-byte ROM seed template copied to `7E:969A` before the `A970` / `$2180` stream-update phase begins.

### C2:B04B..C2:B0AA  ct_c2_0d4d_gated_composed_block_builder_with_cc_selector_table_0d4e_mid_copy_and_ffb310_tail_table   [strong structural]
- When `0D4D == 0`, tail-jumps directly into `EF65` with `Y = 9B76` and exact source descriptor `A = 7E18`.
- Otherwise masks `0D4D`, doubles it, and uses it to select a word from exact table root `7D00`.
- Uses that selected word as `Y` and runs `EF65` with exact source descriptor `CC0B`.
- Writes exact tagged word `(7D & 00FF) | 002D` at the current output pointer in `X`.
- Runs `F114` with exact source descriptor `7E11` and `Y = 0D4E`.
- Zeroes the next word and then uses overlapping same-bank `MVN` with `A = 000F` to shift-copy the following `0x10` bytes forward by two bytes in place.
- Reuses `0D4D * 2` to select a second source from long-table root `FF:B310`.
- Restores `X` and runs `EF65` again with exact source descriptor `FF09`.
- Strongest safe reading: exact `0D4D`-gated composed block-builder tail that either emits one fallback `7E:9B76` block or builds a composed output from a selector-chosen `CC` block, the live `0D4E` block, and a selector-chosen `FF:B310` tail block.

### C2:BF2F..C2:BF3C  ct_c2_contiguous_word_table_root_for_bee6_row_loop_ending_immediately_before_code_at_bf3d   [strong]
- Exact contiguous words rooted here are: `E458`, `E478`, `E498`, `BF3D`, `BF45`, `BF6D`, `BF9F`.
- `BEE6..BF2E` indexes this root as `BF2F + 2*71`.
- Executable code begins immediately afterward at `BF3D`.
- Strongest safe reading: exact contiguous word-table root for the `BEE6` row-loop family, ending immediately before live code at `BF3D`.

### C2:BFFF..C2:C016  ct_c2_exact_twelve_entry_jump_table_for_bfd4_selector_indexed_dispatch_wrapper   [strong]
- Exact 16-bit entries are:
  - `C017`
  - `C06E`
  - `C038`
  - `C04A`
  - `C05C`
  - `C0A7`
  - `C12C`
  - `C080`
  - `C0E9`
  - `C095`
  - `C0B9`
  - `C0D1`
- `BFD4` doubles selector `54` and performs `JSR ($BFFF,X)`.
- Strongest safe reading: exact 12-entry jump table consumed by the already-frozen `BFD4` selector-indexed indirect dispatch wrapper.

### C2:C017..C2:C0E8  ct_c2_negative_gated_bfd4_dispatch_worker_family_mutating_0d86_0d90_and_mirroring_into_0f09_0f12   [strong structural]
- `C017..C037`: negative-gated worker that toggles `0D86 & 1`, mirrors it into `0F09`, and emits exact packet `1E00 = F3`, `1E01 = 0D86` through `C7:0004`.
- `C038..C049`: negative-gated toggle/mirror worker for `0D88 -> 0F0B`.
- `C04A..C05B`: negative-gated toggle/mirror worker for `0D8D -> 0F10`.
- `C05C..C06D`: negative-gated toggle/mirror worker for `0D8E -> 0F11`.
- `C06E..C07F`: negative-gated toggle/mirror worker for `0D89 -> 0F0C`.
- `C080..C094`: negative-gated selector-advance worker that loads `0D8A`, adds exact step `0C`, stores the result into selector `54`, increments `0F0D`, and sets `68 = 03`.
- `C095..C0A6`: negative-gated toggle/mirror worker for `0D8F -> 0F12`.
- `C0A7..C0B8`: negative-gated selector-forcing worker that writes `54 = 0A`, `0417 = 0A`, and `0F0E = 01`.
- `C0B9..C0D0`: calls shared helper `C164` with `X = 0D8B`; when `0D1D & C0 != 0`, forces `54 = 05`, forces `0417 = 05`, and clears `0F0E`.
- `C0D1..C0E8`: calls shared helper `C164` with `X = 0D90`; when `0D1D & C0 != 0`, forces `54 = 05`, forces `0417 = 05`, and clears `0F0E`.
- Strongest safe reading: exact negative-gated worker family behind the `BFD4` jump table, owning the resolved `0D86/88/89/8A/8B/8D/8E/8F/90` toggle-or-selector updates and their mirrors into `0F09/0B/0C/0D/0E/10/11/12`.

### C2:C0E9..C2:C12B  ct_c2_selector_08_and_0d87_dispatch_worker_with_optional_0408_to_0f00_copy_and_fixed_c54f_tail   [strong structural]
- Always ends through exact helper `C54F`.
- If `0D1D` is negative:
  - toggles `0D87 & 1`
  - mirrors that result into `0F0A`
  - if the new value is nonzero, forces `54 = 0F`, increments `68`, and copies exact `0x09` bytes from `0408` to `0F00` via same-bank `MVN`
- If `0D1D` is not negative:
  - requires exact selector `7F == 08`
  - requires `5A & 01 != 0`
  - if `0D87 == 0`, forces `54 = 03` and `0417 = 03`
  - otherwise increments/toggles `0D87 & 1`, mirrors to `0F0A`, and on the nonzero result takes the same `54 = 0F` / `68++` / `0408 -> 0F00` copy path
- Strongest safe reading: exact selector-08 dispatch worker around `0D87/0F0A`, with an optional `0408 -> 0F00` same-bank copy, selector forcing through `54`, and a fixed `C54F` tail.

## Alias / wrapper / caution labels

### 7E:0DAB  ct_c2_staged_decrement_step_word_for_9daf_ramp_and_a886_a970_update_driver   [caution strengthened]
- `9DAF..9E75` clears `0DAB` and repeatedly accumulates it by exact step word `0D22` during the 12-step ramp.
- `A970..AA05` subtracts exact word `0DAB` from `5D42` before retagging and propagating that fill.
- `A886..A969` seeds `0DAB = 06` only for the first counted `A970` phase when `0412 != 0`, then explicitly clears it for the second phase.
- Strongest safe reading: exact staged decrement/step word shared by the `9DAF` ramp and the `A886/A970` update-driver family.

### 7E:0D24  ct_c2_loop_progress_word_shared_by_9daf_ramp_and_a886_a970_counted_update_driver   [caution strengthened]
- `9DAF..9E75` seeds `0D24 = 000C`, decrements it once per ramp iteration, and exits when it reaches zero.
- `A886..A969` starts `0D24` at zero, increments it once per `A970` pass, compares it first against `0D25`, then against exact limit `18`.
- Strongest safe reading: exact loop-progress word shared by the `9DAF` ramp and the `A886/A970` counted update driver.

## Honest remaining gap

This pass turned the open seam into real table and worker structure, but a few honest holes remain:

- `C2:C12C..` is still the first unresolved jump-table worker behind `BFD4`
- `C2:B0AB..` is still the next continuation lane after the newly frozen `B04B` builder
- broader gameplay-facing nouns are still open for:
  - `0D86..0D90`
  - `0F09..0F12`
  - `0D4E`
  - the overall `A886..AA30` stream/template/update family
