# Chrono Trigger (USA) — Disassembly Pass 8

## What this pass focused on

This round pushed on the external VM handlers and then followed their data into the consumer code in bank `FD`.

That finally gives a much stronger subsystem name:

**the external handler cluster around `3711 / 4892 / 4A4E` is a palette/effect descriptor system tied into the slot VM.**

That is no longer a vague guess.

The strongest proof is in the bank `FD` consumer routines:

- they process descriptor records at `0520 + n*0C`
- they operate on **15-bit SNES color values**
- they use the exact SNES color masks:
  - `0x001F`
  - `0x03E0`
  - `0x7C00`-family pieces via `0x7C`
- they use the hardware multiplier at `4202/4203`
- they write transformed color results into `7E:2200`

That is palette math, not generic object scripting.

---

## Biggest conclusion from this pass

### The `0520` table is a 12-byte palette/effect descriptor queue

`C0:4B2C` walks the table in `0x0C`-byte steps:

- start: `Y = 0000`
- test: `LDA $0520,Y`
- next entry: `Y += 000C`
- stop when `Y >= 0060`

So this is a fixed-size descriptor table of **12-byte records**.

The builder routines in `C0` populate fields in that record:

- `0520`
- `0521`
- `0522`
- `0523`
- `0524`
- `0525`
- `0526`
- `0527`
- `0528`
- sometimes `0529/052B`

Then the bank `FD` routines consume those same fields.

### Why this is palette/effect data and not generic script state

The clearest proof is `FD:E64F` and `FD:E8D7`.

Both routines:

- read 15-bit color entries from `7E:2000,X`
- split them into component masks consistent with SNES BGR555 color
- scale or blend those components using the hardware multiply registers
- reassemble the color
- write the result to `7E:2200,X`

That means this descriptor system is driving **palette transforms / palette effects**.

---

## Strong new routine meanings

## `C0:4B2C` — free descriptor scan

This routine is now safe to name as:

**`Find_Free_0520_12ByteDescriptorSlot`**

Behavior:

- scans `0520,Y`
- `0` means free
- step size is `0x0C`
- returns:
  - `CLC` when a free slot is found
  - `SEC` when the table is full

That allocator is used by multiple parser/builder routines.

---

## `C0:4A4E` — descriptor dispatch by high nibble / type class

This routine reads a byte from the slot-VM stream and dispatches by type class:

- high nibble `0x40` → branch into one builder path
- high nibble `0x50` → branch into one builder path
- high nibble `0x80` → branch into a payload-copy path
- otherwise fail/advance out

It is now best treated as:

**`Parse_PaletteRuntimeDescriptorDispatch`**

Its main worker paths are:

- `C0:4A72` — allocate a descriptor slot
- `C0:4A81` — fill a runtime palette-effect descriptor
- `C0:4AE5` — build the `0x80`-class payload-copy descriptor

---

## `C0:4892` — sibling dispatch for another descriptor class family

This routine has the same overall shape as `4A4E`, but with different recognized type values:

- `00`
- `20`
- `30`
- `4x`
- `5x`
- `80`

Best current interpretation:

**`Parse_PaletteDescriptorDispatch`**

Its worker paths are:

- `C0:48C0` — reuse/init path
- `C0:4919 / 4926` — build one descriptor shape
- `C0:4970 / 497E` — build another descriptor shape
- `C0:49F8` — `0x80`-class payload copy

---

## `C0:48C0` — reuse or initialize a palette slot

This routine:

- indexes `7F:0B80,X`
- checks for an existing nonnegative entry
- if found, uses that as a descriptor/table slot
- marks the entry with `FFFF`
- zeroes `0520,Y`
- then copies **two 0x18-byte blocks** from bank `E4`

Those copies go to offsets based on the current slot template index.

The crucial size detail:

- `0x18` bytes = **24 bytes**
- 24 bytes = **12 SNES colors**

So this is not random block copy.
It is exactly the right size for a **12-color palette block**.

Best current name:

**`ReuseOrInit_PaletteSlot_From7F0B80`**

---

## `C0:3711` — install palette template pair for current slot

This routine is a strong sibling of `48C0`.

It:

- sets bit `0x80` in `$54`
- reads a byte from the VM stream
- folds it into the current slot’s `0F81` state
- computes an offset from that template/state byte
- copies **two 0x18-byte blocks** from bank `E4`

The destination bases are derived from:

- `0x2100 + offset`
- then `+ 0x0200`

So this looks like installing a pair of palette template blocks into adjacent palette work banks.

Best current name:

**`Install_CurrentSlot_PaletteTemplatePair_FromE4`**

---

## The palette work buffers are becoming visible

This pass does not fully map all palette banks yet, but the structure is much clearer now.

### Strong evidence

- `C0:3711` and `C0:48C0` copy 24-byte template blocks into work areas derived from `2100` / `2300`
- `C0:49F8` and `C0:4AE5` build payload copies into offsets derived from `2200` and `2000`
- `FD:E64F` / `FD:E8D7` read from `7E:2000`
- those same routines write transformed results to `7E:2200`

That strongly suggests a family of related palette banks in WRAM:

- `7E:2000`
- `7E:2100`
- `7E:2200`
- `7E:2300`

I am **not** claiming the exact semantic role of each bank yet, but they clearly belong to the same palette/effect pipeline.

---

## `FD:E64F` — darken/scale palette transform

This routine is one of the strongest anchors in the whole project now.

Behavior:

- uses `0522` as a count / loop bound
- reads source colors from `7E:2000,X`
- scales color components
- writes transformed colors to `7E:2200,X`

The component handling is consistent with SNES BGR555 layout:

- low five bits
- middle green field
- upper red/blue field pieces

Best current name:

**`Apply_PaletteScale_To7E2200`**

It looks like a scale/darken path rather than a brighten path.

---

## `FD:E8D7` — brighten / inverse-blend palette transform

This routine is the complementary path.

It:

- reads the same palette data format
- inverts component ranges before multiply
- adds them back in
- writes the result to `7E:2200,X`

Best current name:

**`Apply_PaletteBrightenBlend_To7E2200`**

This looks like a brighten / fade-toward-white style transform.

---

## The queue is processed as effect records, not generic objects

The `FD:E5xx` / `FD:E8xx` code updates per-record fields like:

- `0523`
- `0525`
- `0527`
- `0528`

and clears `0520` when a descriptor finishes.

That is the behavior you expect from a running effect queue:

- descriptor active while `0520 != 0`
- fields mutate over time
- descriptor self-terminates by zeroing `0520`

So `0520` is very likely the **active type/state byte** for each palette-effect record.

---

## What this changes about the slot VM

This is the first pass where I’m comfortable saying the slot VM is not just “entity movement plus flags.”

At least part of it clearly has **visual/palette control opcodes**.

The external handlers now look like:

- **descriptor installers**
- **palette template loaders**
- **palette payload transfer builders**
- **palette effect queue emitters**

That means the VM is crossing into the rendering/presentation layer, not just gameplay state.

---

## Updated best-effort labels from this pass

- `C0:3711  Install_CurrentSlot_PaletteTemplatePair_FromE4`
- `C0:4892  Parse_PaletteDescriptorDispatch`
- `C0:48C0  ReuseOrInit_PaletteSlot_From7F0B80`
- `C0:4919  Alloc_PaletteFxSlot_Type20or30`
- `C0:4926  Build_PaletteFxDescriptor_Type20or30`
- `C0:4970  Alloc_PaletteFxSlot_Type4x5x`
- `C0:497E  Build_PaletteFxDescriptor_Type4x5x`
- `C0:49F8  Build_PalettePayloadTransfer_Type80`
- `C0:4A4E  Parse_PaletteRuntimeDescriptorDispatch`
- `C0:4A72  Alloc_PaletteFxSlot_Runtime4x5x`
- `C0:4A81  Build_PaletteFxDescriptor_Runtime4x5x`
- `C0:4AE5  Build_PalettePayloadTransfer_Runtime80`
- `C0:4B2C  Find_Free_0520_12ByteDescriptorSlot`
- `FD:E2C0  Build_0520DescriptorTable_FromFDFA77`
- `FD:E64F  Apply_PaletteScale_To7E2200`
- `FD:E8D7  Apply_PaletteBrightenBlend_To7E2200`

---

## What is still uncertain

These points are still unresolved:

1. the exact semantic meaning of every descriptor field in `0520..052B`
2. whether the `20/30/40/50/80` classes correspond to:
   - fade types
   - palette banks
   - script opcode families
   - or a mix of type + mode
3. the exact role split between the WRAM banks:
   - `2000`
   - `2100`
   - `2200`
   - `2300`
4. the exact meaning of:
   - `0F81`
   - `1400`
   - `7F:0B80`
   - `0B00/0B80`
   in the palette pipeline

But the broad subsystem name is now much stronger than before.

---

## Best next move

The cleanest next target is to stay on this palette path and map:

- the full descriptor format for `0520 + n*0C`
- the WRAM palette bank roles (`2000/2100/2200/2300`)
- the ownership / reservation tables (`0F81`, `1400`, `7F:0B80`, `0B00/0B80`)

That should turn this from:

**“palette/effect descriptor subsystem”**

into:

**“exact per-record format + exact palette bank pipeline.”**
