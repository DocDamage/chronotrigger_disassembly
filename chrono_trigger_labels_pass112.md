# Chrono Trigger Labels — Pass 112

## Purpose
Pass 111 froze the *consumer* side of `7E:0163` in `C0:F05E`, but not the writer chain.

Pass 112 closes the core local writer mechanics without bluffing a broader subsystem noun.

## Strong labels

### C0:1AFB..C0:1B18  ct_c0_save_current_local_63_selector_into_66_then_force_default_restore_state_4   [strong structural]
- Exact body:
  - loads `7E:0163`
  - if negative, skips the save/force block
  - if `63 == 4`, skips the save/force block
  - otherwise:
    - stores old `63 -> 66`
    - forces `63 = 4`
  - then checks `00F6.bit7`
  - if set, clears local word `34`
- Strongest safe reading: exact helper that saves the current live selector and forces local selector `63` into exact default-restore state `4`.

### C0:1B1A..C0:1B2A  ct_c0_increment_local_63_selector_with_inclusive_wrap_to_64_after_65   [strong]
- Exact body increments `63`, compares against `65`, and:
  - stores incremented value when `<= 65`
  - otherwise loads `64` and stores that instead
- Strongest safe reading: exact increment-with-wrap helper for selector `63` over inclusive range `64..65`.

### C0:1B2B..C0:1B37  ct_c0_decrement_local_63_selector_with_inclusive_wrap_to_65_before_64   [strong]
- Exact body decrements `63`, compares against `64`, and:
  - stores decremented value when still `>= 64`
  - otherwise loads `65` and stores that instead
  - if `63 == 0`, immediately wraps to `65`
- Strongest safe reading: exact decrement-with-wrap helper for selector `63` over inclusive range `64..65`.

## WRAM label upgrades

### 7E:0163  ct_c0_local_four_band_vram_prelude_selector_and_default_restore_state_byte   [caution strengthened]
- Pass 111 already froze:
  - negative -> caller `ED15` skips `F05E`
  - `0..3` -> selected special-band overwrite cases
  - other nonnegative -> default-restore path
- Pass 112 adds exact writer mechanics:
  - startup/local reset path at `C0:0BC0` forces `63 = 0x80`
  - `C0:F05E` default-restore tail forces `63 = 0x80`
  - `C0:1AFB..1B18` forces `63 = 4` while saving prior nondefault value into `66`
  - `C0:1B1A..1B2A` and `C0:1B2B..1B37` materialize live selector values by increment/decrement wrap over inclusive range `64..65`
- Strongest safe reading: the local selector byte is now exact enough on the writer side to say its live `0..3` values are produced by wrap helpers, not by a newly frozen direct immediate-writer path.

### 7E:0164  ct_c0_local_inclusive_lower_wrap_bound_for_63_selector   [caution]
- Proven directly by `C0:1B1A..1B2A` and `C0:1B2B..1B37`:
  - increment overflow wraps back to `64`
  - decrement compares against `64` as the lower bound
- Strongest safe reading: local inclusive lower bound for selector `63`.

### 7E:0165  ct_c0_local_inclusive_upper_wrap_bound_for_63_selector   [caution]
- Proven directly by `C0:1B1A..1B2A` and `C0:1B2B..1B37`:
  - increment compares against `65` as the upper bound
  - decrement underflow wraps back to `65`
- Strongest safe reading: local inclusive upper bound for selector `63`.

### 7E:0166  ct_c0_local_saved_predefault_63_selector_byte   [caution]
- Proven directly by `C0:1AFB..1B18`:
  - old `63 -> 66` occurs only when `63` is nonnegative and not already `4`
  - the same helper then forces `63 = 4`
- Strongest safe reading: saved prior selector value captured immediately before the helper forces default state `4`.

## Carry-forward / caution notes

- The nearby bound-seeding evidence block at `C0:367C..3697` strongly suggests:
  - packed source byte -> low 2 bits into `65`
  - same byte -> high 2 bits into `64`
  - then `62 = 1`
- But the surrounding entry/caller chain still wants a cleaner freeze before promoting a broader subsystem noun for the `62/63/64/65/66` family.
- I am intentionally **not** promoting `7E:0162` beyond a vague local state byte yet.
