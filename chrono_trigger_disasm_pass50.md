# Chrono Trigger Disassembly Pass 50

## Scope of this pass
This pass continued directly from pass 49’s live seam:

- determine the real gameplay-facing meaning of the scaled bar path driven by `99DD / 9F22`
- re-check the upstream producer family around `B158 / AFAB / BD6F / BDE0..BF25`
- decide whether the bar in `C1:06F0` is merely a generic meter or the party-lane active-time/readiness gauge

This pass materially tightens that branch.
The strongest result is that the `0CC0` lane bar is no longer best read as a generic “status gauge.”
It is now best read as the **party lane active-time / readiness gauge**.

I am still keeping one layer of caution on the exact current-vs-threshold split of `99DD` and `9F22` in every transition family, but the human-facing role of the bar itself is now much harder.

---

## Method
1. Re-read the full bar writer at `C1:06F0` in the context of pass 49’s already-solved HP/max-HP/MP strip.
2. Re-trace every strong C1-side writer to:
   - `B158`
   - `AFAB`
   - `99DD`
   - `9F22`
3. Focused on four proving bands:
   - `C1:B725..B73F`
   - `C1:BD6F..BDB2`
   - `C1:BCE0..BD63`
   - `C1:BDE0..BF25`
4. Only promoted labels that are supported by the combined UI role and the upstream time/status logic.

---

## Starting point from pass 49
Pass 49 had already established:

- the `0CC0` strip is a three-lane status presentation strip
- it renders current HP, max HP, and a strong-provisional current MP field
- `C1:06F0` is a real scaled bar renderer inside that same strip
- `99DD` behaves like the bar’s display value
- `9F22` behaves like a divisor/capacity input

What pass 49 did **not** yet settle was the actual gameplay-facing stat being shown by that bar.

---

## 1. `C1:B725` initializes the lane-bar exports as **empty progress over a fixed threshold**, not as HP/MP mirrors
The `B725` entry is now important enough to promote.

### Proven initialization body
The routine beginning at `C1:B725` does:

```text
STZ $99D4
LDA #$01
STA $99D8
LDA #$00
STA $99DD
STA $99DE
STA $99DF
LDA #$30
STA $9F22
STA $9F23
STA $9F24
```

### Why this matters
This is not how the already-solved HP/max-HP/MP fields behave.
Those come from battle-record data (`5E30 / 5E32 / 5E34`).
This separate family instead initializes:

- per-lane visible progress = `0`
- per-lane visible cap/threshold = `0x30`

That is exactly the shape you expect from a fill-gauge family, not from duplicated HP/MP state.

Safest promoted reading:

> `99DD..99DF` and `9F22..9F24` are the visible progress/cap exports for the lane bar branch.

And the initial `0 / 0x30` pairing materially supports a **time/readiness gauge** reading.

---

## 2. `C1:BD6F` is a shared **status-modified time-increment helper**, not a generic scalar mutator
This is the strongest semantic result in the pass.

### Exact local behavior
The helper at `C1:BD6F` starts from `AFAB[x]` and applies two different status-driven transforms:

```text
LDY lane_record_offset
LDA $5E4D,Y
ORA $5E52,Y
BIT #$80
BEQ skip_half
LDA $AFAB,X
LSR A
STA $AFAB,X

LDA $5E4B,Y
BIT #$20
BEQ skip_double
LDA $AFAB,X
ASL A
BCC keep
LDA #$FF
STA $AFAB,X

LDA $AFAB,X
BNE done
INC A
STA $AFAB,X
```

and for visible party lanes (`X < 3`) mirrors the adjusted value to:

```text
STA $99DD,X
STA $9F22,X
```

### Structural meaning
This is not HP.
This is not MP.
This is not a direct count of queued records.

What it *is*:
- a base scalar
- halved by one status family
- doubled (saturating) by another status family
- clamped away from zero
- then exported to the visible lane-bar state

That pattern is exactly what you expect for a **battle-time / readiness fill-rate scalar**.

The strongest safe wording from the ROM alone is:

> `BD6F` applies **slow-like / haste-like battle-status modifiers** to the per-lane time increment used by the visible bar branch.

I am intentionally keeping the exact human names of the status bits conservative at the bit level, but the fill-rate semantics are now hard enough that the “generic scalar” wording should be retired.

---

## 3. `B158 -> AFAB -> BD6F` now reads as a **base-rate -> modified-rate** chain for the readiness gauge family
Passes 42–43 already established that `B158` is the primary carried scalar and `AFAB` is its shadow/mirror.
This pass materially tightens what that scalar family is *for*.

### Strong repeated pattern
Multiple paths do the same setup before touching the bar branch:

```text
LDA $B158,X
STA $AFAB,X
JSR $BD6F
```

This appears in particular in:
- `C1:BCE0..BCF5`
- `C1:BDE0..BDF0`
- `C1:BE50..BE60`
- `C1:BED0..BEE0`
- `C1:E653..E65B`

### Meaning of the chain
This is the exact structure you would expect if:

- `B158[x]` = base fill rate / base readiness increment
- `AFAB[x]` = mutable, status-adjusted working rate
- `BD6F` = the status modifier pass

That is much tighter than the earlier “carried scalar / shadow value” wording.

Safest promoted reading:

> `B158` is the lane’s **base active-time/readiness increment**, and `AFAB` is the **status-adjusted working increment**.

---

## 4. The `BDE0 / BE50 / BED0` family now reads like **gauge advance / ready-transition** logic, not generic export churn
These three sibling bands remained vague in earlier passes because the exact caller identities were noisy.
Pass 50 does not fully solve every branch, but it tightens their role materially.

### Shared structural skeleton
All three families do the same high-level sequence:

1. select a lane/group participant through a table path
2. seed `AFAB` from `B158`
3. call `BD6F` to apply battle-status rate modifiers
4. run the adjusted value through `C90B` / `C92A`
5. add the adjusted increment into one or more lane-bar exports
6. set/update lane flags such as `B03A`, `B188`, and `93EE`

### Concrete update evidence
Two representative cases:

- `C1:BE21` ends in:
  ```text
  CLC
  ADC $AFAB,Y
  BCC keep
  LDA #$FF
  STA $AFAB,Y
  STA $9F22,Y
  ```

- `C1:BE9B` / `C1:BF18` end in:
  ```text
  CLC
  ADC $AFAB,Y
  BCC keep
  LDA #$FF
  STA $AFAB,Y
  STA $99DD,Y
  STA $9F22,Y
  ```

So these are not arbitrary copies.
They are saturating advance/update families over the same status-adjusted gauge branch.

### Safest keepable meaning
This is now best described as:

> the **active-time/readiness gauge advance and ready-transition family**

with some sibling variants differing in which visible mirrors are advanced together.

I am still keeping the exact role split between `99DD` and `9F22` slightly conservative here, because some variants advance only one export and others advance both.
But the overall family meaning is no longer generic.

---

## 5. Re-reading `C1:06F0` in that context upgrades the bar from “scaled meter” to **active-time/readiness gauge renderer**
Pass 47 had already solved the renderer mechanically.
Pass 50 upgrades the gameplay meaning.

### What `06F0` already proved structurally
The routine:

- chooses a lane-local anchor from `CC:FA35`
- loads two per-lane bytes from `99DD` and `9F22`
- computes a 32-unit scaled fill amount
- emits a four-tile segmented bar into the lane’s `0CC0` strip block

### What the upstream logic now adds
The upstream producer side now shows that the bar’s source values are:

- initialized as `0 / 0x30`
- driven by a base increment scalar (`B158`)
- modified by slow-like / haste-like status bits via `BD6F`
- advanced through saturating accumulation families tied to ready-state side effects

Combined with the already-solved HP/max-HP/MP fields in the same strip, the safest promoted reading is no longer “some other status gauge.”

The cleanest reading is:

> `C1:06F0` renders the **party lane active-time / readiness gauge**.

In practical terms, this is the UI bar that behaves like an **ATB-style fill gauge**.

---

## 6. Strongest current interpretation of the bar-related WRAM family
This is the state of the labels after this pass.

### `B158[x]`
Best read now as:

> **base active-time/readiness increment**

Still slightly conservative only because the exact caller that seeds it from the underlying actor stat family is not yet the cleanest possible single trace.

### `AFAB[x]`
Best read now as:

> **status-adjusted active-time/readiness increment shadow**

This is materially harder than “primary value shadow.”

### `99DD[x]`
Best read now as:

> **visible lane active-time/readiness gauge progress export**

This is stronger than pass 47’s generic “display value for scaled bar.”

### `9F22[x]`
Best read now as:

> **visible lane active-time/readiness gauge threshold/cap export**

This is stronger than pass 47’s generic “divisor or capacity.”
The `B725` initialization to `0x30` is the strongest single proof here.

---

## 7. What changed from pass 49
This pass did not just rename the bar because it “felt like ATB.”
It changed because the ROM now supports the upgrade through three independent proofs:

1. **UI context proof**
   - the bar sits in the same lane strip as HP / max HP / MP, matching a battle-status panel role
2. **producer semantics proof**
   - the bar’s source scalar is doubled/halved by battle-status bits in a time-like way
3. **initialization/advance proof**
   - the bar state initializes as `0 / 0x30` and is then advanced by saturating increment families with ready-state side effects

That is enough to move the bar from “generic meter” to **active-time/readiness gauge**.

---

## 8. What remains intentionally unresolved
A few details are still worth keeping conservative.

### The exact split between `99DD` and `9F22` in every transition variant
Some sibling advance paths update only `9F22`; others update both `99DD` and `9F22`.
So while the human-facing bar role is now hard enough, the exact per-variant semantics of:

- current visible fill
- threshold/cap
- frozen/full display mirrors during special states

should remain one step cautious until the remaining transition callers are traced more cleanly.

### The exact underlying actor-stat seed for `B158`
The base-rate reading is strong now.
The single cleanest “this exact actor field seeds it” trace is still worth tightening later.

### Exact human-facing names of the status bits in `5E4B / 5E4D / 5E52`
The ROM proves:
- one family halves the gauge rate
- another doubles it with saturation

That is enough for **slow-like / haste-like** semantics.
I am not freezing the exact status names at the individual-bit level in this pass.

---

## Summary of progress in pass 50
This pass materially advanced the bar branch.

It did **not** just restate that `06F0` draws a bar.
It connected the bar to its producer family tightly enough to promote a real gameplay-facing meaning:

- `B158` = base readiness increment
- `AFAB` = status-adjusted readiness increment
- `99DD / 9F22` = visible readiness-gauge exports
- `C1:06F0` = active-time/readiness gauge renderer for the party lane strip

That means the three-lane `0CC0` branch now reads as a much more coherent battle-status presentation unit:

- current HP
- max HP
- current MP
- active-time / readiness gauge

---

## Recommended next target after pass 50
The cleanest continuation point is now:

1. trace the exact seed path into `B158`
2. tighten the `BE21 / BE9B / BF18` variant split so the roles of `99DD` vs `9F22` are frozen per transition family
3. re-check whether the remaining unresolved `9F38[x]` producer side belongs to this same battle-status / readiness subsystem or only runs adjacent to it
