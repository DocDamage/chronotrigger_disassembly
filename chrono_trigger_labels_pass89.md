# Chrono Trigger Labels — Pass 89

## Purpose
Pass 88 froze the ownership of the `C161..C7F3` neighborhood as a real
**dual-bundle eight-table raster-target workspace**, but the local D1 write-side cluster
still needed a sharper noun.

Pass 89 tightens that cluster.

The strongest keepable result is:

- `D1:EDCD..EE2F` is an exact lower-edge byte stamp into one selected primary/shadow lane family
- `D1:EE33..EE95` is an exact companion word-span fill across a clamped range
- `D1:EEA6..EEC4` is an exact descending ramp seed tied to `CD3A`
- `D1:EEC5..F107` is a real curve/profile writer for the first four primary lanes
- the strongest safe structural noun is now a local **primary-lane build + mirror pipeline**

I am still keeping the final gameplay-facing effect noun below frozen.

---

## Strong labels

### D1:EDCD..D1:EE2F  ct_d1_stamp_clamped_lower_edge_byte_into_selected_primary_or_shadow_four_lane_family   [strong structural]
- Reads one selector byte from `[$40]` and takes this path only when that selector is zero.
- Computes `low = max(0, 5DA0 - CD3A)` and `high = min(0xFF, 5DA0 + CD3A)`.
- If `CD3A < 0x08`, increments `CD3A`.
- Exact write loop uses only the low byte in `$45`, not the computed high edge.
- Exact primary roots written when `7C.bit0 == 0`: `C161 / C235 / C309 / C3DD`.
- Exact shadow roots written when `7C.bit0 != 0`: `C4E1 / C5B5 / C689 / C75D`.
- Loop advances `X += 4` until `X == 0x00D4`.
- Strongest safe reading: clamped lower-edge byte stamp into one selected four-lane family.

### D1:EE33..D1:EE95  ct_d1_fill_selected_primary_or_shadow_companion_word_lane_across_clamped_span   [strong structural]
- This is the selector-nonzero path from the same local cluster.
- Computes `low = max(0, 5DA1 - CD3B)` and `high = min(0xD4, 5DA1 + CD3B)`.
- If `CD3B < 0x09`, increments `CD3B`.
- Converts `low` and `high` to 4-byte stepped offsets.
- Exact fill value is `0xFF00`.
- Exact roots: primary `C163`, shadow `C4E3`, selected by `7C.bit0`.
- Strongest safe reading: companion clamped-span fill over one selected word lane.

### D1:EEA6..D1:EEC4  ct_d1_seed_descending_word_ramp_into_primary_c15f_lane_family_from_cd3a   [strong structural]
- Computes `Y = (0xC0 - CD3A) * 4`.
- With `A=0`, stores ascending 16-bit values `0, 1, 2, ...` into `C15F + Y`, stepping backwards by 4 each iteration until `Y < 0`.
- Increments `CD3A` before returning.
- Strongest safe reading: descending ramp seed for the primary `C15F` lane family controlled by `CD3A`.

### D1:EEC5..D1:F107  ct_d1_build_primary_four_lane_curve_profile_from_cef48e_e500_and_center_words   [strong structural]
- Updates `CD3A` from the stream byte at `[$40]`.
- Derives `4B = 0x60 - CD3A`, `4D = (0x60 - CD3A) >> 1`, `45 = 7C * 4`, `47 = 7C * 2`.
- Builds `4F` and `51` from exact sums of `CA5A + CA5E` and `CA5C + CA60`.
- Iterates across an exact `0x350` span in `Y += 8` steps.
- Samples the monotone table at `CE:F48E` and uses `4202 / 4203 / 4217` hardware multiply.
- Stores signed/profile-adjusted results into the first four primary lanes rooted at `C15D / C15F / C161 / C163`.
- Strongest safe reading: primary four-lane curve/profile writer feeding the raster-target workspace.

### D1:EF63..D1:EFCF  ct_d1_store_signed_profile_sample_into_primary_c15d_and_c161_lanes_and_prime_secondary_multiply   [strong structural]
- Sign-extends the sampled byte when required.
- Adds it to baseline table word `E500,Y`.
- Stores the result to both `C15D,Y` and `C161,Y`.
- Then seeds the next hardware multiply from `CE:F48E` using the `45 / 4D` path.
- Strongest safe reading: signed sample store helper for the `C15D / C161` primary pair.

### D1:F0E9..D1:F107  ct_d1_store_signed_profile_sample_into_primary_c15f_and_c163_lanes   [strong structural]
- Sign-extends the sampled byte when required.
- Adds it to center word `51`.
- Stores the result to both `C15F,Y` and `C163,Y`.
- Strongest safe reading: signed sample store helper for the `C15F / C163` primary pair.

---

## Strengthened RAM / workspace labels

### 7E:C15D..7E:C4AB  ct_d1_primary_curve_written_lane_family_upstream_of_raster_target_workspace   [provisional strengthened]
- Pass 89 proves `D1:EEC5..F107` writes four exact primary lanes rooted at `C15D / C15F / C161 / C163` over a `0x350` span.
- Those lanes sit immediately upstream of the pass-88 raster-target workspace and are part of the same local D1-side write pipeline.
- Final gameplay-facing noun still open.

### 7E:CD3A  ct_d1_primary_lane_growth_byte_for_lower_edge_and_ramp_seed_paths   [stronger support]
- Used by `D1:EDCD..EE2F` for the lower-edge byte stamp path.
- Used again by `D1:EEA6..EEC4` and `D1:EEC5..F107` to control ramp/profile generation.
- Strongest safe reading: local growth byte for the primary lower-edge/ramp side.

### 7E:CD3B  ct_d1_companion_lane_growth_byte_for_clamped_span_fill_path   [stronger support]
- Used by `D1:EE33..EE95` to build the clamped companion span.
- Incremented locally until it reaches `0x09`.
- Strongest safe reading: local growth byte for the companion span-fill side.

---

## Honest caution kept explicit
Even after this pass:

- I have **not** frozen the final gameplay-facing noun of the raster-target workspace.
- I have **not** frozen the exact higher-level caller contract connecting the new primary-lane writer to its final presentation/effect name.
- I have **not** frozen the first exact external reader of `CE0F` in clean code territory.
- I have **not** promoted the lone mapped `LDA $CE0F` opcode-pattern hit because it still sits in dense bank-CD script/data territory.
