# Chrono Trigger (USA) — Disassembly Pass 19

## What this pass focused on

This round stayed on the `7F:4800` side instead of the final OAM emitters.

The goal was to answer a simpler question cleanly:

- what *kind* of thing is the `7F:4800` family
- how the class-sized builders feed it
- what the per-frame source block structure looks like before the later render-cache/OAM stages

---

## Biggest conclusion

## `7F:4800` is a write-dominated **metasprite template staging table**

The ROM evidence is strong here:

- there are a large number of **indexed long stores** into `7F:4800`-series addresses from bank `C0`
- there are only a tiny number of local reads back from that same region in the same code cluster
- by contrast, the `7F:4BC0` family has both many writers **and** the confirmed renderer/OAM-emitter reads from earlier passes

That makes the safest current read:

- `7F:4800` = **template staging / intermediate sprite-record build area**
- `7F:4BC0` = **later render-cache family actually consumed by the OAM shadow builder**

This pass does **not** claim I have fully proven the exact handoff path between every `4800` builder and every `4BC0` builder.
It **does** strongly support that `4800` is an upstream staging family, not the main emitted cache.

### New label
- `7F:4800  MetaspriteTemplateStagingTable`

---

## The class-sized `7F:4800` builders all have the same shape

There is a repeated pattern in bank `C0`:

1. compare / sync a per-slot frame selector
2. build a source pointer in `$D3/$D5`
3. pre-process a class-sized header region
4. copy a trailing XY-tail into `7F:4800` template records
5. seed tile/attribute-ish bytes for each 8-byte record

The strong class-sized setup points are:

- `C0:CC20` uses multiplier `#$28`
- `C0:CF40` uses multiplier `#$50`
- `C0:D7F0` uses multiplier `#$78`

Those values are not random:

- `0x28 = 0x20 + 0x08`
- `0x50 = 0x40 + 0x10`
- `0x78 = 0x60 + 0x18`

That matches the later copy cores perfectly:

- class-0 tail copy starts from source offset `Y = #$0020`
- class-1 tail copy starts from source offset `Y = #$0040`
- 12-sprite tail copy starts from source offset `Y = #$0060`

So the source frame blocks are now much easier to describe.

---

## The source frame-block structure is substantially clearer now

### Strong current read

Each class-sized source frame block has two major sections:

1. a **header/descriptor region**
2. a trailing **signed XY tail**

### The sizes line up like this

#### 4-sprite class
- total block size: `0x28`
- header region: `0x20`
- XY tail: `0x08` = `4 * 2`

#### 8-sprite class
- total block size: `0x50`
- header region: `0x40`
- XY tail: `0x10` = `8 * 2`

#### 12-sprite class
- total block size: `0x78`
- header region: `0x60`
- XY tail: `0x18` = `12 * 2`

That is much stronger than the older vague idea that these were just “some source records.”

The template-copy cores are literally stepping through the trailing 2-byte pairs after the header region.

---

## The XY-tail copy pattern is now very clear

### Class-0 core
At `C0:CCC0` the builder starts with `LDY #$0020` and then repeatedly:

- reads one byte from `[$D3],Y`
- sign-extends it into:
  - `7F:4802,X`
  - `7F:4803,X`
- reads the next byte from `[$D3],Y+1`
- stores it into:
  - `7F:4804,X`

Then it repeats for the next template record at:

- `+0A/+0B/+0C`
- `+12/+13/+14`
- `+1A/+1B/+1C`

That is a real per-record pattern.

### Class-1 core
At `C0:CFE0` the exact same logic starts from `Y = #$0040` and fills 8 records.

### 12-sprite core
At `C0:D890` the same logic starts from `Y = #$0060` and fills 12 records.

---

## The template records at `7F:4800` are 8 bytes each, but they are *not* the final OAM records

This pass makes that much more comfortable to say.

### Strong current per-record read

For each staged record in `7F:4800`:

- `+02/+03` = sign-extended relative X work value from the frame block tail
- `+04` = companion 8-bit work value from the frame block tail
- `+06` = seeded tile-ish byte
- `+07` = seeded attr/state-ish byte

What I am **not** claiming yet:

- that `+04` is definitively final relative Y
- that `+07` is already the final low-OAM attr byte with no later reinterpretation
- that the `7F:4800` record format is identical to the later `7F:4BC0` prepared-render-cache format

The honest read is:

`7F:4800` holds **upstream template sprite records** that look close to OAM-ish draw records, but are not yet the final emitted cache.

---

## The header-region pre-pass is real and class-sized

Before the XY-tail copy, the routines run a pre-pass over the frame-block header region.

The strong repeated pattern is:

- set WRAM port address from `$D0`
- iterate a class-sized count in `$C9`
- walk the frame block two bytes at a time
- test bit `0x40` of the current byte
- dispatch to either:
  - `C0:E687`
  - or `C0:E534`

That happens with class-sized boundaries:

- `0x20` header bytes for the 4-sprite class
- `0x40` header bytes for the 8-sprite class
- `0x60` header bytes for the 12-sprite class

So the header region is not dead padding.
It is being actively interpreted before the tail copy stage.

### What is still unresolved

I have **not** pinned the exact semantic meaning of that header region yet.
It is clearly a real descriptor/control area, but I am not fake-naming it as “tile commands,” “animation script,” or “metasprite chunks” until that dispatch is cracked properly.

---

## The frame-block source pointer construction is now concrete

The builders construct `$D3/$D5` as:

- class-local base pointer from the `1300/1380` family
- plus `frame_index * class_block_size`

The multiplier register usage makes the class-local block sizes explicit:

- `#$28`
- `#$50`
- `#$78`

That means the source pointer is not just “a random frame blob.”
It is a true indexed frame-block selection path.

---

## The class system is now cleaner from a source-data standpoint

The render side from earlier passes already told us the final OAM classes are:

- 4 sprites
- 8 sprites
- 12 sprites
- 24 sprites

This pass shows the source side uses matching class-local frame blocks:

- 4-sprite source blocks with `0x20 + 0x08`
- 8-sprite source blocks with `0x40 + 0x10`
- 12-sprite source blocks with `0x60 + 0x18`

The 24-sprite class still looks like it is built from larger / repeated 12-sprite-style source handling, but I am not claiming the exact merge path is fully solved yet.

That part is now a focused question rather than a blind one.

---

## Strongest new takeaways

### Strong now
- `7F:4800` is an upstream template staging family, not the main emitted OAM cache
- the class-sized builders use explicit frame-block sizes: `0x28 / 0x50 / 0x78`
- those frame blocks split cleanly into:
  - header region
  - trailing signed XY tail
- the template-copy cores at `CCC0 / CFE0 / D890` are doing real staged sprite-record construction
- the header region is actively interpreted by dispatch through `E687 / E534`

### Still not fully locked
- exact semantics of the header-region dispatch
- exact meaning of `+04` and `+07` in the `7F:4800` records
- exact 24-sprite merge/build path on the source/template side
- the complete handoff path from every `4800` builder into every later `4BC0`/render-cache stage

---

## New labels from this pass

- `7F:4800  MetaspriteTemplateStagingTable`
- `C0:CC20  Setup_Class0_FrameBlockPtr_Size0x28`
- `C0:CCC0  CopyClass0_XYTail_To7F4800_TemplateRecords`
- `C0:CF40  Setup_Class1_FrameBlockPtr_Size0x50`
- `C0:CFE0  CopyClass1_XYTail_To7F4800_TemplateRecords`
- `C0:D7F0  Setup_Class12Sprite_FrameBlockPtr_Size0x78`
- `C0:D890  CopyClass12Sprite_XYTail_To7F4800_TemplateRecords`

---

## Best next move

The cleanest next target is the **header-region dispatch** through:

- `C0:E534`
- `C0:E687`

That is the missing piece for turning these source frame blocks from:

“class-sized template records with a header and XY tail”

into:

“here is the actual metasprite frame format and command vocabulary.”
