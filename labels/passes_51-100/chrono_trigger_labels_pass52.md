# Chrono Trigger Disassembly Labels — Pass 52

This file contains labels newly added, replaced, or materially strengthened in pass 52.

As in prior passes:
- **strong** = directly supported by control flow and data role in the ROM work of this pass
- **strengthened** = previously useful label materially tightened by new proof
- **provisional** = structurally useful but still not safe as a final frozen name

---

## Strong labels

### C1:C90B  ct_c1_mul_u16_dp28_dp2a_to_dp2c_lowword                              [strong]
- Shift/add multiply helper.
- Consumes 16-bit inputs in `$28` and `$2A`.
- Writes the low word of the product to `$2C`.
- This is the real arithmetic core behind the `C1:FDBF` wrapper used in the readiness seed families.

### C1:FDBF  ct_c1_jsl_mul_u16_dp28_dp2a_to_dp2c_lowword                         [strong]
- Thin long-call wrapper:
  - `JSR $C90B`
  - `RTL`
- Useful because the seed families call it twice with different inputs.

### CC:2E31  ct_cc_battle_speed_page_speed_to_readiness_seed_adjust_table        [strong]
- 8 pages of 16 signed-byte entries each.
- Page selected by `($2990 & 7)`.
- Entry selected by `(speed - 1)`.
- Supplies the additive adjustment term in the exact readiness seed formula.

### FD:B820..FD:B850  ct_fd_seed_primary_visible_lane_readiness_from_config_and_speed [strong]
- Primary visible-lane seed family.
- Computes page = `($2990 & 7)`.
- Loads adjustment from `CC:2E31[page*16 + speed - 1]`.
- Computes final seed:
  - `0x69 - speed*6 + adjustment`
- Stores to:
  - `B158`
  - `AFAB`
- Sets `B03A = 1`.

---

## Strengthened labels

### 7E:2990 low 3 bits  ct_cfg_battle_speed_field                                [strengthened]
- This pass proves the low 3 bits are consumed directly as an 8-way page selector in the readiness seed branch.
- The whole byte is still a broader config byte, but the low field is no longer vague.
- Strongest safe reading: battle-speed option field.

### 7E:[participant_record + 0x38]  ct_battle_participant_effective_speed_byte    [strengthened]
- Previously only “speed-like stat”.
- This pass proves it is used twice in the seed formula:
  - once to select one of 16 entries within the battle-speed page
  - once as the multiplicand in `speed * 6`
- Strongest safe reading: effective/current speed byte for the battle participant record.

### 7E:B158  ct_c1_primary_lane_readiness_seed_value                              [strengthened]
- Still best kept as a seed value rather than a final gameplay-facing name.
- This pass proves the exact upstream formula feeding it.

### 7E:AFAB  ct_c1_primary_lane_readiness_work_value                              [strengthened]
- Receives the same formula result as `B158` in the primary seed family.
- Still the best working/readiness-shadow label.

### 7E:B03A  ct_c1_primary_visible_lane_readiness_seed_valid_flag                 [strengthened]
- This pass confirms it is asserted directly by the primary seed family after the exact formula store.

---

## Provisional labels

### FD:B8C0..FD:B8E0  ct_fd_seed_sibling_visible_lane_readiness_from_config_and_speed [provisional]
- Uses the same core formula as the primary family:
  - `0x69 - speed*6 + adjustment`
- Stores to:
  - `B15B`
  - `AFAE`
- Sets `B03D` only when `AF02[slot] != FF`.
- Also conditionally ORs `#$40` into `AF15[slot]` when record byte `+0x0A` has bit 0 set.
- Final freeze deferred until the higher-level semantic split between the primary/sibling pairs is tighter.

### 7E:B15B  ct_c1_sibling_lane_readiness_seed_value                              [provisional]
- Formula-aligned sibling of `B158`.
- Final freeze deferred until the exact caller/consumer split is clearer.

### 7E:AFAE  ct_c1_sibling_lane_readiness_work_value                              [provisional]
- Formula-aligned sibling of `AFAB`.
- Final freeze deferred pending more downstream consumer proof.

### 7E:B03D  ct_c1_sibling_visible_lane_readiness_seed_valid_flag                 [provisional]
- Sibling of `B03A`, but only set under an extra gate (`AF02 != FF`).
- Final freeze deferred pending tighter alignment with the lane-selection/state machinery.

### 7E:AF15 bit 6  ct_runtime_slot_sibling_seed_side_effect_flag                  [provisional]
- Set by the sibling seed family when record byte `+0x0A` has bit 0 set.
- Real side effect, but gameplay-facing meaning still unresolved.

---

## Replaced / retired wording

### “small random/bias term” in `FD:B820..FD:B850`                               [retired]
- No longer supported.
- Replaced by two exact proven roles for `$2C`:
  1. battle-speed page selector (`($2990 & 7) * 16`)
  2. `speed * 6`

### CC:2E31 old wording “speed-like stat -> readiness bonus table”               [soft-replaced]
- Too narrow after page-selection proof.
- Replaced by `ct_cc_battle_speed_page_speed_to_readiness_seed_adjust_table`.

### FD:B820..FD:B850 old wording “seed ... from speed-like stat”                 [soft-replaced]
- Too narrow after config-field/page proof.
- Replaced by `ct_fd_seed_primary_visible_lane_readiness_from_config_and_speed`.

---

## Exact formula now safe to carry forward

For the primary seed family:

```text
page  = ($2990 & 7)
speed = [participant_record + 0x38]
adj   = CC:2E31[(page * 16) + (speed - 1)]
seed  = 0x69 - (speed * 6) + adj
```

Equivalent pagewise linear forms:

```text
page 0: seed =  50 - 2*speed
page 1: seed =  75 - 3*speed
page 2: seed = 100 - 4*speed
page 3: seed = 125 - 5*speed
page 4: seed = 150 - 6*speed
page 5: seed = 175 - 7*speed
page 6: seed = 200 - 8*speed
page 7: seed = 225 - 9*speed
```

These forms are now strong enough to preserve in future passes.

---

## Still intentionally unresolved

### Exact higher-level semantic split between primary and sibling seed/export pairs [unresolved]
- `B158 / AFAB / B03A`
- `B15B / AFAE / B03D`

### Exact gameplay-facing name for the seed quantity                             [unresolved]
- “readiness seed” is now very safe structurally
- final freeze as countdown/delay/timer/etc. still wants one more downstream pass

### Exact meaning of sibling-only `AF15.bit6` side effect                        [unresolved]
- Real and worth keeping
- not yet safe to freeze
