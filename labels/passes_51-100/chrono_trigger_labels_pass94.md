# Chrono Trigger Labels — Pass 94

## Purpose
Pass 93 turned `C2:0003`, `C2:0009`, and `C7:0004` into exact veneers / dispatch stages.

Pass 94 stays on the very next seams instead of going broad:

- the first real downstream C2 family (`58B2`)
- the first real downstream C7 packet-family bodies (`0755` and `08E3`)

The strongest keepable result is:

- `C7:0140..019D` is now best read as a **sound/APU command opcode-family dispatcher**
- `C7:0755..08E2` and `C7:08E3..09D8` are exact downstream APU-port handlers
- `C2:58B2..5902` is the exact primary stream-token consumer / dispatcher

That is a real noun upgrade, not wording polish.

---

## Strong labels

### C2:584A..C2:58B1  ct_c2_dispatch_0215_substate_through_micro_jump_gate_before_main_token_family_split   [strong structural]
- Exact opening body:
  - loads `0215`
  - doubles it
  - uses exact indexed indirect jump `JMP ($5851,X)`
- Therefore this range is a **pure substate jump gate**, not generic arithmetic.
- The table collapses to a small exact set of entry bodies:
  - `5893` = `SEC ; RTS`
  - `5895` = immediate clear-carry continue path via `BRA` into `CLC ; RTS`
  - `5897` / `589B` = two entry points into the same seed/update body that:
    - seed `0234` with `08` or `14`
    - clear `0217`
    - subtract `08` from `0234` when `(0214 & 0x0F) == 0x02`
    - return with clear carry
- Strongest safe reading: exact `0215`-driven pre-dispatch micro-gate that either forces early exit by carry or prepares local state and returns “continue”.

### C2:58B2..C2:5902  ct_c2_consume_next_stream_token_and_dispatch_primary_token_families   [strong structural]
- Exact opening behavior:
  - reads the next byte through direct-indirect pointer `[0231]`
  - increments the live stream pointer at `0231`
  - then splits on the token value
- Exact family split now frozen:
  - `token >= 0xA0`
    - stores token into `0235`
    - calls exact local helper `JSR $5DC4`
    - decrements `0213`
    - loops this path while `0213` remains nonzero
    - then sets `0215 = 0x10` and returns
  - `0x21 <= token < 0xA0`
    - stores raw token into `023B`
    - indexes the exact long table rooted at `DE:FA00`
    - seeds `0237/0239/023A`
    - sets `0230 = 0x01`
    - jumps directly into `5BF5`
  - `token < 0x21`
    - dispatches through the exact local jump table rooted at `5903`
- Strongest safe reading: exact primary stream-token consumer / dispatcher behind the `57DF -> 5823` chain.

### C7:0192..C7:01A0  ct_c7_common_dispatch_exit_and_register_restore_epilogue   [strong]
- Exact body:
  - `SEP #$20`
  - `STZ $00`
  - `REP #$20`
  - `REP #$10`
  - restores `Y`, `X`, `A`, flags, direct page, and bank
  - returns with `RTL`
- Strongest safe reading: exact common dispatcher exit / cleanup epilogue used by the low-bank C7 sound-command side.

### C7:0AD9..C7:0AE8  ct_c7_packet_opcode_10_17_gate_table_to_active_handler_or_common_exit   [strong]
- Exact eight-entry 16-bit table for packet opcodes `0x10..0x17`:
  - `0x10 -> 01A1`
  - `0x11 -> 01A1`
  - `0x12 -> 0192`
  - `0x13 -> 0192`
  - `0x14 -> 01A1`
  - `0x15 -> 01A1`
  - `0x16 -> 0192`
  - `0x17 -> 0192`
- Strongest safe reading: exact two-target early gate for the `0x10..0x17` family, splitting to either the active handler (`01A1`) or the immediate common exit (`0192`).

### C7:0755..C7:08E2  ct_c7_handle_opcode_71_as_table_driven_apu_triplet_burst_sender   [strong structural]
- Exact opening behavior:
  - checks exact per-slot/state byte `1E20`
  - if that state is active and `1E01 == 0`, exits through `0192`
- Exact setup behavior:
  - computes `(1E01 - 1) * 3`
  - indexes the exact table rooted at `C7:0AEA`
- Exact hardware-facing behavior:
  - performs repeated three-byte burst writes through `2141 / 2142 / 2143`
  - issues exact fixed follow-up command writes including `2141 = 0x05`
  - later issues exact `2141 = 0x02` with paired `2142/2143` values
- Exact tail behavior:
  - caches the current `1E01` value into the per-slot strip at `1E20 + X`
  - exits through the common cleanup path at `0192`
- Strongest safe reading: exact opcode-`0x71` table-driven APU burst sender / uploader over the `1E00..` sound-command workspace.

### C7:08E3..C7:09D8  ct_c7_handle_opcode_70_as_apu_handshake_and_triplet_packet_sender   [strong structural]
- Exact opening behavior:
  - reads `1E01`
  - compares against the latched pair at `1E10 / 1E11`
- Exact hardware-facing behavior:
  - performs handshake traffic through `2140` using `0xFE`
  - later uses exact `2140` handshake/reset traffic with `0xE0`
  - performs repeated command/data triplets through `2141 / 2142 / 2143`
  - selects exact command byte `0x05` when `1E00 == 0x70`
  - otherwise uses exact command byte `0x03` on the shared internal path
- Exact table-backed send behavior:
  - sources repeated triplet payloads from exact tables rooted at `C7:430B` and `C7:5B0D`
  - clears exact local latch byte `F3` before returning in the table-send paths
- Strongest safe reading: exact opcode-`0x70` APU handshake / packet-send handler behind the `1E00` sound-command dispatcher.

### C7:0140..C7:019D  ct_c7_dispatch_1e00_sound_command_opcode_families_into_apu_port_handlers   [strong structural]
- Pass 93 already froze this range as the exact `1E00` opcode-family dispatcher.
- Pass 94 upgrades the subsystem noun with downstream proof:
  - opcode `0x70` lands at `08E3`, which performs exact traffic through `2140..2143`
  - opcode `0x71` lands at `0755`, which also performs exact repeated writes through `2141..2143`
  - the `0x10..0x17` gate table at `0AD9` is now exact
- Strongest safe reading: exact low-bank **sound/APU command** opcode-family dispatcher over the `1E00..` workspace.

---

## Strengthened RAM / workspace labels

### 00:1E00..00:1E10  ct_c7_low_bank_sound_apu_command_packet_workspace   [provisional strengthened]
- Pass 93 already proved this workspace is the live header family consumed by `C7:0140`.
- Pass 94 upgrades the noun with hardware-facing proof from `0755` and `08E3`.
- Exact proven fields now include:
  - `1E00` = sound/APU command opcode / opcode-family selector
  - `1E01` = active selector / payload byte consumed by the `0x70` and `0x71` handlers
  - `1E10 / 1E11` = exact latch pair consumed by the `0x70` handshake path
- Strongest safe reading: low-bank sound/APU command packet workspace consumed by the `C7:0140` dispatcher and its exact downstream handlers.

---

## Honest caution kept explicit
Even after this pass:

- I have **not** frozen the final gameplay-facing noun of the broader C2 stream language behind `58B2 / 5BF5 / 5C3E / 5C77`.
- I have **not** frozen the final user-facing meaning of each opcode family in the C7 sound/APU command set.
- I have **not** returned to the first exact clean-code external reader of `CE0F` yet.
- I **have** crossed an important noun threshold: the C7 packet side is no longer honestly describable as “generic low-bank packet machinery”.
