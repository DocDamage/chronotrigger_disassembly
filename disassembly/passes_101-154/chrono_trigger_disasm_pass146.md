# Chrono Trigger Disassembly — Pass 146

## Summary

Pass 146 closes the callable/helper family that pass 145 left open at `C2:EAC2..C2:EB9A`.

The resolved family is:

- one exact short wrapper at `C2:EAC2..C2:EACB`
- one exact sibling short wrapper at `C2:EACC..C2:EAD5`
- one exact bit-gated packet wrapper at `C2:EAD6..C2:EAF8`
- one exact overlapping packet wrapper late entry at `C2:EAF9..C2:EB02`
- one exact gated packet-emitter helper at `C2:EB03..C2:EB1E`
- one exact signed table-walk / 3-byte record builder owner at `C2:EB1F..C2:EB9A`

## Exact closures

### C2:EAC2..C2:EACB

This span freezes as the exact short wrapper at the front of the family.

Key facts now pinned:
- Begins `PHP ; SEP #$30`.
- Loads exact immediate `00` into exact accumulator `A`.
- Runs exact helper `EB03`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact short wrapper that calls exact helper `EB03` with exact packet/control byte `00`.

### C2:EACC..C2:EAD5

This span freezes as the exact sibling short wrapper immediately behind the first one.

Key facts now pinned:
- Begins `PHP ; SEP #$30`.
- Loads exact immediate `01` into exact accumulator `A`.
- Runs exact helper `EB03`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact sibling short wrapper that calls exact helper `EB03` with exact packet/control byte `01`.

### C2:EAD6..C2:EAF8

This span freezes as the exact bit-gated packet wrapper behind the two short wrappers above.

Key facts now pinned:
- Begins `PHP ; SEP #$30`.
- Clears exact byte `0D76` before probing exact byte `0DBC`.
- When exact bit `0DBC.1` is set, seeds exact `X = 06` and braids into the shared exact `TXA ; JSR EB03` tail.
- Otherwise probes exact bit `0DBC.0`.
- When exact bit `0DBC.0` is set, seeds exact `X = 07`, clears that exact bit from exact byte `0DBC` through exact `TRB`, then braids into the shared exact `TXA ; JSR EB03` tail.
- When neither exact bit is set, returns immediately through exact `PLP ; RTS`.

Strongest safe reading: exact `0DBC`-bit-gated packet wrapper that clears exact latch byte `0D76`, chooses exact packet/control byte `06` versus `07`, clears exact `0DBC.0` on the `07` lane, and then calls exact helper `EB03`.

### C2:EAF9..C2:EB02

This span freezes as an exact overlapping packet-wrapper late entry into the helper below.

Key facts now pinned:
- Direct exact caller exists at `C2:9047`.
- Seeds exact `1E00 = 19`.
- Clears exact byte `0D76`.
- Exact `BRA +05` enters the shared exact `EB08` tail, where the caller-owned exact accumulator is written to exact byte `1E01` before the rest of exact helper `EB03` runs.

Strongest safe reading: exact overlapping packet-wrapper late entry that forces exact `1E00 = 19`, clears exact byte `0D76`, and rejoins the shared exact `EB03` tail.

### C2:EB03..C2:EB1E

This span freezes as the exact gated packet-emitter helper shared by all wrappers in the family.

Key facts now pinned:
- Seeds exact `1E00 = 18` on the main entry.
- Writes the exact incoming accumulator byte `A -> 1E01`.
- Reads exact latch byte `0D76`; when it is already nonzero, returns immediately.
- When exact latch byte `0D76 == 0`, seeds exact `0D76 = 03` and exact `1E02 = 80`.
- Runs exact long helper `C7:0004`.
- Exits `RTS`.

Strongest safe reading: exact gated packet-emitter helper that writes exact bytes `1E00/1E01/1E02`, uses exact byte `0D76` as a one-shot gate, and emits through exact long helper `C7:0004`.

### C2:EB1F..C2:EB9A

This span freezes as the exact signed table-walk / 3-byte record builder owner behind the packet wrappers above.

Key facts now pinned:
- Begins `PHP ; SEP #$30`.
- Uses exact count/state bytes `0DAA`, `0DA9`, `0DAB`, and exact signed control byte `0DAC` as the live front-end inputs.
- Builds exact loop count `00 = 0DAA` and exact `Y = 00`.
- Walks exact table records rooted at exact `9790,X` in exact 3-byte steps, with the sign of exact byte `0DAC` selecting the forward-versus-backward adjustment lane.
- On the exact negative lane, can clear exact bytes `0DAB` and `0DAC`, step exact index `0DA9` backward by one exact 3-byte record, and continue.
- On the exact positive lane, can step exact index `0DA9` forward by one exact 3-byte record and continue.
- Builds exact 3-byte work records into exact bands rooted at `969A,Y` and `969B,Y`.
- Repeats with exact `X += 3`, exact `Y += 3`, and exact loop counter `00--` until the exact `0DAA`-sized record build is complete.
- Finalizes with exact byte subtraction `978D,X - 969A -> 9697,Y`, sets exact bit `80` in exact byte `0D13`, restores exact flags, and exits through exact jump `821E`.

Strongest safe reading: exact signed table-walk / 3-byte record builder owner that uses exact state bytes `0DA9/0DAA/0DAB/0DAC` to walk exact tables rooted at `9790`, materializes exact 3-byte work records into exact `969A/969B`, and finalizes one exact downstream delta byte into exact `9697` before exact jump `821E`.

## Honest remaining gap

- the old seam `C2:EAC2..C2:EB9A` is now honestly closed through exact jump `C2:EB9A`
- the next clean follow-on owner starts at exact `C2:EB9B`
- the next obvious callable band is `C2:EB9B..C2:EC37`
- exact helper/owner anchors immediately visible there are:
  - exact owner entry `C2:EB9B`
  - exact new wrapper entry `C2:EC38`
- broader gameplay-facing nouns are still worth tightening for exact bytes/words `7E:0D76`, `7E:0DA9`, `7E:0DAA`, `7E:0DAB`, and `7E:0DAC`
