# Chrono Trigger (USA) — Disassembly Pass 18

## What this pass focused on

This round finished the two loose ends from the previous pass:

- the missing **class-3 render-cache builder** hanging off `C0:B701`
- the exact role of the helper at `C0:C6E7`

The goal was to stop saying “class 3 probably has a bigger builder somewhere” and instead pin down:

- where the class-3 builder really starts
- how it derives the **6 high-table bytes** needed for a 24-sprite metasprite
- what the cached 8-byte sprite records in `7F:4BC0` actually look like

---

## Biggest conclusion

## `C0:C73E` is the missing **class-3 render-cache builder**

The class selector in `C0:B701` falls through to a `BRL` into bank-local code at `C0:C73E` for class `3`.

That routine is not some generic helper.
It is the real **24-sprite class render-cache builder**.

### Why this is strong

`C0:C73E` does all of the things the first three class builders do, but scaled up for class 3:

- reads per-slot camera/screen-relative anchor state from `0A00/0A80`
- builds **6 cached OAM high bytes**
- finalizes **24 cached low-OAM Y bytes**
- writes into the same `7F:4BC0 / 4F00 / 4B40 / 4F80` cache family used by the smaller classes

That makes the class mapping much cleaner:

- `B8CA` = class 0 cache builder
- `BCDC` = class 1 cache builder
- `C2BF` = class 2 cache builder
- `C73E` = class 3 cache builder

### New label
- `C0:C73E  Build_Class3_RenderCache_24Sprites`

---

## `C0:C6E7` is the key helper: it packs 4 sprite-X words into low-OAM X bytes plus 1 OAM high byte

This helper is the real bridge between the cache records and the OAM high table.

### What it does

For one group of **4 sprite records**, `C0:C6E7`:

1. reads four **16-bit X work words** from:
   - `+02`
   - `+0A`
   - `+12`
   - `+1A`
2. adds the slot screen/camera-relative X anchor from `$C3`
3. stores each resulting **low 8 bits** into:
   - `+00`
   - `+08`
   - `+10`
   - `+18`
4. extracts the low bit of each result's high byte
5. packs those four bits into a single return byte
6. ORs that packed byte with `#$AA`
7. returns that final byte in `A`

### Why `#$AA` matters

`#$AA` means bits `1,3,5,7` are always set in the returned byte.

That is exactly what you would expect for a packed **OAM high-table byte** where each 2-bit pair carries:

- bit 0 / 2 / 4 / 6 = X MSB for one sprite
- bit 1 / 3 / 5 / 7 = sprite-size bit for that sprite

So `C6E7` is not just “some packer.”
It is a real:

**4-sprite X finalizer + OAM high-byte constructor**

### New label
- `C0:C6E7  Pack4SpriteXWords_AndBuildOamHighByte`

---

## Class 3 builds exactly 6 OAM high bytes because 24 sprites = 6 groups of 4

This is the cleanest mechanical proof from the class-3 builder.

`C0:C73E` calls `C0:C6E7` **six times**, stepping the source X register by `#$0020` each time.

That makes perfect sense:

- each cached sprite record is `8` bytes
- one `C6E7` call covers `4` records = `32` bytes = `#$20`
- class 3 uses `24` sprite records
- `24 / 4 = 6` packed high bytes

The six returned bytes are stored to:

- `7F:4F00`
- `7F:4F01`
- `7F:4B40`
- `7F:4B41`
- `7F:4F80`
- `7F:4F81`

That fully explains the class-3 high-table payload that the class-3 emitter later copies into the selected OAM band.

---

## This pass locks the working cache-record format much harder

The combined behavior of:

- the class builders
- `C6E7`
- the class emitters in `B309`

now gives a pretty solid field layout for each **8-byte cached sprite record** in the `7F:4BC0` family.

## Strong current read on the record format

For each 8-byte record:

- `+00` = finalized **low-OAM X** byte
- `+01` = finalized **low-OAM Y** byte
- `+02/+03` = 16-bit **X work word / relative X source**
- `+04` = 8-bit **Y work byte / relative Y source**
- `+05` = still unresolved
- `+06` = low-OAM **tile number** byte
- `+07` = low-OAM **attribute** byte

### Why this is strong

- emitters copy `+00,+01,+06,+07` into final low OAM
- `C6E7` consumes `+02/+03` and writes finalized `+00`
- class-local Y finalization paths consume `+04` and write finalized `+01`
- `+06/+07` are copied straight through as the tile/attr pair

So the cache is no longer just “prepared metasprite records.”
It is now much closer to a real per-sprite draw-record format.

---

## `0A00` and `0A80 & #$01FF` are being used as the class-builder screen anchors

The class-3 builder front-end makes this much harder to deny:

- `0A00,X` is loaded into `$C3` and used as the **16-bit X anchor**
- `0A80,X & #$01FF` is loaded into `$C5/$C6` and used as the **9-bit Y anchor/state**

That does **not** mean the older bucket/cell interpretation was wrong.
It means these values are being reused as the render-side camera-relative/screen-relative anchor state.

### Honest reading

The safest label now is not just “position” and not just “bucket key.”
It is something like:

- camera-relative / screen-relative slot X state
- camera-relative / screen-relative slot Y state

### New labels
- `0A00,X  SlotScreenX_CameraRelative`
- `0A80,X  SlotScreenY9_CameraRelative`

---

## The class-3 builder has 3 Y-finalization variants

After building the 6 high-table bytes, `C0:C73E` runs one of three Y-adjust/finalization paths across the 24 records.

Those paths are selected from the low/high-byte state of the masked `0A80` anchor that was stored in `$C5/$C6`.

### What is strong

- one path applies the Y adjustment in a tight 24-iteration loop
- one path applies it with an `E0` hide/clamp rule on one side
- one path applies it with a broader negative-range hide/clamp rule

### What I am **not** claiming yet

I am **not** pretending I have fully proven the exact semantic names of those three paths
(e.g. “wrap,” “top clip,” “bottom clip,” etc.).

What is solid is that class 3 has a real **Y-finalization / visibility handling stage**, not just a blind copy.

---

## Why this matters

The render pipeline is much cleaner now:

1. movement / camera-relative state updates `0A00/0A80`
2. class-local builder prepares sprite cache records
3. `C6E7` converts 16-bit X work words into low-OAM X bytes and packed high-table bytes
4. class-local Y finalization writes low-OAM Y bytes
5. `B309` copies the prepared cache into the selected OAM band

That is a real staged render architecture.

---

## What is now substantially stronger

### Strong now
- `C73E` is the missing class-3 cache builder
- `C6E7` packs 4 sprite X words into one OAM high byte plus low-X bytes
- class 3 produces **6** high-table bytes because it is **24 sprites / 4 per high byte**
- the `7F:4BC0` cache records now have a credible per-field draw layout
- `0A00/0A80` are render-side camera/screen anchors, not just abstract bucket data

### Still not fully locked
- exact semantic name of the 3 Y-finalization variants
- exact meaning of record byte `+05`
- whether the cached template source at `7F:4800` is pre-baked metasprite frame data, per-frame actor art state, or a hybrid staging table

---

## New labels from this pass

- `C0:C6E7  Pack4SpriteXWords_AndBuildOamHighByte`
- `C0:C73E  Build_Class3_RenderCache_24Sprites`
- `0A00,X   SlotScreenX_CameraRelative`
- `0A80,X   SlotScreenY9_CameraRelative`

---

## Best next move

The cleanest next target is the **template/source side at `7F:4800`**.

Now that the cache record format is much clearer, the next useful question is:

**who populates the `4800`-series template records, and how do those source records map to animation frames / metasprite layout data?**
