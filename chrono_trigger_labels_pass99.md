# Chrono Trigger Labels — Pass 99

## Purpose
This file records the label upgrades justified by pass 99.

Pass 98 tightened the clean D1 selector/profile controller but left the post-controller tail at
`EBDF..EC26` under-described.

Pass 99 closes the first real part of that seam:

- `CDC9` is no longer anonymous
- the three exact phase tables behind the window copier are frozen
- `EB00..EB4B` is now a real duplicated-profile / phase-window materialization path
- the effective source for the `EBDF` copier is now the doubled ring `CDCC..CE03`, not just `CDCC..CDE7`

I am still keeping the final gameplay-facing noun of the profile family and the promoted paired-band interiors below frozen.

---

## Strong labels

### D1:EA01..D1:EA20  ct_d1_find_first_matching_word_between_d0_fbe2_base_profile_and_20a2_window_then_store_index_to_cdc9   [strong structural]
- Exact body scans `D0:FBE2,X` against `20A2,X` for `X = 0,2,4,...,0x1A`.
- On the first equality, it stops and stores the current word index in `Y` to `CDC9`.
- If no match is found across the full 14-word span, it stores `0`.
- Strongest safe reading: exact local phase/match-index finder for `CDC9`.

### D1:EA21..D1:EA4A  ct_d1_three_14entry_circular_phase_offset_tables_base_plus4_plus10   [strong structural]
- Exact tables:
  - `EA21..EA2E`: `00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D`
  - `EA2F..EA3C`: `04 05 06 07 08 09 0A 0B 0C 0D 00 01 02 03`
  - `EA3D..EA4A`: `0A 0B 0C 0D 00 01 02 03 04 05 06 07 08 09`
- Consumed by `D1:EB1D..EB4B` using the current `CDC9` value.
- Strongest safe reading: exact base / `+4` / `+10` circular phase-offset tables.

### D1:EB00..D1:EB1C  ct_d1_decrement_ce0d_clear_ce0a_on_expiry_and_duplicate_cdcc_profile_into_cde8_ce03   [strong structural]
- Exact behavior:
  - `DEC $CE0D`
  - if zero, `STZ $CE0A`
  - copy exactly `0x1C` bytes / 14 words from `CDCC..CDE7` to `CDE8..CE03`
- Strongest safe reading: cooldown-expiry plus active-profile duplication helper that turns the 14-word profile into a doubled 28-word sliding source.

### D1:EB1D..D1:EB4B  ct_d1_materialize_three_14word_phase_windows_from_doubled_profile_ring_into_20a2_22a2_bands   [strong structural]
- Reads `CDC9` as the current phase index.
- Samples all three circular phase tables at `EA21 / EA2F / EA3D`.
- For each selected phase:
  - stores it to direct-page `$45`
  - calls `EBD0` to choose direct vs reversed phase index
  - calls `EBDF` to copy one 14-word window
- Exact destination `Y` offsets are `0x0000`, `0x0020`, and `0x0040`.
- Exact copy destinations are `20A2+Y` and `22A2+Y`.
- Strongest safe reading: three-window phase materializer into the promoted paired bands.

### D1:EBDF..D1:EBFF  ct_d1_copy_one_14word_window_from_cdcc_ce03_doubled_profile_ring_to_20a2_22a2_at_y   [strong structural]
- Exact body:
  - preserves `X`
  - converts input phase selector to `2 * A`
  - copies exactly 14 words from `CDCC+X` forward
  - mirrors the copy into both `20A2+Y` and `22A2+Y`
- This helper relies on `EB00..EB1C` having duplicated `CDCC..CDE7` into `CDE8..CE03` so that sliding contiguous reads do not need explicit wrap logic.
- Strongest safe reading: exact 14-word window copier from the doubled profile ring.

---

## Strengthened helper reading

### D1:EBD0..D1:EBDE  ct_d1_return_direct_or_0e_minus_dp45_based_on_ce10   [strong structural, local reading sharpened]
- Exact body remains:
  - if `CE10 != 0`, return direct `$45`
  - otherwise return `0x0E - $45`
- In the pass-99 caller contract, the strongest local reading is:
  - direct-vs-reversed 14-step phase-selector helper gated by `CE10`

---

## Strengthened RAM / workspace labels

### 7E:CDC9  ct_d1_profile_phase_match_index_byte_for_three_window_materializer   [strong structural]
- `D1:EA01..EA20` computes and writes this byte exactly.
- `D1:EB1D..EB4B` consumes it exactly as the index into the three circular phase tables.
- Strongest safe reading: local phase/match index byte for the three-window materialization path.

### 7E:CDE8..7E:CE03  ct_d1_duplicated_trailing_half_of_active_profile_ring_for_contiguous_sliding_window_reads   [strong structural]
- Exact write source is `CDCC..CDE7`.
- Exact writer is `D1:EB00..EB1C`.
- Exact consumer is `D1:EBDF..EBFF`.
- Strongest safe reading: duplicated tail extension that makes the active profile a 28-word sliding source.

### 7E:CDCC..7E:CDE7  ct_d1_active_14word_profile_buffer_loaded_from_d0_fbe2_via_d1_e9ef   [provisional strengthened]
- Pass 98 froze the rebuild source path.
- Pass 99 adds exact downstream behavior:
  - duplicated into `CDE8..CE03`
  - then consumed as the head half of the doubled sliding profile ring for `EBDF`
- Strongest safe reading stays the same, but the downstream materialization contract is now exact.

### 7E:CE10  ct_cd_d1_direct_vs_mirrored_selector_latch   [provisional strengthened]
- Pass 98 froze the tiny helper at `EBD0`.
- Pass 99 tightens the local meaning:
  - it chooses direct vs reversed phase selection for the three-window materializer at `EB1D..EB4B`.

---

## Honest caution
Even after this pass:

- I have **not** frozen the exact purpose of `D1:EB4C..EB6F`.
- I have **not** fully frozen `D1:EA5F..EAF4`, the in-place active-profile convergence loop that runs before duplication/materialization when `CE0A != 0`.
- I have **not** frozen the final gameplay-facing noun of the `CDCC..CE03` profile family.
- I have **not** frozen the final gameplay-facing noun of the `20A2/22A2` promoted paired-band interiors that receive the three materialized windows.
- I have **not** found a clean direct static reader of `CE0F`.
