# Chrono Trigger Disassembly — Pass 63

## Scope of this pass
This pass continued directly from pass 62's live seam in the early master-opcode band:

1. crack the heavier early global opcodes `01` and `02`
2. inspect the immediately adjacent bodies at `03` and `04` because they sit in the same unresolved cluster
3. determine which of these are true boolean replay gates versus selection-list transforms
4. correct any stale opcode-table carry-forward errors introduced before the master-table model was fully unified

The highest-value result of this pass is that the early band now splits much more cleanly:

> `01`, `02`, and `03` are not generic opaque effects.
>
> They are **selector-driven list builders / filters** layered over the already-solved
> `AC14` selection engine and the `AECC/AECB` selection scratch.
>
> By contrast, `04` is a direct **invertible live-tail presence gate**.
>
> So the early master-opcode band is no longer just “mystery prelude before the gate family.”
> It now clearly contains:
>
> - unconditional replay (`00`)
> - selector/list transforms (`01`, `02`, `03`)
> - direct gate queries (`04`, `05`, `06`, `07`, `20`, `21`)

This also exposes one real correction:

> the toolkit's old carry-forward line that treated global opcode `04` like the old
> group-1 local `0x04` body at `B815` is stale under the pass-61 master-table model.
>
> The actual master-table entry for global opcode `04` is `C1:8FDA`.

---

## Method
1. Re-opened the contiguous master-table entries proved by the `B80D` model:
   - `01 -> 8EAB`
   - `02 -> 8F11`
   - `03 -> 8F87`
   - `04 -> 8FDA`
2. Decoded each body byte-for-byte from ROM rather than inheriting older slice-era labels.
3. Cross-checked helper ownership against already-solved work:
   - `AC14` selector-control engine
   - selector-control bytes `0x01` and `0x16`
   - `AECC/AECB` selected-list scratch
   - `AEFF` occupant map
   - live-tail map `AF02`
   - lane-block family around `5E4A + slot*0x80`
4. Kept the `8C3E` / `AF24` contract from passes 61-62 in view while separating:
   - list-transform bodies
   - hard success/failure gates

---

## 1. Global opcode `01` is a selector-driven filter over existing `AC14` results, not a simple boolean gate
Handler bytes:

```text
C1:8EAB  20 14 AC
C1:8EAE  AD CB AE D0 03 4C 10 8F
C1:8EB6  7B AA 8E C9 AE 86 0A
C1:8EBD  7B AE C9 AE BD CC AE 0A AA
C1:8EC6  C2 20 BF 0B A8 FD AA
C1:8ECD  BD 1D 00 30 1D
C1:8ED2  BD 03 00 85 08
C1:8ED7  BD 05 00 4A C5 08 90 10
C1:8EDF  7B E2 20 AE C9 AE BD CC AE 09 80 9D CC AE
C1:8EED  E6 0A
C1:8EEF  7B E2 20 EE C9 AE AD C9 AE CD CB AE 90 C0
C1:8EFD  A5 0A 8D CB AE
C1:8F02  20 21 AE
C1:8F05  AD 24 AF D0 06
C1:8F0A  20 FD AE
C1:8F0D  20 3E 8C
C1:8F10  60
```

### What it does
1. calls `JSR $AC14`
   - so operand `+1` is an inline selector-control byte
   - results come back in `AECC/AECB`
2. if `AECB == 0`, it returns immediately with no forced `AF24 = 1`
3. otherwise it iterates the current selected entries in `AECC`
4. for each selected byte:
   - uses that byte to index the 16-bit offset table at `FD:A80B`
   - treats the resulting offset as the base of a structured record
   - requires record byte `+1D` to be non-negative
   - then compares:
     - record byte `+3`
     - against `(record byte +5) >> 1`
   - accepts the entry only when the halved `+5` byte is **greater than or equal to** the `+3` byte
5. on acceptance it:
   - increments the selected byte in-place in `AECC`
   - increments local accepted-count `$0A`
6. after the loop:
   - writes accepted-count back to `AECB`
   - runs the existing finalize helper at `AE21`
   - if `AF24 == 0`, runs `AEFD` and then `8C3E`

### What this proves
This is **not** a pure boolean gate in the pass-62 sense.

It is a **selection-list transform/filter** layered on top of the `AC14` selector engine:
- input list -> `AECC/AECB`
- per-entry structured-record test
- accepted entries rewritten in-place
- accepted-count pushed back to `AECB`
- optional continuation through `AEFD` and `8C3E`

### Important caution
The record test is mechanically strong, but the gameplay noun is not yet final.

The strongest safe wording is:

> global opcode `01` filters `AC14`-produced selected entries by a structured-record threshold test rooted through `FD:A80B`, then finalizes and optionally continues replay.

It is **suggestive** that the `FD:A80B`-selected base plus offsets `+3` / `+5` line up with the already-solved lane-block family rooted at `5E2D`, but that last naming jump should stay open until more caller proof exists.

### Behavior contrast with the pass-62 gate family
Unlike `05/06/07/20/21`, this body does **not** force failure whenever selection is empty.
And if `AE21` raises `AF24`, this handler simply returns rather than forcibly overwriting the result with `AF24 = 1`.

That makes `01` read more like a **stateful filter/continuation helper** than a clean yes/no gate.

---

## 2. Global opcode `02` chooses head-vs-nonhead selected entries, then filters them by a lane-flag bitmask
Handler bytes:

```text
C1:8F11  7B AA 86 04 86 06
C1:8F17  AE D2 B1
C1:8F1A  BF 01 00 CC 85 08
C1:8F20  BF 03 00 CC 85 02
C1:8F26  BF 02 00 CC AA 86 00
C1:8F2C  20 46 AC
C1:8F2F  A5 08 1A C9 01 F0 02 A9 16
C1:8F38  20 2C AC
C1:8F3B  A6 04
C1:8F3D  BD CC AE
C1:8F40  C2 20 18 EB 4A 65 00 AA
C1:8F47  7B E2 20 BD 4A 5E 25 02 C5 02 D0 0C
C1:8F53  E6 06
C1:8F55  A6 04 BD CC AE 09 80 9D CC AE
C1:8F5D  E6 04
C1:8F5F  A5 04 CD CB AE 90 D2
C1:8F67  A5 06 F0 13
C1:8F6A  8D CB AE
C1:8F6D  20 21 AE
C1:8F70  AD 24 AF D0 08
C1:8F75  20 FD AE
C1:8F78  20 3E 8C
C1:8F7B  80 05
C1:8F7D  A9 01 8D 24 AF
C1:8F81  60
```

### Operand shape
This handler consumes three meaningful immediate bytes:

- `CC:[B1D2 + 1] -> $08`
- `CC:[B1D2 + 2] -> $00`
- `CC:[B1D2 + 3] -> $02`

### Step 1: operand 1 selects which partition gets copied into `AECC`
After `AC46` clears the scratch lists, the handler uses `AC2C` to dispatch one of two **fixed selector-control bytes**:

- if operand 1 is `0` -> selector-control byte `0x01`
- otherwise       -> selector-control byte `0x16`

Those selector-control entries are already structurally visible from the master selector table:

- local selector-control `0x01 -> A3F7`
- local selector-control `0x16 -> A6ED`

And their bodies are straightforward:
- `A3F7` copies occupied visible/head entries from `AEFF[0..2]` into `AECC`
- `A6ED` copies occupied non-head entries from `AEFF[3..10]` into `AECC`

So global opcode `02` first chooses:

> **visible/head partition**
>
> vs
>
> **non-head partition**

and materializes that chosen partition into `AECC/AECB`.

### Step 2: filter the chosen entries by a lane-block byte/mask test
For each selected entry, the handler computes:

```text
X = selected_entry * 0x80 + operand2
```

and then reads:

```text
LDA $5E4A,X
AND operand3
CMP operand3
```

So an entry is accepted only when:

> **all bits from operand3 are set in the byte at**
> `5E4A + selected_entry*0x80 + operand2`

On acceptance it:
- increments the accepted-count
- increments the selected byte in-place in `AECC`

### Step 3: finalize or fail
After the loop:
- zero accepted entries -> forced failure (`AF24 = 1`)
- otherwise:
  - `AECB = accepted_count`
  - `JSR $AE21`
  - if `AF24 == 0`: `JSR $AEFD` then `JSR $8C3E`
  - else: forced failure (`AF24 = 1`)

### Strongest safe interpretation
Global opcode `02` is best carried forward as:

> **partitioned selected-entry filter by lane-block flag mask**
>
> with operand 1 choosing visible/head vs non-head partition, and operands 2-3 selecting the byte-offset and required bitmask inside the `5E4A + slot*0x80` lane block family.

This is materially stronger than “selector/filter body.”

---

## 3. Global opcode `03` is the arbitrary-selector sibling of `02`, filtering selected slots by `AEFF[selected] == immediate`
Handler bytes:

```text
C1:8F87  20 14 AC
C1:8F8A  AD CB AE F0 45
C1:8F8F  AE D2 B1 E8 8E D2 B1
C1:8F96  BF 00 00 CC 85 08
C1:8F9C  7B AA A8 86 06
C1:8FA1  BD CC AE A8
C1:8FA5  B9 FF AE C5 08 D0 0A
C1:8FAC  E6 06
C1:8FAE  BD CC AE 09 80 9D CC AE
C1:8FB6  E8 8A CD CB AE D0 E4
C1:8FBD  A5 06 F0 13
C1:8FC1  8D CB AE
C1:8FC4  20 21 AE
C1:8FC7  AD 24 AF D0 08
C1:8FCC  20 FD AE
C1:8FCF  20 3E 8C
C1:8FD2  80 05
C1:8FD4  A9 01 8D 24 AF
C1:8FD8  60
```

### What it does
1. calls `AC14`
   - so operand `+1` is again an arbitrary inline selector-control byte
   - the selected result list returns in `AECC/AECB`
2. if that selected list is empty, it forces failure (`AF24 = 1`)
3. advances to the next operand byte and loads it into `$08`
4. iterates the selected entries:
   - `Y = AECC[x]`
   - compare `AEFF[Y]` against the immediate operand
   - on match:
     - increment accepted-count
     - increment `AECC[x]` in-place
5. if no entries matched -> forced failure (`AF24 = 1`)
6. otherwise:
   - `AECB = accepted_count`
   - `AE21`
   - if `AF24 == 0`, run `AEFD` and then `8C3E`
   - else forced failure (`AF24 = 1`)

### What this proves
This is the same broad family as `02`, but with:
- **selector source** = arbitrary `AC14` selector-control byte
- **filter predicate** = occupant-index equality in `AEFF[selected]`

The strongest safe wording is:

> global opcode `03` filters an `AC14`-generated selected list by
> `AEFF[selected_entry] == immediate`, then finalizes and continues replay only on success.

This is a real structural sibling of opcode `02`, not a separate mystery subsystem.

---

## 4. Global opcode `04` is an invertible presence/absence gate over the live tail occupant map
Handler bytes:

```text
C1:8FDA  AE D2 B1
C1:8FDD  E8 E8 8E D2 B1
C1:8FE2  BF 00 00 CC 85 08
C1:8FE8  BF 01 00 CC 85 0A
C1:8FEE  7B AA
C1:8FF0  BD 02 AF C5 08 F0 0D
C1:8FF7  E8 8A CD C6 AE D0 F2
C1:8FFE  A5 0A D0 06 80 09
C1:9004  A5 0A D0 05
C1:9008  20 3E 8C
C1:900B  80 05
C1:900D  A9 01 8D 24 AF
C1:9012  60
```

### What it does
This handler scans the live tail occupant map `AF02[x]` from `x = 0` up to the canonical tail count `AEC6`.

The first meaningful operand byte is compared against `AF02[x]`.
A second byte acts as an invert flag.

### Success / failure contract
Let operand 1 = target occupant byte.
Let operand 2 = mode byte.

The handler succeeds when:

- target **is present** in `AF02[]` and mode byte == `0`
- target **is absent**  in `AF02[]` and mode byte != `0`

Otherwise it sets `AF24 = 1`.

So opcode `04` is best read as:

> **gate tail replay by live-tail occupant presence/absence**
>
> where operand 2 selects normal vs inverted sense.

### Important correction
This is the real master-table meaning of global opcode `04`.

So the older carry-forward line that mapped global `04` to the old group-1 local `0x04` body at `B815` should be retired.
That was an artifact of the pre-pass-61 table model.

---

## 5. What changed structurally after this pass
### A. The early master-opcode band now has a real internal split
The strongest current split is:

#### Replay / gate wrappers
- `00` unconditional replay
- `04` presence/absence gate on live tail occupant map
- `05` live unwithheld tail-count max gate
- `06` 24-bit triplet threshold gate
- `07` current-`B320` comparator gate
- `20` current-`AEB3` nonzero gate
- `21` current-`AF15` zero gate

#### Selector/list-transform bodies
- `01` arbitrary-selector filtered list transform through `FD:A80B`-rooted records
- `02` head-vs-nonhead partition filter through `5E4A + slot*0x80 + offset`
- `03` arbitrary-selector filter through `AEFF[selected] == immediate`

That is a much cleaner architectural picture than the pass-62 seam alone.

### B. `02` and `03` are hard yes/no success bodies; `01` is looser
`02` and `03` both:
- force `AF24 = 1` when no matches survive
- force `AF24 = 1` when `AE21` leaves a nonzero result

`01` does not do that.
So `01` should be kept separate from the tighter gate family even though it still feeds `AE21`, `AEFD`, and `8C3E`.

### C. Visible/head vs non-head partitioning is now explicitly present inside the early global band
The use of selector-control bytes:
- `0x01 -> A3F7` (visible/head occupied entries)
- `0x16 -> A6ED` (non-head occupied entries)

means the master early opcode band is directly aware of the already-solved slot partitioning structure rather than only querying undifferentiated global state.

---

## 6. Label corrections and carry-forward guidance
### Strong enough to promote now
- `01` as a selector-driven filtered-list transform over `FD:A80B`-rooted records
- `02` as a head/non-head partitioned lane-flag mask filter
- `03` as an arbitrary-selector occupant-equality filter
- `04` as the invertible live-tail occupant presence gate

### Important correction to keep
Do **not** keep the stale global-opcode line that says:

- global `04 -> B815`

Under the pass-61 master-table proof, the real master entry is:

- global `04 -> 8FDA`

### Still intentionally open
Do **not** over-freeze:
- why accepted entries in `01/02/03` are incremented in-place before finalization
- the exact gameplay noun behind `AE21`
- the final gameplay noun for the structured-record test in `01`

The byte-level control flow is now strong enough to label structurally, but the final human-facing subsystem noun still wants more caller proof.

---

## Suggested next seam
The cleanest continuation after this pass is:

1. reopen `09`, `0A`, `0B`, `0F`, and `12`
   - these remain pack-observed from pass 61
   - they now sit beside a much more legible early band
2. revisit the exact `AE21` contract
   - especially why `01/02/03` increment accepted entries in-place before finalization
3. decide whether the `01` record test can now be safely tied to the already-solved lane-stat family rooted at `5E2D`

That should keep momentum in the same seam rather than fragmenting into unrelated banks.
