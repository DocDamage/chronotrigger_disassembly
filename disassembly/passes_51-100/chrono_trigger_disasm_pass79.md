# Chrono Trigger Disassembly — Pass 79

## Scope of this pass
This pass continues directly from the pass-78 seam.

Pass 78 proved that the late service-04 front half is a real packed-row/materialization pipeline, but three ugly gaps were still blocking a stronger noun:

1. the four local transform targets under `CD:13E6`
2. the exact role of the `CA32/52/72` auxiliary work families
3. whether the late service-04 path is really graphics/tile-oriented or just some abstract “fragment” system

The big honest result of this pass is:

> the four `CD:13E6` targets are exact **tile-orientation modes**,
> the `C0:FD00` table is a plain **bit-reverse lookup** used for horizontal flipping,
> and the optional `CA32..` path is not a generic work blob at all — it is a **two-slot auxiliary descriptor stream interpreter**.

That still does **not** freeze the final gameplay-facing noun of the downstream `4500.. -> 5D00..` emit family, but it is now much harder to pretend this late path is anything other than a graphics/tile assembly pipeline.

---

## 1. `CD:13E6` is a four-mode tile-orientation jump table
Pass 78 already proved that the shared builder at `1323/1314` extracts a two-bit mode id from the upper bits of the active source word and dispatches through the local table at `13E6`.

Raw bytes:

```text
CD:13E6  09 15   ; 1509
CD:13E8  45 14   ; 1445
CD:13EA  F6 13   ; 13F6
CD:13EC  EE 13   ; 13EE
```

So the four mode bodies are:

- `1509`
- `1445`
- `13F6`
- `13EE`

The important upgrade is that these are **not** arbitrary transform variants.
They line up exactly with the four orientation combinations you would expect for SNES tile assembly work:

- direct
- horizontal flip
- vertical flip
- horizontal + vertical flip

### 1a. `C0:FD00` is a 256-byte bit-reverse lookup table
The body at `1445` repeatedly does:

```text
LDA $2D00,Y
TAX
LDA C0:FD00,X
STA $2D00,Y
```

and the table at `C0:FD00` begins:

```text
00 80 40 C0 20 A0 60 E0 ...
```

That is the classic 8-bit bit-reversal map:

- `0x01 -> 0x80`
- `0x02 -> 0x40`
- `0x03 -> 0xC0`
- etc.

So the `1445` path is not some generic remap.
It is explicitly **reversing the bit order of tile bytes**, which is exactly what you want for a horizontal flip on planar tile data.

### 1b. `13FE..1444` reverses row order inside both 16-byte tile-plane halves
The helper body reached from `13F6` swaps:

- `00 <-> 0E`
- `02 <-> 0C`
- `04 <-> 0A`
- `06 <-> 08`

and then advances `Y` by `0x10` before returning.

Because `13F6` deliberately uses the helper in the “JSR to next body” trick, the helper runs **twice**:

1. once on the first 16-byte half
2. once again after `Y += 0x10` on the second 16-byte half

That is exactly a **vertical row-order reversal** across the two 16-byte halves of a 32-byte SNES 4bpp tile:

- first 16 bytes = row order for bitplanes 0/1
- second 16 bytes = row order for bitplanes 2/3

So `13F6` is not just “some reorder mode.”
It is a **vertical flip** over a materialized 32-byte tile block.

### 1c. `13EE` is the composite HV-flip mode
The wrapper at `13EE` is tiny and exact:

```text
CD:13EE  PHY
CD:13EF  JSR $13F6
CD:13F2  PLY
CD:13F3  JMP $144A
```

That means:

1. run the vertical-flip materializer path at `13F6`
2. restore the original `Y`
3. jump into the main body of the `1445` bit-reverse path (skipping its own setup)

So `13EE` is the exact composite:

> **vertical flip + horizontal flip**

### 1d. the four local modes now read cleanly as direct / H / V / HV tile materializers
Putting the pieces together:

- `1509` = direct materialization
- `1445` = direct materialization + per-byte bit-reverse = horizontal flip
- `13F6` = direct materialization + row-order reversal = vertical flip
- `13EE` = direct materialization + row-order reversal + per-byte bit-reverse = horizontal + vertical flip

That is the strongest result of this pass.
The builder mode table is no longer abstract at all.
It is an exact **tile-orientation mode table**.

---

## 2. `1509` builds one 32-byte 4bpp tile block from one or two `D0` source blocks
The direct mode body begins:

```text
CD:1509  LDA [$53]
CD:150B  STA $65
CD:150D  AND #$1FFF
CD:1510  ASL
CD:1511  ASL
CD:1512  ASL
CD:1513  TAX
```

So the lower 13 bits of the source word become:

- a source index into the `D0:0000` family
- multiplied by 8 before use

Then the body checks bit `0x2000` of the same source word.

### 2a. helper `1488` materializes a 32-byte tile-shaped block
The helper at `1488` repeatedly loads words from `D0:0000,X`, stores them into `2D00 + 0x00..0x0E`, then builds the paired `0x10..0x1E` half from the same word plus the active selector mask in `$5F`.

The resulting shape is exactly tile-like:

- sixteen bytes in the first half
- sixteen bytes in the second half
- total `0x20` bytes

That is the exact size of a SNES 4bpp tile.

### 2b. the `0x2000` bit controls whether a second source block is merged into the upper half
If the source word has bit `0x2000` set, `1509` does one `1488` call and returns after advancing `Y` by `0x20`.

If bit `0x2000` is clear, the code:

1. runs `1488`
2. advances `X` by `0x10`
3. runs the second half-builder at `152E..15CE`

That second path rewrites only the upper `+10..+1E` half of the tile block using the next `D0` source block while combining with the already built lower-half result and the selector mask.

The safest honest upgrade is:

> `1509` = **materialize one 32-byte 4bpp tile block from one or two `D0` source blocks, then advance `Y` by one tile block**

I am intentionally not claiming the final artist-facing noun of the `D0` source entries yet.
But it is now clearly **tile-source data**, not arbitrary fragment bytes.

---

## 3. The optional `CA32..` path is a two-slot auxiliary descriptor stream interpreter
Pass 78 already proved that `CD:0D33` clears `CA32/52/72`, then walks `CA93[...]` and calls `15D5` for each live descriptor.

This pass closes the next gap.

### 3a. `0D33` seeds exactly two runtime slots, not an arbitrary list length
The clear loop is:

```text
REP #$20
TDC
TAX
loop:
  STZ $CA32,X
  STZ $CA52,X
  STZ $CA72,X
  INX
  INX
  CPX #$0020
  BNE loop
```

Then the descriptor-expansion loop does:

```text
TDC
TAX
TAY
loop:
  LDA $CA93,Y
  CMP #$FF
  BEQ skip
  JSR $15D5
skip:
  INY
  TXA
  CLC
  ADC #$0010
  TAX
  CPX #$0020
  BNE loop
```

So the optional stage is not expanding an arbitrary long active list.
It is seeding **two 16-byte runtime slots** from the first two live descriptor ids in `CA93[...]`.

### 3b. `15D5` expands one descriptor id into one active runtime slot
The descriptor expander:

1. multiplies the descriptor id by two
2. looks up a pointer in `D1:646C`
3. stores that pointer into the active slot
4. pulls the low nibble of the first descriptor byte into a reload/count field
5. increments the slot's active byte

The strongest safe reading is:

> `15D5` = **expand one auxiliary descriptor id into one active runtime stream slot**

The slot fields are now much tighter:

- `CA32/42` = active slot flag
- `CA35/45 .. CA37/47` = descriptor stream pointer
- `CA38/48` = reload period / cadence nibble
- `CA39/49` = current countdown
- `CA3A/4A` = stream-local data addend / page addend used on data tokens

### 3c. `1609..16A5` is a scheduler/interpreter over the two active slots
The next body checks global stage state (`CCEA`, `5D9B`, `0E9D`), then loops over the two active `CA32` slots.

For each active slot it:

1. decrements the slot countdown
2. reloads it from `CA38` when it hits zero
3. calls `1654`

Inside `1654`:

- normal bytes `< 0x80` are interpreted as data-bearing tokens that combine with `CA3A[X]` and index into the `D0` data family
- byte `0x7F` is a dedicated advance/skip token
- byte `0xFF` ends the slot and clears `CA32[X]`
- bytes `>= 0x80` dispatch through the large local jump table at `16B5`

That is not just “auxiliary work.”
It is a real **tiny two-channel descriptor token interpreter**.

The safest honest noun is:

> `1609..16A5` = **tick the two active auxiliary descriptor stream slots and interpret their next tokens when their per-slot countdown expires**

### 3d. `5D9B` and `CCEA` are stage-level gate/progression bytes for that interpreter
The same scheduler only runs when `5D9B != 0` and `CCEA == 0`.
If both slots finish a cycle in the local loop, it clears `5D9B` and increments `CCEA`.

So these are now materially tighter too:

- `5D9B` = active flag for the optional auxiliary descriptor stage
- `CCEA` = stage-level progression / completion byte for that same interpreter pass

I am still keeping the final gameplay-facing noun one notch below frozen.
But this is no longer a generic scratch-work interpretation.

---

## 4. Practical impact on the late service-04 noun
This pass does **not** yet prove the final player-facing object emitted through `4500.. -> 5D00..`.
But it changes the language of the seam in a very important way.

The evidence is now:

- `C3:0002` materializes packed bytes into WRAM
- `CD:0015/002A` build fixed row-sections
- `CD:13E6` chooses one of four exact tile-orientation modes
- those modes are direct / H-flip / V-flip / HV-flip over **32-byte tile-sized blocks**
- `4943` then decodes packed batch data into 4-byte workspace records
- the optional `CA32..` stage is a descriptor/token interpreter that can drive extra tile-source selection state

So the strongest safe upgrade is:

> the service-04 late path is now very likely a **graphics/tile assembly and emit pipeline**, not an abstract fragment system.

I am still stopping short of the final noun for the `5D00..` records themselves.
But the old “maybe this is just some arbitrary fragment logic” hedge is no longer the strongest reading.

---

## Honest caution
What this pass **does not** claim:

1. I have **not** fully frozen the artist-facing noun of the `D0` source entries.
2. I have **not** fully frozen the final gameplay/object noun of the downstream `4500.. -> 5D00..` emit family.
3. I have **not** decoded the huge `16B5..` token-handler table end-to-end; I only proved its dispatch role and the scheduler around it.
4. I have **not** fully decoded the `CA52 / CA72` parallel slot families; the strongest proof in this pass lands on the `CA32..CA4F` runtime-slot family.

---

## Next seam after pass 79
The next clean seam is now:

1. decode the `16B5..` token-handler table enough to freeze the final noun of the two-slot auxiliary descriptor stage
2. re-open `4943` and `4500.. / 5D00.. / A07B` with the new tile-orientation proof in hand
3. decide whether `2D00..` should now be promoted from “packed fragment-row stream” to a tighter **tile-row / tile-batch workspace** noun
