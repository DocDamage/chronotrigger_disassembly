# Chrono Trigger Labels — Pass 109

## Purpose
Pass 109 re-opened the old low-bank `0128 -> $420C` seam from the raw ROM bytes and corrected the misleading idea that the old `AE2B/AE33` pair was the main ownership path.

This pass proves instead that:
- the old `AE2B/AE33` pair sits inside a real forced-blank shutdown loop that zeroes both `$420C` and `0128`
- `EC00..EC5D` is the exact low-bank PPU-shadow flush tail that commits `0128 -> $420C`
- `EC74..ECA3` is an exact VRAM DMA upload helper
- `ECA4..ECCB` is an exact OAM DMA upload helper
- `ECCC..ED13` is an exact IRQ-side HBlank wait / force-blank / HDMA-off wrapper that branches by `0153.bit0`

---

## Strong labels

### C0:AE1E..C0:AE65  ct_c0_force_blank_shutdown_loop_zero_4200_420b_420c_and_0128_then_seed_cgram_from_x_and_spin   [strong structural]
- Continuity note: this is the body that contains the old seam pair previously discussed as `AE2B/AE33`.
- Exact body:
  - `SEI`
  - `DB = 0`
  - `$2100 = 0x80`
  - `$4200 = 0`
  - `$420B = 0`
  - `$420C = 0`
  - `0128 = 0`
  - `$212C = 0`
  - `$212D = 0`
  - `$2121 = 0`
  - write the 16-bit value from `X` into `$2122/$2122`
  - `0504 = 0x40`
  - `0500 = 0x40`
  - `0119 = 0x0F`
  - `$4200 = 0x81`
  - `$2100 = 0x0F`
  - `CLI`
  - self-loop forever
- Strongest safe reading: exact forced-blank shutdown/blackout loop that mirrors zero into both hardware HDMA enable and its low-bank shadow byte, seeds a CGRAM color from `X`, then spins.

### C0:EC00..C0:EC5D  ct_c0_interrupt_tail_refresh_fd_c1ee_flush_shadow_ppu_window_color_registers_commit_0128_to_420c_and_rti   [strong structural]
- Conditionally calls exact local helper families from `7B` bits:
  - bit 0 -> `JSR 875B`
  - bit 1 -> `JSR 878D`
  - bit 2 -> `JSR 87BF`
- Then:
  - `STZ 78`
  - `STZ 7A`
  - `D = 0x0100`
  - `JSL FD:C1EE`
  - `STZ 52`
  - `JSL C2:8002`
- Exact PPU/hardware flushes:
  - `0BD9 -> $2123`
  - `0BDA -> $2124`
  - `0BDB -> $2125`
  - `0BDC -> $2128`
  - `0BDD -> $2129`
  - `0BDE -> $2130`
  - `0121 -> $2132`
  - `0128 -> $420C`
- If `0119 == 0`, forces `$2100 = 0x80`.
- Exact terminator is `RTI`.
- Strongest safe reading: exact low-bank interrupt/service tail that refreshes the FD-side materialization path, flushes a contiguous PPU shadow block, commits the HDMA-enable shadow byte to hardware, and returns from interrupt.

### C0:EC74..C0:ECA3  ct_c0_dma_channel7_upload_7e_d800_span_to_vram_address_from_0be5_with_length_0be7   [strong structural]
- Exact body:
  - `0BE5 -> $2116`
  - `$2115 = 0x80`
  - channel 7 DMA config:
    - `$4370 = 0x01`
    - `$4371 = 0x18`
    - `$4372 = 0xD800`
    - `$4374 = 0x7E`
    - `$4375 = 0BE7`
  - `$420B = 0x80`
  - `RTS`
- Strongest safe reading: exact channel-7 VRAM DMA upload helper from `7E:D800`.

### C0:ECA4..C0:ECCB  ct_c0_dma_channel7_upload_000700_0220_bytes_to_oam_via_2104_after_zeroing_oam_address   [strong structural]
- Exact body:
  - `$2102 = 0`
  - `$2103 = 0`
  - channel 7 DMA config:
    - `$4370 = 0x00`
    - `$4371 = 0x04`
    - `$4372 = 0x0700`
    - `$4374 = 0x00`
    - `$4375 = 0x0220`
  - `$420B = 0x80`
  - `RTS`
- Strongest safe reading: exact OAM DMA upload helper.

### C0:ECCC..C0:ED13  ct_c0_irq_side_wait_hblank_force_blank_disable_hdma_then_choose_ed15_or_fd_fffd_by_0153_bit0_and_rti   [strong structural]
- Exact save/restore shape:
  - `REP #$30`
  - `PHA ; PHX ; PHY ; PHD ; PHB`
  - ...
  - `PLB ; PLD ; PLY ; PLX ; PLA ; RTI`
- Exact gating:
  - `LDA.l 010F ; BMI skip`
  - `LDA.l $4211 ; BPL skip`
- Exact active path:
  - `$4200 = 0x81`
  - `DB = 0`
  - poll `$4212` until `bit6` is set
  - `$2100 = 0x80`
  - `$420C = 0`
  - read `0153 & 0x01`
    - if clear -> `JSR ED15`
    - if set -> `JSL FD:FFFD`
- Strongest safe reading: exact IRQ-side HBlank wait / force-blank / HDMA-off wrapper with a hard `0153.bit0` branch split.

---

## Caution labels

### 7E:010F  ct_c0_local_interrupt_path_gate_byte_checked_before_4211_in_eccc   [caution]
- Exact reader proof:
  - `ECCC..ED13` reads `LDA.l 010F`
  - `BMI` skips the active force-blank/HBlank path entirely
- Strongest safe reading: exact interrupt-path gate byte for this wrapper.
- Final higher-level subsystem noun remains intentionally cautious.

### 7E:0BD9..7E:0BDE / 7E:0121  ct_c0_contiguous_shadow_block_flushed_into_2123_2124_2125_2128_2129_2130_and_2132   [caution]
- Exact sink proof from `EC00..EC5D`:
  - `0BD9 -> $2123`
  - `0BDA -> $2124`
  - `0BDB -> $2125`
  - `0BDC -> $2128`
  - `0BDD -> $2129`
  - `0BDE -> $2130`
  - `0121 -> $2132`
- Strongest safe reading: contiguous PPU shadow block flushed by the low-bank interrupt/service tail.
- Final broader subsystem naming should remain conservative for now.

---

## What this pass settles
- The old `AE2B/AE33` seam is no longer a fake “main producer” mystery.
  It is an exact forced-zero mirror path in a shutdown/blackout loop.
- The low-bank `0128 -> $420C` commit tail is now exact.
- The adjacent VRAM DMA and OAM DMA helpers are now exact.
- The IRQ-side wrapper that force-blanks, disables HDMA, and branches by `0153.bit0` is now exact.

---

## Honest caution
- I have **not** yet frozen the full broader meaning of `010F`.
- I have **not** yet solved the full `ED15..` body.
- I have **not** yet solved the deeper target behind `FD:FFFD -> FD:E022`.
- That `ED15 / FD:E022` split is now the cleanest next seam.
