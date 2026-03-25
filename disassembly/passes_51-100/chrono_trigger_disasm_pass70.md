# Chrono Trigger Disassembly — Pass 70

## Scope of this pass
This pass continues directly from the pass-69 seam.

Pass 69 promoted the selector-control slice into its correct master range and materially decoded:

- global `57..5F`

The next stated seam was:

- global `60..6C`
- then the still-open promoted band at `70..7D`

This pass closes the full `60..6C` band.

The real gain is that globals `60..6B` are not thirteen unrelated one-off bodies.
They are one shared **visible-entry FD-record selector family** built on three helpers:

- `C1:AD68`
- `C1:AE70`
- `C1:ADA1`

and global `6C` then breaks cleanly away as a separate tail-live-slot selector.

---

## 1. Shared helper `C1:AE70` scans one visible entry against an FD record offset/mask contract
Handler bytes:

```text
C1:AE70  7B 64 0B AD 1E AF A8 B9 FF AE C9 FF F0 52
C1:AE7E  C2 20 BF 0B A8 FD 85 0C 18 65 0A AA 7B E2 20
C1:AE8E  BD 00 00 2C 1F AF F0 3B A6 0C BD 1D 00 30 34
C1:AE9E  7B AD CB AE A8 AD 1E AF 99 CC AE EE CB AE
C1:AEAC  A6 0C BD 20 00 89 20 F0 0B B9 CC AE 09 40 99 CC AE EE 20 AF
C1:AEBE  BD 20 00 89 10 F0 0B B9 CC AE 09 80 99 CC AE EE 21 AF
C1:AECE  64 0D 60
```

### What it does
This helper takes its control inputs from scratch/state already seeded by the wrapper:

- `AF1E` = visible entry index being scanned (`0`, `1`, or `2`)
- `0A` = FD-record byte offset to test
- `AF1F` = bitmask that the tested byte must satisfy

Then it:

1. skips immediately if `AEFF[AF1E] == FF`
   - so empty visible slots are ignored
2. resolves the per-entry FD record root through the `FD:A80B` pointer table using the visible entry index
3. reads the byte at:
   - `record_base + offset_from_$0A`
4. requires:
   - `(record_byte & AF1F) != 0`
5. also requires:
   - `record_byte_at_+1D` to be nonnegative (`BMI` rejects)
6. on success it appends the visible entry index into `AECC[AECB]` and increments `AECB`
7. then it reads `record_byte_at_+20` and annotates the appended candidate byte:
   - if bit `0x20` is set, ORs candidate with `0x40` and increments `AF20`
   - if bit `0x10` is set, ORs candidate with `0x80` and increments `AF21`

### Strongest safe reading
`AE70` is best carried forward as:

> **scan one visible entry `0..2` for an FD-record offset/mask hit, append it as a candidate, and attach reducer marks from record byte `+20`**

That is the exact per-entry front-end used by globals `60..6B`.

---

## 2. Shared helper `C1:ADA1` reduces those visible candidates by `B23A` priority and optional redirect
Handler bytes:

```text
C1:ADA1  7B AD CB AE F0 79 C9 02 90 68 AD 21 AF F0 28
C1:ADB0  7B AA A8 B9 CC AE 29 0F DD 3A B2 F0 11 C8 98 CD CB AE 90 EF
C1:ADC4  7B A8 E8 8A C9 08 90 E7 80 45
C1:ADCE  B9 CC AE 10 E0 8D CC AE 80 24
C1:ADD8  7B AA A8 B9 CC AE 29 0F DD 3A B2 F0 11 C8 98 CD CB AE 90 EF
C1:ADEC  7B A8 E8 8A C9 08 90 E7 80 1D
C1:ADF6  B9 CC AE 8D CC AE
C1:ADFC  AD 20 AF F0 12 AD CC AE 89 40 F0 0B 20 E0 A4 80 13
C1:AE0D  7B 8D CB AE 80 0D
C1:AE13  A9 01 8D CB AE AD CC AE 29 0F 8D CC AE 60
```

### What it does
This helper consumes the candidate list built in `AECC/AECB`.

#### empty input
- if `AECB == 0`
- it simply returns unchanged

#### single candidate
- if `AECB == 1`
- it forces `AECB = 1`
- strips the high marker bits from `AECC[0]`
- returns the resulting low-nibble entry index

#### multi-candidate input
For `AECB >= 2`, it performs an ordered reduction using `B23A[0..7]`.

1. If any candidate was tagged with `0x80` (`AF21 != 0`), it first searches for the first `B23A` priority match whose stored candidate byte is negative / bit-7 marked.
2. If none is found, it falls back to the first ordinary `B23A` priority match regardless of those marks.
3. The chosen candidate is stored in `AECC[0]`.
4. Then, if any candidate carried the `0x40` redirect mark (`AF20 != 0`) **and** the chosen candidate itself has `0x40`, the helper does:
   - `JSR $A4E0`
   - then returns directly
5. Otherwise it forces:
   - `AECB = 1`
   - `AECC[0] &= 0x0F`
   - return

### Strongest safe reading
`ADA1` is best carried forward as:

> **reduce visible FD-record candidates by `B23A` priority, prefer `0x80`-marked candidates when present, and optionally redirect through `A4E0` when the chosen candidate carries `0x40`**

That is the actual collapse step shared by globals `60..6B`.

### Honest caution
The gameplay-facing noun behind:

- `B23A`
- the `0x40` redirect mark
- the `0x80` preferred mark

is still not fully proved.

But the mechanics are no longer fuzzy.

---

## 3. Shared wrapper `C1:AD68` is the nonzero-mask front-end for visible entries `0..2`
Handler bytes:

```text
C1:AD68  7B 8D CB AE 8D 20 AF 8D 21 AF A8 AA 8C C9 AE
C1:AD77  A9 FF 8D 1F AF
C1:AD7C  7B 8D 1E AF 8D CB AE AA 20 70 AE
C1:AD87  A9 01 8D 1E AF A2 02 00 20 70 AE
C1:AD92  A9 02 8D 1E AF A2 04 00 20 70 AE
C1:AD9D  20 A1 AD 60
```

### What it does
This helper:

1. clears:
   - `AECB`
   - `AF20`
   - `AF21`
2. forces:
   - `AF1F = FF`
3. runs `AE70` for visible entries `0`, `1`, and `2`
4. then runs `ADA1`

So `AD68` is simply the shared family wrapper for:

> **visible-entry FD-record offset tests where any nonzero byte at the chosen offset counts as a hit**

The exact offset comes from the caller through `$0A`.

---

## 4. Globals `60..64` are exact offset wrappers over `AD68`
These five bodies are tiny wrappers that set a literal FD-record offset into `$0A`, then call `AD68`.

### Global `60` (`C1:A541`) sets offset `0x1D`
Bytes:

```text
C1:A541  7B A9 1D AA 86 0A 20 68 AD 60
```

This selects visible candidates whose FD-record byte at `+1D` is nonzero, but because `AE70` also requires the same `+1D` byte to be nonnegative, the practical contract is:

> **select visible entries whose FD-record byte at `+1D` is positive, then reduce by the shared visible-candidate reducer**

### Global `61` (`C1:A54B`) sets offset `0x1E`
Bytes:

```text
C1:A54B  7B A9 1E AA 86 0A 20 68 AD 60
```

This means:

> **select visible entries whose FD-record byte at `+1E` is nonzero, subject to the shared nonnegative `+1D` gate, then reduce by the shared visible-candidate reducer**

### Global `62` (`C1:A555`) sets offset `0x1F`

```text
C1:A555  7B A9 1F AA 86 0A 20 68 AD 60
```

So global `62` is:

> **select visible entries whose FD-record byte at `+1F` is nonzero, subject to the shared nonnegative `+1D` gate, then reduce by the shared visible-candidate reducer**

### Global `63` (`C1:A55F`) sets offset `0x20`

```text
C1:A55F  7B A9 20 AA 86 0A 20 68 AD 60
```

So global `63` is:

> **select visible entries whose FD-record byte at `+20` is nonzero, subject to the shared nonnegative `+1D` gate, then reduce by the shared visible-candidate reducer**

### Global `64` (`C1:A569`) sets offset `0x21`

```text
C1:A569  7B A9 21 AA 86 0A 20 68 AD 60
```

So global `64` is:

> **select visible entries whose FD-record byte at `+21` is nonzero, subject to the shared nonnegative `+1D` gate, then reduce by the shared visible-candidate reducer**

### Why this is stronger than “just wrapper noise”
The family is now concrete:

- visible entries only (`0..2`)
- same FD-record root table
- same `+1D` nonnegative gate
- same `+20` mark extraction
- same `B23A`-ordered reduction
- same optional redirect through `A4E0`

So `60..64` are real selector bodies, not meaningless aliases.

---

## 5. Globals `65..6B` are the masked-bit variants of the same visible FD-record family
These seven bodies inline the same shared setup instead of calling `AD68`, but the logic is the same except they seed `AF1F` with a literal bitmask instead of `FF`.

That makes them exact **offset+mask selector variants** over the same `AE70 -> ADA1` pipeline.

### Global `65` (`C1:A573`)
- sets:
  - `0A = 0x1E`
  - `AF1F = 0x02`

So global `65` is:

> **select visible entries whose FD-record byte at `+1E` matches mask `0x02`, subject to the shared nonnegative `+1D` gate, then reduce by the shared visible-candidate reducer**

### Global `66` (`C1:A5A3`)
- sets:
  - `0A = 0x1E`
  - `AF1F = 0x80`

So global `66` is:

> **select visible entries whose FD-record byte at `+1E` matches mask `0x80`, subject to the shared nonnegative `+1D` gate, then reduce by the shared visible-candidate reducer**

### Global `67` (`C1:A5D3`)
- sets:
  - `0A = 0x1E`
  - `AF1F = 0x04`

So global `67` is:

> **select visible entries whose FD-record byte at `+1E` matches mask `0x04`, subject to the shared nonnegative `+1D` gate, then reduce by the shared visible-candidate reducer**

### Global `68` (`C1:A603`)
- sets:
  - `0A = 0x21`
  - `AF1F = 0x04`

So global `68` is:

> **select visible entries whose FD-record byte at `+21` matches mask `0x04`, subject to the shared nonnegative `+1D` gate, then reduce by the shared visible-candidate reducer**

### Global `69` (`C1:A633`)
- sets:
  - `0A = 0x21`
  - `AF1F = 0x40`

So global `69` is:

> **select visible entries whose FD-record byte at `+21` matches mask `0x40`, subject to the shared nonnegative `+1D` gate, then reduce by the shared visible-candidate reducer**

### Global `6A` (`C1:A663`)
- sets:
  - `0A = 0x20`
  - `AF1F = 0x10`

So global `6A` is:

> **select visible entries whose FD-record byte at `+20` matches mask `0x10`, subject to the shared nonnegative `+1D` gate, then reduce by the shared visible-candidate reducer**

### Global `6B` (`C1:A693`)
- sets:
  - `0A = 0x01`
  - `AF1F = 0x08`

So global `6B` is:

> **select visible entries whose FD-record byte at `+01` matches mask `0x08`, subject to the shared nonnegative `+1D` gate, then reduce by the shared visible-candidate reducer**

---

## 6. Global `6C` is a clean tail-live selector: all occupied non-current tail slots
Handler bytes:

```text
C1:A6C3  7B 64 0B AA
C1:A6C7  AD 52 B2 18 69 03 85 0A
C1:A6CF  A0 03 00
C1:A6D2  C4 0A F0 0C
C1:A6D6  B9 FF AE C9 FF F0 05
C1:A6DD  98 9D CC AE E8
C1:A6E2  C8 C0 0B 00 D0 EA
C1:A6E8  8A 8D CB AE 60
```

### What it does
1. starts with an empty selector list
2. computes the current live tail slot index as:
   - `B252 + 3`
3. scans live slots `3..10`
4. skips the one equal to that current tail slot index
5. appends every other occupied live tail slot (`AEFF[Y] != FF`) into `AECC`
6. stores the count in `AECB`

### Strongest safe reading
Global `6C` is:

> **select all occupied live tail slots except the current tail-local live slot**

This is a completely separate selector body from the visible-entry FD-record family above.

---

## 7. What pass 70 locks down
This pass materially closes the whole promoted `60..6C` seam.

### Closed as a family
- `60..64` = nonzero FD-offset visible selectors through the shared reducer
- `65..6B` = masked FD-offset visible selectors through the same shared reducer
- `6C` = occupied non-current tail-live-slot selector

### New structural helpers worth carrying forward
- `AD68` = visible nonzero-offset family wrapper
- `AE70` = per-visible-entry FD-offset/mask candidate scanner
- `ADA1` = visible candidate reducer by `B23A` order with optional `A4E0` redirect

---

## 8. Best next seam
With `60..6C` closed, the clean next target is now:

- global `70..7D`

That is the next unresolved promoted selector-control band in master form.
