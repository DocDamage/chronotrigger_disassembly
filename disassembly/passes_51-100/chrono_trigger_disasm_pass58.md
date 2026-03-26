# Chrono Trigger Disassembly Pass 58

## Scope of this pass
This pass continued directly from pass 57's open seam:

1. identify which wrapper family owns `C1:AB03..AB49`
2. identify what can actually be proved about the `$0E` feed into `C1:AED3..AEFB`
3. tighten the surrounding selector/materialization structure without inventing a gameplay noun the bytes do not yet prove

The important outcome is:

> `AB03` is no longer floating as an orphan helper.
>
> It sits inside a larger **late local selector-wrapper family**, alongside:
>
> - fixed single-entry selector wrappers
> - a min-of-three selector for visible slots `0/1/2`
> - a second random-reduction candidate builder for **live** tail slots
>
> At the same time, whole-ROM static call scanning found **no direct `JSR/JMP/JSL` references** to either `AB03` or `AED3`.
> So the strongest current ownership proof is:
>
> - table/family contiguity
> - shared scratch/result conventions (`AECC` / `AECB`)
> - and the fact that other already-solved handlers (`9E78`, `86BC`) can materialize tail entries **without** going through `AED3`
>
> That explains why the direct `$0E` feeder is still not statically pinned.

This is real progress, but it is not the same thing as proving the final gameplay-facing wrapper name.

---

## Method
1. Re-scan the ROM for **direct static callers** of:
   - `C1:AB03`
   - `C1:AED3`
2. Re-open the dense late-`C1` pointer region around `B8F0..B92C`
3. Decode the small wrapper family around:
   - `AAAB..AAF8`
   - `AB4E..AB90`
   - `AB9B..ABC8`
   - `ABC9..AC13`
4. Cross-check that family against the already solved tail materializer from pass 33:
   - `C1:9E78`
5. Separate what is now strong from what still needs a runtime/backtrace proof

---

## 1. There are **no direct static `JSR/JMP/JSL` callers** to `AB03` or `AED3` anywhere in the ROM
Whole-ROM byte scans were run for:

- `JSR $AB03`
- `JMP $AB03`
- `JSL $C1AB03`
- `JSR $AED3`
- `JMP $AED3`
- `JSL $C1AED3`

Result:

- **zero hits** for all six patterns

### What this proves
This matters because it rules out the easy interpretation that either helper is entered through a normal direct call edge.

So pass 57's remaining caller question changes shape:

- the missing ownership proof is **not** “find the obvious `JSR $AED3`”
- it is more likely:
  - dispatch through a local pointer table
  - fallthrough from a wrapper family
  - or an indirect path that does not leave a simple absolute-call signature

That is a useful negative proof, not just absence.

---

## 2. `C1:B8F3` is a strong **local selector-wrapper table candidate** (but the dispatch site is still not pinned)
A previously unlabelled pointer run begins cleanly at `C1:B8F3` and yields this highly coherent sequence:

```text
00 -> A819
01 -> A855
02 -> A889
03 -> A8C5
04 -> A8F9
05 -> A935
06 -> A971
07 -> A9AD
08 -> A9E9
09 -> AA25
0A -> AA61
0B -> AAAB
0C -> AAB6
0D -> AAC1
0E -> AACC
0F -> AAD7
10 -> AAE2
11 -> AAED
12 -> AAF8
13 -> AB03
14 -> AB4E
15 -> AB59
16 -> AB64
17 -> AB6F
18 -> AB7A
19 -> AB85
1A -> AB90
1B -> AB9B
1C -> ABC9
```

### Why this is strong
This is **not** random pointer noise.

From `0x13` onward the entries are visibly a coherent selector/materialization helper family:

- `AB03` = withheld-tail candidate builder with random reduction (pass 57)
- `AB4E..AB90` = fixed single-entry wrappers for literal selected entries `0..6`
- `AB9B` = dynamic min-of-three selector over slots `0/1/2`
- `ABC9` = live-tail candidate builder with random reduction

And `0x0B..0x12` are another fixed-wrapper run:

- `AAAB..AAF8` = fixed single-entry wrappers for literal selected entries `3..10`

### What is still not proved
The actual dispatch site into `B8F3` is **still not pinned** in this pass.
So `B8F3` should be carried as a **provisional local selector-wrapper table candidate**, not yet as a globally frozen command table.

But the ownership question from pass 57 is much cleaner now:

> `AB03` belongs to a real local selector-wrapper family, not to generic scratch-list infrastructure and not to the already confirmed `B8BB` group-3 table.

---

## 3. `AAAB..AAF8` and `AB4E..AB90` are two fixed single-entry selector-wrapper runs
The byte pattern is exact:

```text
A9 <imm>
8D CC AE
A9 01
8D CB AE
60
```

### `AAAB..AAF8`
This run sets:

- `AECC = 3`
- `AECC = 4`
- `AECC = 5`
- `AECC = 6`
- `AECC = 7`
- `AECC = 8`
- `AECC = 9`
- `AECC = 10`

and always:

- `AECB = 1`
- `RTS`

### `AB4E..AB90`
This second run sets:

- `AECC = 0`
- `AECC = 1`
- `AECC = 2`
- `AECC = 3`
- `AECC = 4`
- `AECC = 5`
- `AECC = 6`

and again always:

- `AECB = 1`
- `RTS`

### What this proves
This family is not just “misc helper bytes.”
It is a real selector-result family that writes the current selected-entry scratch in the exact same shape used elsewhere:

- selected entry -> `AECC[0]`
- selected-count -> `AECB = 1`

That is very strong structural ownership evidence for the `AB03` neighborhood.

---

## 4. `C1:AB9B..ABC8` is a dynamic **min-of-three selector** over visible entries `0/1/2`
Relevant bytes:

```text
C1:AB9B  7B AC 30 5E 84 02 9C CC AE
C1:ABA4  AC B0 5E C4 02 90 07 84 02 A9 01 8D CC AE
C1:ABB3  AC 30 5F C4 02 90 07 84 02 A9 02 8D CC AE
C1:ABBE  7B A9 01 8D CB AE 64 03 60
```

### Structural read
This routine:

1. seeds the current comparison value from `$5E30`
2. compares `$5EB0`
   - if lower/equal-enough for the branch condition, updates:
     - comparison value
     - `AECC = 1`
3. compares `$5F30`
   - if lower/equal-enough for the branch condition, updates:
     - comparison value
     - `AECC = 2`
4. finally sets:
   - `AECB = 1`

So the exact branch polarity still wants careful runtime confirmation, but the structural meaning is already strong:

> select exactly one of the visible entries `0`, `1`, or `2` according to a min-style comparison across the lane-local values at `5E30 / 5EB0 / 5F30`

This is a dynamic selector wrapper in the same family as the fixed single-entry wrappers.

---

## 5. `C1:ABC9..AC13` is the **live-tail counterpart** to pass 57's `AB03`
Relevant bytes:

```text
C1:ABCA  STZ $0B
C1:ABCC  TAX
C1:ABCD  LDA $B252
C1:ABD1  ADC #$03
C1:ABD3  STA $0A
C1:ABD5  LDY #$0003
...
C1:ABDC  LDA $AEFF,Y
C1:ABE0  CMP #$FF
C1:ABE3  TYA
C1:ABE4  STA $AECC,X
...
C1:ABEE  TXA
C1:ABEF  CMP #$02
C1:ABF6  JSR $AF22
C1:ABF9  TAX
C1:ABFA  LDA $AECC,X
C1:ABFD  STA $AECC
C1:AC00  LDA #$FF
C1:AC05  STA $AECC,X
C1:AC0E  LDA #$01
C1:AC10  STA $AECB
C1:AC13  RTS
```

### Strong structural read
This routine:

1. uses the current live-tail count in `B252`
2. derives an upper bound of `3 + B252`
3. scans unified live-map entries starting at slot index `3`
4. appends every non-`FF` slot index into `AECC`
5. if the collected count is at least `2`, uses `AF22` to choose one random entry
6. stores the chosen slot index into `AECC[0]`
7. forces `AECB = 1`

### Important correction to pass 57-style wording
This routine does **not** obviously clear the full remainder of `AECC[1..]`.
What it definitely does is:

- overwrite the chosen result into `AECC[0]`
- write `FF` once at the next slot
- force `AECB = 1`

So the safe wording is:

> randomly reduce the current live-tail slot candidate list to a single exposed selected slot in `AECC[0]`

That same correction should be carried back mentally to `AB03` as well:
because `AECB = 1`, the extra scratch bytes after slot `0` are no longer semantically live.

### Why this matters
Pass 57 proved the **withheld-tail** candidate builder.
Pass 58 now proves a structurally paired **live-tail** candidate builder in the same local family.

So the selector family now has both sides:

- `AB03` = deferred/withheld tail slots
- `ABC9` = currently live tail slots

That is a real new structural result.

---

## 6. This also explains why `AED3` still lacks an obvious static feeder: not all materialization paths use it
Two already-solved routines now matter more in light of this family.

### A. `C1:9E78` from pass 33
Pass 33 already proved that `9E78` scans tail slots and for each accepted entry directly does:

- `AF0D[x] -> AF02[x]`
- plus per-slot initialization/finalization

That is a **slot-indexed materialization path**.
It does not need `$0E` and does not need `AED3`.

### B. `C1:86BC` style direct current-slot copy
A smaller direct branch also exists around `86BC`:

- load current slot index from `AEC8`
- read `AF0D[current]`
- write `AF02[current]`

Again, that is a **slot-indexed direct copy path**, not an occupant-ID path.

### Consequence
`AED3` is therefore not “the materializer.”
It is:

> a more specific **occupant-ID keyed deferred-tail reinsertion helper**

That explains why the obvious static feeder is still missing.
Some wrapper families operate entirely in slot-index space and never need `AED3`.

So the current best wording is:

- `AB03` / `ABC9` = selector-family helpers producing slot indices in `AECC`
- `AED3` = occupant-ID reinsertion helper used by a narrower deferred-tail path

That is stronger than pass 57 even though the exact caller chain into `$0E` is still unresolved.

---

## 7. What is now safe to carry forward
### Strong
- `AB03` belongs to a real local selector-wrapper family
- `ABC9` is a sibling random-reduction candidate builder for live tail slots
- `AAAB..AAF8` and `AB4E..AB90` are fixed single-entry selector wrappers
- `AB9B` is a dynamic visible-slot selector over entries `0/1/2`
- not all tail materialization goes through `AED3`

### Still open
- the exact dispatch site into the provisional pointer table at `B8F3`
- the exact wrapper(s) that finally translate a selected slot/entry into the occupant ID stored in `$0E` before `AED3`
- the final gameplay-facing noun for the full selector family

---

## Best current reading after pass 58
Pass 57 asked which wrapper family owns `AB03`.
Pass 58 now gives the strongest safe answer:

> `AB03` is one entry in a late local selector-wrapper family that writes selection results into `AECC/AECB`, alongside fixed single-entry selectors, a visible-slot min selector, and a live-tail random candidate selector.

And the `$0E` question is narrower now too:

> the missing proof is no longer “who materializes tail entries?”
>
> It is specifically:
>
> **which indirect wrapper translates a selected slot/entry into the occupant ID consumed by `AED3`?**

That is a much better continuation seam than pass 57 had.

---

## Suggested next seam
The best next continuation point after this pass is:

1. find the real dispatch site that indexes into the provisional `B8F3` selector-wrapper table
2. trace which wrapper family translates `AECC`-style selected slot indices into `$0E` before deferred reinsertion
3. then revisit the readiness/tail-count consumers with the stronger selector-family model in hand
