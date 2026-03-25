# Chrono Trigger Labels — Pass 96

## Purpose
Pass 95 left one clean seam on the table instead of ten fuzzy ones:

- the tail of the negative-`1E05` C7 special path after the staged command-`0x02` emits
- the exact helper cluster that path calls (`0655`, `0734`, `0A39`)
- the immediate `0x18..0x3F` packet-family bridge sitting right beside it (`061C`, `071D`)

Pass 96 closes that seam enough to stop treating the rest of this C7 low-bank pocket as “helper fog.”

The strongest keepable result is:

- `C7:04B1..061B` is now an exact **post-emit special-path tail** that updates current-slot state and sends two exact command-`0x03` APU burst phases
- `C7:0655..071C` is now an exact **per-slot command-`0x03` table-stream emitter** that refreshes the live `1E40..1E63` strip family
- `C7:0734` is now tightened enough to keep an explicit correction: the selector-scan stub currently collapses to exact `1E00 |= 0x04`
- `C7:0A39` is now an exact **selector-table-backed APU handshake gate** with a fatal negative-status unwind path

That is a real closure, not label churn.

---

## Strong labels

### C7:04B1..C7:061B  ct_c7_finish_negative_1e05_special_path_by_updating_current_live_slot_then_sending_two_exact_command_03_burst_phases   [strong structural]
- Runs immediately after the staged command-`0x02` emit phase at `037B..04B0`.
- Uses the first candidate value already loaded from `1F00` and scans backward through live strip `1E20..1E3E`.
- Stores exact local slot selector/index state into `FC`.
- Updates exact latch bytes `1E10 / 1E11` through the carry/result logic at `04C2..04D2`.
- If exact local byte `F3` is nonzero, calls shared helper `0922` before continuing.
- Sends an exact command-`0x03` header through APU ports:
  - `$2143 = 0x20`
  - `$2142 = 0x00`
  - `$2141 = 0x03`
- Then selects a table-backed burst source from exact long table `C7:0D18` using selector `1E05` and streams that variable-length triplet body through `$2141/$2142/$2143`.
- Resets exact local byte `84` to `0xE0`.
- Then computes an exact `36 * selector` block offset and streams a second exact 12-triplet command-`0x03` body from table block `C7:1871 + 36*selector`.
- Finishes by writing exact terminator/reset byte `0xE0`, storing `1E05 = 0xE0`, calling exact cleanup helper `0A12`, and exiting through common dispatcher exit `0192`.
- Strongest safe reading: post-emit tail of the negative-`1E05` special sound-command path, updating current live-slot/latch state and sending two exact command-`0x03` burst phases before final cleanup.

### C7:0655..C7:071C  ct_c7_emit_current_slot_triplet_stream_from_0aea_table_and_refresh_live_1e40_1e63_bounds   [strong structural]
- Called directly from the live-slot reconcile loop at `034F`.
- Reads exact current live-slot index from `1C` and exact current live selector from `1E20 + X`.
- Converts `(selector - 1)` into an exact `*3` index into the long-pointer table at `C7:0AEA`.
- Seeds exact source pointer `12/13/14` from that table.
- Sends an exact command-`0x03` header using the live base pair already stored in `1E60 + X` / `1E61 + X`:
  - `$2142 = 1E60 + X`
  - `$2143 = 1E61 + X`
  - `$2141 = 0x03`
- Reads the first two bytes of the selected stream and stores them exactly into:
  - `1E40 + X`
  - `1E41 + X`
- Adds those exact bytes to the live base pair and stores the sums exactly into:
  - `1E62 + X`
  - `1E63 + X`
- Treats the first data byte as an exact triplet-count and streams the remaining body through `$2141/$2142/$2143` with wrap-safe split logic.
- Normalizes exact local byte `84` back to `0xE0` before returning.
- Strongest safe reading: exact per-slot command-`0x03` table-stream emitter that refreshes the live `1E40..1E63` bound/extent strips for the current sound slot.

### C7:061C..C7:064F  ct_c7_send_exact_four_byte_apu_packet_from_1e00_1e03_then_apply_fc_threshold_fixup_if_needed   [strong]
- Sends exact bytes `1E03 / 1E02 / 1E01 / 1E00` through `$2143/$2142/$2141/$2140`.
- Retries until `$2140` echoes the just-written opcode byte.
- If exact opcode byte `1E00 == 0xFC`, compares exact selector low nibble `1E01 & 0x0F` against exact local byte `F0` and calls `09FD` when they differ.
- Exits through the common dispatcher epilogue at `0192`.
- Strongest safe reading: exact immediate 4-byte APU packet sender for the low-bank `0x18..0x2F` family, with one exact `0xFC` threshold-fixup case.

### C7:071D..C7:0733  ct_c7_table_drive_opcode_30_3f_family_into_1e00_1e03_then_tail_jump_to_0155   [strong]
- Masks exact opcode byte `1E00` to its low nibble.
- Multiplies by four and indexes the exact table rooted at `C7:0A98`.
- Seeds exact packet bytes `1E02` and `1E00` from that table.
- Tail-jumps to `0155`, reusing the same low-bank packet sender / dispatcher flow.
- Strongest safe reading: exact table-driven bridge from the `0x30..0x3F` family into the shared low-bank packet-send path.

### C7:0734..C7:0754  ct_c7_helper_currently_collapses_to_exact_1e00_or_04_due_to_dead_selector_scan_stub_at_0ad8   [strong correction]
- Reads exact opcode byte `1E00`.
- If `1E00 >= 0x14`, forces exact `1E00 |= 0x04` and returns.
- Otherwise enters a selector-scan loop rooted at exact address `C7:0AD8`.
- In the current ROM image, the very first byte at `C7:0AD8` is exact sentinel `0xFF`, so the scan exits immediately.
- That means the helper currently also forces exact `1E00 |= 0x04` for the `< 0x14` case.
- Strongest safe reading: exact helper that currently collapses to `1E00 |= 0x04`, while retaining a dead/degenerate selector-scan stub rooted at `0AD8`.

### C7:0922..C7:09D9  ct_c7_shared_selector_independent_command_03_burst_sender_from_430b_or_5b0d_selected_by_1e10   [strong]
- Sends an exact command-`0x03`/`0x05` header through APU ports:
  - `$2143 = 0x2F`
  - `$2142 = 0x00`
  - `$2141 = 0x05` when `1E00 == 0x70`, otherwise `$2141 = 0x03`
- Uses exact local byte `84` and helper `09DA` for the handshake/ack step.
- If exact byte `1E10 == 0`, selects exact source/count from the table block rooted at `C7:430B`.
- If exact byte `1E10 != 0`, selects exact source/count from the table block rooted at `C7:5B0D`.
- Streams the chosen triplet body through `$2141/$2142/$2143`.
- Clears exact local byte `F3` and normalizes exact `84 = 0xE0` before returning.
- Strongest safe reading: exact shared selector-independent command-`0x03` burst sender used by the later negative-`1E05` tail when the latch/update side says a resend is needed.

### C7:09DA..C7:09E9  ct_c7_write_2140_then_return_incremented_7bit_ack_token_after_echo   [strong]
- Writes `A` to exact APU port `$2140`.
- Spins until `$2140` echoes the same byte.
- Returns exact `((A + 1) & 0x7F)`.
- Strongest safe reading: exact low-bank APU echo/ack helper that advances the local 7-bit handshake token.

### C7:09EA..C7:09FC  ct_c7_restore_2140_from_84_then_normalize_84_back_to_e0   [strong]
- Writes exact local byte `84` to `$2140` and spins until echoed.
- Forces exact `84 = 0xE0` before returning.
- Strongest safe reading: exact low-bank APU reset/normalization helper paired with the `09DA` ack helper.

### C7:09FD..C7:0A38  ct_c7_trim_live_slot_strips_against_exact_threshold_derived_from_selector_handshake_nibble   [strong structural]
- Stores the incoming exact threshold nibble into local byte `F0`.
- Derives exact comparison byte `F2` from that nibble.
- Scans exact live strip `1E63..` in even steps.
- When it finds an entry meeting the threshold rule, zeroes the trailing live strips from that point onward:
  - `1E20..`
  - `1E40..`
  - `1E62..`
- Strongest safe reading: exact live-slot trim helper used by the selector-table handshake path to clamp the trailing live strips against the selector-derived threshold nibble.

### C7:0A39..C7:0A97  ct_c7_selector_table_backed_apu_handshake_gate_with_negative_status_unwind_to_common_exit   [strong structural]
- Uses exact selector byte `1E01 & 0x7F` as a `*2` index into the table at `C7:241D`.
- Seeds exact local bytes:
  - `02` from `C7:241E + index`
  - `03` from low nibble of `C7:241D + index`
- If exact local nibble `03` differs from exact local byte `F0`, calls exact trim helper `09FD`.
- Sends an exact four-byte APU handshake packet through `$2143/$2142/$2141/$2140` using:
  - `$2143 = 03`
  - `$2142 = 02`
  - `$2141 = 1E01`
  - `$2140 = 1E00`
- Retries until `$2140` echoes the just-written opcode byte.
- Then stores exact `84 = ((1E00 + 1) & 0x7F)`.
- If exact status byte read from `$2141` is negative, writes `84` back through `$2140`, waits for the decremented echo, discards the local return frame, and jumps directly to common exit `0192`.
- Otherwise returns normally.
- Strongest safe reading: exact selector-table-backed APU handshake / gate helper with one fatal negative-status unwind path.

---

## Strengthened RAM / workspace labels

### 00:1E20..00:1E63  ct_c7_live_sound_slot_selector_base_and_end_strip_family   [provisional strengthened]
- Pass 95 already proved this workspace is the live slot family touched by the negative-`1E05` path.
- Pass 96 tightens exact subroles:
  - `1E20..1E3E` = live selector strip scanned and updated by the special path
  - `1E40..1E41` per slot = exact lower/base pair written by helper `0655`
  - `1E60..1E61` per slot = exact base pair consumed as the command-`0x03` destination/header pair
  - `1E62..1E63` per slot = exact base+extent / end pair written by helper `0655`
- Strongest safe reading: live sound-slot selector/base/end strip family consumed and refreshed by the negative-`1E05` special path.

---

## Honest caution kept explicit
Even after this pass:

- I have **not** frozen the final user-facing audio noun behind every `0x18..0x3F` packet family.
- I have **not** frozen the exact semantic meaning of the latch pair `1E10 / 1E11` beyond its now-exact control role in the later tail and `0x70` path.
- I have **not** returned to the first exact clean-code external reader of `CE0F` yet.
- I **have** closed the specific helper fog around the negative-`1E05` path: `04B1..061B`, `0655`, `0734`, and `0A39` are no longer honest unknowns.
