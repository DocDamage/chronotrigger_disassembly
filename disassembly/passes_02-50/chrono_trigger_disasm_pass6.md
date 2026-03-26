# Chrono Trigger (USA) — Disassembly Pass 6

## What this pass focused on

This round stayed on the `7F:2000` lane and tried to answer the next real question:

**what kind of runtime structure is the `7F:2000` blob actually building?**

The cleanest answer so far is:

- `7F:2000` begins with a **slot count**
- the blob after that is **command / pointer data**
- bank `C0:56A6` is an **orchestrator** that builds per-slot work tables from it
- banks `C0:59D9` and `C0:5A46` are **runtime maintenance / scheduler code** for those slots

I am still **not** claiming the exact game subsystem yet (battle, map objects, etc.), because the code supports a generic “slot + command stream + scheduler” interpretation, but not a subsystem-precise name yet.

---

## Strong correction / clarification for `C0:5CC7`

The previous passes called `5CC7` a “signature/size dispatcher.”
That was close, but this pass makes it sharper:

### `C0:5CC7` is first and foremost a validator

It does exactly two meaningful checks before returning:

1. header bytes at `7F:2000/2001`
2. decompressed size at `$0306`

### Case 1: `7F2000 == 0D` and `7F2001 == 0A`

```asm
LDA.l $7F2000
CMP #$0D
BNE ...
LDA.l $7F2001
CMP #$0A
BNE ...
LDX #$01F0
BRL $2E1C
```

So the blob starting with `0D 0A` is treated as a fatal invalid case and branches to the color-hang path at `2E1C` with error color/value `01F0`.

### Case 2: decompressed size too large

```asm
LDX #$1700
CPX $0306
BPL ok
LDX #$000F
BRL $2E1C
```

So if decompressed size exceeds `0x1700`, this is also fatal and branches to `2E1C` with error color/value `000F`.

### Otherwise

It simply returns with `RTS`.

Best current name:

**`Validate_7F2000_HeaderAndSize`**

That is stronger and more honest than “dispatcher.”

---

## `C0:56A6` — orchestrates the `7F:2000` slot build path

This routine is now important enough to call out directly.

It does:

```asm
LDX #$0048
STX $69
LDX #$0078
STX $6B
STZ $09A0
JSR $6F79
JSR $7155
JSR $E935
JSR $5929
JSR $B204
JSR $A7E9
JSR $5709
JSR $595C
...
JSL $C28004
RTS
```

The key point is that it explicitly runs the newly-understood `5709` and `595C` builders after other setup helpers.

So this is no longer just anonymous startup code.
It is a real **build / initialize runtime slot state from the decompressed `7F:2000` asset** routine.

Best current name:

**`Build_RuntimeSlots_From7F2000`**

---

## `C0:5709` — initializes per-slot WRAM work tables from the slot count

This routine is much more meaningful now.

### What it does first

It uses the byte at `7F:2000` as a count:

```asm
LDA.l $7F2000
REP #$20
AND #$00FF
ASL A
ASL A
ASL A
ASL A
ASL A
STA $D9
```

That computes:

**`D9 = slot_count * 0x20`**

Then it sets direct page to `2100`, so writes to `$80/$81/$83` are actually WRAM-port writes to `$2180/$2181/$2183`.

### First build phase

It copies 2-byte values from the decompressed blob into a contiguous WRAM table:

- source: `7F:2001 + X` and `7F:2002 + X`
- source stride: `0x20`
- destination: WRAM via `$2180`, starting at address `0x1180`

This strongly suggests the decompressed blob is organized as **32-byte records**, one record per slot, and the routine is extracting the first 2 bytes of each record into a dense runtime pointer/index table.

### Then it seeds many other slot arrays with repeated defaults

Using `slot_count` from `7F:2000`, it repeatedly fills slot-aligned WRAM tables at addresses like:

- `1C00`
- `1000`
- `1080`
- `1100`
- `1800`
- `1880`
- `1A00`
- `1A80`
- `1780`
- `1C80`
- `0F80`
- `0B00`
- `0B80`

with constant byte pairs or constant values.

The patterns include values like:

- `07 00`
- `04 00`
- `80 80`
- `00 FF`
- `10 00`
- `00 01`
- `03 00`
- etc.

### What that means

This is not generic memory clearing.
It is a **structured per-slot runtime table initializer**.

Best current name:

**`Init_SlotWorkTables_From7F2000_Count`**

---

## `C0:58DE` — builds / advances per-slot command pointers using the opcode table at `5D6E`

This routine is the first strong evidence that `7F:2000` holds command-stream-like data.

### What it does

- reads slot count from `7F:2000`
- loops slots in 2-byte steps
- clears:

  - `1B01,X`
  - `1B80,X`

- uses `1180,X` as a current pointer/offset into `7F:2001+`
- dispatches bytes through:

```asm
JSR ($5D6E,X)
```

That is a real opcode handler table.

### Important behavior

After handler execution, it writes the updated command pointer back to `1180,X`.

So `1180,X` is strongly acting like a **current script / command-stream position** for each slot.

### Other strong signs

It initializes a series of `7F:0580/0600/0680/.../0900` slot-indexed buffers to zero and sets:

```asm
LDA #$07
STA $1C00,X
```

So `1C00,X` is a slot state byte that starts at `07` after this path.

Best current name:

**`Build_SlotCommandState_FromPrimaryStream`**

---

## `C0:595C` — runs a secondary command stream starting from `7F:2003`

This is now clearer too.

It does:

```asm
REP #$20
STZ $6D
LDA.l $7F2003
TAX
SEP #$20
LDA.l $7F2001,X
...
JSR ($5D6E,X)
```

So instead of starting from slot-local pointers, it starts from a **global / secondary pointer stored at `7F:2003`** and executes the same command table.

That makes it a second command-stream pass over the same blob format.

Best current name:

**`Run_Secondary7F2000_CommandStream`**

---

## `C0:59D9` — maintains a linked-list style slot chain in the `1000/1080` work area

This routine only makes sense if entered with **8-bit X**, and `00BF` does exactly that before calling it.

Once decoded with the correct X width, the logic becomes coherent.

### What it does

It sets direct page to `1000`, then iterates slot entries in 2-byte steps up to:

**`slot_count * 2`**

using the count from `7F:2000`.

It checks slot-local bytes in:

- `1000,X`
- `1001,X`
- `1100,X`
- `1080,X`

and maintains head/tail bytes at:

- `0174`
- `0175`

### Strong inference

This is maintaining a **linked list / queue of runnable slots**.

The `1080,X` array behaves exactly like a “next slot” field.
The `0174/0175` bytes behave like queue head/tail values.

Best current name:

**`Refresh_RunnableSlotLinkedList`**

---

## `C0:5A46` and `C0:5A93` — time-budgeted runtime slot scheduler

This is the clearest runtime behavior in the pass.

### `C0:5A46`

This routine:

1. reads the current PPU counter state from `2137/213D/213F`
2. compares it against threshold `$69`
3. walks the slot linked list through `$74/$75`
4. repeatedly calls `5A93`
5. stops when budget / timing says stop

This is not boot code.
This is a live runtime **scheduler/update burst**.

### `C0:5A93`

This helper:

- copies `$68 -> $67` (a local command budget)
- loads current slot pointer from `1180,X`
- dispatches command bytes through `JSR ($5D6E,X)`
- stops when carry clears or when `$67` runs out
- writes the updated pointer back to `1180,X`

So this is a real **“run a bounded burst of commands for one runnable slot”** function.

Best current names:

- **`Run_TimeBudgetedSlotScheduler`** at `5A46`
- **`Run_BoundedSlotCommandBurst`** at `5A93`

---

## Strong handler-level findings from the `5D6E` dispatch table

I did not try to label all handlers, but several are now strong enough to name.

### `C0:5F6E`

```asm
LDX #$1639
BRL $2E1E
```

This is a hard fatal handler.
Best current name:

**`Fatal_Invalid7F2000Opcode`**

---

### `C0:6240` and `C0:624B`

These are simple and solid:

```asm
6240: STA $1C01,X <- 01
624B: STA $1C01,X <- 00
```

Best names:

- **`Set_SlotBusyFlag`**
- **`Clear_SlotBusyFlag`**

---

### `C0:6254`

This one is also strong:

```asm
LDA #$80
STA $1100,X
LDA #$00
STA $1A81,X
```

This is a slot termination / disable path.

Best current name:

**`Terminate_Slot`**

---

### `C0:5F74`

This one is not fully named yet, but the behavior is real:

- reads `1C00,X`
- uses hardware multiply by `0x80`
- writes/reads slot-indexed words in `7F:0580 + bucket_offset`
- increments `1C00,X`
- returns with carry set on one path and clear on another

This looks like a **bucket / arena allocator or priority-lane placement helper** based on `1C00,X`.

Best provisional name:

**`AdvanceOrAllocate_SlotBucket`**

---

## What the current model looks like now

The strongest grounded interpretation is now:

1. `56D4` decompresses a descriptor-selected blob to `7F:2000`
2. `5CC7` validates the blob
3. `56A6` orchestrates slot-building helpers
4. `5709` seeds slot work tables based on `7F:2000` count
5. `58DE` and `595C` parse command streams through opcode table `5D6E`
6. `59D9` builds/refreshes runnable linked lists
7. `5A46` and `5A93` run a time-budgeted runtime scheduler

That is a much stronger picture than “asset blob to `7F:2000` then unknown code.”

---

## What I am still **not** claiming

I am still avoiding three claims that are not locked down yet:

1. the exact subsystem name for this slot system
2. the exact meaning of every `5D6E` opcode
3. the precise semantics of every work table (`1A80`, `1B80`, `1C80`, etc.)

That would be guessing.

But the code is now strong enough to say this is a **slot-based command interpreter / scheduler system** built from the decompressed `7F:2000` blob.

---

## Suggested label updates from this pass

- `C0:56A6  Build_RuntimeSlots_From7F2000`
- `C0:5709  Init_SlotWorkTables_From7F2000_Count`
- `C0:58DE  Build_SlotCommandState_FromPrimaryStream`
- `C0:595C  Run_Secondary7F2000_CommandStream`
- `C0:59D9  Refresh_RunnableSlotLinkedList`
- `C0:5A46  Run_TimeBudgetedSlotScheduler`
- `C0:5A93  Run_BoundedSlotCommandBurst`
- `C0:5CC7  Validate_7F2000_HeaderAndSize`
- `C0:5F6E  Fatal_Invalid7F2000Opcode`
- `C0:5F74  AdvanceOrAllocate_SlotBucket`
- `C0:6240  Set_SlotBusyFlag`
- `C0:624B  Clear_SlotBusyFlag`
- `C0:6254  Terminate_Slot`

---

## Best next target

The best next pass is not more broad scanning.

It is:

1. map the `5D6E` opcode table systematically
2. identify which handler updates which slot arrays
3. classify the `1Axx / 1Bxx / 1Cxx` tables by role

That is the shortest path from “generic slot scheduler” to the actual subsystem name.
