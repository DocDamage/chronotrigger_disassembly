# Chrono Trigger Disassembly Labels — Pass 46

This file contains labels newly added, corrected, or materially strengthened in pass 46.

As in prior passes:
- **strong** = directly supported by control flow and data role in the ROM work of this pass
- **provisional** = structurally useful but still not safe as a final gameplay-facing name

---

## Strong labels

### C1:081F  ct_c1_compose_three_slot_panel_strip_into_0b40              [strong]
- Corrected entry boundary for the pass-45 panel-strip composer.
- Begins with `STZ $84`, checks `A6D9/A6DA/A6DB`, selects destination offsets in `$82`,
  and repeatedly calls `C1:0929`.
- This is the actual `0B40` three-slot strip composer entry.

### C1:07BD  ct_c1_blit_companion_strip_template_a_into_0cc0_pair29      [strong]
- Outer loop = 6 rows.
- Inner loop = 7 source bytes per row.
- Reads from `CC:FA41`.
- Writes source byte to `0CC0+Y`, then constant `0x29` to `0CC1+Y`.
- Row stride = `0x40` bytes.

### C1:07EE  ct_c1_blit_companion_strip_template_b_into_0cc0_pair29      [strong]
- Same loop shape as `C1:07BD`.
- Reads from `CC:FA6B` instead of `CC:FA41`.
- Writes the same paired-byte pattern into the `0CC0` family.

### CC:FA41  ct_cc_companion_strip_template_a_6x7_bytes                  [strong]
- Compact ROM byte template consumed only by `C1:07BD` in this pass.
- Structurally matches the proven `6-row x 7-byte` loop.

### CC:FA6B  ct_cc_companion_strip_template_b_6x7_bytes                  [strong]
- Compact ROM byte template consumed only by `C1:07EE` in this pass.
- Structurally matches the proven `6-row x 7-byte` loop.

### 7E:0CC0..7E:0E08  ct_c1_companion_paired_byte_strip_buffer           [strong]
- Built with row stride `0x40`.
- Written as alternating byte pairs rather than tilemap words.
- Slice-local clear/update paths exist at `C1:086D` and `C1:08E8`.
- Strongest safe reading: a narrow companion strip buffer rebuilt alongside `0B40`.

### C1:086D  ct_c1_clear_current_companion_strip_slice_0cc0              [strong]
- Uses `95D5` to select a local slice.
- Clears two adjacent columns across six rows inside the `0CC0` companion strip family.
- Strongest safe reading: clear the current slice in the paired-byte companion strip.

### C1:08E8  ct_c1_update_current_companion_strip_slice                  [strong]
- Writes back into the same `0CC0 / 0D00` companion-strip family after slice clear.
- Uses selector tables rooted at `CC:FA23`, `CC:FA29`, and `CC:FADD`.
- Exact human-facing meaning still open, but the slice-local update role is strong.

### C1:0958  ct_c1_rebuild_companion_record_buffer_0e80                  [strong]
- Clears exactly `0x0180` bytes at `0E80+Y`.
- Then enters a 3-iteration build loop calling `C1:09B0`.
- Strongest safe reading: rebuild a full-size companion record buffer.

### 7E:0E80..7E:0FFF  ct_c1_companion_record_buffer_0x180                [strong]
- Full `0x0180`-byte region cleared and rebuilt by `C1:0958`.
- Distinct from the `0B40` tilemap-word strip and from the `0CC0` paired-byte strip.

### C1:09B0  ct_c1_emit_fixed_format_companion_record                    [strong]
- Checks the `C1:1580` per-entry control table.
- Copies 11 bytes from `CC:94A0` to `0B5E + 11*index` using `MVN`.
- Emits additional paired bytes into `0E86/0EC6` style regions with companion byte `0x2D`.
- Strongest safe reading: emit a fixed-format companion record.

### CC:94A0  ct_cc_companion_record_template_table                       [strong]
- ROM template source copied by `C1:09B0`.
- Used as structured record data, not code.

---

## Strengthened / corrected labels

### C1:07FD  ct_c1_compose_three_slot_panel_strip_into_0b40              [withdrawn as exact entry]
- Pass 45 used `07FD` as a broad anchor for the panel-strip composer.
- Pass 46 tightens the true entry to `C1:081F`.
- The earlier structural reading of the composer remains valid; the entry boundary was just too broad.

### D1:5800 / D1:5A50 / D1:5BD0  ct_d1_alt_base_strip_layout_family      [strengthened context]
- Pass 46 strengthens their caller-context roles:
  - `5800` = default/base restore through `C1:1C3A`
  - `5A50` = latched alternate via `A86A`
  - `5BD0` = transition/reset alternate in later state-advance paths

---

## Provisional labels

### D1:5800  ct_d1_base_strip_template_default                           [provisional]
- Caller context strongly suggests the default/base restore variant.
- Final gameplay-facing mode name still open.

### D1:5A50  ct_d1_base_strip_template_latched_alt                       [provisional]
- Single-shot alternate selected when `A86A` is nonzero, then that latch is cleared.
- Kept provisional until the higher-level mode name is pinned.

### D1:5BD0  ct_d1_base_strip_template_transition_alt                    [provisional]
- Copied in later state-transition/reset paths with surrounding controller bookkeeping.
- Strong structural role, but final mode name still unresolved.

### CC:FA23 / CC:FA29 / CC:FADD  ct_cc_companion_strip_selector_tables   [provisional]
- These tables clearly feed `C1:08E8` slice-local updates in the `0CC0` companion strip.
- Exact semantics of each selector lane remain open.

### 7E:0CC0..7E:0E08  ct_c1_roster_presentation_companion_strip          [provisional]
- Strongly linked to the same roster/strip refresh band as `0B40`.
- Kept provisional because the final gameplay-facing subsystem name is still unresolved.

### 7E:0E80..7E:0FFF  ct_c1_roster_presentation_companion_records        [provisional]
- Strongly linked to the same refresh band and built in three iterations.
- Still not safe to call text, icon metadata, or anything more specific yet.

---

## Still intentionally unresolved

### 7E:9F38  ct_c1_lane_emitted_aux_or_mask                               [provisional, unchanged]
- Pass 46 stayed on the strip/companion-buffer seam and did not expose a trustworthy positive writer.
- Clear/consume behavior remains real.
- Positive producer remains unresolved.
