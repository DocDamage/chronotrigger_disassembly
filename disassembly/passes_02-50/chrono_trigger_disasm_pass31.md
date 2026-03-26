# Chrono Trigger Disassembly — Pass 31

This pass followed the exact open question from pass 30:

- what higher-level command tables actually enter the `9260..977D` and `A4AA..A75F` wrapper regions
- and whether the relation-query service is wired to real bytecode opcodes or just ad-hoc helper calls

The answer is now much cleaner:

**the bank-C1 object layer uses four explicit jump tables for CC-bank command bytes, and the relation-query wrappers live inside those opcode tables.**

## Big structural result

I now have four hard `JSR (abs,X)` dispatch sites in bank `C1`:

- `C1:874E -> JSR ($B80D,X)`
- `C1:8CE7 -> JSR ($B85F,X)`
- `C1:8D88 -> JSR ($B88D,X)`
- `C1:AC2E -> JSR ($B8BB,X)`

Those are not speculative.
They are real 65816 indexed-indirect subroutine dispatches into four separate word tables.

That means the higher-level bank-C1 wrapper layer is not “just a cluster of callers.”
It is an actual **multi-table command interpreter layer**.

## The four command jump tables

### `C1:B80D` — group-0 command jump table (`0x00..0x28`)

This table runs for 41 entries, ending right before `C1:B85F`.

The live entries include:

- `00 -> A78E`
- `01 -> AB8E`
- `02 -> 8F11`
- `03 -> 8F87`
- `04 -> 8FDA`
- `05 -> 9013`
- `06 -> 9045`
- `07 -> 9082`
- `08 -> 90BE`
- `09 -> 9130`
- `0A -> 918E`
- `0B -> 91F9`
- `0C -> 925D`
- `0D -> 92A3`
- `0E -> 9314`
- `0F -> 938D`
- `10 -> 93E6`
- `11 -> 942A`
- `12 -> 9474`
- `13 -> 94D2`
- `14 -> 9514`
- `15 -> 959A`
- `16 -> 95D6`
- `17 -> 95DA`
- `18 -> 95FA`
- `19 -> 9652`
- `1A -> 9656`
- `1B -> 96A5`
- `1C -> 96D4`
- `1D -> 9728`
- `1E -> 975C`
- `1F -> 9765`
- `20 -> 97AB`
- `21 -> 97C0`
- `22 -> 97D5`
- `23..28 -> 95FA`

The repeated fill at `23..28 -> 95FA` is the strongest current sign of a shared stub/failure/default handler in this table.

### `C1:B85F` — group-1 command jump table (`0x00..0x16`)

This table runs for 23 entries, ending right before `C1:B88D`.

The repeated tail fill is also obvious here:

- `11..15 -> 99B4`

### `C1:B88D` — group-2 command jump table (`0x00..0x16`)

This table also runs for 23 entries.

Its entries are a different command family entirely:

- `00 -> 99B8`
- `01 -> 99BE`
- `02 -> 9A39`
- ...
- `16 -> A396`

### `C1:B8BB` — group-3 command jump table (`0x00..0x1B`)

This table runs for 28 entries.

This is the table that most clearly contains the already-decoded **target-selection wrappers**:

- `06 -> A4AF`
- `07 -> A4E0`
- `17 -> A709`
- `18 -> A737`

Those are the same wrappers pass 30 identified at the family level as the mode-`00/01/02/03` target-selection clients of the relation-query service.

## The relation-query wrappers are now tied to concrete command opcodes

This is the biggest practical payoff of the pass.

### Group-0 table entries that land in the relation-query predicate family

These are now hard opcode-table entries, not just loose caller addresses:

- `group0[0x0C] -> 925D`  
  best-fit family: relation-query mode `04`
- `group0[0x0D] -> 92A3`  
  best-fit family: relation-query mode `05`
- `group0[0x0E] -> 9314`  
  best-fit family: relation-query mode `06`
- `group0[0x0F] -> 938D`  
  best-fit family: relation-query mode `08`
- `group0[0x10] -> 93E6`  
  selects between relation-query modes `09` and `0A`
- `group0[0x11] -> 942A`  
  selects between relation-query modes `0B` and `0C`
- `group0[0x1F] -> 9765`  
  best-fit family: relation-query mode `0E`

So the earlier “predicate wrapper cluster” is now grounded as a real **opcode span** inside the group-0 command table.

### Group-3 table entries that land in the target-selection family

These are also now hard opcode-table entries:

- `group3[0x06] -> A4AF`  
  target-select mode `00`
- `group3[0x07] -> A4E0`  
  target-select mode `01`
- `group3[0x17] -> A709`  
  target-select mode `02`
- `group3[0x18] -> A737`  
  target-select mode `03`

That means the already-decoded target-selection wrappers are not one-off helpers.
They are first-class bytecode handlers in the group-3 command family.

## Dispatch-site behavior

### `C1:874E` and `C1:B006`

Both sites fetch a command byte from the current `CC`-bank stream, double it with `ASL A`, and dispatch through `JSR ($B80D,X)`.

These are the clearest live entry points for the group-0 command family.

### `C1:8CE7`

Fetches a command byte into `AEE3`, and for the non-negative path dispatches via `JSR ($B85F,X)`.

### `C1:8D88`

Fetches another command byte path into `AEE3` and dispatches through `JSR ($B88D,X)` on the non-negative route.

### `C1:AC2E`

Dispatches through `JSR ($B8BB,X)` after fetching a positive command byte from the current `CC` stream.

This is the dispatch site that grounds the target-selection family as an actual opcode table rather than a loose block of helper code.

## What this pass proves

### It **does** prove

- bank `C1` contains **four explicit CC-byte command jump tables**
- the relation-query wrappers from pass 30 are real opcode handlers inside those tables
- the target-selection wrappers are also real opcode handlers inside those tables
- the higher-level bank-C1 layer is a genuine **multi-table object-command interpreter**, not just a bag of helper subroutines

### It **does not** prove yet

- the user-facing semantic names of every command in those tables
- the exact top-level names of the four command groups
- whether the group-1 and group-2 tables are best described as motion/state, script control, animation control, or some mixed command families

## Best-fit architectural conclusion

The cleanest current read is:

**Chrono Trigger’s bank-C1 object layer is a multi-table bytecode interpreter fed from CC-bank command streams, and the already-decoded relation-query service is embedded directly into those opcode tables for both predicate testing and target selection.**

That is a much stronger answer than “some wrapper routines call the relation-query block.”

## Best next target

The best next move is to decode the **table-specific command families** themselves:

- classify what group-1 (`B85F`) and group-2 (`B88D`) are for
- map more group-0 and group-3 opcode handlers to concrete object-command semantics
- then connect the command tables back to the exact CC-bank byte stream format
