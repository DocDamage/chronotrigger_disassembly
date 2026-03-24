# Chrono Trigger Disassembly — Pass 112

## Purpose

Pass 111 froze what `C0:F05E` does with local selector byte `7E:0163`, but it left the honest ownership question open:

1. who actually writes `0163`
2. how do the live `0..3` selector values get materialized
3. what exact role do nearby locals `0164/0165/0166` play in that writer chain

This pass stayed narrow and only promoted what the bytes justify.

---

## 1. The reset / forced-state writers of `0163` are now exact

### A. Startup/local-reset path forces `63 = 0x80`

The entry at `C0:0BC0` is real code and contains the exact local reset:

```text
C0:0BE6  64 62
C0:0BE8  A9 80
C0:0BEA  85 63
```

So the local family is explicitly reset to:

- `62 = 00`
- `63 = 80`

This matches pass 111's already-frozen meaning of negative `63`:

> caller `ED15` skips the `F05E` four-band prelude when `63` is negative.

So `0x80` is no longer just “what fell out of `F05E` once.”  
It is an exact forced/reset state for the selector family.

### B. `F05E` default-restore path also forces `63 = 0x80`

Pass 111 already froze the tail:

```text
C0:F082  2B
C0:F083  A9 80
C0:F085  85 63
C0:F087  60
```

Together with `0BC0`, that means there are now **two exact forced-state writers** of `63`:

- startup/local reset -> `63 = 0x80`
- default four-band restore tail -> `63 = 0x80`

That materially sharpens the ownership story.

---

## 2. `C0:1AFB..1B18` is the exact helper that saves the current live selector and forces default state `4`

This range has real callsites and clean code:

```text
C0:1AFB  A5 63
C0:1AFD  30 0A
C0:1AFF  C9 04
C0:1B01  F0 06
C0:1B03  85 66
C0:1B05  A9 04
C0:1B07  85 63
C0:1B09  AD F6 00
C0:1B0C  89 80
C0:1B0E  F0 05
C0:1B10  A2 00 00
C0:1B13  86 34
C0:1B15  60
```

Exact behavior:

1. loads `63`
2. if `63` is negative, skip the save/force block
3. if `63 == 4`, skip the save/force block
4. otherwise:
   - save old `63 -> 66`
   - force `63 = 4`
5. then checks `00F6.bit7`
6. if that bit is set, clears local word `34`

The strongest safe reading is:

> **`C0:1AFB..1B18` saves the current nonnegative/non-4 selector into `66`, then forces selector `63` into exact state `4`, with one local side effect on `34` gated by `00F6.bit7`.**

That matters because pass 111 had already proved that `F05E` treats non-`0..3` nonnegative values as the default-restore path.  
This helper is now the clean bridge between those two facts.

---

## 3. `C0:1B1A..1B2A` is the exact increment-with-wrap writer for `63`

```text
C0:1B1A  A5 63
C0:1B1C  1A
C0:1B1D  C5 65
C0:1B1F  F0 02
C0:1B21  B0 03
C0:1B23  85 63
C0:1B25  60
C0:1B26  A5 64
C0:1B28  80 F9
```

Exact behavior:

- starts from `A = 63 + 1`
- compares that value against `65`
- if result `<= 65`, stores it into `63`
- if result exceeds `65`, loads `64` and stores that into `63`

So this helper is exactly:

> **increment `63` and wrap back to `64` when the increment would move beyond inclusive upper bound `65`.**

That is the first exact, validated path explaining how live nonnegative selector values are produced **without** direct immediate stores to `0..3`.

---

## 4. `C0:1B2B..1B37` is the exact decrement-with-wrap writer for `63`

```text
C0:1B2B  A5 63
C0:1B2D  F0 05
C0:1B2F  3A
C0:1B30  C5 64
C0:1B32  B0 F0
C0:1B34  A5 65
C0:1B36  80 EC
```

Exact behavior:

- if `63 == 0`, it immediately loads `65`
- otherwise decrements `63`
- if decremented value is still `>= 64`, stores it into `63`
- if decremented value falls below `64`, loads `65` and stores that instead

So this helper is exactly:

> **decrement `63` and wrap back to `65` when the decrement would move below inclusive lower bound `64`.**

Together, `1B1A` and `1B2B` close the live range mechanics.

---

## 5. Therefore `64` and `65` are exact inclusive wrap bounds for the `63` selector family

The two helper bodies above prove the local meanings cleanly:

- `64` = inclusive lower bound used when increment-wrap overflows
- `65` = inclusive upper bound used when decrement-wrap underflows and when increment compares for overflow

Even before freezing the broader subsystem noun, their local role is now exact enough to promote.

---

## 6. `66` is the exact saved pre-force selector byte

`66` is written only on the `1AFB` save/force path:

```text
C0:1B03  85 66
```

And that write happens only when:

- old `63` is nonnegative
- old `63` is not already `4`

So `66` is not an arbitrary scratch byte here.  
Its exact local job is:

> **saved prior selector value, captured immediately before forcing `63 = 4`.**

I did **not** yet freeze the global restore consumer of `66`, but the save side is now exact.

---

## 7. Honest constraint: the broad owner noun is still not frozen

I also checked the nearby packed-bound materialization evidence block:

```text
C0:367C  BF 01 20 7F
C0:3680  85 2A
C0:3682  E8
C0:3683  BF 01 20 7F
C0:3687  85 D9
C0:3689  29 03
C0:368B  85 65
C0:368D  A5 D9
C0:368F  4A
C0:3690  4A
C0:3691  29 03
C0:3693  85 64
C0:3695  A9 01
C0:3697  85 62
```

This is strong evidence that one nearby helper splits a packed byte into two exact 2-bit fields:

- low 2 bits -> `65`
- high 2 bits -> `64`
- then seeds `62 = 1`

That is useful, but I did **not** promote the surrounding routine yet because its exact entry/caller chain still wants a cleaner freeze than the three helper bodies above.

So the honest architectural statement after this pass is:

- `63` ownership is now much tighter locally
- the exact **subsystem noun** of the `62/63/64/65/66` family still wants one more caller-side pass

---

## 8. What this pass closes from pass 111

Pass 111 asked the sharp question:

> who writes `63` to the exact `0..3` selector values before `ED15` runs?

The answer is now:

- no validated direct immediate writer to `0..3` was needed
- the live selector values are produced by **increment/decrement wrap helpers** over an exact local inclusive range `[64..65]`
- `63 = 4` is an exact forced/default state
- `63 = 0x80` is an exact reset/skip state
- `66` is the saved prior nondefault selector
- `64/65` are the exact local wrap bounds

That is a real seam closure.

---

## 9. Labels justified this pass

- `C0:1AFB..1B18` -> exact save-and-force-default helper for `63`
- `C0:1B1A..1B2A` -> exact increment-with-wrap helper for `63`
- `C0:1B2B..1B37` -> exact decrement-with-wrap helper for `63`
- `7E:0164` -> local inclusive lower wrap bound for selector `63`
- `7E:0165` -> local inclusive upper wrap bound for selector `63`
- `7E:0166` -> saved pre-force selector byte

I intentionally did **not** over-promote `7E:0162` yet.

---

## 10. Remaining live seam

The next honest seam is no longer “who writes `63` at all.”  
It is:

1. freeze the exact caller/entry chain that seeds `64/65` from the packed `7F:2001+X` byte
2. trace the restore/consumer side of saved byte `66`
3. then decide whether the `62/63/64/65/66` family can safely be promoted from “local selector/range mechanics” into a broader subsystem noun
