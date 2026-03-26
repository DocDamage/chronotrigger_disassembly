# Chrono Trigger Disassembly Pass 60

## Scope of this pass
This pass continued directly from pass 59's open seam:

1. decode the late selector-control byte range `0x39..0x52`, with priority on the late `0x46..0x52` band
2. test whether that late band is the missing bridge into the `$0E -> AED3` deferred-tail reinsertion path
3. determine whether the late band is really more selector-wrapper logic, or a different kind of stateful executor
4. tighten the strongest late-range globals without globalizing unsupported gameplay nouns

The important outcome is:

> the late selector-control band is **not** the missing `$0E -> AED3` reinsertion bridge.
>
> The strongest real structure in this pass is a separate **stateful late selector pack executor** centered on:
>
> - `C1:AFD7..C1:B08E`
> - `CC:8B08`-indexed pointer records
> - secondary dispatch through `C1:B80D`
>
> This family executes FE/FF-delimited micro-packs, captures per-tail results into scratch/status arrays, and can chain to another pack segment.
>
> So the pass-59 seam narrows in a useful way:
>
> - the late band does **not** directly explain deferred-tail reinsertion
> - instead it opens a distinct late selector/executor subsystem

That is a real structural correction, not just a relabel.

---

## Method
1. Re-opened the late selector-control dispatch targets from pass 59:
   - `AFB6`
   - `AFC1`
   - `AFCC`
   - `AFD7`
   - `AFE2`
   - `AFED`
   - `AFF8`
   - `B003`
   - `B00E`
   - `B019`
   - `B024`
   - `B02F`
   - `B03A`
2. Reconstructed the shared fallthrough/common-tail structure around `AFD7..B08E`.
3. Checked the pointer source used by the full top-level entry.
4. Re-opened the helper reached from the common path:
   - `C1:B4AA..B4E6`
5. Reframed the late-range findings against the pass-57/59 deferred-tail question.

---

## 1. `0x49 -> C1:AFD7` is the first structurally complete top-level entry in the late selector-control band
Relevant bytes:

```text
C1:AFD7  0A AA BF 08 8B CC 8D D2 B1 AA 8E D0 B1
C1:AFE4  7B 85 0A E2 20 9C 24 AF BF 04 00 CC C9 FE F0 05
C1:AFF4  A9 01 8D CF B1 20 AA B4
C1:AFFC  7B AE D2 B1 BF 00 00 CC 8D 39 B2 0A AA FC 0D B8
```

### Strong structural read
This entry does something materially different from the pass-58/59 selector-wrapper family.

It:

1. doubles the already-doubled selector value again, forming a `4 * selector` byte offset
2. reads a **16-bit pointer** from `CC:8B08 + (selector * 4)`
3. stores that pointer into:
   - `B1D2`
   - `B1D0`
4. enters a common execution path that:
   - clears `AF24`
   - inspects byte `+4` at the selected pointer
   - optionally sets `B1CF = 1`
   - calls `B4AA`
   - reads byte `0` from the selected/adjusted pointer into `B239`
   - dispatches through `B80D`

That is **not** a plain selector wrapper and it is **not** a deferred-tail reinsertion helper.

It is a pointer-seeded executor.

### Immediate consequence
The pass-59 late range should not be described as “more selector wrappers.”
The `0x49` family is a different structure:

> **late selector-control byte -> pointer-record lookup -> pack/segment execution -> per-tail status capture**

---

## 2. `CC:8B08` is a late selector-control pointer-record table, and `0x49..0x52` index it at 4-byte stride
For selector-control bytes `0x49..0x52`, the first word of each `CC:8B08 + 4*n` record is:

```text
0x49 -> CC:8C2C -> A77B
0x4A -> CC:8C30 -> A7E5
0x4B -> CC:8C34 -> A8E5
0x4C -> CC:8C38 -> A96A
0x4D -> CC:8C3C -> AA1F
0x4E -> CC:8C40 -> AAE2
0x4F -> CC:8C44 -> ABB5
0x50 -> CC:8C48 -> ACDD
0x51 -> CC:8C4C -> AD5B
0x52 -> CC:8C50 -> ADFF
```

The record width is mechanically proved by `AFD7`:

- entry arrives with `A = selector * 2`
- `ASL A` produces `selector * 4`
- that doubled result is used as the `CC:8B08` index

### What is safely proved
The late control bytes are not indexing a simple pointer array of 2-byte entries.
They are indexing **4-byte records** at `CC:8B08`.

In this pass, only the **first word** of those records is directly used by the top-level executor.
The second word remains unresolved and should stay unlabeled.

---

## 3. The common path executes FE/FF-delimited late selector packs and can chain to a second sub-op
Relevant common bytes:

```text
C1:AFE2  7B 85 0A E2 20 9C 24 AF
C1:AFEA  BF 04 00 CC C9 FE F0 05 A9 01 8D CF B1
C1:AFF8  20 AA B4
C1:AFFB  7B AE D2 B1 BF 00 00 CC 8D 39 B2
C1:B006  0A AA FC 0D B8
C1:B00C  AD CF B1 F0 16
C1:B011  AE D0 B1 E8 E8 E8 E8 8E D2 B1
C1:B019  BF 00 00 CC 8D 39 B2 0A AA FC 0D B8
```

### Strong structural read
This path has a consistent shape:

1. look at byte `+4` from the current pack/segment pointer
2. if it is not `FE`, set `B1CF = 1`
3. run `B4AA`
4. read byte `0` from the selected pack/segment into `B239`
5. dispatch through the secondary table at `B80D`
6. if `B1CF != 0`, advance the pointer by `+4` and dispatch a **second** sub-op through `B80D`

That proves the current late-pack segment supports either:

- one 4-byte sub-op
- or two chained 4-byte sub-ops, with the second one starting at `+4`

### FE / FF role
The later continuation path proves the sentinel roles more strongly:

```text
C1:B051  9C CF B1
C1:B054  AE D2 B1
C1:B057  E8
C1:B058  BF 00 00 CC C9 FE D0 F7
C1:B060  8E D2 B1
C1:B063  9C C0 B2
C1:B066  AE D2 B1
C1:B069  E8
C1:B06A  BF 00 00 CC C9 FF D0 F7
C1:B073  8E D2 B1
C1:B076  BF 00 00 CC C9 FF F0 10
```

This is strong enough to state:

- `FE` = segment terminator / boundary sentinel
- `FF` = end-of-pack sentinel

So the late family is executing **FE/FF-delimited micro-packs**, not flat wrappers.

---

## 4. `C1:B4AA..B4E6` is the segment-selection helper for the late pack executor
The common path does not dispatch directly from the pointer loaded at `AFD7`.
It first passes through `B4AA`.

Even without overclaiming its gameplay noun, the structure is now useful enough to promote:

- it receives/stores the current pack pointer in `B1D2`
- it uses the current tail-local index in `B252`
- it performs helper math through `C90B/C92A`-style arithmetic scratch
- it conditionally adjusts the selected pointer before the `B80D` dispatch

Best safe reading after this pass:

> `B4AA` is the **tail-local segment selector / pointer adjuster** used by the late selector-pack executor

This is still not the place to force a final gameplay noun, but it is much stronger than “some helper before `B80D`.”

---

## 5. `B239`, `B24A`, `B263`, and `B1CF` are real late-pack executor scratch/status fields
Relevant bytes:

```text
C1:AFFC  ... BF 00 00 CC 8D 39 B2 0A AA FC 0D B8
C1:B028  AD 52 B2 AA AD 24 AF 9D 4A B2
C1:B032  C9 02 D0 05 A9 00 9D B6 B2
C1:B045  A9 FF 9D 42 B2
C1:B07E  8E D0 B1
C1:B081  AD 52 B2 AA FE 63 B2
C1:B08E  AD 52 B2 AA 9E 63 B2 60
```

### Strong results from this pass
- `B239` is the current **late-pack sub-op byte** sent to `B80D`.
- `B1CF` is a **has chained second sub-op** flag for the currently selected segment.
- `B24A[B252]` captures the resulting `AF24` status after the sub-op execution.

### Provisional but useful results
- `B263[B252]` is a **has another FE-delimited segment after the current one** flag/counter.
  - it is incremented when another segment is found and immediately chained
  - it is cleared when no additional segment remains
- `B242[B252]` is a **nonzero-result invalidation/mark byte** set to `FF` on the nonzero-`AF24` path.
  - its exact higher-level noun is still open
- `B2B6[B252]` is explicitly cleared when `AF24 == 2`, which is a meaningful special-case result code in this executor family

The exact human-facing meaning of those result codes still needs the downstream consumers.

---

## 6. This late family does **not** touch the deferred-tail reinsertion path
One of the reasons to decode this band was the pass-59 suspicion that it might bridge into the unresolved `$0E -> AED3` path.

This pass materially narrows that suspicion.

What the late family actually does is:

- read pointer records from `CC:8B08`
- select/adjust a pack segment with `B4AA`
- dispatch late sub-ops through `B80D`
- capture `AF24` into per-tail result/status scratch
- optionally advance to another FE-delimited segment

What it does **not** do here:

- load `$0E`
- compare against `AF0D[x]`
- write `AF02[x] = AF0D[x]`
- clear `AF15.bit7`
- call or fall into `AED3`

So the late selector-control executor is a separate subsystem seam, not the reinsertion bridge.

That is a real narrowing of the search space.

---

## 7. Important caution: parts of `0x46..0x48` and `0x51..0x52` still look like alias/overrun entrypoints, not safely promotable standalone control bytes
Pass 59 mechanically parsed the `B8BB` table through `0x52` because the pointer words continue cleanly.

This pass shows why that alone is **not** enough to promote every late byte as a normal standalone selector-control byte.

Examples:

- `0x46 -> AFB6` lands on a short branch into a stack-sensitive shared tail
- `0x47 -> AFC1` and `0x48 -> AFCC` fall through a `PLX`-based tail with no local `PHX` in the entry body
- `0x51 -> B02F` and `0x52 -> B03A` are clearly deep internal alias points into the status/continuation logic, not clean top-level initializers

So after this pass, the safest wording is:

- `0x49` is the first clearly top-level late-pack initializer
- `0x4A..0x50` are context-dependent alias entries into its shared executor
- `0x46..0x48` and `0x51..0x52` should remain **late-range alias/overrun candidates**, not globally promoted standalone control bytes

This is an important correction to the broadest possible read of pass 59.

---

## Net result of pass 60
Pass 59 left the search centered on the late selector-control range as the best bridge candidate into deferred reinsertion.

Pass 60 changes that in a useful way.

The strongest new model is:

- the late range opens a separate **stateful late selector-pack executor**
- the key top-level entry is `0x49 -> AFD7`
- that entry indexes `CC:8B08` 4-byte records
- the first word of each record points to an FE/FF-delimited micro-pack
- `B4AA` selects the current tail-local segment
- `B80D` executes one or two 4-byte sub-ops from that segment
- results are captured into per-tail executor scratch/status arrays

So the next seam is no longer “assume late selector bytes must explain `AED3`.”

The better next seam is:

1. decode the `B80D` late-pack sub-op family as a unit
2. identify the downstream consumers of:
   - `B239`
   - `B24A`
   - `B242`
   - `B263`
3. then return to deferred reinsertion with a cleaner separation between:
   - the late selector-pack executor
   - the actual `$0E -> AED3` materialization problem

---

## Suggested next seam
The strongest next continuation point after pass 60 is:

1. decode `C1:B80D` as the late-pack secondary dispatch table
2. determine the exact meaning of `AF24` result codes in this family, especially:
   - `0`
   - `2`
   - nonzero-not-2
3. identify downstream consumers of:
   - `B24A[x]`
   - `B242[x]`
   - `B263[x]`
4. only then revisit whether any of those late-pack sub-ops can indirectly feed the deferred-tail materialization side
