# Chrono Trigger Labels — Pass 146

## Purpose

Pass 146 closes the callable/helper family that pass 145 left open at `C2:EAC2..C2:EB9A`.

## Strong labels

### C2:EAC2..C2:EACB  ct_c2_short_wrapper_calling_eb03_with_a_00   [strong structural]
- Begins `PHP ; SEP #$30`.
- Loads exact immediate `00` into exact accumulator `A`.
- Runs exact helper `EB03`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact short wrapper that calls exact helper `EB03` with exact packet/control byte `00`.

### C2:EACC..C2:EAD5  ct_c2_short_wrapper_calling_eb03_with_a_01   [strong structural]
- Begins `PHP ; SEP #$30`.
- Loads exact immediate `01` into exact accumulator `A`.
- Runs exact helper `EB03`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact sibling short wrapper that calls exact helper `EB03` with exact packet/control byte `01`.

### C2:EAD6..C2:EAF8  ct_c2_0dbc_bit_gated_packet_wrapper_clearing_0d76_selecting_06_or_07_then_calling_eb03   [strong structural]
- Clears exact byte `0D76` before probing exact byte `0DBC`.
- When exact bit `0DBC.1` is set, seeds exact packet/control byte `06` and braids into the shared exact `TXA ; JSR EB03` tail.
- Otherwise probes exact bit `0DBC.0`.
- When exact bit `0DBC.0` is set, seeds exact packet/control byte `07`, clears exact `0DBC.0` through exact `TRB`, and then calls exact helper `EB03`.
- When neither exact bit is set, returns immediately through exact `PLP ; RTS`.
- Strongest safe reading: exact `0DBC`-bit-gated packet wrapper choosing exact packet/control byte `06` versus `07` before exact helper `EB03`.

### C2:EAF9..C2:EB02  ct_c2_overlapping_packet_wrapper_entry_forcing_1e00_19_clearing_0d76_then_joining_eb03_tail   [strong structural]
- Exact overlapping callable late entry with a direct exact caller at `C2:9047`.
- Seeds exact `1E00 = 19`.
- Clears exact byte `0D76`.
- Exact `BRA +05` enters the shared exact `EB08` tail, where the caller-owned exact accumulator is written to exact byte `1E01` before the rest of exact helper `EB03` runs.
- Strongest safe reading: exact overlapping packet-wrapper late entry into the shared exact `EB03` tail.

### C2:EB03..C2:EB1E  ct_c2_gated_1e00_1e01_1e02_packet_emitter_using_0d76_then_c70004   [strong structural]
- Seeds exact `1E00 = 18` on the main entry.
- Writes the exact incoming accumulator byte `A -> 1E01`.
- Reads exact latch byte `0D76`; when it is already nonzero, returns immediately.
- When exact latch byte `0D76 == 0`, seeds exact `0D76 = 03` and exact `1E02 = 80`.
- Runs exact long helper `C7:0004`.
- Strongest safe reading: exact gated packet-emitter helper for exact bytes `1E00/1E01/1E02`.

### C2:EB1F..C2:EB9A  ct_c2_signed_9790_table_walk_and_3_byte_record_builder_using_0da9_0daa_0dab_0dac_into_969a_969b_9697   [strong structural]
- Uses exact front-end state bytes `0DAA`, `0DA9`, `0DAB`, and exact signed control byte `0DAC`.
- Walks exact table records rooted at exact `9790,X` in exact 3-byte steps, with the sign of exact byte `0DAC` selecting the forward-versus-backward adjustment lane.
- Can step exact index/state byte `0DA9` backward or forward by one exact 3-byte record depending on the exact compare lane.
- Can clear exact bytes `0DAB` and `0DAC` on the negative exact saturation lane.
- Builds exact 3-byte work records into exact bands rooted at `969A,Y` and `969B,Y`.
- Finalizes with exact byte subtraction `978D,X - 969A -> 9697,Y`, sets exact bit `80` in exact byte `0D13`, restores exact flags, and exits through exact jump `821E`.
- Strongest safe reading: exact signed table-walk / 3-byte record builder owner for the downstream exact `969A/969B/9697` work bands.

## Honest remaining gap

- the old seam `C2:EAC2..C2:EB9A` is now honestly closed through exact jump `C2:EB9A`
- the next clean follow-on owner starts at exact `C2:EB9B`
- the next obvious callable band is `C2:EB9B..C2:EC37`
