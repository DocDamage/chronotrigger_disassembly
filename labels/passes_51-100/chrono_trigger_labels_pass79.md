# Chrono Trigger Labels — Pass 79

## Purpose
This file records the label upgrades justified by pass 79.

Pass 78 proved the late service-04 path was a real packed-row/materialization pipeline, but the transform modes and the optional `CA32..` stage were still too fuzzy.

Pass 79 closes that seam:

- `CD:13E6` is now pinned as a four-mode **tile-orientation** jump table
- `C0:FD00` is now pinned as a **bit-reverse lookup table**
- `1509 / 1445 / 13F6 / 13EE` now read cleanly as **direct / H-flip / V-flip / HV-flip** tile materializers
- `15D5` and `1609` now pin the optional `CA32..` path as a **two-slot auxiliary descriptor stream interpreter**
- `5D9B` and `CCEA` are materially tighter as stage-level gate/progression bytes for that optional auxiliary stage

This still stops short of the final gameplay-facing noun for the downstream `4500.. -> 5D00..` emit family, but the late path is now much more clearly graphics/tile-oriented.

---

## Strengthened helper labels

### CD:13E6..CD:13ED  ct_cd_tile_orientation_mode_ptr_table_direct_hflip_vflip_hvflip   [strong]
- Exact four-entry local jump table used by the shared `1323/1314` row builder.
- Entry order is now pinned as:
  - `1509` = direct
  - `1445` = horizontal flip
  - `13F6` = vertical flip
  - `13EE` = horizontal + vertical flip

### CD:1509..CD:15D4  ct_cd_materialize_one_32byte_4bpp_tile_block_from_d0_source_with_optional_second_block_merge   [strong structural]
- Uses the low 13 bits of the active source word as the `D0` source index, multiplied by 8.
- Always materializes one 32-byte tile-shaped block into the active `2D00..` row section.
- Bit `0x2000` controls whether a second `D0` source block is merged into the upper half.
- Safest reading: direct tile materializer over one or two `D0` source blocks.

### CD:1488..CD:1508  ct_cd_materialize_base_tile_planes_and_masked_upper_half_from_d0_source_block   [strong structural]
- Shared helper used by `1509`.
- Builds the first `0x10` bytes directly from `D0`, then derives the paired `+0x10` upper half under selector mask `$5F`.
- Strongest safe reading: base 32-byte tile-block materializer helper.

### CD:13F6..CD:1444  ct_cd_materialize_tile_then_apply_vertical_flip_to_both_plane_halves   [strong structural]
- Calls the direct tile materializer, then uses the internal `13FE` helper twice.
- The helper swaps word pairs `00<->0E`, `02<->0C`, `04<->0A`, `06<->08` and advances `Y` by `0x10`.
- Therefore reverses row order in both 16-byte plane halves of one 32-byte tile block.
- Strongest safe reading: vertical-flip tile materializer.

### CD:1445..CD:1484  ct_cd_materialize_tile_then_apply_horizontal_flip_via_c0_fd00_bit_reverse   [strong structural]
- Calls the direct tile materializer, then rewrites the resulting bytes through `C0:FD00`.
- `C0:FD00` is a plain bit-reverse map, so this is the tile horizontal-flip path.

### CD:13EE..CD:13F5  ct_cd_materialize_tile_then_apply_hv_flip_composite_path   [strong structural]
- Exact body is `PHY ; JSR 13F6 ; PLY ; JMP 144A`.
- So it composes the vertical-flip path with the bit-reverse horizontal-flip body.
- Strongest safe reading: horizontal + vertical flip tile materializer.

### C0:FD00..C0:FDFF  ct_c0_bit_reverse_lookup_256   [strong]
- Exact 256-byte bit-reversal table.
- Example mappings: `01->80`, `02->40`, `03->C0`.
- Used directly by the `1445` horizontal-flip tile path.

### D1:646C..D1:652B  ct_d1_auxiliary_descriptor_pointer_table   [strong structural]
- `15D5` multiplies the descriptor id by two and reads a pointer from this table.
- The returned pointer seeds one active runtime slot in the optional auxiliary descriptor stage.

### CD:15D5..CD:1608  ct_cd_expand_one_auxiliary_descriptor_id_into_one_active_runtime_slot   [strong structural]
- Looks up a descriptor pointer from `D1:646C`.
- Seeds the active slot's stream pointer and cadence bytes.
- Increments the slot active flag.
- Strongest safe reading: expand one descriptor id into one active runtime stream slot.

### CD:1609..CD:16A5  ct_cd_tick_two_auxiliary_descriptor_runtime_slots_and_interpret_ready_tokens   [strong structural]
- Runs only while the optional auxiliary stage is active.
- Walks the two active `CA32` runtime slots.
- Decrements each slot countdown and calls `1654` whenever the countdown expires.
- `1654` treats `<80` bytes as data tokens, `7F` as a dedicated advance token, `FF` as end-of-slot, and `>=80` as command tokens dispatched through the large local jump table.
- Strongest safe reading: two-slot auxiliary descriptor stream scheduler/interpreter.

### CD:16B5..CD:17A6  ct_cd_auxiliary_descriptor_token_dispatch_table   [strong structural]
- Large local dispatch table reached from `16A6` for command bytes `>= 0x80`.
- Exact handler nouns remain open, but the dispatch-table role is now settled.

---

## Strengthened RAM/state labels

### 7E:2D00..7E:2DFF  ct_c1_service04_packed_tile_row_or_tile_batch_workspace   [strong correction]
- Pass 78 already proved this is a packed row/materialization workspace consumed by `4943`.
- Pass 79 strengthens the noun: the local `CD:13E6` builder modes are exact tile orientation modes over 32-byte tile-shaped blocks.
- Strongest safe reading now: packed tile-row / tile-batch workspace for the late service-04 graphics assembly path.

### 7E:CA32..7E:CA4F  ct_cd_two_auxiliary_descriptor_runtime_slot_structs_2x16   [strong structural]
- `0D33` clears this range in 16-byte slot steps.
- `15D5` seeds each active slot from a descriptor pointer looked up in `D1:646C`.
- `1609` ticks these slots, decrements their countdowns, and interprets stream tokens through `1654`.
- Strongest safe reading: two active runtime slot structs for the optional auxiliary descriptor stage.

### 7E:CA52..7E:CA8F  ct_cd_secondary_and_tertiary_auxiliary_descriptor_work_families   [provisional strengthened]
- Cleared alongside the active runtime slot family in `0D33`.
- Exact field meanings still need another pass, but these are parallel work families for the same optional auxiliary stage.

### 7E:CA93..7E:CA9F  ct_cd_auxiliary_descriptor_id_list_first_two_seed_runtime_slots   [strong correction]
- `0D33` only consumes the first two live ids here because the runtime expansion loop advances `X` by `0x10` and stops at `0x20`.
- So the first two live entries seed the two active runtime slots in `CA32..CA4F`.

### 7E:5D9B  ct_cd_optional_auxiliary_descriptor_stage_active_flag   [strong structural]
- Cleared at stage start by `0D28`.
- Checked by `1609` before any runtime-slot ticking occurs.
- Cleared again when the stage-level local completion condition is met.

### 7E:CCEA  ct_cd_optional_auxiliary_descriptor_stage_progress_byte   [provisional strengthened]
- `1609` only services runtime slots while this byte is zero.
- Incremented when the local two-slot service pass reaches its completion condition.
- Strongest safe reading: stage-level progression/completion byte for the optional auxiliary descriptor stage.

---

## Honest caution
Even after this pass:

- I have **not** fully frozen the artist-facing noun of the `D0` source entries.
- I have **not** fully frozen the final gameplay/object noun of the downstream `4500.. -> 5D00..` emit family.
- I have **not** decoded the entire `16B5..` token-handler table end-to-end.
- I have **not** fully frozen the exact field meanings of the `CA52 / CA72` parallel work families.
