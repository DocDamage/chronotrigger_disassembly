# Chrono Trigger (USA) — Disassembly Pass 15

## What this pass focused on

This round followed the **arrival / active-region / post-move bookkeeping side** of the movement system.

The concrete targets from the previous pass were:

- `C0:A88D`
- `C0:A947`
- `C0:A98A`
- `C0:A9CD`

The goal was to answer:

- what actually happens after the movement integrators update position
- whether the engine is just flipping a visible flag, or maintaining real per-slot region membership structures
- how moved slots get reclassified after `1800/1880` change

---

## Biggest conclusion

## Movement update is tied directly to an **active-region spatial bucket system**

This is the useful architectural win from this pass.

The movement layer is not just:

- update position
- maybe update facing

It is also:

- test whether the slot is still inside the current active region/window
- activate/deactivate that slot when crossing the boundary
- remove the slot from an old linked bucket
- recompute camera-relative coarse cell state
- insert the slot into the new linked bucket

That is a much tighter and more practical model than “collision or arrival probably happens somewhere.”

---

## Hard dispatch findings from the main loop

The block beginning at `C0:A810` is now much clearer.

It loads the slot count from `7F:2000`, iterates `X = 0,2,4,...`, and dispatches by `1100,X`.

### Observed split
- `1100 < 3` → skipped here
- `1100 == 7` → `JSR C0:AAFD`, then `JSR C0:A88D`
- `1100 == 8` → `JSR C0:A947`
- other `1100 >= 3` cases seen in this loop → `JSR C0:AA07`, then `JSR C0:A88D`

When `C0:A88D` returns carry set, the loop does:

- `JSR C0:C98A`
- `JSR C0:A98A`
- `JSR C0:AB45`
- `JSR C0:A9CD`

That is the clearest sign yet that the movement/update layer is maintaining an explicit **spatial membership structure**.

### Stronger naming upgrade
- `1100,X` is now best treated as a **slot update / movement class byte**

I am still not pretending every class value is solved, but the class split is real.

---

## `C0:A88D` is an active-region membership updater

This routine is now much more specific.

### What it does
It builds a padded bounds window from:

- `1D0A`
- `1D0C`
- `1D0E`
- `1D10`

Then it compares the slot’s high position bytes:

- `1801,X`
- `1881,X`

against that window.

### Padding used
- X-ish bounds: `left - 4`, `right + 4`
- Y-ish bounds: `top - 2`, `bottom + 5`

The high position bytes are doubled before comparison (`ASL`), so the window test is happening in the same scaled coordinate space the engine is using for this phase.

### Inside-window behavior
If the slot is inside the padded region:

- if `0F00,X` is already negative, it immediately returns carry set
- otherwise it:
  - sets `0E80,X = 0x80`
  - sets `0E81,X = 0x80`
  - sets `0F00,X = 0x80`
  - clears `1681,X`
  - clears `1601,X`
  - clears `1B00,X`
  - sets `0F01,X = 0xFF`
  - calls:
    - `7170`
    - `6F9A`
    - `A9CD`
  - returns carry set

### Outside-window behavior
If the slot is outside the padded region:

- if `0F00,X` is non-negative already, it just returns carry clear
- if `0F00,X` is negative, it:
  - clears `0F00,X`
  - calls:
    - `EA42`
    - `734C`
    - `7056`
    - `A98A`
  - performs a couple of state notifications through `7F:0A00,X`, `7F:0B01,X`, and DP `$29`
  - returns carry clear

### Clean read now
`C0:A88D` is not a generic collision routine.

It is best read as:

- **test slot against current active-region window**
- **activate/register if entering**
- **deactivate/unregister if leaving**

### New label
- `C0:A88D  Update_SlotActiveRegionMembership_AndActivationState`

---

## `0F00` is an active-region / active-membership sentinel

This byte is now materially stronger than before.

Observed behavior:
- `A88D` sets it to `0x80` when activating the slot
- later calls treat a negative value as “already active/in-region”
- leaving the active region clears it to `0`
- `A947` also sets/clears it directly based on the simpler region test

So the no-BS read is:

- `0F00,X < 0` → slot currently marked active / inside region
- `0F00,X >= 0` → not currently active / not registered in that region path

### New label
- `0F00,X  SlotActiveRegionFlag`

---

## `C0:A947` is the simple region test/setter used by movement class 8

This smaller helper performs a narrower version of the same region check.

It computes bounds from the same `1D0A/0C/0E/10` group, but with a simpler window:

- X-ish: `left - 4`, `right + 4`
- Y-ish: `top + 0`, `bottom + 5`

If inside:
- sets `0F00,X = 0x80`
- returns carry set

If outside:
- clears `0F00,X`
- returns carry clear

This routine does **not** do the full activation/deactivation call set from `A88D`.

### Clean read
This is a **lightweight active-region flag updater**, probably for a class that does not need the full registration path.

### New label
- `C0:A947  Test_SlotAgainstActiveRegion_SimpleAndSet0F00`

---

## `C0:A98A` and `C0:A9CD` are real linked-list remove/insert routines

This was the biggest structural lock in the pass.

These routines are not vague bookkeeping anymore.

They operate on:

- `0E00`
- `0E01`
- `0E80`
- `0E81`

with a bucket key derived from:

- `0A80,X >> 1 & 0xFE`

### `C0:A9CD` = insert if absent
Behavior:
- if `0E01,X` is non-negative, it returns immediately
- otherwise it computes the bucket index from `0A80,X`
- reads `0E00[bucket]` as the current bucket head

If the head is negative:
- `0E00[bucket] = X`
- `0E01,X = 0`
- `0E80,X = 0x80`
- `0E81,X = 0x80`

If the head is valid:
- old head’s `0E80 = X`
- `0E81,X = old head`
- `0E00[bucket] = X`
- `0E01,X = 0`

### `C0:A98A` = remove if present
Behavior:
- if `0E01,X` is negative, it returns immediately
- otherwise it removes the slot from that same bucketed linked structure

If `0E80,X` is negative:
- the slot is the bucket head
- bucket head is replaced with `0E81,X`
- if the new head is valid, its `0E80` gets the sentinel `0x80`

If `0E80,X` is valid:
- it patches:
  - `next.prev = prev`
  - `prev.next = next`

Then it sets:
- `0E80,X = 0x80`
- `0E81,X = 0x80`
- `0E01,X = 0x80`

### Clean field model now
- `0E00[bucket]` = bucket head index
- `0E80,X` = previous link / prev sentinel
- `0E81,X` = next link / next sentinel
- `0E01,X` = list-membership sentinel
  - negative = absent/unlinked
  - non-negative = present/linked

### New labels
- `C0:A98A  Remove_SlotFromBucketList_By0A80`
- `C0:A9CD  Insert_SlotIntoBucketList_By0A80_IfAbsent`

---

## `AB45` + `A98A/A9CD` prove the post-move rebucketing path

This is the part that ties movement to spatial membership cleanly.

When `A88D` returns carry set in the main loop, the code does:

1. `A98A` — remove old bucket membership
2. `AB45` — recompute coarse camera-relative cell state
3. `A9CD` — insert into the new bucket

So the engine is explicitly **rebucketing moved active slots** after motion update.

That is much better than just saying “maybe collision gets checked later.”

---

## `0A80` is part of the camera-relative coarse cell state, and it is used as the bucket key

The earlier routine at `C0:AB45` already showed that `0A00/0A80` are derived from position versus camera/region-origin state.

This pass tightens that further:

- `0A80` is not just some random cached value
- it directly feeds the linked-bucket index through:
  - `LSR`
  - `AND #$FE`

So the bucket structure is keyed by a **camera-relative coarse slot position**, with `0A80` providing the grouping dimension.

### Honest interpretation
This is very likely some kind of **row/cell bucket** for later per-bucket traversal.

I am **not** claiming the final consumer is definitively “render only” yet, because the exact downstream use still matters.

But it is no longer honest to call it generic unknown bookkeeping.

---

## Why this matters

The movement layer now looks like this:

1. VM opcode starts or updates motion
2. motion integrator updates `1800/1880`
3. active-region logic checks whether the slot should still be considered live/in-region
4. if live, the slot is removed from its old bucket, coarse cell state is recomputed, and it is inserted into the new bucket

That is a real engine architecture, not a pile of unrelated bytes.

---

## What is now substantially stronger

### Strong now
- `A88D` = active-region membership updater with activation/deactivation side effects
- `A947` = lightweight region test/setter for class 8
- `0F00` = active-region sentinel
- `A98A` = remove from bucketed doubly linked list
- `A9CD` = insert into bucketed doubly linked list
- `0E00` = bucket head table
- `0E80/0E81` = prev/next link bytes
- `0E01` = list-membership sentinel
- `1100` = slot update/movement class byte
- post-move pipeline includes explicit rebucketing via `AB45`

### Still not fully solved
- exact final consumer(s) of the bucket lists
- exact semantics of class values `3..8`
- exact user-facing meaning of `0F01`
- exact meanings of the activation/deactivation helpers:
  - `7170`
  - `6F9A`
  - `EA42`
  - `734C`
  - `7056`
  - `C98A`

---

## Best next target

The cleanest next step is following the downstream traversal of the bucket lists.

The strongest visible candidate in bank `C0` is the code around `B2A0`, which iterates:

- `0E00[bucket]`
- then `0E81` next links

That should tell us whether these rebucketed active slots are primarily feeding:

- render ordering
- spatial update
- collision/proximity work
- or a hybrid object-processing pass
