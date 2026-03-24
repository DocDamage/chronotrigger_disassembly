# Chrono Trigger Labels — Pass 78

## Purpose
This file records the label upgrades justified by pass 78.

Pass 77 grounded the service-04 output path but left the front-half builder/materializer stages too fuzzy.

Pass 78 closes that specific seam:

- `C3:0002` is now pinned as a packed-stream-to-WRAM materializer veneer
- `C3:0557` is the real unpack/materialize worker returning output size in `0306`
- `CD:0015` and `CD:002A` are now pinned as the two fixed packed row-section builders for the `2D00..` workspace
- `CD:0018` is now pinned as the optional selector-driven auxiliary fragment-stage initializer / expander
- `2D00..` gets a tighter noun as a packed fragment-row stream workspace

This still stops short of a final gameplay-facing noun for the downstream `4500.. -> 5D00..` family, but the pre-decode pipeline is now materially clearer.

---

## Strengthened helper labels

### C3:0002..C3:0004  ct_c3_unpack_stream_to_caller_selected_wram_buffer_veneer   [strong]
- Exact body is `JMP $0557`.
- Used by service-04 and many other callers as the standard packed-stream-to-WRAM entry.
- Caller passes source pointer in `0300..0302`, destination pointer in `0303..0305`, and receives output size in `0306`.

### C3:0557..C3:08A8  ct_c3_unpack_packed_stream_to_wram_via_2180_and_return_output_size   [strong structural]
- Writes destination address through `$2181/$2183` and output bytes through `$2180`, proving it materializes directly into caller-selected WRAM.
- Contains multiple inner packed decode variants, but all branches are output materializers in the same family.
- Exit path stores `Y - start_dest_offset` into `0306`, so the returned value is output byte count / destination advance.

### CD:0015..CD:0017  ct_cd_build_first_four_packed_fragment_row_sections_into_2d00_veneer   [strong]
- Exact body is `JMP $1323`.
- Called unconditionally from `C1:4833` with `A = 987A`.

### CD:002A..CD:002C  ct_cd_build_last_two_packed_fragment_row_sections_into_2d00_veneer   [strong]
- Exact body is `JMP $1314`.
- Called unconditionally from `C1:4833` with `A = 987B`.

### CD:1314..CD:1322  ct_cd_build_last_two_packed_fragment_row_sections_into_2d00   [strong structural]
- Seeds `CACE = A`, `CACF = 4`, `CAD0 = 6`, then falls into the shared row-section builder.
- Therefore covers section ids `4..5`.
- Uses the `CD:1308` base-offset table to target `2D00 + 0014 / 0016`.

### CD:1323..CD:13C8  ct_cd_build_first_four_packed_fragment_row_sections_into_2d00   [strong structural]
- Seeds `CACE = A`, `CACF = 0`, `CAD0 = 4`.
- Therefore covers section ids `0..3`.
- Uses the same shared builder machinery as `1314`, targeting `2D00 + 000C / 000E / 0010 / 0012`.

### CD:1308..CD:1313  ct_cd_packed_fragment_row_section_base_offsets_000c_000e_0010_0012_0014_0016   [strong]
- Proven six-word table used by the shared `CD:1314/1323` builder loop.
- Supplies the six fixed base offsets for the `2D00..` row-section workspace.

### CD:0018..CD:001A  ct_cd_optional_selector_driven_auxiliary_fragment_stage_veneer   [strong]
- Exact body is `JMP $0D28`.
- Called conditionally from `C1:4833` only when `AE94 == 0`, `987C != FF`, and `AE93 != 37`.

### CD:0D28..CD:0D32  ct_cd_optional_selector_driven_auxiliary_fragment_stage   [strong structural]
- Clears `5D9B`, treats input `A` as the selector, runs `0EBD`, then runs `0D33`.
- This is the top-level coordinator for the optional pre-decode auxiliary stage.

### CD:0D33..CD:0D5F  ct_cd_clear_auxiliary_fragment_work_tables_and_expand_ca93_descriptor_list   [strong structural]
- Clears the `CA32 / CA52 / CA72` work families over the local loop.
- Then walks `CA93[...]` until `FF`, calling `15D5` for each live descriptor.
- Strongest safe reading: descriptor-list expander into auxiliary fragment work tables.

### CD:0EBD..CD:0F9F  ct_cd_init_auxiliary_fragment_stage_by_selector_and_battle_layout   [strong structural]
- Consumes the selector passed through `X` and checks live battle-layout / side-state bytes (`A017/A018`, `2A21`, `2C66/67`, etc.).
- Seeds the `CC91 / CC93 / CC95 / CCA2` family and related local state before the later `0D33` expansion stage.
- Strongest safe reading: selector/battle-layout initializer for the optional auxiliary fragment stage.

---

## Strengthened RAM/state labels

### 7E:0300..7E:0302  ct_c3_unpack_source_pointer   [strong structural]
- Caller-provided source pointer consumed by the standard `C3:0002 -> C3:0557` unpack/materialize worker.

### 7E:0303..7E:0305  ct_c3_unpack_destination_pointer   [strong structural]
- Caller-provided destination pointer for the same worker.
- `C3:0557` writes through the WRAM port using this destination address.

### 7E:0306..7E:0307  ct_c3_unpack_output_size_or_destination_advance   [strong structural]
- Exact worker exit stores `Y - start_dest_offset` here.
- Service-04 immediately uses it as the termination point for the materialized `2D00..` workspace.

### 7E:2D00..7E:2DFF  ct_c1_service04_packed_fragment_row_stream_workspace   [strong correction]
- Pass 77 proved this is a packed stream consumed by `4943`.
- Pass 78 tightens that noun: `CD:0015/002A` populate six fixed row-sections at offsets `000C/000E/0010/0012/0014/0016`, and `C3:0002` materializes packed bytes into the same workspace.
- Strongest safe reading: packed fragment-row stream workspace for the service-04 decode path.

### 7E:CA32..7E:CA8F  ct_cd_auxiliary_fragment_work_tables_primary_secondary_tertiary   [provisional strengthened]
- Cleared by `CD:0D33` before descriptor expansion.
- Populated indirectly from the `CA93` descriptor list via `15D5`.
- Final gameplay-facing noun still needs one more pass, but these are now clearly the core auxiliary-stage work tables.

### 7E:CA93..7E:CA9F  ct_cd_auxiliary_fragment_descriptor_list   [provisional strengthened]
- Walked by `CD:0D33` until `FF`.
- Each live byte triggers a `15D5` descriptor-expansion pass into the `CA32/52/72` work families.

---

## Honest caution
Even after this pass:

- I have **not** fully decoded the four transform/materialization modes under `CD:13E6`.
- I have **not** frozen the final gameplay-facing noun of the `CA32/52/72` auxiliary work families.
- I have **not** fully frozen the downstream noun of the `4500.. -> 5D00..` output family.
- The strongest proof on `C3:0557` is family role, WRAM-port output, and returned output size — not a full codec taxonomy.
