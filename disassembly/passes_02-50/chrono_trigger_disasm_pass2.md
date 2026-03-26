# Chrono Trigger (USA) — Disassembly Pass 2

## What this pass accomplished

This pass turned the earliest startup chain into named, explained routines instead of a raw byte dump.

The biggest concrete finding is that the helper at **`$C0:2DF1`** is a **WRAM zero-fill routine implemented with SNES DMA**, using the **Mode 7 multiplication result register** as a constant-zero source.

That matters because it means the opening boot code is not just "calling some DMA thing" — it is deliberately clearing large memory regions during startup.

---

## Context from existing public research

Before pushing deeper into the ROM, I anchored against the strongest public Chrono Trigger modding references:

- **Chrono Compendium / Modification** — still the best hub for the Chrono Trigger hacking ecosystem, with references to **Temporal Flux**, **Geiger's offsets**, and related utilities.
- **Data Crystal** — strong quick-reference documentation for the USA SNES build, including the ROM profile, RAM map, text table, and other technical notes.

Those sources matter because they confirm the ROM profile and provide trustworthy subsystem context, while the actual code work below comes from the uploaded ROM itself.

---

## Confirmed ROM identity

Uploaded file: `Chrono Trigger (USA).sfc`

- Size: `0x400000` (4 MiB)
- CRC32: `2D206BF7`
- MD5: `a2bc447961e52fd2227baed164f729dc`
- Headerless
- HiROM
- FastROM

This matches the commonly documented USA SNES build profile.

---

## Confirmed early boot chain

### 1) Reset stub

```asm
$00:FF00  SEI
$00:FF01  CLC
$00:FF02  XCE
$00:FF03  JML $FD:C000
```

### 2) Hardware bootstrap

```asm
$FD:C000  REP #$10
$FD:C002  SEP #$20
$FD:C004  LDX #$06FF
$FD:C007  TXS
$FD:C008  LDA #$00
$FD:C00A  PHA
$FD:C00B  PLB
$FD:C00C  REP #$20
$FD:C00E  LDA #$4200
$FD:C011  TCD
...
$FD:C0D4  JML $C0:000E
```

This is the low-level CPU/PPU/bootstrap stage.

### 3) Main boot stage 1

```asm
$C0:000E  SEP #$20
$C0:0010  REP #$10
$C0:0012  JSR $0B64
$C0:0015  JSR $0B75
$C0:0018  REP #$20
$C0:001A  LDA #$0100
$C0:001D  TCD
$C0:001E  SEP #$20
$C0:0020  JSR $0B4E
...
```

This stage installs RAM trampolines, sets direct page to `$0100`, disables rendering/interrupts again, then begins work RAM initialization.

---

## Newly confirmed routine meanings

## `$C0:0B4E` — Disable display + disable interrupts/DMA

```asm
$C0:0B4E  SEI
$C0:0B4F  LDA #$00
$C0:0B51  PHA
$C0:0B52  PLB
$C0:0B53  LDA #$80
$C0:0B55  STA $2100
$C0:0B58  LDA #$00
$C0:0B5A  STA $4200
$C0:0B5D  STA $420B
$C0:0B60  STA $420C
$C0:0B63  RTS
```

**Interpretation:**
- forces screen blank via `$2100`
- disables NMI/joypad auto-read via `$4200`
- disables DMA via `$420B`
- disables HDMA via `$420C`

This is a clean reusable “shut the machine down to a known state” helper.

---

## `$C0:0B64` — Install NMI RAM trampoline

```asm
$C0:0B64  LDA #$5C
$C0:0B66  STA $0500
$C0:0B69  LDX #$EA63
$C0:0B6C  STX $0501
$C0:0B6F  LDA #$C0
$C0:0B71  STA $0503
$C0:0B74  RTS
```

Writes this into RAM:

```asm
$00:0500  JML $C0:EA63
```

---

## `$C0:0B75` — Install IRQ RAM trampoline

```asm
$C0:0B75  LDA #$5C
$C0:0B77  STA $0504
$C0:0B7A  LDX #$ECCC
$C0:0B7D  STX $0505
$C0:0B80  LDA #$C0
$C0:0B82  STA $0507
$C0:0B85  RTS
```

Writes this into RAM:

```asm
$00:0504  JML $C0:ECCC
```

So the native interrupt vectors point at RAM stubs that are populated during boot.

---

## `$C0:2DF1` — WRAM zero-fill via Mode 7 multiplier DMA

```asm
$C0:2DF1  LDA #$00
$C0:2DF3  STA $211B
$C0:2DF6  STA $211B
$C0:2DF9  STA $211C
$C0:2DFC  STA $211C
$C0:2DFF  LDA #$80
$C0:2E01  STA $4370
$C0:2E04  LDA #$34
$C0:2E06  STA $4371
$C0:2E09  LDX $4B
$C0:2E0B  STX $4372
$C0:2E0E  LDA $4D
$C0:2E10  STA $4374
$C0:2E13  LDX $4E
$C0:2E15  STX $4375
$C0:2E18  LDA #$80
$C0:2E1A  STA $420B
$C0:2E1D  RTS
```

### Why this is important

This routine is **not** a normal ROM-to-RAM or RAM-to-VRAM copy.

What it does:
- zeros `$211B/$211C` (Mode 7 multiplication input registers)
- configures DMA channel 7 to read from **B-bus register `$2134`**
- since the multiplication result is zero, DMA receives a stream of zeros
- those zeros are written to the A-bus destination specified by:
  - `$4B` = destination address
  - `$4D` = destination bank
  - `$4E` = transfer length

So this is best understood as:

**`WramZeroFill_M7Result_DMA7`**

That is one of the first genuinely high-value reverse-engineering anchors in the ROM.

---

## What memory gets cleared during early boot

The three earliest calls to `$2DF1` clear the following regions:

### Clear 1

```asm
$C0:0023  LDX #$0500
$C0:0026  STX $4E      ; length = 0x0500
$C0:0028  LDX #$0000
$C0:002B  STX $4B      ; dest = 0000
$C0:002D  LDA #$7E
$C0:002F  STA $4D      ; bank = 7E
$C0:0031  JSR $2DF1
```

Clears:
- **`$7E:0000-$7E:04FF`**

### Clear 2

```asm
$C0:0034  LDX #$E900
$C0:0037  STX $4E      ; length = 0xE900
$C0:0039  LDX #$0700
$C0:003C  STX $4B      ; dest = 0700
$C0:003E  LDA #$7E
$C0:0040  STA $4D
$C0:0042  JSR $2DF1
```

Clears:
- **`$7E:0700-$7E:EFFF`**

### Clear 3

```asm
$C0:0045  LDX #$5080
$C0:0048  STX $4E      ; length = 0x5080
$C0:004A  STX $4B      ; dest = 5080
$C0:004C  LDA #$7F
$C0:004E  STA $4D
$C0:0050  JSR $2DF1
```

Clears:
- **`$7F:5080-$7F:A0FF`**

### Total bytes cleared in this stage

- `0x0500 + 0xE900 + 0x5080 = 0x13E80`
- total = **81,536 bytes**

That is substantial startup memory sanitization, not incidental cleanup.

---

## `$C0:2E1F` — fatal / diagnostic color-loop path

When the boot logic takes the high-X path, it branches into a routine that shuts down display activity, sets a backdrop color from `X`, installs RAM `RTI` stubs, reenables NMI, and spins forever.

Relevant sequence:

```asm
$C0:0077  LDX #$7C00
$C0:007A  BRL $2E21
```

Decoded behavior at `$C0:2E1F+`:

```asm
$C0:2E1F  SEI
$C0:2E20  LDA #$00
$C0:2E22  PHA
$C0:2E23  PLB
$C0:2E24  LDA #$80
$C0:2E26  STA $2100
...
$C0:2E3C  REP #$20
$C0:2E3E  TXA
$C0:2E3F  SEP #$20
$C0:2E41  STA $2122
$C0:2E44  XBA
$C0:2E45  STA $2122
...
$C0:2E65  CLI
$C0:2E66  BRA $2E66
```

This is best labeled something like:

**`FatalColorLoop`** or **`BootErrorColorHang`**

The literal `X = $7C00` value strongly suggests this path uses a visible fixed color to indicate a hard-stop condition.

---

## `$C0:0B86` — early direct-page variable initialization

This routine runs after direct page is set to `$0100`:

```asm
$C0:0082  REP #$20
$C0:0084  LDA #$0100
$C0:0087  TCD
$C0:0088  SEP #$20
$C0:008A  JSR $0B86
```

The first part of `$C0:0B86` clearly:
- copies startup values from `$00/$02/$04` into `$0A/$0C/$0E`
- zeros a large set of direct-page state variables
- seeds several default values and pointers

This is not yet fully semantically named, but it is definitely an **engine state/default variable initializer**.

Candidate label:

**`Init_DirectPageState`**

---

## `$C0:00F4` — grouped early engine init chain

```asm
$C0:00F4  JSR $092B
$C0:00F7  JSR $1B53
$C0:00FA  JSR $0960
$C0:00FD  JSR $6DCF
$C0:0100  JSR $7084
$C0:0103  JSR $7F7E
$C0:0106  JSR $A33B
$C0:0109  JSR $09DD
$C0:010C  JSR $0A14
$C0:010F  JSR $56D4
$C0:0112  JSL $FD:FFFA
$C0:0116  JSL $FD:FFF4
$C0:011A  RTS
```

This is a broad, staged subsystem initializer.

It is too early to name each subcall honestly, but the wrapper itself is clearly an **early engine cold-init pass**.

Candidate label:

**`EngineInit_GroupA`**

---

## `$C0:B1B2` — VRAM DMA upload queue processor (first-pass interpretation)

The second major routine reached from the startup chain appears to process a table of transfer descriptors in direct page and perform VRAM DMA uploads from bank `7F`.

Key clues:
- `$2115` is set to `$80` (VRAM increment mode)
- DMA channel 7 is set for VRAM target register `$2118`
- looped entries load VMADD and DMA source/size from tables
- two DMA launches occur per entry

This is not fully named yet, but a good first-pass label is:

**`Process_VramUploadQueue`**

---

## Current best labels after pass 2

```text
$00:FF00  Reset_Stub_Emu
$FD:C000  HwInit_Bootstrap
$C0:000E  MainBoot_Stage1
$C0:0B4E  DisableDisplayAndInterrupts
$C0:0B64  Install_NMI_RamTrampoline
$C0:0B75  Install_IRQ_RamTrampoline
$C0:0B86  Init_DirectPageState
$C0:00F4  EngineInit_GroupA
$C0:2DF1  WramZeroFill_M7Result_DMA7
$C0:2E1F  BootErrorColorHang
$C0:B1B2  Process_VramUploadQueue
$C0:EA63  Native_NMI_Handler_Entry
$C0:ECCC  Native_IRQ_Handler_Entry
$00:0500  NMI_RamTrampoline
$00:0504  IRQ_RamTrampoline
```

---

## What is now known with confidence

### Strongly confirmed
- ROM identity/profile
- reset path
- hardware bootstrap at `$FD:C000`
- bank `C0` boot handoff at `$C0:000E`
- RAM-installed NMI/IRQ trampolines
- reusable machine-shutdown helper at `$0B4E`
- DMA-based WRAM zero-fill routine at `$2DF1`
- fatal color-loop/hang routine at `$2E1F`

### First-pass, but still grounded
- `$0B86` = direct-page state/default initializer
- `$00F4` = grouped engine/system init wrapper
- `$B1B2` = VRAM DMA queue processor / staged upload routine

---

## Best next targets

1. Fully trace the `$C0:0082` path into the rest of the cold boot chain.
2. Name the subroutines inside `EngineInit_GroupA`.
3. Trace `$C0:EA63` and `$C0:ECCC` far enough to distinguish true NMI work from IRQ work.
4. Map the direct-page variables touched by `$0B86`.
5. Use Data Crystal / Geiger context only when it helps identify data structures, not as a substitute for code tracing.

