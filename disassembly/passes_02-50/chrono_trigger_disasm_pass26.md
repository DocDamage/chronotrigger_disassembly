# Chrono Trigger Disassembly — Pass 26

This pass targeted the open question from pass 25:

- pass 25 proved that `C0:46DF` uses the **first 5 bytes** of each `E4:F600` 10-byte record for class-3 setup
- but it did **not** resolve what bytes **5..9** of the `E4:F600` records actually do

## Goal

Trace the code paths that consume `E4:F605..F609` and determine whether those bytes are:

- padding / unused baggage
- reused by another subsystem
- or real runtime control fields

## High-confidence findings

## The full 10-byte `E4:F600` records are installed by a separate 8-slot runtime loader at `CC:EA5B`

The routine beginning at `CC:EA5B` is a real **8-slot installer loop**.

It iterates `slot = 0..7` through a remap table at `CC:F939`, checks an enable/state byte at `29C5`, and then installs a large bundle of per-slot state from the `29BF..29CA` tables.

The critical bridge to `E4:F600` is:

- it reads the 16-bit field at `29C4`
- uses the **low byte** as an index
- multiplies that low byte by **10**
- and uses the result as an index into `E4:F600`

So `CC:EA5B` is a real second consumer of the `E4:F600` record family, independent of the class-3 setup path in `C0:46DF`.

That matters because it means the “extra” 5 bytes are not just class-3 leftovers.
They are part of a separate runtime install path.

## `E4:F601` still resolves a 3-byte pointer through `E4:2300`

Within `CC:EAE0..EB0E`, the loader does:

- `E4:F601 * 3` -> index into `E4:2300`
- installs the resulting 3-byte pointer into:
  - `1C81`
  - `1C83`

So byte 1 of the record is being used here in the same general way as in pass 25: it selects a long-pointer record from the boot-seeded `E4:2300` table.

## `E4:F603` selects a pair of word-table entries from `E4:2600` / `E4:2800`

`CC:EAE0..EB4F` also does:

- `E4:F603 * 2` -> index into `E4:2600`
- `E4:F603 * 2` -> index into `E4:2800`

and installs those into working fields at:

- `1CA2/1CA4`
- `1CC3/1CC5`

It then computes:

- `(E4:2600[idx] - prior_2600_word) >> 2`
- `(E4:2800[idx] - prior_2800_word)`

and stores the results into runtime arrays rooted at:

- `966E`
- `A2C8`

So byte 3 is not just a table index in the abstract.
It is selecting a pair of range/bounds words whose deltas are then converted into runtime per-slot measurements.

## `E4:F604` is a real per-slot flags byte

`CC:EB70..EBAE` loads `E4:F604` and installs it into `9700,Y`.

The loader then immediately tests several bits and applies real side effects:

- bit `0x80`
  - mirrored into `A5C5,Y`
- bit `0x08`
  - increments global `AA63`
  - stores the current slot index into `A002`
- bit `0x20`
  - increments `A006,slot`
- bit `0x04`
  - masked into `A08F,Y`
- and it also clears `A5DB,Y`

So byte 4 is definitely **live flag/state input**, not padding.

## `E4:F605..F608` are copied verbatim into four dedicated per-slot arrays

The loader copies:

- `E4:F605 -> 970B,Y`
- `E4:F606 -> 9716,Y`
- `E4:F607 -> 9721,Y`
- `E4:F608 -> 972C,Y`

This is strong evidence that bytes `5..8` are real per-slot parameters, not dead tail bytes.

What is still unresolved in this pass is the exact semantic name of each of the four arrays.
But the copy pattern is clear and direct.

## `E4:F609` is a packed timing/phase descriptor byte

The last byte of the 10-byte record is consumed in a structured way.

At `CC:EBCB..EBFA`, the loader does:

- low 3 bits (`F609 & 0x07`) -> `98C2,Y`
- high nibble (`F609 >> 4`) -> both:
  - `9742,Y`
  - `9819,Y`

Then it derives a lookup index from the high nibble and low bits and uses table `CC:F544` to produce:

- `989F,Y`
- `9897,Y`

So byte 9 is not a raw opaque value.
It is a real **packed descriptor** whose fields are split and expanded into runtime phase/timer state.

## Two downstream consumers prove that the installed byte-9 state is a live timing system

### `FF:F97A` decrements `9819`, reloads it from `9742`, and advances `9737` by `98C2`

The routine at `FF:F97A` loops through active slots and does:

- if slot active:
  - `DEC 9819,X`
  - if zero:
    - `9819 = 9742`
    - `9737 += 98C2`

That is the exact behavior of a **repeating phase/countdown stepper**.

So:

- `9742` is strongly the **reload/countdown seed**
- `9819` is strongly the **live countdown**
- `98C2` is strongly the **phase increment / step amount**

### `C1:3719` decrements `9897`, reloads it from `989F`, and triggers follow-up work on expiry

The routine at `C1:3719` does:

- `DEC 9897,X`
- if zero:
  - `9897 = 989F`
  - `JSR 373B`

That is a second repeating timer pair:

- `989F` = reload value
- `9897` = live countdown

Since both of those are seeded from `E4:F609` via `CC:F544`, the table at `CC:F544` is best understood as a **packed-nibble -> period/reload lookup table**.

## What this means for `E4:F600` bytes 5..9

The honest state now is:

- bytes `5..8` are real installed per-slot parameters in the `97xx` runtime block
- byte `9` is definitely a **packed timing/phase descriptor**
- and the whole second half of the record is part of a live runtime stepping/timer system

So the “extra half” of the 10-byte records is **not** padding and **not** dead shared baggage.
It is real runtime control data.

## Best-fit names after this pass

These are the strongest names I am comfortable assigning right now:

- `CC:EA5B` = `Install_F600_Record10_ExtendedSlotState_Loop`
- `CC:F544` = `PackedNibble_ToPhaseReloadTable`
- `FF:F97A` = `Tick_SlotPhaseCountdown_9819_AndAdvance9737`
- `C1:3719` = `Tick_SlotReloadCountdown_9897`

And for the record fields:

- `F604` = flags byte
- `F605..F608` = four extended per-slot parameter bytes (exact names still unresolved)
- `F609` = packed timing/phase descriptor

## Honest limits

What is still unresolved after this pass:

- the exact semantic names of `970B/9716/9721/972C`
- the exact meaning of the stepped phase variable at `9737`
- the exact real-world interpretation of the `CC:F544` reload values
  - they clearly behave like timer periods/reload counts
  - but the higher-level subsystem name is still not locked

## Practical takeaway

Pass 25 proved the first 5 bytes of `E4:F600` drive class-3 setup.

Pass 26 proves the last 5 bytes drive a **separate live runtime timer/phase state install path**.

So the full `E4:F600` records are now best understood as **shared 10-byte extended runtime descriptors**, not “class-3 records with an unused tail.”
