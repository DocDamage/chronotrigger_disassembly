# Chrono Trigger (USA) — Disassembly Pass 4

## What this pass focused on

This pass went after the biggest unresolved question from the previous round:

**what is `$C3:0002` actually doing?**

That question matters because several descriptor-driven loaders in bank `C0` build source/destination pointers and then call:

```asm
JSL $C3:0002
```

This pass confirms that the routine is **not** a generic memcpy.

It is the game's **core WRAM decompression / block expansion engine**, and it is clearly part of Chrono Trigger's proprietary compressed asset path.

---

## Strong new findings

## `$C3:0002` — entry is just a jump to the real core

The first bytes at the published entry are:

```asm
$C3:0002  JMP $0557
```

So the actual work starts at **`$C3:0557`**.

That means the name attached to `$C3:0002` should reflect the behavior of `$C3:0557`, not some imagined generic dispatcher role.

Best current name:

**`DecompressToWram_Core`**

---

## `$C3:0557` — proven WRAM decompression core

This routine is now strong enough to name with confidence.

### Why this is no longer speculative

The routine does all of the following:

- sets **direct page = `$0300`**
- uses caller-supplied values in `$0300-$0305`
- writes destination address through the SNES **WRAM port registers**
  - **`$2181/$2182`** = WRAM address low/high
  - **`$2183`** = WRAM bank (`7E` / `7F`)
  - **`$2180`** = WRAM data port
- reads a stream from a banked source pointer
- interprets control bytes rather than blindly copying data
- performs **in-place history copies** with:
  - `MVN $7E,$7E`
  - `MVN $7F,$7F`

Those same-bank `MVN` copies are the killer detail:
they show this routine is copying **already-decompressed bytes from earlier in the destination buffer**, which is textbook **LZ-style backreference behavior**.

That proves this routine is doing **decompression / expansion**, not plain transfer.

---

## Concrete evidence inside `$C3:0557`

### 1. Destination is WRAM, not ROM or VRAM

The routine loads the caller's destination pointer from DP and pushes it into the WRAM port:

```asm
LDA $03
STA.l $002181   ; sets WRAM address low/high
...
LDA $05
STA.l $002183   ; selects bank 7E or 7F
```

Then it repeatedly writes bytes through:

```asm
STA.l $002180
```

So the output target is definitely **WRAM**.

---

### 2. The stream is command-driven

Early in the routine, it fetches a source byte and masks the top bits:

```asm
LDA ($09)
AND #$C0
```

The code then takes different branches depending on those top bits and the target bank (`7E` vs `7F`).

That means the input stream is structured into **commands / block types**, not raw data.

---

### 3. It has literal copy paths

Multiple blocks in the routine perform direct writes of sequential source bytes into `$2180`, i.e. literal writes into WRAM.

Representative pattern:

```asm
LDA $0001,X
STA.l $002180
LDA $0002,X
STA.l $002180
...
```

So part of the format is definitely **literal data emission**.

---

### 4. It has backreference copy paths

This is the most important part.

One branch computes a length/offset pair and then executes:

```asm
MVN $7E,$7E
```

and a sister path executes:

```asm
MVN $7F,$7F
```

That is a **copy from earlier destination bytes to later destination bytes within the same WRAM bank**.

That is not something a simple block transfer helper would do.
It is exactly what you expect from an **LZ-family decompressor**.

---

## Best current interpretation of the format

I am **not** claiming the exact codec name yet, but the mechanics now support this statement:

- the routine consumes a **Chrono Trigger proprietary compressed stream**
- the stream contains:
  - literal-write commands
  - backreference/history-copy commands
  - likely multiple command families chosen by the upper control bits
- the output is decompressed directly into **WRAM bank `7E` or `7F`**

That lines up with existing Chrono Trigger hacking references saying the game uses a **proprietary compression scheme**. Chrono Compendium's utilities page explicitly notes that **Chrono Compressor** uses Evil Peer’s algorithm because CT uses a proprietary compression format, and Bisqwit's Chronotools page states the project's **compression algorithms are fully implemented**. citeturn496565search4turn784551search2

---

## What this changes in the bank `C0` loader analysis

Several routines previously labeled only as "descriptor loaders" now have stronger identities because they all prepare parameters for this decompressor.

## `$C0:6DCF`

Confirmed setup pattern:

- reads selector from **`F6:0002`**
- builds a source pointer from **`F6:2220+`**
- sets destination to:
  - **`$7F:5000`**
- calls:
  - **`JSL $C3:0002`**

Best current interpretation:

**decompress descriptor-selected asset block into `7F:5000`**

Safe name for now:

**`DescriptorDecompress_Group0002_To7F5000`**

---

## `$C0:A33B`

Confirmed setup pattern:

- reads selector from **`F6:0004`**
- builds a source pointer from **`F6:1E00+`**
- sets destination to:
  - **`$7E:B500`**
- calls:
  - **`JSL $C3:0002`**
- immediately parses bytes at **`7E:B500+`** into many runtime flags / config bytes

Best current interpretation:

**decompress descriptor-selected config/header-like data into `7E:B500`, then parse it**

Safe name for now:

**`DescriptorDecompress_Group0004_To7EB500_AndParse`**

---

## `$C0:56D4`

Confirmed setup pattern:

- reads selector from **`F6:0008`**
- builds a source pointer from **`FC:F9F0+`**
- sets destination to:
  - **`$7F:2000`**
- calls:
  - **`JSL $C3:0002`**
- then immediately begins iterating over the decompressed data

Best current interpretation:

**decompress descriptor-selected table data into `7F:2000`, then build runtime structures from it**

Safe name for now:

**`DescriptorDecompress_Group0008_To7F2000_AndBuild`**

---

## What I am still not claiming

Still avoiding fake precision on these points:

- exact formal name of the CT compression codec
- exact meaning of each command family inside the stream
- exact semantic identity of the assets loaded by groups `0002`, `0004`, and `0008`

Those are the next layer, but the core behavior is now solid.

---

## Stronger project state after this pass

The disassembly now has a real asset-loading backbone:

```text
Select_InitDescriptor_14Byte
 -> Run_InitDescriptorLoaders
    -> descriptor-specific setup
    -> DecompressToWram_Core (C3:0002 -> C3:0557)
    -> parse / copy / queue follow-up data
```

That is a major improvement over "generic block transfer" because it gives us a real framework for identifying higher-level systems.

---

## Best current labels after this pass

```text
$C3:0002  DecompressToWram_Core
$C3:0557  DecompressToWram_LZCore
$C0:6DCF  DescriptorDecompress_Group0002_To7F5000
$C0:A33B  DescriptorDecompress_Group0004_To7EB500_AndParse
$C0:56D4  DescriptorDecompress_Group0008_To7F2000_AndBuild
```

---

## Best next move

The highest-value next step is:

1. identify the exact stream command families inside `$C3:0557`
2. map which descriptor groups feed which asset classes
3. trace where `7F:5000`, `7E:B500`, and `7F:2000` are consumed later

That will let the next pass replace destination-based names with actual subsystem names.
