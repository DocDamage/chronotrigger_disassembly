# Chrono Trigger Labels — Pass 113

## Purpose
Pass 112 froze the local selector writer mechanics, but not the exact VM caller chain that seeds `64/65`, and not the first exact downstream consumer of `66`.

Pass 113 closes those two edges.

## Strong labels

### C0:3643..C0:3670  ct_c0_vm_opcode_c0_mode0_overwrite_or_vacant_slot_two_byte_initializer_with_66_persist_tail   [strong structural]
- Exact VM table mapping: opcode `0xC0 -> C0:3643`.
- Local path only runs when `2D != 0`; otherwise diverts to an earlier external helper via `LDX #$7FE0 ; BRL ...`.
- If `29 != 0`, returns early.
- Otherwise loads slot index from `6D` and inspects exact long byte `7F:0A00,X`.
- If that slot byte is zero:
  - `30 = 0`
  - branches to shared helper `C0:3674`
- If that slot byte is nonzero:
  - clears `7F:0A00,X`
  - writes `66 -> 7F:0A80,X`
  - clears `62`
  - returns through `TYX ; INX ; INX ; INX ; SEC ; RTS`
- Strongest safe reading: exact opcode-`0xC0` overwrite/retire-or-init handler for mode `0`, sharing the same occupied-slot retire tail as the later `0xC3/0xC4` siblings.

### C0:3674..C0:36A8  ct_c0_shared_two_byte_vm_stream_initializer_mark_slot_0a00_active_seed_2a_64_65_set_62_1_and_arm_29   [strong structural]
- Entered by exact branches from the vacant-slot paths of `3643`, `36AA`, and `36DD`.
- Writes `01` to exact long slot byte `7F:0A00,X`.
- Treats `Y` as the script-stream cursor and consumes two successive bytes from `7F:2001+X`.
- First stream byte -> local `2A`.
- Second stream byte is split exactly as:
  - `65 = byte & 0x03`
  - `64 = (byte >> 2) & 0x03`
- Then forces:
  - `62 = 1`
  - `2E = 6D`
  - `32 = 0`
  - `29 = 1`
  - `54 |= 0x20`
- Returns through `TYX ; CLC ; RTS`.
- Strongest safe reading: exact shared two-byte VM stream initializer for the `0xC0 / 0xC3 / 0xC4` family.

### C0:36AA..C0:36DC  ct_c0_vm_opcode_c3_mode1_overwrite_or_vacant_slot_two_byte_initializer_with_66_persist_tail   [strong structural]
- Exact VM table mapping: opcode `0xC3 -> C0:36AA`.
- Same exact front-gate shape as `3643`.
- Vacant-slot path sets `30 = 1`, then branches to shared initializer `3674`.
- Occupied-slot path matches the exact retire/persist tail:
  - clear `7F:0A00,X`
  - write `66 -> 7F:0A80,X`
  - clear `62`
  - return with `SEC`
- Strongest safe reading: exact opcode-`0xC3` sibling of `0xC0`, using mode `1` before the shared two-byte initializer.

### C0:36DD..C0:370D  ct_c0_vm_opcode_c4_mode2_overwrite_or_vacant_slot_two_byte_initializer_with_66_persist_tail   [strong structural]
- Exact VM table mapping: opcode `0xC4 -> C0:36DD`.
- Same exact front-gate shape as `3643` / `36AA`.
- Vacant-slot path sets `30 = 2`, then branches to shared initializer `3674`.
- Occupied-slot path matches the exact retire/persist tail:
  - clear `7F:0A00,X`
  - write `66 -> 7F:0A80,X`
  - clear `62`
  - return with `SEC`
- Strongest safe reading: exact opcode-`0xC4` sibling of `0xC0` and `0xC3`, using mode `2` before the shared two-byte initializer.

## WRAM / local byte upgrades

### 7E:0162  ct_c0_local_multistate_control_byte_for_the_62_63_64_65_66_family   [caution strengthened]
- New exact transitions from this pass:
  - `3674` forces `62 = 1`
  - the occupied-slot overwrite tails in `3643 / 36AA / 36DD` force `62 = 0`
- Carry-forward exact transition from pass 112 context:
  - `1AF8` forces `62 = 3`
- Strongest safe reading: local multi-state control byte inside the same selector/range family as `63/64/65/66`, with exact states `0`, `1`, and `3` now proven.

### 7E:0164  ct_c0_local_inclusive_lower_wrap_bound_for_63_selector_seeded_from_bits_2_3_of_shared_packed_stream_byte   [caution strengthened]
- Pass 112 already froze the wrap-bound behavior.
- Pass 113 now freezes the exact stream-seed source:
  - in shared helper `3674`, `64 = ((packed_byte >> 2) & 0x03)`
- Strongest safe reading: exact inclusive lower wrap bound for `63`, seeded from bits `2..3` of the family's packed stream byte.

### 7E:0165  ct_c0_local_inclusive_upper_wrap_bound_for_63_selector_seeded_from_bits_0_1_of_shared_packed_stream_byte   [caution strengthened]
- Pass 112 already froze the wrap-bound behavior.
- Pass 113 now freezes the exact stream-seed source:
  - in shared helper `3674`, `65 = (packed_byte & 0x03)`
- Strongest safe reading: exact inclusive upper wrap bound for `63`, seeded from bits `0..1` of the family's packed stream byte.

### 7E:0166  ct_c0_local_saved_predefault_63_selector_byte_later_persisted_into_exact_slot_byte_7f0a80_on_overwrite_path   [caution strengthened]
- Pass 112 froze the save side: prior live `63 -> 66` before forcing `63 = 4`.
- Pass 113 closes the first exact consumer edge:
  - occupied-slot overwrite tails in `3643 / 36AA / 36DD` write `66 -> 7F:0A80,X`
- Strongest safe reading: saved prior selector value that is later persisted outward into exact slot state during the overwrite/retire path.

## Correction note

- Pass 112's broad wording about the packed source byte should now be read more exactly as:
  - low 2 bits -> `65`
  - bits `2..3` -> `64`
- I am intentionally **not** freezing a broader noun for `7F:0A00/0A80` yet, because earlier render-anchor evidence in that neighborhood still deserves one more caution pass.
