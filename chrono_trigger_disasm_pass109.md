# Chrono Trigger Disassembly Pass 109

## What this pass focused on

Pass 108 said the clean next seam was the low-bank owner/update lane around the `0128 -> $420C` HDMA shadow commit path.

This pass reopened that lane from the ROM bytes themselves and did **not** trust the toolkit’s C0 address rendering blindly.
That mattered, because the bank-`C0` printer/viewer path in the toolkit can render some file-window offsets with an `+0x8000`-looking presentation.
So this pass kept two things separate:

- the **continuity address** used by the handoff/toolkit discussion
- the **raw ROM byte window** actually decoded for proof

That correction paid off immediately.

The old “`C0:AE2B..AE33` producer seam” is no longer vague.
It is the zeroing core of a real **forced-blank / display-off shutdown loop**, not the general nonzero HDMA-owner path.

This pass also froze three exact low-bank service bodies that sit right next to the old seam:

- the exact **PPU shadow flush + `0128 -> $420C` commit tail**
- the exact **VRAM DMA upload helper**
- the exact **OAM DMA upload helper**
- the exact **IRQ-side HBlank wait / force-blank / HDMA-off wrapper** that chooses between `ED15` and `FD:FFFD`

---

## Address-rendering caveat kept in this pass

For continuity with the handoff, I still refer to the old seam as “around `C0:AE2B..AE33` and `C0:EC48..ED0D`”.

But the byte proof in this pass came from the raw low-bank file windows:

- old seam `C0:AE2B..AE33` -> raw decoded body at **bank-C0 file window `0x2E1E..0x2E65`**
- old seam `C0:EC48..ED0D` -> raw decoded bodies around **`0xEC00..0xED13`**

That is the only reason this pass avoids bluffing exact CPU-side bus addresses for every one of these C0 bodies.
The code itself is still real and the local semantics are now much tighter.

---

## 1. The old `AE2B/AE33` seam is the core of a forced-blank shutdown loop

Decoded raw body:

```asm
SEI
LDA #$00
PHA
PLB
LDA #$80
STA $2100
LDA #$00
STA $4200
STA $420B
STA $420C
STA $0128
STA $212C
STA $212D
STA $2121
REP #$20
TXA
SEP #$20
STA $2122
XBA
STA $2122
LDA #$40
STA $0504
LDA #$40
STA $0500
LDA #$0F
STA $0119
LDA #$81
STA $4200
LDA #$0F
STA $2100
CLI
BRA $FE
```

Strongest safe reading:

- enters with interrupts masked
- forces display blank via `$2100 = 0x80`
- clears:
  - `$4200`
  - `$420B`
  - `$420C`
  - `7E:0128`
  - `$212C`
  - `$212D`
  - `$2121`
- writes two bytes from `X` through `$2122`, so `X` is being used as a 15-bit CGRAM color payload here
- seeds exact local bytes:
  - `0504 = 0x40`
  - `0500 = 0x40`
  - `0119 = 0x0F`
- then re-enables `$4200 = 0x81`, restores `$2100 = 0x0F`, unmasks IRQs with `CLI`, and falls into a self-loop

### Why this matters

This closes the old producer interpretation cleanly:

> the `STA $420C` / `STA $0128` pair here is a **forced-zero mirror** inside a shutdown/blackout path.

So this body is **not** the general nonzero producer of the HDMA enable shadow.
It is a special path that zeros the hardware register and mirrors that zero into `0128`.

That is a real closure and it removes one fake remaining seam from the dashboard.

---

## 2. `EC00..EC5D` is the exact low-bank PPU-shadow flush tail that commits `0128 -> $420C`

Decoded exact tail shape:

- conditionally calls exact helper families from bits of `7B`
  - bit 0 -> `JSR $875B`
  - bit 1 -> `JSR $878D`
  - bit 2 -> `JSR $87BF`
- then:
  - `REP #$20`
  - `STZ $78`
  - `STZ $7A`
  - `LDA #$0100 ; TCD`
  - `SEP #$20`
  - `JSL FD:C1EE`
  - `STZ $52`
  - `JSL C2:8002`

Then it flushes the exact shadow bytes:

```asm
0BD9 -> $2123
0BDA -> $2124
0BDB -> $2125
0BDC -> $2128
0BDD -> $2129
0BDE -> $2130
0121 -> $2132
0128 -> $420C
```

And finally:

- if `0119 == 0`, force `$2100 = 0x80`
- restore registers
- `RTI`

### Strongest safe reading

This body is now exact enough to call:

> **the low-bank interrupt/service tail that refreshes FD-side materialization, flushes a contiguous PPU shadow block into window/color-math registers, commits `7E:0128` to `$420C`, and returns by `RTI`.**

This is the first really solid closure on the low-bank commit side since the earlier trampoline work.

### Important semantic consequence

The `0128 -> $420C` edge here is a **consumer/commit** edge, not a constructor edge.
So the real nonzero-owner seam moves forward to:

- the paths that write or alter `0128` before this tail runs
- the exact local branch at `ECCC..ED13`
- and the deeper `ED15` / `FD:FFFD -> FD:E022` split

---

## 3. `EC74..ECA3` is an exact VRAM DMA upload helper

Decoded body:

```asm
LDX $0BE5
STX $2116
LDA #$80
STA $2115
LDA #$01
STA $4370
LDA #$18
STA $4371
LDX #$D800
STX $4372
LDA #$7E
STA $4374
LDX $0BE7
STX $4375
LDA #$80
STA $420B
RTS
```

Strongest safe reading:

> exact DMA-channel-7 helper that uploads from `7E:D800` to VRAM address `$0BE5`, with exact transfer length `$0BE7`, then starts DMA via `$420B = 0x80`.

This is no longer vague DMA soup.

---

## 4. `ECA4..ECCB` is an exact OAM DMA upload helper

Decoded body:

```asm
LDA #$00
STA $2102
STA $2103
LDA #$00
STA $4370
LDA #$04
STA $4371
LDX #$0700
STX $4372
LDA #$00
STA $4374
LDX #$0220
STX $4375
LDA #$80
STA $420B
RTS
```

Strongest safe reading:

> exact DMA-channel-7 helper that uploads `0x0220` bytes from low-bank source `000700` into OAM through `$2104`, after zeroing the OAM address registers.

Again, exact and no longer vague.

---

## 5. `ECCC..ED13` is the IRQ-side HBlank wait / force-blank / HDMA-off wrapper

Decoded body:

```asm
REP #$30
PHA
PHX
PHY
PHD
PHB
SEP #$20
LDA.l $00010F
BMI skip
LDA.l $004211
BPL skip
LDA #$81
STA.l $004200
LDA #$00
PHA
PLB
wait_hblank:
LDA $4212
BIT #$40
BEQ wait_hblank
LDA #$80
STA $2100
LDA #$00
STA $420C
LDA $0153
AND #$01
BNE long_side
JSR $ED15
BRA done
long_side:
JSL FD:FFFD
done:
REP #$30
PLB
PLD
PLY
PLX
PLA
RTI
```

Strongest safe reading:

> exact interrupt-side wrapper that gates on `010F` and `$4211`, waits for HBlank, force-blanks the display, disables HDMA, then chooses one of two follow-up update paths based on `0153.bit0`: local `ED15` when clear, or `FD:FFFD` when set, before restoring state and `RTI`.

### Why this matters

This finally makes the `0153.bit0` split in the low-bank interrupt path concrete on the **consumer side** too.
That bit is not just an FD builder-table selector elsewhere.
It is also steering which follow-up update implementation runs after the wrapper has already turned HDMA off.

---

## 6. What changed about the real seam after pass 109

The honest state now is:

- the old “`AE2B/AE33` owner seam” is **closed**
  - it is the zeroing core of a force-blank shutdown loop
- the exact `0128 -> $420C` **commit** tail is now closed at `EC00..EC5D`
- the IRQ-side wrapper that turns HDMA off and then branches by `0153.bit0` is now closed at `ECCC..ED13`
- the remaining live seam is **not** “what is `0128`?”
  - that part is already strong
- the remaining live seam is:

> which exact path between `ED15` and `FD:FFFD -> FD:E022` rebuilds or mutates the nonzero PPU/HDMA shadow state before the next `EC00..EC5D` commit tail runs?

That is a much cleaner next seam than the older fake ownership wording.

---

## Strongest keepable reading after this pass

- `0128` remains the low-bank HDMA-enable shadow byte
- the old `AE2B/AE33` claim is now refined:
  - it is an **exact forced-zero mirror path**, not the general producer
- `EC00..EC5D` is the exact low-bank **PPU-shadow flush + HDMA-commit tail**
- `EC74..ECA3` is the exact **VRAM DMA upload helper**
- `ECA4..ECCB` is the exact **OAM DMA upload helper**
- `ECCC..ED13` is the exact **IRQ-side HBlank wait / force-blank / HDMA-off branch wrapper**

---

## Honest caution

- I have **not** yet frozen the final higher-level noun of the contiguous shadow block at `0BD9..0BDE / 0121`.
  The hardware sinks are exact, but the broader subsystem name should still stay conservative.
- I have **not** yet frozen the broader meaning of `010F`.
  Only its exact gating role in `ECCC..ED13` is now hard.
- I have **not** yet solved the full body at `ED15..` or the deeper target behind `FD:FFFD -> FD:E022`.
  That is now the best next seam.
