# Chrono Trigger (USA) — Disassembly Pass 17

## What this pass focused on

This round drilled directly into the four render-class branches under:

- `C0:B309`
- `C0:B701`

The goal was to answer:

- what the four `1201 & 3` render classes actually mean in practice
- how many OAM records each class emits
- whether the three OAM cursor sets are real sub-buffers/bands
- what `1700`, `4BC0`, `4F00`, `4F80`, and `4B40` are doing in the per-slot render path

---

## Biggest conclusion

## The low two bits of `1201` select a **fixed metasprite size class**

This is now the cleanest read on the render-class system.

From the four class-local emitters under `B309`:

- class `0` emits **4 low-OAM records** and **1 high-table byte**
- class `1` emits **8 low-OAM records** and **2 high-table bytes**
- class `2` emits **12 low-OAM records** and **3 high-table bytes**
- class `3` emits **24 low-OAM records** and **6 high-table bytes**

That is far too regular to be accidental.
These are real fixed-size metasprite classes.

So `1201 & 3` is no longer just "some render-class selector."
It is strongly the **metasprite size/layout class**.

### Strong new labels
- `C0:B329  Emit_Class0_4SpriteMetasprite_ToSelectedOamBand`
- `C0:B3DF  Emit_Class1_8SpriteMetasprite_ToSelectedOamBand`
- `C0:B4B8  Emit_Class2_12SpriteMetasprite_ToSelectedOamBand`
- `C0:B5AF  Emit_Class3_24SpriteMetasprite_ToSelectedOamBand`
- `$1201,X  SlotMetaspriteClassFlags`

---

## Each render class has the same 3-way OAM band select

All four class emitters begin by checking:

- `LDA $0F80,X`
- `AND #$0C`

and then choosing one of three cursor pairs:

- high cursor at `0181`, low cursor at `01DB`
- high cursor at `0185`, low cursor at `01DD`
- high cursor at `0189`, low cursor at `01DF`

### Actual branch behavior
The mapping is:

- masked value `00` -> cursor set **A**
- masked value `08` -> cursor set **C**
- masked value `04` or `0C` -> cursor set **B**

That means bits `2-3` of `0F80` are definitely not random.
They select which OAM sub-buffer / band this slot emits into.

I am still not pretending I know whether these are priority bands, actor groups, or a split tied to main/subscreen handling.
But they are absolutely real **band selectors**.

### New labels
- `$0F80,X  SlotOamBandFlags`
- `0181/01DB  OamBandA_HighAndLowCursors`
- `0185/01DD  OamBandB_HighAndLowCursors`
- `0189/01DF  OamBandC_HighAndLowCursors`

---

## `1700` is the low-OAM cache offset per slot

In every class emitter, after choosing the output cursor, the routine does:

- `LDA $1700,X` (16-bit)
- `TAX`

That offset is then used to walk cached render records from `7F:4BC0`.

The class-local loops all advance that offset by `+8` each iteration.

### What that means
`1700,X` is not generic slot state.
It is strongly the **per-slot low-OAM cache offset / metasprite-record offset**.

### New label
- `$1700,X  SlotLowOamCacheOffset`

---

## The class loops all pull low-OAM bytes from `7F:4BC0` on an 8-byte stride

This is the common class pattern:

- set WRAM write address from the chosen low cursor
- set iteration count
- read from `7F:4BC0 + offset`
- write four bytes through the WRAM port (`$2180`)
- advance source offset by `+8`
- repeat

The four copied bytes are always:

- `+0`
- `+1`
- `+6`
- `+7`

for each 8-byte source stride.

### Record counts by class
- class 0: loop count `4`, cursor advance `+0x10`
- class 1: loop count `8`, cursor advance `+0x20`
- class 2: loop count `12`, cursor advance `+0x30`
- class 3: loop count `24`, cursor advance `+0x60`

This lines up exactly with 4 bytes written per sprite record.

### Stronger read
`7F:4BC0` is no longer just "some metasprite template area."
It is behaving like a **prepared low-OAM cache** that the final emitter copies into the selected OAM band.

### Updated label
- `$7F:4BC0  SlotLowOamCacheRecords`

---

## The high-table bytes come from a class-sized cache, not directly from the template loop

Each class writes a fixed number of bytes into the high-table cursor before copying low-OAM records.

### Class 0
Writes **1 byte**:
- `7F:4F00`

### Class 1
Writes **2 bytes**:
- `7F:4F00`
- `7F:4F01`

### Class 2
Writes **3 bytes**:
- `7F:4F00`
- `7F:4F01`
- `7F:4B40`

### Class 3
Writes **6 bytes**:
- `7F:4F00`
- `7F:4F01`
- `7F:4B40`
- `7F:4B41`
- `7F:4F80`
- `7F:4F81`

### What that means
These addresses are not interchangeable scratch bytes.
They are a real **per-slot cached OAM high-table / size-bit payload**, and larger classes reserve more of it.

### Stronger labels
- `$7F:4F00  SlotOamHighCache_Byte0`
- `$7F:4F01  SlotOamHighCache_Byte1`
- `$7F:4B40  SlotOamHighCache_Byte2`
- `$7F:4B41  SlotOamHighCache_Byte3`
- `$7F:4F80  SlotOamHighCache_Byte4`
- `$7F:4F81  SlotOamHighCache_Byte5`

I am keeping the names generic because I have not fully proven which exact high-table bitfields each byte carries, but their role as cached high-table payload is now strong.

---

## `B701` is a real class-aware render-prep gate, with class-specific staging thresholds

The earlier pass already identified `B701` as the render-prep / skip gate.
This pass makes the structure much more specific.

### Common front-end
For classes 0-2, the gate first reads:

- `LDA $1B00,X`

If zero:
- return `SEC` -> skip emission

Otherwise:
- positive states and negative states are handled differently

### Class-specific thresholds
For the positive-state path, the classes gate on progressively larger thresholds:

- class 0: prepare path for any positive nonzero state
- class 1: prepare path only when state `>= 2`
- class 2: prepare path only when state `>= 3`

The negative-state path masks off the sign bit and uses matching class-local thresholds before either:

- re-running the class prep path
- or using a smaller class-local helper and returning `CLC`

### What that means
`1B00` is not a simple visible/hidden flag.
It is a real **render-prep stage/state byte**, and its interpretation depends on metasprite class.

### Stronger labels
- `C0:B701  Gate_AndPrepare_CurrentSlotMetaspriteByClass`
- `$1B00,X  SlotRenderPrepStage`

---

## The class-local prep builders line up with the emit sizes

The helpers called from `B701` for the first three classes are:

- class 0 -> `C0:B8CA`
- class 1 -> `C0:BCDC`
- class 2 -> `C0:C2BF`

These helpers all build data into the same `7F:4BC0 / 7F:4F00 / 7F:4B40 / 7F:4F80` cache family, but with progressively larger payloads matching the class size.

That means the architecture is now much cleaner:

1. `B701` checks whether the slot's cached metasprite data is ready
2. if needed, it runs the class-specific cache builder
3. `B309` then copies the prepared cache into one of the three OAM bands

So the final emitter is **not** assembling everything from scratch.
It is copying from a class-sized render cache.

### New labels
- `C0:B8CA  Build_Class0_RenderCache`
- `C0:BCDC  Build_Class1_RenderCache`
- `C0:C2BF  Build_Class2_RenderCache`

I am still leaving the class-3 prep builder unnamed here because `B701` tail-calls out of the local block for that case and I have not finished mapping its exact entry/exit contract yet.

---

## Why this matters architecturally

The render pipeline is now much less vague:

1. slot VM / movement system updates active slots
2. slots are rebucketed into camera-relative render buckets
3. bucket traversal chooses slots in render order
4. `B701` ensures the slot's class-sized render cache is ready
5. `B309` copies the cached metasprite payload into the selected OAM band
6. trailing unused records are hidden

That is a real engine subsystem now, not just "sprite stuff happens somewhere in B2xx-B7xx."

---

## What is now substantially stronger

### Strong now
- the four render classes are fixed metasprite-size classes
- class sizes are 4 / 8 / 12 / 24 low-OAM records
- the high-table payload sizes are 1 / 2 / 3 / 6 bytes
- `0F80 & 0x0C` selects one of three OAM bands
- `1700` is a per-slot low-OAM cache offset
- `4BC0` is a prepared low-OAM cache record area
- `4F00/4F01/4B40/4B41/4F80/4F81` are cached high-table payload bytes
- `B701` is a class-aware render-prep/staging gate
- `B8CA / BCDC / C2BF` are render-cache builders, not generic helpers

### Still not fully solved
- exact semantic meaning of the three OAM bands
- exact bitfield layout of the cached high-table bytes
- full class-3 prep builder entry point / staging contract
- why the low-cache source stride is 8 bytes while the final OAM write stride is 4 bytes

---

## Best next target

The cleanest next step is to finish the **class-3 cache builder** and then decode the cache record layout itself.

That should answer:

- what each byte in the 8-byte low-cache stride really means
- whether the bands correspond to priority, layer, actor type, or some more specific render partition
- how the largest 24-sprite metasprite class is staged before emission
