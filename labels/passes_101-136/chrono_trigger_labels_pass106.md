# Chrono Trigger Labels — Pass 106

## Purpose
This file records the label upgrades justified by pass 106.

Pass 105 froze the installed D1 RAM NMI trampoline body and proved that `C0:0005 -> C0:0AFF` returns the byte later written to `$420C`.

Pass 106 closes that seam and proves that the returned byte is the current contents of `7E:0128`, which is now exact enough to call the low-bank / FD-side HDMA enable shadow byte.

---

## Strong labels

### C0:0AFF..C0:0B27  ct_c0_set_dp0100_and_db00_raise_0153_bit7_run_double_fd_c2c1_then_fd_c1ee_and_return_0128_hdma_enable_shadow   [strong structural]
- Exact body is now frozen:
  - `PHP ; PHB`
  - `REP #$20 ; LDA #$0100 ; TCD`
  - `SEP #$30 ; LDA #$00 ; PHA ; PLB`
  - `LDA #$80 ; TSB $53`
  - `JSL FD:C2C1`
  - `JSL FD:C2C1`
  - `LDA #$80 ; TRB $53`
  - `REP #$10 ; JSL FD:C1EE`
  - `LDA $28 ; PLB ; PLD ; RTL`
- `TCD` makes `$28` mean `7E:0128` here, not `$0028`.
- Pass 105 already proved the consumer edge:
  - `D1:F4E2  JSL C0:0005`
  - `D1:F4E6  STA $420C`
- Strongest safe reading: exact low-bank helper that runs the doubled `FD:C2C1` subpass plus `FD:C1EE`, then returns the current `7E:0128` HDMA enable shadow byte in `A`.

### 7E:0128  ct_c0_fd_hdma_enable_shadow_byte_returned_by_0aff_and_committed_to_420c   [strong structural]
- Clean producer-side mirror proof:
  - `C0:AE2B  STA $420C`
  - `C0:AE33  STA $0128`
- Clean hardware commit proof:
  - `C0:EC48  LDA $0128`
  - `C0:EC4B  STA $420C`
- Clean trampoline-side return/consume proof:
  - `C0:0B23  LDA $28` with `D = $0100`
  - `D1:F4E6  STA $420C`
- Strongest safe reading: exact low-bank / FD-side HDMA enable shadow byte.

### FD:C2C1..FD:C2DF  ct_fd_dispatch_one_of_two_local_three_entry_builder_jump_tables_by_0153_bit0_and_0126_then_flip_bit0   [strong structural]
- Exact body is now frozen:
  - reads `$53`
  - branches on `bit0`
  - reads `$26`, doubles it, moves it to `X`
  - dispatches through one of two exact local jump tables via `JSR (abs,X)`
  - on the clear-bit side: sets `53.bit0`
  - on the set-bit side: clears `53.bit0`
  - returns with `RTL`
- Exact local jump tables:
  - `FD:C2DF` -> `C2EB / C995 / CFCF`
  - `FD:C2E5` -> `C847 / CD0C / D27E`
- Strongest safe reading: exact two-table local builder dispatcher selected by `0153.bit0` and indexed by `0126`, with `bit0` flipped on return.

### C0:0B2B..C0:0B50  ct_c0_call_fd_c124_then_refresh_fd_c2c1_fd_c1ee_wait_4210_set_enable_nmi_vtime_00d3_and_cli   [strong structural]
- Exact body is now frozen:
  - `JSL FD:C124`
  - `SEP #$10 ; JSL FD:C2C1 ; REP #$10 ; JSL FD:C1EE`
  - poll `LDA $4210 ; BPL loop`
  - `LDA #$81 ; STA $4200`
  - `REP #$20 ; LDA #$00D3 ; STA $4209 ; SEP #$20`
  - `CLI ; RTS`
- Strongest safe reading: startup/helper sibling that runs the same FD-side refresh family, waits for the NMI flag, then enables NMI and seeds `VTIME = 0x00D3`.

---

## Caution label

### 7E:0153  ct_fd_local_builder_phase_flag_byte_with_exact_bit7_gate_in_0aff_and_exact_bit0_table_flip_in_c2c1   [caution]
- Exact local `bit7` contract in `C0:0AFF`:
  - `LDA #$80 ; TSB $53`
  - doubled `JSL FD:C2C1`
  - `LDA #$80 ; TRB $53`
- Exact local `bit0` contract in `FD:C2C1..C2DF`:
  - chooses between the two local jump tables
  - then flips `bit0` on return
- Strongest safe reading: local builder-phase/control byte for this family.
- Broader subsystem noun remains intentionally cautious.

---

## What this pass settles
- The byte returned by `C0:0005 -> C0:0AFF` is now exact: it is the current contents of `7E:0128`.
- `7E:0128` is no longer anonymous work RAM; it is the low-bank / FD-side HDMA enable shadow byte.
- The installed D1 RAM NMI trampoline now has an exact HDMA-mask producer edge behind its `$420C` write.
- `FD:C2C1..C2DF` is no longer fuzzy helper soup; it is an exact two-table local dispatcher.

---

## Honest caution
- I have **not** yet frozen the full exact role of `FD:C1EE..C2C0`; only its position in the shadow/materialization path is now exact.
- I have **not** frozen the final broader subsystem noun of `0153` or `0126`; only the exact local contracts used by this helper family.
