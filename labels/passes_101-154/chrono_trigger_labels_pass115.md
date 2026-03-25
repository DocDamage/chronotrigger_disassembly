# Chrono Trigger Labels — Pass 115

## Purpose

Pass 114 finished the exact earlier VM sibling family, but the shared `2E1E` fallback and the first real downstream roles of locals `30` and `2C` were still open.

Pass 115 closes those edges without overclaiming a larger subsystem noun.

## Strong labels

### C0:2E1E..C0:2E65  ct_c0_forced_blank_error_color_hang_shared_invalid_fallback_for_local_2d_zero   [strong structural]
- Exact target reached by the `BRL C0:2E1E` fallback in the `0xBB / 0xC1 / 0xC2 / 0xC0 / 0xC3 / 0xC4` family when local `2D == 0`.
- Forces blank through `$2100 = 0x80`.
- Zeros:
  - `$4200`
  - `$420B`
  - `$420C`
  - exact mirror byte `0128`
  - `$212C`
  - `$212D`
  - `$2121`
- Writes the 16-bit `X` value into CGRAM data port `$2122/$2122`.
- Seeds:
  - `0504 = 0x40`
  - `0500 = 0x40`
  - `0119 = 0x0F`
- Re-enables NMI through `$4200 = 0x81`, restores `$2100 = 0x0F`, then spins forever through `CLI ; BRA $FE`.
- The calling family loads `X = 0x7FE0` before entering this body.
- Strongest safe reading: exact forced-blank fixed-color hard-stop path used as the shared invalid fallback for the local-`2D` gate.

### C0:88E5..C0:88EC  ct_c0_copy_local_2a_2b_into_later_working_pair_2e_30   [strong]
- Byte-exact body:
  - `2A -> 2E`
  - `2B -> 30`
  - `RTS`
- First exact downstream transfer of the pass-114 seed bytes into a later working lane.
- Strongest safe reading: exact local handoff from earlier seed bytes into a later two-byte working pair.

### C0:88ED..C0:8A69  ct_c0_low_nibble_template_dispatch_write_signed_step_bytes_2c_2d_and_shift_working_pair_2e_30   [strong structural]
- Tests exact local/control byte `0138`; when nonzero, returns through the short `REP #$10 ; RTS` tail.
- Otherwise reads exact selector nibble `00F9 & 0x0F`, doubles it, and dispatches through the inline helper table beside `8900`.
- Unique helper bodies reached from that table:
  - `8924` (no-op return)
  - `8925..8943`
  - `8944..8962`
  - `8963..8981`
  - `8982..89A0`
  - `89A1..89D1`
  - `89D2..8A06`
  - `8A07..8A3B`
  - `8A3C..8A69`
- Shared exact behavior across the active helpers:
  - tests `00F8.bit1`
  - chooses coarse signed step `±0x20` when set
  - chooses fine signed step `±0x10` when clear
  - writes those exact step bytes into local `2C` and/or `2D`
  - adds or subtracts the same step from working pair `2E` and/or `30`
- Strongest safe reading: exact signed-step template-dispatch lane for the later `2E/30` working pair.

### C0:8A6C..C0:8A9D  ct_c0_sign_zero_dispatch_on_working_pair_2e_30_into_eight_downstream_branch_bodies   [strong structural]
- First exact downstream reader of local `30`.
- Reads local `30`, branches first on `zero / negative / positive`.
- Then reads local `2E` and branches again on `zero / negative / positive`.
- Selects one of these exact branch bodies:
  - `8AB5`
  - `8BC4`
  - `8BF9`
  - `8D11`
  - `8E21`
  - `8EF1`
  - `8FC1`
  - `909C`
- Strongest safe reading: exact sign/zero router over the later working pair.

## Caution-strengthened local roles

### 7E:0130  ct_c0_local_second_working_byte_in_later_2e_30_pair_and_first_exact_sign_dispatch_input   [caution strengthened]
- Pass 115 proves `88E5..88EC` copies exact local `2B -> 30`.
- Pass 115 proves `8A6C..8A9D` is the first exact downstream reader of `30`.
- Strongest safe reading: later working-byte copy sourced from the earlier family, and first exact sign/zero dispatch input in that later chain.
- Honest limit: this is still **not** the final human-facing noun of `30`.

### 7E:012C  ct_c0_local_signed_step_byte_written_by_later_template_helpers_after_seed_lane   [caution strengthened]
- Pass 114 already proved `3557` seeds exact second triplet byte into local `2C`.
- Pass 115 proves the later helper lane at `88ED..8A69` explicitly overwrites local `2C` with exact signed step values `0x10 / 0x20 / 0xF0 / 0xE0` depending on template and `00F8.bit1`.
- Strongest safe reading: local byte later reused as a signed step/output byte in the downstream working-vector/template lane.
- Honest limit: this does **not** replace the earlier pass-114 seed role; it proves a later exact overwrite role in a downstream lane.

### 7E:012E  ct_c0_local_first_working_byte_in_later_2e_30_pair_shifted_by_template_helpers   [caution]
- `88E5..88EC` copies exact local `2A -> 2E`.
- The helper family at `88ED..8A69` then adds or subtracts exact coarse/fine step values from `2E`.
- `8A6C..8A9D` reads `2E` as the second-stage sign/zero discriminator after `30`.
- Strongest safe reading: first byte of the later working pair in the template-dispatch chain.
- Honest limit: final human-facing noun still open.

## Honest remaining gap

- I am intentionally **not** freezing the final subsystem noun of the `2E/30` working pair.
- I am intentionally **not** freezing the final global noun of `2C/2D`.
- I am intentionally leaving the eight downstream branch bodies (`8AB5 / 8BC4 / 8BF9 / 8D11 / 8E21 / 8EF1 / 8FC1 / 909C`) as the next live seam.
