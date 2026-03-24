# Chrono Trigger Labels — Pass 107

## Purpose
This file records the label upgrades justified by pass 107.

Pass 106 closed the `C0:0AFF` return-value seam and proved that the installed NMI trampoline ultimately commits the current `7E:0128` HDMA enable shadow byte to `$420C`.

Pass 107 closes the exact body at `FD:C1EE..C2C0` and proves that this routine is the local **HDMA channel-register programming/finalization** step, not the direct producer of `7E:0128`.

---

## Strong labels

### FD:C1EE..FD:C2C0  ct_fd_program_all_eight_indirect_hdma_channel_register_blocks_from_one_of_two_7f_table_bundles_with_channel7_target_selected_by_013c_bit0   [strong structural]
- Exact body is now frozen:
  - `PHD`
  - `REP #$20 ; LDA #$4300 ; TCD`
  - `SEP #$20`
  - writes exact channel-control bytes to `$4300/$4310/.../$4370`:
    - `44,43,43,43,44,41,41,40`
  - writes exact B-bus target bytes to `$4301/$4311/.../$4371`:
    - `07,0D,0F,11,2C,26,31,(28 or 29)`
  - writes `7F` into every exact source-bank and indirect-bank byte:
    - `$4304/$4314/.../$4374`
    - `$4307/$4317/.../$4377`
  - reads `0153 & 0x0F`
  - installs one of two exact 8-entry source-address bundles into `$4302/$4303 ... $4372/$4373`
  - exits with `PLD ; RTL`
- Strongest safe reading: exact eight-channel indirect-HDMA installer/finalizer that programs the channel register blocks from one of two paired WRAM table bundles in `7F`.
- This pass also proves what it is **not**: no clean direct `7E:0128` read/write occurs inside this body, so it is not the direct HDMA-enable-shadow producer.

### 7F:0F80..7F:1237  ct_fd_first_paired_eight_channel_7f_indirect_hdma_table_bundle_selected_when_0153_low_nibble_is_zero   [strong structural]
- Exact source starts written by `FD:C1EE` when `($0153 & 0x0F) == 0`:
  - `0F80`
  - `0FD7`
  - `102E`
  - `1085`
  - `10DC`
  - `1133`
  - `118A`
  - `11E1`
- Exact spacing is `0x57` between successive starts.
- Strongest safe reading: first exact 8-table WRAM bundle installed by the FD-side HDMA finalizer when the local low-nibble selector is zero.

### 7F:1238..7F:14EF  ct_fd_second_paired_eight_channel_7f_indirect_hdma_table_bundle_selected_when_0153_low_nibble_is_nonzero   [strong structural]
- Exact source starts written by `FD:C1EE` when `($0153 & 0x0F) != 0`:
  - `1238`
  - `128F`
  - `12E6`
  - `133D`
  - `1394`
  - `13EB`
  - `1442`
  - `1499`
- Exact spacing is `0x57` between successive starts.
- Strongest safe reading: second exact 8-table WRAM bundle installed by the FD-side HDMA finalizer when the local low-nibble selector is nonzero.

---

## Caution labels

### 7E:013C  ct_fd_local_channel7_hdma_bbus_target_selector_byte_with_exact_bit0_choosing_28_vs_29   [caution]
- Exact local reader in `FD:C1EE`:
  - `LDA $013C`
  - `BIT #$01`
  - clear -> `LDA #$28`
  - set   -> `LDA #$29`
  - stored to `$71` with direct page at `$4300`
- Strongest safe reading: exact local selector byte whose `bit0` chooses channel 7's installed B-bus target byte `0x28` vs `0x29` in this HDMA finalizer body.
- Broader subsystem noun remains intentionally cautious.

### 7E:0126  ct_fd_local_three_way_builder_family_index_byte_used_as_0126_times2_to_select_one_of_three_paired_fd_c2c1_targets   [caution]
- `FD:C2C1..C2DF` already proved the exact local dispatch mechanics:
  - `LDA $26`
  - `ASL`
  - `TAX`
  - `JSR (abs,X)` through one of two exact 3-entry tables
- The paired targets are exact:
  - clear-side table: `C847 / CD0C / D27E`
  - set-side table:   `C2EB / C995 / CFCF`
- Strongest safe reading: exact local 3-way builder-family index byte for this paired HDMA-builder family.
- Final broader noun still remains cautious.

### 7E:0153  ct_fd_local_hdma_builder_phase_and_bundle_selector_byte_with_exact_bit7_gate_bit0_table_flip_and_low_nibble_zero_nonzero_bundle_select   [caution]
- Exact previously frozen local contracts remain true:
  - `C0:0AFF` uses `bit7` as the doubled-builder gate around `FD:C2C1`
  - `FD:C2C1` uses `bit0` to choose one of the two local 3-entry jump tables and flips that bit on return
- Pass 107 adds one more exact local contract:
  - `FD:C1EE` reads `LDA $0153 ; AND #$0F`
  - zero -> installs the `7F:0F80..1237` bundle
  - nonzero -> installs the `7F:1238..14EF` bundle
- Strongest safe reading: local phase/control/bundle-selector byte for this FD-side HDMA builder/finalizer family.
- Final broader subsystem noun still remains intentionally cautious.

---

## What this pass settles
- `FD:C1EE..C2C0` is no longer vague “HDMA-side materialization.”
- It is the exact eight-channel indirect-HDMA installer/finalizer body for this family.
- The two exact paired WRAM HDMA table bundles it can install are now frozen.
- `7E:013C.bit0` now has a real exact local contract inside this body.
- The live seam has moved upstream again: the remaining producer question is now in the paired builder families behind `FD:C2C1`, not in `FD:C1EE` itself.

---

## Honest caution
- I have **not** yet frozen which of the six paired builder targets is the direct owner of the final `7E:0128` value.
- I have **not** yet proven whether the two paired `7F` bundles are true double-buffer siblings, true mode siblings, or a hybrid state/buffer arrangement.
- I have **not** yet frozen a broader gameplay/UI noun for `013C`, `0126`, or `0153`; only the exact local contracts used by this HDMA family are now pinned.
