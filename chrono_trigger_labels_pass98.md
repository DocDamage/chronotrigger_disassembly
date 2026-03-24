# Chrono Trigger Labels — Pass 98

## Purpose
This file records the label upgrades justified by pass 98.

Pass 97 sent the work back to the `CDC8 / CE0F / CFFF` pocket.
Pass 98 first scrubbed the remaining bad `CE0F` reader lead, then froze the nearest clean D1 controller instead of forcing a false noun.

The biggest correction is negative but valuable:

- `CD:BEF8` should no longer be treated as a believable clean direct `CE0F` reader

The biggest positive upgrade is nearby:

- `D1:EB70..EBCF` is now exact enough to freeze structurally
- `D1:EBD0..EBDE` is exact
- `D1:E9EF..E9FE` is now an exact table root
- `CE0E / CE10 / CE0B / CE0C / CE0D / CDCC..CDE7` are materially tighter than before

---

## Strong labels

### D1:EB70..D1:EBCF  ct_d1_step_active_profile_selector_toward_signed_ce0e_target_and_rebuild_14word_profile_into_cdcc_cde7   [strong structural]
- Exact behavior:
  - reads `CE0E`
  - derives unsigned target byte `CE0B` from it
  - compares target `CE0B` against active byte `CE0C`
  - if unchanged, returns immediately
  - otherwise increments `CE0A`, seeds `CE0D = 0x20`, updates `CE0C` toward the target, mirrors that result back into `CE0B`, then copies exactly `0x1C` bytes / 14 words into `CDCC..CDE7`
- Exact table roots used by the copy stage:
  - `D1:E9EF..E9FE`
  - `D0:FBE2..`
- Strongest safe reading: active selector/profile controller for one D1-side 14-word profile buffer.

### D1:EBD0..D1:EBDE  ct_d1_return_direct_or_0e_minus_dp45_based_on_ce10   [strong structural]
- Exact body:
  - `LDA $CE10`
  - if nonzero, return direct byte `$45`
  - otherwise return `0x0E - $45`
- Strongest safe reading: one-byte direct-vs-mirrored selector helper gated by the `CE10` latch.

### D1:E9EF..D1:E9FE  ct_d1_eight_entry_word_offset_table_for_cdcc_profile_rebuild   [strong structural]
- Exact 8-entry word table:
  - `00A0, 0100, 00C0, 0080, 00E0, 0060, 0040, 0020`
- Consumed by `D1:EB70..EBCF` as the exact offset selector table into `D0:FBE2`.

### D0:FBE2..  ct_d1_source_profile_word_table_root_for_cdcc_rebuild_controller   [strong structural]
- `D1:EB70..EBCF` uses `D1:E9EF` offsets into this exact ROM root.
- The helper copies exactly `0x1C` bytes / 14 words from here into `CDCC..CDE7`.
- Final gameplay-facing noun of the source profiles remains open.

---

## Strengthened RAM/state labels

### 7E:CE0E  ct_cd_d1_signed_profile_target_selector_byte   [strong structural]
- Earlier passes already proved auxiliary token `0xF7` writes the immediate byte here.
- Pass 98 proves clean D1-side consumption at `D1:EB70..EBCF`:
  - sign bit changes controller behavior
  - low 7 bits derive the target selector copied into `CE0B`
- Strongest safe reading: signed target selector byte shared between the older token path and the clean D1 profile controller.

### 7E:CE10  ct_cd_d1_direct_vs_mirrored_selector_latch   [provisional strengthened]
- Earlier passes proved token-side gate behavior.
- Pass 98 adds exact clean D1-side behavior at `D1:EBD0..EBDE`:
  - nonzero selects direct byte `$45`
  - zero selects `0x0E - $45`
- Strongest safe reading: one-bit direct-vs-mirrored selector latch, while the older token-local rewind-gate wording remains useful as a caution alias.

### 7E:CE0B  ct_d1_current_unsigned_profile_target_selector   [provisional strengthened]
- `D1:EB70..EBCF` derives this byte from `CE0E` and uses it as the immediate comparison target for `CE0C`.
- Mirrored from the newly updated active selector before profile rebuild.

### 7E:CE0C  ct_d1_active_profile_selector_byte_stepped_toward_ce0b   [provisional strengthened]
- `D1:EB70..EBCF` compares `CE0B` against this byte and updates this byte toward the target before rebuilding `CDCC..CDE7`.
- Exact table index is `2 * CE0C` into `D1:E9EF`.

### 7E:CE0D  ct_d1_profile_change_cooldown_or_arm_byte_seeded_to_20   [provisional strengthened]
- `D1:EB70..EBCF` writes exact value `0x20` here whenever the active selector changes.
- Final higher-level noun still wants one more pass, but the exact seed behavior is now frozen.

### 7E:CDCC..7E:CDE7  ct_d1_active_14word_profile_buffer_loaded_from_d0_fbe2_via_d1_e9ef   [provisional strengthened]
- Rebuilt by `D1:EB70..EBCF` only when the active selector changes.
- Exact size loaded is `0x1C` bytes / 14 words.
- Exact source path is `D1:E9EF -> D0:FBE2`.

---

## CE0F caution update

### 7E:CE0F  ct_d1_palette_seed_side_arm_or_epoch_byte   [caution sharpened]
- Pass 98 did **not** freeze a new direct reader.
- The strict mapped-code scan leaves only the already-known D1-side write facts as clean code:
  - `D1:E987` increments it
  - `D1:F26E` clears it
- The old `CD:BEF8` candidate should not be treated as clean CPU code.
- Strongest safe reading remains: write-side seed/epoch-style control byte inside the D1 palette/control cluster, with the first honest direct static reader still unresolved.

---

## Honest caution
Even after this pass:

- I have **not** frozen the first exact direct static reader of `CE0F`.
- I have **not** frozen the final gameplay-facing noun of the `CDCC..CDE7` 14-word profile buffer.
- I have **not** frozen the final gameplay-facing noun of the `D0:FBE2` source-profile family.
- I have **not** yet decided whether `CE0F` will yield statically at all, or whether it needs runtime proof instead.
