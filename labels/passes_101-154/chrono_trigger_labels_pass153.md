# Chrono Trigger Labels — Pass 153

## Purpose

Pass 153 corrects the front of the old seam and freezes the real shared callable/helper block behind it.

## Strong labels

### C2:F588..C2:F5A6  ct_c2_eight_row_direct_page_row_clear_helper_over_19c0_minus_40n   [strong structural]
- Begins `PHP ; PHD ; PEA $19C0 ; PLD ; SEP #$30`.
- Seeds exact row byte `00 = FF` and clears exact row bytes `11` and `18`.
- Reenters exact 16-bit accumulator mode while also clearing exact carry through `REP #$21`.
- Uses exact `TDC ; SBC #$003F ; TCD` to walk the exact direct-page base downward by exact `0x0040` per iteration.
- Continues while the exact resulting direct-page base remains `>= 1800`.
- Exact cleared row bases are `19C0`, `1980`, `1940`, `1900`, `18C0`, `1880`, `1840`, and `1800`.
- Strongest safe reading: exact eight-row direct-page row-clear helper over exact row bands `19C0 - 0x40*n` down through exact `1800`.

### C2:F5A7..C2:F5EC  ct_c2_two_phase_strip_staging_import_owner_using_e4_ffe8_then_f5ed_into_95a2_95ba_bands   [strong structural]
- Begins `PHP ; REP #$30`, loads exact word `E4:FFE8 -> 00`, and seeds exact destination `Y = 95A2`.
- First exact phase repeatedly loads one exact bank-`E4` source word through exact pointer list `[00]`, copies exact `0x0018` bytes into bank `7E`, advances exact word `00 += 0002`, and advances exact destination by exact `0x0020`.
- Exact first-phase destination starts are `95A2`, `95C2`, `95E2`, `9602`, `9622`, `9642`, and `9662`.
- Second exact phase seeds exact destination `Y = 95BA`, clears exact loop word `00`, and for exact loop values `00 = 0000..0006` runs exact helper `F5ED` to derive one exact bank-`D1` source.
- Each exact second-phase iteration copies exact `0x0006` bytes into bank `7E` and advances exact destination by exact `0x0020`.
- Exact second-phase destination starts are `95BA`, `95DA`, `95FA`, `961A`, `963A`, `965A`, and `967A`.
- Strongest safe reading: exact two-phase strip staging/import owner that materializes one exact `E4:FFE8`-driven strip family and one exact `F5ED`-derived bank-`D1` strip family into the exact `95xx` staging bands.

### C2:F5ED..C2:F625  ct_c2_bank_d1_strip_source_derivation_helper_using_hw_mul_50_and_tables_2629_cd6cec   [strong structural]
- Preserves the incoming exact byte in exact 8-bit accumulator mode.
- Writes exact multiplicand `50` to exact hardware register `$4202` and the preserved exact input byte to exact `$4203`.
- On the observed exact non-negative path, snapshots exact product `$4216` into `X`, loads one exact byte from exact table `2629,X`, and mirrors that exact byte into exact `041B`.
- Uses that exact byte as an index into exact table `CD:6CEC`, keeps only the exact low byte `v`, and derives exact source word `X = 4B00 + 6*v`.
- Returns exact transfer length `A = 0005`.
- Strongest safe reading: exact bank-`D1` strip-source helper that maps one exact small selector byte into one exact `D1:4B00 + 6*v` source plus fixed exact length `0005`.

### C2:F626..C2:F642  ct_c2_a_times_40_hardware_multiply_helper_returning_0d2c_and_y   [strong structural]
- Preserves the incoming exact accumulator and flags.
- In exact 8-bit accumulator mode writes the exact incoming byte to exact `$4202` and exact factor byte `40` to exact `$4203`.
- Reenters exact 16-bit mode and snapshots exact product `$4216 -> 0D2C`.
- Mirrors that exact product into exact `Y`.
- Restores the exact original accumulator and exact flags before returning.
- Strongest safe reading: exact helper that derives exact row/base offset `0D2C/Y = 0x40 * input_byte` while preserving the caller’s exact accumulator.

### C2:F643..C2:F656  ct_c2_fixed_8249_scheduler_wrapper_for_local_f657_callback   [strong structural]
- Begins `PHP ; REP #$30`.
- Clears exact words `0D2E` and `0D30`.
- Seeds exact callback pointer `A = F657` and exact delay/count `X = 0028`.
- Runs exact helper `8249`, restores exact flags, and returns.
- Strongest safe reading: exact fixed `8249` scheduler/setup wrapper for the downstream local callback/service owner rooted at exact `F657`.

## Caution labels

### C2:F56A..C2:F587  ct_c2_unresolved_pre_f588_span_needing_stack_balance_proof   [caution structural]
- No direct exact call xrefs currently land here.
- As a standalone exact entry, the visible exact stack discipline does not yet balance cleanly enough to freeze.
- This span may be exact helper tail / data crossover rather than one exact clean callable owner.
- Do not freeze it as exact standalone code until upstream proof lands.

## Honest remaining gap

- exact `C2:F588..C2:F656` is now honestly closed
- exact `C2:F56A..C2:F587` remains a correction hole rather than a proven callable entry
- the next clean forward callable band begins at exact `C2:F657`
