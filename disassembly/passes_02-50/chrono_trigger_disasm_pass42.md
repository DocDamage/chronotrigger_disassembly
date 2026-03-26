# Chrono Trigger Disassembly Pass 42

## Scope of this pass
This pass continued directly from pass 41’s live seam:

- decode the downstream `93F3` category-dispatch families behind `C1:B96A..BA25`
- determine whether the nibble values in `93F3` are arbitrary IDs or a tighter lane set
- classify the helpers at `FD:A8A5`, `FD:A8CE`, `FD:A8FE`, `FD:A93C`, and `FD:A95F`
- re-check the upstream `9F38[x]` producer question without forcing a bad label

This pass did **not** try to rename the entire gameplay subsystem.
It stayed on the exact helper band that pass 41 exposed.

---

## Method
1. Re-traced `C1:B575..B6C9` as the front-end that interprets the canonical trio’s packed category bytes.
2. Decoded the helper family at:
   - `FD:A8A5`
   - `FD:A8CE`
   - `FD:A8FE`
   - `FD:A93C`
   - `FD:A95F`
3. Confirmed the tiny wrapper at `C1:B961`.
4. Did a targeted ROM-wide operand scan for direct accesses to `7E:9F38` to check whether a clean writer could be pinned this pass.

---

## Starting point from pass 41
Pass 41 had already proven:

- `93EE / 93F5 / 93FC` are the three canonical fixed records
- `93F3 + 7*n` is a packed low/high nibble category pair for those records
- the dispatch path behind `B96A..BA25` fans out through `FD:A8A5` / `FD:A93C` families
- `9F38[x]` feeds the emitted `93EF` aux byte, but its human-facing meaning and producer path were still unresolved

That is the exact seam this pass tightened.

---

## 1. `C1:B575..B6C9` is a **canonical-record category reconciler** over exactly three lane IDs: `0`, `1`, `2`
The start of the routine is much more informative than it looked on a casual pass:

```text
C1:B575  TDC
C1:B576  TAX
C1:B577  LDA #$FF
loop:
C1:B579  STA $B3EB,X
C1:B57C  INX
C1:B57D  CPX #$0009
C1:B580  BCC loop

C1:B582  TDC
C1:B583  STA $B3EB
C1:B586  INC A
C1:B587  STA $B3EE
C1:B58A  INC A
C1:B58B  STA $B3F1
C1:B58E  STZ $B3E7
C1:B591  STZ $B3E8
C1:B594  STZ $B3E9
```

So the routine does **not** start from arbitrary category bytes.
It explicitly seeds three root values:

- `B3EB = 0`
- `B3EE = 1`
- `B3F1 = 2`

Everything else in `B3EB..B3F3` starts as `FF`.

This makes the nibble space materially tighter:

> the meaningful nibble values here are **lane IDs `0`, `1`, and `2`**, with `F` used as the disabled / no-category sentinel.

That is stronger than the pass-41 wording of “small dispatch category IDs.”

---

## 2. The low and high nibbles of the canonical trio populate a **3 x 3 lane-membership scratch matrix**
After seeding the three root lane IDs, the routine reads the category-pair bytes from the three canonical records:

- `93F3`
- `93FA`
- `9401`

For each byte, it splits:

- low nibble
- high nibble

and conditionally stores only lane IDs `0/1/2`, ignoring `F`.

The scratch layout is:

```text
lane 0 family -> B3EB / B3EC / B3ED
lane 1 family -> B3EE / B3EF / B3F0
lane 2 family -> B3F1 / B3F2 / B3F3
```

The important structural result is that these are **not** three unrelated buckets.
They are a small reconciler matrix derived from the three canonical records’ nibble pairs.

Safest reading:

> `C1:B575..B6C9` = **reconcile the canonical trio’s packed nibble pairs into lane-family scratch arrays and final lane-enable flags**

---

## 3. `FD:A8A5` is a **lane-eligibility gate** over three `0x80`-spaced WRAM blocks
`FD:A8A5` no longer looks like generic cleanup.
The key transform is:

```text
REP #$20
XBA
LSR
TAY
SEP #$20
```

When the caller supplies lane IDs `0`, `1`, or `2` in 8-bit A, this produces:

- lane `0` -> `Y = 0x0000`
- lane `1` -> `Y = 0x0080`
- lane `2` -> `Y = 0x0100`

So the helper is explicitly selecting one of **three `0x80`-byte lane blocks**.

Then it tests:

```text
LDA $5E4A,Y
BIT #$80
BNE hit

LDA $5E4E,Y
ORA $5E53,Y
BIT #$80
BNE hit

LDA $5E4B,Y
BIT #$86
BEQ miss

hit:
LDA #$01
STA $B3EA
```

So the helper’s actual job is:

> given lane ID `0/1/2`, test the corresponding `0x80`-spaced WRAM lane block for eligibility and set `B3EA = 1` if any of the lane’s qualifying bits are present.

This is a strong structural result even though the exact gameplay meanings of the bits at `5E4A/5E4B/5E4E/5E53` still need a later pass.

---

## 4. `B3E7 / B3E8 / B3E9` are **final lane-enable flags**, not generic scratch
The three loops at `C1:B63B`, `B66A`, and `B699` are now much clearer.

Each loop:

1. picks one lane family root (`0`, then `1`, then `2`)
2. tries up to three candidate lane IDs from that lane family
3. calls `FD:A8A5` on each non-negative entry
4. if any candidate lane block is eligible, sets final enable flags in `B3E7/B3E8/B3E9` according to which sibling lane IDs are present in the family

So `B3E7/B3E8/B3E9` are not arbitrary temporaries.
They are the **final three-lane enable mask** produced from the canonical trio’s nibble pairs plus the lane-block eligibility test.

Safest reading:

> `7E:B3E7..B3E9` = **final enabled-lane flags derived from canonical-record category pairs and lane-block eligibility**

---

## 5. `FD:A93C` is the **phase-1 enabled-lane clear/reset dispatcher**
`FD:A93C` simply walks the three final lane flags:

```text
if B3E7 != 0 -> lane = 0 -> JSR A8CE
if B3E8 != 0 -> lane = 1 -> JSR A8CE
if B3E9 != 0 -> lane = 2 -> JSR A8CE
RTL
```

So this is not an opaque action family.
It is a compact dispatcher over the final lane mask.

Safest reading:

> `FD:A93C` = **iterate enabled lanes and run phase-1 clear/reset helper `A8CE`**

---

## 6. `FD:A8CE` is a **canonical-record lane clear/reset helper** for one `7`-byte fixed record
The first operation is:

```text
LDA lane
ASL
ASL
ASL
SEC
SBC lane
TAX
```

That computes:

> `X = lane * 7`

So the helper is directly indexing the fixed canonical record stride.

Then it clears:

```text
STZ $93EE,X
STZ $93EF,X
LDA #$FF
STA $93F3,X
```

That is the exact status/aux/category trio that pass 41 tied to the canonical fixed records.
So `A8CE` is explicitly clearing one canonical record slot’s key metadata.

After that it resets per-lane state using the lane number in `$14`:

```text
LDA $B158,X -> STA $AFAB,X
                STA $99DD,X
                STA $9F22,X
STZ $B188,X
STZ $B03A,X
RTS
```

This makes `A8CE` much more concrete than “some category helper.”

Safest reading:

> `FD:A8CE` = **clear one canonical 7-byte record slot and reset the matching lane’s carried state**

The exact human-facing roles of `AFAB/99DD/9F22/B188/B03A` are still open, so this should remain a structural label, not a flavor label.

---

## 7. `C1:B961` is a tiny **service-2 wrapper**
This byte sequence is direct:

```text
C1:B961  LDA #$02
C1:B963  JSR $0003
C1:B966  RTL
```

Pass 37 already proved `JSR $0003` is the bank-C1 local-service dispatcher and that service 2 routes to `C1:1BAA`.

So `C1:B961` is simply:

> **invoke local service 2**

This matters because the next helper uses it.

---

## 8. `FD:A95F` is the **phase-2 enabled-lane refresh dispatcher**
`FD:A95F` is the sibling of `A93C`.
It walks the same final lane mask in `B3E7/B3E8/B3E9`, but it calls `A8FE` instead of `A8CE`.

So the downstream family is now clearly two-phase:

- phase 1: `A93C -> A8CE`
- phase 2: `A95F -> A8FE`

That is a real structural split, not noise.

---

## 9. `FD:A8FE` is a **conditional lane clear/reset helper with service-2 refresh**
`A8FE` begins by checking one lane-local byte:

```text
LDA $B188,X
BEQ done
```

So unlike `A8CE`, this helper only runs if the lane is currently marked/occupied in that local byte.

If the lane is active, it performs the **same canonical-record clear** and the **same lane-state reset copies** as `A8CE`, but then it does one additional step:

```text
JSL C1:B961
RTS
```

Since `C1:B961` is the service-2 wrapper, the actual reading is:

> `FD:A8FE` = **if the lane is currently occupied/latched, clear the canonical record, reset the lane state, and then invoke local service 2**

This is one of the cleanest concrete results in the pass.

---

## 10. The downstream `93F3` family is now best described as a **three-lane reconcile + two-phase lane-reset pipeline**
Putting sections 1–9 together:

1. the canonical trio’s `93F3` bytes carry two lane IDs each (plus `F = none`)
2. `C1:B575..B6C9` reconciles those nibble pairs into three lane families
3. `FD:A8A5` decides which lane families are actually eligible by testing three `0x80`-spaced lane blocks
4. `B3E7/B3E8/B3E9` becomes the final enabled-lane mask
5. `FD:A93C` performs phase-1 clear/reset across the enabled lanes
6. `FD:A95F` performs phase-2 conditional clear/reset plus a service-2 refresh across the enabled lanes

That is much better than the old “mysterious `FD:A8A5` / `FD:A93C` families” description.

---

## 11. The `9F38[x]` producer question did **not** close cleanly this pass
A targeted ROM-wide direct-operand scan for `9F38` found only a very small number of apparent matches, and the promising-looking non-C1 hits sit in regions that are still data-heavy / table-like on this pass.

The result is:

- no clean bank-`C1` writer to `9F38[x]` was pinned this pass
- no obviously trustworthy direct writer in the quick non-`C1` scan was strong enough to label
- the pass-41 reading of `9F38[x]` as an **input aux-flag byte consumed by the service-7 record emitter** still stands
- but the **producer path remains unresolved**

So this pass deliberately does **not** fake a source label for `9F38[x]`.

That restraint is the correct move here.

---

## Revised structural picture after pass 42
The service-7 outer sink side now looks like:

1. service-7 wrappers choose/emit results into the canonical fixed record trio
2. each canonical fixed record carries a packed nibble pair in `93F3`
3. those nibble pairs are not arbitrary small IDs; they are lane IDs `0/1/2` plus `F = none`
4. `C1:B575..B6C9` reconciles the canonical trio into lane families and a final 3-bit lane enable mask
5. `FD:A93C` runs phase-1 clear/reset on enabled lanes
6. `FD:A95F` runs phase-2 occupied-lane clear/reset plus service-2 refresh
7. `9F38[x]` still feeds emitted aux flags, but its producer remains open

That is a materially tighter description of the downstream category side.

---

## Strengthened interpretations

### `7E:93F3 + 7*n`
> **packed pair of lane IDs for canonical record `n`**
>
> valid values observed by the reconciler:
>
> - `0`
> - `1`
> - `2`
> - `F` = none / disabled

### `7E:B3E7..B3E9`
> **final enabled-lane mask derived from the canonical trio’s lane-ID pairs plus lane-block eligibility**

### `FD:A8A5`
> **lane-block eligibility test for lane IDs `0/1/2`, using three `0x80`-spaced WRAM lane blocks**

### `FD:A93C`
> **phase-1 enabled-lane clear/reset dispatcher**

### `FD:A8CE`
> **clear one canonical fixed-record slot and reset the matching lane’s carried state**

### `FD:A95F`
> **phase-2 enabled-lane conditional refresh dispatcher**

### `FD:A8FE`
> **if the lane is occupied, clear the canonical fixed-record slot, reset lane state, and invoke local service 2**

### `C1:B961`
> **local service-2 wrapper**

---

## What remains unresolved after pass 42
1. the exact gameplay-facing meaning of lane IDs `0/1/2`
2. the exact human-facing roles of the lane-carried bytes:
   - `AFAB`
   - `99DD`
   - `9F22`
   - `B188`
   - `B03A`
3. the producer path for `9F38[x]`
4. the exact effect of the service-2 refresh on the just-cleared lane
5. whether the canonical trio / lane-reset logic belongs to one gameplay subsystem or a shared controller used by multiple higher-level systems

---

## Best next target
The cleanest next continuation point is now:

- trace service 2 (`C1:1BAA`) specifically in the contexts reached from `FD:A8FE`
- identify the consumer/producer roles of `B158 / B188 / AFAB / 99DD / 9F22 / B03A`
- keep the `9F38[x]` search open, but only with stronger proof than the quick direct-operand scan provided

That is the seam most likely to convert the current honest “lane/reset” wording into final gameplay-facing names without bluffing.
