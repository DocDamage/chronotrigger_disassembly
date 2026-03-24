# Chrono Trigger Disassembly — Pass 90

## Scope of this pass
Pass 89 froze the local D1 write-side mechanics around `EDCD..F107`, but it still left the
most important caller-side question open:

- what is the exact higher-level local routine that seeds this whole lane/raster workspace?
- how are the `CA5A / CA5C` center-side inputs actually staged?
- what exact helper is built immediately before the `CD:0235 / C0:0008` follow-up chain?

This pass closes that caller-contract seam materially.

The strongest keepable result is:

> `D1:F331..F410` is a real **local seed/reset + follow-up invoke orchestrator** for the same
> lane/raster workspace tightened in passes 88 and 89.
>
> It:
> - clears local state bytes at `C861 / C862`
> - seeds `CD46` from `2A21.bit0`
> - seeds a fixed group of `BE..`, `CA..`, `C0..`, and `C14F/150` locals
> - snapshots the 8 descriptor headers through the already-frozen `F411`
> - seeds exact `BEAB/BEAD` and `BF6B/BF6D` stepped table families
> - fills `C161` and `C4E1` with `0x00FF`
> - clears `BB05`
> - copies `2030..203E` into `CCEE..CCFC`
> - then invokes the exact four-stage tail:
>   `CE:EE6E -> D1:F83D -> CD:0235 -> C0:0008`
> - and finally increments `CAD3`

That is enough to stop treating the pass-89 builder as a locally-floating blob.

---

## 1. `D1:F331..F410` is the missing local orchestrator
The routine begins by clearing two exact local bytes:

```text
D1:F331  STZ $C861
D1:F334  STZ $C862
```

Then it derives `CD46` from live state byte `2A21.bit0`:

```text
LDA $2A21
AND #$01
BEQ +
LDA #$FD
+ STA $CD46
```

So this is the first exact non-token seed path for `CD46`.

It then seeds a fixed local constant set:

```text
C14F = 0x09
C150 = 0x00
BEA1 = 0x0077
BEA9 = 0x0077
BEA5 = 0xFFDF
CA04 = 0xFF27
CA08 = 0x00D7
CA0C = 0x00D7
CA10 = 0x000D
CA14 = 0x00BD
C02B = 0x0505
C02D = 0x0505
```

Then it immediately calls the already-frozen descriptor-header snapshot helper:

```text
JSR D1:F411
```

### exact stepped-table seed block
With `REP #$20`, it seeds two exact stepped families in `X += 4` steps.

The first family:

- clears `BEAB,X`
- clears `BF6B,X`
- stores the current word in `$55` to `BEAD,X`
- stores `$55 - 0x0098` to `BF6D,X`

The control shape is exact:

- inner group count starts at `0x0013`
- when that group count expires, `$55 += 0x0004`
- the next group begins with count `0x000C`
- loop stops when `X == 0x00C0`

I am still keeping the final gameplay-facing noun of those `BE.. / BF..` families below frozen,
but the seed contract is now exact.

### exact primary/shadow fill block
The routine then fills both:

- `C161 + X`
- `C4E1 + X`

with `0x00FF`, for `X = 0, 2, 4, ...` until `X == 0x0380`.

That is the first exact local whole-workspace seed for one primary/shadow pair inside the
pass-88 raster-target neighborhood.

### exact clear/copy follow-up block
It then:

- clears `BB05 + X` for `X = 0, 2, 4, ...` until `X == 0x0180`
- copies 8 exact words from `2030..203E` into `CCEE..CCFC`

### exact four-stage tail
Finally it runs this exact sequence:

```text
SEP #$20
LDA #$08
JSL CE:EE6E
JSL D1:F83D
JSL CD:0235
PHB / PHD / PHP
JSL C0:0008
PLP / PLD / PLB
TDC
INC $CAD3
RTL
```

### strongest safe reading
> `D1:F331..F410` is an exact **local seed/reset + four-stage follow-up invoke orchestrator**
> for the same primary/shadow lane and raster-target workspace tightened in passes 88 and 89.

That is the missing caller contract pass 89 explicitly left open.

---

## 2. `D1:F83D..F8EA` is an exact quartet-table seed helper
Pass 89 knew `D1:F331..F410` called `D1:F83D`, but the helper itself was still unnamed.
It is now exact enough to freeze structurally.

### exact behavior
The routine first clears `C02F..C14E` across an exact `0x0120`-byte span.

Then it builds two stepped quartet families.

#### first quartet family
For `X = 0, 4, 8, ...` until `X == 0x0060`, it writes:

- `C031,X` = high byte of a running word seeded from `E8AB`
- `C091,X` = high byte of a running word seeded from `E055`
- `C090,X` = `0x81`
- `C030,X` = `0x01`

After each record, the running first word is decremented by `0x0055` and the second running word
is incremented by `0x0055`.

#### second quartet family
Then for `X = 0, 4, 8, ...` until `X == 0x0030`, it writes:

- `C0F1,X` = high byte of a running word seeded from `E056`
- `C121,X` = high byte of a running word seeded from `E0AA`
- `C120,X` = `0x81`
- `C0F0,X` = `0x01`

After each record, the first running word is decremented by `0x00AA` and the second is
incremented by `0x00AA`.

#### exact tail sentinels
At the end it seeds:

- `C0ED = 0xE0`
- `C14D = 0xE0`
- clears `C0EB / C0EC / C0EE / C14B / C14C / C14E`

### strongest safe reading
> `D1:F83D..F8EA` is an exact **quartet-table seed helper** for the `C030..C14F` local family,
> immediately upstream of the `CD:0235 / C0:0008` follow-up path.

I am still keeping the final gameplay-facing noun of that table family one notch below frozen.

---

## 3. `D1:F474..F4BF` is the missing `CA5A / CA5C` input stager
Pass 89 proved that `EEC5..F107` builds center words from:

- `CA5A + CA5E`
- `CA5C + CA60`

but the write-side seed for `CA5A / CA5C` was still open.
This pass freezes it.

### tiny exact helper: `D1:F474..F47B`
This helper is exact:

```text
ADC $7C
TAX
LDA C0:FE00,X
RTS
```

So it is a pure lookup helper over table `C0:FE00`, indexed by `(A + 7C)`.

### exact staging routine: `D1:F47C..F4BF`
The caller then does this exactly:

1. `Y = 2`, read `[$40],Y` into local byte `49`
2. call `F474`
3. `AND 49`
4. `ADC [40]`
5. store result in local byte `45`
6. `Y = 1`, call `F474` again from `[$40],Y`
7. `AND 49`
8. `ADC [$40],Y`
9. store result in local byte `47`
10. load runtime slot index from `43`
11. with `REP #$20`, store:
    - `CA5A,X = -(45 & 0x00FF)`
    - `CA5C,X = -(47 & 0x00FF)`
12. advance stream pointer `40` by 2
13. `RTL`

### strongest safe reading
> `D1:F47C..F4BF` is an exact **masked-pair stager** that writes the negated `CA5A / CA5C`
> seed words later consumed by the pass-89 primary curve/profile writer.

This is the missing input-side half of the `CA5A..CA60` choreography.

---

## 4. What materially changes after this pass
Before pass 90, the project knew the **local writer mechanics** and the **local mirror helpers**,
but not the missing caller contract tying them together.

After this pass, the local chain is materially tighter:

1. `D1:F331..F410` seeds and resets the lane/raster workspace and invokes the exact four-stage tail.
2. `D1:F83D..F8EA` seeds the local `C030..C14F` quartet table family just before `CD:0235 / C0:0008`.
3. `D1:F47C..F4BF` seeds the missing `CA5A / CA5C` center-offset words.
4. `D1:EEC5..F107` then consumes `CA5A..CA60` to build the first four primary lanes.
5. Pass 88’s mirror helpers still sit downstream of that build side.

That is enough to justify a stronger “local build pipeline” reading without pretending we already
know the final gameplay-facing presentation noun.

---

## 5. Keepable conclusions from pass 90
1. `D1:F331..F410` is the first exact higher-level caller contract for the pass-89 writer cluster.
2. `CD46` now has an exact non-token seed path from `2A21.bit0`.
3. `D1:F83D..F8EA` is an exact quartet-table seed helper for `C030..C14F`.
4. `D1:F474..F47B` is an exact `C0:FE00` lookup helper indexed by `(A + 7C)`.
5. `D1:F47C..F4BF` is the exact staging path for the missing `CA5A / CA5C` seed words.
6. The local `CA5A..CA60` choreography is no longer vague: `F47C` seeds one pair and pass 89’s
   `EEC5..F107` consumes the combined pair-sums.

---

## Honest caution kept explicit
Even after this pass:

- I have **not** frozen the final gameplay-facing noun of the `C030..C14F` quartet family.
- I have **not** frozen the final gameplay-facing noun of the pass-88/89 lane+raster workspace.
- I have **not** frozen the exact roles of the external follow-up stages `CE:EE6E`, `CD:0235`, or `C0:0008`.
- I have **not** frozen the first exact clean-code external reader of `CE0F`.

---

## Best next seam
Do **not** go broad.

The best next move now is:

1. freeze `CE:EE6E` as the first exact external follow-up stage in the new local orchestrator tail
2. freeze `CD:0235` and then `C0:0008` for the same tail
3. only then decide whether the `C030..C14F` quartet family deserves promotion to a stronger
   table/upload noun
4. return to `CE0F` only after that local pipeline noun is tighter
