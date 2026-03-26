# Chrono Trigger Disassembly Labels — Pass 44

This file contains labels newly added or materially strengthened in pass 44.

As in prior passes:
- **strong** = control flow and data role are directly supported by the ROM work in this pass
- **provisional** = structurally useful but still not safe as a final gameplay-facing name

---

## Strong labels

### 7E:0B40 / 00:0B40  ct_c1_tilemap_staging_buffer_vram7a00_0180        [strong]
- `0x180`-byte WRAM staging buffer.
- Written from ROM templates at `D1:5800`, `D1:5A50`, and `D1:5BD0`.
- Uploaded by DMA from the low-bank WRAM mirror `00:0B40` to VRAM address `7A00`
  when `99E2` is nonzero.

### 7E:99E2  ct_c1_tilemap_upload_pending_counter                         [strong]
- Dirty/request latch (or small counter) for the `0B40 -> VRAM 7A00` upload.
- Multiple bank-`C1` paths `INC` it after rewriting `0B40`.
- `CF:E380` checks it, performs the DMA upload, then clears it.

### CF:E380  ct_cf_upload_pending_tilemap_0b40_to_vram_7a00             [strong]
- Cross-bank sink for the `0B40` render buffer.
- If `99E2 != 0`, configures DMA to upload `0x0180` bytes from `00:0B40`
  to VRAM address `7A00`, then clears `99E2`.

### D1:5800  ct_d1_tilemap_template_default_0b40_0180                   [strong]
- Default/reset ROM template copied into `0B40` by `C1:1C3A`.
- Same size as the upload buffer and structurally part of the same tilemap-template family.

### D1:5A50  ct_d1_tilemap_template_alt_a_0b40_0180                     [strong]
- Alternate ROM template variant copied into `0B40` by the `0EA1..0EB1` path.
- Followed by `INC $99E2`, proving it feeds the same upload path as the default template.

### D1:5BD0  ct_d1_tilemap_template_alt_b_0b40_0180                     [strong]
- Alternate ROM template variant copied into `0B40` by the `1301..1315`,
  `1594..15A9`, and `15B5..15C5` paths.
- Followed by `INC $99E2`, proving it feeds the same upload path as the default template.

---

## Strengthened existing labels

### C1:1C3A  ct_c1_service2_restore_default_tilemap_template_0b40       [strong]
- Strengthened from pass 43.
- No longer just “restore workspace template.”
- Specifically restores the default `0x180`-byte tilemap/upload template from `D1:5800`
  into `0B40`, the staging buffer later DMA-uploaded to VRAM `7A00`.

---

## Provisional labels

### 7E:0B40  ct_c1_panel_or_screen_tilemap_buffer                        [provisional]
- Human-facing interpretation of the same `0B40` staging buffer.
- The tilemap/upload role is now strong.
- The exact panel/menu/screen name is still unresolved.

### D1:5800 / D1:5A50 / D1:5BD0  ct_d1_tilemap_template_family_16x12_words [provisional]
- The three source blocks are best interpreted as a 192-word (likely 16x12) template family.
- This matrix interpretation fits both the dense row-structured data and the fixed-size VRAM upload,
  but the exact UI vocabulary is still open.

---

## Still intentionally unresolved

### 7E:9F38  ct_c1_lane_emitted_aux_or_mask                              [provisional, unchanged]
- Re-checked during pass 44.
- The newly solved `0B40` upload path did not expose a trustworthy positive writer.
- Clear/consume behavior remains real; positive producer remains unresolved.
