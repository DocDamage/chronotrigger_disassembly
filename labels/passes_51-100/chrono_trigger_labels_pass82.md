# Chrono Trigger Labels — Pass 82

## Purpose
This file records the label upgrades justified by pass 82.

Pass 81 proved that token `0x80` in the auxiliary `CD:0018` VM reaches exact D1-bank wrappers, but the D1 targets still had no strong nouns.

Pass 82 closes that gap:

- sub-op `0x17` can now be tightened from a fuzzy anchored entry to an **exact wrapper** to `D1:E984`
- `D1:E899` and `D1:E8C1` are now pinned as exact **`0x7FFF` sentinel-fill helpers** for paired palette-band work tables
- `D1:E91A` and `D1:E984` are now pinned as complementary **promote/copy** vs **seed/snapshot** helpers
- `D0:FD00..D0:FD5F` is now pinned as the exact ROM-side **48-color seed block**
- `0520..0543` and `0544..0567` are now much more strongly tied together as two adjacent **3-record palette/effect descriptor slabs**

This still does **not** freeze the final gameplay-facing noun of every `20xx/21xx/22xx/23xx` band.
The labels stay structural where the last step still needs runtime proof.

---

## Strengthened helper labels

### CD:2AAA..CD:2AAE  ct_cd_auxiliary_token_80_subop_17_exact_wrapper_call_d1_e984   [strong correction]
- Exact body: `JSL D1:E984 ; RTS`.
- The local code at `CD:2AAF..` belongs to the shared helper used by sub-op `0x16`, not to sub-op `0x17`.

### D1:E899..D1:E8C0  ct_d1_fill_palette_band_pairs_2040_2240_and_2120_2320_with_7fff_sentinel   [strong]
- Fills `7E:2040..20FF` and `7E:2240..22FF` with `0x7FFF`.
- Then fills `7E:2120..217F` and `7E:2320..237F` with the same sentinel.
- Exact structural role: paired palette-band/table sentinel initializer.

### D1:E8C1..D1:E8D4  ct_d1_fill_palette_band_pair_21a0_23a0_with_7fff_sentinel   [strong]
- Fills `7E:21A0..21FF` and `7E:23A0..23FF` with `0x7FFF`.
- Exact smaller sibling of `D1:E899`.

### D1:E91A..D1:E983  ct_d1_promote_first_48color_palette_band_and_restore_active_3record_descriptor_slab   [strong structural]
- Copies `7E:2040..209F` into `7E:20A0..20FF` and `7E:22A0..22FF`, then clears `7E:2040..209F` and `7E:2240..229F`.
- Copies `7E:0544..0567` back into `7E:0520..0543`.
- Adds `0x30` to the `+1` byte of each copied 12-byte record.
- Seeds `0520/052C/0538` and `CD2F..CD31` with `0x30`.
- Clears `CD32..CD34` and `CDC8`.
- Increments `CE12`.
- Strongest safe reading: promote/copy helper for one palette-band pair plus one active descriptor slab restore/arm step.

### D1:E984..D1:E9EB  ct_d1_seed_first_48color_palette_band_from_d0_fd00_and_snapshot_active_descriptor_slab_outward   [strong structural]
- Increments `CDC8` and `CE0F`.
- Copies ROM data from `D0:FD00..FD5F` into `7E:2040..209F` and `7E:2240..229F`.
- Copies `7E:0520..0543` outward into `7E:0544..0567`.
- Subtracts `0x30` from the `+1` byte of each copied 12-byte record.
- Seeds `0548/0554/0560` with `0x0100`.
- Seeds `0544/0550/055C` and `CD32..CD34` with `0x30`.
- Increments `CE12`.
- Strongest safe reading: complementary seed/snapshot helper paired with `D1:E91A`.

### D0:FD00..D0:FD5F  ct_d0_palette_band_seed_block_48colors_for_d1_e984   [strong]
- Exact fixed ROM table copied by `D1:E984` into `7E:2040..209F` and `7E:2240..229F`.
- Not compressed and not computed locally.

---

## Strengthened RAM/state labels

### 7E:0520..7E:0543  ct_palette_effect_descriptor_active_slab_3x12byte_records   [stronger support]
- Passes 8–9 already proved `0520 + n*0C` is a palette/effect descriptor family.
- Pass 82 adds exact slab-level proof: `D1:E91A` restores `0544..0567 -> 0520..0543`, and `D1:E984` snapshots `0520..0543 -> 0544..0567`.
- Strongest safe reading: active 3-record descriptor slab.

### 7E:0544..7E:0567  ct_palette_effect_descriptor_secondary_slab_3x12byte_records   [stronger support]
- Exact `0x24`-byte partner slab adjacent to `0520..0543`.
- `D1:E91A` copies this slab back into the active slab.
- `D1:E984` copies the active slab outward into this slab and biases fields afterward.

### 7E:2040..7E:209F  ct_d1_first_48color_palette_band_work_pair_a   [provisional strengthened]
- Seeded from `D0:FD00` by `D1:E984`.
- Later promoted/cleared by `D1:E91A`.
- Final gameplay-facing band noun still open.

### 7E:2240..7E:229F  ct_d1_first_48color_palette_band_work_pair_b   [provisional strengthened]
- Exact partner band written alongside `7E:2040..209F` by both `D1:E984` and `D1:E91A`.
- Final noun still open.

### 7E:20A0..7E:20FF  ct_d1_promoted_48color_palette_band_pair_a   [provisional strengthened]
- Filled only by `D1:E91A` from `7E:2040..209F`.
- Strongest safe reading: promoted/latched counterpart of the first work band.

### 7E:22A0..7E:22FF  ct_d1_promoted_48color_palette_band_pair_b   [provisional strengthened]
- Exact partner band written alongside `7E:20A0..20FF` by `D1:E91A`.

### 7E:2120..7E:217F and 7E:2320..7E:237F  ct_d1_secondary_palette_band_pairs_seeded_to_7fff   [provisional strengthened]
- Seeded to `0x7FFF` by `D1:E899`.
- Later consumed by the nearby `D1:E71D..E77A` swap path.
- Final higher-level noun remains open.

### 7E:21A0..7E:21FF and 7E:23A0..7E:23FF  ct_d1_tertiary_palette_band_pairs_seeded_to_7fff   [provisional strengthened]
- Seeded to `0x7FFF` by `D1:E8C1`.
- Also tied to the nearby `D1:E71D..E77A` swap/exchange seam.

### 7E:CD2F..7E:CD31  ct_d1_palette_band_control_triplet_a_seeded_by_e91a   [provisional strengthened]
- Seeded to `0x30` by `D1:E91A`.
- Exact final noun remains open.

### 7E:CD32..7E:CD34  ct_d1_palette_band_control_triplet_b_seeded_by_e984_or_cleared_by_e91a   [provisional strengthened]
- Cleared by `D1:E91A`.
- Seeded to `0x30` by `D1:E984`.
- Strongest safe reading: paired control/state triplet for the same subcluster.

### 7E:CDC8  ct_d1_palette_band_seed_snapshot_latch   [provisional strengthened]
- Incremented by `D1:E984`.
- Cleared by `D1:E91A`.
- Strongest safe reading: latch/flag tied to the seed-vs-promote half-cycle.

### 7E:CE0F  ct_d1_palette_band_seed_count_or_arm_latch   [provisional strengthened]
- Incremented by `D1:E984`.
- No matching clear is yet proven in this pass.
- Final noun remains open.

### 7E:CE12  ct_d1_palette_band_promote_snapshot_pending_counter   [provisional strengthened]
- Incremented by both `D1:E91A` and `D1:E984`.
- Also consumed nearby at `D1:F42B..F46C`.
- Strongest safe reading: shared pending-step / handshake counter for this subcluster.

---

## Honest caution
Even after this pass:

- I have **not** frozen the final human-facing noun of the `2040/20A0/2120/21A0/2240/22A0/2320/23A0` palette-band families.
- I have **not** finished the downstream `CE12 / CDC8 / CE0F` control logic.
- I have **not** closed the exact relationship to the later swap path at `D1:E71D..E77A`.
- I have **not** yet tied this subcluster all the way into the final higher-level battle/UI mode name.
