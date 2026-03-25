# Chrono Trigger Disassembly Progress — Pass 138

## Summary

Pass 138 closes the exact follow-on callable/helper family that pass 137 left open at `C2:DACB..C2:DB30`, but the first correction is structural again: the seam does **not** end at `DB30`. It resolves cleanly into:

- one exact setup/import/export owner at `C2:DACB..C2:DB97`
- one exact local 7-byte selector descriptor packet at `C2:DB98..C2:DB9E`
- one exact `1000`-strip scan helper at `C2:DB9F..C2:DBE6`
- one exact `0D5F -> 104D/93CC/93CD` export helper at `C2:DBE8..C2:DC1C`
- one exact `104D`-driven row/materializer owner at `C2:DC1E..C2:DC73`
- one exact local 7-byte row-offset table at `C2:DC74..C2:DC7A`

The important closure is that this band is not a fuzzy packet blob. It is one exact setup/build owner that fans into two exact local helpers and one exact follow-on materializer owner, with two exact local data packets feeding the tail.

## What this pass closes

### C2:DACB..C2:DB97

This span freezes as the real exact setup/import/export owner immediately after the pass-137 exact `FD68` accumulator tail.

Key facts now pinned:
- Begins `SEP #$20`, seeds exact bytes `79 = 0C` and `54 = 08`, then runs exact helpers `984A` and `ED31` with exact selector word `C213`.
- Reenters exact `REP #30`, clears exact words `1040` and `1042`, then copies exact block `7E:9990 -> 7E:9380` across exact length `0x0048`.
- Uses exact slot byte `71` to index exact long table `CC:2C6D`, selecting one exact source block that is copied into exact WRAM window `1000` across exact length `0x0020`.
- Runs exact helpers `DCBE` and `E012`, then clears exact byte `0D77`.
- Imports four exact fixed blocks into exact WRAM packet/work bands: two copies from exact `FF:CBAC` into exact `94C0/94C8`, then two copies from exact `FF:9C70` into exact `9560/9568`.
- Seeds exact `Y = 9500` and runs exact helper `A0E7`.
- Seeds exact word `5D42 = 61FF` and uses overlapping same-bank `MVN 7E,7E` to propagate that exact fill band forward.
- Runs exact long helper `FFF548`, exact local helper `DC1E`, and exact helper `F643`.
- In exact 8-bit mode, clears exact bytes `04C9` and `04CA`, increments exact byte `0D15`, then runs exact helpers `DD7C`, `86DD`, and exact local helper `DB9F`.
- Tail-emits four exact selector packets through `8385` in exact order `FC3E`, `FBCE`, `FBF8`, and exact local packet `DB98`, then seeds exact byte `0D13 = 2F` and exits `PLP ; RTS`.

Strongest safe reading: exact setup/import/export owner that seeds selector `C213`, mirrors exact block `9990 -> 9380`, imports one exact `CC:2C6D[71]`-selected `0x20`-byte strip into exact WRAM window `1000`, refreshes exact fixed packet bands through `DCBE / E012 / A0E7`, propagates exact fill `61FF` across the `5D42` band, and finalizes through exact helper `DB9F` plus a four-packet exact `8385` selector tail.

### C2:DB98..C2:DB9E

This span freezes as the exact local 7-byte selector descriptor packet used only by the exact `DACB` owner.

Key facts now pinned:
- Exact bytes: `00 10 00 B0 7E 00 11`.
- Reached only through exact helper `8385` from the exact final tail of `DACB`.

Strongest safe reading: exact local selector descriptor packet for the exact `DACB` setup/import/export owner.

### C2:DB9F..C2:DBE6

This span freezes as the exact `1000`-strip scan helper called directly by exact owner `DACB`.

Key facts now pinned:
- Begins `PHP ; REP #30`.
- Loads exact long word `7F:01CD -> 04`, seeds exact word `02 = 0002`, and clears exact loop index word `22`.
- Walks exact word strip `1000,X` until the first exact zero entry.
- For each nonzero exact strip entry, doubles it into exact `Y`, loads exact word `7800,Y -> 00`, and runs exact helper `FD58`.
- When exact word `41 & 00FF` is nonzero, forces exact result word `FDE8`.
- Otherwise derives the exact result from the exact `3E/3F` pair, incrementing exact byte `3F` when needed and forcing exact result word `0001` when the exact low-byte result would otherwise stay zero.
- Stores one exact result word into exact table `6E00,Y`, increments exact index word `22`, and loops.
- Exits `PLP ; RTS` at the exact zero terminator in the `1000` strip.

Strongest safe reading: exact `1000`-strip scan helper that stages exact `7F:01CD/0002`, uses exact `7800` and exact helper `FD58` to derive one exact word result per live exact `1000` entry, and writes that exact result table into `6E00..` until the strip terminates.

### C2:DBE8..C2:DC1C

This span freezes as the exact compact/export helper directly called by exact owner `DACB`.

Key facts now pinned:
- Begins `PHP ; SEP #$30`.
- Scans exact byte table `0D5F[0..8]`.
- Copies every non-negative exact byte into compact exact list `104D,Y`, incrementing exact destination `Y` only for accepted exact entries.
- Stops after exact `X == 09`, appends exact terminator byte `FF` at `104D,Y`, and stores the exact compacted length pointer into exact word `1055`.
- Loads exact byte `85`, decrements it by exact one step, mirrors that exact value into direct-page `00`, then seeds exact byte `93CC = (85 - 1) + 0C`.
- Computes exact `X = 3 * (85 - 1)` and seeds exact byte `93CD,X = 0C`.
- Exits `PLP ; RTS`.

Strongest safe reading: exact `0D5F` compactor/export helper that builds a compact exact non-negative byte list in `104D` with exact `FF` terminator and exact length pointer `1055`, then stamps exact export/control bytes into `93CC` and `93CD` from exact byte `85`.

### C2:DC1E..C2:DC73

This span freezes as the exact follow-on `104D`-driven row/materializer owner called directly by exact owner `DACB`.

Key facts now pinned:
- Begins `PHP ; SEP #$20`, runs exact helper `F588`, seeds exact byte `0D75 = 07`, and clears exact bytes `02` and `03`.
- Switches to exact 16-bit index mode, seeds exact destination row pointer `Y = 51`, clears exact slot byte `71`, and initializes exact `X = 0000`.
- Walks compact exact list `104D,X` until the exact `FF` terminator.
- For each live exact entry, runs exact helper `8816`, loads exact byte `9A90`, runs exact helper `F626`, and stores the exact result byte into exact row field `1800,Y`.
- Uses exact byte `02` to index exact local table `DC74`, writing one exact table byte to exact row field `180F,Y` and exact constant byte `C0` to exact row field `180E,Y`.
- Derives exact slot UI/materializer offset `Y = 8 * 02`, writes exact byte `(9A90 | 20)` to exact field `3404,Y`, exact byte `20` to exact field `3405,Y`, and exact byte `2E` to exact field `3444,Y`.
- Increments exact bytes `02` and `71` and loops while the exact carry from helper `F626` remained clear.
- Exits `PLP ; RTS` when the compact exact `104D` list terminates or the exact carry-driven loop ends.

Strongest safe reading: exact `104D`-driven row/materializer owner that seeds mode `0D75 = 07`, walks the compact exact active-entry list, uses exact helper `F626` to derive one exact `1800` row byte per entry, stamps exact local row-offset bytes from table `DC74`, and writes matching exact `3404/3405/3444` UI/materializer bytes for each accepted slot.

### C2:DC74..C2:DC7A

This span freezes as the exact 7-byte local row-offset table used only by exact owner `DC1E`.

Key facts now pinned:
- Exact bytes: `20 40 60 80 A0 C0 E0`.

Strongest safe reading: exact local seven-byte row-offset table for the exact `DC1E` row/materializer owner.

## What remains after pass 138

- the next clean seam now begins at the follow-on callable family `C2:DC7B..C2:DD80`
- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
