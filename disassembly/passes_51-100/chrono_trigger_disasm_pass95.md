# Chrono Trigger Disassembly — Pass 95

## What I targeted
Pass 94 isolated two very clean seams instead of a fog bank:

- the remaining downstream C2 handler families at `5BF5 / 5C3E / 5C77`
- the active C7 `0x10/11/14/15` special path at `01A1`

I stayed on those seams.

---

## Strongest keepable result
This pass closes two real ambiguities:

> the three downstream C2 families are not “more token handlers” in the abstract. They are a **chained three-family stream stage** over the long pointer at `0237..0239`, with exact counter-driven exits keyed by `023A` and `0213`.

> the `C7:01A1` side is not just “the active 0x10..0x17 path”. It is a real **negative-`1E05` special path** that rebuilds/stages slot lists in `1F00..` / `1F20..`, reconciles them against the live `1E20/1E40/1E60` strips, and then performs exact APU traffic through `$2141/$2142/$2143` with command phases `0x07` and `0x02`.

That is a real structural closure.

---

## 1. `C2:5BF5` is the first downstream long-stream family

Pass 94 already proved `58B2` seeds `0237/0239/023A` and jumps into `5BF5` for the `0x21..0x9F` stream-token family.

Pass 95 freezes what `5BF5` actually does.

Exact keepable behavior:

- consumes the live long-pointer stream through exact direct-page indirect-long reads from `[0237]`
- advances the pointer by exact `INC 0237` steps
- normalizes the consumed value into exact local word `0235`
  - if the first consumed byte is neither `01` nor `02`, the already-read word is kept
  - if the first consumed byte is `01` or `02`, the path swaps / re-reads and promotes the next byte before storing `0235`
- calls the exact shared local helper `JSR $5DC4`
- then decrements both counters:
  - `023A`
  - `0213`
- reduces their post-decrement zero/nonzero state to a four-way indexed jump through the exact table at `5C28`

That four-way tail is exact enough to keep:

- if **both counters are exhausted**, it forces `0215 = 0x10` and returns
- if **`023A` remains but `0213` is exhausted**, it stores the live tail state directly into `0215` (exact fallthrough target `5C32`) and returns
- if **`023A` is exhausted but `0213` remains**, it jumps back to the primary dispatcher at `58B2`
- if **both remain nonzero**, it enters the next downstream family at `5C3C/5C3E`

So the strongest safe reading is:

> `C2:5BF5..5C3D` is the first downstream long-stream family, consuming entries from `[0237]`, materializing exact word `0235` through the shared `5DC4` helper, and routing by the exact exhausted/non-exhausted state of `023A` and `0213`.

---

## 2. `C2:5C3E` is the second downstream family with exact `+C2D4` rebasing

This family is very close to `5BF5`, but it has one exact change that is too concrete to ignore.

Exact keepable behavior:

- consumes the next entry from the exact same long pointer `[0237]`
- adds exact immediate base `C2:D4` before storing into `0235`
- calls the same exact shared helper `JSR $5DC4`
- decrements the same counter pair `023A` and `0213`
- dispatches through the exact four-entry jump table at `5C61`

The exact tail behavior is now frozen:

- case 0: clears `0230`, forces `0215 = 0x10`, returns
- case 1: forces `0215 = 0x10`, returns
- case 2: clears `0230`, jumps back to `58B2`
- case 3: branches directly into the third family at `5C77`

So the strongest safe reading is:

> `C2:5C3E..5C76` is the second downstream long-stream family, identical in its counter-driven control shape to `5BF5` but with an exact `+C2D4` rebasing step before the shared `5DC4` materializer runs.

That is materially more exact than “another handler family.”

---

## 3. `C2:5C77` is the third downstream family and the terminal self-looping stage

The third family reuses the same shared shape one more time.

Exact keepable behavior:

- consumes entries from the same live long pointer `[0237]`
- normalizes/stores exact word `0235`
- calls exact shared helper `JSR $5DC4`
- decrements exact counters `023A` and `0213`
- dispatches through the exact four-entry table at `5CAA`

Its exact tail behavior is now frozen:

- case 0: clears `0230`, forces `0215 = 0x10`, returns
- case 1: forces `0215 = 0x10`, returns
- case 2: clears `0230`, jumps back to `58B2`
- case 3: branches back into `5C77` itself (`BRA $B7`), making this the **terminal self-looping family** while both counters remain live

That means the broad C2 downstream picture is finally honest:

```text
58B2
 -> family 1 at 5BF5
 -> family 2 at 5C3E
 -> family 3 at 5C77
```

with exact transitions controlled by the live exhaustion state of `023A` and `0213`.

I am still keeping the final gameplay-facing noun of that stream language below frozen.
But the family shape itself is now exact enough to keep.

---

## 4. `C2:5D1D..5D55` is the exact local sentinel-scan helper cluster

This little helper neighborhood turned out to matter because `5BE0` uses it to seed `023A` before dropping into the first family.

There are three exact local scanners here:

- `5D1D..5D2E`
  - scans `[0237],Y` for exact byte `0xEF`
  - stops at `Y == 0x000A`
  - returns `Y`
- `5D2F..5D40`
  - scans `[0237],Y` for exact byte `0xEF`
  - stops at `Y == 0x000B`
  - returns `Y`
- `5D41/5D45..5D56`
  - scans `[0237],Y` for exact byte `0x00`
  - stops at `Y == 0x0005`
  - returns `Y`

So the strongest safe reading is:

> `C2:5D1D..5D55` is the exact local sentinel-scan cluster used to derive bounded inner counts from the active long stream at `0237`.

That tightens how `023A` is seeded before the chained family stage begins.

---

## 5. `C7:01A1..0216` is the special-path slot-list rebuild / candidate staging gate

Pass 94 already proved the early `0x10..0x17` table routes `0x10/11/14/15` into `01A1`, and pass 93 already proved negative `1E05` diverts here directly.

Pass 95 freezes the first phase of that path.

Exact keepable behavior:

- validates exact selector byte `1E01` against exact long value at `C7:0AE9`
  - on out-of-range, branches back to the common exit side
- calls exact local helpers `0734` and `0A39`
- copies `1E01 -> 1E05`
- clears two exact 0x20-byte strips through the loop over:
  - `1EFE..1F1E`
  - `1F1E..1F3E`
- scans backward through exact live strip `1E20..1E3E` to seed the last-active index in `0C`
- seeds two exact staging pointers:
  - `12 = 1F00`
  - `14 = 1F20`
- derives an exact `X` limit from masked / shifted `1E04`
- then walks the exact long table rooted at `C7:0E11`
  - writes nonzero entries sequentially into `[12]` (the `1F00..` candidate strip)
  - only writes entries not already present in `1E20..1E3E` into `[14]` (the `1F20..` “new / unmatched” strip)

Then it makes one exact early split:

- if `1F20 == 0`, it jumps directly to `037B`
- otherwise it continues into the reconciliation side at `0217`

So the strongest safe reading is:

> `C7:01A1..0216` is the special-path candidate rebuild / staging gate for the negative-`1E05` sound-command path, producing two exact staging strips at `1F00..` and `1F20..` before the live-slot reconcile phase runs.

---

## 6. `C7:0217..0325` is the exact live-slot reconcile / migration phase with command `0x07`

This is the next internal phase of the same path.

Exact keepable behavior:

- prunes dead entries from the live `1E20..1E3E` strip if they are absent from the new candidate strip at `1F00..1F1E`
- finds the first open slot in `1E20..1E3E`
- finds the last occupied slot in `1E20..1E3E`
- if those are the same, jumps directly to `0326`
- otherwise sends exact APU command byte `0x07` through `$2141`
- then iterates over the unmatched/new strip at `1F20..1F3E`
  - selects exact payload words from `1E60..` and `1E40..`
  - writes exact triplets through `$2142/$2143`
  - mirrors/migrates values back into the live strips `1E20..`, `1E40..`, and `1E62..`
  - updates exact local byte `84` through repeated helper calls to `09DA`
- if no free slot is available, it sends exact zero payload through `$2142/$2143`, then rebuilds `1EFE..1F7E` from the exact table rooted at `C7:0E0F`

Then it normalizes state for the next phase:

- forces `84 = 0xE0`
- jumps into the later emit phase at `0326/037B`

So the strongest safe reading is:

> `C7:0217..0325` is the exact live-slot reconcile / migration phase of the negative-`1E05` path, using command `0x07` and the `1F20..` unmatched strip to move staged sound-slot state into the live `1E20/1E40/1E60` workspace.

---

## 7. `C7:037B..04B0` is the exact staged emit phase using command `0x02`

After the staging / reconcile phases, the path turns into a packet emitter.

Exact keepable behavior:

- seeds exact pointer `12 = 1F80`
- walks candidate strip `1F00..1F1E`
  - for entries already present in live `1E20..`, it writes a paired word sequence into `1F80..` using the exact long table rooted at `C7:0BA4`
  - for entries not present, it duplicates the same value into the paired output stream
- then sends an exact block header through APU ports:
  - `$2143 = 0x1E`
  - `$2142 = 0x80`
  - `$2141 = 0x02`
- streams the exact `1F80..1FBF` paired output block through `$2141/$2142`
- sends two more exact command-`0x02` blocks rooted at:
  - `1F40..` using exact table `C7:0C20`
  - `1FC0..` using exact table `C7:0C9C`
- updates exact local byte `84` through repeated `JSR 09DA`
- normalizes `84` back to `0xE0` before the next phase

So the strongest safe reading is:

> `C7:037B..04B0` is the exact command-`0x02` emit phase of the negative-`1E05` special path, staging paired output blocks at `1F80..` and streaming them to the APU through `$2141/$2142/$2143`.

I am intentionally **not** claiming the final user-facing audio noun of each payload table yet.
But the exact staged-emitter shape is real now.

---

## What changed semantically
Before pass 95, the open seams still sounded like this:

```text
C2: more downstream token families
C7: active 0x10/11/14/15 path at 01A1
```

After pass 95, the safe wording is much tighter:

```text
C2: a chained three-family long-stream stage with exact counter-driven exits
C7: a negative-1E05 special path that rebuilds candidate slot strips,
    reconciles them against live slot state, and emits staged APU command traffic
```

That is not cosmetic. It closes two real structural gaps.

---

## Honest caution
I am still keeping a few things below frozen:

- the final gameplay-facing noun of the broader C2 stream language behind `58B2 / 5BF5 / 5C3E / 5C77`
- the exact semantic meaning of helpers `0734`, `0A39`, `0655`, and the later `04B1..061B` tail of the `01A1` path
- the first exact clean-code external reader of `CE0F`

But pass 95 absolutely moved the project forward:

- the three downstream C2 families are no longer anonymous
- the `01A1` path is no longer just “the active branch”
- the special-path sound/APU staging pipeline now has exact internal phase boundaries

---

## Best next seam
The cleanest next move now is:

1. **Finish the tail of the `01A1` special path**
   - `04B1..061B`
   - plus the helper at `0655`

2. **Tighten the helper pair called at the top of `01A1`**
   - `0734`
   - `0A39`

3. **Only then go back to `CE0F`**
