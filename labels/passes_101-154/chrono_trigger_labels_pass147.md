# Chrono Trigger Labels — Pass 147

## Purpose

Pass 147 closes the callable/helper family that pass 146 left open at `C2:EB9B..C2:EC37`, and it also closes the immediate callable spillover through `C2:ED30`.

## Strong labels

### C2:EB9B..C2:EC37  ct_c2_9696_9698_0daa_driven_wram_strip_materializer_and_step_seed_helper   [strong structural]
- Seeds exact word `9694 = 969A`.
- Uses exact caller-owned words `9696` and `9698` plus exact count byte `0DAA`.
- Copies an exact `3 * 0DAA` byte prefix into exact WRAM band `9793`.
- Materializes the downstream exact tail block into exact WRAM band `969A + 3*0DAA`.
- Patches exact metadata in the exact `9790/9791` family.
- Exact control bit `5A.bit2` chooses exact signed step word `0D22 = +0003` versus `-0003`.
- Clears exact byte `0DA9`, seeds exact loop word `0D24 = 0004`, and rewrites exact byte `00FD` from `05` to `04` on the exact compare lane.
- Strongest safe reading: exact WRAM strip/template materializer and exact stepped-loop seed helper for the downstream exact `EB1F` lane.

### C2:EC38..C2:EC92  ct_c2_six_row_ascending_word_writer_and_ff_block_importer_keyed_by_0d46_61_and_01   [strong structural]
- Uses exact selector byte `0D46` to load one exact seed byte from exact FF-bank table `FF:CE70`.
- Uses exact caller-owned exact destination base word `61`.
- Across six exact `0x40`-spaced rows, writes six consecutive exact words per row to offsets `+00/+02/+04/+06/+08/+0A`.
- Uses exact low three bits of exact `0D46` to choose one exact FF-bank source pointer from exact table `FF:CE78`.
- Uses exact caller-owned exact byte/word `01`, masked as exact `01 & 001C`, to choose exact WRAM destination band `9480 + 8*(01 & 001C)`.
- Copies exact `0x0020` bytes from that exact FF-bank source block into the chosen exact WRAM destination.
- Increments exact byte `0D15`.
- Strongest safe reading: exact six-row ascending-word writer plus exact FF-bank block importer.

### C2:EC93..C2:ECAB  ct_c2_counted_ecc2_row_wrapper_stepping_61_by_0040   [strong structural]
- Preserves the exact incoming accumulator on the stack.
- Replays that exact preserved descriptor through exact helper `ECC2` once per pass.
- After each pass, advances exact destination base word `61 += 0040`.
- Uses exact caller-owned `X` as the exact loop count.
- Strongest safe reading: exact counted `ECC2` row wrapper with exact `0x40` destination stride.

### C2:ECAC..C2:ECC1  ct_c2_paired_odd_byte_fill_helper_using_value_hi_and_count_lo_from_a   [strong structural]
- Uses exact low byte of caller-owned `A` as the exact loop count.
- Uses exact `XBA` so the exact high byte of caller-owned `A` becomes the exact written byte value.
- Writes that exact byte into both exact odd-byte twin lanes rooted at exact base word `61`.
- Strongest safe reading: exact paired odd-byte fill helper interpreting exact caller word `A` as `(value_hi,count_lo)`.

### C2:ECC2..C2:ECDA  ct_c2_counted_odd_byte_low_nibble_preserve_and_upper_bits_merge_helper   [strong structural]
- Uses exact low byte of caller-owned `A` as the exact loop count.
- Reads the current exact odd byte at exact base word `61`, preserves its exact low nibble through exact `AND #0F`, and merges exact caller-owned upper bits through exact `ORA`.
- Repeats over the exact odd-byte strip with exact stride `2`.
- Strongest safe reading: exact counted odd-byte nibble-merge helper preserving existing low nibble state.

### C2:ECDB..C2:ED07  ct_c2_bank_7e_setup_owner_deriving_0d47_0d48_then_running_edf6_ee7f_ed08   [strong structural]
- Temporarily sets exact data bank `7E`.
- Computes exact word `0D47 = 20 * 0D8C`.
- Computes exact byte/word `0D48 = (((79 + 1) << 2) | 03)`.
- Runs exact helper chain `EDF6 -> EE7F -> ED08`.
- Strongest safe reading: exact bank-7E setup owner in front of the `EDF6/EE7F/ED08` helper chain.

### C2:ED08..C2:ED30  ct_c2_ff_bank_16_byte_importer_keyed_by_0d8c_and_0d48_into_9490   [strong structural]
- Uses exact low three bits of exact `0D8C` to compute exact FF-bank source base `B210 + 0x0010 * (0D8C & 0007)`.
- Uses exact `0D48 & 001C`, scaled by exact stride `8`, to choose exact WRAM destination band `9490 + 8*(0D48 & 001C)`.
- Copies exact `0x0010` bytes from the computed exact FF-bank source block into that exact WRAM destination.
- Increments exact byte `0D15`.
- Strongest safe reading: exact FF-bank 16-byte importer keyed by exact state bytes `0D8C/0D48`.

## Honest remaining gap

- the old seam `C2:EB9B..C2:EC37` is now honestly closed through exact `C2:ED30`
- the next clean follow-on owner starts at exact `C2:ED31`
- the next obvious callable band is `C2:ED31..C2:EE7F`
