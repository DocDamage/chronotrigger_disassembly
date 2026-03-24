# Chrono Trigger Disassembly — Pass 87

## Scope of this pass
Pass 86 proved that `CD0D..CD1B` was a real four-point work bundle,
but it still left the `D1:F8EB / F91C / F972 / F9AF / F9E7` cluster too fuzzy.

This pass closes that cluster.

The main correction is important:

> the downstream helper family is **column-oriented**, not scanline-oriented.
>
> The four point pairs are sorted by their **second byte**,
> and the WRAM-port seed helper uses that same byte to choose the target column address.

That means the cleanest keepable reading is now:

- the work bundle at `CD0D..CD1B` is a **four `(row,column)` point-pair bundle**
- `D1:F8EB` sorts those four pairs by **column/X** ascending
- `D1:F91C` computes four signed **row/Y-per-column** edge steps
- `D1:F9E7` rasterizes the sorted bundle column by column into a WRAM-port-selected buffer
- `CD:38B2` seeds that WRAM port target from the start column plus two selector bits

This also corrects one local axis assumption from pass 86:

> for the `EC28 -> F9AF` path, the strongest current local reading is now
> `5DA0 = row/Y-like` and `5DA1 = column/X-like`, not the other way around.

I am keeping that axis correction local to this path until more consumers prove it globally.

---

## 1. `D1:F8EB..F91B` is an exact in-place sort of four point pairs by the second byte
The exact body is a four-pass bubble-sort-style loop:

```text
LDA #$04
PHA
loop:
  LDA $13 : CMP $15 : BCC +swap_skip_0
    swap $12 <-> $14
  LDA $15 : CMP $17 : BCC +swap_skip_1
    swap $14 <-> $16
  LDA $17 : CMP $19 : BCC +swap_skip_2
    swap $16 <-> $18
  PLA
  DEC A
  BNE loop
RTS
```

The key detail is exact:

- the compare keys are `13 / 15 / 17 / 19`
- the paired values swapped with them are `12 / 14 / 16 / 18`

So this helper does **not** treat the first byte of each pair as the sort key.
It treats the **second byte** as the key and keeps the first byte paired with it.

### strongest safe reading
This is an exact structural freeze:

> `D1:F8EB..F91B` sorts four `(row,column)`-style pairs by the **column/X byte** ascending.

That is the correction that unlocks the rest of the cluster.

---

## 2. `D1:F972..F9AE` is the signed edge-step helper using hardware divide
This helper is exact enough now to stop being generic arithmetic fog.

Its inputs are staged in direct page as:

- `0B` = endpoint row/Y byte B
- `0C` = endpoint row/Y byte A
- `0D` = column/X delta

Then it:

- computes `0B - 0C`
- takes the absolute magnitude when negative
- writes the dividend/divisor into `4204/4206`
- reads the quotient from `4214`
- restores the sign when needed
- returns the signed result in `Y`

### strongest safe reading
> `D1:F972..F9AE` computes a signed **row/Y step per column/X** from one edge segment.

It is the reusable slope helper for the rasterizer.

---

## 3. `D1:F91C..F971` computes four signed edge steps for the four-point bundle
Once the bundle is interpreted as four `(row,column)` pairs,
this helper becomes clean.

It stages four exact edge calculations and stores the returned signed steps in:

- `03` from edge `(12,13) -> (16,17)`
- `05` from edge `(16,17) -> (18,19)`
- `07` from edge `(12,13) -> (14,15)`
- `09` from edge `(14,15) -> (18,19)`

Because `F972` is now frozen,
these are not generic “deltas” anymore.
They are signed **row-per-column edge steps**.

### strongest safe reading
> `D1:F91C..F971` computes the four signed edge-step values for one sorted four-point work bundle,
> storing them in local direct-page slope slots `03 / 05 / 07 / 09`.

---

## 4. `CD:38B2..38E3` seeds the WRAM-port address for one column-raster target
The exact entry stub is:

```text
CD:38B2  JSR $38B6
CD:38B5  RTL
```

The real helper at `CD:38B6..38E3` does this exactly:

- takes the incoming `A` value and multiplies it by `4`
- masks `7C.bit0`
- masks `7E:CC64.bit0`
- combines those two selector bits into a 0..3 table index
- reads one 16-bit base from `CD:38AA..38B1`
- adds the `column * 4` offset
- writes the result to `2181`
- writes bank `7E` to `2183`

The exact four-word base table is:

- `CD:38AA = C161`
- `CD:38AC = C163`
- `CD:38AE = C4E1`
- `CD:38B0 = C4E3`

### strongest safe reading
> `CD:38B2..38E3` seeds the WRAM data-port address for one of **four interleaved column-raster target strips**,
> selected by `7C.bit0` and `CC64.bit0`, at `7E:C161 / C163 / C4E1 / C4E3` plus `column * 4`.

That is why the downstream writer is column-oriented.

---

## 5. `D1:F9AF..F9E6` is the wrapper/dispatcher for the column rasterizer
This helper is now exact in structure:

- `TXA ; STA $CC64`
- loads `CD0D..CD1B` into direct-page work slots `12..19`
- calls `D1:F8EB` to sort the four pairs by column
- temporarily sets `DB = 00`
- calls `D1:F9E7`
- restores the previous bank and returns long

### strongest safe reading
> `D1:F9AF..F9E6` is the D1-side dispatcher that loads one four-point work bundle,
> records the raster-target selector in `CC64`, sorts the points by column,
> and hands them off to the column-rasterizer.

---

## 6. `D1:F9E7..FB67` rasterizes the sorted four-point bundle in three exact cases
This helper is no longer generic geometry fog.

It has three exact branches.

### case A: equal first two column bytes
When `13 == 15`, it normalizes the row ordering within the first shared-column pair,
and within the last shared-column pair, then jumps to one single-run emitter.

That emitter:

- calls `F91D`
- calls `CD:38B2` with the start column in `0F`
- uses one exact column count in `45`
- advances two running row values with the signed steps in `03` and `09`
- writes the paired row values through the WRAM port for each column

### case B / case C: non-equal first two column bytes
When `13 != 15`, it compares the middle row bytes `16` and `14` and chooses one of two three-run emitters.
One path uses the run schedule:

- `45` columns with steps `03` and `07`
- `47` columns with steps `03` and `09`
- `49` columns with steps `05` and `09`

The other path uses:

- `45` columns with steps `03` and `07`
- `47` columns with steps `05` and `07`
- `49` columns with steps `05` and `09`

All three emitters:

- call `CD:38B2` first to seed the WRAM-port address from the start column
- keep two running row accumulators in `X` and `Y`
- update them by signed per-column edge steps
- write paired row values column by column into the selected WRAM target strip

### strongest safe reading
> `D1:F9E7..FB67` is a real three-case **column rasterizer** for the sorted four-point work bundle.
>
> It emits paired row/Y values for each column/X into one of four WRAM-port-selected target strips.

---

## 7. this tightens `CD0D..CD1B` and corrects the local axis reading for `5DA0 / 5DA1`
Pass 86 already proved that `EC28` builds four endpoint pairs and sends them to `F9AF`.
Pass 87 explains what `F9AF` actually does with them.

That is enough to freeze a much better noun for `CD0D..CD1B`:

> `CD0D..CD1B` is a **four `(row,column)` point-pair work bundle** consumed by the D1 column-rasterizer.

And because `EC28` writes:

- transformed values into the **first** byte of the first two pairs
- `5DA0 +/- 0x10` into the **first** byte of the second two pairs
- `5DA1` into the **second** byte of the second two pairs

while `F8EB` sorts by the **second** byte and `CD:38B2` seeds a **column** address from that same byte,
the local path-level correction is now strong:

> for the `EC28 -> F9AF` path,
> `5DA0` is the stronger **row/Y-like** byte,
> and `5DA1` is the stronger **column/X-like** byte.

I am still keeping that correction local to this path until another consumer freezes it globally.

---

## 8. strongest keepable conclusions from pass 87
1. `D1:F8EB..F91B` sorts four point pairs by their **second byte** ascending.
2. That second byte is the **column/X** byte for this rasterizer path.
3. `D1:F972..F9AE` computes a signed **row-per-column** step using hardware divide.
4. `D1:F91C..F971` computes the four edge-step values for the four-point bundle.
5. `D1:F9AF..F9E6` loads `CD0D..CD1B`, saves the target selector to `CC64`, sorts the points, and dispatches the rasterizer.
6. `D1:F9E7..FB67` is a real three-case **column rasterizer**.
7. `CD:38B2..38E3` seeds the WRAM-port address for one of four interleaved column-raster target strips using `7C.bit0`, `CC64.bit0`, and `column * 4`.
8. `CD0D..CD1B` is best described now as a **four `(row,column)` point-pair work bundle** for the D1 rasterizer.
9. The strongest local correction for the `EC28 -> F9AF` path is now `5DA0 = row/Y-like`, `5DA1 = column/X-like`.

---

## Honest caution
Even after this pass:

- I have **not** frozen the final gameplay/presentation noun of the four-point bundle. It is clearly rasterized, but I am not yet locking it as “sprite quad”, “window mask quad”, or another final noun without one more downstream producer/consumer pair.
- I have **not** frozen the final higher-level noun of the four WRAM target strips at `7E:C161 / C163 / C4E1 / C4E3`.
- I have **not** frozen the first exact external reader of `CE0F`.
- I have **not** promoted the remaining low-half `CE0F` code-like hits, because they still sit inside dense script/data neighborhoods and are not yet clean enough to trust.

---

## Next recommended target
The cleanest next seam after pass 87 is:

1. identify the exact higher-level owner of the four WRAM target strips rooted by `CD:38AA..38B1`
2. find the first exact downstream consumer of the column-raster output at `7E:C161 / C163 / C4E1 / C4E3`
3. then come back to the `CE0F` external-reader seam with stricter confidence filters
