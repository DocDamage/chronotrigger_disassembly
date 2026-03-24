# Chrono Trigger Disassembly — Pass 86

## Scope of this pass
Pass 85 left two explicit cleanup seams open:

- stop treating `5DA0..5DA5` and `CAEA..CAF5` as generic six-byte fog if their first real mapped consumers can tighten them
- find the first exact external reader of `CDC8`

This pass does both, with one important cleanup step first:

> only **valid HiROM-mapped code references** were trusted this pass.
>
> A lot of earlier raw word/opcode hits in low-half ROM aliases were just mirrored data noise.
> Once those aliases are discarded, the useful seam gets much cleaner.

That cleanup materially changes the picture:

- the first solid external reader of `CDC8` is now exact at `CE:E18E`
- the valid mapped consumers of `5DA0..5DA5` and `CAEA..CAF5` collapse almost entirely into a tight D1-side helper cluster
- that D1 cluster is strong enough to stop calling `5DA0..5DA5` a generic live vector and instead describe it as a **current three-pair point bundle**

I am still **not** forcing the final gameplay-facing presentation noun of that bundle.
But the local structural noun is now much tighter.

---

## 1. alias cleanup: trust only valid HiROM-mapped references
A useful correction came before any new labels:

- many earlier raw xref scans were showing opcode-like matches in ROM offsets whose low 16-bit half was `< 0x8000`
- those bytes can alias to displayed SNES addresses, but they are not valid directly mapped HiROM CPU code locations
- once those are discarded, the “candidate readers” for `CD23 / CD24 / CD25 / 5DA0 / CAEA / CDC8 / CE0F` become much smaller and much cleaner

That matters because it removes a lot of fake confidence from bank-CD script/data noise.

The strongest practical outcome is:

> the valid mapped consumers of `5DA0..5DA5` are overwhelmingly D1-local, not scattered across unrelated engine banks.

That is a real structural tightening, not just bookkeeping.

---

## 2. `CE:E18E` is the first exact external reader of `CDC8`
At `CE:E18E..E1A4`, the exact body is:

```text
LDA $CDC8
BEQ +$12
TDC
TAX
REP #$20
loop:
  STZ $CD47,X
  INX
  INX
  CPX #$0080
  BNE loop
TDC
SEP #$20
RTL
```

### exact behavior
If `CDC8 == 0`, the helper returns immediately.

If `CDC8 != 0`, it clears an exact `0x80`-byte work strip rooted at `CD47`:

- start: `7E:CD47`
- end: `7E:CDC6`
- width: `0x80` bytes total
- clear step: 16-bit `STZ` while X advances by 2

### strongest safe reading
This is the first exact external reader of `CDC8`, and it materially tightens that byte:

> `CDC8` is not just a vague phase byte.
> It is also a real **nonzero gate** for clearing one D1-adjacent `0x80`-byte work strip at `CD47..CDC6`.

I am still **not** claiming that `CDC8` means only “dirty/clear this strip” globally.
But locally that gate behavior is exact.

---

## 3. `D1:F5CD` is the D1-side reusable snapshot helper behind the `5DA0 -> CAEA` family
At `D1:F5CD..F5F2`, the exact body is:

```text
LDA [$40]
TAX
LDA $5DA0  ; STA $CAEA,X
LDA $5DA2  ; STA $CAEE,X
LDA $5DA4  ; STA $CAF2,X
LDA $5DA1  ; STA $CAEC,X
LDA $5DA3  ; STA $CAF0,X
LDA $5DA5  ; STA $CAF4,X
RTL
```

This is the same structural copy pattern already frozen for auxiliary token `0xE3`, but now seen again as an exact D1-side helper.

### strongest safe reading
This is strong evidence that the family is not accidental local scratch.

> D1 has its own exact helper for copying the current `5DA0..5DA5` bundle into one indexed `CAEA..CAF5` destination record.

That materially strengthens the ownership of this state family:

- `5DA0..5DA5` is a real current bundle consumed by D1 helpers
- `CAEA..CAF5` is a real indexed snapshot record family for that bundle

---

## 4. `D1:EC27..EC5B` proves the first pair in `5DA0..5DA5` behaves like an XY-style point pair, not a generic word
At `D1:EC27..EC5B`, the helper:

- takes one stream/immediate index through `[$40]`
- reads the high multiply result byte at `4217`
- builds four 16-bit endpoint slots in `CD0D..CD1B`
- uses `5DA0` as a horizontal-style byte with `-0x10` and `+0x10` offsets
- uses `5DA1` as the paired vertical-style byte copied into both endpoint records
- then calls `D1:F9AF`

The exact writes are structurally:

- one pair from transformed `4217`
- a second neighboring pair from that same transformed value
- one pair from `5DA0 - 0x10` with `5DA1`
- one pair from `5DA0 + 0x10` with `5DA1`

### strongest safe reading
This is the first really clean local evidence that:

> `5DA0` and `5DA1` behave as a **paired coordinate-like byte pair**, not as one undifferentiated 16-bit scalar.

That does **not** prove the final presentation noun of the whole system.
But it is enough to stop calling the bundle a generic six-byte vector.

---

## 5. `D1:EDCD..EE95` turns the same pair into axis-aligned expanding span masks
At `D1:EDCD..EE95`, the helper reads one selector byte from `[$40]` and splits into two exact paths.

### path A: selector `== 0`
This path uses:

- current byte `5DA0`
- growing radius/half-width byte `CD3A`

It clamps:

- low edge to `>= 0x00`
- high edge to `<= 0xFF`

Then it fills one of two four-plane strip families with the computed low-edge value, depending on `7C.bit0`.
The stride is exact:

- write one byte
- advance by 4
- stop at `0x00D4`

### path B: selector `!= 0`
This path uses:

- current byte `5DA1`
- growing radius/half-height byte `CD3B`

It clamps:

- low edge to `>= 0x00`
- high edge to `<= 0xD4`

Then it clears one of two corresponding four-plane strip families across the exact computed span.
Again the stride is 4 bytes per plane step.

### strongest safe reading
This is strong structural support that the first two bytes of the bundle are an axis pair:

> `5DA0` behaves as an X-like current byte feeding expanding horizontal strip fills.
> `5DA1` behaves as a Y-like current byte feeding expanding vertical strip clears/spans.

I am deliberately keeping the final screen/effect noun one notch below frozen.
But the **axis-pair behavior** is now exact enough to keep.

---

## 6. this tightens `5DA0..5DA5` from “live vector” to “current three-pair point bundle”
Pass 85 already proved the raw copy pattern.
Pass 86 adds valid mapped consumer proof:

- `D1:EC27..EC5B` uses `5DA0 / 5DA1` as a coordinate-like pair
- `D1:EDCD..EE95` uses the same pair as axis inputs for expanding strip generation
- `D1:F5CD..F5F2` snapshots all six bytes into the indexed `CAEA..CAF5` family

That is enough for a stronger structural noun:

> `5DA0..5DA5` is best described now as a **current three-pair point/coordinate bundle**
> rather than a generic six-byte live vector.

And correspondingly:

> `CAEA..CAF5` is best described now as an **indexed snapshot record family** for that three-pair bundle.

I am still avoiding the final gameplay-facing noun like “sprite vertices”, “window corners”, or “effect polygon” until a later consumer proves it cleanly.

---

## 7. strongest keepable conclusions from pass 86
1. The first exact external reader of `CDC8` is `CE:E18E..E1A4`.
2. Nonzero `CDC8` gates clearing of an exact `0x80`-byte strip at `CD47..CDC6`.
3. `D1:F5CD..F5F2` is a D1-side reusable helper that snapshots the current `5DA0..5DA5` bundle into indexed `CAEA..CAF5` records.
4. `D1:EC27..EC5B` proves `5DA0 / 5DA1` behave as a paired coordinate-like byte pair.
5. `D1:EDCD..EE95` proves the same pair feeds expanding axis-aligned strip builders.
6. The strongest safe structural noun for `5DA0..5DA5` is now a **current three-pair point bundle**.
7. The strongest safe structural noun for `CAEA..CAF5` is now an **indexed snapshot record family** of that bundle.

---

## Honest caution
Even after this pass:

- I have **not** frozen the final gameplay-facing noun of the `5DA0..5DA5` bundle.
- I have **not** proven whether the three pairs are literally polygon vertices, window points, or another nearby geometric/effect structure.
- I have **not** frozen the final higher-level noun of the `CD47..CDC6` work strip; only its clear-gate behavior by `CDC8` is exact.
- I have **not** frozen the first exact external reader of `CE0F`.
- I have **not** resolved the remaining valid mapped false-positive-looking hits for `CD23 / CD24 / CD25`; those still need stricter proof before being promoted.
