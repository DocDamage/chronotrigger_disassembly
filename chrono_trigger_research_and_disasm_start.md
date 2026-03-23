# Chrono Trigger (USA) — Research + Disassembly Start

## 1) What I reviewed first

Before touching the ROM, I anchored on the strongest public Chrono Trigger reverse-engineering resources:

- **Chrono Compendium / Modification** — best hub for the existing CT hacking ecosystem, including Temporal Flux, Mauron's tools, and references to Geiger's offsets.
- **Data Crystal** — reliable quick-reference pages for the SNES ROM profile, RAM map, text table, enemy AI docs, and other technical notes.
- **SMW Central / Yoshifanatic references** — useful for understanding the broader SNES disassembly framework landscape, but not a verified finished public Chrono Trigger disassembly.

## 2) ROM fingerprint of the uploaded file

File: `Chrono Trigger (USA).sfc`

- Size: `4,194,304` bytes (`0x400000`) — **headerless 4 MiB ROM**
- CRC32: `2D206BF7`
- MD5: `a2bc447961e52fd2227baed164f729dc`
- SHA1: `de5822f4f2f7a55acb8926d4c0eaa63d5d989312`

Header fields at `0x00FFC0`:

- Title: `CHRONO TRIGGER`
- Map mode: `0x31` → **FastROM + HiROM**
- Cart type: `0x02`
- ROM size exponent: `0x0C` → **4 MiB**
- SRAM size exponent: `0x03` → **8 KiB**
- Country: `0x01` → USA
- Version: `0x00`
- Checksum complement: `0x8773`
- Checksum: `0x788C`

These values line up with the commonly documented USA v1.0 technical profile.

## 3) Vector map from the uploaded ROM

### Emulation-mode vectors
- `RESET` → `$00:FF00`
- `NMI` → `$FFFF` (unused here)
- `IRQ/BRK` → `$FFFF` (unused here)
- `COP` → `$FF18`

### Native-mode vectors
- `NMI` → `$FF10`
- `IRQ` → `$FF14`
- `BRK` → `$FF18`
- `COP` → `$FFFF`

## 4) First confirmed startup path

### Reset stub
At ROM offset `0x00FF00` / CPU address `$00:FF00`:

```asm
$00:FF00  SEI
$00:FF01  CLC
$00:FF02  XCE
$00:FF03  JML $FD:C000
```

This is the first real anchor point.

### First startup routine
At ROM offset `0x3DC000` / CPU address `$FD:C000`:

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
$FD:C012  SEP #$20
$FD:C014  LDA #$01
$FD:C016  STA $0D      ; -> $420D, FastROM enable
$FD:C018  LDA #$00
$FD:C01A  STA $00      ; -> $4200
$FD:C01C  STA $0B      ; -> $420B
$FD:C01E  STA $0C      ; -> $420C
... many more hardware init writes ...
$FD:C0D4  JML $C0:000E
```

What this tells us immediately:

- The reset flow is clean and conventional.
- The routine at `$FD:C000` is an **early hardware/PPU/CPU init block**.
- It explicitly sets direct page to `$4200` first, then later to `$2100`, so the early `STA dp` writes are **hardware register setup**, not ordinary RAM variables.
- After the hardware init, control jumps into bank `C0` at `$C0:000E`.

### Next confirmed boot target
At ROM offset `0x00000E` / CPU address `$C0:000E`:

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
$C0:0023  LDX #$0500
$C0:0026  STX $4E
$C0:0028  LDX #$0000
$C0:002B  STX $4B
$C0:002D  LDA #$7E
$C0:002F  STA $4D
$C0:0031  JSR $2DF1
...
```

This looks like the handoff from raw hardware init into the game's own main boot/setup logic, probably involving work RAM setup and helper routines.


## 4.5) Early interrupt trampoline setup (confirmed)

Two early boot subroutines write **long-jump trampolines into RAM**:

- `JSR $0B64` writes a `JML` stub at **`$00:0500`** that targets **`$C0:EA63`**.
- `JSR $0B75` writes a `JML` stub at **`$00:0504`** that targets **`$C0:ECCC`**.

That strongly suggests the native interrupt vectors at `$FF10` and `$FF14` are meant to jump into RAM-based trampolines very early in boot, rather than directly into ROM code.

Relevant ROM-side helper snippets:

```asm
$C0:0B64  LDA #$5C
$C0:0B66  STA $0500
$C0:0B69  LDX #$EA63
$C0:0B6C  STX $0501
$C0:0B6F  LDA #$C0
$C0:0B71  STA $0503

$C0:0B75  LDA #$5C
$C0:0B77  STA $0504
$C0:0B7A  LDX #$ECCC
$C0:0B7D  STX $0505
$C0:0B80  LDA #$C0
$C0:0B82  STA $0507
```

Since `$5C` is `JML`, the RAM contents become:

- `$00:0500 = JML $C0:EA63`
- `$00:0504 = JML $C0:ECCC`

This is one of the first really useful architectural findings from the ROM itself.

## 5) Initial labels I would keep

```text
$00:FF00  Reset_Stub_Emu
$FD:C000  HwInit_Bootstrap
$C0:000E  MainBoot_Stage1
$FF10      Native_NMI_Trampoline
$FF14      Native_IRQ_Trampoline
$FF18      BRK_or_COP_Trampoline
```

## 6) Why the research matters

The public docs give us strong non-guess anchors for:

- **ROM profile / mapping**
- **RAM layout**
- **text encoding table**
- **enemy AI structures**
- **Temporal Flux / editor-oriented data knowledge**

That means the disassembly should not be approached as “blind 65816 bytes.” It should be approached as:

1. boot/init code,
2. engine code,
3. event/script systems,
4. battle/AI subsystems,
5. text/tables/assets,
6. compression/pointer formats.

## 7) Immediate next passes

1. Label the `$C0:000E` boot chain and the three early `JSR $0Bxx` routines.
2. Identify whether `$00:0500` and `$00:0504` are RAM-based interrupt trampolines populated during startup.
3. Build a first-pass bank map of clearly code-heavy versus clearly data-heavy regions.
4. Bring in Data Crystal text/AI references when we hit those subsystems instead of guessing command formats from raw bytes.
5. Turn the ad-hoc notes into a reusable disassembly project layout (`labels`, `notes`, `vectors`, `boot`, `battle`, `events`, etc.).
