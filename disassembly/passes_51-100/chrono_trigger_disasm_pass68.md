# Chrono Trigger Disassembly — Pass 68

## Scope of this pass
This pass continues directly from the pass-67 seam and finishes the remaining table-ownership cleanup for the old `B85F` and `B88D` local slices under the pass-61 master-table model.

Covered here:

- global `30..3F` (the rest of old local group-1 `07..16`)
- global `40..56` (the full old local group-2 `00..16`)

This pass is partly promotion / ownership cleanup, but there are also two real semantic upgrades inside the old group-1 tail:

- `32 -> C1:9967` is now pinned as a tiny inline-parameter capture body into `AEE4`
- `39 / 3F -> C1:9981` is now pinned as a real gate on whether any canonical tail slot is eligible for live materialization

That means the remaining promoted master rows are no longer “unknown because they used to be local.”
They now have correct global-master identities.

---

## 1. Exact master-table map for `30..56`
Direct pointer-table bytes at `C1:B86D..C1:B8B7`:

```text
30 -> C1:9962
31 -> C1:9966
32 -> C1:9967
33 -> C1:9978
34 -> C1:9979
35 -> C1:997D
36 -> C1:997E
37 -> C1:997F
38 -> C1:9980
39 -> C1:9981
3A -> C1:99B4
3B -> C1:99B4
3C -> C1:99B4
3D -> C1:99B4
3E -> C1:99B4
3F -> C1:9981

40 -> C1:99B8
41 -> C1:99BE
42 -> C1:9A39
43 -> C1:9B46
44 -> C1:9B47
45 -> C1:9B48
46 -> C1:9B8C
47 -> C1:9B8D
48 -> C1:9C6E
49 -> C1:9C6F
4A -> C1:9CB3
4B -> C1:9D1B
4C -> C1:9D72
4D -> C1:9DCE
4E -> C1:9E62
4F -> C1:9E63
50 -> C1:9E78
51 -> C1:9F5A
52 -> C1:9FD2
53 -> C1:A14E
54 -> C1:A188
55 -> C1:A20B
56 -> C1:A396
```

What this proves:

- `30..3F` really are just the back half of the old `B85F` slice, now promoted to proper master globals
- `40..56` really are the full old `B88D` slice, likewise promoted to proper master globals

So after this pass the master coverage sheet no longer needs the fake gap between the already-solved early globals and the already-solved old local bodies.

---

## 2. Global `30..3F` is mostly explicit alias/stub control, with two real bodies

The rest of the old group-1 slice stays exactly as stub-heavy as pass 32 first suggested.
The difference is that the results now live under the correct global-master numbering.

### Exact shared exits

```text
30 -> C1:9962 = STZ $AF24 ; RTS
31 -> C1:9966 = RTS
33 -> C1:9978 = RTS
34 -> C1:9979 = STZ $AF24 ; RTS
35 -> C1:997D = RTS
36 -> C1:997E = RTS
37 -> C1:997F = RTS
38 -> C1:9980 = RTS
3A -> C1:99B4 = STZ $AF24 ; RTS
3B -> C1:99B4 = STZ $AF24 ; RTS
3C -> C1:99B4 = STZ $AF24 ; RTS
3D -> C1:99B4 = STZ $AF24 ; RTS
3E -> C1:99B4 = STZ $AF24 ; RTS
```

So the safest carry-forward here is not fake semantic inflation.
These are mostly:

- pure no-op aliases
- or explicit short-circuit-clear success exits

That matters because it keeps the table density honest.

---

## 3. Global opcode `32` (`C1:9967`) captures the current inline byte into `AEE4`
Handler bytes:

```text
C1:9967  AE D2 B1 AD 52 B2 0A 0A A8 BF 01 00 CC 8D E4 AE 60
```

### What it does
1. loads the current CC stream pointer from:
   - `B1D2`
2. loads the current slot index from:
   - `B252`
3. multiplies that slot index by four only to build `Y`, but the actual read is:
   - `LDA $CC0001,X`
4. stores that byte into:
   - `AEE4`
5. returns

### Strongest safe interpretation
This body does **not** perform local selection logic.
It does **not** update `B1D2`.
It simply captures the current opcode's first inline byte into the working state byte already reused elsewhere as a raw follow-up parameter.

So global opcode `32` is best carried forward as:

> **capture current inline parameter byte into `AEE4`**

That is a much stronger and more useful label than the old generic `op09_body` wording.

---

## 4. Global opcodes `39` and `3F` (`C1:9981`) gate on whether a canonical tail slot can be materialized into the live map
Handler bytes:

```text
C1:9981  7B AA 86 10 86 0C A6 10 BD 0D AF C9 FF F0 10
C1:9991  BD 02 AF C9 FF D0 09 BD 15 AF 89 80 D0 02 E6 0C
C1:99A1  E6 10 A5 10 C9 08 90 DF A5 0C C9 00 D0 05 A9 02
C1:99B1  8D 24 AF 60 9C 24 AF 60
```

### What it counts
Across `X = 0..7`, the body accepts a slot only when all of these are true:

- `AF0D[x] != FF`
- `AF02[x] == FF`
- `AF15[x] & 0x80 == 0`

Passes 56 and 57 already hardened those fields as:

- `AF0D` = canonical tail occupant submap
- `AF02` = live tail occupant submap
- `AF15.bit7` = deferred / withheld-from-live tail materialization flag

So the accepted slots here are exactly:

> canonical tail entries that exist, are not currently live, and are not deferred-withheld

### Success / failure behavior
- if the accepted count is nonzero:
  - `STZ AF24 ; RTS`
- if the accepted count is zero:
  - `AF24 = 2 ; RTS`

### Strongest safe interpretation
Global `39` and `3F` are exact aliases of the same body.
The best current reading is:

> **gate success on whether at least one canonical tail slot is immediately materializable into the live tail map**

This is materially stronger than the old generic `op10_op16_shared_body` label.

---

## 5. Global `40..56` is the old group-2 slice promoted into proper master ownership
This pass does not pretend that every old group-2 body suddenly became fully solved.
But under the pass-61 master-table proof, the correct thing now is to promote the already-earned local results into the master coverage sheet.

### Strong promoted globals

#### `40 -> C1:99B8`
Old local group-2 `00`.
Still the same exact body:

> **set `B3B8 = 2` and return**

#### `41 -> C1:99BE`
Old local group-2 `01`.
Passes 34 and 35 already pinned this strongly:

> **seed a one-entry list from `5E15[current]`, capture `AEE4/AEE5`, run the unique `FD:AB01` helper, then finalize through `AC89/ACCE`**

#### `42 -> C1:9A39 -> 9A3D`
Old local group-2 `02`.
Still the same strong seeded validation/commit path:

> **seed a one-entry list from `B16E[current]`, optionally resolve inline selectors, validate through `C1DD`, then commit through `AD09/AD35/FDAAD2/AC89/ACCE`**

#### `4D -> C1:9DCE`
Old local group-2 `0D`.
Still the same strong state-control body:

> **bitmask-driven per-slot/global state control**

with operand-driven effects on:

- `B320[current]`
- flag bits under `5E4A...`
- global clears of `96F1/96F2/96F3`
- optional `JSL $CD0033`

#### `4F -> C1:9E63`
Old local group-2 `0F`.
Still the same minimal wrapper:

> **if operand 1 is nonzero, call `JSL $CD0033`, then set `B3B8 = 2` and return**

#### `50 -> C1:9E78`
Old local group-2 `10`.
Passes 33, 56, and 57 now combine cleanly here.
This is best carried forward as:

> **materialize eligible tail slots from the canonical tail map, then finalize selection/masks**

It scans using the already-hardened tail gates around `AF0D / AF02 / AF15`, appends accepted entries to `AECC`, applies the known side effects, builds masks, optionally reaches `CD0033`, and returns with `B3B8 = 1`.

#### `51 -> C1:9F5A`
Old local group-2 `11`.
Still the same strong writer family body:

> **group-base-selected write of four odd/even operand pairs**

#### `52 -> C1:9FD2`
Old local group-2 `12`.
Still the same strong writer-plus-validation body:

> **group-base-selected write of five odd/even operand pairs plus selector/validation/commit follow-up**

#### `53 -> C1:A14E`
Old local group-2 `13`.
Still the same strong arithmetic body:

> **saturating signed-delta update to `B158[current]`**

#### `56 -> C1:A396`
Old local group-2 `16`.
Still the same strong wrapper:

> **thin wrapper around fused long helper `FD:A990`**

### Promoted-but-still-provisional globals
These bodies were already real in the old local analysis, but they were not yet solved tightly enough for flavored gameplay-facing names:

- `44 -> C1:9B47`  shared variable-control entry A
- `45 -> C1:9B48`  shared variable-control entry B
- `46 -> C1:9B8C`
- `47 -> C1:9B8D`
- `48 -> C1:9C6E`
- `49 -> C1:9C6F`
- `4A -> C1:9CB3`
- `4B -> C1:9D1B`
- `4C -> C1:9D72`
- `54 -> C1:A188`
- `55 -> C1:A20B`

The useful change in this pass is not pretending they are newly solved.
It is making sure they now live under the correct global-master opcode identities instead of stale local-only names.

---

## 6. Alias cleanup that should now be treated as settled
The following promoted globals are exact table aliases or one-instruction exits and should stop being described as if they were meaningful unknown commands:

### pure `RTS`
- `31`
- `33`
- `35`
- `36`
- `37`
- `38`
- `43`
- `4E`

### `STZ AF24 ; RTS`
- `30`
- `34`
- `3A`
- `3B`
- `3C`
- `3D`
- `3E`

### exact shared-body aliases
- `39` and `3F` share `C1:9981`

That is now strong enough to carry forward without hedging.

---

## 7. Strongest working master-opcode readings after this pass
Newly clarified / promoted global labels worth treating as live:

- `30` = clear short-circuit flag and return
- `31` = `RTS` no-op alias
- `32` = capture current inline byte into `AEE4`
- `33` = `RTS` no-op alias
- `34` = clear short-circuit flag and return
- `35..38` = `RTS` no-op aliases
- `39` = gate on whether a canonical tail slot is immediately materializable into the live map
- `3A..3E` = clear short-circuit flag and return
- `3F` = same body as `39`
- `40..56` = promoted master ownership of the old group-2 slice, with strong/global names now carried forward where already solved

---

## 8. What is now the next clean seam
With this pass, the whole old `B85F` and `B88D` local territory is finally promoted into the master table.

So the next clean seam is:

- global `57..5F` first
- then continue through the early `B8BB` slice with special attention on whether the first few promoted globals can be named more strongly than their old local wording

Targeted cleanup items for that next pass:

1. promote the first `B8BB`-slice globals into master ownership instead of leaving them only under old local labels
2. decide whether the provisional `44..4C` shared-body cluster can be tightened from caller/state evidence
3. keep `50` tied explicitly to the pass-56/57 canonical-vs-live tail map wording so it does not drift back into generic “eligible slot” phrasing
