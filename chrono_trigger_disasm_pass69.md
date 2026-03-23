# Chrono Trigger Disassembly — Pass 69

## Scope of this pass
This pass continues directly from the pass-68 seam.

Pass 68 finished global `30..56` and pointed at:

- global `57..5F`
- then the early `B8BB` slice immediately after that

This pass does two concrete things:

1. promotes the old selector-control slice at `C1:B8BB..C1:B95F` into its correct **master global** range:
   - global `57..A9`
2. materially decodes the first real promoted band:
   - global `57..5F`

It also carries forward the strongest already-solved selector-control results into their proper master identities, instead of leaving them stranded as “local selector bytes” forever.

---

## 1. The selector-control table is now promoted into the master coverage sheet as global `57..A9`
Pass 61 already proved the table geometry:

- `C1:B80D + (0x57 * 2) = C1:B8BB`

Pass 59 already proved the exact local selector-control table rooted at `B8BB`.
So the correct master mapping is now:

> **global opcode = 0x57 + selector-control local byte**

That means the old local selector-control table:

- local `00..52`

is really:

- global `57..A9`

This pass updates the toolkit worksheets to reflect that directly instead of pretending the master table still stops at `56`.

### Immediate practical consequence
The master opcode coverage files now include:

- the exact dispatch address for every promoted global `57..A9`
- strong global labels where semantics were already earned
- explicit “ownership promoted, semantics pending” rows for the still-open bodies

That is a real toolkit fix, not cosmetic cleanup.

---

## 2. Exact promoted master ownership for the first selector-control band
The first promoted globals land like this:

```text
57 -> C1:A3F6
58 -> C1:A3F7
59 -> C1:A411
5A -> C1:A42E
5B -> C1:A43D
5C -> C1:A452
5D -> C1:A4AF
5E -> C1:A4E0
5F -> C1:A508
```

And some important already-solved later promotions now become:

```text
6D -> C1:A6ED
6E -> C1:A709
6F -> C1:A737

7E..85 -> C1:AAAB..C1:AAF8
86      -> C1:AB03
87..8D -> C1:AB4E..C1:AB90
8E      -> C1:AB9B
8F      -> C1:ABC9

A0      -> C1:AFD7
```

So the selector-control layer is no longer just a side worksheet.
It is now visibly part of the master `B80D` space.

---

## 3. Global `57` is an exact RTS alias
Handler bytes:

```text
C1:A3F6  60
```

That is just:

- `RTS`

So the right promoted master reading is simply:

> **global `57` = exact RTS no-op alias**

No fake semantics needed.

---

## 4. Global `58` selects all occupied visible-head live slots `0..2`
Handler bytes:

```text
C1:A3F7  7B AA A8
C1:A3FA  B9 FF AE C9 FF F0 05
C1:A401  98 9D CC AE E8
C1:A406  C8 C0 03 00 D0 EE
C1:A40D  8A 8D CB AE 60
```

### What it does
This is a simple scan:

- start `X = 0`
- start `Y = 0`
- for `Y = 0..2`
  - if `AEFF[Y] != FF`
    - write `Y` into `AECC[X]`
    - increment `X`
- after the scan:
  - `AECB = X`
  - return

Pass 56 already hardened `AEFF` as the unified live occupant map.
So this body is selecting:

> occupied visible-head live slots

### Strongest safe reading
Global `58` is:

> **select occupied visible-head live slots `0..2` into `AECC`, count in `AECB`**

That is a strong structural selector body, not just a helper.

---

## 5. Global `59` extends global `58` to all occupied live slots `0..10`
Handler bytes:

```text
C1:A411  20 F7 A3
C1:A414  A0 03 00
C1:A417  B9 FF AE C9 FF F0 05
C1:A41E  98 9D CC AE E8
C1:A423  C8 C0 0B 00 D0 EE
C1:A42A  8A 8D CB AE 60
```

### What it does
1. first calls global `58`, so visible occupied entries `0..2` are already loaded
2. then resumes scanning at `Y = 3`
3. appends every occupied `AEFF[Y]` through `Y = 10`
4. stores the final count into `AECB`

So global `59` is just the full live-map counterpart:

> **select all occupied live slots `0..10` into `AECC`, count in `AECB`**

This gives the master table a clean “visible occupied subset” vs “all occupied live slots” pair at `58/59`.

---

## 6. Global `5A` is the current tail-local live slot selector
Handler bytes:

```text
C1:A42E  AD 52 B2
C1:A431  18 69 03
C1:A434  8D CC AE
C1:A437  A9 01
C1:A439  8D CB AE
C1:A43C  60
```

### What it does
- load current tail-local index from `B252`
- add `3`
- store the result in `AECC[0]`
- set `AECB = 1`
- return

This is the exact same head/tail index convention already proved elsewhere:

- visible head = `0..2`
- tail-local `0..7` corresponds to live slots `3..10`

So global `5A` is:

> **select the current tail-local live slot index (`B252 + 3`)**

---

## 7. Global `5B` selects the low nibble of the current quad-record byte
Handler bytes:

```text
C1:A43D  7B
C1:A43E  AD 52 B2
C1:A441  0A 0A
C1:A443  AA
C1:A444  BD 9E B1
C1:A447  29 0F
C1:A449  8D CC AE
C1:A44C  A9 01
C1:A44E  8D CB AE
C1:A451  60
```

### What it does
- use `B252 * 4` as an index into the current-slot quad-record base at `B19E`
- read:
  - `B19E + 4*B252`
- mask to the low nibble
- store that nibble into `AECC[0]`
- force `AECB = 1`

### Strongest safe reading
Global `5B` is:

> **select the low nibble of the current slot quad-record byte `B19E + 4*B252`**

I am not forcing a more flavored gameplay noun yet.
The structural selector contract is already good enough.

---

## 8. Global `5C` is a random visible-head live-slot selector with an unresolved pre-refresh gate
Handler bytes:

```text
C1:A452  9C CB AE
C1:A455  AD 24 00 D0 54
C1:A45A  A2 00 00 A0 00 00 20 79 B2
C1:A462  A2 80 00 A0 01 00 20 79 B2
C1:A46A  A2 00 01 A0 02 00 20 79 B2
C1:A472  AD FF AE 10 0C
C1:A477  AD 00 AF 10 07
C1:A47C  AD 01 AF 10 02
C1:A481  80 28
C1:A483  7B AA A9 63 20 22 AF
C1:A489  C9 21 B0 04 A9 00 80 0A
C1:A491  C9 42 B0 04 A9 01 80 02
C1:A499  A9 02 A8
C1:A49C  B9 FF AE 30 B5
C1:A49F  98 8D CC AE
C1:A4A2  A9 01
C1:A4A4  8D CB AE
C1:A4A7  60
```

### What it does
The important parts are clear even though one DP gate is still unresolved.

1. clear `AECB`
2. if DP scratch `$24 != 0`, bail out immediately with zero-count result
3. otherwise call `B279` three times for visible entries `0`, `1`, and `2`
4. if none of `AEFF[0..2]` are occupied, return with zero-count result
5. otherwise generate a random bucket over `0/1/2`
6. if the chosen visible slot is empty, retry
7. on success:
   - `AECC[0] = chosen_visible_slot`
   - `AECB = 1`

### Strongest safe reading
What I am comfortable freezing now is:

> **randomly choose one occupied visible-head live slot, after an optional `B279` refresh/clear pre-pass gated by DP scratch `$24`**

The exact higher-level noun of the `$24` gate is still open, so this should stay **provisional structural**.

But the body is definitely no longer a mystery blob.

---

## 9. Globals `5D` and `5E` are the promoted relation-query target selectors for modes `00` and `01`
These were already structurally solved earlier in the old local selector-control model.
This pass promotes them into their correct master identities.

### `5D -> C1:A4AF`
This is the pass-30 target-selection wrapper that seeds relation mode `00` and then consumes the returned selected slot from the relation-query service.

Best promoted master reading:

> **global `5D` = select target through relation-query mode `00`**

### `5E -> C1:A4E0`
Sibling wrapper for relation mode `01`.

Best promoted master reading:

> **global `5E` = select target through relation-query mode `01`**

---

## 10. Global `5F` selects one visible entry `0..2` by minimum current HP
Handler bytes:

```text
C1:A508  7B
C1:A509  AC 30 5E
C1:A50C  C9 00 D0 03 A0 FF 7F
C1:A513  84 02
C1:A515  9C CC AE
C1:A518  AC B0 5E F0 0B C4 02 B0 07
C1:A521  84 02 A9 01 8D CC AE
C1:A528  AC 30 5F F0 0B C4 02 B0 07
C1:A531  84 02 A9 02 8D CC AE
C1:A538  7B
C1:A539  A9 01
C1:A53B  8D CB AE
C1:A53E  64 03
C1:A540  60
```

### What it does
It compares the visible-head lane values at:

- `5E30`
- `5EB0`
- `5F30`

Earlier UI/panel passes already hardened those lane fields as current HP.
The body keeps the smallest seen value in scratch and writes the winning visible entry index into `AECC[0]`.

Then it forces:

- `AECB = 1`

### Strongest safe reading
Global `5F` is:

> **select one visible entry `0..2` by minimum current HP**

This is a real semantic upgrade beyond the old “some selector in the A508 region” read.

---

## 11. Important promoted globals already solved elsewhere
This pass also folds earlier selector results into the master table so coverage is honest.

### `6D -> C1:A6ED`
Already used as the non-head occupied-entry selector in pass 63.

Promoted master reading:

> **select occupied non-head live slots `3..10` into `AECC`, count in `AECB`**

### `6E -> C1:A709`
Promoted target-select wrapper for relation mode `02`.

### `6F -> C1:A737`
Promoted target-select wrapper for relation mode `03`.

### `7E..85`
Promoted fixed single-entry selector wrappers for literal entries `3..10`.

### `86`
Promoted master identity of the pass-57 withheld-tail random reducer:

> **build withheld-tail candidate list and randomly reduce to one**

### `87..8D`
Promoted fixed single-entry selector wrappers for literal entries `0..6`.

### `8E`
Promoted master identity of the pass-58 visible min selector at `AB9B`.

### `8F`
Promoted master identity of the pass-58 live-tail random reducer at `ABC9`.

### `A0`
Promoted master identity of the pass-60 late selector-pack executor at `AFD7`.

This matters because those bodies were already earned.
Leaving them out of master coverage was just stale ownership.

---

## 12. Toolkit fix: master opcode worksheet generation now matches the proved table span
One real tooling bug was sitting underneath the coverage files:

- `scripts/ct_build_opcode_coverage.py` still generated the master worksheet only through `0x3F`

That was wrong after passes 61, 67, and 68.

This pass updates the generator so the master coverage worksheet now spans:

- `00..A9`

which matches the currently proved master table extent from:

- `C1:B80D..C1:B95F`

That means future workspace refreshes will stop silently truncating the promoted master rows.

---

## What pass 69 proves

### It **does** prove
- global `57..A9` is now promoted into the master coverage sheet with exact dispatch addresses
- global `57` is an exact RTS alias
- global `58` selects occupied visible-head live slots
- global `59` selects all occupied live slots
- global `5A` selects the current tail-local live slot
- global `5B` selects the current quad-record low nibble
- global `5C` is a random visible-head live-slot selector with an unresolved pre-refresh gate
- globals `5D/5E` are the master forms of relation target-select modes `00/01`
- global `5F` selects one visible entry `0..2` by minimum current HP
- the toolkit coverage generator was stale and is now corrected to the proved master span

### It **does not** prove yet
- the final top-level noun for the DP `$24` gate feeding `5C`
- the exact flavored semantics of the parameterized selector family at:
  - `60..6C`
- the exact higher-level noun for many promoted late selector-control entries in:
  - `90..A9`

---

## Best next seam
The clean next move is now:

1. decode the parameterized selector family at **global `60..6C`**
   - especially the `A541..A6C3` band
2. then tighten the promoted still-open selector globals in:
   - `70..7D`
3. then revisit the late promoted range:
   - `90..A9`

The important difference after this pass is that the selector layer is no longer floating beside the master table.
It now sits inside it where it belongs.
