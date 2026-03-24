# Chrono Trigger Labels — Pass 83

## Purpose
This file records the label upgrades justified by pass 83.

Pass 82 closed the meanings of the `D1:E899 / E8C1 / E91A / E984` palette-band helpers.
Pass 83 closes a real chunk of the downstream consumer logic:

- `D1:F411` is now exact as an 8-slot descriptor-header shadow helper
- `D1:F431` and `D1:F457` are now exact as the suspend vs restore halves of a local one-shot gate
- `CD2F..CD36` is now pinned as the real 8-byte shadow array, correcting the too-narrow pass-82 focus on `CD2F..CD34`
- `CFFF` is now pinned locally as the suspend-vs-restore selector
- `D1:E70A..E77B` is now pinned as the exact 48-word exchange path for the `2120/21A0` and `2320/23A0` band pairs

I am still keeping the final gameplay-facing nouns of `CFFF`, `A101`, `2A21.bit1`, and the `0575.bit6` toggle one notch below frozen.

---

## Strengthened helper labels

### D1:F411..D1:F426  ct_d1_snapshot_palette_descriptor_header_bytes_8slots_to_cd2f_cd36   [strong]
- Walks the 8-slot `0520 + n*0C` descriptor queue.
- Copies the first byte of each slot (`0520/052C/0538/0544/0550/055C/0568/0574`) into `CD2F..CD36`.
- Exact structural role: descriptor-header shadow helper.

### D1:F427..D1:F430  ct_d1_select_descriptor_header_suspend_or_restore_by_cfff   [strong structural]
- Reads `CFFF`.
- `CFFF != 0` jumps to the shadow-and-suspend path at `D1:F431`.
- `CFFF == 0` jumps to the restore path at `D1:F457`.

### D1:F431..D1:F456  ct_d1_arm_ce12_shadow_descriptor_headers_and_suspend_family_10_slots   [strong structural]
- Returns immediately when `CE12 != 0`.
- Otherwise increments `CE12`, snapshots all 8 descriptor headers through `D1:F411`, and scans the full 8-slot queue.
- Clears only non-negative `0x1x` header bytes in `0520 + n*0C`.
- Strongest safe reading: one-shot shadow-and-suspend path for the positive palette-animation family.

### D1:F457..D1:F473  ct_d1_restore_shadowed_descriptor_headers_from_cd2f_cd36_and_clear_ce12   [strong structural]
- Returns immediately when `CE12 == 0`.
- Otherwise clears `CE12` and restores `CD2F..CD36` back into the first byte of all 8 descriptor slots.
- Strongest safe reading: one-shot restore half paired with `D1:F431`.

### D1:E70A..D1:E77B  ct_d1_optional_exchange_secondary_and_tertiary_palette_band_pairs   [strong structural]
- Clears `A101`.
- Tests `2A21.bit1`; when set, toggles bit `0x40` in `0575`.
- Exchanges the full 48-word pairs `2120..217F <-> 21A0..21FF` and `2320..237F <-> 23A0..23FF`.
- Decrements direct-page `$40` and returns.
- Strongest safe reading: selector-sensitive band-exchange helper.

---

## Strengthened RAM/state labels

### 7E:0520..7E:057F  ct_palette_effect_descriptor_queue_8x12byte_records   [strong structural]
- Passes 8–9 already proved the `0x0C` stride and 8-slot queue shape.
- Pass 83 adds exact header-walk proof through `D1:F411` / `D1:F457`, covering slot headers at `0520/052C/0538/0544/0550/055C/0568/0574`.
- Strongest safe reading: full 8-record palette/effect descriptor queue.

### 7E:0568..7E:057F  ct_palette_effect_descriptor_tail_slab_2x12byte_records   [stronger support]
- The tail two descriptor slots are now surfaced directly by `D1:F411` / `D1:F457` via header bytes at `0568` and `0574`.
- Pass 82 did not touch these tail slots directly; pass 83 proves they participate in the same header-shadow gate.

### 7E:CD2F..7E:CD36  ct_palette_effect_descriptor_header_shadow_bytes_8slots   [strong correction]
- Exact shadow array for the first byte of all 8 `0520 + n*0C` descriptor slots.
- Written by `D1:F411`, restored by `D1:F457`.
- Pass 82's narrower `CD2F..CD34` interpretation is now tightened into this larger 8-byte mirror.

### 7E:CD35..7E:CD36  ct_palette_effect_descriptor_header_shadow_tail_slots_6_7   [strong addition]
- Tail two bytes of the new 8-slot shadow array.
- Correspond to descriptor headers at `0568` and `0574`.

### 7E:CFFF  ct_d1_palette_descriptor_suspend_restore_selector   [provisional strengthened]
- `CFFF != 0` selects the shadow-and-suspend path at `D1:F431`.
- `CFFF == 0` selects the restore path at `D1:F457`.
- Mapped-ROM proof for nonzero writers is still incomplete, so the final gameplay-facing noun remains open.

### 7E:CE12  ct_d1_palette_band_promote_snapshot_pending_counter   [stronger local gate support]
- Earlier passes already proved that `E91A` and `E984` increment `CE12`.
- Pass 83 proves local one-shot gate behavior in `D1:F431 / D1:F457`: nonzero blocks re-arm, zero blocks restore, and restore clears it.
- Strongest safe reading: locally gate-like latch behavior inside this D1 consumer pair, even if the wider cluster noun still wants caution.

---

## Honest caution
Even after this pass:

- I have **not** frozen the final gameplay-facing noun of `CFFF`.
- I have **not** frozen the exact higher-level role of `A101`, `2A21.bit1`, or the `0575.bit6` toggle in `D1:E70A`.
- I have **not** claimed that `CE12` is globally nothing but a latch; the local gate behavior is exact, but the wider cluster may still be richer.
- I have **not** yet tied this whole D1 control cluster all the way to the final battle/UI presentation noun.
