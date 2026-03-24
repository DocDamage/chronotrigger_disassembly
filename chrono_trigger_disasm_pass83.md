# Chrono Trigger Disassembly — Pass 83

## Scope of this pass
This pass continues directly from the pass-82 seam.

Pass 82 closed the exact meanings of the `D1:E899 / E8C1 / E91A / E984` palette-band helpers,
but the downstream control half-cycle was still fuzzy:

- what `CE12` actually does at `D1:F42B..F46C`
- what `CD2F..CD34` really are
- how the later `D1:E70A..E77B` path uses the `2120/21A0` and `2320/23A0` bands

This pass closes a real chunk of that gap.

The honest result is:

> `CE12` is not just an abstract “pending counter” in this local cluster.
> At `D1:F431` / `D1:F457` it behaves as a **one-shot suspend/restore gate**.
>
> `CD2F..CD34` were also too narrow in pass 82.
> The real structure is larger: `D1:F411` proves an **8-byte shadow header array at `CD2F..CD36`**,
> mirroring the first byte of all eight `0520 + n*0C` palette-effect descriptor slots.
>
> And `D1:E70A..E77B` is now exact enough to stop calling it a vague swap seam:
> it performs a full **48-word exchange** between `2120 <-> 21A0` and `2320 <-> 23A0`,
> with a small pre-step tied to `2A21` and `0575`.

I am still **not** freezing the exact gameplay-facing noun of `CFFF`, `A101`, `2A21.bit1`, or the `0575.bit6` toggle.
But the mechanics are now concrete.

---

## 1. `D1:F411` is an exact header-shadow helper for the full 8-slot descriptor queue
The bytes at `D1:F411` decode cleanly:

```text
TDC
TAX
TAY
loop:
  LDA $0520,X
  STA $CD2F,Y
  TXA
  CLC
  ADC #$000C
  TAX
  INY
  CPY #$0008
  BNE loop
RTS
```

That is an exact walk over the **eight** `0x0C`-byte palette-effect descriptor slots.
It copies only the first byte of each slot.

The exact source bytes are:

- `0520`
- `052C`
- `0538`
- `0544`
- `0550`
- `055C`
- `0568`
- `0574`

The exact destinations are:

- `CD2F`
- `CD30`
- `CD31`
- `CD32`
- `CD33`
- `CD34`
- `CD35`
- `CD36`

That is a real correction to pass 82.
`CD2F..CD34` are not merely two local triplets.
They sit inside a wider **8-byte shadow array for descriptor header bytes**.

### strongest safe reading
The strongest safe reading is:

> `D1:F411` snapshots the **type/header byte** of every palette-effect descriptor slot
> from the full `0520..057F` queue into `CD2F..CD36`.

That directly ties the D1 control cluster back into the already-proven 8-record queue from passes 8–9.

---

## 2. `D1:F431` is the suspend half of the `CE12` gate
The first downstream branch body is:

```text
LDA $CE12
BNE done
INC $CE12
JSR $F411
TDC
TAX
loop:
  LDA $0520,X
  BMI skip
  AND #$F0
  CMP #$10
  BNE skip
  STZ $0520,X
skip:
  TXA
  CLC
  ADC #$000C
  TAX
  CPX #$0060
  BNE loop
done:
RTL
```

This is exact enough for three strong claims.

### 2a. it is a one-shot arm path
If `CE12 != 0`, the routine returns immediately.

If `CE12 == 0`, it increments `CE12` and continues.
So locally this is clearly a **one-shot arm path**, not a free-running count loop.

### 2b. it snapshots descriptor headers before mutating them
Before touching the queue, it calls `D1:F411`.
So the original header bytes are preserved in `CD2F..CD36`.

### 2c. it suspends only non-negative `0x1x` descriptors
The per-slot test is exact:

- if bit 7 is set, skip the slot entirely
- otherwise isolate the high nibble with `AND #$F0`
- if the high nibble is `0x10`, clear the header byte with `STZ`

Pass 9 already proved:

- `0x1x` and `0x8x` are the palette-animation frame-player families

So this routine is not blanking all descriptors.
It is specifically suppressing the **non-negative `0x1x` family headers** while leaving the `0x8x` signed family alone.

### strongest safe reading
The strongest safe reading is:

> `D1:F431` is the **shadow-and-suspend** half of the local D1 gate:
> it arms `CE12`, snapshots all eight descriptor header bytes to `CD2F..CD36`,
> and then temporarily clears only the active non-negative `0x1x` palette-animation family headers.

That is much tighter than the old “CE12 consumer” wording.

---

## 3. `D1:F457` is the restore half of the same gate
The sibling body is:

```text
LDA $CE12
BEQ done
STZ $CE12
TDC
TAX
TAY
loop:
  LDA $CD2F,Y
  STA $0520,X
  TXA
  CLC
  ADC #$000C
  TAX
  INY
  CPY #$0008
  BNE loop
done:
RTL
```

This is the exact inverse of `D1:F411` + the header clear from `F431`.

### 3a. it is also one-shot gated
If `CE12 == 0`, it returns immediately.
If `CE12 != 0`, it clears `CE12` and performs the restore.

Again, that is latch/gate behavior, not an open-ended counter consumer.

### 3b. it restores all eight header bytes
The loop restores:

- `CD2F..CD36`
  back into
- `0520 / 052C / 0538 / 0544 / 0550 / 055C / 0568 / 0574`

So the exact thing being restored is the first byte of each descriptor record.

### strongest safe reading
The strongest safe reading is:

> `D1:F457` is the **restore** half of the same local gate:
> when `CE12` is armed, it clears the latch and restores the shadowed descriptor header bytes
> back into all eight palette-effect descriptor slots.

---

## 4. `D1:F427` selects suspend vs restore through `CFFF`
The branch selector in front of the two bodies is exact:

```text
LDA $CFFF
BEQ restore_path
JMP $F431
restore_path:
JMP $F457
```

So the local selector is simple:

- `CFFF != 0` -> run the **shadow-and-suspend** path at `F431`
- `CFFF == 0` -> run the **restore** path at `F457`

The mapped ROM proof I currently have for `CFFF` itself is still limited.
`D1:F295` clears it during nearby setup, but I do **not** yet have a clean mapped-ROM writer that sets it nonzero.
So the exact higher-level noun of `CFFF` stays open.

### strongest safe reading
The safest keepable conclusion is:

> `CFFF` is a **local suspend-vs-restore selector** for the descriptor-header shadow gate.

That is real behavior even though the final gameplay-facing flavor of the flag remains open.

---

## 5. `CE12` can now be tightened from vague counter to local one-shot gate
Pass 82 called `CE12` a shared pending-step / handshake counter.
That was directionally okay, but too vague.

This pass proves the local shape:

- `F431` does nothing if `CE12 != 0`, otherwise increments it and arms the suspend step
- `F457` does nothing if `CE12 == 0`, otherwise clears it and restores the shadowed headers

So for this exact downstream consumer:

> `CE12` behaves like a **one-shot suspend/restore gate latch**.

I am still keeping some caution because `E91A` and `E984` also increment it,
and there may still be wider cluster semantics beyond just this local pair.
But it is definitely more gate-like than “free counter” inside `F431/F457`.

---

## 6. `D1:E70A..E77B` is an exact 48-word exchange between the secondary and tertiary palette bands
The later swap seam also came into focus.

The entry is:

```text
STZ $A101
LDA $2A21
AND #$02
BEQ no_toggle
LDA $0575
EOR #$40
STA $0575
no_toggle:
REP #$20
LDX #$0000
loop:
  LDY $2320,X
  LDA $23A0,X
  STA $2320,X
  TYA
  STA $23A0,X

  LDY $2340,X
  LDA $23C0,X
  STA $2340,X
  TYA
  STA $23C0,X

  LDY $2360,X
  LDA $23E0,X
  STA $2360,X
  TYA
  STA $23E0,X

  LDY $2120,X
  LDA $21A0,X
  STA $2120,X
  TYA
  STA $21A0,X

  LDY $2140,X
  LDA $21C0,X
  STA $2140,X
  TYA
  STA $21C0,X

  LDY $2160,X
  LDA $21E0,X
  STA $2160,X
  TYA
  STA $21E0,X

  INX
  INX
  CPX #$0020
  BNE loop
DEC $40
TDC
SEP #$20
RTL
```

### 6a. the swap geometry is exact
This is not a vague transform.
It is a full pairwise exchange of the `0x60` bytes / 48 words in:

- `2120..217F` <-> `21A0..21FF`
- `2320..237F` <-> `23A0..23FF`

implemented as three `0x20`-byte sub-bands per side.

That closes the main structural question from pass 82.
The tables seeded by `E899` and `E8C1` really do feed a later **swap/exchange** path.

### 6b. there is a small selector-sensitive pre-step
Before the swap:

- `A101` is cleared
- `2A21.bit1` is tested
- if that bit is set, bit `0x40` of `0575` is toggled

The exact higher-level meaning of those three state bytes is still open.
But this is now concrete enough to say the swap path is not a pure memory shuffle;
it has a mode-sensitive pre-step.

### 6c. post-step local counter/depth byte
The tail decrements direct-page `$40`.
That is exact, but I am not freezing its wider noun yet.

### strongest safe reading
The strongest safe reading is:

> `D1:E70A..E77B` is a selector-sensitive **band exchange helper**:
> it optionally toggles one descriptor field based on `2A21.bit1`,
> then swaps the full 48-word secondary/tertiary palette-band pairs
> `2120 <-> 21A0` and `2320 <-> 23A0`,
> then decrements local DP state.

---

## 7. strongest safe upgrades from this pass
The strongest keepable conclusions are now:

1. `D1:F411` is an exact **8-slot descriptor-header shadow helper**
2. `CD2F..CD36` is the real shadow array, not just the narrower `CD2F..CD34` subset
3. `D1:F431` is the **shadow-and-suspend** half of a one-shot gate
4. `D1:F457` is the **restore** half of the same gate
5. `CFFF` locally selects **suspend vs restore**
6. `CE12` behaves as a local **one-shot gate latch** in this consumer pair
7. `D1:E70A..E77B` is an exact **48-word exchange** between the `2120/21A0` and `2320/23A0` band pairs

That is a real semantic step forward because the pass-82 helper cluster now has a concrete downstream control story instead of stopping at “these helpers exist.”

---

## Honest caution
Even after this pass:

- I am **not** freezing the final gameplay-facing noun of `CFFF`.
- I am **not** freezing the final noun of `A101`, `2A21.bit1`, or the `0575.bit6` toggle.
- I am **not** claiming that `CE12` is globally only a latch with no wider meaning outside this local consumer pair.
- I am **not** yet tying this cluster all the way to the final battle/UI presentation name.

But the D1 half-cycle is now materially less fuzzy than it was after pass 82.

---

## Best next step
The cleanest continuation from here is:

1. trace who actually drives `CFFF` nonzero in mapped runtime behavior
2. tighten `CE0F` and `CDC8` now that `CE12` is locally much clearer
3. explain why the suspend path clears only `0x1x` headers while sparing the signed `0x8x` family
4. freeze the exact role of the two tail descriptor slots at `0568..057F`
5. then return to the remaining auxiliary command families in `0x88..0x9F`
