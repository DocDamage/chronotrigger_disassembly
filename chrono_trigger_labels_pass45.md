# Chrono Trigger Disassembly Labels — Pass 45

This file contains labels newly added or materially corrected in pass 45.

As in prior passes:
- **strong** = directly supported by control flow and data role in the ROM work of this pass
- **provisional** = structurally useful but still not safe as a final gameplay-facing name

---

## Strong labels

### C1:07FD  ct_c1_compose_three_slot_panel_strip_into_0b40              [strong]
- Checks the three active-roster entries `A6D9 / A6DA / A6DB`.
- For each occupied entry, calls `C1:0929` with one of three horizontal destination positions
  inside `0B40`.
- Chooses merged/non-merged placement by shifting the second and third segment left by one
  word when the preceding slot is absent.
- Strongest safe reading: composes a 3-position horizontal panel strip in the `0B40` tilemap buffer.

### C1:0929  ct_c1_blit_6row_panel_segment_into_0b40_merge_left_border    [strong]
- Dynamic `0B40` patcher using source data from `D1:59FC`.
- Writes 6 rows with a destination stride of `0x40` bytes per row.
- Copies either:
  - 7 words per row (full segment), or
  - 6 words per row after skipping the first source word (merge mode)
- Strongest safe reading: blits a 6-row panel segment into `0B40`, optionally omitting
  the left border so adjoining segments share a border.

### D1:59FC  ct_d1_panel_segment_template_6x7_words                       [strong]
- Unique ROM source table used by `C1:0929`.
- Resolves cleanly as 6 rows of 7 words.
- Tile values form a compact border/interior segment template rather than logic data.

### 7E:0B40 / 00:0B40  ct_c1_tilemap_strip_buffer_32x6_words_vram7a00     [strong]
- Corrected from pass 44’s provisional geometry.
- The proven row stride from `C1:0929` is `0x40` bytes, yielding a 32-word by 6-row layout
  for the `0x0180`-byte uploaded strip.

### D1:5800 / D1:5A50 / D1:5BD0  ct_d1_base_strip_template_family_32x6     [strong]
- Corrected geometrically in this pass.
- All three `0x0180`-byte base templates are best modeled as 32-word by 6-row strip layouts.
- Used as the base tilemap copied into `0B40` before dynamic patching and upload.

---

## Strengthened / corrected labels

### 7E:0B40  ct_c1_panel_or_screen_tilemap_buffer                         [provisional -> corrected context]
- Still not given a final human-facing UI name.
- But now known much more concretely as a 32x6 strip buffer with dynamic three-slot panel composition.

### D1:5800 / D1:5A50 / D1:5BD0  ct_d1_tilemap_template_family_16x12_words [withdrawn]
- Pass 45 corrects this earlier provisional geometry.
- The safer keepable geometry is `32x6`, not `16x12`.

---

## Provisional labels

### D1:5800 / D1:5A50 / D1:5BD0  ct_d1_alt_base_strip_layout_family        [provisional]
- The three templates are clearly alternate base layouts within the same 32x6 strip region.
- Exact gameplay/UI mode names are still unresolved.

### 7E:0B40  ct_c1_lane_roster_strip_tilemap_buffer                        [provisional]
- Supported by the strong link from `C1:07FD` to the active-roster state.
- Kept provisional because the final gameplay-facing subsystem name is still open.

---

## Still intentionally unresolved

### 7E:9F38  ct_c1_lane_emitted_aux_or_mask                               [provisional, unchanged]
- Re-checked again during pass 45.
- The newly solved `07FD / 0929 / 59FC` layer did not expose a trustworthy positive writer.
- Clear/consume behavior remains real; positive producer remains unresolved.
