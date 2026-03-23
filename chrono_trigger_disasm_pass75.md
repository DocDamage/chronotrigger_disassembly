# Chrono Trigger Disassembly — Pass 75

## Scope of this pass
This pass continues directly from the pass-74 seam.

Pass 74 tightened the late packet callers, but it still left one ugly blind spot in the fixed-`7F` follow-up tail:

- `C1:AC57`
- `C1:BFA4`
- the nearby `AE91..AE96` consumers
- the downstream side-effect helpers:
  - `FD:ABA2`
  - `FD:AC6E`

The biggest correction from this pass is simple but important:

> `C1:BFA4` is **not** a fuzzy helper blob.
> It is an exact tiny wrapper:
> `LDA #$04 ; JSR $0003 ; RTS`

That instantly sharpens `AC57`:

> the shared fixed-`7F` tail is **service-04 hook first, packet-apply second**.

This pass also finally gives the tail a concrete descriptor loader and queue-consumer shape instead of the older “some follow-up side effects happen here” wording.

---

## 1. `C1:BFA4` is an exact local service-`04` wrapper
Direct bytes:

```text
C1:BFA4  A9 04
C1:BFA6  20 03 00
C1:BFA9  60
```

That is as clean as it gets:

- load `A = 0x04`
- `JSR $0003`
- `RTS`

So this routine should no longer be treated like an unresolved mini-blob.
It is a real **service / local-dispatch wrapper for service id `04`**.

That also means the already-solved `AC57` tail is now tighter by force:

```text
C1:AC57  20 A4 BF
C1:AC5A  20 85 AC
C1:AC5D  60
```

So `AC57` is exactly:

1. run local service `04`
2. run `AC85 -> EC7F`
3. return

Safest upgraded reading:

> `C1:AC57` = **run service-`04` hook, then apply pending stat-delta channels**

That is materially stronger than the pass-74 wording that left `BFA4` open.

---

## 2. `C1:BF7F` copies a 17-byte descriptor/profile record from `CC:213F` indexed by `B18C`
Direct bytes:

```text
C1:BF7F  7B
C1:BF80  A8
C1:BF81  AD 8C B1
C1:BF84  C2 20
C1:BF86  85 0E
C1:BF88  0A 0A 0A 0A
C1:BF8C  18 65 0E
C1:BF8E  AA
C1:BF8F  7B
C1:BF90  E2 20
C1:BF92  BF 3F 21 CC
C1:BF96  99 E6 AE
C1:BF99  C8
C1:BF9A  E8
C1:BF9B  C0 11 00
C1:BF9E  90 F2
C1:BFA0  60
```

This computes:

- `X = 0x11 * B18C`

because the code does:

- `A = B18C`
- `A <<= 4`
- `A += original`

Then it copies `0x11` bytes from:

- `CC:213F + X`

into:

- `AEE6..AEF6`

So this routine is now structurally firm:

> `C1:BF7F` = **copy one 17-byte follow-up/descriptor profile record from `CC:213F` indexed by `B18C` into `AEE6..AEF6`**

That is the missing bridge between the follow-up context fields and a real descriptor table.

---

## 3. `C1:BFAA` initializes current-tail follow-up context, optionally loads the current descriptor, and runs the common tail
The large routine immediately after the tiny `BFA4` wrapper is where the useful shape finally appears.

Direct front-half bytes:

```text
C1:BFAA  7B
C1:BFAB  AD FC B1
C1:BFAE  09 02
C1:BFB0  8D FC B1
C1:BFB3  9C 93 AE
C1:BFB6  9C 94 AE
C1:BFB9  9C 95 AE
C1:BFBC  9C 96 AE
C1:BFBF  9C 99 AE
C1:BFC2  9C 9A AE
C1:BFC5  9C 9B AE
C1:BFC8  A9 FF
C1:BFCA  8D 97 AE
C1:BFCD  8D 98 AE
C1:BFD0  7B
C1:BFD1  8D 90 AE
C1:BFD4  AD 8B B1
C1:BFD7  8D 91 AE
C1:BFDA  A9 01
C1:BFDC  8D 92 AE
C1:BFDF  AD 8E AD
C1:BFE2  8D CC AE
C1:BFE5  A9 01
C1:BFE7  8D 8D AD
C1:BFEA  8D CB AE
C1:BFED  20 09 AD
C1:BFF0  8D 94 AE
```

That gives a very concrete setup contract:

- set `B1FC.bit1`
- clear `AE93/AE94/AE95/AE96/AE99/AE9A/AE9B`
- set `AE97 = AE98 = 0xFF`
- set `AE90 = 0`
- set `AE91 = B18B`
- set `AE92 = 1`
- seed single-entry selection state:
  - `AECC = AD8E`
  - `AECB = 1`
- build/store the one-hot first-entry mask through `AD09 -> AE94`

Then the next block resolves the current descriptor/profile only when the current live slot is occupied:

```text
C1:BFF3  AD 8B B1
C1:BFF6  AA
C1:BFF7  BD FF AE
C1:BFFA  C9 FF
C1:BFFC  F0 23
C1:BFFE  AA
C1:BFFF  BF 83 25 CC
C1:C003  8D 8C B1
C1:C006  20 7F BF
C1:C009  AD 23 AF
C1:C00C  D0 13
```

That proves this exact path:

- `AEFF[B18B]` = current occupant / resident id
- `CC:2583[occupant] -> B18C`
- `JSR BF7F` copies the corresponding 17-byte descriptor/profile into `AEE6..AEF6`
- if that descriptor-load/validation path leaves `AF23 != 0`, skip the common tail

And on success it runs:

```text
C1:C00E  20 57 AC
C1:C011  AD CC AE
C1:C014  C9 03
C1:C016  90 05
C1:C018  A9 01
C1:C01A  8D C0 B2
C1:C01D  22 EE AC FD
C1:C021  AD FC B1
C1:C024  29 FD
C1:C026  8D FC B1
C1:C029  60
```

So on success it:

- runs the common `AC57` tail
- arms `B2C0 = 1` when `AECC >= 3`
- clears transient packet workspace through `FD:ACEE`
- clears `B1FC.bit1`
- returns

Safest upgraded reading:

> `C1:BFAA` = **initialize current-tail follow-up context, optionally resolve/load the current occupant descriptor profile, run the common service-04 + packet-apply tail on success, optionally arm continuation, then clear transient workspace and exit**

This is the real “current-tail fixed follow-up context runner” that pass 74 was circling around.

---

## 4. `C1:AC57` is now best understood as “hook then apply,” not just “bridge into packet apply”
Pass 74 already proved the outer shape.
Pass 75 removes the only unresolved noun inside it.

Because:

- `AC57 = JSR BFA4 ; JSR AC85 ; RTS`
- `BFA4 = exact service-04 wrapper`
- `AC85 = exact `EC7F` wrapper`

The strongest safe reading is now:

> `C1:AC57` = **run service-04 follow-up hook, then apply queued stat-delta packets**

This matters because globals `91` and `99` both end through:

- `A = 0x7F`
- `JSR 895B`
- `JSR AC57`

So the fixed-`7F` late tail is no longer “some common post-context thing.”
It is concretely:

- context seed
- service-04 hook
- pending packet apply

---

## 5. `FD:ABA2` is a 7-byte slot-descriptor accumulator with optional unique-token queue fill
This helper is still not fully frozen at the gameplay-facing noun level, but its mechanics are now much tighter.

### Proven front-end gate
Direct bytes:

```text
FD:ABA2  7B
FD:ABA3  A6 0E
FD:ABA5  BD 12 AF
FD:ABA8  89 40
FD:ABAA  F0 03
FD:ABAC  4C 6D AC
FD:ABAF  BD 0A AF
FD:ABB2  C9 FF
FD:ABB4  D0 03
FD:ABB6  4C 6D AC
```

It only continues when:

- `AF12[slot]` does **not** carry bit `0x40`
- `AF0A[slot] != 0xFF`

So it is keyed by a real per-slot descriptor index in `AF0A`.

### Proven record size
The next block does:

- `DP28 = AF0A[slot]`
- `DP2A = 7`
- `JSL C1:FDBF`

Pass 52 already proved `C1:FDBF` is just the `C90B` multiply wrapper.
So this computes:

- `DP2C = 7 * AF0A[slot]`

That is a hard size proof:

> the helper is indexing a **7-byte descriptor record family**

### Proven accumulator writes
Using the resulting record offset `X = DP2C`, it accumulates table values from:

- `CC:5E00 + X`
- `CC:5E02 + X`
- `CC:5E06 + X`

into:

- `B28C`
- `B2A5`
- `B2DB/B2DD`

This is not a blind memcpy.
It is additive accumulation into live workspace totals.

### Proven optional token queues
When the record’s bytes at:

- `CC:5E04 + X`
- `CC:5E05 + X`

are nonzero, and the current slot’s `AE5D[slot-3]` carries bit `0x40`, the helper uses a threshold/selection subpath and then tries to insert the resulting 8-bit token into the first free entry of:

- `B2A7..B2A9`
- `B2AA..B2AC`

while avoiding duplicates.
When it successfully inserts, it ORs bit `0x20` into `B2AF`.

### Safest upgraded reading
The exact human-facing meaning of those accumulators and token queues is still open.
But the structure is now much stronger:

> `FD:ABA2` = **for one eligible slot, index a 7-byte descriptor record by `AF0A[slot]`, accumulate three live workspace totals, and optionally queue up to two small unique-token lists while setting `B2AF.bit5`**

That is materially better than leaving it as a vague “downstream side-effect helper.”

---

## 6. `FD:AC6E` consumes a pending queue and attempts slot admission/materialization
This helper is also still one notch below final gameplay-facing naming, but the outer structure is now real.

Direct entry bytes:

```text
FD:AC6E  AD B9 B3
FD:AC71  F0 77
FD:AC73  7B
FD:AC74  8D 15 B3
FD:AC77  7B
FD:AC78  AD 15 B3
FD:AC7B  AA
FD:AC7C  BD AC B3
FD:AC7F  C9 FF
FD:AC81  F0 5D
```

So it begins with a cursor/count gate:

- if `B3B9 == 0`, return
- otherwise mirror it into `B315`
- use `B3AC[B315]` as the next pending slot id
- if that slot id is `0xFF`, return

Then for the chosen slot it does all of the following:

- rejects lane blocks whose `5E4A` / `5E4B` flags fail the gate
- requires `5E78` bit `0x40`
- runs the same threshold/selection subpath used elsewhere in this neighborhood
- when admitted, may mark `AFAB[slot] = 1`
- seeds:
  - `B18B = slot`
  - `AD8E = selected value`
- then dispatches through the downstream materialization/helper path (`JSL C1:FDC7`)
- advances `B315`
- either continues the queue walk or clears `B3B9` and exits

The tail also hard-clears `B3B9` when the walk is finished.

### Safest upgraded reading
Without overclaiming the final gameplay noun:

> `FD:AC6E` = **consume the pending slot queue at `B3AC` under cursor/count `B3B9/B315`, validate each pending slot against lane/block gates, mark admitted slots, seed materialization inputs (`B18B`, `AD8E`), dispatch the downstream materialization helper, and clear the queue when done**

That is a real queue-consumer / admission runner.

---

## What changed structurally after this pass
Before this pass, the fixed-`7F` tail still looked like this:

- `895B` = context seed
- `AC57` = common tail into packet apply
- `BFA4` = unresolved helper
- `FD:ABA2` / `FD:AC6E` = vaguely known downstream side effects

After this pass, the seam looks more like this:

- `895B` = seed fixed follow-up context
- `AC57` = **run service-04 hook, then apply pending packets**
- `BFA4` = **exact local service-04 wrapper**
- `BF7F` = **17-byte descriptor/profile loader from `CC:213F` by `B18C`**
- `BFAA` = **current-tail follow-up-context initializer + descriptor-load + common-tail runner**
- `FD:ABA2` = **7-byte descriptor accumulator + optional unique-token queue filler**
- `FD:AC6E` = **pending slot queue consumer / admission-materialization runner**

That is a real cleanup pass, not just label churn.

---

## Honest caution
Three things should still stay explicit:

1. `FD:ABA2`'s accumulators `B28C/B2A5/B2DB` and token queues `B2A7/B2AA` are structurally real, but their final gameplay-facing nouns are still open.
2. `FD:AC6E` is clearly a pending queue consumer and admission/materialization runner, but the exact queue owner noun is still one notch below frozen.
3. `AE90..AE99` are now much better as a context block, but not every individual byte is ready for a final human-facing name yet.

---

## Best next seam after pass 75
The cleanest next targets are now:

1. the service dispatcher around local `JSR $0003`
   - especially how service id `04` behaves in the late fixed-`7F` path
2. the exact semantics of the 17-byte `CC:213F` descriptor/profile records copied into `AEE6..AEF6`
3. the exact role of the 7-byte `CC:5E00` records and the live accumulators:
   - `B28C`
   - `B2A5`
   - `B2DB/B2DD`
   - `B2A7..B2AC`
   - `B2AF`
4. the exact queue-owner noun behind:
   - `B3AC`
   - `B3B9`
   - `B315`

