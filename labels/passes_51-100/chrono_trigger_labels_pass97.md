# Chrono Trigger Labels — Pass 97

## Strong labels

### C7:0155..C7:0191  ct_c7_shared_post_prologue_redispatch_entry_for_preseeded_1e00_header_bytes_under_negative_1e05_gate   [strong structural]
- Entered only after the `0140` dispatcher prologue has already saved registers, forced `DB = 00`, and installed exact direct page `D = 1E00`.
- Re-reads exact control byte `1E05`; if it is non-negative, exits through common dispatcher epilogue `0192`.
- Re-reads exact opcode byte `1E00`; if it is zero, exits.
- If exact opcode byte `1E00` is negative / signed-high, jumps directly to `061C`.
- If exact opcode is below `0x10`, exits.
- If `0x10..0x17`, dispatches through exact gate table `0AD9`.
- If `0x18..0x2F`, jumps directly to `061C`.
- If `0x30..0x3F`, jumps to `071D`.
- If `0x70`, jumps to `08E3`; if `0x71`, jumps to `0755`; otherwise exits.
- The only exact external tail-entry back into this body is raw `JMP $0155` from `071D`.
- Strongest safe reading: exact shared post-prologue redispatch entry over preseeded low-bank packet header bytes, under the negative-`1E05` control gate.

### C7:061C..C7:064F  ct_c7_send_exact_four_byte_apu_packet_from_1e00_1e03_for_negative_or_18_2f_header_opcodes_then_apply_fc_threshold_fixup_if_needed   [strong]
- Dispatcher body `0155..0191` reaches this sender in two exact cases:
  - exact opcode byte `1E00` is negative / signed-high
  - exact opcode byte is in the direct `0x18..0x2F` band
- Sends exact bytes `1E03 / 1E02 / 1E01 / 1E00` through `$2143/$2142/$2141/$2140`.
- Retries until `$2140` echoes the just-written opcode byte.
- If exact opcode byte `1E00 == 0xFC`, compares exact selector low nibble `1E01 & 0x0F` against exact local byte `F0` and calls `09FD` when they differ.
- Exits through the common dispatcher epilogue at `0192`.
- Strongest safe reading: exact shared immediate 4-byte APU packet sender for negative-header opcodes and for the direct low-bank `0x18..0x2F` family, with one exact `0xFC` threshold-fixup case.

### C7:071D..C7:0733  ct_c7_rewrite_opcode_30_3f_family_into_synthetic_10_selector_ff_ff_packets_then_redispatch_at_0155   [strong structural]
- Masks exact opcode byte `1E00` to its low nibble.
- Multiplies by four and indexes the exact 16-entry packet-rewrite table rooted at `C7:0A98`.
- Loads one exact 16-bit word from `C7:0A98 + index` into `1E00 / 1E01`.
- Loads one exact 16-bit word from `C7:0A9A + index` into `1E02 / 1E03`.
- The rewritten header is exact:
  - `1E00 = 0x10`
  - `1E01 = low nibble of original `0x30..0x3F` opcode`
  - `1E02 = 0xFF`
  - `1E03 = 0xFF`
- Tail-jumps to exact redispatch entry `0155`.
- Because `0155` redispatches exact opcode `0x10` through gate table `0AD9`, and `0AD9[0] = 01A1`, this bridge lands in the negative-`1E05` special path.
- Strongest safe reading: exact packet-rewrite + redispatch bridge from the `0x30..0x3F` family into the `01A1` special-path entry.

### C7:0A98..C7:0AD7  ct_c7_exact_16_entry_rewrite_table_mapping_opcode_30_3f_low_nibbles_to_synthetic_10_selector_ff_ff_packets   [strong]
- Exact 16-entry table.
- Exact entry width: 4 bytes.
- Exact consumer: bridge body `071D..0733`.
- Entry `n` is exactly:
  - byte 0 = `0x10`
  - byte 1 = `n`
  - byte 2 = `0xFF`
  - byte 3 = `0xFF`
- Therefore exact rewritten packets are:
  - `30 -> 10 00 FF FF`
  - `31 -> 10 01 FF FF`
  - `32 -> 10 02 FF FF`
  - ...
  - `3F -> 10 0F FF FF`
- Strongest safe reading: exact packet-rewrite table that converts the `0x30..0x3F` family into synthetic `{0x10, selector, 0xFF, 0xFF}` headers before redispatch at `0155`.

## Provisional labels
None added this pass.

## Alias / wrapper / caution labels
None added this pass.
