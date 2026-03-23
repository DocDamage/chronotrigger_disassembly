# Chrono Trigger Labels — Pass 66

## Purpose
This file records the label upgrades justified by pass 66.

Pass 66 closes most of the remaining direct-record / early-control seam opened by pass 65:

- `13/14/15` are the continuation of the current-slot record gate band
- `16/19` are pure replay aliases
- `17/1B/22` are simple gate bodies
- `18/1C/1F` are stronger structurally, but still want caution on the final noun

---

## Strong labels

### C1:94D2..C1:9513  ct_global_opcode_13_gate_tail_replay_on_current_b19e_bit4_match_mode   [strong structural]
- Computes `X = B252 * 4`.
- Reads `B19E[X] & 0x10`.
- Operand `+1` bit `0` selects the target bit state (`0x00` vs `0x10`).
- Operand `+3` selects equality vs inequality.
- Success continues through `8C3E`; failure sets `AF24 = 1`.

### C1:959A..C1:95D5  ct_global_opcode_15_gate_tail_replay_on_current_b1a0_mask_match_mode   [strong structural]
- Computes `X = B252 * 4`.
- Reads `B1A0[X]`.
- Operand `+1` is a required mask.
- Operand `+3 == 0` -> require full-mask containment.
- Operand `+3 != 0` -> require non-match.

### C1:95D6..C1:95D9  ct_global_opcode_16_unconditional_tail_replay_step_alias   [strong]
- Exact alias of the unconditional `8C3E ; RTS` replay step.

### C1:95DA..C1:95F9  ct_global_opcode_17_gate_tail_replay_on_rng_percent_below_immediate   [strong structural]
- Calls the known RNG helper at `AF22` with `A = 0x64`.
- Succeeds only when the returned value is below operand `+1`.

### C1:9652..C1:9655  ct_global_opcode_19_unconditional_tail_replay_step_alias   [strong]
- Exact alias of the unconditional `8C3E ; RTS` replay step.

### C1:96A5..C1:96D3  ct_global_opcode_1B_gate_tail_replay_on_visible_head_live_count_at_or_below_immediate   [strong structural]
- Counts non-`FF` entries in `AEFF[0..2]`.
- Uses `operand+1 + 1` internally, so the effective success predicate is:
  - visible-head live count `<= operand+1`

### C1:9728..C1:975B  ct_global_opcode_1D_gate_tail_replay_on_selected_tail_live_presence_mode   [strong structural]
- Calls `AC14`.
- Uses `AECC[0]` as the selected entry index.
- Reads `AF02[selected]`.
- Operand `+2` selects presence vs absence polarity.

### C1:975C..C1:9764  ct_global_opcode_1E_unconditional_tail_replay_then_abort   [strong structural]
- Always runs `8C3E`.
- Then always writes `AF24 = 1`.

### C1:97D5..C1:980F  ct_global_opcode_22_gate_tail_replay_on_selected_b158_threshold_mode   [strong structural]
- Calls `AC14`.
- Uses `AECC[0]` as the selected entry index.
- Reads `B158[selected]`.
- Operand `+1` is the threshold.
- Operand `+2 == 0` -> success on `< threshold`
- Operand `+2 != 0` -> success on `>= threshold`

---

## Provisional / strengthened labels

### C1:9514..C1:9599  ct_global_opcode_14_gate_tail_replay_on_current_b19e_bit4_clear_selector_mode   [provisional structural]
- Two-form handler.
- In the primary form (`operand+2 == 0`):
  - requires current `B19E[X]` bit 4 clear
  - uses `B19E[X] & 0x0F` to index `AF0A[...]`
  - compares that byte against operand `+1`
  - operand `+3` selects equality vs inequality
- In the alternate form (`operand+2 != 0`):
  - still requires current `B19E[X]` bit 4 clear
  - then effectively collapses to:
    - operand `+3 == 0` -> fail
    - operand `+3 != 0` -> success
- The apparent `01/02/05` compare chain in the alternate branch should not be overclaimed as real content logic.

### C1:95FA..C1:9651  ct_global_opcode_18_reduce_selected_entries_by_indirect_table_byte_equals_immediate   [provisional structural]
- Calls `AC14`.
- Scans selected entries in `AECC`.
- Resolves an `FD:A80B` record-rooted value and uses it as the `Y` component of `LDA ($0A),Y`.
- On equality with operand `+1`, reduces through `AE21`, then `AEFD`, then `8C3E`.
- Keep provisional because the base-pointer setup through `$0A/$0B` still wants harder confirmation.
- Important context: master opcodes `23..28` all alias back to this same body.

### C1:9656..C1:96A4  ct_global_opcode_1A_gate_tail_replay_on_live_tail_occupant_search_mode   [strengthened structural]
- Scans the live-tail occupant submap `AF02[0..AEC6-1]` for operand `+1`.
- Dead leading `LDA $B252` should be ignored; the real scan starts from `X = 0`.
- Operand `+2` enables a mode that skips current-slot hits and requires another matching live-tail entry.
- Operand `+3` controls the final success gate once a usable match is found.

### C1:96D4..C1:9727  ct_global_opcode_1C_optionally_replay_on_selected_head_canonical_membership_then_abort   [provisional structural]
- Calls `AC14`.
- Searches `AF0A[0..2]` for a byte equal to `AECC[0]`.
- Uses operand `+2` plus optional `AEFF[x] != FF` live-head confirmation to decide whether to call `8C3E`.
- Always exits with `AF24 = 1`, even after replay.

### C1:9765..C1:97AA  ct_global_opcode_1F_gate_tail_replay_on_relation_mode0E_current_subject_vs_selection_head   [strengthened structural]
- Calls `AC14`.
- Seeds relation-query mode `0E` with:
  - `986F = B252 + 3`
  - `9870 = AECC[0]`
- Operand `+1` selects the final zero/nonzero gate on `9872`.
- Success forces `AECB = 1` and continues through `8C3E`.
- Keep the wrapper label strong-structural, but do not pretend mode `0E`'s underlying noun is already frozen.

---

## Supporting interpretation upgrades

### C1:2CF3..C1:2D80  relation-query mode `0E` body   [strengthened context]
- This mode is no longer best imagined as a trivial boolean compare.
- The body pulls projected position pairs from `1D0C/1D23`, computes two subject-relative squared-distance-like values, differences them, normalizes the result through `0116`, and returns a value through `9873`.
- That is why opcode `1F` should stay “mode-0E wrapper” rather than a fake-final gameplay noun.

---

## Important corrections to carry forward

### Opcode `14`
Do not keep over-claiming a rich subtype decoder in the `operand+2 != 0` branch.
That branch collapses far more bluntly than it first appears.

### Opcode `1A`
Do not keep describing the scan as starting from `B252`.
The `LDA $B252` is dead before `TDC/TAX`.

### Opcode `1C`
Do not describe it as a normal replay gate.
It always writes `AF24 = 1` after the optional replay call.

### Opcode `1F`
Do not finalize mode `0E` from wrapper shape alone.
The wrapper is clear; the underlying mode noun is still open.

---

## Suggested next seam
- Alias cluster `23..28`
- then `29..2F`
- plus a direct decode pass over relation-query mode `0E` at `2CF3`
