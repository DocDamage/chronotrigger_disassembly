# Chrono Trigger (USA) — Disassembly Pass 40

## Scope
This pass continues directly from pass 39 and stays on the exact seam it identified:

- trace the higher-level code that preloads the service-7 wrapper state bytes
- explain who writes `$960D`, `$960F`, `$9614`, and the surrounding launch-state fields
- classify the outer controller layer above `C1:1F79` instead of treating it as miscellaneous battle glue

The focus in this pass was the contiguous caller band rooted around:

- `C1:1153`
- `C1:129C / 12BC / 12ED`
- `C1:1369`
- `C1:1498`
- `C1:1561`
- `C1:176C / 1786`
- `C1:17DD`

This pass does **not** claim final gameplay-facing names for the whole subsystem yet.
The bytes now strongly suggest a cursor/grid-driven target-selection controller layered above service 7, but the exact downstream meaning of the `93EE..93F4` records still needs one more proof pass before locking that wording in as final.

---

## Baseline carried forward from pass 39
Pass 39 had already established:

- `C1:1FF8` is the real wrapper-opcode table for service 7
- `$960D & 7Fh` is the outer service-7 wrapper opcode
- `$9614` is the result-vector cursor
- `$960C.7` is the whole-vector mirror flag
- the wrapper bodies at `203A..22F5` choose between bounded collectors, scalar selectors, and packet builders for the service-7 geometry bodies

What remained open was the **caller layer above that wrapper table**:

- who picks the wrapper opcode,
- who resets / advances the result cursor,
- what `$9609` actually means,
- and how the outer controller chooses between the fixed-opcode, dynamic-opcode, and table-opcode launch paths.

---

## What was done in this pass
1. Re-traced the common service-7 entry at `C1:1F79`
2. Traced every in-bank caller of `C1:1F79`
3. Classified the three real launch families that feed `$960D`
4. Classified the shared replay/finalize path at `C1:1561`
5. Tightened the meanings of `$9609`, `$960F`, `$95DB`, `$95DC`, `$95E5`, `$95E6`, `$9F35`, and `$9F36`
6. Identified the inline 5-byte entry table consumed by the `1498` family

---

## Core results

### 1. `C1:1F79` is the common service-7 launch initializer, and it hard-binds `$960F` to the current slot
The common launch entry now has one especially important caller-visible fact pinned:

```text
LDA $95D5
TAX
STX $960F
STZ $9613
STZ $960C
STZ $960A
...
clear $99C0.. and $A62D..
...
use ($960D & 7Fh) to JSR through $1FF8
```

So within this whole outer controller layer:

> `$960F` = **current / preferred source slot for the next service-7 wrapper launch**

That is no longer a vague “seed slot” guess.
It is written exactly once here from `$95D5`, before every wrapper dispatch.

This also means the caller families in this pass are **not** choosing `$960F` themselves.
They choose the **wrapper opcode** and the **launch family**, while the common initializer injects the current slot.

---

### 2. `$9609` is the outer service-7 replay / follow-up phase counter
Before this pass, `$9609` was visibly involved in the service-7 path but was still vague.
The caller-layer control flow now makes it much tighter.

Observed facts:

- `115F`: if `$9609 != 0`, skip the fresh-launch path and jump straight to `1561`
- successful fresh launches at `12B6`, `1389`, and `14D5` all `INC $9609`
- the replay/finalize path at `157D` and `1626` decrements it
- `17E5`: if `$9609 != 0`, jump to the in-progress post-query branch at `1979`
- the general reset path at `1BFC` clears it

Safest reading:

> `$9609` = **outer service-7 replay / in-progress follow-up counter**

This is stronger than “some phase byte.”
The pattern is exactly “fresh launch increments it; replay/finalize decrements it; outer frame logic branches on nonzero.”

---

### 3. `C1:1153` is the outer current-slot service-7 controller
`C1:1153` is now the correct anchor for the caller layer above service 7.
Its structure is:

1. call `CFFAE2`
2. require current slot `$95D5 >= 0`
3. if `$9609 != 0`, jump to the replay/finalize path at `1561`
4. call `1115`
5. inspect `$95DB`
6. branch to one of three outer families:
   - `0` -> plain local-control branch band
   - `1` -> follow-up family rooted at `1320`
   - `2` -> follow-up family rooted at `143D`

So this is no longer a random shared routine.
It is the **outer controller for the current-slot service-7 query/selection flow**.

I am keeping the label source-neutral for one more pass, but architecturally this routine is the real top of the local caller stack.

---

### 4. `$95DC[current]` is a real 3-state local submode selector, not disposable scratch
The local branch family under `1153` proved a very clean 3-state control byte.

Observed facts:

- `1250` decrements `$95DC,current`, wrapping negative to `2`
- `1264` increments `$95DC,current`, wrapping `3 -> 0`
- `128B` reads `$95DC,current` and dispatches:
  - `0` -> `129C`
  - `1` -> `12BC`
  - `2` -> `12ED`
- `11FE` / `1236` copy the current slot's `$95DC` value into another slot chosen through the 3-entry ring at `$A6D9`
- `16B1` snapshots `$95DC,current` into `$9916,current`

Safest reading:

> `$95DC[x]` = **per-slot 3-state local query/selection submode index**

The exact human-facing mode names are still open.
The 3-state structure itself is no longer open.

---

### 5. `129C / 12BC / 12ED` are the three launch branches selected by `$95DC[current]`
Once the local 3-state selector is pinned, the three launch branches become much easier to read.

#### `C1:129C` — state 0 fixed-opcode launch
This branch:

- does `JSL $CD002D` with `A = FFh`
- increments `$A43F` twice
- stores constant `07h` into `$960D`
- clears `$9615`
- calls `1F79`
- on success, increments `$A4EE` and `$9609`

Safest reading:

> `129C` = **state-0 fixed-wrapper-opcode launch (`$960D = 07h`)**

This is the cleanest proof in the pass that the outer caller layer really does choose service-7 wrapper opcodes.

#### `C1:12BC` — state 1 launch-family setup
This branch is gated by `$A0A7.bit0` and, when allowed, does:

- `STA $9EE7 = FFh`
- `STZ $A09A`
- `STZ $A099`
- `INC $A862`
- `JSR $0A88`
- `JSR $0AD3`
- `STZ $A862`
- `STA $9615 = 1`
- `STA $95DB = 1`
- `STZ $A869`
- `INC $A86A`

This branch does **not** call `1F79` directly.
Instead, it sets up the later follow-up family that `1153` will route into via `$95DB = 1`.

Safest reading:

> `12BC` = **state-1 outer follow-up-family setup**

#### `C1:12ED` — state 2 launch-family setup
This branch, when allowed, does:

- `STZ $A09A`
- `STA $9615 = 2`
- load `$95E6` into `$80`
- `JSR $095D`
- `JSL $CFFD6A`
- copy `0180h` bytes from `D1:5BD0` to `$0B40`
- `INC $99E2`
- `STA $95DB = 2`

Again, this branch does **not** launch `1F79` directly.
It prepares the later follow-up family selected by `$95DB = 2`.

Safest reading:

> `12ED` = **state-2 outer follow-up-family setup**

So the `95DC` tri-state dispatcher is now materially solved:

- one immediate fixed-opcode launch
- two deferred follow-up families

---

### 6. `C1:1369` is the dynamic-opcode launch family, and it pulls the wrapper opcode from `$9EE4`
The first follow-up family reached via `$95DB = 1` now has a very clean opcode source.

Observed structure:

```text
LDA $A099
BEQ fail
LDA $9EE5
BMI fail
LDA $9EE4
STA $960D
JSR $1F79
LDA $9613
if negative: STZ $9614
else: INC $A4EE ; INC $9609
```

Safest reading:

> `1369` = **dynamic service-7 wrapper launch using opcode from `$9EE4`**

This is the first caller family where the wrapper opcode is **not** hardcoded and **not** read from an inline table.
It comes from a live state byte pair (`$9EE4/$9EE5`) gated by `$A099`.

The exact semantic names of `$9EE4/$9EE5/$A099` remain open.
What is now strong is the launch role:

- `$9EE4` feeds `$960D`
- `$9EE5` is a validity/sign gate
- `$A099` is an enable/non-empty gate

---

### 7. `C1:1498` is the table-driven launch family, fed by 5-byte entries rooted at `C1:1580`
The second follow-up family reached via `$95DB = 2` turned out to be the richest result in the pass.

Its first half is:

```text
CLC
LDA $95E6
ADC $95E5
STA $80
STA $AD
LDA #$05
STA $AE
JSR $0089      ; multiply AD * AE -> AF
LDX $AF
LDA $1582,X    ; sign gate
BMI fail
LDA $1583,X    ; remaining-count gate
BEQ fail
LDA $1580,X
STA $9F35
LDA $1581,X
STA $960D
STX $9F36
JSR $1F79
...
```

Two strong outcomes fall out of this.

#### 7a. `($95E6 + $95E5)` is the entry index used by this family
The code explicitly sums `$95E6 + $95E5`, then multiplies that sum by 5.
So the outer cursor bytes are **not** independent here.
They combine into the linear index for the 5-byte entry table.

#### 7b. The family uses a real 5-byte entry table rooted at `C1:1580`
Because the product is multiplied by 5 and used as `X`, the reads from `1580/1581/1582/1583` are not random code fetches.
They are deliberate record-field reads from 5-byte entries.

The proven fields are:

- `entry + 0` -> copied to `$9F35`
- `entry + 1` -> copied to `$960D` (wrapper opcode)
- `entry + 2` -> sign/validity gate (`BMI` fails)
- `entry + 3` -> remaining-count / enabled gate (`BEQ` fails)
- `entry + 4` -> still unresolved in this pass

And later, at `1685`, the same family does:

```text
LDX $9F36
DEC $1583,X
LDA $9F35 -> $84
```

So `entry + 3` is definitely a consumable counter-like field, and `$9F36` is the saved byte offset of the selected 5-byte record.

Safest reading:

> `1498` = **table-driven service-7 launch using 5-byte entries at `1580 + 5*index`**

This is one of the strongest results in the session so far because it turns a vague band of code into a real data-driven launcher.

---

### 8. `$95E5` and `$95E6` are outer cursor/index components, not random temporary bytes
This became materially stronger because the table-driven family consumes their sum as an entry index.

Observed behavior:

- `$95E5` is decremented / incremented with clamp logic around `0..2`
- `$95E6` is adjusted in coarse steps of `±3`
- helper paths at `17A1/17BF` also nudge `$95E6` by `±1` when edge conditions are hit
- `1498` uses `($95E6 + $95E5)` as the table index source

Safest reading:

> `$95E5` / `$95E6` = **outer cursor/index components whose sum feeds the table-driven launch family**

I am intentionally not forcing final human-facing “row/column/page” names yet.
The bytes prove indexed cursor components and a summed linear table index.
They do not yet prove the exact UI vocabulary.

---

### 9. `$9F35` and `$9F36` are the latched aux/opcode-record fields for the table-driven family
These bytes were nearly unlabeled before this pass.
They now have clean structural roles.

#### `$9F36`
Written only by the table-driven launch family:

- `STX $9F36` after choosing a 5-byte entry
- later used as `LDX $9F36` before `DEC $1583,X`

Safest reading:

> `$9F36` = **saved byte offset of the selected 5-byte launch entry**

#### `$9F35`
Written from `entry + 0`, then later consumed in the finalize path:

- `LDA $1580,X -> STA $9F35`
- later `LDA $9F35 -> STA $84`
- `$84` is then written into the per-result record at `93F4`

Safest reading:

> `$9F35` = **latched auxiliary payload byte from the selected 5-byte launch entry**

The human-facing meaning of that payload byte remains open.
Its table-field role is now strong.

---

### 10. `C1:1561` is the common replay/finalize path layered above a completed wrapper launch
The nonzero-`$9609` path and the success continuation from the fresh launchers converge here.

Its structure is:

1. call `1F79` again using the already-prepared wrapper state
2. inspect `$9613`
3. if failed, clear `$9614`
4. otherwise:
   - optionally play the `1B55` helper path depending on `EE`
   - clear `$9614` and `$960E`
   - decrement `$9609`
   - branch through a longer follow-up/finalize family

Later in the same flow:

- `176C` advances `$9614` to the next live `$99C0` entry and exports it to `$A62D`
- `1786` moves `$9614` to the previous live `$99C0` entry and exports it to `$A62D`
- both end through the common cleanup at `179C`

Safest reading:

> `1561` = **common service-7 replay/finalize path after a successful wrapper launch**

This is also where the result cursor discovered in pass 39 becomes anchored to the outer controller.
Pass 39 proved what `$9614` does inside the wrapper layer.
This pass proves the higher-level controller actually uses it as a replay/finalize cursor.

---

### 11. `$EF` is now stronger as an outer option byte with two distinct bit families
I still do **not** have the ultimate producers of `$EF` in hand, but its outer behavior is materially tighter now.

In the outer controller layer:

- bits `0` and `2` choose local decrement/increment style branches in the `11xx / 13xx / 14xx` bands
- bits `1` and `3` are later consumed by the service-7 packet builders as result-cursor rotation controls (pass 39)

That means `$EF` is not random scratch and not just a pure service-7 local byte.
It is an **outer option/control byte** that survives long enough to influence both:

- pre-launch local state changes
- post-collector result-cursor rotation

Safest reading:

> `$EF` = **caller-provided outer option byte spanning local-state and result-rotation behavior**

I am still keeping it provisional until I trace the true producers.

---

### 12. The whole caller stack now looks much more like a cursor/selection controller than an abstract relation service shell
This pass does **not** lock the final gameplay-facing subsystem name yet.
But the evidence has crossed a meaningful threshold.

Taken together, the outer layer now contains:

- a current-slot controller (`1153`)
- a per-slot 3-state submode selector (`95DC[x]`)
- cursor/index components (`95E5/$95E6`)
- a fixed-wrapper launch family
- a dynamic-opcode launch family
- a table-driven launch family using 5-byte records
- result-vector cursor stepping (`9614`)
- repeated sound/helper calls via `1B55`
- UI-ish writes to `0700..070F` and `0900`
- final record emission into `93EE..93F4`

So the outer shell above service 7 is no longer best described as “misc code around the query engine.”
It is a **real selection/controller layer**.

The only reason I am not force-renaming it to a final battle-targeting label in this pass is that the `93EE..93F4` sink still deserves one more direct semantic pass.

---

## Strengthened state-byte interpretations

### `$9609`
> **outer service-7 replay / in-progress follow-up counter**

### `$960F`
> **current / preferred source slot injected by the common service-7 launch init**

### `$95DC[x]`
> **per-slot 3-state local query/selection submode index**

### `$95DB`
> **outer follow-up-family selector**

Observed values now proven in practice:

- `0` = local/no deferred follow-up family
- `1` = route into the `1369` dynamic-opcode family
- `2` = route into the `1498` table-driven family

### `$95E5`, `$95E6`
> **outer cursor/index components whose sum feeds the table-driven launch family**

### `$9F35`
> **latched auxiliary payload byte from the selected 5-byte launch entry**

### `$9F36`
> **saved byte offset of the selected 5-byte launch entry**

### `$9615`
Still provisional, but stronger than before:

> **outer launch-family tag carried into the emitted `93F0` record byte**

Observed values in this pass:

- `0` = fixed-opcode family (`129C`)
- `1` = state-1 / `1369` family
- `2` = state-2 / `1498` family

---

## Cleaned-up control picture
The outer stack above service 7 is now best read as:

1. `1153` = current-slot controller
2. local input/submode handling via `$95DC[x]`, `$95E5`, `$95E6`, `EE`, and `EF`
3. launch-family selection:
   - fixed wrapper opcode `07`
   - dynamic opcode from `$9EE4`
   - table-driven opcode from 5-byte records at `1580 + 5*index`
4. `1F79` = common wrapper launch initializer
5. service-7 wrapper table at `1FF8`
6. replay/finalize path at `1561`
7. result-cursor stepping through `$9614`
8. final record sink at `93EE..93F4`

This is a major narrowing of the architecture gap above the already-solved service-7 geometry core.

---

## What remains unresolved after pass 40
1. the true producers of `EE` and `EF`
2. the exact gameplay meaning of the 5-byte entry table rooted at `1580`
3. the human-facing names for the `93EE..93F4` emitted record fields
4. the exact semantic names of `$9EE4/$9EE5/$A099/$A09A`
5. whether the whole subsystem can now be safely renamed from “service-7 outer controller” to a final battle-target-selection label

---

## Best next target
The cleanest next continuation point is now:

- the final sink at `16DA..1713` into `93EE..93F4`
- plus the consumers of those records

That is the seam most likely to convert the current conservative “selection/controller layer above service 7” wording into final gameplay-facing subsystem names.

A secondary target is tracing the upstream producers of `EE` and `EF`, since those bits now clearly shape both pre-launch and post-launch behavior.
