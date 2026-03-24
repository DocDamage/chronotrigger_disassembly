# Chrono Trigger Labels — Pass 110

## Purpose
Pass 110 closes the pass-109 `ED15` vs `FD:FFFD -> E022` split.
The strongest safe result is that this split is not about a hidden `0128` owner.
It is an exact split between:
- a low-bank **CPU-side immediate VRAM patch dispatcher**
- an FD-side **channel-7 VRAM DMA descriptor streamer**

---

## Strong labels

### FD:FFFD  ct_fd_bank_local_jump_veneer_to_e022_vram_dma_streamer   [strong structural]
- Exact body: `JMP $E022`
- Strongest safe reading: tiny bank-local veneer used by the IRQ-side wrapper to enter the real FD-side VRAM DMA routine.

### C0:ED15..C0:F058  ct_c0_cpu_side_immediate_vram_patch_dispatcher_by_5f_bits_with_optional_f05e_prelude   [strong structural]
- Exact entry shape:
  - sets `D = 0x0100`
  - if `63` is not negative, runs `JSR F05E`
  - reads `5F`
  - dispatches by exact bits `0x10` and `0x02`
- Exact leaf families now frozen:
  - `ED31..EDA3` = 8-word immediate VRAM patch from `7E:BF28/2A/2C/2E/38/3A/3C/3E` into `09CA..09D8`, then clear `5F.bit4`
  - `EE88..EFD0` = 24-word immediate VRAM patch from the exact `7E:BFA8..BFAE`, `BFB8..BFBE`, `BFC8..BFCE`, `BFD8..BFDE`, `BFE8..BFEE`, `BF98..BF9E` families into `09CA..09F8`, then clear `5F.bit4`
  - `EFD7..F019` = 4-word immediate VRAM patch from `7E:BFF8..BFFE` into `09B2..09B8`, then clear `5F.bit1`
  - `F01A..F058` = 4-word immediate VRAM patch from `7E:BF08..BF0E` into `09B2..09B8`, then clear `5F.bit1`
- Strongest safe reading: exact low-bank direct-VRAM patch dispatcher with two pending-flag families and four exact leaf transfer grammars.

### FD:E022..FD:E272  ct_fd_channel7_vram_dma_streamer_over_two_six_entry_descriptor_halves_selected_by_051d_bit0   [strong structural]
- Exact setup:
  - `DB = 0x00`
  - `$2115 = 0x80`
  - `$4370 = 0x41`
  - `$4371 = 0x18`
  - `D = 0x0500`
  - `INC 051D`
  - `LSR 051D`-derived carry selects first vs second descriptor half
- Exact first descriptor half:
  - `05B0/05B2/05B4`
  - `05B5/05B7/05B9`
  - `05BA/05BC/05BE`
  - `05BF/05C1/05C3`
  - `05C4/05C6/05C8`
  - `05C9/05CB/05CD`
- Exact second descriptor half:
  - `05CE/05D0/05D2`
  - `05D3/05D5/05D7`
  - `05D8/05DA/05DC`
  - `05DD/05DF/05E1`
  - `05E2/05E4/05E6`
  - `05E7/05E9/05EB`
- Exact per-descriptor grammar:
  - if descriptor `+2` word is negative, skip
  - else write that word to `$2116`
  - use descriptor `+0 & 0x0E00` to index exact tables at `7F:0400` and `7F:0410`
  - add the `7F:0400` delta back into descriptor `+0`
  - write DMA source low/high from `7F:0410[index]` into `$4372`
  - write DMA source bank from descriptor `+4` into `$4374`
  - zero `$4375/$4376`, set `$4375 = 0x80`, and start DMA with `$420B = 0x80`
- Strongest safe reading: exact FD-side channel-7 VRAM DMA streamer over two alternating six-entry descriptor halves.

---

## Provisional strengthened RAM/state labels

### 7E:05B0..7E:05EB  ct_fd_local_two_half_vram_dma_descriptor_workspace_for_e022   [provisional strengthened]
- Pass 110 freezes the exact local consumption contract in `FD:E022..E272`.
- This region is now exact enough locally to call the descriptor workspace for the two DMA-stream halves.
- Broader subsystem ownership is still intentionally left open.

---

## Honest caution

### 7E:051D  ct_fd_local_descriptor_half_toggle_counter_consumed_by_e022   [caution]
- Exact local contract from pass 110:
  - `FD:E022` increments `051D`
  - uses the resulting bit-0 state to choose first vs second descriptor half
- Strongest safe reading: local half-toggle/counter for the FD-side VRAM DMA streamer.
- I have **not** frozen the broader writer/owner story yet.

### 7E:005F  ct_c0_local_pending_small_vram_patch_flag_byte_with_exact_bits_10_and_02_in_ed15   [caution]
- Pass 110 proves exact local contracts only:
  - `bit4` selects the primary immediate-patch family
  - `bit1` selects the secondary immediate-patch family
  - both are cleared by exact `TRB $5F` tails in their respective leaf bodies
- Broader subsystem meaning remains intentionally cautious.

---

## Important negative closure
- `FD:FFFD` is not a second deep body; it is only a veneer.
- `C0:ED15..F058` and `FD:E022..E272` are both VRAM update paths, but they are not twins.
- Neither path directly writes `7E:0128` or `$420C`.
- So the pass-109 split is now closed as a **transfer-method split**, not an HDMA-mask-ownership split.
