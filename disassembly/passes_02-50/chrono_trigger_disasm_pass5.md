# Chrono Trigger (USA) — Disassembly Pass 5

## What this pass focused on

This round followed the decompressed destinations more carefully and, just as important, corrected one control-flow assumption from the previous pass.

The biggest win here is that bank `C0:A33B` is no longer just “some parser after decompression.”
It is now clearly part of the game's **display / BG configuration path**.

---

## Important correction from the previous pass

I re-checked the control flow at `C0:56D4` and found that the previous pass had blended adjacent code too aggressively.

### `C0:56D4` does **not** fall through into the long body at `C0:570A+`

The actual tail of the routine is:

```asm
$C0:56FF  JSL $C3:0002
$C0:5703  JSR $5CC7
$C0:5706  BRL $5CED
```

That means the routine:

1. sets up a descriptor-selected source
2. decompresses to `7F:2000`
3. calls `5CC7`
4. **tail-branches away** to `5CED`

So the large block of code at `570A+` is **not justified as immediate fall-through logic for `56D4`**.

That does **not** invalidate the decompression result itself, but it does mean any earlier claim that `56D4` immediately executed the `570A+` table-builder body was too strong.

---

## New solid findings

## `C3:08A4` — decompressor returns output length in `$06`

The decompressor epilogue does:

```asm
REP #$20
TYA
SEC
SBC $03
STA $06
...
RTL
```

So after `JSL $C3:0002`, the routine returns a decompressed output length in `DP+$06`.

That matters because `C0:5CC7` directly compares against `$0306`, which means it is making decisions based on the **actual decompressed size**, not some ROM-table size.

Best current helper name:

**`DecompressToWram_ReturnLength`** at the `C3:08A4` epilogue.

---

## `C0:5CC7` — `7F:2000` post-decompress signature/size dispatcher

This routine now has a much clearer role.

It immediately checks:

- `7F:2000`
- `7F:2001`
- decompressed size at `$0306`

Key patterns:

```asm
LDA.l $7F2000
CMP #$0D
...
LDA.l $7F2001
CMP #$0A
...
LDX #$1700
CPX $0306
...
```

So `5CC7` is a **post-decompression dispatcher** that keys off:

- the first two bytes of the `7F:2000` asset
- and the returned decompressed length

It has:

- a normal return path
- and two unusual long-branch paths back into older code around `C0:2E1C/2E1E`

Those branch targets are still unresolved and I am **not** pretending they are understood yet.

Best current name:

**`Asset7F2000_SignatureSizeDispatch`**

---

## `C0:5CED` — copies fixed template blocks into `7F:3700+`

After `56D4` runs `5CC7`, it tail-branches to `5CED`.

That routine is straightforward and strong enough to name.

It performs a series of `MVN $7F,$C0` block copies:

- `C0:5D37 -> 7F:3700`, length `0x20`
- `C0:5D50 -> 7F:3720`, length `0x20`
- `C0:5D50 -> 7F:3740`, length `0x20`
- `C0:5D50 -> 7F:3760`, length `0x20`
- `C0:5D68 -> 7F:3780`, length `0x06`

So this is a real fixed-template initializer, not parser noise.

Best current name:

**`Init_7F3700_TemplateBlocks`**

---

## `C0:A50A` — confirmed PPU display register loader

This is the strongest finding of the pass.

The routine does exactly this:

```asm
LDA $0BD7
STA $212C
LDA $0BD8
STA $212D
LDA $0BDF
STA $2131
LDA #$00
STA $2106
RTS
```

Those hardware registers are SNES PPU display registers:

- `212C` = main screen designation (`TM`)
- `212D` = sub screen designation (`TS`)
- `2131` = color math selection (`CGADSUB`)
- `2106` = mosaic

That means the values parsed earlier by `A33B` are definitely feeding **live display-layer configuration**, not some abstract game-only flags.

Best current name:

**`Apply_DisplayConfig_ToPpu`**

---

## `C0:A520` — reads layer/map data through the WRAM port into working buffers

This routine is still a bit messy, but its overall shape is now clear.

It:

1. sets up the WRAM port address via `2181/2183`
2. uses parsed size values from `0BCB/0BCD/0BCF/0BD1`
3. repeatedly reads bytes from `2180`
4. stores them into WRAM working buffers rooted at:
   - `7E:3000`
   - `7E:3040`
   - `7E:3080`
   - and `7E:7000`-series destinations

Representative write patterns:

```asm
LDA $2180
STA.l $7E3000,X
...
LDA $2180
STA.l $7E3040,X
...
LDA $2180
STA.l $7E3080,X
```

This is exactly the sort of routine you expect after parsing BG/layout dimensions: it is pulling structured data through the WRAM port into layer-oriented working buffers.

Best current name:

**`Read_DisplayBuffers_FromWramPort`**

---

## `C0:A33B` is now strongly identified as a display / BG config packet parser

Because of the `A50A` and `A520` findings, `A33B` can now be described much more precisely.

It still starts as a descriptor-selected decompression into `7E:B500`, but the post-parse behavior is now much clearer.

### Packet bytes at `7E:B500+` drive display-layer state

The routine reads bytes from:

- `7E:B500`
- `7E:B501`
- `7E:B502`
- `7E:B503`
- `7E:B504`
- `7E:B505`

and breaks them into bitfields.

### Strong mappings now supported

#### `7E:B504` feeds main/sub screen layer masks

`A33B` parses `7E:B504` into:

- `0BD7`
- `0BD8`

and later `A50A` writes those to:

- `212C`
- `212D`

So `B504` is definitely part of the **screen layer enable/mask configuration** path.

#### `7E:B505` feeds color math configuration

`A33B` loads `7E:B505` into:

- `0BDF`
- `0BE0`

and `A50A` writes `0BDF` to `2131`.

So `B505` is definitely part of the **color math / blending configuration** path.

#### `7E:B500` and `7E:B501` feed dimension/control fields

The code derives the following globals from packed 2-bit/flag fields:

- `0BCB`
- `0BCD`
- `0BCF`
- `0BD1`
- `0BD3`
- `0BD5`
- `0BC9`
- `0BCA`

The derived size-like fields land in the set:

- `0x10`
- `0x20`
- `0x30`
- `0x40`

which is exactly the sort of quantized value pattern you expect for **BG/tilemap dimensions or page geometry**, not arbitrary gameplay stats.

### Best current interpretation

`A33B` is no longer best described as just “decompress to `7E:B500` and parse.”

It is now best described as:

**descriptor-selected display/BG config packet decompress + parse**

Best current name:

**`DescriptorDecompress_DisplayConfig_To7EB500_AndParse`**

---

## Current project-state improvement

The bank-`C0` startup/load path is now cleaner in two important ways:

### 1. `7E:B500` is tied to real PPU/display setup

That gives us our first solid high-level subsystem identity.

### 2. `7F:2000` now has a corrected post-decompress control-flow picture

Instead of pretending the big `570A+` body belongs to `56D4`, the path is now:

```text
DescriptorDecompress_Group0008_To7F2000_AndBuild
 -> JSL C3:0002
 -> Asset7F2000_SignatureSizeDispatch
 -> Init_7F3700_TemplateBlocks
 -> return
```

That is much more trustworthy than forcing a false fall-through interpretation.

---

## Best current labels after this pass

```text
$C0:5CC7  Asset7F2000_SignatureSizeDispatch
$C0:5CED  Init_7F3700_TemplateBlocks
$C0:A50A  Apply_DisplayConfig_ToPpu
$C0:A520  Read_DisplayBuffers_FromWramPort
$C0:A33B  DescriptorDecompress_DisplayConfig_To7EB500_AndParse
$C3:08A4  DecompressToWram_ReturnLength
```

---

## Best next move

The highest-value next pass is now either:

1. trace who consumes the `7F:3700` template blocks and `7F:2000` signature-dispatch results
2. or finish decoding the `C3:0557` command families so the compression format itself is better defined

Right now the **display/BG config lane** is the cleanest subsystem lead.
