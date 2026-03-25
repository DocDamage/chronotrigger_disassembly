# Chrono Trigger Labels — Pass 114

## Purpose

Pass 113 froze the exact VM ownership of the two-byte `0xC0 / 0xC3 / 0xC4` family, but the earlier one-byte sibling family and the first exact downstream consumer edge were still open.

Pass 114 closes those edges.

## Strong labels

### C0:3557..C0:356F  ct_c0_vm_opcode_b8_shared_three_byte_stream_loader_seed_2b_2c_2d_for_bb_c0_family   [strong structural]
- Exact VM table mapping: opcode `0xB8 -> C0:3557`.
- Reads three successive bytes from exact stream `7F:2001+X` after `TYX`.
- Stores them exactly as:
  - first byte -> local `2B`
  - second byte -> local `2C`
  - third byte -> local `2D`
- Returns through `TYX ; SEC ; RTS`.
- Strongest safe reading: exact three-byte stream loader for the local `2B / 2C / 2D` triplet later used by the same `0xBB / 0xC1 / 0xC2 / 0xC0 / 0xC3 / 0xC4` family.

### C0:3570..C0:35B4  ct_c0_vm_opcode_bb_mode0_one_byte_overwrite_or_vacant_slot_initializer_with_2a_seed   [strong structural]
- Exact VM table mapping: opcode `0xBB -> C0:3570`.
- Reads local `2D`; when `2D == 0`, branches to exact fallback target `C0:2E1E`.
- Checks local `29`; returns early when already nonzero.
- Vacant-slot path:
  - writes `01 -> 7F:0A00,X`
  - first stream byte -> local `2A`
  - `2E = 6D`
  - `32 = 0`
  - `29 = 1`
  - `30 = 0`
  - `54 |= 0x20`
  - returns with carry clear
- Occupied-slot path:
  - clears exact long slot byte `7F:0A00,X`
  - returns through `TYX ; INX ; INX ; SEC ; RTS`
- Strongest safe reading: exact one-byte mode-`0` sibling of the later pass-113 two-byte family.

### C0:35B5..C0:35FB  ct_c0_vm_opcode_c1_mode1_one_byte_overwrite_or_vacant_slot_initializer_with_2a_seed   [strong structural]
- Exact VM table mapping: opcode `0xC1 -> C0:35B5`.
- Same exact gate shape as `3570`.
- Vacant-slot path matches the one-byte initializer body, except `30 = 1`.
- Occupied-slot path matches the same clear-and-return tail.
- Strongest safe reading: exact one-byte mode-`1` sibling of `0xBB`.

### C0:35FC..C0:3642  ct_c0_vm_opcode_c2_mode2_one_byte_overwrite_or_vacant_slot_initializer_with_2a_seed   [strong structural]
- Exact VM table mapping: opcode `0xC2 -> C0:35FC`.
- Same exact gate shape as `3570` / `35B5`.
- Vacant-slot path matches the one-byte initializer body, except `30 = 2`.
- Occupied-slot path matches the same clear-and-return tail.
- Strongest safe reading: exact one-byte mode-`2` sibling of `0xBB` and `0xC1`.

### C0:20F0..C0:2126  ct_c0_local_seed_020c_0214_c2_packet_from_2a_2b_2d_with_54_bit5_force_override_then_call_c2_0003   [strong structural]
- Front-calls local helper `JSR $A560`, then builds the exact `020C..0214` packet.
- Always copies:
  - local `2A -> 020C`
  - `0210 = F000`
  - `0212 = 7E`
  - `0214 = 00`
- Tests exact local flag bit `54.bit5`.
- If `54.bit5 == 1`:
  - writes `FF00 -> 020D`
  - writes `DE -> 020F`
- If `54.bit5 == 0`:
  - writes local `2B -> 020D`
  - writes local `2D -> 020F`
- Calls exact external veneer `JSL C2:0003`, then returns.
- Strongest safe reading: exact local packet builder tying the `2A / 2B / 2D` family into the already-frozen `020C..0214 -> C2:0003` stream-init lane.

## WRAM / local byte upgrades

### 7E:012A  ct_c0_local_one_byte_stream_parameter_seeded_by_bb_c1_c2_and_copied_into_020c_by_20f0   [caution strengthened]
- Pass 113 already proved the two-byte family can also seed `2A`.
- Pass 114 proves the exact one-byte family `0xBB / 0xC1 / 0xC2` seeds `2A` from one stream byte.
- Pass 114 also proves `20F0..2126` copies exact local `2A -> 020C`.
- Strongest safe reading: local one-byte parameter/selector for the family's downstream `020C` packet emission.

### 7E:012B  ct_c0_local_first_byte_of_exact_b8_seed_triplet_used_by_20f0_when_54_bit5_clear   [caution strengthened]
- `3557` seeds exact first triplet byte into local `2B`.
- `20F0..2126` copies local `2B -> 020D` when `54.bit5` is clear.
- Strongest safe reading: exact first byte of the `0xB8` seed triplet, consumed by the `020D` packet field on the non-override path.

### 7E:012C  ct_c0_local_middle_byte_of_exact_b8_seed_triplet   [caution]
- `3557` seeds exact second triplet byte into local `2C`.
- No exact downstream consumer edge was frozen in this pass.
- Strongest safe reading: exact middle byte of the `0xB8` seed triplet; final role still open.

### 7E:012D  ct_c0_local_gate_byte_for_local_vs_2e1e_fallback_and_packet_tail_byte_on_nonoverride_path   [caution strengthened]
- `3557` seeds exact third triplet byte into local `2D`.
- All six handlers `0xBB / 0xC1 / 0xC2 / 0xC0 / 0xC3 / 0xC4` gate locally on `2D != 0`, else branch to exact fallback target `C0:2E1E`.
- `20F0..2126` copies local `2D -> 020F` when `54.bit5` is clear.
- Strongest safe reading: exact local/nonlocal gate byte for the family, and exact tail-byte source for the non-override `020F` packet path.

### 7E:0154.bit5  ct_c0_local_override_flag_bit_selecting_forced_ff00_de_packet_fields_in_20f0   [caution strengthened]
- Pass 113 already proved the one-byte and two-byte family bodies set `54 |= 0x20`.
- Pass 114 proves `20F0..2126` tests `54.bit5` and, when set, forces:
  - `020D = FF00`
  - `020F = DE`
  instead of using local `2B / 2D`.
- Strongest safe reading: exact local override bit for the packet-builder split in `20F0..2126`.

## Honest remaining gap

- I am intentionally **not** freezing the first exact consumer of local `30` yet.
- I am intentionally **not** freezing the final noun of `7F:0A00/0A80`.
- I am intentionally keeping `2C` one notch below strong until its first exact consumer edge is frozen.
