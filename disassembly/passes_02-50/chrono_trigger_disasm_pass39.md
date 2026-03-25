# Chrono Trigger (USA) — Disassembly Pass 39

## Scope
This pass continues directly from pass 38 and stays on the exact seam it identified:

- the wrapper/parameterization layer above the now-decoded service-7 geometric bodies
- the opcode wrapper table at `C1:1FF8`
- the wrapper family spanning `C1:203A..22F5`
- the result-cursor helpers at `C1:27FA`, `C1:2814`, and `C1:282D`
- the packet / state bytes that this layer materially strengthens

The goal of this pass was to stop treating the `2029..22F5` area as a vague “wrapper band” and pin which wrappers are:

- plain candidate collectors,
- direct scalar selectors,
- packet builders for `25A3`, `2701`, and `2332`,
- and result-cursor helpers layered on top of the service-7 result vector.

This pass does **not** claim final gameplay-facing names for the numeric slot classes in `$2980`.
The bytes prove a discriminator field is being used there, but they do not yet prove the human-facing class names for values `03`, `04`, `05`, and `06`.

---

## Baseline carried forward from pass 38
Pass 38 had already established:

- service `#07` is a sub-dispatched candidate-query family in bank `C1`
- the real geometry bodies are:
  - `2332` = seeded band scan on `$1D23`
  - `23A4` = three-vertex inclusion scan
  - `25A3` = dual-anchor oriented inclusion scan
  - `2701` = seeded cell-radius scan using `dx^2 + dy^2`
- `$9604..$9608` are the packet bytes consumed by those bodies
- `27D9` / `27E8` are the clear/finalize helpers for the service-7 result vectors

What remained open was the wrapper layer that chooses those bodies, preloads packet bytes, rotates result selection, and decides whether to return only one scalar result or a mirrored whole vector.

---

## What was done in this pass
1. Re-traced the wrapper dispatch that indexes via `C1:1FF8`
2. Decoded the shared scan wrapper family rooted at `C1:203A`
3. Decoded the scalar wrappers at `20D6`, `20E0`, `2136`, and `2163`
4. Decoded the packet-building wrappers for `25A3`, `2701`, and `2332`
5. Decoded `27FA`, `2814`, and `282D` as result-cursor helpers
6. Strengthened the roles of `$960A`, `$960C`, `$960D`, `$960F`, `$9613`, `$9614`, and `$2980`

---

## Core results

### 1. `C1:1FF8` is the real 33-entry service-7 wrapper table
The bytes immediately above the table are now strong enough to pin the wrapper dispatch:

```text
LDA $960D
AND #$7F
CMP #$21
BCC +
  LDA #$20
+ ASL A
TAX
JSR ($1FF8,x)
```

So the service-7 wrapper selector is:

- `($960D & 0x7F)`
- clamped to `0x20`
- multiplied by 2
- then `JSR`’d through `C1:1FF8`

This means `C1:1FF8` is **not** a random table near service 7.
It is the actual opcode wrapper table for the outer service-7 command layer.

That also means `$960D & 0x7F` is no longer just some generic command byte.
For this family it is the **wrapper opcode**.

---

### 2. The outer post-wrapper tail caches the first live mirrored result into `$9613`
Immediately after the wrapper returns, the outer code does:

```text
TDC
TAX
loop:
  LDA $A62D,x
  BPL found
  INX
  CPX #$000B
  BNE loop
found:
STA $9613
RTS
```

So the outer service-7 wrapper layer always scans the mirrored result vector at `$A62D..` and stores:

- the first non-negative entry if one exists, or
- the terminal negative value if no valid result is found

Safest reading:

> `$9613` = **outer service-7 cached first-live result / failure marker**

This is stronger than treating `$9613` as an untyped scratch byte.

---

### 3. `C1:203A` is the shared eligible-slot collector for the fixed-range scan wrappers
This routine turned out to be the common body behind several table entries.

Its structure is:

```text
caller supplies:
  $80 = exclusive upper bound
  X   = initial slot index
  optional: bit7 of $960C preset to request whole-vector mirror

INC $960A
TDC
TAY
loop over X .. ($80-1):
  require $96F5,x != 0
  require $9FF7,x >= 0
  apply an extra gate through $A0A8/$A09B for one opcode case
  if x == $960F:
    STA $99C0
  else:
    STA $99C1,y
    INY
finish via JSR $27C5
load cursor-selected result $99C0[$9614] -> $A62D
if bit7($960C) set:
  mirror entire $99C0.. -> $A62D..
RTS
```

The important part is not the exact unresolved meaning of `$A0A8/$A09B` yet.
The important part is that `203A` is now structurally pinned as a **bounded eligible-slot collector** with:

- caller-selected start/end range,
- preferred-slot preservation through `$960F`,
- optional whole-vector mirror through `$960C.7`.

So the wrappers that land here are no longer “mystery query stubs.”
They are parameter variants of the same collector.

---

### 4. `209A`, `20A9`, `20B6`, and `20C6` are just range/mirror variants of `203A`
These wrappers set up different bounds and mirror behavior before falling into the common collector.

#### `C1:209A`
- sets upper bound to `3`
- starts at slot `0`
- sets `$960C = 0x80`
- then joins `203A`

Safest reading:

> **first-three-slot eligible collector with whole-vector mirror enabled**

#### `C1:20A9`
- sets upper bound to `11`
- starts at slot `3`
- then joins `203A`

Safest reading:

> **later-partition eligible collector (slots `3..10`)**

#### `C1:20B6`
- sets upper bound to `11`
- starts at slot `3`
- sets `$960C = 0x80`
- then joins `203A`

Safest reading:

> **later-partition eligible collector with whole-vector mirror enabled**

#### `C1:20C6`
- sets upper bound to `11`
- starts at slot `0`
- sets `$960C = 0x80`
- then joins `203A`

Safest reading:

> **full-range eligible collector with whole-vector mirror enabled**

This is a real cleanup of the wrapper layer: these entries are not different query engines; they are bounded setup variants of one shared collector.

---

### 5. `C1:20D6` is the direct passthrough scalar-result wrapper
The body is minimal:

```text
LDA $95D5
STA $99C0
STA $A62D
RTS
```

So this wrapper does not scan anything and does not build a vector.
It directly seeds result slot 0 and its mirror from `$95D5`.

Safest reading:

> `C1:20D6` = **direct current-slot / direct-source passthrough wrapper via `$95D5`**

The exact outward name of `$95D5` is still not proven here, so the label should stay source-neutral.

---

### 6. `C1:20E0` is a first-three-slot flagged-state scan, not a generic collector
This routine is separate from `203A` and explicitly inspects only the first three slots.

Observed structure:

- increments `$960A`
- checks slot `0`, `1`, `2` individually through:
  - `$96F5`
  - `$A09B/$A09C/$A09D`
  - sign bit of `$5E4A/$5ECA/$5F4A`
- appends literal slot numbers `0`, `1`, `2` into `$99C0+`
- if the selected scalar result is negative, writes `0x80` to `$9613`
- exports the cursor-selected result to `$A62D`

Safest reading:

> `C1:20E0` = **first-three-slot negative-flag state scan**

This is materially stronger than “some actor-state wrapper.”
The routine is checking explicit sign bits on fixed per-slot flag bytes.

---

### 7. `C1:2136` and `C1:2163` are first-three-slot discriminator scans on `$2980`
These two wrappers are siblings.
They only differ in the literal discriminator value loaded into `$80` before sharing the same body.

#### `C1:2136`
Loads `#$05` into `$80`, then scans slots `2 -> 0` for the first slot where:

- `$96F5,x != 0`
- `$A09B,x == 0`
- `$2980,x == 5`

If found, it writes that slot to both `$99C0` and `$A62D`.
Otherwise it writes `0x80` to `$9613`.

#### `C1:2163`
Same structure, but loads `#$04` instead.

So these are not geometry wrappers at all.
They are fixed first-three-slot discriminator selectors.

Safest reading:

> `2136` = **first-three-slot `$2980 == 5` selector**
>
> `2163` = **first-three-slot `$2980 == 4` selector**

This is enough to treat `$2980` as a real slot discriminator/class byte, even though the human-facing names for values `4/5` remain unresolved.

---

### 8. `27FA`, `2814`, and `282D` are the result-cursor helpers layered above `$99C0..`
These helpers are now fully structural.

#### `C1:282D`
This routine scans `$99C0..$99CA` for any non-`FF` entry.
If at least one live entry exists, it returns with Z clear.
If the whole vector is empty, it returns with Z set.

Safest reading:

> `282D` = **service-7 result-vector any-live probe**

#### `C1:27FA`
Structure:

```text
JSR $282D
BEQ done_if_empty
loop:
  INC $9614
  if $9614 == 0x0B: wrap to 0
  if $99C0[$9614] is negative: repeat
RTS
```

Safest reading:

> `27FA` = **advance `$9614` to the next live result entry with wraparound**

#### `C1:2814`
Same structure, but decrements and wraps from `0 -> 10`.

Safest reading:

> `2814` = **move `$9614` to the previous live result entry with wraparound**

This is a major cleanup because it means `$9614` is now strongly pinned as the **service-7 result cursor index**.

---

### 9. `2169`, `21AF`, and `2203` are packet-building wrappers for the dual-anchor scan at `25A3`
All three wrappers share the same broad shape:

1. build a later-partition candidate vector with `20A9`
2. clear `$960A`
3. optionally rotate the result cursor through `27FA` or `2814`, gated by bits in `$EF`
4. preload packet bytes `$9604..$9608`
5. call `25A3`
6. finalize via `27E8`

The differences are in how they choose the anchor pair and whether `$9608` is `0` or `1`.

#### `C1:2169`
Preloads:
- `$9604 = 0`
- `$9605 = $960F`
- `$9606 = $99C0[$9614]`
- `$9607 = 2`
- `$9608 = 0`

#### `C1:2203`
Same as `2169`, except:
- `$9608 = 1`

#### `C1:21AF`
Same outer shape, but chooses `$9605` by scanning slots `0..2` for the first `$2980 == 3` entry before preloading the rest of the packet.

Safest reading:

> `2169 / 2203 / 21AF` = **wrapper family that builds dual-anchor packet variants for `25A3` after optional cursor rotation**

That is now stronger than the pass-38 generic “wrappers around 25A3.”
These are explicit packet constructors with stable anchor-selection patterns.

---

### 10. `224B`, `225F`, `22A4`, and `22D3` are packet-building wrappers for the radius scan at `2701`
These wrappers all end by preloading a seed slot into `$9605`, a threshold into `$9607`, then calling `2701` and finalizing through `27E8`.

#### `C1:224B`
Preloads:
- `$9604 = 0`
- `$9605 = $960F`
- `$9607 = 0x10`

So this is the direct seeded-radius wrapper around the `$960F` slot.

#### `C1:225F`
Outer shape:
- build later-partition vector via `20A9`
- optionally rotate cursor via `27FA` or `2814` depending on `$EF`
- use `$99C0[$9614]` as `$9605`
- set `$9607` to:
  - `0x19` when `($960D & 0x7F) == 0x1A`
  - otherwise `0x09`
- call `2701`

So one wrapper body serves two opcodes with different thresholds.

#### `C1:22A4`
Scans slots `0..2` for the first `$2980 == 3` slot and uses that as `$9605`.
Then sets `$9607` to:
- `0x19` when `($960D & 0x7F) == 0x14`
- otherwise `0x10`

Then calls `2701`.

#### `C1:22D3`
Scans slots `0..2` for the first `$2980 == 6` slot, uses that as `$9605`, sets `$9607 = 0x19`, then calls `2701`.

Safest reading:

> `224B / 225F / 22A4 / 22D3` = **wrapper family that builds seeded-radius packet variants for `2701` using different seed sources and threshold literals**

---

### 11. `C1:22F5` is the band-scan wrapper for `2332`
This wrapper shares the same outer pattern as `225F`:

- build later-partition candidate vector with `20A9`
- optionally rotate cursor via `27FA` or `2814`, gated by `$EF`
- set `$9604 = 0`
- set `$9605 = $99C0[$9614]`
- call `2332`
- finalize via `27E8`

So it is not just “another wrapper near 2332.”
It is the explicit **cursor-selected seeded-band wrapper** for the already-solved `2332` body.

---

### 12. `C1:232A` is a direct no-packet-adjust triangle wrapper for `23A4`
Immediately after the table-driven region sits:

```text
STZ $9604
JSR $23A4
JMP $27E8
```

So there is also a clean direct wrapper around the triangle/polygon inclusion scan.

I am keeping this separate from the `1FF8` table claims because the table entry at `0x18` lands at `2329` (`RTS`), not at `232A`.
So `232A` is real code with clear meaning, but it should not be mislabeled as a table entry for opcode `0x18` without an additional xref pass.

---

## Strengthened state-byte interpretations

### `$960D`
Now strong as:

> **service-7 wrapper opcode byte (low 7 bits)**

### `$9614`
Now strong as:

> **service-7 result cursor index**

### `$960C.7`
Now materially stronger than in pass 37.
The common collector at `203A` uses sign of `$960C` to decide whether to mirror the whole vector `99C0.. -> A62D..`, and `27E8` also sets `$960C = 0x80` before mirroring.

Safest reading:

> **service-7 whole-vector mirror/valid flag family**

### `$960A`
Still not fully named, but its pattern is much tighter now:

- incremented by the bounded collector and several scalar wrappers
- explicitly cleared before cursor-rotation-driven wrapper reuse

Safest reading:

> **service-7 local scan/query counter or epoch byte**

### `$960F`
Still generic in human terms, but structurally stronger:

- preserved specially by the common collector
- used directly as the seed/anchor slot by several wrappers

Safest reading:

> **service-7 preferred/seed slot parameter**

### `$2980`
Now strong as a slot discriminator/class byte, because wrappers explicitly search for first-three slots with exact values `3`, `4`, `5`, or `6`.

The human-readable meaning of those numeric classes is still open.

---

## Wrapper opcode map (`C1:1FF8`)
This is the current safe map of the 33 wrapper-table entries.
Names stay structural rather than gameplay-facing.

```text
00 -> 203A  first-three eligible collector
01 -> 209A  first-three eligible collector + whole-vector mirror
02 -> 20D6  direct passthrough scalar wrapper via $95D5
03 -> 20E0  first-three negative-flag state scan
04 -> 209A  same as 01
05 -> 2136  first-three $2980 == 5 selector
06 -> 2163  first-three $2980 == 4 selector
07 -> 20A9  later-partition eligible collector
08 -> 20B6  later-partition eligible collector + whole-vector mirror
09 -> 20C6  full-range eligible collector + whole-vector mirror
0A -> 20B6  same as 08
0B -> 2169  later-partition + rotated dual-anchor packet (toggle 0)
0C -> 2203  later-partition + rotated dual-anchor packet (toggle 1)
0D -> 21AF  class-3 anchor + rotated dual-anchor packet
0E -> 203A  same as 00
0F -> 22F5  later-partition + rotated seeded-band wrapper
10 -> 203A  same as 00
11 -> 224B  direct seeded-radius wrapper around $960F
12 -> 225F  rotated seeded-radius wrapper (threshold 09h)
13 -> 22A4  class-3 seeded-radius wrapper (threshold 10h)
14 -> 22A4  class-3 seeded-radius wrapper (threshold 19h)
15 -> 203A  same as 00
16 -> 203A  same as 00
17 -> 203A  same as 00
18 -> 2329  RTS / no additional wrapper body at this table slot
19 -> 203A  same as 00
1A -> 225F  rotated seeded-radius wrapper (threshold 19h)
1B -> 22D3  class-6 seeded-radius wrapper (threshold 19h)
1C -> 203A  same as 00
1D -> 203A  same as 00
1E -> 203A  same as 00
1F -> 203A  same as 00
20 -> 203A  same as 00
```

This is a real semantic gain because the wrapper table is no longer “lots of nearby code.”
It is now a mostly classified outer command map.

---

## Architectural consequences of pass 39

1. The service-7 layer is now visibly split into three tiers:
   - **wrapper opcode tier** (`1FF8`)
   - **packet-building / bounded-scan wrapper tier** (`203A..22F5`)
   - **geometry body tier** (`2332/23A4/25A3/2701`)

2. `$9614` is no longer ambiguous scratch; it is the result cursor over the service-7 result vector.

3. `$960C.7` is materially closer to a true name: it is tied to whole-vector mirror/valid behavior, not just vague finalization.

4. `$2980` now belongs in the architecture map as a real slot discriminator/class byte.

5. The unresolved work is no longer “what do the service-7 bodies do?”
   That part is mostly done.
   The remaining ambiguity is:
   - the human-facing meaning of `$2980 == 3/4/5/6`
   - the exact source meaning of `$95D5`
   - the extra gate through `$A0A8/$A09B` inside the common collector
   - the xref/use-case layer above these wrapper opcodes

---

## What remains unresolved after pass 39

### Still open
- exact human-readable class names for `$2980` values `03`, `04`, `05`, `06`
- exact semantic meaning of `$95D5`
- exact meaning of the extra collector gate using `$A0A8/$A09B`
- the call sites / higher-level opcode users that decide *which* wrapper opcode to place in `$960D`
- whether table slot `0x18 -> 2329` is an intentional no-op/retain-current-results opcode or just one entry in a larger outer flow that expects `232A` from elsewhere

### Best next continuation point
The cleanest next seam is now **above** the wrapper table:

- trace the callers that preload `$960D`, `$960F`, `$9614`, and `$EF`
- identify what higher-level command families select wrapper opcodes `0B/0C/0D/0F/11/12/13/14/1A/1B`
- resolve the human-facing slot-class meaning of `$2980`

That is the shortest path from structural wrapper names to true subsystem names.
