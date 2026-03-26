# Chrono Trigger Labels — Pass 160

## Purpose

Pass 160 closes the exact unresolved bank-end tail at exact `C2:FFEE..C2:FFFF` honestly as one exact non-owner overlap/tail span.

## Alias / wrapper / caution labels

### C2:FFEE..C2:FFFF  ct_c2_bank_end_truncated_duplicate_tail_of_ff87_import_and_mirror_helper_family   [caution structural]
- Exact bytes: `95 A9 05 00 54 7E D1 A2 BA 95 A0 3A 96 A9 05 00 54 7E`.
- The exact span begins in the middle of one exact already-proven import/mirror byte pattern, not at one exact sane routine prologue.
- Exact interior pattern matches the exact helper family already frozen at exact `C2:FF87..C2:FFA3` / exact `C2:FFC1..C2:FFDD`:
  - exact `... A9 05 00 ; MVN 7E,D1 ; A2 BA 95 ; A0 3A 96 ; A9 05 00 ; MVN 7E,7E ...`
- At exact `FFEE..FFFF`, the bank ends before one exact balanced standalone stream can finish.
- No exact cached hot direct caller currently lands at exact `FFEE`.
- Strongest safe reading: exact bank-end truncated duplicate / overlap tail from the exact `FF87` import-and-mirror helper family, not one exact independently callable owner.

## Honest remaining gap

- bank `C2` is now honestly closed through exact `FFFF`
- the next real investigation target is the raw low-bank startup cluster immediately after the boundary, especially exact `C3:0000..C3:0013` and the exact owner beginning at exact `C3:0014`
- toolkit v6.7 still has one exact low-bank inspection gap for these raw/project addresses, so the next pass should use one exact manual/raw-byte lane there instead of pretending the default inspector already handles it
