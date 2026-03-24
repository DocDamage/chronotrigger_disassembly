# Chrono Trigger Disassembly — Pass 81

## Scope of this pass
This pass continues directly from the pass-80 seam.

Pass 80 proved that token `0x80` inside the auxiliary `CD:0018` stream VM is not a normal one-step command.
It is a **secondary sub-dispatch** through `CD:2A51`.

The ugly gap left open was that the sub-op table still looked like a pile of unrelated handlers.
This pass closes the first solid chunk of that seam.

The honest result is:

> the `0x80` token does **not** open a full 32-way clean family.
> What is actually present in ROM is a **29-entry live sub-op band (`0x00..0x1C`)**,
> followed immediately by ordinary code bytes.
>
> The upper half of that band is now materially tighter:
> several entries are exact wrappers/latches,
> several are exact state/preset builders,
> and three entries (`0x00`, `0x0E`, `0x13`) are now clearly one family that seeds the parallel `BB06/BB07`, `BB86/BB87`, and `BC06/BC07` tables.

I still do **not** claim the final gameplay-facing noun of every affected WRAM table.
But the `0x80` extended token is no longer just “meta-dispatch”; it now has real internal shape.

---

## 1. the token-`0x80` secondary table is a **29-entry live sub-op table**, not a flat 32-entry clean block
The table reached by `CD:2A4A` starts at `CD:2A51`.

Parsing the little-endian pointers straight from ROM gives live targets for:

- sub-op `0x00` through `0x1C`

After that, the bytes stop behaving like pointer-table content and fall straight into ordinary code.
So the safest strong reading is:

> token `0x80` exposes a **29-entry extended sub-op family**, not a real fully-populated 32-entry namespace.

That matters because it keeps us from inventing fake “missing subcommands” out of adjacent code bytes.

---

## 2. the uppermost `0x80` sub-ops are now exact wrappers and latches
The tail end of the table turns out to be much cleaner than the middle.

### 2a. sub-op `0x18` = exact wrapper to `D1:E91A`
Entry `0x18` lands at `CD:2AA5`:

```text
22 1A E9 D1
60
```

So this sub-op is exactly:

- `JSL D1:E91A`
- `RTS`

### 2b. sub-op `0x19` = exact one-byte latch set on `CE10`
Entry `0x19` lands at `CD:2AA1`:

```text
EE 10 CE
60
```

So this sub-op simply increments `CE10` and returns.

That tightens the pass-80 picture immediately:

> token `0x80:19` is the clean setter/arm path for the `CE10` rewind gate later consumed by token `0xF6`.

### 2c. sub-op `0x1A` = exact wrapper to `D1:E899`
Entry `0x1A` lands at `CD:2A9C`:

```text
22 99 E8 D1
60
```

So this is another exact JSL wrapper.

### 2d. sub-op `0x1C` = exact wrapper to `D1:E8C1`
Entry `0x1C` lands at `CD:2A97`:

```text
22 C1 E8 D1
60
```

Again, exact wrapper.

### 2e. sub-op `0x1B` = 8-byte increment strip over `9FFA..`
Entry `0x1B` at `CD:2A8B` is tiny but not a wrapper:

```text
7B
AA
FE FA 9F
E8
E0 08 00
D0 F7
60
```

The exact structural behavior is:

- start from zeroed X
- increment `9FFA,X`
- walk eight consecutive byte positions
- return

So the safest strong label here is:

> sub-op `0x1B` increments an **8-byte counter/flag strip rooted at `7E:9FFA`**.

The final gameplay-facing noun of that strip still needs another pass.

---

## 3. sub-ops `0x15..0x17` are the first exact **E500/E850 table-control** family
These three entries are not wrappers.
They are the first place where the `0x80` extended band clearly reaches into a larger strided state table family.

### 3a. sub-op `0x15` = clear strided `E500/E502` pair table over a `0x06A0` span
Entry `0x15` lands at `CD:2AEF`.
It loops in 4-byte steps, zeroing:

- `7E:E500,X`
- `7E:E502,X`

until `X == 0x06A0`.

That is exact enough to state plainly:

> sub-op `0x15` clears a **strided pair-table family at `E500/E502`**.

### 3b. sub-op `0x16` = triple-call setup plus `E500 -= 0x10` where `E850` is live
Entry `0x16` lands at `CD:2AC6`.
Its structure is:

1. `JSR 2AAF` three times
2. walk the same strided table family
3. if `E850,X` is nonzero, subtract `0x0010` from `E500,X`

So the strongest safe reading is:

> sub-op `0x16` is an **E500/E850 linked table-update pass**:
> it runs a repeated setup helper and then decrements active `E500` entries by `0x10` where the companion `E850` marker is live.

I am intentionally leaving the final noun of the `E500/E850` tables open.

### 3c. sub-op `0x17` = wrapper to `D1:E984`, then local `CD3B`-driven follow-up
Entry `0x17` begins at `CD:2AAA`.
The first bytes are exact:

```text
22 84 E9 D1
60
```

but the live table target lands inside the wider local blob and the useful structural point is the surrounding follow-up:

- `D1:E984` is the shared setup helper here
- `CD3B` is incremented locally
- the follow-up walks a local lookup/copy path rather than simply returning to the stream VM

So the safest honest summary is:

> sub-op `0x17` is the **`D1:E984`-anchored local setup entry** for the same `E500/E850`-side family,
> but its exact downstream copy/lookup noun still wants a dedicated pass.

---

## 4. sub-ops `0x0F..0x14` are now a tight **state/preset-builder band**
This middle-high run turned out cleaner than expected.

### 4a. sub-op `0x0F` = exact indexed clear of `99B5`
Entry `0x0F` at `CD:2B5C` is tiny and exact:

```text
AD 00 CD
AA
9E B5 99
60
```

So it loads `CD00` into X and clears `99B5,X`.

### 4b. sub-op `0x10` = seed `E0` into the high-byte members of three parallel `BB/BC` arrays
Entry `0x10` at `CD:2B45` loops in 4-byte steps and writes `0xE0` into:

- `BB07,Y`
- `BB87,Y`
- `BC07,Y`

across the whole family.

So this is not random scratch mutation.
It is a real **parallel-table preset builder**.

### 4c. sub-op `0x11` = set `99D2.bit7` and mirror `99D3` around `0x80`
Entry `0x11` at `CD:2B27` is exact enough to freeze structurally.
It:

- sets `99D2 |= 0x80`
- copies `99D3` into `05A5` and `0599`
- stores `0x80 - 99D3` into `05A6` and `059A`

So the safest strong reading is:

> sub-op `0x11` seeds a **mirrored pair / complement pair** around the `0x80` midpoint while arming `99D2.bit7`.

### 4d. sub-op `0x12` = exact clamp of `5DA1` into `[0x31, 0xD4]`
Entry `0x12` at `CD:2B12` is also exact.
It forces `5DA1` into the closed byte range:

- minimum `0x31`
- maximum `0xD4`

That is a real upgrade because it proves `5DA1` is not unconstrained free scratch in this path.

### 4e. sub-op `0x14` = exact constant seeds for `CD3A` and `$007C`
Entry `0x14` at `CD:2B05` is tiny and exact:

- `CD3A = 0x0060`
- `$007C = 0x0040`

This is another hard preset token, not a general helper.

---

## 5. sub-ops `0x00`, `0x0E`, and `0x13` are one shared **BB/BC table seeding family**
These three entries were the nicest structural cleanup in the pass.

### 5a. shared tail at `2D53`
Entries:

- `0x00` -> `2D4A`
- `0x0E` -> `2D44`
- `0x13` -> `2D39`

all converge into the same tail beginning at `2D53`.

That tail writes parallel values into:

- `BB06/BB07`
- `BB86/BB87`
- `BC06/BC07`

with a repeated stride pattern.

So these are clearly not unrelated one-off commands.
They are one family.

### 5b. `0x0E` = fixed-width seed into the shared tail
Sub-op `0x0E` simply seeds `A = 0x04` and drops into the tail.

### 5c. `0x13` = arm `5D9A`, seed `A = 0x14`, then drop into the shared tail
Sub-op `0x13` first writes:

- `5D9A = 1`

then seeds `A = 0x14` and branches into the same shared builder.

### 5d. `0x00` = countdown-driven variant using `CD04`
Sub-op `0x00` is the most complex member.
It:

- clears `CD04`
- seeds `A = 0x04`
- consumes/updates `CD04`
- then runs the same `BB/BC` table-construction tail

So the safest strong family reading is:

> sub-ops `0x00`, `0x0E`, and `0x13` are a **shared parallel-table seed/builder family** over the `BB06/07`, `BB86/87`, and `BC06/07` arrays,
> with `0x13` adding a latch on `5D9A` and `0x00` adding a `CD04` countdown/variation path.

I am deliberately keeping the final gameplay-facing noun of those three `BB/BC` array families one notch below frozen.

---

## 6. strongest safe upgrades from this pass
The safest new top-level conclusions are:

1. token `0x80` really exposes **29 live sub-ops (`0x00..0x1C`)**
2. sub-ops `0x18`, `0x1A`, and `0x1C` are exact wrappers into the `D1:E8xx/E9xx` helper neighborhood
3. sub-op `0x19` is the clean setter for the later `CE10` rewind gate
4. sub-op `0x1B` increments an exact **8-byte strip rooted at `9FFA`**
5. sub-ops `0x15..0x17` are the first concrete **E500/E850 strided table-control family**
6. sub-ops `0x0F..0x14` are a real **state/preset-builder band**
7. sub-ops `0x00`, `0x0E`, and `0x13` are one shared **BB/BC parallel-table builder family**

That is a real semantic upgrade. The `0x80` token is no longer just “the token that opens a mystery table.”
It now has recognizable internal bands.

---

## 7. honest caution
I am **not** claiming all of these nouns are final.
Still open:

- exact gameplay-facing noun of the `E500/E850` strided families
- exact gameplay-facing noun of the `BB06/07`, `BB86/87`, `BC06/07` parallel tables
- exact downstream identity of the `D1:E899`, `D1:E8C1`, `D1:E91A`, and `D1:E984` helpers
- whether `9FFA..A001` is counters, phase bytes, or another 8-byte scheduler strip
- how this `0x80` extended-family state ties back into the final `4500 -> 5D00 -> A07B` emit path

But the structural proof is now strong enough that those next passes can work from real bands instead of one giant undifferentiated command table.
