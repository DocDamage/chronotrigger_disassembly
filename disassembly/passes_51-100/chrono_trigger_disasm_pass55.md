# Chrono Trigger Disassembly Pass 55

## Scope of this pass
This pass continued from pass 54's live seam:

- trace the **producer / owner side** of `AEFF`
- decide whether `AEFF` is merely an eligibility gate or a real slot-owner map
- tighten the roles of:
  - `AF0A`
  - `AEC5`
  - `B1BE`
- re-check downstream consumers that use `AEFF` values as indices
- decide whether pass 54's `AEFF == FF` gate can now be upgraded into a stronger gameplay-facing noun

This pass resolves the biggest remaining ambiguity from pass 54.

The main result is:

> `AEFF..AF09` is **not** best treated as a mere active-entry gate array.  
> It is a real **11-slot battle-slot occupant index map**, where each non-`FF` entry names the battler/participant currently assigned to that battle slot, and `FF` means the slot is unoccupied / inactive for slot-driven processing.

That is materially stronger than pass 54's still-cautious gating wording.

---

## Method
1. Re-read the direct producer/reset paths that store into `AEFF`:
   - `FD:B24D..B2A3`
   - `C1:FB06..FB2C`
   - `C1:B279..B2C0`
2. Re-check the inverse-map builder around `FD:B280..B2A3`.
3. Re-check downstream consumers that use `AEFF` values as **entity indices**, not booleans:
   - `C1:BE50..BF24`
   - `FD:B363...`
4. Compare these results against pass 54's normalization logic, which already proved:
   - `AEFF == FF` excludes a slot from readiness normalization
   - non-`FF` entries keep the slot inside the active subset

---

## 1. `FD:B24D..B2A3` is a canonical head-slot occupant-map initializer
The strongest direct producer path starts here:

```text
FD:B24D  TDC
FD:B24E  TAX
FD:B24F  LDA #$FF
FD:B251  STA $AEFF,X
FD:B254  STA $AF0A,X
FD:B257  INX
FD:B258  CPX #$000B
FD:B25B  BCC $B24F
```

This first loop clears **all 11 slots** of both arrays:

- `AEFF[0..10] = FF`
- `AF0A[0..10] = FF`

That already tells us two useful things:

1. `AEFF` and `AF0A` are paired arrays of the same slot space.
2. `FF` is the canonical empty / absent sentinel, not just a random compare value.

The next loop is the real producer:

```text
FD:B268  TAX = 0
FD:B26C  LDA $2980,X
FD:B26F  BMI $B27A
FD:B271  STA $AEFF,X
FD:B274  STA $AF0A,X
FD:B277  INC $AEC5
FD:B27A  INX
FD:B27B  CPX #$0003
FD:B27E  BCC $B26C
```

### What this proves
For the first three visible/head slots only:

- if the source entry at `2980[X]` is valid/non-negative,
- slot `X` receives occupant index `X`
- and that same value is mirrored into `AF0A[X]`
- while `AEC5` counts how many such head slots were admitted

This is not how a pure boolean gate array is initialized.
It is how an **occupant-index map** is initialized.

### Strongest safe reading
`AEFF[slot]` holds the battler / participant index currently assigned to that battle slot.
For the visible head at startup, the map is self-assigned:

- slot 0 -> battler 0
- slot 1 -> battler 1
- slot 2 -> battler 2

when those battlers are valid.

---

## 2. `AF0A` is not a random mirror; it is the remembered / baseline occupant map
The same initializer writes the identical occupant index to both arrays:

```text
STA $AEFF,X
STA $AF0A,X
```

That could still be dismissed as a redundant mirror if it happened only once.
But `C1:B279..B2C0` proves the split is real.

Key section:

```text
C1:B279  LDA $AF0A,Y
C1:B27C  CMP #$FF
C1:B27E  BNE $B283
C1:B280  JMP $B3B7
...
C1:B28B  LDA $AF0A,Y
C1:B28E  STA $AEFF,Y
```

### What this proves
This path:

- checks whether the slot has a remembered occupant in `AF0A[Y]`
- and if so, restores that remembered occupant into the live slot map `AEFF[Y]`

So `AF0A` is **not** just another gate byte.
It is the remembered / baseline occupant identity for the slot.

This is the strongest direct evidence in this pass that:

- `AEFF` = live slot occupant map
- `AF0A` = remembered/default slot occupant map

---

## 3. `C1:B279..B2C0` also proves `AEFF = FF` means “slot emptied”, not merely “temporarily skipped”
The same routine has a later branch that forcibly clears the slot:

```text
C1:B2B9  LDA #$00
C1:B2BB  STA $B03A,Y
C1:B2BE  LDA #$FF
C1:B2C0  STA $AEFF,Y
```

with accompanying battler-side clears:

```text
STA $5E4B,X
STA $5E4C,X
STA $5E4D,X
STA $5E4E,X
```

and a flag clear in `5E2F`.

### Strongest safe reading
This is not “leave slot occupant alone but mark it ineligible for one routine.”
This is a real **slot-emptying / occupant-removal** action.

That sharply upgrades pass 54's wording.
The `FF` sentinel is now best treated as:

> **no battler currently assigned to this battle slot**

which naturally explains why pass 54's readiness normalization skips it.

---

## 4. `C1:FB06..FB2C` is a second canonical head-map rebuild, not a one-off curiosity
The later setup path at `C1:FB06..FB2C` repeats the same structural pattern:

```text
C1:FB06  STZ $AEC5
C1:FB0A  TAX = 0
C1:FB0B  LDA #$FF
C1:FB0D  STA $AEFF,X
C1:FB10  STA $AF0A,X
...
C1:FB18  LDA $2980,X
C1:FB1B  BMI $FB26
C1:FB1D  STA $AEFF,X
C1:FB20  STA $AF0A,X
C1:FB23  INC $AEC5
```

with one extra guard:

```text
C1:FB13  LDA $A09B,X
C1:FB16  BNE $FB26
```

### What this adds
This confirms the `AEFF/AF0A/AEC5` trio is not local weirdness from a single init path.
It is the canonical way this subsystem rebuilds the visible head-slot occupant map.

The extra `A09B[X]` guard simply means:
- this rebuild has one more exclusion condition than the base path,
- but it is still the same occupant-map construction model.

That is strong enough to freeze the noun at the head level.

---

## 5. `FD:B280..B2A3` proves `B1BE` is the inverse map from battler index -> visible head slot
Immediately after the head-map build, the routine clears and rebuilds `B1BE`:

```text
FD:B280  STZ $24
FD:B282  TDC
FD:B283  TAX
FD:B284  LDA #$FF
FD:B286  STA $B1BE,X
FD:B289  INX
FD:B28A  CPX #$0007
FD:B28D  BCC $B286
```

then:

```text
FD:B28F  TDC
FD:B290  TAX
FD:B291  LDA $AEFF,X
FD:B294  CMP #$FF
FD:B296  BEQ $B29D
FD:B298  TAY
FD:B299  TXA
FD:B29A  STA $B1BE,Y
FD:B29D  INX
FD:B29E  CPX #$0003
FD:B2A1  BCC $B291
```

### What this proves
For the three head slots only:

- read occupant = `AEFF[slot]`
- if occupant is valid,
- store `slot` into `B1BE[occupant]`

So `B1BE` is the inverse map:

```text
B1BE[battler] = visible head slot
```

for battlers currently represented in the head.

This is exactly the structure you'd expect if:
- `AEFF` maps **slot -> battler**
- `B1BE` maps **battler -> visible slot**

It is **not** the structure you'd build for a generic gate byte.

---

## 6. `C1:BE50..BF24` uses `B1BE` exactly like an inverse visible-slot map
This consumer family was already partially understood in passes 50–51.
Pass 55 tightens the front half.

Entry checks:

```text
C1:BE4B  LDA $B2EB
C1:BE4E  CMP #$FF
C1:BE50  BNE $BE55
C1:BE52  JMP $BF45
```

and similarly:

```text
C1:BEC8  LDA $B2EC
C1:BECB  CMP #$FF
C1:BECD  BNE $BED2
C1:BECF  JMP $BF45
```

If the selected battler index is absent (`FF`), the helper bails out.
If present:

```text
C1:BE55  TAX              ; X = battler index
C1:BE56  LDA $B1BE,X
C1:BE59  TAX              ; X = visible head slot
```

then the helper continues on the visible slot's readiness/gauge state:

- `B158`
- `AFAB`
- `99DD`
- `9F22`

### What this proves
`B1BE` is being used here exactly as:

> **translate battler identity into visible head slot identity**

That directly reinforces the pass-55 model:

- `AEFF/B2EB/B2EC` carry battler IDs
- `B1BE` converts battler ID -> visible head slot

---

## 7. `FD:B363...` proves `AEFF[Y]` is consumed as a battler index into battler-state tables
Another crucial consumer starts like this:

```text
FD:B36B  LDA $AEFF,Y
FD:B36E  CMP #$FF
FD:B370  BEQ $B3EA
```

So if the slot is empty, the helper exits.
If not empty, it uses the value to reach battler-side state:

```text
FD:B37D  LDA $5E79,X
...
FD:B385  LDA $5E7B,X
FD:B38A  LDA $5E7A,X
...
FD:B399  LDA $5E4A,X
...
FD:B3AA  LDA $5E57,X
...
FD:B3B3  LDA $5E32,X
```

### What this proves
The value loaded from `AEFF[Y]` is not being used as a boolean or a small local mode.
It is used to reach battler-structured WRAM in the `5E**` family.

That is exactly what we needed to freeze the noun.

### Strongest safe reading
`AEFF[slot]` holds a battler/participant identity that can be used to index into the battler-state tables.

---

## 8. What this changes about pass 54's normalization model
Pass 54 correctly proved the arithmetic role:

- `AEFF == FF` slots are excluded from readiness normalization
- non-`FF` slots remain inside the active subset

Pass 55 now tells us **why**.

It is not because `AEFF` is merely a “gate byte.”
It is because:

- `AEFF` names the battler currently occupying each readiness slot
- `FF` means no battler occupies that slot
- therefore there is no active countdown/readiness entry to normalize for that slot

So pass 54's normalization model should now be carried forward as:

> normalize the readiness work values only for battle slots that currently have a real battler occupant.

That is stronger and cleaner.

---

## 9. Tightened roles now safe to carry forward

### `AEFF..AF09`
Best current noun:

> **battle-slot occupant index map**

Meaning:
- index = battle slot
- value = battler/participant assigned to that slot
- `FF` = slot unoccupied

### `AF0A..AF14`
Best current noun:

> **remembered/default battle-slot occupant index map**

Meaning:
- used to restore live slot ownership in `C1:B279..B28E`
- shares the same `FF` empty sentinel

### `AEC5`
Best current noun:

> **visible head occupant count**

Meaning:
- incremented exactly when visible head slots `0..2` are populated during the canonical head-map rebuilds

### `B1BE`
Best current noun:

> **battler-to-visible-head-slot inverse map**

Meaning:
- rebuilt from `AEFF[0..2]`
- used by `BE50/BED0` to target visible slot state from battler IDs

---

## 10. What is still open after this pass
This pass freezes the owner/gate noun for `AEFF`, but some edges still want more work:

1. the exact producer path for **tail-slot** occupant assignments beyond the visible head rebuilds
2. the exact high-level gameplay meaning of:
   - `B03A`
   - `B188`
   inside the ready-transition helpers
3. the exact downstream consumer that distinguishes:
   - `AFAB == 0`
   - `AFAB == 1`
   - `AFAB > 1`
   using the newly frozen occupant-map model
4. whether the tail partition should be finalized specifically as enemy-side slots, or kept at the safer “runtime battle-slot” wording for now

---

## Bottom line
Pass 55 closes the biggest semantic gap left open by pass 54.

`AEFF..AF09` is no longer best described as a mere active-entry gate array.
It is a real **battle-slot occupant index map**:

- each slot carries a battler/participant index when occupied
- `FF` means the slot is empty
- `AF0A` is the remembered/default version of that mapping
- `AEC5` counts occupied visible head slots
- `B1BE` is the inverse map from battler index back to visible head slot

That gives pass 54's normalization logic the right noun at last.
