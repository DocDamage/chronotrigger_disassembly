# Chrono Trigger (USA) — Disassembly Pass 35

## Scope
This pass continues directly from pass 34 and stays on the helper seam that was left as the highest-value ambiguity:

- `C1:C1DD`
- `C1:AC89`
- `C1:ACCE`
- `FD:AB01`

The goal of this pass was not to overreach into a full rewrite of the `C1:C1DD` case tree. The goal was to convert the previously vague “helper” layer into concrete, byte-proven subroutines and to determine whether `FD:AB01` was real code or an opaque interpreter/data edge.

---

## Baseline carried forward from pass 34
Pass 34 had already established:

- group-2 opcode `0x01` routes through unique long helper `FD:AB01`
- group-2 opcode `0x02` uses `C1:C1DD` plus the shared success tail
- both paths eventually converge on the post-selector/finalization helper region around `AC89` / `ACCE`

What was still unclear was:

- whether `FD:AB01` is true linear code
- what `AC89` and `ACCE` actually do
- whether `AD09` / `AD35` are generic “mask rebuild” helpers or something more specific
- whether `C1:C1DD` is only a validator or also a candidate/materialization engine

---

## What was done in this pass
1. Fully decoded the linear body at `FD:AB01`
2. Fully decoded `C1:AC89`
3. Fully decoded `C1:ACCE` and split the adjacent `C1:ACF2` routine cleanly away from it
4. Fully decoded `C1:AD09` and `C1:AD35`
5. Re-traced the front half of `C1:C1DD` far enough to pin its high-level role and several concrete case families
6. Confirmed the shared failure site at `C1:C72B`

---

## Core results

### 1. `FD:AB01` is ordinary linear code, not data or an opaque interpreter entry
This was the most important uncertainty from pass 34.

`FD:AB01` is a normal long helper and it is short enough to decode directly.

Observed body:

```text
LDA $B18C
TAX
STX $28
LDA #$0B
TAX
STX $2A
JSL $C1FDBF
LDX $2C
STX $B2C3
LDX $B2C3
LDA $CC88CB,x
STA $B18E
LDA $B18C
STA $B18F
LDA $CC88CC,x
STA $B190
STZ $B191
RTL
```

So this helper does all of the following:

- uses current control value `$B18C` as an input argument
- hardcodes secondary argument `#$0B`
- resolves an index/result via `JSL $C1:FDBF`
- stores that result index into `$B2C3`
- materializes a **four-byte follow-up descriptor/state packet**:
  - `$B18E = $CC88CB[result]`
  - `$B18F = $B18C`
  - `$B190 = $CC88CC[result]`
  - `$B191 = 0`

This is now strong enough to retire the pass-34 caution that `FD:AB01` might be something other than real code.

### 2. `C1:AC89` is an opcode-sensitive merge/finalize helper for the `$B18E/$B18F` follow-up packet
`C1:AC89` is not a generic “commit” blob. It is compact and very specific.

Observed body:

```text
CLC
ADC #$03
ORA $B18E
STA $B18E
STZ $B191
LDA $AEE3
BEQ op00_tail
CMP #$01
BNE check_op02
LDA $B18E
ORA #$80
STA $B18E
STZ $B18F
LDA #$04
STA $AEEB
BRA done
check_op02:
CMP #$02
BNE done
LDA $B18E
ORA #$40
STA $B18E
LDA $0E
STA $B18F
done:
LDA $B18E
STA $10
RTS
```

Concrete behavior:

- input A is first increased by `3`
- that value is ORed into `$B18E`
- `$B191` is cleared every time
- then the helper switches on `$AEE3` (the current command/opcode class already tracked by the dispatcher)

Resolved opcode-sensitive tails:

#### If `$AEE3 == 0`
- clear `$B18F`

#### If `$AEE3 == 1`
- set bit 7 of `$B18E`
- clear `$B18F`
- set `$AEEB = 4`

#### If `$AEE3 == 2`
- set bit 6 of `$B18E`
- copy normalized parameter `$0E -> $B18F`

#### All cases
- copy final `$B18E -> $10`
- return

The safest label is therefore:

> **opcode-sensitive follow-up packet merge/finalize helper**

Do not over-name `$B18E/$B18F` as gameplay-facing fields yet, but they are clearly not random scratch anymore.

### 3. `C1:ACCE` is a tiny normalization helper, not a broad finalizer
This routine was previously grouped mentally with `AC89`, but it turns out to be much smaller and narrower.

Observed body:

```text
TDC
LDA $AEE5
TAX
CPX #$0001 : if equal A = #$04
CPX #$0002 : if equal A = #$04
CPX #$0003 : if equal A = #$0D
CPX #$0004 : if equal A = #$0D
STA $0E
RTS
```

So this helper simply normalizes the raw opcode-`0x01` secondary parameter `$AEE5` into the working scratch value `$0E`.

Resolved mapping:

- `1 -> 4`
- `2 -> 4`
- `3 -> 0D`
- `4 -> 0D`
- all other values fall through unchanged

This is strong enough to rename it from vague “follow-up helper” to:

> **`AEE5` normalization helper feeding scratch `$0E`**

### 4. `C1:ACF2` is a separate helper and should not be conflated with `ACCE`
The bytes immediately after `ACCE` start a separate routine.

Observed body:

```text
TDC
STA $AE90
LDA $B18B
STA $AE91
LDA $AEE3
STA $AE92
LDA $AEE4
STA $AE93
RTS
```

This routine is directly called by the group-2 dispatcher on the `B3B8 = 0` continuation path.

Best current reading:

> **snapshot current follow-up context into `AE90..AE93`**

That split matters because earlier passes treated the whole `AC89..ACF2` region as a blurrier helper zone than it really is.

### 5. `C1:AD09` and `C1:AD35` are exact bitmask builders, not generic “rebuild masks”
These two helpers are now fully pinned.

#### `C1:AD09`
Observed behavior:

- clears `$AE95`
- if `$AECB == 0`, returns
- if first selected entry `$AECC == $FF`, returns
- otherwise computes `0x8000 >> AECC[0]`
- ORs that into `$AE95`

Best reading:

> **build one-hot mask for the first current selected entry**

#### `C1:AD35`
Observed behavior:

- clears `$AE99`
- if `$AECB == 0`, returns
- iterates `X = AECB-1 .. 0`
- for each entry `AECC[x]`, computes `0x8000 >> AECC[x]`
- ORs those bits into `$AE99`

Best reading:

> **build aggregate bitmask for the full current selected-entry list**

This is stronger than the old generic “rebuild masks” wording. `AD09` is a single-entry one-hot builder; `AD35` is the multi-entry aggregate version.

### 6. `C1:C72B` is the shared local failure helper used by `C1:C1DD`
`C1:C72B` is simple and now worth carrying as a real label:

```text
LDA #$01
STA $AF23
RTS
```

So the working interpretation used in earlier passes is confirmed:

- `$AF23 = 0` -> validation/materialization success
- `$AF23 = 1` -> local failure reported by the `C1:C1DD` family

### 7. `C1:C1DD` is not just a validator; it is a validation + candidate materialization dispatcher
This pass does **not** fully solve the entire `C1:C1DD` tree, but it does finally pin its role tightly enough to relabel it.

#### Proven front-half behavior
At entry it:

- clears `$AF23`
- uses `$B18C` and helper `JSR $CB93`
- validates the primary seed/subject described by `$B18B/$B18C` against per-entry flag bytes in the `$5E4A/$5E4B/$5E4C/$5E4E/$5E53` family
- when `$B18B >= 3`, also validates mapped selector targets derived from:
  - `$AE97/$AE98`
  - `$B2EB/$B2EC`
  - `$B1BE[...]`
  against that same per-entry flag family

This makes it clear that the routine is not operating blind; it checks that the seed/selector-derived entries are eligible before building a result list.

#### Proven type-derivation step
The routine then derives a control/type byte (working scratch `$00`) and an auxiliary byte (`$0C`) from lookup tables, with the source tables changing by context:

- when `$B18B < 3`, it uses the `CC:1ACB/CC:1ACC` family or alternate `CC:1BB5` path depending on current stream flags
- when `$B18B >= 3`, it uses the `CC:86C9/CC:86CA` family

That type byte is then dispatched through a large case tree.

#### Proven case families from this pass
The full case tree is still open, but several concrete cases are now firm.

##### Type `0`, `5`, or `6`
These collapse to the same structure:

- map `$B2AE` through `JSR $C8F7`
- store one entry into `$AD8E`
- require the entry to pass the `$5E4A` bit-7 eligibility test
- set `$AD8D = 1`
- clear `$3A`
- jump into the common downstream path at `C55F`

##### Type `1`
Builds a list from the first three `AEFF` slots:

- scan `AEFF[0..2]`
- copy non-`FF` entries into `$AD8E[]`
- require at least one copied entry
- set `$AD8D = count`
- set `$3A = 1`
- jump into the common downstream path

##### Type `3`
Single mapped-entry case with extra gating:

- map `$B2AE` through `JSR $C8F7`
- store one entry into `$AD8E`
- require `$5E4A` bit 7 eligibility
- set `$AD8D = 1`
- if entry `< 3`, set `$0A = 1`
- otherwise require `$AF15[entry]` bit 7 and clear `$0A`
- set `$3A = 5`
- jump into the common downstream path

##### Type `4`
Builds a fixed list:

- `$AD8E = [0,1,2]`
- `$AD8D = 3`
- `$3A = 5`
- jump into the common downstream path

##### Type `7`
Routes through another helper family:

- `JSR $C82D`
- if that helper sets `$AF23 != 0`, fail through `C72B`
- otherwise clear `$3A` and continue into the common downstream path

That is enough to safely relabel `C1:C1DD` as:

> **validation + type-dispatched candidate-list materializer for `$AD8E/$AD8D`**

This is materially better than the old generic “validation helper” label.

---

## What changed in the understanding of the helper seam
Before this pass, the helper seam still looked like this:

- `FD:AB01` = unique but semantically unclear long helper
- `AC89/ACCE` = generic post-commit follow-up helpers
- `AD09/AD35` = generic mask rebuilds
- `C1DD` = some sort of validator

After this pass, it looks more like this:

- `FD:AB01` = **real code that resolves and materializes a four-byte follow-up descriptor packet into `B18E..B191`**
- `AC89` = **opcode-sensitive merger/finalizer for that packet**
- `ACCE` = **tiny secondary-parameter normalizer (`AEE5 -> 0E`)**
- `ACF2` = **separate snapshot helper for `AE90..AE93`**
- `AD09` = **one-hot first-entry mask builder**
- `AD35` = **aggregate selected-entry mask builder**
- `C1DD` = **validation + type-dispatched candidate-list materializer**

That is a substantial tightening of the actual semantics around the group-2 success/finalization side.

---

## Working interpretations strengthened by this pass

### `FD:AB01`
Best current reading:

> **resolve opcode-`0x01` follow-up descriptor from `$B18C` and materialize it into `B18E..B191`**

### `C1:AC89`
Best current reading:

> **merge current index/opcode mode into the `B18E/B18F/B191` follow-up packet**

### `C1:ACCE`
Best current reading:

> **normalize raw secondary parameter `$AEE5` into working scratch `$0E`**

### `C1:AD09`
Best current reading:

> **build one-hot mask from `AECC[0]` into `AE95`**

### `C1:AD35`
Best current reading:

> **build aggregate selected-entry mask from `AECC[0..AECB-1]` into `AE99`**

### `C1:C1DD`
Best current reading:

> **validate seed/selector context and materialize a candidate list into `AD8E/AD8D` via a type-dispatched case tree**

---

## New cautions after this pass
- Do **not** claim a gameplay-facing meaning for `B18E/B18F/B190/B191` yet. It is now proven that they form a structured follow-up packet, but their exact outward purpose still needs downstream-consumer proof.
- Do **not** over-name `$AEEB`; only one opcode-sensitive path in `AC89` writes it here.
- Do **not** pretend the full `C1:C1DD` tree is solved. The routine’s role is now pinned, but many of the later type cases still need decoding.
- Do **not** collapse `ACCE` and `ACF2`; they are separate routines with different responsibilities.

---

## Recommended next target after this pass
The best next continuation point is now:

1. continue deeper through the unresolved later type cases inside `C1:C1DD`
2. then trace the common downstream path rooted at `C1:C55F`
3. then trace the consumers of `B18E..B191` and `AE90..AE93`

That sequence should finally turn the current “follow-up packet” wording into real subsystem semantics instead of just strong structural labels.
