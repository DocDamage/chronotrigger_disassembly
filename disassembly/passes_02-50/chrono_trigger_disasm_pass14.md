# Chrono Trigger (USA) — Disassembly Pass 14

## What this pass focused on

This round followed the **movement-state side** of the slot VM instead of staying on the opcode handlers that *start* movement.

The target bytes were the ones already implicated by the `0x89..0x92` handler block:

- `1A01`
- `1A80`
- `1B80`
- `1600`
- `1900/1901`
- `1980/1981`

The goal was to answer:

- what the runtime update loops do with these fields
- how a script-supplied movement command turns into a real signed motion vector
- whether the engine is using a crude direction enum or a richer angle index internally

---

## Biggest conclusion

## The movement system is using an **8-bit angle index + trig-like lookup tables**, not just four-way direction bytes

That is the major architectural upgrade from this pass.

There are now two clearly separated layers:

1. **Script / command layer**
   - handlers set targets, durations, speeds, and angle-like values

2. **Runtime motion layer**
   - converts an angle index into signed X/Y deltas
   - decrements a per-slot movement timer
   - integrates those deltas into `1800/1880`

So the engine is not just “move north/south/east/west.”  
It has a proper **angle-indexed vector step system**.

---

## Hard runtime findings

## `1A01` is the active movement duration / remaining step counter

This is now solid.

Multiple runtime update paths do:

- `LDA 1A01,X`
- return immediately if zero
- otherwise `DEC A`
- store it back to `1A01,X`

Examples:

- `C0:AA11`
- `C0:AAC7`
- `C0:AB06`

That is not “unknown movement state” anymore.  
It is the clearest read yet for **remaining movement time / remaining movement steps**.

This also lines up with startup handlers in the high-opcode cluster that explicitly seed `1A01` from immediate bytes.

---

## `1A80` is the motion-active state byte / in-progress flag

This is now strong.

The movement-start handlers at `4E73+` gate on `1A80` first:

- if `1A80 != 0` and `1A01 != 0`, the command reports “still busy”
- if `1A80 != 0` but `1A01 == 0`, the handler clears `1A80`
- otherwise it starts a new movement command

And the movement-start code explicitly increments or stores nonzero values into `1A80`.

So the honest read is:

- `1A80 == 0` → no active movement for that command family
- `1A80 != 0` → movement currently in progress

I am still calling it a **state/flag byte** rather than a pure boolean, because some paths `INC` it and others directly `STA #$01`.

---

## `1B80` selects the motion integrator / update mode

This is one of the most useful new findings.

At `C0:AA07`:

- if `1B80 == 0`, the runtime uses one movement update path

At `C0:AAFD`:

- another path is also taken when `1B80 == 0`, but under a different `1100,X` mode class

At `C0:AAC7`:

- if `1B80 != 0`, the runtime uses a different integrator

So `1B80` is not just random side state.  
It is selecting which **motion integration behavior** is used for that slot.

I am not pretending the exact user-facing meaning is fully solved yet, but structurally it is absolutely a **movement update mode selector**.

---

## `1900/1980` are signed per-step motion delta components

This is now very strong.

The runtime update loops add/subtract them into the 16-bit position words:

- `1800/1801`
- `1880/1881`

Examples:

### `C0:AA07`
Uses `1900` and `1980` as signed 8-bit deltas, with explicit overflow/underflow handling into the high bytes `1801` and `1881`.

### `C0:AAFD`
Sign-extends the 8-bit deltas into 16-bit values before adding them directly into `1800` and `1880`.

### `C0:AAC7`
Uses a different path that treats the fields more like a wider/fractional movement state.

So the no-BS naming upgrade is:

- `1900/1901` = signed X-ish movement delta state
- `1980/1981` = signed Y-ish movement delta state

The exact axis naming can still be swapped depending on map conventions, but these are definitely the **two motion vector components**.

---

## `1600` is set from an angle-to-facing table, not directly from script

This got much cleaner.

The directional movement start code around `C0:4E8E+` does:

- load an 8-bit angle-like value into `EE`
- use that as an index into `C0:F700`
- store the result into `1600,X`

And the table at `C0:F700` is not arbitrary. It is a 256-byte mapping split into four coarse sectors:

- `0x00..0x1F`   -> `3`
- `0x20..0x5F`   -> `1`
- `0x60..0x9F`   -> `2`
- `0xA0..0xDF`   -> `0`
- `0xE0..0xFF`   -> `3`

So `1600` is best read as a **coarse 4-way facing value derived from a fuller 8-bit angle index**.

That is much more specific than the earlier “probably facing/direction byte.”

---

## Angle construction and vector synthesis

## `C0:ABA2` computes an 8-bit angle index in `EE` from target-vs-current coarse coordinates

Inputs:
- target coarse coords in `F2/F3`
- current coarse coords in `F0/F1`

What it does:
- computes absolute X/Y deltas
- determines the quadrant
- seeds `EE` with one of:
  - `0x00`
  - `0x40`
  - `0x80`
  - `0xC0`
- refines that base angle through slope-quantization lookups from `C0:F300`

That means `EE` is not a 4-way direction.  
It is an **angle/octant-ish 8-bit index**.

The table at `C0:F300` is therefore best treated as a **slope-to-angle quantization table**.

### New label:
- `C0:ABA2  Compute_AngleEE_FromTargetDelta_CoarseXY`

---

## `C0:AC69` converts `EE` + speed `1A00` into signed motion vector components

This is the next big lock.

The routine:

- clears the current delta fields
- multiplies `1A00,X` by lookup values from `C0:F800` and `C0:F840`
- uses the `EE` angle index and `EE + 0x40`
- flips sign depending on which half of the angle range is active
- stores the results into:
  - `1980/1981`
  - `1900/1901`

This is a real **angle-indexed vector builder**.

The table at `C0:F800` is therefore best read as a **256-entry trig-like magnitude table** (sine/cosine style, quarter-shifted by `+0x40` between components).

### New label:
- `C0:AC69  Build_SignedMoveVector_FromAngleEE_AndSpeed1A00`

---

## `C0:ACFD` is the richer variant that also refreshes tile/side state after vector build

The code beginning at `C0:ACFD`:

- builds signed deltas from the same angle machinery
- projects those deltas into tentative position state
- uses `7E:7000` / `7E:7040`
- updates `0C00/0C01` based on the projected result

So this is not just “build vector.”  
It is more like:

- **build move vector**
- **derive/update placement-side metadata**

### New label:
- `C0:ACFD  Build_MoveVectorAndRefreshTileSideState_FromAngleEE`

---

## Movement update routine split

This pass also made the update-loop names much cleaner.

### `C0:AA07`
This is the main decrement-and-integrate path for one movement class.

Characteristics:
- decrements `1A01`
- applies signed deltas from `1900/1980`
- manually handles high-byte overflow/underflow
- optionally clamps and zeroes `1A01` when limits are crossed

### `C0:AAC7`
This is the alternate integrator when `1B80 != 0`.

Characteristics:
- decrements `1A01`
- integrates through wider/fractional state
- uses `1B81` as part of the second component update

### `C0:AAFD`
This is another simpler signed-delta integrator used by a different `1100,X` class.

### New labels:
- `C0:AA07  Update_ActiveMovement_Mode0_WithClampOrWrap`
- `C0:AAC7  Update_ActiveMovement_Mode1_WithFractionalAccumulator`
- `C0:AAFD  Update_ActiveMovement_Mode0_Signed8ToPos16`

---

## What is now substantially stronger than before

### Strong now
- `1A01` = active movement timer / remaining steps
- `1A80` = movement in-progress state byte
- `1B80` = motion update mode selector
- `1600` = coarse 4-way facing derived from an 8-bit angle
- `1900/1980` = signed motion vector components
- `ABA2` = target-delta -> angle index
- `AC69` = angle + speed -> signed movement deltas

### Still not fully solved
- exact user-facing meaning of each `1100,X` movement class
- exact meaning of `7F0B00,X` in the `AA07` path
- exact role of `1B81` beyond “extra state used by the alternate/fractional integrator”
- whether `1800` is the horizontal axis and `1880` vertical, or vice versa, in every map context

---

## Best next target

The best next move is following:

- `1100,X` movement class dispatch
- `A88D`
- `A98A`
- `A9CD`

That should tell us how the slot VM’s motion layer ties into collision, arrival, and post-move state transitions.
