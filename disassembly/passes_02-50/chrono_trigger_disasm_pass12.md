# Chrono Trigger (USA) — Disassembly Pass 12

## What this pass focused on

This round chased the exact linkage between the previously identified **palette command parsers** and the larger `7F:2000` script/runtime system.

The goal was to answer:

- are `C0:4892` and `C0:4A4E` isolated helpers
- or are they directly reachable from the same opcode VM as the slot logic, predicates, and scheduler

---

## Biggest conclusion

## The palette command parsers are **direct opcode handlers inside the main `7F:2000` slot VM**

That is the cleanest answer yet for subsystem identity.

The dispatch logic at `C0:595C` does:

- read a bytecode from `7F:2001 + X`
- widen it with `ASL`
- dispatch through `JSR ($5D6E,X)`

So opcode value maps directly to a **16-bit pointer in the giant table rooted at `C0:5D6E`**.

This means the palette system is **not** merely called by the VM from some external special-case path.

It is part of the VM.

---

## `C0:5D6E` is a **large contiguous opcode table**, not a tiny local one

Earlier passes treated `C0:5D6E` as “the opcode table,” which was true but underspecified.

This pass confirms the table continues well past the first 64 entries previously examined.

Using the direct dispatch math from `C0:595C`, the following opcode -> handler relationships are now hard-confirmed:

- opcode `0x2E` -> `C0:4A4E`
- opcode `0x33` -> `C0:3711`
- opcode `0x88` -> `C0:4892`

So both palette parsers and one of the earlier palette/template install paths live inside the same VM table.

That is an important architectural correction.

---

## Hard opcode mappings

## opcode `0x2E` -> `C0:4A4E`
### `Parse_RuntimePaletteCommand_From7F2001`

This is the **runtime/absolute palette command parser** identified in earlier passes.

Since it is a direct VM opcode target, the `40/50/80` runtime palette command families are now best understood as **first-class script VM operations**, not helper-side subformats only reachable through some other command.

---

## opcode `0x33` -> `C0:3711`
### `Install_CurrentSlot_PaletteTemplatePair_FromE4`

This already looked palette/template related in earlier work.

Now we know it is also a **direct VM opcode target**.

So the same VM can:

- install a palette template pair from bank `E4`
- issue runtime palette descriptor commands
- issue the higher-level primary palette command parser path

That is a much tighter subsystem picture than before.

---

## opcode `0x88` -> `C0:4892`
### `Parse_PrimaryPaletteCommand_From7F2001`

This is the big linkage win of the pass.

`C0:4892` is not just some side parser referenced from unrelated code/data.

It is a direct entry in the same giant opcode table dispatched by the `7F:2000` slot VM.

So the earlier “primary palette command parser” label was mechanically correct, but this pass tells us where it lives architecturally:

- it is a **real VM opcode handler**
- it consumes stream data out of `7F:2001`
- it allocates/builds palette effect descriptors relative to the current slot / actor context

---

## Why this matters

The same VM table now contains:

- slot control
- target-slot / mapped-slot logic
- variable predicates
- position/facing tests
- palette template install
- runtime palette commands
- primary palette commands

That means the `7F:2000` blob is no longer best described as merely a generic “slot scheduler with some effect commands attached.”

A much stronger description is:

## `7F:2000` is a slot/object script VM that directly owns visual effect and palette behavior alongside gameplay/state logic.

I am intentionally still using “slot/object script VM” instead of claiming “this is definitively the map event script engine,” because I have not yet traced it all the way back to high-level scene/event loaders.

But the evidence now strongly pushes it out of the “render-only helper” bucket.

---

## Strong architectural inference

The palette commands are not isolated render opcodes.

They are actor/current-slot-aware.

We already knew from previous passes that the palette builders use:

- current slot context
- actor-relative palette bases
- current-slot descriptor allocation/state

Now, with `0x88`, `0x2E`, and `0x33` all proven to be direct VM opcodes, the clean inference is:

- this VM controls per-object/per-slot behavior
- palette changes are scriptable behavior attached to those objects/slots
- the palette engine is one execution service used by the VM, not a separate script language

That is a much more useful reverse-engineering target if the long-term goal is tooling or a rebuildable disassembly.

---

## Secondary useful finding: the opcode table extends into a higher-opcode cluster

Around the `0x84`-range of the same table, the following cluster appears:

- `0x84` -> `C0:4867`
- `0x85` -> invalid (`C0:5F6E`)
- `0x86` -> invalid (`C0:5F6E`)
- `0x87` -> `C0:4876`
- `0x88` -> `C0:4892`
- `0x89` -> `C0:4B49`
- `0x8A` -> `C0:4B58`
- `0x8B` -> `C0:4B74`
- `0x8C` -> `C0:4BC3`
- `0x8D` -> `C0:4C27`
- `0x8E` -> `C0:4C74`
- `0x8F` -> `C0:5429`
- `0x90` -> `C0:4CD5`
- `0x91` -> `C0:4CE0`
- `0x92` -> `C0:4E73`

I am **not** over-naming all of these yet.

But the clustering strongly suggests that `0x87` through at least `0x92` is a **related high-opcode behavior group**, and several of these handlers clearly touch the same current-slot state ranges (`18xx`, `1Axx`, `0Cxx`) seen around the palette/appearance work.

So this is a good next frontier for turning the VM into an editable opcode spec.

---

## What got corrected / tightened this pass

### Earlier ambiguity:
“`C0:4892` and `C0:4A4E` are palette parsers related somehow to the runtime system.”

### New grounded answer:
They are both directly tied into the main `7F:2000` VM architecture:

- `C0:4A4E` via opcode `0x2E`
- `C0:4892` via opcode `0x88`

That is a much stronger and cleaner statement.

---

## Best current description of the system

The cleanest no-BS wording now is:

## `7F:2000` decompresses into a slot-based object/script VM whose opcode table directly drives state logic, movement/position tests, and visual/palette effect commands.

That is the strongest subsystem identification achieved so far.

---

## Best next target

The best next move is to map the **high-opcode cluster `0x87..0x92`** handler-by-handler.

That cluster now looks like the most concentrated block of:

- appearance / palette / slot visual state
- current-slot state transitions
- maybe actor-facing/appearance coupling

If that cluster gets decoded cleanly, the VM stops being “script VM with palette support” and starts becoming a real opcode reference for the engine.
