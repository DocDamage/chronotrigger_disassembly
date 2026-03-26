# Chrono Trigger (USA) — Disassembly Pass 7

## What this pass focused on

This round stayed on the `5D6E` opcode table and tried to answer the next real question:

**what kind of VM is this actually?**

The strongest grounded answer now is:

- this is a **slot-based script VM**
- it has a **real opcode table** at `C0:5D6E`
- it has a **script-variable table** at `7F:0200`
- it has **predicate subtables** for comparisons
- it has commands for:
  - slot activation / promotion
  - slot flags / termination
  - variable loads and tests
  - facing / direction writes
  - spatial checks
  - input / global flag gates

That is a lot more specific than “runtime scheduler.”
It is still not a fully named game subsystem, but it is definitely a real command VM now, not just generic init glue.

---

## `C0:5D6E` is the main opcode table

The handler table at `C0:5D6E` now resolves cleanly as a dispatch table for the slot VM.

The first 0x40 entries are:

- `00 -> 5F74`
- `01 -> 5F6E`
- `02 -> 5FB6`
- `03 -> 607E`
- `04 -> 6109`
- `05 -> 61E9`
- `06 -> 61FE`
- `07 -> 6214`
- `08 -> 6240`
- `09 -> 624B`
- `0A -> 6254`
- `0B -> 6269`
- `0C -> 6282`
- `0D -> 6295`
- `0E -> 62A4`
- `0F -> 5535`
- `10 -> 62B5`
- `11 -> 62CB`
- `12 -> 62DE`
- `13 -> 6313`
- `14 -> 6361`
- `15 -> 63A4`
- `16 -> 63E6`
- `17 -> 5539`
- `18 -> 6442`
- `19 -> 653B`
- `1A -> 6568`
- `1B -> 553D`
- `1C -> 654E`
- `1D -> 5541`
- `1E -> 556C`
- `1F -> 5579`
- `20 -> 658F`
- `21 -> 65AA`
- `22 -> 65EB`
- `23 -> 65F8`
- `24 -> 661F`
- `25 -> 5586`
- `26 -> 5593`
- `27 -> 662C`
- `28 -> 6655`
- `29 -> 3E84`
- `2A -> 3ED6`
- `2B -> 3EDE`
- `2C -> 3EE6`
- `2D -> 66A5`
- `2E -> 4A4E`
- `2F -> 3F12`
- `30 -> 66B2`
- `31 -> 66BC`
- `32 -> 3EE2`
- `33 -> 3711`
- `34 -> 66C6`
- `35 -> 66E5`
- `36 -> 66EF`
- `37 -> 66F9`
- `38 -> 6705`
- `39 -> 670F`
- `3A -> 5F6E`
- `3B -> 6719`
- `3C -> 6724`
- `3D -> 5F6E`
- `3E -> 5F6E`
- `3F -> 6732`

That table structure is solid now.

---

## `7F:0200` is a script-variable table

This is one of the best new conclusions in the pass.

Multiple handlers treat `7F:0200 + index*2` as a variable destination or source table.

### Strong examples

#### `C0:658F`
This takes a variable index from the stream and stores a value into `7F:0200 + index*2`:

- source: `7E:2980`
- destination: `7F:0200 + index*2`

#### `C0:65AA`
This stores **two values** from a target slot into two variable entries:

- target slot `1801`
- target slot `1881`

Those look like slot X/Y coarse coordinates.

#### `C0:65EB`
This maps a target slot through `$97,X`, then stores its coarse position pair into script vars.

#### `C0:65F8`
This stores `1600,target_slot` into a script variable.

That `1600` byte now looks strongly like a **facing / direction byte**.

#### `C0:661F`
This uses the mapped slot from `$97,X`, then stores that slot’s `1600` byte into a script variable.

### Best current interpretation

`7F:0200` is not just scratch RAM.
It is behaving like a **VM variable table / script work variable table**.

---

## `1600/1601` now looks like facing / direction state

This pass made that much stronger.

### Why

The `5535/5539/553D/5541/5545` group writes values `0,1,2,3` or a stream byte into `1600,current_slot` and clears `1601,current_slot`.

The target-slot versions `556C/5579/5586/5593` do the same to another slot.

Then `55A0` does something more interesting:

1. reads current slot position and target slot position
2. if coarse coordinates match, falls back to the lower position bytes
3. calls `JSR $ABA2`
4. uses the result to index a table at `F700`
5. writes that result to `1600,current_slot`

That is not a generic state write anymore.
That is exactly what a **“face toward target” / direction-resolution helper** looks like.

### Best current interpretation

- `1801 / 1881` look like **coarse slot position bytes**
- `1800 / 1880` look like **fine / sub-position bytes**
- `1600` looks like **slot facing / direction**
- `1601` looks like a paired secondary state byte cleared with it

---

## `C0:6467` and `C0:6477` are predicate subtables

These two little tables are now clearly predicate dispatch tables used by the script-test handlers.

### `C0:6467` — byte predicate table

This table has 8 entries:

- `6487` → `==`
- `648F` → `!=`
- `6497` → `>`
- `64A1` → `<`
- `64A9` → `>=`
- `64B5` → `<=`
- `64BF` → `(A & B) != 0`
- `64C7` → `(A | B) != 0`

These return:

- `CLC` when predicate succeeds
- `SEC` when predicate fails

That matches the surrounding “skip on false” handler structure.

### `C0:6477` — word / extended predicate table

This table has 8 entries:

- `64CF`
- `64DB`
- `64E7`
- `64F5`
- `6503`
- `6511`
- `6523`
- `652F`

The first six are the same comparison-family shape in 16-bit mode.
The last two are the word versions of the nonzero bit/OR tests.

Best current name:

**`CompareWordPredicateTable`**

---

## The test handlers are now meaningful

### `C0:62DE`
This is now best described as:

**`ScriptTest_VarByte_ImmByte_SkipIfFalse`**

It does:

1. read a variable index from the stream
2. load the variable from `7F:0200[index*2]`
3. read an immediate compare byte
4. read a byte-predicate selector
5. dispatch through `6467`
6. if false, skip by a count byte
7. if true, continue

That is classic bytecode-VM behavior.

### `C0:6313`
This is another test form that mixes a variable-table fetch with an immediate and uses the word predicate table.

### `C0:6361`
This is the variable-vs-variable form using the byte predicate table.

### `C0:63A4`
This is the variable-vs-variable form using the word predicate table.

### `C0:63E6`
This is a more special table-driven test form that can source through `7F:0000` and then run a word predicate.

The exact semantic source behind every input form is not fully nailed down yet, but the overall structure is no longer vague:
these are **script conditionals with skip counts**.

---

## `C0:6240` through `C0:62CB` are slot-control primitives

These handlers are now grounded enough to group.

### Already solid

- `6240` → set slot busy flag (`1C01 = 1`)
- `624B` → clear slot busy flag (`1C01 = 0`)
- `6254` → terminate slot (`1100 |= 80`, `1A81 = 0`)

### Strongly improved

- `6269` sets bit 7 in `1000,target_slot`
- `6282` clears bit 7 in `1000,target_slot`
- `6295` writes an immediate byte into `1C80,current_slot`
- `62A4` writes an immediate byte into `1C81,current_slot`
- `62B5` advances the script pointer by an immediate byte count
- `62CB` rewinds the script pointer by an immediate byte count

That is a real script machine vocabulary.

---

## `C0:5FB6 / 607E / 6109 / 61E9 / 61FE / 6214` are activation / promotion style commands

These are still the least comfortable names in the pass, but they are no longer blank.

### What is now solid

These routines all do some version of:

- read a target slot from the script stream
- reject busy / terminated / flag-blocked targets
- compare a nibble-derived priority / bucket value against the target slot’s current `1C00`
- copy / seed a pointer into `7F:0580 + computed_bucket`
- install a new `1180,target_slot` script pointer
- set `1C00,target_slot`
- clear `1A80,target_slot`
- clear `1A01,target_slot`

The `6109 / 6214` group also uses a per-slot latch at `7F:0980`.

### Best current interpretation

These are **slot activation / promotion / retargeting opcodes**.
The latch-driven forms look like “one-shot / latched” variants of the same idea.

I am still not claiming the exact gameplay-facing name for them yet.

---

## `C0:66A5` onward are global/input/flag gates

This block makes the VM look even more script-like.

### Strong examples

- `66B2` tests bit `0x02` in `$00F8`
- `66BC` tests bit `0x80` in `$00F8`
- `66C6` tests bit `0x80` in `$00F2`
- `66E5` tests bit `0x08` in `$00F2`
- `66EF` tests bit `0x40` in `$00F2`
- `66F9` tests bit `0x04` in `$00F2`
- `6705` tests bit `0x20` in `$00F2`
- `670F` tests bit `0x10` in `$00F2`

These all use the same pattern:

- if test passes, consume one byte and continue
- if test fails, skip by a byte count

Then there are latch-consuming forms:

- `6719` checks bit `0x02` in `$50` and clears it with `TRB`
- `6724` checks bit `0x80` in `$50` and clears it
- `6732` checks bit `0x80` in `$51` and clears it

That is absolutely bytecode-VM control flow.

---

## `C0:6655` is a real spatial gate

This one is too specific to ignore.

It:

- reads a target slot
- reads the target slot’s coarse X/Y bytes from `1801/1881`
- compares them against halved globals from `1D0A / 1D0E`
- accepts only when both deltas are within a limited range window

Best current interpretation:

**a spatial proximity / region gate against a global reference position**

I am not hard-naming `1D0A/1D0E` yet, but this is clearly positional logic, not arbitrary math.

---

## Where the overall interpretation stands now

The strongest grounded model is now:

1. `56D4` decompresses a script blob to `7F:2000`
2. `5709` initializes slot work tables from the slot count
3. `58DE` / `595C` parse command streams
4. `59D9` / `5A46` / `5A93` maintain and run runnable slots
5. `5D6E` provides the opcode vocabulary
6. `7F:0200` acts as the VM’s variable table
7. many opcodes are clearly about slot direction, slot position, slot flags, spatial tests, and input/global gates

So this is now much closer to:

**“slot script VM for actor/object-style runtime logic”**

than to a generic anonymous scheduler.

That is still an inference, but it is a much stronger one now.

---

## What I am still not claiming

- the exact user-facing subsystem name in game terms
- the exact meaning of every global in `$00F2/$00F8/$50/$51`
- the exact role of `$97,X`
- the exact role of every external handler in the table (`3E84`, `4A4E`, `3711`, etc.)

Those need another pass.

---

## Best next move

The next high-value pass is:

- trace the external opcode handlers at:
  - `3E84`
  - `3ED6`
  - `3EDE`
  - `3EE2`
  - `3EE6`
  - `3F12`
  - `4A4E`
  - `3711`

Those are probably where the VM stops looking generic and starts telling us exactly what subsystem it belongs to.
