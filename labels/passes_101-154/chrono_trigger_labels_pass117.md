# Chrono Trigger Labels — Pass 117

## Purpose

Pass 116 closed the mirrored candidate-search family, but not the enclosing owner.

Pass 117 closes the owner band structurally without bluffing the final gameplay-facing noun.

## Strong labels

### C0:8820..C0:8857  ct_c0_dp1d00_enclosing_current_slot_candidate_offset_settlement_pipeline   [strong structural]
- Exact DP-scoped entry:
  - writes `01EB`
  - `PHD`
  - sets `D = $1D00`
  - runs exact seed copy `88E5` (`2A -> 2E`, `2B -> 30`)
  - clears `2C/2D`
  - conditionally runs exact step-template writer `88EE` when `0162 != 0` or `011F != 0`
  - conditionally runs already-closed sign/zero dispatcher `8A6D` when `0120 != 0`
  - then runs exact downstream sequence:
    - `9175`
    - `99DE`
    - `91AC`
    - `93E1`
  - restores `D`
  - returns
- Strongest safe reading: exact enclosing current-slot candidate-offset settlement pipeline.

### C0:9175..C0:91AB  ct_c0_initial_axis_bound_acceptance_gate_for_signed_candidate_components_2e_30_into_32_33   [strong structural]
- Clears local `32` and `33`.
- Uses current slot index `0197`.
- Tests sign of `2E`:
  - negative path calls `5B86`
  - nonnegative path calls `5B79`
- Copies `2E -> 32` only when the chosen helper accepts.
- Tests sign of `30`:
  - negative path calls `5B71`
  - nonnegative path calls `5B63`
- Copies `30 -> 33` only when the chosen helper accepts.
- Strongest safe reading: exact initial axis-bound acceptance gate for signed candidate components.

### C0:99DE..C0:9A1E  ct_c0_signed_candidate_component_nibble_quantizer_and_out_of_range_zeroer_for_2e_30   [strong structural]
- Processes `2E` first:
  - sign split
  - magnitude convert
  - divide by `0x10`
  - positive helper `9A60`
  - negative helper `9A7E`
  - clears `2E` when rejected
- Processes `30` second with sibling helpers:
  - positive helper `9A1F`
  - negative helper `9A3D`
  - clears `30` when rejected
- Strongest safe reading: exact nibble-quantizer and out-of-range zeroer for the signed candidate pair.

### C0:91AC..C0:93E0  ct_c0_six_lane_signed_accumulator_builder_and_high_low_nibble_splitter_with_optional_0400_bias_and_lane_decay   [strong structural]
- Optional front gate:
  - compares local `02/03` against `0A/0E`
  - seeds `2E/30` to `+0x10` or `-0x10` when unequal
  - uses `87.low_nibble` and `89.low_nibble` to set local `01.bit0/bit1` when equal
  - when `01 == 3`, forces `00 = 2` and clears `01`
- Optional `0400`-flag bias pair:
  - when `01BC != 0`, reads `0400.bit0/bit1`
  - materializes axis bias pair `4E/4F`
  - zero-suppresses the bias when `0A == 0` or `0E == 0`
- Builds exact signed lane accumulator pairs:
  - `3B/3C`
  - `3D/3E`
  - `3F/40`
- Splits each signed accumulator into:
  - high-nibble magnitude buckets `41..4C`
  - low-nibble signed residues remaining in `3B..40`
- Exact tail:
  - decrements `4D`
  - when expired, clears lane bytes `24..29`
- Strongest safe reading: exact six-lane signed accumulator builder and coarse/fine nibble splitter.

### C0:93E1..C0:991F  ct_c0_six_lane_phase_coarse_cell_propagation_and_wrap_flag_fanout_stage   [strong structural]
- Clears exact wrap/crossing flags:
  - `76`
  - `77`
  - `74`
  - `75`
- Runs six repeated lane-updater families over phase-like locals:
  - `93`
  - `96`
  - `94`
  - `97`
  - `95`
  - `98`
- Updates coarse-cell / coarse-index locals such as:
  - `0A/0C`
  - `0E/10`
  - `12/14`
  - `16/18`
  - plus paired locals `87/89/8B/8D/8F/91`
- Exact split is by sign of `0BC9` and bits in local `35`.
- Detects crossings at exact thresholds including:
  - `07/08`
  - `0F/10`
  - `1F/20`
- Sets crossing flags in `74..77`.
- Clears `78..7B`.
- Fans the crossing results into downstream helper families that update locals `99..9E`.
- Strongest safe reading: exact six-lane phase/coarse-cell propagation and wrap-flag fanout stage.

## Caution-strengthened locals

### 7E:0132  ct_c0_local_accepted_in_range_1800_side_candidate_component_after_axis_bound_gate   [caution strengthened]
- Written only when `9175..91AB` accepts the signed `2E` component through the sign-specific current-slot bound helpers.
- Strongest safe reading: accepted in-range candidate component on the same axis side earlier tied to slot word `1800`.

### 7E:0133  ct_c0_local_accepted_in_range_1880_side_candidate_component_after_axis_bound_gate   [caution strengthened]
- Written only when `9175..91AB` accepts the signed `30` component through the sign-specific current-slot bound helpers.
- Strongest safe reading: accepted in-range candidate component on the same axis side earlier tied to slot word `1880`.

## Honest remaining gap

- I am intentionally **not** freezing the final gameplay noun of this whole solver band yet.
- The real remaining gap now lives in caller context, especially the broad caller family in bank `C2` and other banks that feed `2A/2B`, `011F`, `0120`, `0162`, `01BC`, `35`, and `36`.
