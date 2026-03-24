# Chrono Trigger Disassembly Pass 110

## What this pass focused on

Pass 109 closed the low-bank `0128 -> $420C` commit tail and proved that the old `AE2B/AE33` idea was only a forced-zero shutdown path.
That left one honest split:

- `C0:ED15..`
- `FD:FFFD -> FD:E022`

This pass freezes that split.
The important outcome is that these two sides are **not** alternate owners of `0128` and they are **not** the same routine in two banks.
They are two different **VRAM update/transfer implementations** selected by the IRQ-side wrapper after HDMA has already been turned off for the frame-safe update window.

---

## 1. `FD:FFFD` is only a bank-local veneer to `FD:E022`

Exact body:

```asm
FD:FFFD  JMP $E022
```

So the pass-109 split is now cleaner than it looked:

> there is no second deep body behind `FD:FFFD`.
> The real FD-side work is the single routine at **`FD:E022..E272`**.

That matters because it removes a fake seam immediately.

---

## 2. `C0:ED15..F058` is an exact CPU-side immediate VRAM patch dispatcher

The entry body now reads cleanly:

```asm
REP #$20
LDA #$0100
TCD
SEP #$20
LDA $63
BMI skip_f05e
JSR $F05E
skip_f05e:
LDA $5F
BIT #$10
BNE family_bit4
BRL $EFD1
```

So `ED15` does three exact things before any leaf transfer body runs:

1. sets `D = $0100`
2. optionally runs the prelude helper at `F05E` when `63` is not negative
3. dispatches by exact bits in `5F`

### Family A — `5F.bit4`

If `5F.bit4` is set, `ED15` uses `60` as the subselector:

- `60 == 0` -> leaf at **`ED31..EDA3`**
- `60 != 0` -> leaf at **`EE88..EFD0`**

#### `ED31..EDA3`
Exact shape:
- sets `$2115 = 0x80`
- performs **8 immediate word writes** to VRAM through `$2116/$2118`
- destinations come from `09CA..09D8`
- data words come from:
  - `7E:BF38`
  - `7E:BF3A`
  - `7E:BF3C`
  - `7E:BF3E`
  - `7E:BF28`
  - `7E:BF2A`
  - `7E:BF2C`
  - `7E:BF2E`
- then clears `5F.bit4` via `TRB $5F`
- returns

#### `EE88..EFD0`
Exact shape:
- sets `$2115 = 0x80`
- performs **24 immediate word writes** to VRAM through `$2116/$2118`
- destinations come from `09CA..09F8`
- data words come from the exact `7E:BFxx` families:
  - `BFD8..BFDE`
  - `BFB8..BFBE`
  - `BF98..BF9E`
  - `BFE8..BFEE`
  - `BFC8..BFCE`
  - `BFA8..BFAE`
- then clears `5F.bit4`
- returns

### Family B — `5F.bit1`

If `5F.bit4` is clear, the code falls into the exact secondary test at `EFD1`:

```asm
BIT #$02
BNE continue
RTS
```

So `5F.bit1` is a second exact pending-patch gate.
Its subselector is `61`:

- `61 == 0` -> leaf at **`EFD7..F019`**
- `61 != 0` -> leaf at **`F01A..F058`**

#### `EFD7..F019`
Exact shape:
- sets `$2115 = 0x80`
- performs **4 immediate word writes** to VRAM
- destinations come from `09B2..09B8`
- data words come from `7E:BFF8..BFFE`
- clears `5F.bit1`
- returns

#### `F01A..F058`
Exact shape:
- sets `$2115 = 0x80`
- performs **4 immediate word writes** to VRAM
- destinations come from `09B2..09B8`
- data words come from `7E:BF08..BF0E`
- clears `5F.bit1`
- returns

### Strongest safe reading

`C0:ED15..F058` is now exact enough to call:

> **the low-bank CPU-side immediate VRAM patch dispatcher, with two pending-flag families in `5F`, optional `F05E` prelude work, and four exact leaf patch grammars selected by `60/61`.**

This is no longer vague “IRQ followup” soup.
It is a real VRAM patch engine that writes directly through `$2116/$2118`.

---

## 3. `FD:E022..E272` is an exact channel-7 VRAM DMA streamer over one of two six-entry descriptor halves

The setup is exact:

```asm
PHP
PHD
PHB
LDA #$00
PHA
PLB
LDA #$80
STA $2115
LDA #$41
STA $4370
LDA #$18
STA $4371
LDX #$0500
PHX
PLD
INC $1D
SEP #$10
LDY #$80
LDA $1D
LSR A
BCC first_half
JMP $E160
```

So this routine:
- sets `DB = $00`
- sets `$2115 = 0x80`
- configures **DMA channel 7** for transfer to `$2118`
- sets `D = $0500`
- increments `051D`
- uses the resulting `051D.bit0` to select one of two local descriptor halves

### First half: `E045..E15B`
This half walks exactly **6 descriptors** rooted at:

- `05B0/05B2/05B4`
- `05B5/05B7/05B9`
- `05BA/05BC/05BE`
- `05BF/05C1/05C3`
- `05C4/05C6/05C8`
- `05C9/05CB/05CD`

### Second half: `E160..E272`
This half walks the sibling **6 descriptors** rooted at:

- `05CE/05D0/05D2`
- `05D3/05D5/05D7`
- `05D8/05DA/05DC`
- `05DD/05DF/05E1`
- `05E2/05E4/05E6`
- `05E7/05E9/05EB`

### Exact per-descriptor grammar
For each descriptor, the body does the same exact work:

1. load the descriptor word at `+2`
2. if that word is negative, skip this descriptor
3. otherwise write that word to `$2116`
4. read the descriptor word at `+0`
5. extract `& 0x0E00`, `XBA`, and use it as an index into exact tables at:
   - `7F:0400`
   - `7F:0410`
6. add the `7F:0400` table delta back into the descriptor `+0` word and store it back
7. load the DMA source low/high from `7F:0410[index]` into `$4372`
8. load the DMA bank byte from descriptor `+4` into `$4374`
9. zero `$4375/$4376`, then set `$4375 = 0x80`
10. start the transfer with `$420B = 0x80`

### Strongest safe reading

`FD:E022..E272` is now exact enough to call:

> **the FD-side channel-7 VRAM DMA streamer that alternates between two six-entry descriptor halves in `7E:05B0..05EB`, using `051D.bit0` as the half selector and `7F:0400/0410` as exact source-table helpers.**

This is not the same thing as `ED15` in another bank.
It is a separate transfer method built around DMA descriptors.

---

## 4. What the `ED15` vs `E022` split now means

This pass closes the real semantic question from pass 109:

- `ED15` = **CPU-side immediate VRAM patch writer**
- `FD:E022` = **channel-7 DMA VRAM block streamer**
- `FD:FFFD` = only a tiny veneer into `E022`

So the bit-0 split proven in pass 109 is best read as:

> **two distinct VRAM update implementations selected by the IRQ-side wrapper after HDMA shutdown**

not:
- two copies of the same body
- a hidden alternate `0128` owner
- or a second unknown routine behind `FD:FFFD`

### Important negative closure
Neither side directly writes:
- `7E:0128`
- `$420C`

So this pass also hardens the earlier conclusion:

> `ED15 / FD:E022` are **pre-commit VRAM update paths**, not the missing direct nonzero owner of the HDMA enable shadow byte.

---

## 5. Best next seam after pass 110

Now that the transfer-method split is closed, the honest next seam is upstream content construction:

1. **who fills `7E:05B0..05EB` and `7E:051D` before `FD:E022` runs?**
2. **who fills `09B2..09F8` and the `7E:BF08..BFFE` word families before `ED15` runs?**
3. what exact role does the optional prelude `C0:F05E` play relative to `63`?

So the clean next push is:

- follow writers of the DMA descriptor workspace around `05B0..05EB`
- follow writers of the low-bank immediate-patch shadows `09B2..09F8` and `7E:BF08..BFFE`
- then decide whether `63/5F/60/61` can safely be promoted from local patch controls to broader display/update state nouns

---

## Completion estimate after pass 110

Conservative project completion estimate: **~68.5%**

Why it rose a bit:
- the fake `FD:FFFD` sub-seam is gone
- the `ED15 / E022` split is no longer fuzzy
- the transfer-method distinction is now exact enough to carry forward without bluffing

Why it did not jump more:
- this still closes structure and semantics, not new bank coverage
- the real upstream producers for both update paths are still open
