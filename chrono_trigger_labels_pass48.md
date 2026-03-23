# Chrono Trigger Disassembly Labels — Pass 48

This file contains labels newly added, corrected, or materially strengthened in pass 48.

As in prior passes:
- **strong** = directly supported by control flow and data role in the ROM work of this pass
- **provisional** = structurally useful but still not safe as a final gameplay-facing name

---

## Strong labels

### C1:011F  ct_c1_format_u16_as_three_decimal_tile_bytes_949d_949f      [strong]
- Uses `9499` as the numeric working input.
- Repeatedly subtracts `0x64` and `0x0A` to derive hundreds/tens/ones.
- Maps those digits through `CC:F903`.
- Emits tile bytes to `949D`, `949E`, `949F` and sets `949C = 0xFF`.

### C1:0174  ct_c1_format_u16_as_two_decimal_tile_bytes_949e_949f        [strong]
- Repeatedly subtracts `0x0A` to derive tens and ones.
- Maps through `CC:F903`.
- Emits tile bytes to `949E`, `949F` and blanks `949C`, `949D` with `0xFF`.

### C1:104E  ct_c1_blank_leading_zero_decimal_tiles_949d_949e            [strong]
- Converts tile `0x73` at `949D` to `0xFF`.
- Converts tile `0x73` at `949E` to `0xFF` only when `949D` is already blank.
- This is a leading-zero suppression helper over the decimal tile buffer.

### CC:F903  ct_cc_decimal_digit_tile_table_73_to_7c                    [strong]
- Live digit tile codes used by `011F` and `0174` are:
  - `73 74 75 76 77 78 79 7A 7B 7C`
- Strongest safe reading: decimal digit tile codes for `0..9`.

### 7E:9499  ct_c1_decimal_tile_format_input_u16                        [strong]
- Working numeric input consumed by `011F` and `0174`.
- Loaded from per-lane record fields during `C1:0299` numeric field emission.

### 7E:949C..7E:949F  ct_c1_decimal_tile_format_output_4bytes           [strong]
- Shared 4-byte tile buffer emitted by the decimal formatter helpers.
- `949C` is used as a blank/fill slot.
- `949D..949F` hold the generated digit tiles before they are copied into the strip.

---

## Strengthened labels

### C1:0299  ct_c1_rebuild_full_companion_strip_0cc0                     [strengthened]
- Pass 47 proved this was the full rebuild entry.
- Pass 48 proves the dynamic helper-generated groups inside it are numeric fields, not generic glyph fragments.
- The strip therefore includes fixed lane glyph runs, decimal numeric fields, and later separator/bar logic.

### 7E:0CC0..7E:0E08  ct_c1_companion_paired_byte_strip_buffer           [strengthened]
- Pass 47 established full-strip rebuild and lane-anchor semantics.
- Pass 48 proves the strip contains lane-selected decimal presentation fields rendered from per-record numeric state.

### 7E:9F20  ct_c1_companion_strip_layout_mode_3state                    [strengthened]
- Pass 47 proved it selected among multiple strip layouts.
- Pass 48 tightens that role: it repositions the same numeric fields and controls whether later separator/bar logic is present.
- Strongest safe reading now: a 3-layout numeric panel mode selector.

### C0:A270..C0:A335  ct_c0_parallel_source_plane_consumer_band         [strengthened]
- Not promoted to a final high-level subsystem name.
- But this band now has stronger proven structure:
  - reads `7F:0C00/X`, `7F:0C80/X`, `7F:0E00/X`, `7F:0E80/X`
  - consumes those families as parallel source planes in a downstream copy path
- This materially strengthens the producer/consumer relationship from the strip/record side.

---

## Provisional labels

### CC:F8ED  ct_cc_live_three_lane_record_block_offsets_0000_0080_0100  [provisional]
- Proven live subgroup used by the numeric writer path:
  - `0000`
  - `0080`
  - `0100`
- Acts as the lane-selected record-block offset table for the dynamic numeric fields.
- Broader table family may contain additional entries beyond the live subgroup.

### 7E:5E30  ct_c1_lane_primary_numeric_field                           [provisional]
- Rendered through `011F` as a 3-digit decimal field in `C1:0299`.
- Structurally related to the `5E32` field by a pre-render compare.
- Final gameplay-facing meaning still open.

### 7E:5E32  ct_c1_lane_secondary_numeric_field                         [provisional]
- Rendered through `011F` as a second 3-digit decimal field.
- Its high byte is compared against `5E30` before rendering.
- Final gameplay-facing meaning still open.

### 7E:5E34  ct_c1_lane_aux_two_digit_numeric_field                     [provisional]
- Rendered through `0174` as a 2-digit decimal field.
- Final gameplay-facing meaning still open.

### 7E:A10F  ct_c1_numeric_threshold_or_warning_counter                 [provisional]
- Incremented when the pre-render compare between `5E30` and `5E32 >> 8` fails in one direction.
- Strongly acts like a counter or warning latch related to numeric inconsistency/overflow.
- Final semantics remain unresolved.

---

## Still intentionally unresolved

### Final gameplay-facing names of the three numeric fields             [unresolved]
- Pass 48 proves the fields are numeric and lane-selected.
- It does not yet prove whether they are HP/MP/level, another stat trio, or a different presentation family.

### Final routine identity of the bank-`C0` destination side            [unresolved]
- The source-plane relationship is stronger.
- The exact destination-side subsystem name is still not ready.
