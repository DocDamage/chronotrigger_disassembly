# Chrono Trigger Disassembly — Pass 71

## Scope of this pass
This pass continues directly from the pass-70 seam.

Pass 70 closed global `60..6C` and showed that `60..6B` are one shared **visible-entry FD-record selector family** built on:

- `C1:AD68`
- `C1:AE70`
- `C1:ADA1`

The explicit next seam was:

- global `70..7D`

This pass closes that full promoted selector band.

The main result is simple:

> global `70..7D` are not random leftovers.
> They split into:
>
> - two **minimum-FD-word selectors** over occupied nonhead live slots (`70`, `7D`)
> - and a **nonhead counterpart** to the pass-70 visible FD-byte selector family (`71..7C`)

That is a real structural promotion, not a cosmetic table-fill.

---

## 1. Global `70` selects one occupied nonhead live slot by minimum nonzero FD record word `+3`
Handler bytes:

```text
C1:A765  A0 FF FF 84 02 7B A9 03 85 0E A5 0E AA BD FF AE
C1:A775  C9 FF F0 1D A5 0E 0A AA C2 20 BF 0B A8 FD AA BC
C1:A785  03 00 F0 0D C4 02 B0 09 84 02 E2 20 A5 0E 8D CC
C1:A795  AE E2 20 7B E6 0E A5 0E C9 0B 90 CE A9 01 8D CB
C1:A7A5  AE 64 03 60
```

### What it does
This body scans live slots `3..10`.

For each slot:

1. it skips the slot if `AEFF[slot] == FF`
2. it resolves the FD record root through `FD:A80B + slot*2`
3. it reads the 16-bit word at `record + 3`
4. it ignores zero values
5. it keeps the smallest nonzero value seen so far in direct-page `$02`
6. when a new minimum is found, it stores the corresponding live slot into `AECC[0]`

At the end it forces:

- `AECB = 1`

and returns.

### Strongest safe reading
Global `70` is:

> **select one occupied nonhead live slot `3..10` by minimum nonzero FD record word `+3`**

### Honest note
This body does **not** expose an explicit empty/no-hit failure path.
If every scanned slot is empty or yields `record_word(+3) == 0`, it still forces `AECB = 1`.
So the selection contract is strong, but the no-candidate edge case still wants runtime confirmation.

---

## 2. Globals `71..76` are the nonhead counterpart of pass 70's visible FD-byte selector family
These bodies reuse the same underlying helpers already hardened in pass 70:

- `AE70`
- `ADA1`

But instead of scanning visible entries `0..2`, they scan nonhead live slots `3..10`.

The shared setup is:

- `AF1E = 3` to start the scan at live slot `3`
- `0E = 6` so the `FD:A80B` pointer table is indexed as `slot * 2`
- `0A` = FD record byte offset to test
- `AF1F` = mask byte to apply
- after each iteration, the code advances:
  - `AF1E += 1`
  - `0E += 2`
- then the candidate list is collapsed through `ADA1`

That makes this whole band the **nonhead / tail-side version** of the visible family from globals `60..6B`.

---

## 3. Globals `71` and `72` use FD record byte `+1D`
### Global `71` (`C1:A7A9`)
Handler bytes:

```text
C1:A7A9  9C CB AE 9C 20 AF 9C 21 AF 7B A9 06 AA 86 0E A9
C1:A7B9  1D 85 0A A9 FF 8D 1F AF A9 03 8D 1E AF AD 1E AF
C1:A7C9  CD 8B B1 F0 03 20 70 AE A6 0E E8 E8 86 0E EE 1E
C1:A7D9  AF AD 1E AF C9 0B 90 E5 20 A1 AD 60
```

This is the nonhead equivalent of global `60`, except it skips the slot indexed by `B18B` before calling `AE70`.

So global `71` is:

> **select occupied nonhead live slots whose FD record byte `+1D` is positive, excluding the primary-seed slot `B18B`, then reduce through `ADA1`**

### Global `72` (`C1:A7E5`)
Handler bytes:

```text
C1:A7E5  9C CB AE 9C 20 AF 9C 21 AF 7B A9 06 AA 86 0E A9
C1:A7F5  1D 85 0A A9 FF 8D 1F AF A9 03 8D 1E AF 20 70 AE
C1:A805  A6 0E E8 E8 86 0E EE 1E AF AD 1E AF C9 0B 90 ED
C1:A815  20 A1 AD 60
```

This is the same selector family without the `B18B` exclusion.

So global `72` is:

> **select occupied nonhead live slots whose FD record byte `+1D` is positive, then reduce through `ADA1`**

---

## 4. Globals `73` and `74` use FD record byte `+1E`
### Global `73` (`C1:A819`)
Handler bytes:

```text
C1:A819  9C CB AE 9C 20 AF 9C 21 AF 7B A9 06 AA 86 0E A9
C1:A829  1E 85 0A A9 FF 8D 1F AF A9 03 8D 1E AF AD 1E AF
C1:A839  CD 8B B1 F0 03 20 70 AE A6 0E E8 E8 86 0E EE 1E
C1:A849  AF AD 1E AF C9 0B 90 E5 20 A1 AD 60
```

So global `73` is:

> **select occupied nonhead live slots whose FD record byte `+1E` is nonzero, excluding the primary-seed slot `B18B`, then reduce through `ADA1`**

As in the visible family, this still inherits the shared nonnegative `record[+1D]` gate inside `AE70`.

### Global `74` (`C1:A855`)
Handler bytes:

```text
C1:A855  9C CB AE 9C 20 AF 9C 21 AF 7B A9 06 AA 86 0E A9
C1:A865  1E 85 0A A9 FF 8D 1F AF A9 03 8D 1E AF 20 70 AE
C1:A875  A6 0E E8 E8 86 0E EE 1E AF AD 1E AF C9 0B 90 ED
C1:A885  20 A1 AD 60
```

So global `74` is:

> **select occupied nonhead live slots whose FD record byte `+1E` is nonzero, then reduce through `ADA1`**

---

## 5. Globals `75` and `76` use FD record byte `+1F`
### Global `75` (`C1:A889`)
Handler bytes:

```text
C1:A889  9C CB AE 9C 20 AF 9C 21 AF 7B A9 06 AA 86 0E A9
C1:A899  1F 85 0A A9 FF 8D 1F AF A9 03 8D 1E AF AD 1E AF
C1:A8A9  CD 8B B1 F0 03 20 70 AE A6 0E E8 E8 86 0E EE 1E
C1:A8B9  AF AD 1E AF C9 0B 90 E5 20 A1 AD 60
```

So global `75` is:

> **select occupied nonhead live slots whose FD record byte `+1F` is nonzero, excluding the primary-seed slot `B18B`, then reduce through `ADA1`**

### Global `76` (`C1:A8C5`)
Handler bytes:

```text
C1:A8C5  9C CB AE 9C 20 AF 9C 21 AF 7B A9 06 AA 86 0E A9
C1:A8D5  1F 85 0A A9 FF 8D 1F AF A9 03 8D 1E AF 20 70 AE
C1:A8E5  A6 0E E8 E8 85 0E EE 1E AF AD 1E AF C9 0B 90 ED
C1:A8F5  20 A1 AD 60
```

Structurally this is clearly meant to be the no-exclusion sibling of global `75`.
But unlike the matching family bodies, its loop update stores back to `$0E` with:

- `STA $0E`

instead of the expected:

- `STX $0E`

That is a real byte-level anomaly in the ROM, not a transcription mistake.

### Strongest safe reading
Global `76` is best frozen as:

> **intended nonhead selector sibling for FD record byte `+1F` without the `B18B` exclusion, collapsing through `ADA1`; loop-update byte at `C1:A8E9` is anomalous and still wants runtime confirmation**

So this body is usable structurally, but not frozen as hard as the rest of the family.

---

## 6. Globals `77..7C` are masked nonhead variants that exclude `B18B`
These six bodies all share the same skeleton:

- scan nonhead live slots `3..10`
- skip slot `B18B`
- call `AE70`
- reduce through `ADA1`

The only thing that changes is:

- `0A` = record-byte offset
- `AF1F` = mask

### Global `77` (`C1:A8F9`)
- `0A = 0x1E`
- `AF1F = 0x02`

So global `77` is:

> **select occupied nonhead live slots excluding `B18B` whose FD record byte `+1E` matches mask `0x02`, then reduce through `ADA1`**

### Global `78` (`C1:A935`)
- `0A = 0x1E`
- `AF1F = 0x80`

So global `78` is:

> **select occupied nonhead live slots excluding `B18B` whose FD record byte `+1E` matches mask `0x80`, then reduce through `ADA1`**

### Global `79` (`C1:A971`)
- `0A = 0x1E`
- `AF1F = 0x04`

So global `79` is:

> **select occupied nonhead live slots excluding `B18B` whose FD record byte `+1E` matches mask `0x04`, then reduce through `ADA1`**

### Global `7A` (`C1:A9AD`)
- `0A = 0x21`
- `AF1F = 0x40`

So global `7A` is:

> **select occupied nonhead live slots excluding `B18B` whose FD record byte `+21` matches mask `0x40`, then reduce through `ADA1`**

### Global `7B` (`C1:A9E9`)
- `0A = 0x1D`
- `AF1F = 0x02`

So global `7B` is:

> **select occupied nonhead live slots excluding `B18B` whose FD record byte `+1D` matches mask `0x02`, then reduce through `ADA1`**

### Global `7C` (`C1:AA25`)
- `0A = 0x19`
- `AF1F = 0x01`

So global `7C` is:

> **select occupied nonhead live slots excluding `B18B` whose FD record byte `+19` matches mask `0x01`, then reduce through `ADA1`**

---

## 7. Global `7D` is the `70` min-word selector with the `B18B` exclusion added
Handler bytes:

```text
C1:AA61  A0 FF FF 84 02 7B A9 03 85 0E A5 0E AA BD FF AE
C1:AA71  C9 FF F0 23 8A CD 8B B1 F0 1D A5 0E 0A AA C2 20
C1:AA81  BF 0B A8 FD AA BC 03 00 F0 0D C4 02 B0 09 84 02
C1:AA91  E2 20 A5 0E 8D CC AE E2 20 7B E6 0E A5 0E C9 0B
C1:AAA1  90 C8 A9 01 8D CB AE 64 03 60
```

This is the same minimum-word selector as global `70`, but it skips the slot whose index matches `B18B` before evaluating the candidate.

So global `7D` is:

> **select one occupied nonhead live slot by minimum nonzero FD record word `+3`, excluding the primary-seed slot `B18B`**

Like global `70`, it still lacks an explicit empty/no-hit failure path.

---

## 8. Structural conclusion for `70..7D`
This band now resolves into a clean internal shape:

- `70`, `7D`
  - minimum-word selectors over occupied nonhead live slots
- `71..76`
  - unmasked nonhead FD-byte selectors using the `AE70 -> ADA1` pipeline
- `77..7C`
  - masked nonhead FD-byte selectors using the same pipeline

So pass 71 closes the promoted selector-control master band:

- global `70..7D`

with one explicit caution left attached to opcode `76`.

---

## 9. Toolkit update required by this pass
The toolkit should now carry strong promoted ownership for:

- master globals `70..7D`
- selector-control locals `19..26`

with opcode `76` / selector `1F` marked **provisional structural** because of the anomalous `STA $0E` loop-update byte.

---

## Suggested next seam
- revisit the late promoted band at global `90..A9`
- keep opcode `76` on the runtime-confirmation shortlist because of the anomalous `C1:A8E9` byte
