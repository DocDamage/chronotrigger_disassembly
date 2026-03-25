# Chrono Trigger Labels — Pass 118

## Purpose

Pass 117 structurally closed the internal `C0:8820` settlement pipeline.

Pass 118 closes the first exact caller-side ownership seam in bank `C2` without bluffing the final gameplay-facing noun.

## Strong labels

### C2:8E2D..C2:8E81  ct_c2_iterative_current_slot_settlement_sweep_with_optional_axis_export_and_clamp   [strong structural]
- Seeds the six-word scratch export band at `0F63..0F6E` with `FFFF` sentinel fill using `STA $0F63` plus overlapping `MVN`.
- Runs setup helper `8ECC`.
- Seeds loop index `71` from `0DBE` and default loop count `00 = 1`.
- If `0DBD.bit3` is set, switches to `71 = 0` and `00 = 73`.
- Repeatedly runs exact current-slot settlement service `C0:8820`.
- If `0DBD.bit7` is set, runs `8E82`:
  - exports a settled word into `0F63 + 2*71`
  - clamps current-slot word `0003,Y` against `003F,Y`
- If `0DBD.bit6` is set, runs `8EAB`:
  - exports a settled word into `0F69 + 2*71`
  - clamps current-slot word `0007,Y` against `0009,Y`
- Strongest safe reading: exact iterative current-slot settlement sweep with optional per-axis export and clamp.

### C2:8F6C..C2:8FC8  ct_c2_selective_accepted_slot_list_builder_over_exported_settlement_bands   [strong structural]
- Clears:
  - `0F53`
  - `0F5D`
  - local `71`
  - local `00`
  - local `04`
- Calls exact precheck helpers:
  - `8FCB` over `0F63 + 2*71`
  - `8FEF` over `0F69 + 2*71`
- `8FCB`:
  - skips on negative sentinel
  - sets `92 = 2`
  - calls `F13F`
  - stores `8A` into `0F63 + 2*00`
  - sets `0F5D.bit0`
  - increments `04`
- `8FEF`:
  - skips on negative sentinel
  - sets `92 = 1`
  - calls `F13F`
  - stores `8A` into `0F69 + 2*00`
  - ORs `0F5D` with `0x0002`
  - increments `04`
- When `04 != 0`, reruns `C0:8820`, then appends current-slot word `180E,Y` into `0F57 + 2*n` and increments accepted-slot count `0F53`.
- Strongest safe reading: exact selective accepted-slot list builder over the exported settlement bands.

### C2:9137..C2:916D  ct_c2_template_block_commit_and_mirror_helper_after_current_slot_settlement   [strong structural]
- Runs preparatory helper `916E`.
- If `9ABA == A8`, shifts `9B21`.
- Writes `9A93 -> 0003,Y`.
- Copies exact `0x0B`-byte template block rooted at `9B1C` into:
  - current-slot record at `Y + 0x36`
  - mirror block `9AC6`
- Strongest safe reading: exact template-block commit/mirror helper after settlement.

### C2:A22F..C2:A26F  ct_c2_one_shot_settlement_driven_materialization_wrapper   [strong structural]
- Runs fixed front helper `F28D` with `X = 3390`, `Y = 0402`.
- Seeds `71 = 0412 + 0413`.
- Runs exact current-slot settlement service `C0:8820`.
- Immediately commits/mirrors the settled block through exact helper `9137`.
- Runs downstream materializer chain:
  - `31ED` with `X = BE1C`
  - `A6F0` with `X = 30A2`
  - `EC38` after seeding:
    - `01 = 0x0E`
    - `0D46 = 9A90`
    - `61 = 2EDE`
  - `A273`
- Finishes through common service call `8385` with `X = FBE3`.
- Strongest safe reading: exact one-shot settlement-driven materialization wrapper.

### C2:A273..C2:A2C5  ct_c2_selector_driven_staircase_and_block_materializer_used_by_one_shot_wrapper   [strong structural]
- Increments `0D15`.
- Uses 8-bit selector `9A90`.
- Uses byte table rooted at `C2:A2C6`.
- Uses selector-derived word tables rooted at:
  - `FF:CE88`
  - `FF:CE92`
- Materializes an incrementing twelve-word staircase into:
  - `2EEC`
  - `2EEE`
  - `2EF0`
  - `2EF2`
  - `2EF4`
  - `2EF6`
  - `2F2C`
  - `2F2E`
  - `2F30`
  - `2F32`
  - `2F34`
  - `2F36`
- Performs an additional exact selector-derived `0x20`-byte banked block move.
- Strongest safe reading: exact selector-driven staircase-and-block materializer used by the one-shot wrapper.

## Caution-strengthened outputs

### 7E:0F53  ct_c2_accepted_slot_count_built_by_selective_settlement_band_probe   [caution strengthened]
- Cleared at the front of `8F6C..8FC8`.
- Incremented only when `04 != 0` and current-slot word `180E,Y` is appended into `0F57..`.
- Strongest safe reading: accepted-slot count for the selective settlement-band probe caller.

### 7E:0F57..7E:0F5C  ct_c2_packed_accepted_slot_word_list_from_selective_settlement_band_probe   [caution strengthened]
- Appended through `LDX 00` / `LDA $180E,Y` / `STA $0F57,X` inside `8F6C..8FC8`.
- Advanced in 2-byte steps through local `00`.
- Strongest safe reading: packed accepted-slot word list built from the selective settlement-band probe.

### 7E:0F5D  ct_c2_per_axis_accepted_hit_mask_for_current_slot_selective_settlement_probe   [caution strengthened]
- Cleared at the front of `8F6C..8FC8`.
- `8FCB` sets bit 0.
- `8FEF` ORs in bit 1.
- Strongest safe reading: per-axis accepted-hit mask for the current slot during the selective settlement-band probe.

### 7E:0F63..7E:0F6E  ct_c2_six_word_settled_axis_export_scratch_band_for_c2_settlement_callers   [caution strengthened]
- Seed-filled with `FFFF` sentinel in `8E2D..8E81`.
- Written by exact masked export helpers `8E82` and `8EAB`.
- Later re-probed by exact selective caller `8F6C..8FC8`.
- Strongest safe reading: six-word settled-axis export scratch band shared by the bank-`C2` settlement callers.

## Honest remaining gap

- I still am **not** freezing the final gameplay-facing noun of the whole subsystem.
- The internal `C0` solver is solved structurally.
- These first `C2` caller contracts are now solved structurally.
- The real remaining gap is the higher-level sibling/outer-bank family name tying together:
  - `A1C3`
  - `A2D2`
  - `A31C`
  - `D4:CE8A`
  - `E5:C1AA`
  - and the final downstream consumers of `0F57..` and `2EEC..2F36`.
