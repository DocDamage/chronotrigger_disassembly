# Chrono Trigger Labels — Pass 100

## Purpose
This file records the label upgrades justified by pass 100.

Pass 99 froze the `CDC9 -> phase tables -> doubled ring -> three-window materializer` path,
but it still left the feeder loop at `D1:EA5F..EAF4` under-described.

Pass 100 closes the color semantics of that seam:

- `EA5F..EAF4` is not a generic profile stepper; it is an exact per-channel **BGR555 palette convergence loop**
- `D0:FBE2..FD01` is no longer just a vague source-profile root; it is a compact family of **base + selectable 16-word palette profiles**
- `CDCC..CE03` is no longer just a profile ring; it is an **active 14-color palette ring** that gets duplicated, windowed, and copied into the promoted palette bands
- `CE0A / CE0D / CE0B / CE0C` are materially tighter as the latch, cooldown, and selector bytes for that palette transition path

I am still keeping `D1:EB4C..EB6F` as caution because its exact local behavior is clear but it still leaves no persistent state before falling into the selector rebuild.

---

## Strong labels

### D1:EA4B..D1:EA5E  ct_d1_guard_palette_profile_maintenance_tick_on_aux_stage_and_slot_activity_then_branch_by_ce0a   [strong structural]
- Exact body ORs `5D9B`, `05A4`, `0598`, `058C`, and `0580`.
- If any of those bytes are nonzero, it returns immediately.
- If all are zero and `CE0A != 0`, it enters the active in-place convergence path at `EA5F`.
- If all are zero and `CE0A == 0`, it jumps to `EB4C`, which then falls into the selector/profile rebuild path at `EB70`.
- Strongest safe reading: exact top-level guard/dispatcher for one D1 palette-profile maintenance tick.

### D1:EA5F..D1:EAF4  ct_d1_step_each_bgr555_channel_of_active_14color_palette_toward_selected_target_profile_in_place   [strong structural]
- Exact loop walks 14 words across `CDCC..CDE7` using `Y = 0,2,4,...,0x1A`.
- Exact target source is the selector-chosen 14-word span under `D0:FBE2 + D1:E9EF[2 * CE0B]`.
- For each current target word pair:
  - low `0x001F` field is compared and stepped by `±1`
  - middle `0x03E0` field is compared and stepped by `±0x0020`
  - high-byte `0x7C` field is compared and stepped by `±0x04` in the byte, i.e. `±0x0400` in the 16-bit word
- Those three masks correspond exactly to the three component fields of SNES `BGR555` color words.
- Strongest safe reading: exact in-place palette tween/convergence loop for the active 14-color profile.

### D0:FBE2..D0:FD01  ct_d1_base_plus_eight_selectable_16word_bgr555_palette_profiles_root   [strong structural]
- `D1:EA01..EA20` compares against the first 14 words at the root `D0:FBE2`.
- `D1:E9EF..E9FE` selects eight `0x20`-byte-spaced target records under this same root.
- Each selected record is treated by `EA5F..EAF4` and `EB70..EBCF` as a 14-word live palette span, with two trailing words unused by the active copy loops.
- Strongest safe reading: compact ROM root containing one base palette profile plus eight selectable target palette profiles.

---

## Strengthened helper readings

### D1:E9EF..D1:E9FE  ct_d1_eight_entry_word_offset_table_for_selectable_target_palette_profiles   [strong structural]
- Exact eight-entry word table remains:
  - `00A0, 0100, 00C0, 0080, 00E0, 0060, 0040, 0020`
- Pass 100 tightens the noun of those offsets:
  - they select the eight target `0x20`-byte palette-profile records rooted at `D0:FBE2`
- Strongest safe reading: exact offset table for the eight selectable target palette profiles.

### D1:EA01..D1:EA20  ct_d1_find_first_matching_word_between_d0_fbe2_base_profile_and_20a2_window_then_store_index_to_cdc9   [strong structural, color noun strengthened]
- Exact code body remains unchanged.
- Pass 100 tightens the compared noun:
  - the match is between the base 14-color palette profile at `D0:FBE2` and the first materialized 14-color window at `20A2..20BD`
- Strongest safe reading stays exact, but this is now clearly a palette-window phase index finder rather than a generic word matcher.

### D1:EB00..D1:EB1C  ct_d1_decrement_ce0d_clear_ce0a_on_expiry_and_duplicate_cdcc_profile_into_cde8_ce03   [strong structural, palette noun strengthened]
- Exact behavior remains unchanged.
- Pass 100 tightens the noun of the copied data:
  - this is the active 14-color palette profile being duplicated into a second 14-color tail so the later window reader can slide contiguously.

### D1:EB1D..D1:EB4B  ct_d1_materialize_three_14word_phase_windows_from_doubled_profile_ring_into_20a2_22a2_bands   [strong structural, palette noun strengthened]
- Exact control flow remains unchanged.
- Pass 100 tightens the noun of the copied windows:
  - they are three 14-color palette windows copied into the interiors of the promoted palette bands rooted at `20A0` and `22A0`.

### D1:EBDF..D1:EBFF  ct_d1_copy_one_14word_window_from_cdcc_ce03_doubled_profile_ring_to_20a2_22a2_at_y   [strong structural, palette noun strengthened]
- Exact body remains unchanged.
- Pass 100 tightens the noun of the copied words:
  - this is one 14-color BGR555 palette window copied into both promoted palette-band interiors.

---

## Strengthened RAM / workspace labels

### 7E:CDCC..7E:CDE7  ct_d1_active_14color_bgr555_palette_profile_buffer   [strong structural]
- `D1:EB70..EBCF` rebuilds this span from the selector-chosen target record under `D0:FBE2`.
- `D1:EA5F..EAF4` then steps every color channel in place toward that target profile.
- `D1:EB00..EB1C` duplicates this exact 14-color span into `CDE8..CE03`.
- Strongest safe reading: active 14-color BGR555 palette profile buffer.

### 7E:CDE8..7E:CE03  ct_d1_duplicated_trailing_half_of_active_14color_palette_ring_for_contiguous_window_reads   [strong structural]
- Exact write source is the active 14-color palette profile at `CDCC..CDE7`.
- Exact consumer remains `D1:EBDF..EBFF`.
- Pass 100 tightens the noun from generic profile data to exact palette data.

### 7E:CE0A  ct_d1_active_palette_profile_convergence_latch   [strong structural]
- `D1:EB70..EBCF` increments this byte whenever the selector/profile controller detects a change and seeds a new active transition.
- `D1:EA4B..EA5E` uses nonzero `CE0A` to choose the in-place convergence path.
- `D1:EB00..EB1C` clears it when `CE0D` expires.
- Strongest safe reading: latch/flag marking an active palette-profile convergence phase.

### 7E:CE0D  ct_d1_palette_profile_convergence_cooldown_byte   [strong structural]
- `D1:EB70..EBCF` seeds this byte to `0x20` when a new selector transition begins.
- `D1:EB00..EB1C` decrements it every active convergence tick and clears `CE0A` on expiry.
- Strongest safe reading: exact per-transition cooldown/countdown byte for the active palette convergence path.

### 7E:CE0B  ct_d1_target_palette_profile_selector_byte   [strong structural]
- `D1:EB70..EBCF` derives this byte from signed `CE0E` and mirrors the current selector step result back into it.
- `D1:EA5F..EAF4` reads it exactly as the selector for the target palette-profile record.
- Strongest safe reading: target palette-profile selector byte.

### 7E:CE0C  ct_d1_active_palette_profile_selector_byte_stepped_toward_ce0b   [strong structural]
- `D1:EB70..EBCF` compares this byte against `CE0B`, steps it toward the target, then uses `2 * CE0C` as the index into `D1:E9EF`.
- Pass 100 tightens the noun from generic profile selection to exact palette-profile selection.

### 7E:CDC9  ct_d1_profile_phase_match_index_byte_for_three_window_materializer   [strong structural, palette noun strengthened]
- Exact code meaning remains unchanged.
- Pass 100 tightens the noun:
  - it is a phase/match index inside the materialized 14-color palette windows.

---

## Honest caution
Even after this pass:

- `D1:EB4C..EB6F` still resolves only as a side-effect-free threshold-doubling probe over `5FB2 >> 3` and `5FB0` before falling into the selector rebuild.
- I have **not** frozen the final gameplay-facing noun of the higher-level subsystem that owns this palette-transition path.
- I have **not** frozen the exact noun of the four low-RAM bytes `0580 / 058C / 0598 / 05A4` checked by the `EA4B` guard.
- I have **not** found a clean direct static reader of `CE0F`.
