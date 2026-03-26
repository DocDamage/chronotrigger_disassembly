# Chrono Trigger (USA) — Disassembly Pass 37

## Scope
This pass continues directly from pass 36 and stays on the exact seam it exposed:

- the `C1:C736 / C1:C741 -> JSR $0003` trigger wrappers
- the engine behind `C1:0003 / C1:0045`
- the consumers/producers of `$9604..$9608`
- the result-vector lifecycle around `$99C0` and `$A62D`

The goal of this pass was **not** to overclaim final gameplay semantics for every query submode.
The goal was to stop calling `JSR $0003` a vague "service" and to pin:

1. the real dispatch layer behind it
2. which top-level selector each descriptor wrapper actually targets
3. how the selector-`7` family uses `$99CC` and `$9604..$9608`
4. how the result vectors are initialized and finalized

---

## Baseline carried forward from pass 36
Pass 36 had already established:

- `C1:C55F` is a descriptor-driven candidate expansion/finalization pipeline
- `C1:C95C` dispatches packet writers that emit bytes into `$9604..$9608`
- `C1:C736` and `C1:C741` are two descriptor-selected wrappers that:
  - store `$3D` into either `$986E` or `$99CC`
  - invoke `JSR $0003` with fixed selector `A=#05` or `A=#07`
- the exact engine behind `JSR $0003` and the meaning of the downstream result buffers were still left open

This pass closes that exact gap.

---

## What was done in this pass
1. Fully decoded the local bank-`C1` dispatch veneer at `C1:0003 / C1:0045`
2. Extracted the primary service table at `C1:0051`
3. Confirmed the `A=#05` and `A=#07` selector targets used by `C736` / `C741`
4. Decoded the secondary selector-`7` dispatch at `C1:1FDD`
5. Extracted the selector-`7` submode table at `C1:1FEA`
6. Decoded the result-buffer lifecycle helpers at `C1:27D9` and `C1:27E8`
7. Re-traced the major selector-`7` handler families far enough to pin what they consume and what they produce without over-naming the exact gameplay predicates

---

## Core results

### 1. `C1:0003 / C1:0045` is a real bank-local indexed-JSR dispatch veneer
This is no longer speculative.

Observed body:

```text
C1:0003  JMP $0045

C1:0045
  PHA
  PHX
  PHY
  ASL A
  TAX
  JSR ($0051,x)
  PLY
  PLX
  PLA
  RTS
```

So `JSR $0003` is a compact **A-register-selected local service dispatcher**, not an opaque helper call.

That matters because pass 36 only knew that `C736` and `C741` called it with fixed selectors.
This pass proves the dispatch mechanism itself.

Safest reading:

> `C1:0003 / C1:0045` = **bank-C1 indexed local-service dispatcher**

---

### 2. `C1:0051` is the primary local-service jump table
The first 8 table entries are now pinned directly from the bytes:

```text
service 0 -> C1:0023
service 1 -> C1:1B19
service 2 -> C1:1BAA
service 3 -> C1:106E
service 4 -> C1:4058
service 5 -> C1:2986
service 6 -> C1:006D
service 7 -> C1:1FDD
```

Only services `5` and `7` are relevant to the current `C55F` descriptor path.

This cleanly upgrades the pass-36 wrapper understanding:

- `C1:C736` does **not** call a vague service blob; it routes into **service 5** at `C1:2986`
- `C1:C741` does **not** call the same thing; it routes into **service 7** at `C1:1FDD`

This also matches the older handoff result that service `5` is the relation-query block.

---

### 3. `C1:C736` now ties directly into the already-proven relation-query subsystem
Pass 36 had only proven:

- `986E = 3D`
- `A = #05`
- `JSR $0003`

Pass 37 closes the loop:

- selector `#05` from the local dispatcher lands at `C1:2986`
- `C1:2986` is already the known **relation-query workspace + dispatch** entry
- `C1:2D81` remains its secondary jump table

So `C1:C736` can now be strengthened from:

> store `3D` to `986E` and call service 5

to:

> **store relation-query mode to `986E` and dispatch the bank-C1 relation-query service**

This is a genuine strengthening, not a rename for style.

---

### 4. `C1:C741` routes into a different service family entirely: `C1:1FDD`
Selector `#07` in the same local dispatcher lands at:

```text
C1:1FDD
  LDA $99CC
  CMP #$07
  BCS return
  ASL A
  TAX
  JSR ($1FEA,x)
return:
  RTS
```

So `C1:C741` feeds:

- `$99CC = 3D`
- `A = #07`
- `JSR $0003`
- which lands in `C1:1FDD`
- which then **sub-dispatches again** using `$99CC`

This is a second-stage mode dispatch, completely separate from the relation-query family.

Safest reading:

> `C1:1FDD` = **selector-`7` submode dispatcher keyed by `$99CC`**

This is the first strong structural proof that the pass-36 descriptor path was driving **two different downstream engines**, not one.

---

### 5. `C1:1FEA` is a 7-entry selector-`7` submode table
The submode table used by `C1:1FDD` resolves as:

```text
0 -> C1:25A3
1 -> C1:2701
2 -> C1:2701
3 -> C1:23A4
4 -> C1:25A3
5 -> C1:23A4
6 -> C1:2332
```

So the selector-`7` family is **not** 7 unique handlers.
It collapses into 4 real bodies:

- `C1:25A3` for submodes `0` and `4`
- `C1:2701` for submodes `1` and `2`
- `C1:23A4` for submodes `3` and `5`
- `C1:2332` for submode `6`

That is the same kind of alias/compression pattern already seen in the command tables themselves.

---

### 6. The selector-`7` family is a coordinate-driven candidate-list materializer
This is the most important semantic upgrade of the pass.

Across the four real selector-`7` handler bodies (`2332`, `23A4`, `25A3`, `2701`), the bytes consistently show the same broad structure:

- read packet parameters from `$9604..$9608`
- read slot-position/state tables including `1D0C` / `1D23`
- scan bounded object-slot ranges using the active-slot/state tables (`96F5`, `9FF7`, `A0A8`, `A09B`)
- append qualifying slot indices into the bounded vector at `$99C1+`
- seed or preserve a leading slot in `$99C0`
- finalize through the local buffer helpers at `27D9` / `27E8`

This is enough to safely say:

> selector `#07` is a **spatial / coordinate-driven candidate query family that materializes slot lists into `$99C0..`**

That is still intentionally conservative.
The exact gameplay meaning of each submode is still open, but the overall family role is no longer vague.

---

### 7. `C1:27D9` is the twin-result-buffer clear helper
Observed body:

```text
LDX #$000B
LDA #$FF
loop:
  STA $99C0,x
  STA $A62D,x
  DEX
  BPL loop
RTS
```

This proves all of the following:

- `$99C0..$99CB` is a bounded vector, not a scalar
- `$A62D..$A638` is a parallel/mirror bounded vector
- both vectors use `FF` as their empty marker
- the selector-`7` family explicitly clears both together before materializing results

So the old pass-36 wording "query result slots" can now be strengthened to:

> **twin bounded result vectors with `FF` empties**

---

### 8. `C1:27E8` is the selector-`7` result-finalize mirror helper
Observed body:

```text
LDA #$80
STA $960C
LDX #$000A
loop:
  LDA $99C0,x
  STA $A62D,x
  DEX
  BPL loop
RTS
```

Concrete behavior:

- sets bit 7 in `$960C` via `#$80`
- mirrors the first 11 bytes of `$99C0..` into `$A62D..`

Safest reading:

> **mark selector-`7` result state finalized/valid and mirror the live result vector into the shadow copy**

Do not over-name the exact bit meaning of `$960C.7` yet, but it is clearly tied to result finalization for this family.

---

### 9. `$99C0` and `$A62D` are now stronger labels than in pass 36
Pass 36 could only safely say `$99C0` was a bounded result vector consumed by `C55F`.

Pass 37 tightens this significantly:

- `$99C0..$99CB` is **directly produced** by selector-`7` candidate queries
- `$A62D..$A638` is a **shadow/mirror result vector** cleared in lockstep and later refreshed from `$99C0..`
- `FF` is the empty terminator/empty slot marker in both
- `C55F` is therefore consuming a result vector that is not abstract anymore; it is concretely one output path of the selector-`7` spatial candidate engine

This is a real semantic upgrade.

---

### 10. The selector-`7` submodes collapse into four handler families, but exact predicates remain open
The bytes are strong enough to pin the handler families, but not strong enough yet to assign final gameplay names.

#### `C1:2332` (submode `6`)
Strong structure:

- uses `$9605` as the seed slot
- computes simple low/high bounds around that slot's `1D23` coordinate using `±0x20`
- clears result buffers via `27D9`
- scans qualifying object slots
- appends matches to `$99C1+`
- stores the seed slot into `$99C0`

Safest reading:

> **seeded one-axis window/range scan**

#### `C1:23A4` (submodes `3`, `5`)
Strong structure:

- loads multiple position values from `1D0C/1D23`
- sorts/reorders local coordinate pairs into ordered min/max form
- uses repeated `JSR $0222` geometry/math helper calls
- scans object slots and appends qualifying matches into `$99C1+`
- finalizes through the result-buffer tail

Safest reading:

> **multi-point bounds/geometry scan family**

#### `C1:25A3` (submodes `0`, `4`)
Strong structure:

- consumes a wider parameter set from `$9605/$9606/$9607/$9608`
- builds several derived local metrics through `JSR $0222` / `JSR $01F9`
- scans object slots and appends matches into `$99C1+`
- finalizes through the same result-buffer tail

Safest reading:

> **extended spatial metric scan family**

#### `C1:2701` (submodes `1`, `2`)
Strong structure:

- normalizes slot coordinates through `JSR $011A`
- computes absolute deltas to a seed position
- maps each delta through lookup table `CC:FB6F`
- combines the mapped deltas and compares against `$9607`
- appends qualifying slot indices into `$99C1+`

Safest reading:

> **transformed-delta threshold scan family**

These are still provisional labels, but they are far better than treating selector `7` as an anonymous black box.

---

## What changed from pass 36, in practical terms
Before this pass, the best safe wording was:

- `C736/C741` are wrappers that call some local service engine
- `$9604..$9608` are packet bytes
- `$99C0` is some common-tail result vector

After this pass, the stronger byte-proven picture is:

- `C1:0003 / C1:0045` is a real indexed local-service dispatcher
- selector `#05` = the known relation-query engine at `C1:2986`
- selector `#07` = a different submode-dispatched candidate-query engine at `C1:1FDD`
- `$99CC` is the selector-`7` submode register
- `$9604..$9608` feed the selector-`7` handler families directly
- `$99C0..` and `$A62D..` are twin bounded result vectors produced/finalized by that engine

That is a substantial tightening of the pass-36 downstream picture.

---

## Remaining uncertainty / guardrails
What is still **not** safe to claim yet:

- final gameplay names for selector-`7` submodes `0..6`
- exact semantics of packet bytes `$9604..$9608` per submode
- whether `$960C.7` means "results valid", "results mirrored", or a broader mode flag beyond this family
- the exact relationship between selector-`7` result vectors and every consumer outside the `C55F` common tail

So the right posture is:

- strong labels for the dispatch and result-buffer lifecycle
- provisional labels for the specific query shapes/metrics
- no fake final subsystem names beyond "spatial / coordinate-driven candidate query family"

---

## Best next target after pass 37
The cleanest continuation point is now:

1. fully decode the four real selector-`7` bodies (`2332`, `23A4`, `25A3`, `2701`) to turn the current provisional scan-family labels into exact query semantics
2. re-check how `C55F` interprets selector-`7` outputs in `$99C0..` when entries are `<3` vs `>=3`
3. then return to the remaining unresolved `C1:C1DD` / `C82D` type-`9` / mode-`4` seams with much stronger downstream context

At this point, the biggest uncertainty is no longer the dispatch engine.
It is the exact geometric/predicate meaning of the selector-`7` submodes.
