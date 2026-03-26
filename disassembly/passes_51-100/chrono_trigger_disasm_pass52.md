# Chrono Trigger Disassembly Pass 52

## Scope of this pass
This pass continued directly from pass 51's live seam:

- identify the exact source and meaning of the local `$2C` term inside `FD:B820..B850`
- decide whether pass 51's “small random/bias term” reading survives direct code inspection
- re-check the sibling family at `FD:B8C0..B8E0`
- tighten the exact battle-side formula feeding the visible lane readiness seed path

This pass materially resolves the biggest remaining ambiguity from pass 51.

The main result is simple:

> the `FD:B820..B850` seed family is **not** using a random/bias term.  
> It is using a **configuration-selected battle-speed page** plus the participant's **speed stat** in a two-stage multiply/table formula.

That is a real structural upgrade, not just a rename.

---

## Method
1. Re-read the exact control flow around `FD:B820..B850` and `FD:B8C0..B8E0`.
2. Disassemble the long helper at `C1:FDBF` and the local helper it immediately enters.
3. Inspect the full data run at `CC:2E31` instead of treating it like a single 16-byte table.
4. Algebraically simplify the resulting seed formula and compare it against the battle-speed interpretation already hinted by the community-side context from earlier research.

---

## 1. `C1:FDBF` is just a thin wrapper into `C1:C90B`
The long helper used twice in the seed family is:

```text
C1:FDBF  JSR $C90B
C1:FDC2  RTL
```

So the real work happens at `C1:C90B`.

That matters because it lets us stop guessing about `$2C` and read the exact arithmetic.

---

## 2. `C1:C90B` is a real unsigned multiply helper writing the low result to `$2C`
The body at `C1:C90B` is the classic shift/add multiply pattern:

```text
REP #$20
LDX #$0010
STZ $2C
STZ $2E
loop:
  ROR $2A
  BCC skip_add
  CLC
  LDA $28
  ADC $2E
  STA $2E
skip_add:
  ROR $2E
  ROR $2C
  DEX
  BNE loop
SEP #$20
RTS
```

The important practical result for this branch is:

> `C1:C90B` multiplies the two 16-bit inputs at `$28` and `$2A` and leaves the low word in `$2C`.

That is enough to hard-kill the pass-51 “maybe random/bias” reading.

---

## 3. First multiply in `FD:B820..B850`: `$2C = ($2990 & 7) * 0x10`
The first relevant setup in the seed family is:

```text
LDA $2990
AND #$07
TAX
STX $28
LDX #$0010
STX $2A
JSL $C1:FDBF
```

So after the helper returns:

```text
$2C = ($2990 & 7) * 0x10
```

This is not noise and not entropy.
It is a clean page selector.

### Consequence
When the code then does:

```text
LDA record+38
DEC A
CLC
ADC $2C
TAX
LDA.l $CC:2E31,X
STA $00
```

the effective table index is:

```text
index = (speed - 1) + (($2990 & 7) * 16)
```

So `CC:2E31` is **not** a single 16-byte speed table.
It is an **8-page x 16-entry** table family.

---

## 4. `CC:2E31` is an 8x16 battle-speed page family
Reading the full data block instead of only the first 16 bytes yields:

### Page 0
`CD D1 D5 D9 DD E1 E5 E9 ED F1 F5 F9 FD 01 05 09`

### Page 1
`E5 E8 EB EE F1 F4 F7 FA FD 00 03 06 09 0C 0F 12`

### Page 2
`FD FF 01 03 05 07 09 0B 0D 0F 11 13 15 17 19 1B`

### Page 3
`15 16 17 18 19 1A 1B 1C 1D 1E 1F 20 21 22 23 24`

### Page 4
`2D` repeated 16 times

### Page 5
`45 44 43 42 41 40 3F 3E 3D 3C 3B 3A 39 38 37 36`

### Page 6
`5D 5B 59 57 55 53 51 4F 4D 4B 49 47 45 43 41 3F`

### Page 7
`75 72 6F 6C 69 66 63 60 5D 5A 57 54 51 4E 4B 48`

This data is far too structured to be accidental:
- page size = 16
- page count = 8
- each page is indexed by the same clamped speed byte
- the page selector is the low 3 bits of config byte `$2990`

Best current reading:

> `CC:2E31` is the **battle-speed-page x speed-stat readiness seed adjustment table**.

---

## 5. Second multiply in `FD:B820..B850`: `$2C = speed * 6`
After loading the table adjustment into `$00`, the code immediately does a second multiply:

```text
LDA record+38
TAX
STX $28
LDX #$0006
STX $2A
JSL $C1:FDBF
```

So this second helper call yields:

```text
$2C = speed * 6
```

This is then consumed by the final seed expression:

```text
LDA #$69
SEC
SBC $2C
CLC
ADC $00
STA $B158,X
STA $AFAB,X
```

So the exact seed formula is now:

```text
seed = 0x69 - (speed * 6) + battle_speed_adjust[page][speed - 1]
```

where:

```text
page = ($2990 & 7)
speed = [participant record + 0x38]
```

That is materially stronger than anything in pass 51.

---

## 6. The formula simplifies into 8 exact linear families
When the 8 table pages are substituted into the final arithmetic above, the seed collapses into these exact page formulas:

### Page 0
`seed = 50 - 2*speed`

### Page 1
`seed = 75 - 3*speed`

### Page 2
`seed = 100 - 4*speed`

### Page 3
`seed = 125 - 5*speed`

### Page 4
`seed = 150 - 6*speed`

### Page 5
`seed = 175 - 7*speed`

### Page 6
`seed = 200 - 8*speed`

### Page 7
`seed = 225 - 9*speed`

This is the cleanest battle-side algebra yet for the readiness branch.

### Why this matters
This does three things at once:

1. It proves the page selector is a **configuration-controlled speed mode**, not randomness.
2. It proves the participant byte at `+0x38` is functionally the speed input for the seed path.
3. It shows the readiness seed is controlled by a **subtractive speed model** whose slope changes with the selected configuration page.

That lines up extremely well with the outside/community understanding that Chrono Trigger's battle-speed option changes ATB timing behavior, but here the ROM work gives the exact numbers.

---

## 7. `FD:B8C0..B8E0` is a true sibling seed family, not a separate formula family
The sibling path at `FD:B8C0..B8E0` reuses the same two core steps:

1. page-selected adjustment already in `$00`
2. second multiply with `speed * 6`
3. final seed:

```text
0x69 - (speed * 6) + $00
```

and then stores the result to:

```text
B15B,X
AFAE,X
```

So this branch is **not** using a different readiness formula.
It is the same seed family applied to the sibling export pair.

### Additional side effects in the sibling path
This pass also tightens two side effects that are specific to the sibling branch:

- if record byte `+0x0A` has bit 0 set, the routine ORs `#$40` into `$AF15[slot]`
- it sets `B03D[slot] = 1` only when `$AF02[slot] != #$FF`

Those are real structural differences, but the seed math itself is shared.

---

## 8. What this does to earlier labels
This pass forces one important correction to pass 51:

### Retired interpretation
- local `$2C` in `FD:B820..B850` is **not** “small random/bias term”

### Stronger replacement
- first `$2C` use = battle-speed page selector (`($2990 & 7) * 16`)
- second `$2C` use = `speed * 6`

That is a genuine upgrade in certainty.

---

## 9. Strongest safe readings after pass 52

### `7E:2990` low 3 bits
Best current reading:

> **battle-speed config field** used directly by the battle readiness seed branch

I am still keeping one step of caution on naming the whole byte because the upper bits are clearly carrying other configuration options elsewhere.

### participant record byte `+0x38`
Best current reading:

> **current/effective speed byte** used directly by the battle readiness seed formula

This is now stronger than pass 51's “speed-like stat” wording.

### `CC:2E31`
Best current reading:

> **8-page battle-speed x speed adjustment table for the readiness seed branch**

### `FD:B820..B850`
Best current reading:

> **primary visible-lane readiness seed writer from battle-speed config and speed stat**

### `FD:B8C0..B8E0`
Best current reading:

> **sibling visible-lane readiness seed writer using the same formula, with extra per-slot side effects**

---

## 10. Open edges after this pass
This pass resolves the biggest algebraic ambiguity, but a few things still deserve one more pass:

1. the exact higher-level semantic split between the two export pairs:
   - `B158 / AFAB / B03A`
   - `B15B / AFAE / B03D`
2. the precise gameplay-facing meaning of the sibling-only flag updates:
   - `AF15.bit6`
   - `AF02 != FF -> B03D = 1`
3. whether `B158` should ultimately freeze as a “readiness seed,” “delay seed,” or a narrower timing name after tracing more of the downstream consumers

---

## Bottom line
Pass 52 materially upgrades the readiness branch.

The battle-side seed is no longer:
- “speed-like stat + maybe bias/random”

It is now:

> **an exact two-stage formula driven by**
> - the participant's speed byte at `+0x38`
> - the low-3-bit config field in `$2990`
> - the 8x16 page table at `CC:2E31`

That is real progress and a real reduction in uncertainty.
