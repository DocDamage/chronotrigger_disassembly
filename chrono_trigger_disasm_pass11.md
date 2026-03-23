# Chrono Trigger (USA) — Disassembly Pass 11

## What this pass focused on

This round moved **upstream from the palette effect executor** and into the **descriptor builders / command formats**.

The goal was to stop treating the palette system as just a runtime black box and instead answer:

- how the preset descriptor table is seeded
- how `7F:2000` command streams build palette descriptors
- what several descriptor bytes actually mean before the updater ever runs

---

## Biggest conclusion

## The palette system has **two distinct descriptor-construction paths**

1. **Preset FD-table path**  
   `FD:E2C0` seeds descriptor records from the table at `FD:FA77`

2. **Script/runtime command path**  
   `C0:4892` and `C0:4A4E` parse palette-related command bytes from stream data and build descriptors on demand

That means the palette engine is not just “hardcoded effect presets.”  
It is a real mixed system:

- some effects come from a built-in preset table
- others are emitted dynamically from script data

---

## `FD:E2C0` is the preset descriptor-table seeder

This pass tightened the meaning of the earlier label:

### `FD:E2C0` → `Seed_PaletteFxDescriptors_FromFDFA77`

What it is doing:

- walks records in the table at `FD:FA77`
- writes them into the descriptor structure rooted at `0520`
- treats high-nibble families differently:
  - `00` -> empty slot
  - `10` -> fixed-bank preset animation descriptor
  - `80` -> long-pointer animation descriptor
  - all other nonzero families -> shorter direct descriptors

The really important detail is the `80` handling:

- after the base descriptor bytes are copied,
- `0529/052A/052B` are filled with a **long pointer back into the `FD:FA77` data stream**
- the **low nibble of `0520`** is used to advance `X`

So for family `8x`, the low nibble is now best understood as a **frame-count / payload-count style field**, not random flags.

---

## Stronger field meanings for `0523`, `0524`, and `0525`

This pass gave a clean answer on the timer side.

## `0524` = effect timer / cadence counter

The updater at `FD:E3AC` does:

- `0524 += 1`
- compare against `0525`
- if not equal, skip effect execution
- if equal, reset `0524` and run the effect body

So `0524` is definitely the **per-descriptor timer accumulator**.

## `0525` = execution period / cadence

Since `0524` counts up to `0525`, this is the **period / delay value** for the descriptor.

This fits the stream builders too, because the parser routines all copy one stream byte into `0525`.

## `0523` is family-dependent state

This is not one universal meaning.

### For `1x / 8x` animation families:
`0523` behaves like a **current frame index**

At `FD:E3C5+`:

- `0523` increments when the period expires
- the low nibble of `0520` acts as the wrap bound
- when the bound is hit, `0523` resets to `00`

So for the animation families, `0523` is now strongly a **frame cursor**.

### For transform / stepped families:
`0523` is the **step delta / signed increment seed**

That matches the previously-mapped stepped transform families (`6x / 7x`) and the direct transform builders that explicitly seed `0523 = 08`.

So `0523` is not a fixed semantic field across all families. It is **family-local state**.

---

## `C0:4892` is the primary script-side palette descriptor parser

The earlier label is now too vague.

### `C0:4892` → `Parse_PrimaryPaletteCommand_From7F2001`

What it does:

- uses `C7` as the stream cursor base
- reads a command byte from `7F:2001 + X`
- dispatches on the **high nibble** of that command byte

Recognized families in this parser are:

- `20`
- `30`
- `40`
- `50`
- `80`

That means the palette command stream is real script data, not just a direct descriptor dump.

---

## `C0:4926` builds actor-relative rotate descriptors

The old label was close, but this pass gives the stream layout.

### `C0:4926` → `Build_RotatePaletteDescriptor_20x30_ActorRelative`

The command byte’s high nibble chooses the family (`20` or `30`).

The bytes following the opcode are interpreted as:

- **packed segment byte**
- **period byte**

What the builder does with that packed segment byte:

- low nibble -> `0522` (segment color count)
- high nibble -> added to an actor-relative base -> `0521` (start color index)

So the `20/30` commands are now strongly:

- **rotate a palette segment**
- with actor-relative segment selection
- at a script-defined cadence

This fits the runtime updater mapping from earlier passes:

- `20` / `30` feed the rotation-family handlers

---

## `C0:497E` builds actor-relative transform descriptors

### `C0:497E` → `Build_TransformPaletteDescriptor_40x50_ActorRelative`

This one is much more informative now.

Bytes following the opcode are interpreted as:

- **packed segment byte**
- **packed current/target byte**
- **period byte**

What gets written:

- `0520` = family high nibble (`40` or `50`)
- `0526` = opcode low nibble (inner mode selector)
- packed segment byte:
  - low nibble -> `0522`
  - high nibble + actor-relative base -> `0521`
- packed current/target byte:
  - high nibble repeated (`H -> HH`) -> `0527`
  - low nibble repeated (`L -> LL`) -> `0528`
- `0523` = `08`
- `0524` = `00`
- `0525` = period byte

That repeated-nibble expansion is real and useful:

- `0xAB` becomes:
  - `0527 = 0xAA`
  - `0528 = 0xBB`

So the stream format is giving **two 4-bit magnitudes**, expanded into full 8-bit effect state.

This is the cleanest builder-side confirmation yet for the transform descriptors.

---

## `C0:49F8` is an actor-relative literal palette upload command

### `C0:49F8` → `Run_PalettePayloadUpload_80_ActorRelative`

This one does not build a long-lived effect descriptor the same way the others do.

Instead it:

- derives a destination palette position from the opcode low nibble plus an actor-relative base
- copies literal palette data from the `7F:2000` stream into:
  - `7E:2200`
  - `7E:2000`

So this is strongly a **literal payload / direct palette upload** command.

The data length is read from the stream and then reduced by `3` before the double `MVN` copies, which says the inline command has a small header before raw palette payload bytes.

I am **not** claiming the exact full command-byte count yet, but this is clearly a literal-upload path, not a rotating or stepped descriptor family.

---

## `C0:4A4E` is the runtime/absolute palette command parser

### `C0:4A4E` → `Parse_RuntimePaletteCommand_From7F2001`

This parser is similar to `C0:4892`, but the commands are **not actor-relative in the same way**.

Recognized families here are:

- `40`
- `50`
- `80`

Notably, `20/30` are absent here.

That suggests two command spaces:

- a more actor-relative / setup-oriented primary palette command path
- a runtime/absolute path for direct transform/upload work

---

## `C0:4A81` builds absolute transform descriptors

### `C0:4A81` → `Build_TransformPaletteDescriptor_40x50_Absolute`

Bytes following the opcode are interpreted as:

- `0521` = explicit start color index
- `0522` = explicit segment color count
- packed current/target byte -> expanded into `0527` / `0528`
- `0525` = period

And just like the actor-relative form:

- `0520` = family high nibble
- `0526` = opcode low nibble
- `0523 = 08`
- `0524 = 00`

So this is the same transform family as `C0:497E`, but with **absolute segment addressing** instead of actor-relative segment addressing.

---

## `C0:4AE5` is the absolute literal palette upload command

### `C0:4AE5` → `Run_PalettePayloadUpload_80_Absolute`

This is the runtime/absolute companion to `C0:49F8`.

It:

- reads an explicit palette destination byte from the stream
- converts it into a `7E:2200` / `7E:2000` destination
- copies inline literal palette payload bytes from bank `7F`

So the `80` upload family has **two forms**:

- actor-relative
- absolute

That is exactly the kind of split you would expect in a script system that supports both “use this actor’s palette region” and “touch this exact palette region.”

---

## Updated working descriptor spec

This pass makes the descriptor spec better on the construction side:

### Common fields

- `0520` = outer family nibble + family-local low-nibble meaning
- `0521` = start color index
- `0522` = segment color count
- `0523` = family-local state  
  - frame index for `1x / 8x`
  - step delta / ramp seed for transform families
- `0524` = timer accumulator
- `0525` = execution period / cadence
- `0526` = inner transform selector for transform families
- `0527` = current amount / current ramp state
- `0528` = target / peak / bound
- `0529..052B` = long pointer (used by `8x` preset animation descriptors)

---

## Stronger interpretation of command families

### Primary palette script parser (`C0:4892`)
- `20/30` -> actor-relative rotate segment descriptors
- `40/50` -> actor-relative transform descriptors
- `80` -> actor-relative literal palette upload

### Runtime/absolute palette parser (`C0:4A4E`)
- `40/50` -> absolute transform descriptors
- `80` -> absolute literal palette upload

That is a much more practical model than the earlier “some palette handlers exist.”

---

## What I am still not claiming yet

Still keeping this honest:

- I have **not** nailed the exact human-facing meaning of every actor-relative base derived from `0F81,X`
- I have **not** finalized the exact byte-for-byte full header length of the `80` upload commands
- I have **not** yet mapped the outer-family semantic split between `20` vs `30` and `40` vs `50` all the way back to script authorship terminology
- I have **not** yet traced who emits these palette commands at a higher gameplay/cutscene layer

But the builder layer is now real enough to start writing an editor spec.

---

## Best next target

The next smart move is to trace **where `C0:4892` / `C0:4A4E` are called from** inside the slot VM / event pipeline.

That should answer the next important question:

> are these palette commands authored by a generic event-script subsystem, a map/cutscene VM, or something even narrower?

That is the cleanest path to turning this from “palette command format” into “here is exactly where game scripts issue palette effects.”
