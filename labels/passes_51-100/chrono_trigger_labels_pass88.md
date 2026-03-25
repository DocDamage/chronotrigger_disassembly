# Chrono Trigger Labels — Pass 88

## Purpose
This file records the label upgrades justified by pass 88.

Pass 87 froze the downstream `F8EB / F91C / F972 / F9AF / F9E7` cluster as a real
column-raster family, but the WRAM targets rooted by `C161 / C163 / C4E1 / C4E3`
still lacked a firm owner.

Pass 88 upgrades that seam.

The strongest keepable result is:

- the `7E:C161..7E:C7F3` neighborhood is a real **dual-bundle eight-table raster-target workspace**
- `CE:E000..E08D` mirrors selected `0x6C` bands between two eight-table bundles
- `D1:F5F6..F676` mirrors selected `0x70` bands between the companion eight-table bundles
- `D1:FD80..FE46` performs the transformed mirror for that same `0x70` family
- `7C.bit0` is the exact direction selector for all of those helpers

I am still keeping the final presentation noun below frozen.

---

## Strong labels

### CE:E000..CE:E08D  ct_ce_mirror_selected_0x6c_band_between_primary_and_shadow_eight_table_raster_target_bundles   [strong structural]
- Reads one byte from `[$40]`, doubles it, computes stop offset `start + 0x006C`, then mirrors that selected band across eight exact root tables.
- Exact primary roots: `C161 / C1CD / C239 / C2A5 / C311 / C37D / C3E9 / C455`.
- Exact shadow roots: `C4E1 / C54D / C5B9 / C625 / C691 / C6FD / C769 / C7D5`.
- When `7C.bit0 != 0`, direction is primary -> shadow; otherwise shadow -> primary.
- Strongest safe reading: selected-band mirror helper for one `0x6C` raster-target bundle family.

### D1:F5F6..D1:F676  ct_d1_mirror_selected_0x70_band_between_primary_and_shadow_companion_raster_target_bundles   [strong structural]
- Mirrors one selected `0x70` window between the exact root families below, in `X += 4` steps.
- Exact primary roots: `C163 / C1D3 / C243 / C2B3 / C323 / C393 / C403 / C473`.
- Exact shadow roots: `C4E3 / C553 / C5C3 / C633 / C6A3 / C713 / C783 / C7F3`.
- `7C.bit0` chooses primary -> shadow vs shadow -> primary.
- Strongest safe reading: companion selected-band mirror helper for the `0x70` raster-target family.

### D1:FD80..D1:FE46  ct_d1_transform_and_mirror_selected_0x70_band_between_companion_raster_target_bundles   [strong structural]
- Uses the exact same root families as `D1:F5F6..F676`, but applies `EOR #$FFFF ; XBA` before every store.
- `7C.bit0` again chooses direction.
- Strongest safe reading: transformed selected-band mirror helper for the same companion `0x70` raster-target family.

---

## Strengthened RAM/workspace labels

### 7E:C161..7E:C7F3  ct_ce_d1_dual_bundle_eight_table_raster_target_workspace   [stronger structural]
- Pass 87 proved the column-rasterizer writes into roots selected through `C161 / C163 / C4E1 / C4E3`.
- Pass 88 proves those roots belong to a larger structured workspace with exact mirror helpers spanning the full `C161..C7F3` neighborhood.
- Strongest safe reading: dual-bundle eight-table raster-target workspace with primary and shadow sides.

### 7E:7C.bit0  ct_ce_d1_raster_target_bundle_direction_select_bit   [stronger structural]
- `CE:E000..E08D`, `D1:F5F6..F676`, and `D1:FD80..FE46` all branch on `7C.bit0` to decide copy direction.
- Strongest safe reading: active/shadow bundle direction selector bit for the raster-target mirror family.

---

## Honest caution kept explicit
Even after this pass:

- I have **not** frozen the final presentation noun of the workspace at `C161..C7F3`.
- I have **not** frozen the first exact higher-level caller contract that explains why one family mirrors in `0x6C` windows and the other in `0x70` windows.
- I have **not** frozen the full write-side semantics of the nearby `EDF3 / EE50 / EEA6` cluster.
- I have **not** found the first exact external reader of `CE0F` in clean code territory.
