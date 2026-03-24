# Chrono Trigger Disassembly — Pass 82

## Scope of this pass
This pass continues directly from the pass-81 seam.

Pass 81 proved that token `0x80` inside the optional `CD:0018` auxiliary VM reaches four exact long-call wrappers:

- `0x17 -> D1:E984`
- `0x18 -> D1:E91A`
- `0x1A -> D1:E899`
- `0x1C -> D1:E8C1`

The ugly remaining gap was that those `D1:E8xx/E9xx` targets still had no real nouns.
This pass closes that gap.

The honest result is:

> the high `0x80` sub-ops are not generic helper escapes.
> They are a **palette-band control cluster**.
>
> More specifically, they clear, seed, copy, and bias exact WRAM palette-band tables
> and exact **3-record palette/effect descriptor slabs** that sit right next to the already-proven `0520` descriptor system from passes 8–9.

I am still **not** freezing the final player-facing noun of every `20xx/21xx/22xx/23xx` band.
But these helpers are now concrete enough to stop calling them opaque wrappers.

---

## 1. pass-81 caution on sub-op `0x17` can now be tightened
Pass 81 kept some caution around token `0x80:17` because the bytes after `CD:2AAA` looked like they belonged to the same entry.

That is too loose.

The live pointer-table entry for sub-op `0x17` lands exactly at `CD:2AAA`, and the live body is exactly:

```text
22 84 E9 D1
60
```

So sub-op `0x17` is simply:

- `JSL D1:E984`
- `RTS`

The local code at `CD:2AAF..` is **not** part of sub-op `0x17`.
It is the shared setup helper used by sub-op `0x16`.

That is a real cleanup because it means the whole `0x17/0x18/0x1A/0x1C` tail is now a clean wrapper cluster.

---

## 2. `D1:E899` and `D1:E8C1` are exact sentinel-fill helpers for palette-band tables
These two routines are small and exact.

### 2a. `D1:E899` fills `2040/2240` and `2120/2320` with `0x7FFF`
Disassembly shape:

```text
TDC
TAX
REP #$20
LDA #$7FFF
loop A:
  STA $2040,X
  STA $2240,X
  INX
  INX
  CPX #$00C0
  BNE loop A

LDX #$0000
loop B:
  STA $2120,X
  STA $2320,X
  INX
  INX
  CPX #$0060
  BNE loop B

TDC
SEP #$20
RTL
```

So this helper does two exact fills:

- `7E:2040..20FF`
- `7E:2240..22FF`

and then:

- `7E:2120..217F`
- `7E:2320..237F`

all with the 16-bit sentinel `0x7FFF`.

That is not generic scratch clearing.
It is a very deliberate **max-value palette-band/table fill**.

### 2b. `D1:E8C1` fills `21A0/23A0` with the same sentinel
This is the smaller sibling:

```text
TDC
TAX
REP #$20
LDA #$7FFF
loop:
  STA $21A0,X
  STA $23A0,X
  INX
  INX
  CPX #$0060
  BNE loop
TDC
SEP #$20
RTL
```

So token `0x80:1C` is the precise fill helper for:

- `7E:21A0..21FF`
- `7E:23A0..23FF`

again with `0x7FFF`.

### 2c. strongest safe reading
The safest keepable conclusion is:

> sub-ops `0x1A` and `0x1C` are not abstract VM escapes.
> They initialize exact **paired palette-band work tables** to a saturated sentinel value.

I am deliberately keeping the final role of each band one notch below frozen.
But the table mechanics are exact now.

---

## 3. `D1:E91A` is a promote/copy helper for one 48-color band plus a 3-record descriptor slab
This routine is the strongest upgrade in the pass.

Its first half is exact:

```text
REP #$20
TDC
TAX
loop A:
  LDA $2040,X
  STA $20A0,X
  STA $22A0,X
  STZ $2040,X
  STZ $2240,X
  INX
  INX
  CPX #$0060
  BNE loop A
```

So `D1:E91A` copies the **first `0x60` bytes** (48 words / 48 colors) from `2040` into:

- `20A0`
- `22A0`

and clears the source pair at:

- `2040`
- `2240`

That is already a real band move, not a vague helper.

### 3a. it then copies `0544..0567` back into `0520..0543`
After dropping to 8-bit A, the routine does:

```text
TDC
TAX
loop B:
  LDA $0544,X
  STA $0520,X
  INX
  CPX #$24
  BNE loop B
```

That is an exact `0x24`-byte copy:

- source: `7E:0544..0567`
- destination: `7E:0520..0543`

`0x24` bytes is exactly **three 12-byte records**.

That lines up directly with passes 8–9, which already proved that `0520 + n*0C` is a palette/effect descriptor record family.
So this pass can safely tighten the local noun:

> `0520..0543` and `0544..0567` are two adjacent **3-record descriptor slabs** belonging to the same palette/effect subsystem.

### 3b. it biases the `+1` byte of each descriptor by `+0x30`
After the copy, the routine adds `0x30` to:

- `0521`
- `052D`
- `0539`

Those are exactly the `+1` bytes of the three copied 12-byte records.

### 3c. it seeds three type/control bytes with `0x30`
It then writes `0x30` to:

- `0520`
- `052C`
- `0538`

which are the first bytes of the same three 12-byte records,

and also to:

- `CD2F`
- `CD30`
- `CD31`

### 3d. it clears the next control trio and `CDC8`, then increments `CE12`
The tail is exact:

```text
STZ $CD32
STZ $CD33
STZ $CD34
STZ $CDC8
INC $CE12
RTL
```

### 3e. strongest safe reading
The safest strong reading is:

> `D1:E91A` promotes one 48-color paired palette band out of `2040/2240` into `20A0/22A0`,
> clears the source band,
> copies the secondary 3-record palette/effect descriptor slab `0544..0567` back into the active slab `0520..0543`,
> seeds all three active record headers to `0x30`,
> resets the `CD32..34 / CDC8` side state,
> and raises `CE12`.

I am still leaving the final human noun of the `+1` byte and the `CD2F..34` bytes open.
But structurally this is now a real **promote-and-arm** helper.

---

## 4. `D1:E984` is the complementary seed/snapshot helper
The sibling routine at `D1:E984` is the other half of the same story.

Its exact head is:

```text
INC $CDC8
INC $CE0F
REP #$20
TDC
TAX
loop A:
  LDA.l $D0FD00,X
  STA $2040,X
  STA $2240,X
  INX
  INX
  CPX #$0060
  BNE loop A
```

So before doing anything else it:

- increments `CDC8`
- increments `CE0F`
- copies a fixed 48-word ROM table from `D0:FD00` into both:
  - `2040`
  - `2240`

That is the exact opposite of a mystery wrapper.

### 4a. `D0:FD00` is an exact 48-word seed block
ROM inspection shows that `D0:FD00..FD5F` is the exact table consumed here.
It is neither compressed nor computed locally.

So the strongest safe reading is:

> `D0:FD00..FD5F` is the ROM-side **palette-band seed block** used by token `0x80:17`.

### 4b. it then snapshots `0520..0543` outward into `0544..0567`
After returning to 8-bit A, the routine copies the same exact `0x24`-byte slab in the other direction:

```text
TDC
TAX
loop B:
  LDA $0520,X
  STA $0544,X
  INX
  CPX #$24
  BNE loop B
```

So unlike `E91A`, this one snapshots the active descriptor slab outward.

### 4c. it biases the `+1` byte of each copied descriptor by `-0x30`
It subtracts `0x30` from:

- `0545`
- `0551`
- `055D`

again the `+1` byte of each 12-byte record.

### 4d. it seeds three 16-bit fields with `0x0100`
It then writes `0x0100` to:

- `0548`
- `0554`
- `0560`

which are the `+4` fields of the same three records.

### 4e. it seeds the secondary slab and `CD32..34` with `0x30`, then increments `CE12`
The tail then writes `0x30` to:

- `0544`
- `0550`
- `055C`
- `CD32`
- `CD33`
- `CD34`

and finally increments `CE12`.

### 4f. strongest safe reading
The safest strong reading is:

> `D1:E984` seeds the working 48-color band at `2040/2240` from a fixed ROM block at `D0:FD00`,
> snapshots the active 3-record descriptor slab `0520..0543` into the secondary slab `0544..0567`,
> biases the copied records in the opposite direction from `E91A`,
> seeds three `+4` word fields to `0x0100`,
> arms `CD32..34`,
> and raises both `CDC8/CE0F` before incrementing `CE12`.

That is a real complementary **seed-and-snapshot** helper.

---

## 5. these four sub-ops now read as one coherent palette-band control cluster
With the D1 targets decoded, the upper `0x80` sub-op tail now has real internal shape:

- `0x17 -> D1:E984`
  - seed first working palette band from ROM
  - snapshot active descriptor slab outward
  - arm `CDC8/CE0F/CE12`

- `0x18 -> D1:E91A`
  - move first working palette band into the promoted/latched pair
  - copy the secondary descriptor slab back into the active slab
  - arm `CE12` while clearing `CDC8`

- `0x1A -> D1:E899`
  - fill several paired palette-band tables with `0x7FFF`

- `0x1C -> D1:E8C1`
  - fill one more paired palette-band table with `0x7FFF`

That is no longer “some wrappers plus unknown D1 code.”
It is a real **palette-band state-control cluster**.

---

## 6. strongest safe upgrades from this pass
The safest new top-level conclusions are:

1. sub-op `0x17` should now be treated as an **exact wrapper** to `D1:E984`, not a fuzzy anchored entry
2. `D1:E899` and `D1:E8C1` are exact **`0x7FFF` sentinel-fill helpers** for paired palette-band work tables
3. `D1:E91A` is an exact **promote/copy helper** for:
   - one 48-color working band pair
   - one 48-color promoted band pair
   - one 3-record palette/effect descriptor slab
4. `D1:E984` is the complementary **seed/snapshot helper** that:
   - loads a fixed 48-color ROM seed block from `D0:FD00`
   - snapshots the active descriptor slab outward
   - arms `CDC8`, `CE0F`, and `CE12`
5. `0520..0543` and `0544..0567` can now be treated much more confidently as **adjacent 3-record slabs of the same palette/effect descriptor family** already proven in passes 8–9

That is a real semantic step forward because it ties the auxiliary `CD:0018` VM back into a known subsystem instead of leaving the D1 calls opaque.

---

## Honest caution
Even after this pass:

- I am **not** freezing the final gameplay-facing noun of the `2040/20A0/2120/21A0/2240/22A0/2320/23A0` band families.
- I have **not** fully traced how `CE12`, `CE0F`, and `CDC8` are consumed downstream.
- I have **not** yet closed the relationship between these palette-band helpers and the later `E71D` band-swap routine.
- I have **not** tied this all the way forward into the final output/UI mode or battle-state noun.

But the old “opaque D1 wrappers” gap is now materially smaller.

---

## Best next step
The cleanest next continuation from here is:

1. trace `D1:F42B..F46C` around the `CE12` gate
2. re-open `D1:E71D..E77A` as the exact swap/exchange path for the `2120/21A0` and `2320/23A0` bands
3. then return to the remaining auxiliary command families in `0x88..0x9F`

That should be enough to close the control noun on this palette-band subcluster before going back to the wider tile/materialization seam.
