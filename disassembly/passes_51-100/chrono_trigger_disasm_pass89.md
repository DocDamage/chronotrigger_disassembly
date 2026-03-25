# Chrono Trigger Disassembly — Pass 89

## Scope of this pass
Pass 88 proved that the `C161 / C163 / C4E1 / C4E3` neighborhood belongs to a real
**dual-bundle eight-table raster-target workspace**, but it still left the most important local
write-side question open:

- what do the nearby D1 writers at `EDCD..EE95` and `EEA6..EF5F` actually do?
- are they just vague "span helpers", or can they be frozen as exact lane writers?
- does the `CD3A / CD3B / 5DA0 / 5DA1` cluster feed the newly-frozen workspace in a more precise way?

This pass closes that local seam much more tightly.

The strongest keepable result is:

> `D1:EDCD..F107` is not one generic blob.
>
> It splits cleanly into:
> - an exact **lower-edge byte stamp** into one selected primary/shadow lane family
> - an exact **companion word-span fill** across a clamped range
> - an exact **descending ramp seed** tied to `CD3A`
> - an exact **curve-table / hardware-multiply writer** that builds the first four primary lanes
>   rooted at `C15D / C15F / C161 / C163`
>
> That is enough to stop calling this whole area merely a local strip helper cluster.

I am still keeping the final gameplay-facing presentation noun below frozen.
But the write-side mechanics are now much more exact.

---

## 1. `D1:EDCD..EE2F` splits into two exact selector paths
The routine really begins at `D1:EDCD`:

```text
D1:EDCD  LDA [$40]
D1:EDCF  BNE $EE33
```

So the selector byte read from `[$40]` is exact.

### selector `== 0` path: `5DA0 / CD3A`
The `== 0` path does this exactly:

```text
LDA $5DA0
SEC
SBC $CD3A
BCS +
TDC
STA $45          ; low = max(0, 5DA0 - CD3A)

LDA $5DA0
CLC
ADC $CD3A
BCC +
LDA #$FF
STA $46          ; high = min(0xFF, 5DA0 + CD3A)

LDA $CD3A
CMP #$08
BCS +
INC $CD3A
```

Then the actual write loop **does not use the computed high edge**.
It uses only the low edge byte in `$45` and stamps it repeatedly.

With `REP #$20` active and `7C.bit0` choosing bundle side:

- when `7C.bit0 != 0`, it writes `$45` into:
  - `C4E1 + X`
  - `C5B5 + X`
  - `C689 + X`
  - `C75D + X`
- when `7C.bit0 == 0`, it writes `$45` into:
  - `C161 + X`
  - `C235 + X`
  - `C309 + X`
  - `C3DD + X`

with:

- `X = 0, 4, 8, ...`
- stop when `X == 0x00D4`

### strongest safe reading
This is stronger than the earlier generic wording.

> selector `0` is an exact **clamped lower-edge byte stamp**.
>
> It uses `5DA0` and the growing byte `CD3A`, then writes the resulting **lower edge byte**
> into one selected primary-or-shadow four-lane family.

The important correction here is that the computed high edge is local bookkeeping in this path,
not the value actually streamed by the stamp loop.

---

## 2. `D1:EE33..EE95` is the exact companion clamped-span fill
The selector `!= 0` path begins at `D1:EE33` and is exact enough to freeze.

It uses:

- current byte `5DA1`
- growing span byte `CD3B`

and computes:

```text
low  = max(0,   5DA1 - CD3B)
high = min(D4,  5DA1 + CD3B)
```

Then:

```text
LDA $CD3B
CMP #$09
BCS +
INC $CD3B
```

so `CD3B` grows locally until it reaches `0x09`.

The write loop then does this exactly:

- convert `low` into `X = low * 4`
- convert `high` into stop offset `end = high * 4`
- while `X != end`:
  - if `7C.bit0 != 0`, store `0xFF00` to `C4E3 + X`
  - else              store `0xFF00` to `C163 + X`
  - `X += 4`

### strongest safe reading
This is not a vague companion strip helper anymore.

> selector `!= 0` is an exact **clamped companion word-span fill**.
>
> It uses `5DA1` and the growing span byte `CD3B`, then fills `0xFF00` across the selected
> primary-or-shadow companion lane from `low * 4` up to `high * 4`.

This is materially stronger than the earlier wording because the actual fill value,
start/stop contract, and exact roots are now frozen.

---

## 3. `D1:EEA6..EEC4` is an exact descending ramp seed tied to `CD3A`
This tiny routine looked fuzzy before, but it is actually exact.

Body:

```text
LDA #$C0
SEC
SBC $CD3A
REP #$20
ASL A
ASL A
TAY
BMI done

TDC                ; A = 0
loop:
  STA $C15F,Y
  INC A
  DEY
  DEY
  DEY
  DEY
  BPL loop

INC $CD3A
done:
TDC
SEP #$20
RTL
```

### exact behavior
It computes:

- `Y = (0xC0 - CD3A) * 4`

and, while `Y >= 0`, writes an ascending 16-bit ramp:

- first word = `0`
- next word  = `1`
- next word  = `2`
- etc.

into:

- `C15F + Y`
- `C15F + Y - 4`
- `C15F + Y - 8`
- ...

Then it increments `CD3A` and returns.

### strongest safe reading
> `D1:EEA6..EEC4` is an exact **descending 16-bit ramp seed** into the primary lane family
> rooted at `C15F`, with its length controlled by `CD3A`.

I am still not forcing the final presentation noun of that ramp.
But its exact mechanics are no longer vague.

---

## 4. `D1:EEC5..EF62` is the real primary four-lane curve/profile writer
This was the richest open seam from pass 88.
It now freezes as a real curve-table writer rather than an anonymous math blob.

### 4a. exact local setup
The routine begins by updating `CD3A` from the stream byte at `[$40]`:

```text
LDA $CD3A
CLC
ADC [$40]
STA $CD3A
```

Then it derives three exact local parameters:

```text
A   = 0x60 - CD3A
4B  = A
4D  = A >> 1
45  = 7C * 4
47  = 7C * 2
```

Then with `REP #$20` it builds two center words:

```text
4F = CA5A + CA5E
51 = CA5C + CA60
```

### 4b. exact outer loop
The outer loop is exact:

- `Y` starts at `0`
- each iteration ends with `Y += 8`
- loop stops when `Y == 0x0350`

So the write span is an exact `0x350` bytes in 8-byte row steps.

### 4c. exact sample source and hardware multiply
Each iteration samples the monotone table at `CE:F48E` using either `45` or `47` as the index,
then feeds the SNES hardware multiplier:

- multiplicand source: `CE:F48E,X`
- multiplier `A`: `4B` or `4D`
- registers used: `4202 / 4203`
- result consumed from `4217`

That means this routine is not generic software math.
It is a real **table-driven, hardware-multiply profile writer**.

### 4d. what gets written
Two exact helper paths do the actual stores:

#### `D1:EF63..EFCF`
This helper:

- sign-extends the sampled byte when needed
- adds it to the baseline table word at `E500,Y`
- stores the result to both:
  - `C15D,Y`
  - `C161,Y`
- then primes the next multiply using `45 / 4D`
- returns carry based on the sign branch taken through that second setup

#### `D1:F0E9..F107`
This helper:

- sign-extends the sampled byte when needed
- adds it to center word `51`
- stores the result to both:
  - `C15F,Y`
  - `C163,Y`

### strongest safe reading
This is now exact enough to keep structurally:

> `D1:EEC5..F107` builds the first four primary lanes
> `C15D / C15F / C161 / C163`
> over an exact `0x350` span,
> using:
> - the monotone profile table at `CE:F48E`
> - the baseline pair table at `E500`
> - center words derived from `CA5A..CA60`
> - and the SNES hardware multiplier.

That is a real upgrade because it turns the vague “local math blob” into a concrete
**curve/profile lane writer** for the primary bundle.

---

## 5. this materially tightens the write-side meaning of the workspace
Pass 88 froze the mirror ownership of the `C161..C7F3` workspace.
Pass 89 now freezes the local write side much more exactly.

The keepable picture is now:

- `EDCD..EE2F` stamps a clamped **lower edge byte** into one selected lane family
- `EE33..EE95` fills a clamped **companion span** with `0xFF00`
- `EEA6..EEC4` seeds a descending **primary ramp** tied to `CD3A`
- `EEC5..F107` builds the first four primary lanes from a real **curve/profile writer**
- pass 88 already proved later mirror helpers move selected bands between primary and shadow bundles

That means the project no longer has to describe this whole local region as only
“adjacent strip helpers.”

It is now safe to say:

> this is a real local **primary-lane build + mirror** pipeline feeding the raster-target workspace.

I am still keeping the final presentation noun below frozen.
But the pipeline shape is now much stronger.

---

## 6. CE0F reader check: still not clean enough to freeze
I also checked the `CE0F` seam again, but more strictly.

Useful result:

- the only clean mapped `LDA $CE0F` opcode pattern currently found lands at `CD:BEF8`
- that neighborhood is still dense bank-CD script/data territory, not clean proven code

So this pass does **not** freeze the first exact external reader of `CE0F` yet.

That is an honest non-result, but it is still useful because it prevents promoting a bad label
from script/data noise.

---

## 7. strongest keepable conclusions from pass 89
1. `D1:EDCD..EE2F` selector `0` is an exact **clamped lower-edge byte stamp** using `5DA0 / CD3A`.
2. That path writes the stamped byte into the selected primary/shadow four-lane family rooted at:
   - primary: `C161 / C235 / C309 / C3DD`
   - shadow:  `C4E1 / C5B5 / C689 / C75D`
3. `D1:EE33..EE95` selector `!= 0` is an exact **clamped companion word-span fill** using `5DA1 / CD3B`.
4. That path fills `0xFF00` from `low * 4` to `high * 4` at `C163` or `C4E3`, selected by `7C.bit0`.
5. `D1:EEA6..EEC4` is an exact **descending 16-bit ramp seed** into the primary `C15F` lane family, tied to `CD3A`.
6. `D1:EEC5..F107` is an exact **curve/profile lane writer** that builds `C15D / C15F / C161 / C163` over a `0x350` span using `CE:F48E`, `E500`, `CA5A..CA60`, and hardware multiply.
7. The strongest safe structural noun is now a local **primary-lane build + mirror pipeline** feeding the raster-target workspace.

---

## Honest caution
Even after this pass:

- I have **not** frozen the final gameplay-facing presentation noun of the raster-target workspace.
- I have **not** frozen the exact higher-level caller contract that explains the full `CD3A / CD3B / 7C / 5DA0..5DA5 / CA5A..CA60` choreography.
- I have **not** frozen the first exact external reader of `CE0F` in clean code territory.
- I have **not** yet tied the local primary-lane builder to one exact downstream gameplay-facing effect name.
