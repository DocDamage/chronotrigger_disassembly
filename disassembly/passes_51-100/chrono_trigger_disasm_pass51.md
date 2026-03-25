# Chrono Trigger Disassembly Pass 51

## Scope of this pass
This pass continued directly from pass 50's live seam:

- settle the exact practical split between `99DD` and `9F22` in the `0CC0` lane-gauge renderer
- trace a harder upstream writer/seed path into `B158`
- decide whether the battle-side writer families are really feeding a speed/readiness seed rather than just generic gauge churn

This pass materially tightens both.

The strongest results are:

1. `C1:06F0` really does treat `99DD` as the lane gauge's **current/fill numerator** and `9F22` as the **denominator/goal/cap export**.
2. Several later paths intentionally mirror them equal in order to force a **full/committed gauge export**.
3. The strongest upstream battle-side seed into `B158` is now the `FD:B820..B850` family, which derives it from a clamped **speed-like stat** plus a signed 16-step bonus table at `CC:2E31` and a small random/bias term.

I am still keeping one layer of caution on the exact final human-facing name of the source stat at record offset `+0x38`, but this is no longer vague enough to leave as “some scalar.”

---

## Method
1. Re-read `C1:06F0` as actual math instead of only as a renderer.
2. Compare three export families side by side:
   - `C1:B390`
   - `C1:BE00..BE2A`
   - `C1:BE80..BEA7`
   - `C1:BF00..BF24`
3. Trace the strongest battle-side stores to `B158` and `AFAB`:
   - `FD:B820..B850`
   - `FD:B8C0..B8E0`
4. Only promote labels that are supported by the combined producer/consumer chain.

---

## 1. `C1:06F0` proves `99DD` is the **fill/current** export and `9F22` is the **denominator/goal/cap** export
The renderer was already known to use both bytes.
This pass tightens the exact practical split.

### Key load/use sequence
At `C1:06F0`:

```text
LDA lane_index
ASL
TAX
LDA.l $CC:FA35,X
ADC #$001A
TAY
...
LDX lane_index
LDA $99DD,X
STA $AD
STZ $AE
LDA $9F22,X
STA $B3
STZ $B4
REP #$20
LDA $AD
JSR $010D
STA $B1
...
JSR $00D7
```

`$010D` is the simple 8x-`ASL` helper already identified in pass 49, so the renderer is scaling the `99DD` value before division.
`$00D7` is the hardware-divide path that consumes the `(B1/B2)` numerator and `(B3/B4)` denominator inputs.

That is strong enough to promote the practical semantics:

- `99DD` = exported **current/fill progress**
- `9F22` = exported **goal/cap/denominator**

This is stronger than the older, more generic “two bar inputs” wording.

### Why the earlier ambiguity existed
Pass 50 still had a real ambiguity because several higher-level update paths mirror the same value into both exports.
That is now explainable:

- when `99DD < 9F22`, the renderer produces a partial fill
- when code intentionally makes `99DD == 9F22`, the renderer produces a forced full bar

So the equal-write paths are not evidence that the two bytes always mean the same thing.
They are evidence of a **ready/full commit export mode**.

---

## 2. The three major update families split cleanly into **goal-only** versus **goal+current snap** paths
This pass materially tightens the exact split left open in pass 50.

### A. `C1:BE00..BE2A` updates `AFAB` and `9F22`, but not `99DD`
Representative tail:

```text
CLC
ADC $AFAB,Y
BCC keep
LDA #$FF
keep:
STA $AFAB,Y
STA $9F22,Y
```

This is the cleanest proof that `9F22` is not merely a copy of `99DD`.
This family advances the working value and exports it only as the **goal/cap-side denominator**.

Strongest safe reading:

> this family advances the lane gauge's working/goal value without also snapping the visible current fill to match.

### B. `C1:BE80..BEA7` and `C1:BF00..BF24` update both `99DD` and `9F22`
Representative tail:

```text
CLC
ADC $AFAB,Y
BCC keep
LDA #$FF
keep:
STA $AFAB,Y
STA $99DD,Y
STA $9F22,Y
```

These are the strongest “snap-to-full / commit-visible” paths in the branch.
They make the current export equal the denominator export, which forces the renderer to display a full bar.

This resolves the exact split left intentionally open in pass 50:

- `99DD` = visible current fill export
- `9F22` = visible denominator/goal export
- equal writes are a **state transition** choice, not the base semantics of the two bytes

---

## 3. `C1:B390` is a direct **seed/export mirror** path from `B158`
This routine is important because it sits above the renderer but below the higher-level controller noise.

### Proven write pattern
At `C1:B390`:

```text
LDA $B158,Y
STA $9F22,Y
STA $99DD,Y
STA $AFAB,Y
```

This is the cleanest direct bridge yet between the battle-side seed state and the visible lane-gauge exports.

### Meaning
This does **not** prove that `B158` is always the current visible bar value in every context.
But it does prove something important:

> `B158` is a direct upstream seed for the same lane-gauge branch that feeds `AFAB`, `99DD`, and `9F22`.

That materially tightens the upstream-side uncertainty from pass 50.
It is now too narrow to keep describing `B158` as only a vague carried scalar.

---

## 4. `FD:B820..B850` is the strongest upstream seed into `B158`
This is the most important battle-side finding in the pass.

### Proven structure
The family around `FD:B7E7..B850` iterates selected visible participants and, for each one:

1. obtains a participant/record pointer through the existing selector path
2. clamps record byte `+0x38` to a maximum of `0x10`
3. uses that clamped value (minus one, via the local setup) to index `CC:2E31`
4. combines the table result with a `0x69` base and the local `$2C` bias/random term
5. stores the result to both `B158` and `AFAB`
6. sets `B03A = 1` for the affected visible lane slot

The key write tail is:

```text
LDA #$69
SEC
SBC $2C
CLC
ADC $00
LDX visible_lane_slot
STA $B158,X
STA $AFAB,X
LDA #$01
STA $B03A,X
```

where `$00` was just loaded from `CC:2E31[index]`.

### What `CC:2E31` looks like
The 16-byte table at `CC:2E31` is:

```text
CD D1 D5 D9 DD E1 E5 E9 ED F1 F5 F9 FD 01 05 09
```

Interpreted as signed bytes, this is a smooth +4-step ladder from `-0x33` up to `+0x09`.
That is exactly the shape you would expect from a compact **speed/readiness bonus table** keyed by a clamped actor stat.

### Strongest safe reading
The ROM now supports the following stronger interpretation:

- record byte `+0x38` is a **speed-like stat** used to seed lane readiness
- `CC:2E31` is the corresponding **16-step readiness bonus table**
- `FD:B820..B850` is the strongest current candidate for the battle-side **base readiness seed writer** into `B158`

I am still keeping the human-facing word “speed” one step conservative because this pass did not fully unwind the outer record layout for that struct.
But the stat family is no longer generic.

---

## 5. `FD:B8C0..B8E0` is a sibling seed family for the adjacent visible-lane branch
The immediately following sibling does the same shape of work, but writes to the next pair:

```text
STA $B15B,X
STA $AFAE,X
```

instead of:

```text
STA $B158,X
STA $AFAB,X
```

It also sets the sibling flag family:

```text
STA $B03D,X
```

This is not just noise.
It shows that the `B158/AFAB` seed logic is part of a wider repeated visible-lane pattern rather than a one-off special case.

I am still keeping the exact per-offset family layout a little conservative here, but the structural repetition is now real.

---

## 6. Harder overall reading after this pass
With pass 50 plus this pass combined, the lane gauge branch now reads as:

1. battle-side seed into `B158` from a speed-like stat plus bonus/bias (`FD:B820..B850`)
2. mirror/working seed into `AFAB`
3. higher-level controller families advance/export either:
   - only the denominator/goal export (`9F22`), or
   - both current and denominator exports (`99DD == 9F22`) for full/ready commit
4. `C1:06F0` renders the visible segmented bar from that exact current-vs-goal pair

This is materially better than pass 50's still-slightly-fuzzy “readiness gauge with unresolved subvariant split.”
The subvariant split is now mostly solved.

---

## What this pass changes from pass 50
### Promoted
- `99DD` should now be treated as the **current/fill** export for the renderer.
- `9F22` should now be treated as the **goal/cap/denominator** export.
- `FD:B820..B850` should now be treated as the strongest current **battle-side readiness seed** writer into `B158`.
- `CC:2E31` should now be treated as a **speed-like stat to readiness bonus** table.

### Soft correction / caution
Pass 50's wording of `B158` as a pure “increment” is now probably too narrow.
This pass proves that `B158` is at least a direct **seed value** for the readiness-gauge branch and may subsume more than a single raw per-tick increment role.
I am intentionally leaving that one notch cautious instead of over-correcting it all the way in one pass.

---

## Next clean seam
The next best continuation point is now:

1. freeze the exact record layout around the participant byte at `+0x38`
2. identify the precise caller/source of the `$2C` bias term in `FD:B820..B850`
3. unwind the sibling family rooted at `B15B/AFAE/B03D`
4. re-check whether `B158/AFAB` should be finalized as **base/current seed** rather than the narrower **increment** wording from pass 50

That is where the remaining ambiguity actually lives now.
