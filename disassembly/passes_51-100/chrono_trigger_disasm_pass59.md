# Chrono Trigger Disassembly Pass 59

## Scope of this pass
This pass continued directly from pass 58's open seam:

1. pin the real dispatch site into the provisional `B8F3` selector-wrapper table candidate
2. determine whether `B8F3` is actually its own table or part of an already-live dispatcher path
3. convert the strongest selector-wrapper results into exact inline selector-control byte values
4. tighten the `AED3` question based on the corrected dispatch ownership

The important outcome is:

> `B8F3` is **not** a separate selector-wrapper table.
>
> It is the middle portion of the already-live table dispatched by:
>
> - `C1:AC14`
> - `C1:AC2E  JSR ($B8BB,X)`
>
> where `X = selector_byte * 2`.
>
> That means the pass-58 “table candidate at `B8F3`” should be retired.
> The real structure is a **single larger inline selector-control dispatch table** beginning at `C1:B8BB` and running at least through `C1:B95F`.

This is a real ownership proof, not just table contiguity.

---

## Method
1. Re-opened `C1:AC14..AC45` and decoded the exact selector dispatch path.
2. Compared the table base used there (`B8BB`) against the pass-58 pointer run beginning at `B8F3`.
3. Parsed the full contiguous pointer run from `B8BB` until the pointer pattern stops and real code begins.
4. Derived the exact selector-control byte values for the already-solved wrappers:
   - fixed single-entry wrappers
   - withheld-tail random reducer
   - visible-slot min selector
   - live-tail random reducer
5. Reframed the still-open `$0E -> AED3` question with the corrected dispatch ownership.

---

## 1. `C1:AC14` is the direct dispatch site, and it already reaches straight through `B8F3`
Relevant bytes:

```text
C1:AC14  JSR $AC46
C1:AC17  LDX $B1D2
C1:AC1A  INX
C1:AC1B  STX $B1D2
C1:AC1E  LDA.l $CC0000,X
C1:AC22  BPL $08
C1:AC24  LDA $AED8
C1:AC27  STA $AECC
C1:AC2A  BRA $13
C1:AC2C  ASL A
C1:AC2D  TAX
C1:AC2E  JSR ($B8BB,X)
```

### What this proves
This is the missing direct ownership proof from pass 58.

For any non-negative inline selector-control byte read from the CC stream:

- byte value is doubled via `ASL A`
- result becomes `X`
- dispatch happens through `JSR ($B8BB,X)`

So if the selector-control byte is `0x1C`, then:

- `X = 0x38`
- effective pointer address = `B8BB + 0x38 = B8F3`

That is exactly the start of the pass-58 “candidate table.”

So `B8F3` is not merely adjacent to the live dispatcher.
It is **directly inside the same indexed dispatch table already used by `AC14`**.

---

## 2. The real table is one continuous inline selector-control dispatch table: `B8BB..B95F`
Parsing the table from the actual dispatch base gives this contiguous run:

```text
00 -> A3F6
01 -> A3F7
02 -> A411
03 -> A42E
04 -> A43D
05 -> A452
06 -> A4AF
07 -> A4E0
08 -> A508
09 -> A541
0A -> A54B
0B -> A555
0C -> A55F
0D -> A569
0E -> A573
0F -> A5A3
10 -> A5D3
11 -> A603
12 -> A633
13 -> A663
14 -> A693
15 -> A6C3
16 -> A6ED
17 -> A709
18 -> A737
19 -> A765
1A -> A7A9
1B -> A7E5
1C -> A819
1D -> A855
1E -> A889
1F -> A8C5
20 -> A8F9
21 -> A935
22 -> A971
23 -> A9AD
24 -> A9E9
25 -> AA25
26 -> AA61
27 -> AAAB
28 -> AAB6
29 -> AAC1
2A -> AACC
2B -> AAD7
2C -> AAE2
2D -> AAED
2E -> AAF8
2F -> AB03
30 -> AB4E
31 -> AB59
32 -> AB64
33 -> AB6F
34 -> AB7A
35 -> AB85
36 -> AB90
37 -> AB9B
38 -> ABC9
39 -> 8876
3A -> 88C5
3B -> 8975
3C -> 89B9
3D -> 8A05
3E -> 8A51
3F -> 8A9D
40 -> 8A9E
41 -> 8A9F
42 -> 8B10
43 -> 8BB9
44 -> 8C08
45 -> 8461
46 -> AFB6
47 -> AFC1
48 -> AFCC
49 -> AFD7
4A -> AFE2
4B -> AFED
4C -> AFF8
4D -> B003
4E -> B00E
4F -> B019
50 -> B024
51 -> B02F
52 -> B03A
```

The next byte at `B961` is real code (`A9 02 ...`), so `B95F` is the last proved table byte in this pass.

### What this changes
Pass 58's local “selector-wrapper table candidate” should be collapsed into this larger confirmed table.

Best current reading:

> `C1:B8BB..C1:B95F` = **inline selector-control dispatch table used by `AC14`**

This is materially stronger than the old “group-3 table” wording because it now includes:

- the earlier selector-control families already known from passes 33–35
- the pass-58 selector-wrapper run (`AAAB..ABC9`)
- a later family of dispatch targets reaching back into `8876..8C08`
- a final late family landing in the `AFB6..B03A` region

---

## 3. The pass-58 wrapper family now has exact selector-control byte values
Because the dispatch site is now direct, the pass-58 family can be mapped to precise inline selector-control bytes.

### Fixed single-entry wrappers for entries `3..10`
```text
0x27 -> AAAB  AECC = 3 ; AECB = 1
0x28 -> AAB6  AECC = 4 ; AECB = 1
0x29 -> AAC1  AECC = 5 ; AECB = 1
0x2A -> AACC  AECC = 6 ; AECB = 1
0x2B -> AAD7  AECC = 7 ; AECB = 1
0x2C -> AAE2  AECC = 8 ; AECB = 1
0x2D -> AAED  AECC = 9 ; AECB = 1
0x2E -> AAF8  AECC = 10 ; AECB = 1
```

### Withheld-tail random candidate reducer
```text
0x2F -> AB03
```
This is the pass-57/58 helper that:

- scans canonical tail entries via `AF15.bit7`
- builds candidate slot indices in `AECC`
- randomly reduces multiple candidates to one exposed slot in `AECC[0]`
- forces `AECB = 1`

### Fixed single-entry wrappers for entries `0..6`
```text
0x30 -> AB4E  AECC = 0 ; AECB = 1
0x31 -> AB59  AECC = 1 ; AECB = 1
0x32 -> AB64  AECC = 2 ; AECB = 1
0x33 -> AB6F  AECC = 3 ; AECB = 1
0x34 -> AB7A  AECC = 4 ; AECB = 1
0x35 -> AB85  AECC = 5 ; AECB = 1
0x36 -> AB90  AECC = 6 ; AECB = 1
```

### Dynamic visible-slot selector
```text
0x37 -> AB9B
```
This is the pass-58 dynamic selector over visible entries `0/1/2`, choosing a single exposed result in `AECC` and setting `AECB = 1`.

### Live-tail random candidate reducer
```text
0x38 -> ABC9
```
This is the pass-58 live-tail sibling to `AB03`, using the live unified occupant map rather than withheld canonical tail entries.

---

## 4. The previous split between “`B8BB` table” and “`B8F3` candidate table” was artificial
Pass 58 was careful because it lacked the direct dispatch proof.
That caution was appropriate then.

But after reopening `AC14`, the split is no longer correct.

### The correct model now
- `AC14` consumes one inline selector-control byte
- non-negative values dispatch through **one table base only**: `B8BB`
- the pass-58 wrapper family is just the `0x27..0x38` portion of that same table

So the correct progression is:

- old narrow read: `B8BB` looked like a smaller selector/group table
- pass 58 intermediate read: `B8F3` looked like a second local table candidate
- pass 59 corrected read: both are one continuous **inline selector-control dispatch table**

That is a real cleanup of the control-flow model, not a wording tweak.

---

## 5. This also sharpens the `$0E -> AED3` question
Pass 58 left the open question as:

> which indirect wrapper translates a selected slot/entry into the occupant ID consumed by `AED3`?

Pass 59 does not fully solve that feeder.
But it narrows the search much better.

### What is now proved
The wrapper family that produces selection results in `AECC/AECB` is not orphaned and not indirectly floating.
It is explicitly entered via `AC14` selector-control bytes.

So the remaining question is no longer about table ownership.
It is specifically about **which selector-control opcodes later transition from slot-selection result space to occupant-ID reinsertion space**.

That means the most likely candidates are now:

- the later still-less-decoded selector-control entries beyond `0x38`
- especially the `0x46..0x52` family landing in `AFB6..B03A`
- and any paths that consume `AECC` / `AECB` after `AC14` returns and before/without direct slot-index materialization

### What this rules out
It is no longer useful to keep searching for a separate dispatcher into `B8F3`.
That problem is solved.

The remaining work is **semantic**, not structural:

- which selector-control byte values are the deferred-tail reinsertion modes
- and which one(s) feed `$0E` for `AED3`

---

## 6. Best current reading after pass 59
The strongest safe wording now is:

> `C1:B8BB..C1:B95F` is a single **inline selector-control dispatch table** used by `C1:AC14`.
>
> The pass-58 “late local selector-wrapper family” is the confirmed `0x27..0x38` subrange of that table.

And the `AB03 / ABC9` family can now be named more precisely in context:

- they are not standalone helper islands
- they are concrete selector-control opcodes inside the `AC14` selector engine

That is a much better control-flow position than pass 58 had.

---

## Suggested next seam
The best continuation after this pass is:

1. decode the still-open selector-control entries `0x39..0x52`
2. prioritize the late `0x46..0x52` family (`AFB6..B03A`) because it is the strongest current candidate bridge into deferred reinsertion semantics
3. re-check whether any of those late opcodes translate `AECC`-selected slot indices into occupant IDs before `AED3`

That is now the real remaining seam.
