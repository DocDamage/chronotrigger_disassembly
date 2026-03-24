# Chrono Trigger Labels — Pass 87

## Purpose
This file records the label upgrades justified by pass 87.

Pass 86 proved that `CD0D..CD1B` was a real point-pair work bundle,
but it still left the downstream `F8EB / F91C / F972 / F9AF / F9E7` cluster too fuzzy.

Pass 87 freezes that cluster as a real **column-raster** family:

- `F8EB` sorts four point pairs by the **second byte** ascending
- `F972` is the signed row-per-column hardware-divide helper
- `F91C` computes the four edge steps for the work bundle
- `F9AF` loads the bundle, saves the target selector in `CC64`, and dispatches the rasterizer
- `F9E7` is a real three-case column rasterizer
- `CD:38B2..38E3` seeds the WRAM-port address for one of four interleaved target strips

This also justifies one local correction:

- for the `EC28 -> F9AF` path, the strongest local reading is now
  `5DA0 = row/Y-like`, `5DA1 = column/X-like`

I am still keeping the final presentation noun one notch below frozen.

---

## Strong labels

### D1:F8EB..D1:F91B  ct_d1_sort_four_row_column_point_pairs_by_column_byte_ascending   [strong structural]
- Exact body is a four-pass bubble-sort-style loop comparing `13/15/17/19` and swapping the paired bytes `12/14/16/18` in lockstep.
- Strongest safe reading: in-place sort of four `(row,column)` point pairs by the second-byte column/X key ascending.

### D1:F91C..D1:F971  ct_d1_compute_four_signed_row_per_column_edge_steps_for_cd0d_fourpoint_bundle   [strong structural]
- Calls `F972` four times and stores the returned signed steps into local slope slots `03 / 05 / 07 / 09`.
- Exact edge schedule is `(12,13)->(16,17)`, `(16,17)->(18,19)`, `(12,13)->(14,15)`, `(14,15)->(18,19)`.
- Strongest safe reading: edge-step builder for the D1 four-point column-raster work bundle.

### D1:F972..D1:F9AE  ct_d1_compute_signed_row_per_column_step_via_hw_divide   [strong structural]
- Uses `4204/4206` and reads quotient `4214` after taking the signed row delta between `0B` and `0C` and the column delta in `0D`.
- Restores sign on the negative path and returns the signed step in `Y`.
- Strongest safe reading: reusable signed slope helper for the column rasterizer.

### D1:F9AF..D1:F9E6  ct_d1_load_cd0d_fourpoint_bundle_set_cc64_target_selector_sort_and_dispatch_column_rasterizer   [strong structural]
- Saves `X` into `CC64`, loads `CD0D..CD1B` into `12..19`, calls `F8EB`, temporarily sets `DB=00`, then calls `F9E7`.
- Strongest safe reading: wrapper/dispatcher for rasterizing one four-point work bundle into the selected column target family.

### D1:F9E7..D1:FB67  ct_d1_column_rasterize_sorted_fourpoint_bundle_into_wram_port_target_in_three_cases   [strong structural]
- Chooses among three exact cases from `13 == 15` and the middle-row ordering test `16 ? 14`.
- All three cases call `CD:38B2` with start column `0F`, use the signed steps in `03 / 05 / 07 / 09`, and stream paired row values column by column into the selected WRAM-port target.
- Strongest safe reading: three-case column rasterizer for the sorted four-point bundle.

### CD:38AA..CD:38B1  ct_cd_column_raster_wram_port_base_table_4words   [strong structural]
- Exact four-word table used by `CD:38B6..38E3`: `C161 / C163 / C4E1 / C4E3`.
- Strongest safe reading: base-address table for four interleaved WRAM target strips used by the column rasterizer.

### CD:38B2..CD:38E3  ct_cd_seed_wram_port_address_for_column_raster_target_from_a_cc64_and_7c   [strong structural]
- `CD:38B2` is an exact wrapper `JSR $38B6 ; RTL`.
- `CD:38B6..38E3` multiplies the incoming `A` by `4`, combines `7C.bit0` and `CC64.bit0` into a 0..3 selector, adds that column offset to one base from `CD:38AA..38B1`, writes the result to `2181`, and writes bank `7E` to `2183`.
- Strongest safe reading: WRAM-port seed helper for one of four interleaved column-raster targets.

---

## Strengthened RAM/state labels

### 7E:CD0D..7E:CD1B  ct_d1_four_row_column_point_pair_work_bundle_for_column_rasterizer   [strong structural]
- `EC28` builds four point pairs here and immediately calls `F9AF`.
- `F9AF` loads exactly these eight bytes into direct-page work slots `12..19`, sorts them by the second byte, and rasterizes them.
- Strongest safe reading: four `(row,column)` point-pair work bundle for the D1 column rasterizer.

### 7E:CC64  ct_cd_d1_column_raster_target_selector_byte   [stronger structural]
- `D1:F9AF` stores `X` here before dispatch.
- `CD:38B6..38E3` masks `CC64.bit0`, combines it with `7C.bit0`, and uses the result to choose one of the four WRAM-port base addresses in `CD:38AA..38B1`.
- Strongest safe reading: local target-strip selector byte for the column-raster family.

---

## Corrections / caution kept explicit

### 7E:5DA0..7E:5DA5  ct_cd_d1_current_three_pair_point_bundle   [strong structural, orientation corrected locally]
- Pass 86 correctly froze this family as a real three-pair point bundle.
- Pass 87 tightens the local `EC28 -> F9AF` orientation: the downstream column rasterizer proves the **second** byte of each pair is the column/X byte.
- Therefore the strongest local reading for this path is `5DA0 = row/Y-like`, `5DA1 = column/X-like`.
- I am keeping that orientation correction local until one more consumer proves it globally.

---

## Honest caution
Even after this pass:

- I have **not** frozen the final presentation noun of the four-point bundle at `CD0D..CD1B`.
- I have **not** frozen the final higher-level noun of the four WRAM target strips rooted by `CD:38AA..38B1`.
- I have **not** frozen the first exact external reader of `CE0F`.
- I have **not** promoted the remaining low-half `CE0F` code-like hits, because they still sit inside dense script/data neighborhoods.
