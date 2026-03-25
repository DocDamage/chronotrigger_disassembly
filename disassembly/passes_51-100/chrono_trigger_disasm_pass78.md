# Chrono Trigger Disassembly — Pass 78

## Scope of this pass
This pass continues directly from the pass-77 seam.

Pass 77 tightened the late service-04 output side a lot, but three useful things were still sitting in the "structural but annoyingly black-box" bucket:

1. `C3:0002`, which service-04 uses to materialize the packed `2D00..` stream before `4943` decodes it
2. the two unconditional `CD` helpers at `0015` and `002A`
3. the optional `CD:0018` stage that only runs when `AE94 == 0`, `987C != FF`, and `AE93 != 37`

The big honest result of this pass is:

> `C3:0002` is a generic packed-stream-to-WRAM unpack/materialize worker,
> `CD:0015` and `CD:002A` are the two fixed builders that populate the six packed row-sections of the `2D00..` workspace,
> and `CD:0018` is an optional selector-driven auxiliary fragment-stage initializer/expander.

That still does **not** freeze every final gameplay noun downstream of `4500.. -> 5D00..`, but it gives the pre-decode pipeline a much cleaner memory model.

---

## 1. `C3:0002` is a generic packed-stream-to-WRAM materializer veneer
The call site inside the common service-04 tail is:

```text
C1:486D  AE 7F 98      LDX $987F
C1:4870  8E 00 03      STX $0300
C1:4873  A9 D1         LDA #$D1
C1:4875  8D 02 03      STA $0302
C1:4878  A2 00 2D      LDX #$2D00
C1:487B  8E 03 03      STX $0303
C1:487E  A9 7E         LDA #$7E
C1:4880  8D 05 03      STA $0305
C1:4883  22 02 00 C3   JSL $C3:0002
C1:4887  AE 06 03      LDX $0306
C1:488A  9E 00 2D      STZ $2D00,X
C1:488D  9E 01 2D      STZ $2D01,X
```

So the service-04 caller is clearly passing:

- `0300..0302` = source pointer (`D1:987F`)
- `0303..0305` = destination pointer (`7E:2D00`)
- `0306`       = returned size / destination advance

Direct bytes at the entry:

```text
C3:0002  4C 57 05      JMP $0557
```

So `C3:0002` is just a veneer. The real worker is `C3:0557`.

### 1a. `C3:0557` writes through the WRAM port and therefore materializes directly into caller-selected WRAM
The front of the worker does this:

```text
C3:056B  A5 03         LDA $03
C3:056D  8F 81 21 00   STA $2181
...
C3:0581  A5 05         LDA $05
C3:0583  8F 83 21 00   STA $2183
```

That is explicit use of the SNES WRAM data-port address registers:

- `$2181` = WRAM address low/high
- `$2183` = WRAM bank
- repeated stores to `$2180` = actual streamed destination bytes

Then the routine repeatedly writes bytes with:

```text
8F 80 21 00
```

So this is not a generic CPU-memory `MVN` copy.
It is a **packed-stream expander/materializer that writes its decoded output through the WRAM port into caller-selected WRAM**.

### 1b. the routine has multiple inner variants, but they are all output materializers
The top-level worker dispatches into several large inner bodies (`0557`, `06A8`, `072D`, `08A4` neighborhood) depending on source/destination-state bits.

The repeated structure is the same in all of them:

- read packed source bytes from the caller-supplied source pointer
- interpret control bits / run lengths / literal spans
- write decoded bytes to `$2180`
- track the destination advance in `Y`

The internal details differ, but all branches are clearly **different packed decode grammars / variants of the same WRAM-output materializer family**, not unrelated code.

### 1c. `0306` is the returned output size / destination advance
The worker exits with:

```text
C3:08A3  98            TYA
C3:08A4  38            SEC
C3:08A5  E5 03         SBC $03
C3:08A7  85 06         STA $06
```

That is exact:

- current destination offset in `Y`
- minus starting destination offset at `$03`
- stored to `$06`

So `0306` is **not** a returned source cursor.
It is the **number of output bytes materialized into the destination buffer**.

That is why the service-04 caller immediately uses `0306` as the zero-termination point inside `2D00..`.

Safest upgraded reading:

> `C3:0002 -> C3:0557` = **generic packed-stream-to-caller-selected-WRAM materializer / unpacker returning output byte count in `0306`**

This also sharpens the noun of `2D00..`: it is the **materialized packed row-stream workspace** consumed next by `4943`, not an opaque scratch blob.

---

## 2. `CD:0015` and `CD:002A` are the two fixed builders that populate the six packed row-sections of `2D00..`
The service-04 common tail begins with:

```text
C1:4833  AD 7A 98      LDA $987A
C1:4836  22 15 00 CD   JSL $CD:0015
C1:483A  AD 7B 98      LDA $987B
C1:483D  22 2A 00 CD   JSL $CD:002A
```

The entry veneers are just jumps into two real workers:

```text
CD:0015  4C 23 13      JMP $1323
CD:002A  4C 14 13      JMP $1314
```

### 2a. the two workers are the same family, but they cover different row-section ranges
The front of the two real entries is the key split:

```text
CD:1323  8D CE CA      STA $CACE
CD:1326  9C CF CA      STZ $CACF
CD:1329  A9 04         LDA #$04
CD:132B  8D D0 CA      STA $CAD0
...
```

versus:

```text
CD:1314  8D CE CA      STA $CACE
CD:1317  A9 04         LDA #$04
CD:1319  8D CF CA      STA $CACF
CD:131C  A9 06         LDA #$06
CD:131E  8D D0 CA      STA $CAD0
```

Then the shared loop does:

- `CF = CACE / CACF / CAD0` bookkeeping
- `Y = CD:1308[CF]`
- write through a `2D00 + Y` destination pointer
- increment `CACF`
- stop when `CACF == CAD0`

The `CD:1308` table is:

```text
000C 000E 0010 0012 0014 0016
```

So the split is exact:

- `CD:0015 -> CD:1323` builds section indices `0..3`
  - bases `2D00 + 0C / 0E / 10 / 12`
- `CD:002A -> CD:1314` builds section indices `4..5`
  - bases `2D00 + 14 / 16`

That is why the C1 caller always runs them in that order: together they populate the **six packed row-sections** later consumed from the `2D00..` workspace.

### 2b. the shared worker uses a selector-word stream plus a per-section source stream
Inside the shared body:

```text
CD:1335  AD CE CA      LDA $CACE
CD:1338  AA            TAX
CD:1339  20 68 13      JSR $1368
CD:133C  AD CF CA      LDA $CACF
CD:133F  0A            ASL A
CD:1340  AA            TAX
CD:1341  C2 20         REP #$20
CD:1343  BF 08 13 CD   LDA CD:1308,X
CD:1347  A8            TAY
...
CD:137F  A6 57         LDX $57
CD:1381  BF 00 E0 CF   LDA CF:E000,X
CD:1385  8D 9D CC      STA $CC9D
CD:1388  8D 9F CC      STA $CC9F
```

and later:

```text
CD:13A0  20 CA 13      JSR $13CA
CD:13A3  AA            TAX
CD:13A4  C2 20         REP #$20
CD:13A6  BF 00 13 CD   LDA CD:1300,X
CD:13AA  85 5F         STA $5F
CD:13AC  A7 53         LDA [$53]
```

This is strong structural proof that each section-build iteration uses **two coordinated data sources**:

1. a selector-word stream rooted in `CF:E000 + 0x40*section`
2. a per-section source stream rooted in `CF:A000 + 0x40*section`

The selector helper at `13CA` extracts one of four 2-bit selector classes from the active selector word in `CC9D/CC9F`, then `CD:1300` maps that selector class to one of four masks:

```text
0000, 00FF, FF00, FFFF
```

So the row-section builder is not a dumb literal copier.
It is a **selector/mask-driven packed row-section constructor** into `2D00..`.

### 2c. the worker chooses one of four transform modes per source byte
The shared body takes the source byte from `[$53]`, derives a small transform id from its upper bits, and dispatches through the local jump table at `13E6`:

```text
CD:13AC  A7 53         LDA [$53]
CD:13AE  EB            XBA
CD:13AF  4A 4A 4A 4A 4A
CD:13B4  29 06 00      AND #$0006
CD:13B7  AA            TAX
CD:13B8  FC E6 13      JSR ($13E6,X)
```

The four local targets are:

- `13F6`
- `1445`
- `14EE`
- `1509`

So each section byte can take one of **four transform/materialization modes** before being written into the packed `2D00..` row workspace.

The safest honest noun here is still structural, but much stronger than pass 77:

> `CD:0015` and `CD:002A` = **the two fixed packed row-section builders that populate the six `2D00..` fragment-row sections via selector-word masks and per-section source streams**

---

## 3. `CD:0018` is an optional selector-driven auxiliary fragment-stage initializer / expander
The optional stage in the service-04 common tail is:

```text
C1:4841  AD 93 AE      LDA $AE93
C1:4844  C9 37         CMP #$37
C1:4846  F0 05         BEQ skip
C1:4848  AD 94 AE      LDA $AE94
C1:484B  D0 0B         BNE skip
C1:484D  AD 7C 98      LDA $987C
C1:4850  C9 FF         CMP #$FF
C1:4852  F0 04         BEQ skip
C1:4854  22 18 00 CD   JSL $CD:0018
```

The entry veneer is just:

```text
CD:0018  4C 28 0D      JMP $0D28
```

### 3a. `CD:0D28` is a coordinator, not the real heavy worker
Front bytes:

```text
CD:0D28  9C 9B 5D      STZ $5D9B
CD:0D2B  AA            TAX
CD:0D2C  20 BD 0E      JSR $0EBD
CD:0D2F  20 33 0D      JSR $0D33
CD:0D32  6B            RTL
```

So the optional stage has a clean top-level shape:

1. clear `5D9B`
2. treat input `A` as a selector
3. run selector/battle-layout init through `0EBD`
4. expand the resulting descriptor list through `0D33`

### 3b. `CD:0D33` clears three work tables and expands a descriptor list from `CA93`
The first half of `0D33` does:

```text
REP #$20
TDC
TAX
STZ $CA32,X
STZ $CA52,X
STZ $CA72,X
... loop until X == 0x20
```

Then the second half walks `CA93`:

```text
SEP #$20
TDC
TAX
TAY
LDA $CA93,Y
CMP #$FF
BEQ skip
JSR $15D5
...
```

So the auxiliary stage is clearly building or refreshing a **descriptor-driven auxiliary work model** in the `CA32/52/72` families, not directly touching the `2D00..` row stream.

### 3c. `CD:0EBD` is selector/battle-layout initialization for that auxiliary stage
The front of `0EBD` shows that it does selector-sensitive setup and also checks battle-layout state (`A017/A018`, `2A21`, `2C66/67`, etc.) before seeding the later work:

```text
CD:0EBD  E0 88 00      CPX #$0088
...
CD:0EC2  AD 18 A0      LDA $A018
CD:0EC5  C9 07         CMP #$07
...
CD:0EE7  8E 91 CC      STX $CC91
CD:0EEA  8E 93 CC      STX $CC93
CD:0EED  8E 95 CC      STX $CC95
...
```

So the best safe reading is:

> `CD:0018 -> CD:0D28` = **optional selector-driven auxiliary fragment-stage initializer / expander** that seeds a descriptor list and clears/builds the `CA32/52/72` auxiliary work tables before the later service-04 decode/output path runs.

That is still one notch short of a final gameplay noun, but it is now a real stage identity instead of “mystery optional helper”.

---

## 4. Stronger noun for `2D00..`
Pass 77 called `2D00..` a packed fragment stream, which was directionally right but still loose.

This pass makes two harder points clear:

1. `C3:0002` materializes **packed bytes** into it
2. `CD:0015/002A` then build **six fixed row-sections** rooted at offsets `0C/0E/10/12/14/16`

So the strongest safe upgrade is:

> `2D00..` = **service-04 packed fragment-row stream workspace**

That is still structural, but it is better than a generic “opaque packed stream” description.

---

## 5. Practical impact on the late service-04 pipeline
With this pass, the front half of the service-04 common path now reads much more cleanly:

1. load mode-specific descriptor/profile bytes
2. `CD:0015` = build first four packed row-sections into `2D00..`
3. `CD:002A` = build last two packed row-sections into `2D00..`
4. optional `CD:0018` = seed/expand auxiliary fragment-stage work tables
5. `48EC` = parse segmented CE fragment-group stream into `A280/A2A0`
6. `C3:0002` = materialize packed row-stream bytes into `2D00..` and return output size
7. `4943` = decode packed fragment batches from `2D00..` into `4500..`
8. final slot seeding into `5D00..` with `A07B` active flags

That is not the end of the output-family story, but the pre-decode chain is now materially less fuzzy.

---

## Honest caution
What this pass **does not** claim:

1. I have **not** fully frozen the final player-facing noun of the downstream `4500.. -> 5D00..` object family.
2. I have **not** fully decoded all four local transform modes under `CD:13E6`; I only proved they are four distinct section-build/materialization modes.
3. I have **not** fully named the `CA32/52/72` auxiliary tables beyond their role as selector-driven auxiliary work tables.
4. I have **not** collapsed every inner variant of `C3:0557` into a perfect codec taxonomy; the strong proof here is the family role, WRAM-port output, and returned output size.

---

## Next seam after pass 78
The next clean seam is now:

1. decode the four local section-build transform modes under `CD:13E6`
2. tighten the final noun of the `CA32/52/72` auxiliary work tables seeded by `CD:0018`
3. keep pushing toward the final noun of the `4500.. / 5D00.. / A07B` output family now that the front-half pipeline is cleaner
