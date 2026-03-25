# Chrono Trigger Disassembly Labels — Pass 47

This file contains labels newly added, corrected, or materially strengthened in pass 47.

As in prior passes:
- **strong** = directly supported by control flow and data role in the ROM work of this pass
- **provisional** = structurally useful but still not safe as a final gameplay-facing name

---

## Strong labels

### C1:0299  ct_c1_rebuild_full_companion_strip_0cc0                     [strong]
- Begins by clearing/filling the full paired-byte `0CC0` strip.
- Stamps layout-dependent fixed glyphs based on `9F20`.
- Iterates the three lane blocks and writes both static and dynamic glyph groups.
- This is the full-strip rebuild entry, not just a local mutator.

### CC:FA23..CC:FA3F  ct_cc_companion_strip_lane_anchor_offset_family    [strong]
- Family of 3-entry 16-bit offset tables.
- Every table uses `0x80` lane spacing.
- Proven live subgroups:
  - `FA23` = `0029,00A9,0129`
  - `FA29` = `001B,009B,011B`
  - `FA2F` = `0068,00E8,0168`
  - `FA35` = `005A,00DA,015A`
  - `FA3B` = `0066,00E6,0166`
- These are lane-anchor tables for distinct `0CC0` strip subfields/layouts.

### CC:FADD  ct_cc_companion_strip_lane_block_offsets_0000_0080_0100     [strong]
- Proven live words used by `C1:08BF`:
  - `0000`
  - `0080`
  - `0100`
- Exact role: the three base offsets for the lane blocks inside the `0CC0` strip.

### C1:06F0  ct_c1_render_scaled_lane_bar_into_0cc0                      [strong]
- Uses `FA35[lane] + 0x1A` as the bar anchor.
- Scales per-lane state through the hardware divide helper at `C1:00D7`.
- Emits repeated `67` / `6F` glyphs and a partial tail tile into `0CC0`.
- Strongest safe reading: render a segmented bar/meter into the lane strip.

### CC:FAE9  ct_cc_companion_record_lane_marker_offsets_0002_0082_0102   [strong]
- Proven live words:
  - `0002`
  - `0082`
  - `0102`
- Used by `C1:1918..1969` to clear/stamp one of three `0E80` lane marker positions.

### C1:1918  ct_c1_refresh_current_0e80_lane_marker_glyphs               [strong]
- Clears the old marker block selected by `991F`.
- Stamps the current marker block selected by `95E5`.
- Writes `60/61/62/63` plus companion `29` bytes into `0E80/0EC0`.
- Strongest safe reading: refresh the current lane marker glyphs inside the `0E80` companion-record region.

---

## Strengthened labels

### C1:08E8  ct_c1_fill_current_companion_strip_slice_from_anchor_table   [strengthened]
- Pass 46 proved this was a slice-local `0CC0` update helper.
- Pass 47 tightens that role:
  - it selects an anchor from `FA23` or `FA29`
  - then fills five positions with `0x29`
- This is more specific than the earlier generic “update current slice” wording.

### 7E:0CC0..7E:0E08  ct_c1_companion_paired_byte_strip_buffer           [strengthened]
- Pass 46 proved geometry and row stride.
- Pass 47 proves a full-strip rebuild entry at `C1:0299` and a segmented bar renderer at `C1:06F0`.
- The buffer is now known to be lane-structured and layout-driven, not just a passive side strip.

### 7E:0E80..7E:0FFF  ct_c1_companion_record_buffer_0x180                [strengthened]
- Pass 46 proved the writer-side rebuild path.
- Pass 47 adds:
  - lane-marker anchor table `FAE9`
  - current-lane marker refresh at `C1:1918`
  - hard read-side consumer proof in bank `C0`
- This region is now known to participate in downstream composition, not just local build logic.

---

## Provisional labels

### 7E:99DD  ct_c1_lane_display_value_for_scaled_bar                     [provisional]
- Read by `C1:06F0` as one input to the segmented bar renderer.
- Reset/clear paths still mirror it from broader lane-carried state.
- Strong structural role, but final gameplay-facing meaning still open.

### 7E:9F22  ct_c1_lane_display_divisor_or_capacity                      [provisional]
- Read by `C1:06F0` as the other scaling input to the segmented bar renderer.
- Exact human-facing meaning still unresolved.

### 7E:9F20  ct_c1_companion_strip_layout_mode_3state                    [provisional]
- Selects among multiple `FAxx` lane-anchor tables.
- Also selects where fixed glyphs are stamped in the full-strip rebuild.
- Strongly acts like a 3-state layout selector, but the mode names remain unresolved.

### 7E:0CC0..7E:0E08  ct_c1_three_lane_status_or_command_strip           [provisional]
- Pass 47 makes the three-lane, layout-driven presentation role much stronger.
- Still not safe to commit to the final gameplay-facing subsystem name.

### 7E:0E80..7E:0FFF  ct_c1_three_lane_marker_record_presentation_block  [provisional]
- Strongly tied to lane markers and downstream consumption.
- Still not safe to collapse into “text”, “command labels”, or any narrower final name.

---

## Still intentionally unresolved

### C0:A2B0..A335 consumer path                                           [unlabeled as final routine]
- Pass 47 found direct `0E00/0E80` read-side proof there.
- Exact routine entry and full higher-level purpose are still open.
- The consumer relationship is real; the final routine label is not ready yet.

### 7E:9F38  ct_c1_lane_emitted_aux_or_mask                               [provisional, unchanged]
- Pass 47 stayed on the strip/record presentation seam.
- Positive writer side remains intentionally unresolved.
