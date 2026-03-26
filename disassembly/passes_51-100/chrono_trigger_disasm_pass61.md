# Chrono Trigger Disassembly Pass 61

## Scope of this pass
This pass continued directly from pass 60's open seam:

1. re-open `C1:B80D` itself instead of treating it as a late-pack-only helper table
2. determine how `B80D` relates to the already-solved `B85F`, `B88D`, and `B8BB` slices
3. tighten the controller that records late-pack execution into `B242 / B24A / B263`
4. correct any pass-60 provisional labels that no longer survive direct byte proof

The main result of this pass is a structural correction:

> `C1:B80D` is not a dedicated late-pack subopcode table.
>
> It is the **master bank-C1 opcode dispatch table**.
>
> The tables previously carried as:
>
> - `B85F` (group 1)
> - `B88D` (group 2)
> - `B8BB` (inline selector-control)
>
> are all just **interior slices of that same master table**.
>
> So the pass-60 “late selector pack subopcode” model was too narrow.
> The late pack executor is actually feeding **global bank-C1 opcode bytes** back into the same shared dispatcher used by the rest of the engine.

That is a real architectural change, not a wording tweak.

---

## Method
1. Re-opened `C1:B80D..B95F` as one contiguous pointer table instead of reading only the pass-60 entrypoints.
2. Measured the exact slice offsets for:
   - `B85F`
   - `B88D`
   - `B8BB`
3. Re-checked the late-pack common path around:
   - `AFFB..B024`
   - `8C0A..8CF7`
4. Verified what gets stored to:
   - `B239`
   - `B242[x]`
   - `B24A[x]`
   - `B263[x]`
5. Reframed the late-pack executor against the already-solved group-1, group-2, and selector-control work from passes 32-35 and 59-60.

---

## 1. `C1:B80D..C1:B95F` is one master opcode dispatch table
The late-pack executor still does the same local step proved in pass 60:

```text
C1:AFFB  AE D2 B1
C1:AFFE  BF 00 00 CC
C1:B002  8D 39 B2
C1:B005  0A
C1:B006  AA
C1:B007  FC 0D B8
```

That is:

1. load the current opcode byte from the selected CC segment into `B239`
2. double it
3. use it as an index into `JSR ($B80D,X)`

The new part of this pass is the table geometry.

### Exact slice offsets
The already-known dispatch entrypoints line up exactly as interior slices:

- `B80D + (0x29 * 2) = B85F`
- `B80D + (0x40 * 2) = B88D`
- `B80D + (0x57 * 2) = B8BB`

So the prior “separate tables” are really these global ranges:

- global `0x29..0x3F` = the old local group-1 table at `B85F`
- global `0x40..0x52` = the old local group-2 table at `B88D`
- global `0x57..0xA9` = the old local selector-control table at `B8BB`

### What this proves
`B80D` is the real root dispatcher.
The later entrypoints are just convenient slices into the same pointer table.

So the correct architecture is now:

> **master C1 opcode dispatch table**
>
> with multiple callers entering it at different local-numbering slices.

That is stronger and cleaner than carrying three “separate” top-level tables forever.

---

## 2. The late-pack executor is reusing the same global opcode space, not a private micro-op space
Because the late-pack executor uses `JSR ($B80D,X)`, the bytes in the FE/FF-delimited late packs are not just local executor-private opcodes.
They are entries in the same shared global bank-C1 opcode space.

### Concrete consequence
The late-pack layer can directly reuse already-solved handler families.

Examples from the slice alignment:

- global `0x29` enters the old group-1 local `0x00`
- global `0x40` enters the old group-2 local `0x00`
- global `0x57` enters the old selector-control local `0x00`
- global `0xA0` enters the pass-60 late top-level executor at `AFD7`

So the late-pack system is not a detached mini-VM.
It is a **macro/script layer over the master C1 opcode table**.

That is why pass-60's `B80D` findings fit so cleanly with the earlier solved command families once the table is viewed globally.

---

## 3. `B239` and `B242[x]` are now pinned much harder
Pass 60 correctly proved that `B239` is loaded from the current CC segment immediately before the `B80D` dispatch.

This pass tightens the tail-local mirror.

Relevant bytes:

```text
C1:8C3E  7B
C1:8C3F  AD 52 B2
C1:8C42  AA
C1:8C43  AD 39 B2
C1:8C46  9D 42 B2
```

That is:

1. `X = B252`
2. `A = B239`
3. `STA B242,X`

### Correction to pass 60
The pass-60 provisional label for `B242[x]` as a nonzero-result mark byte does not survive direct proof.

`B242[x]` is not a boolean/nonzero marker.
It is the per-tail **last executed global opcode byte**.

So the late-pack controller is explicitly recording, per tail slot:

- which global opcode just ran (`B242[x]`)
- what result/status it produced (`B24A[x]`)
- whether/where more chained segment work remains (`B263[x]`)

That is a much better fit for the controller logic around `8C3E`.

---

## 4. `C1:8C0A..8CF7` is the tail replay/controller layer around the master opcode dispatcher
This pass does not yet give every byte in this block a final gameplay-facing noun, but the control role is much cleaner now.

### `8C0A..8C37`
This block:

- clears `B24A[x]`
- clears `B263[x]`
- iterates the live tail map
- skips withheld tail entries (`AF15.bit7`)
- can call the materialization helper path through `AFD2`

That is not “generic cleanup.”
It is the front end that prepares the per-tail execution state before replaying the late-pack flow.

### `8C3E..8CF7`
This block:

1. records the just-executed global opcode into `B242[x]`
2. captures `AF24` into `B24A[x]`
3. searches for the next `FE` segment boundary
4. updates the segment pointer state in `B1D2 / B1D0 / B273`
5. increments or clears `B263[x]` depending on whether another FE-delimited segment remains
6. resumes execution from the next byte at the updated CC pointer

The important structural detail is what happens at the resume point:

```text
C1:8CD8  AE 73 B2
C1:8CDB  8E D2 B1
C1:8CDE  BF 00 00 CC
C1:8CE2  8D E3 AE
C1:8CE5  30 13
C1:8CE7  0A
C1:8CE8  AA
C1:8CE9  FC 5F B8
```

If the resumed byte is non-negative, execution continues through `JSR ($B85F,X)`.

That is the already-solved group-1 slice.

So the replay/controller layer does **not** just loop inside the pass-60 late executor.
It can hand control straight into the older group-1 command slice after advancing to the next CC byte.

This is another reason the master-table read is the right one.

---

## 5. Revised interpretation of the late-pack subsystem
### Old pass-60 wording
- late selector pack executor
- late selector pack subopcode
- separate late-pack dispatch helper table

### Stronger wording after pass 61
The stronger structural model is:

- `CC:8B08` selects a late pointer-record family
- `AFD7..B08E` seeds and executes FE/FF-delimited pack segments
- `B80D..B95F` is the **master C1 opcode dispatch table** used by that executor
- `8C0A..8CF7` is the **tail replay/controller layer** that records per-tail execution state and resumes through the shared opcode slices

So the late system is now best read as:

> a **tail-oriented pack/replay layer over the shared C1 master opcode space**

not as a detached private micro-op VM.

---

## 6. What this changes in prior pass framing
### `B85F`
Keep the old local group-1 numbering because it is useful, but its root label should now clearly state that it is a **slice entrypoint** inside the master table.

### `B88D`
Same correction: useful local numbering, but not an independent root table.

### `B8BB`
Same correction again: selector-control local numbering is still useful, but it is a **slice** inside the same master dispatcher.

### `B242[x]`
Correct the old provisional label.
It is the **per-tail last executed global opcode byte**, not a generic nonzero-result mark.

---

## Strongest safe labels upgraded by this pass
- `C1:B80D..C1:B95F` = master bank-C1 opcode dispatch table
- `C1:B85F..C1:B88C` = group-1 local dispatch slice inside the master table
- `C1:B88D..C1:B8BA` = group-2 local dispatch slice inside the master table
- `C1:B8BB..C1:B95F` = selector-control local dispatch slice inside the master table
- `7E:B242..7E:B249` = per-tail last executed global opcode bytes
- `C1:8C0A..C1:8CF7` = tail pack replay/controller layer around the master dispatcher

---

## Remaining uncertainty
This pass does **not** solve every early global opcode in the `0x00..0x28` band.
Those still need real handler-by-handler work.

It also does **not** fully close the `$0E -> AED3` deferred materialization bridge.
What it does is separate that question from a wrong model of `B80D`.

The engine picture is cleaner now even though every individual opcode is not yet named.

---

## Next clean seam
1. decode the early global opcode band in `B80D`:
   - especially the actually observed late-pack opcodes like `00, 01, 02, 04, 05, 06, 07, 09, 0A, 0B, 0F, 12, 15, 1B, 20`
2. determine exactly when the replay/controller resumes through:
   - the group-1 slice (`B85F`)
   - the selector-control slice (`B8BB`)
3. only then re-open the deferred-tail reinsertion search with the dispatcher geometry finally corrected
