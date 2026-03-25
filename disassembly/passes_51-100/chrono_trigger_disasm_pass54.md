# Chrono Trigger Disassembly Pass 54

## Scope of this pass
This pass continued directly from pass 53's live seam:

- decode the exact normalization block at `FD:B8F5..B93A`
- decide whether the pre-export step is:
  - simple copy/setup,
  - saturation/clamp logic,
  - or a true subtractive normalization across the unified 11-slot readiness family
- tighten the role of the `AEFF` sentinel gating inside that block
- decide what the normalization implies about zero values in `AFAB..AFB5`

This pass resolves the remaining ambiguity from pass 53.

The main result is:

> `FD:B8F7..B93A` is a real **minimum-positive subtractive normalization** over the unified 11-slot readiness work array.  
> It finds the smallest eligible positive work value, subtracts `(min - 1)` from every other eligible positive entry, leaves zero entries untouched, and only then exports the visible head.

That is materially stronger than the old provisional “normalize before export” wording.

---

## Method
1. Re-read the exact bytes at `FD:B8F5..B94F` from the ROM.
2. Realign the entry boundary correctly:
   - `FD:B8F5` is the tail-loop jump-back site
   - the actual normalization body begins at `FD:B8F7`
3. Decode both loops:
   - the candidate-selection loop at `B8FC..B918`
   - the subtract/apply loop at `B923..B939`
4. Compare the end of the routine against pass 53's head export copy at `B93B..B94F`.
5. Re-check what the logic does to:
   - zero values
   - `AEFF == FF` slots
   - head vs tail partition values

---

## 1. Entry correction: `B8F5` is not the body start
Pass 53 carried the unresolved seam as:

- `FD:B8F5..FD:B93A`

That was directionally right, but the exact body start is now clear.

At `FD:B8F0..B8F5` the tail seeder ends with:

```text
A5 02
CD C6 AE
B0 03
4C 67 B8
```

That is just:
- compare local tail index against `AEC6`
- if not done, jump back to `B867`

So the real normalization body begins immediately after that jump site:

```text
FD:B8F7
```

That matters because it means the normalization is a self-contained post-seed phase, not part of the tail-seed loop body.

---

## 2. `FD:B8F7..B918` is a minimum-positive candidate scan
The routine starts with:

```text
7B          TDC
AA          TAX
A8          TAY
86 00       STX $00
AD AB AF    LDA $AFAB
```

So it seeds:
- `X = 0`
- `Y = 0`
- `$00 = 0`
- `A = AFAB[0]`

Then the scan loop is:

```text
B8FF: E8             INX
B900: DD AB AF       CMP $AFAB,X
B903: 90 10          BCC B915
B905: BD AB AF       LDA $AFAB,X
B908: F0 08          BEQ B912
B90A: BD FF AE       LDA $AEFF,X
B90D: C9 FF          CMP #$FF
B90F: F0 01          BEQ B912
B911: 9B             TXY
B912: B9 AB AF       LDA $AFAB,Y
B915: E0 0A 00       CPX #$000A
B918: 90 E5          BCC B8FF
```

### What this actually does
This is not random compare noise.

It scans the later entries and updates `Y` only when the new candidate:
- is **not zero**
- has `AEFF[X] != FF`
- and is `<=` the current candidate in `A`

So the scan is best read as:

> **find the smallest eligible positive readiness work value**

with:
- candidate values taken from `AFAB..AFB5`
- eligibility gated by `AEFF != FF`
- zero entries ignored as minimum candidates

The loop seeds from slot 0 and then compares against slots `1..10`.

That is real structure.

---

## 3. Zero values are deliberately excluded from the minimum search
The critical block is:

```text
BD AB AF    LDA $AFAB,X
F0 08       BEQ ...
```

If the candidate value is zero, the loop does **not** update `Y`.

That means zero is not treated as the minimum positive countdown.
It is explicitly excluded from candidate replacement.

This is a very useful semantic result.

### Strongest safe reading
Within this normalization pass:
- `0` does **not** mean “smallest active timer”
- `0` behaves as a **special/terminal/already-resolved state** that should not drive subtractive normalization

I am keeping the final gameplay-facing noun slightly cautious, but the code is explicit: zeros are preserved, not normalized downward.

---

## 4. `AEFF == FF` entries are also excluded from candidate replacement
The second gate is:

```text
BD FF AE
C9 FF
F0 01
9B
```

If `AEFF[X] == FF`, the candidate index is not replaced.

So the minimum search is not over all 11 raw work bytes.
It is over the subset of entries that are both:
- nonzero in `AFAB`
- non-`FF` in `AEFF`

That upgrades the old vague “AEFF is somehow involved” wording.

### Strongest safe reading
`AEFF` is functioning here as an **active/eligible slot gate** for the readiness normalization pass.

I am still not freezing the final gameplay-facing noun for `AEFF`, but its role in this routine is now concrete.

---

## 5. The selected minimum is converted into a subtractive delta of `(min - 1)`
After the scan completes, the routine does:

```text
B91B: B9 AB AF    LDA $AFAB,Y
B91E: 3A          DEC A
B91F: 85 00       STA $00
```

So `$00` becomes:

```text
selected_minimum - 1
```

That is the key arithmetic fact.

This is not a clamp-to-zero pass.
It is not a “make everything start at zero” pass either.

It is a **subtract-to-one** pass.

---

## 6. `FD:B923..B939` subtracts that delta from every eligible positive entry
The second loop is:

```text
B921: 7B             TDC
B922: AA             TAX

B923: BD FF AE       LDA $AEFF,X
B926: C9 FF          CMP #$FF
B928: F0 0B          BEQ B935

B92A: BD AB AF       LDA $AFAB,X
B92D: F0 06          BEQ B935

B92F: 38             SEC
B930: E5 00          SBC $00
B932: 9D AB AF       STA $AFAB,X

B935: E8             INX
B936: E0 0B 00       CPX #$000B
B939: 90 E8          BCC B923
```

### What it proves
For each slot `0..10`:
- skip if `AEFF[X] == FF`
- skip if `AFAB[X] == 0`
- otherwise:

```text
AFAB[X] = AFAB[X] - (selected_minimum - 1)
```

So this is a clean subtractive normalization across the unified work array.

---

## 7. The exact postcondition is now clear: the smallest eligible positive entry becomes `1`
Given the arithmetic above:

```text
new_value = old_value - (min - 1)
```

For the selected minimum entry itself:

```text
new_min = min - (min - 1) = 1
```

So the pass guarantees:

> after normalization, the smallest eligible positive readiness work value is exactly `1`

That is the cleanest, strongest statement this pass can support.

### Consequence
This preserves the relative spacing between all eligible positive entries while shifting the active range downward so the next active positive event is always one step away.

That is much stronger than pass 53's provisional wording.

---

## 8. Zero entries remain zero; absent/ineligible entries remain untouched
Because the second loop skips:
- `AFAB[X] == 0`
- `AEFF[X] == FF`

those entries are not modified.

So the normalization has three classes:

### Class A — eligible positive entries
- participate in the minimum search
- receive subtractive normalization
- minimum positive becomes `1`

### Class B — zero entries
- excluded from minimum search
- excluded from subtraction
- remain `0`

### Class C — `AEFF == FF` entries
- excluded from minimum search
- excluded from subtraction
- remain unchanged

This is an important semantic cleanup because it tells us the routine is not a blind whole-array math pass.

It is an **active-subset normalization**.

---

## 9. Export tail at `B93B..B94F` now has exact semantics in context
Pass 53 already proved that only the head partition is exported:

```text
AFAB -> 99DD / 9F22
AFAC -> 99DE / 9F23
AFAD -> 99DF / 9F24
```

What pass 54 adds is the exact meaning of that export timing:

> the visible head export is not a raw copy of seeded work values.  
> It is a copy of the **post-normalized** head partition after the full 11-slot active subset has been shifted so the next eligible positive slot is at `1`.

That matters a lot.

It means the head panel/gauge export is being presented in a normalized readiness space that already incorporates:
- the hidden/runtime tail slots
- the active eligibility gate from `AEFF`
- zero-preservation for already-special entries

So the visible head is downstream of the unified 11-slot readiness model, not just a local three-entry panel trick.

---

## 10. This materially strengthens the readiness/timer interpretation from passes 49–53
The combined story is now much tighter:

- pass 49 pinned the numeric panel fields toward HP/MP
- pass 50 and pass 51 pinned the lane bar path as readiness/active-time related
- pass 52 solved the config/speed seed formula
- pass 53 proved the visible 3-slot head + hidden 8-slot tail partition
- **pass 54 proves the whole 11-slot work array is normalized together by subtracting the smallest eligible positive countdown to `1` before the head export occurs**

That is a real timer/countdown behavior, not generic status storage.

### Strongest safe reading after pass 54
`AFAB..AFB5` behaves here as a unified battle-readiness countdown/work array where:
- `0` is special/already-resolved
- positive eligible values are shifted together
- the next positive-to-fire entry becomes `1`
- only the head partition is then copied out to the visible export buffers

That is no longer a loose metaphor. It is what the code is doing.

---

## 11. What changes from pass 53

### Retired provisional wording
Pass 53 ended with:

> `FD:B8F5..B93A` strongly looks like a pre-export normalization pass,
> but the exact minimum/subtractive semantics still deserve one dedicated pass.

That uncertainty is now gone.

### Strong replacement
The exact semantics are:

> **minimum-positive subtractive normalization of the active subset of the unified 11-slot readiness work array, forcing the smallest eligible positive value to `1` before head export**

That is the right carry-forward description now.

---

## 12. Open edges after this pass
This pass resolves the normalization math itself, but a few edges remain worth tracing:

1. the exact gameplay-facing identity of `AEFF`
   - it is now definitely an eligibility/presence gate in this routine
   - final frozen subsystem noun still wants one more direct producer pass
2. the exact higher-level meaning of zero in `AFAB`
   - structurally “special/already-resolved” is safe here
   - final noun (ready/just-fired/blocked/etc.) still wants one more downstream confirmation
3. the exact relation between the normalized readiness array and the later ready-transition helpers:
   - `BDE0`
   - `BE50`
   - `BED0`
4. whether the tail partition is purely enemy/runtime-side or a more generic extended battler slot space

---

## Bottom line
Pass 54 closes the last real ambiguity from pass 53.

`FD:B8F7..B93A` is not generic cleanup.
It is a real arithmetic normalization pass over the unified 11-slot readiness work array:

- find the smallest eligible positive entry
- compute `(min - 1)`
- subtract that from every eligible positive entry
- leave zeros untouched
- leave `AEFF == FF` entries untouched
- then export only head slots `0..2` to the visible buffers

That is actual semantic progress, not just another rename.
