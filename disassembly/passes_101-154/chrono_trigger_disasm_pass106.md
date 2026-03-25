# Chrono Trigger Disassembly Pass 106

## What this pass focused on

Pass 105 deliberately stopped at the exact return edge from `D1:F4C0` into `C0:0005 -> C0:0AFF`.

This pass closes that seam.

The key result is that the byte returned in `A` is **not** a fixed literal.
It is the current contents of **`7E:0128`**, and the surrounding code now proves that `7E:0128` is the exact **HDMA enable shadow byte** that later gets committed to `$420C`.

That means the installed D1 RAM NMI trampoline is not pulling a random helper byte. It is asking the low-bank helper family to rebuild / expose the current HDMA enable mask, then writing that exact shadow byte into hardware.

---

## What I did

- re-decoded the exact body at `C0:0AFF..0B27`
- re-decoded the nearby startup sibling at `C0:0B2B..0B50`
- decoded the exact front dispatch at `FD:C2C1..C2DF`
- searched for additional exact consumers and producers of `7E:0128`
- checked whether the return byte into `D1:F4E6  STA $420C` was constant, staged, or shadow-backed

---

## 1. `C0:0AFF..0B27` is exact, and its return value is `7E:0128`

Exact body:

```asm
C0:0AFF  PHP
C0:0B00  PHB
C0:0B01  REP #$20
C0:0B03  LDA #$0100
C0:0B06  TCD
C0:0B07  SEP #$30
C0:0B09  LDA #$00
C0:0B0B  PHA
C0:0B0C  PLB
C0:0B0D  LDA #$80
C0:0B0F  TSB $53
C0:0B11  JSL $FD:C2C1
C0:0B15  JSL $FD:C2C1
C0:0B19  LDA #$80
C0:0B1B  TRB $53
C0:0B1D  REP #$10
C0:0B1F  JSL $FD:C1EE
C0:0B23  LDA $28
C0:0B25  PLB
C0:0B26  PLD
C0:0B27  RTL
```

Two exact things matter here:

1. `TCD` sets the direct page to **`$0100`**.
2. The returned `LDA $28` therefore reads **`7E:0128`**, not zero-page `$0028`.

So the exact answer to the pass-105 seam is:

> the byte returned by `C0:0005 -> C0:0AFF` is the current contents of **`7E:0128`**.

This is a strong closure because `D1:F4E2  JSL C0:0005` followed by `D1:F4E6  STA $420C` means the installed RAM NMI trampoline writes **that exact shadow byte** straight into the HDMA enable register.

---

## 2. `7E:0128` is now exact enough to call the HDMA enable shadow byte

The crucial external proof is not just the return from `C0:0AFF`.
There is also a clean direct hardware commit elsewhere in bank `C0`:

```asm
C0:EC48  LDA $0128
C0:EC4B  STA $420C
```

And there is a clean zeroing producer in the early low-bank machine-reset path:

```asm
C0:AE2B  STA $420C
C0:AE33  STA $0128
```

That pairing matters a lot:

- one clean path writes zero to `$420C` and mirrors that same zero into `7E:0128`
- another clean path loads `7E:0128` and writes it straight back to `$420C`
- `C0:0AFF` returns `7E:0128`, and `D1:F4C0` immediately writes the returned byte to `$420C`

That is enough to stop calling `0128` a generic work byte.

Best safe reading now:

> **`7E:0128` is the low-bank / FD-side HDMA enable shadow byte, and `C0:0AFF` is one of the exact helper paths that refreshes and returns it.**

---

## 3. `FD:C2C1..C2DF` is exact and explains the doubled subpass inside `C0:0AFF`

Exact body:

```asm
FD:C2C1  LDA $53
FD:C2C3  BIT #$01
FD:C2C5  BNE alt
FD:C2C7  LDA $26
FD:C2C9  ASL
FD:C2CA  TAX
FD:C2CB  JSR (C2E5,X)
FD:C2CE  LDA #$01
FD:C2D0  TSB $53
FD:C2D2  RTL

FD:C2D3  alt:
FD:C2D3  LDA $26
FD:C2D5  ASL
FD:C2D6  TAX
FD:C2D7  JSR (C2DF,X)
FD:C2DA  LDA #$01
FD:C2DC  TRB $53
FD:C2DE  RTL
```

The two exact three-entry jump tables are:

- `FD:C2DF` -> `C2EB / C995 / CFCF`
- `FD:C2E5` -> `C847 / CD0C / D27E`

So `FD:C2C1` is not a monolithic builder.
It is an exact **two-table dispatcher**:

- uses `53.bit0` to choose which local jump table to use
- uses `26` to select one of three entries inside that chosen table
- flips `53.bit0` on return

That explains why `C0:0AFF` calls it **twice** before calling `FD:C1EE`.

The strongest safe structural reading is:

> `C0:0AFF` deliberately runs a doubled `FD:C2C1` subpass around the `53.bit7` gate, then calls `FD:C1EE`, then returns the resulting `7E:0128` HDMA shadow byte.

I am still being careful not to overclaim the broader gameplay-facing noun of `53` or `26`.
But the exact dispatch mechanics are now real.

---

## 4. `C0:0B2B..0B50` is a startup sibling that reuses the same HDMA-shadow refresh family

Exact body:

```asm
C0:0B2B  JSL $FD:C124
C0:0B2F  SEP #$10
C0:0B31  JSL $FD:C2C1
C0:0B35  REP #$10
C0:0B37  JSL $FD:C1EE
C0:0B3B  LDA $4210
C0:0B3E  BPL $0B3B
C0:0B40  LDA #$81
C0:0B42  STA $4200
C0:0B45  REP #$20
C0:0B47  LDA #$00D3
C0:0B4A  STA $4209
C0:0B4D  SEP #$20
C0:0B4F  CLI
C0:0B50  RTS
```

This is useful because it ties the `0AFF` helper family back into a clearly hardware-facing startup path.

The safe reading is:

> startup/helper sibling that runs the same FD-side HDMA/display refresh family, waits for the NMI latch at `$4210`, then enables NMI with `$4200 = 0x81`, sets `VTIME = 0x00D3`, and exits with interrupts enabled.

That does not prove every higher-level noun around the FD family, but it does prove this is not random data shuffling. This is a real display / interrupt / HDMA-side control cluster.

---

## 5. What this changes semantically

Pass 105 ended with the question:

> what exact byte comes back in `A`, and is it the true HDMA-enable mask/value producer?

Pass 106 answers that cleanly:

- the returned byte is **not a constant**
- it is **`7E:0128`**
- `7E:0128` is now exact enough to call the **HDMA enable shadow byte**
- `C0:0AFF` is an exact helper that rebuilds / exposes that shadow through the FD-side helper family
- `D1:F4C0` then writes that exact returned byte to **`$420C`**

So yes: within the current honest static proof, this is the real **HDMA-enable mask/value producer edge** behind the installed RAM NMI trampoline.

---

## 6. Strongest safe reading after pass 106

The cleanest grounded reading now is:

- `D1:F4C0` is the installed RAM NMI trampoline body
- inside it, `C0:0005 -> C0:0AFF` is the exact low-bank helper edge that returns the current **HDMA enable shadow**
- that shadow lives at **`7E:0128`**
- `FD:C2C1` is the exact front dispatcher used by that helper family before `FD:C1EE`
- `C0:0B2B..0B50` is a startup sibling proving the same family lives in a real display / interrupt / HDMA control neighborhood

---

## Honest caution

Even after this pass:

- I have **not** frozen the broader final noun of `7E:0153`; only the local `bit7` and `bit0` contracts around this helper family are exact enough to use.
- I have **not** frozen the broader gameplay-facing noun of `7E:0126`; I only know it selects one of three entries inside the two local `FD:C2C1` dispatch tables.
- I have **not** yet lifted the full exact semantics of `FD:C1EE..C2C0`; it is clearly part of the shadow/table rebuild family, but the best next move is to freeze it directly instead of bluffing a noun now.

---

## Best next move

The cleanest next seam is now:

- **`FD:C1EE..C2C0`**

Specifically:

1. freeze the exact roles of the pointer seeds and table roots it writes
2. determine how it materializes or finalizes `7E:0128`
3. decide whether `7E:0153` and `7E:0126` are true mode/state bytes or only local builder selectors in this family

That is cleaner than jumping sideways to `CD:09CE` or `CD:0C89`, because the HDMA-mask producer edge inside the trampoline is now isolated down to the remaining FD-side builder body.
