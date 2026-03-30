# Chrono Trigger Disassembly — Continuation Notes After C3:B500..

## Scope completed
This continuation closed:

- `C3:B500..C3:BEFF`

That corresponds to:

- **passes 332 through 341**

## What actually happened
This continuation stayed in real mixed material the whole way through.

There was no giant zero-field to dismiss and no clean owner-rich breakout.
Instead, this block behaved like a **mixed-control stretch with a few honest near-misses and several strong local splinters**.

That matters because this is exactly the kind of continuation where the seam feels “almost there”:
- a couple of outside-call targets look cleaner than usual
- several pages produce strong return-anchored local pockets
- some starts look better than the ugly mixed seam behind them
- and still none of it locks into one caller-backed owner/helper boundary

The right move here was still the conservative one.

## Most important findings

### 1) `B574` was the strongest early outside multi-hit false dawn
The first real temptation in the block came right away.

`B574` received two outside `JSR` hits:
- `C3:2E33 -> JSR $B574`
- `C3:552E -> JSR $B574`

That looks useful until you inspect the landing byte.
It lands directly on:

- `60` (`RTS`)

So this is classic return-stub bait, not a defendable owner start.

That makes `B500` a good early sanity-check page:
real outside pressure can still be completely fake if the landing byte kills it instantly.

### 2) `B769..B772` and especially `B994..B9AC` were the strongest early pure local-control splinters
The early-middle continuation produced its best structure without much outside traction.

`B700` mattered because it had **no outside callers at all**, but still produced:
- `B769..B772`
- `B7A2..B7AF`
- `B7A2..B7B8`

That made it the strongest pure local-control page of the early continuation.

Then `B900` went a step further and produced:
- `B994..B9AC`
- `B979..B991`
- `B986..B99E`

These are strong internal-control splinters.
They still failed for the same reason the honest local pockets keep failing:
- no caller-backed true start
- no outside pressure that actually owns the page
- the structure remains local, not externally defended

So `B900` was structurally interesting, not promotable.

### 3) `BBDA` was the cleanest single outside lure of the continuation
The cleanest single outside landing in the whole block was:

- `BBDA` from `C3:0A01 -> JSR $BBDA`
- caller risk = low
- target risk = low

That is better than most of the seam.

And it still was not enough.

Why:
- it is still only single-hit support
- the page’s most obvious local structure is a noisy early return cluster around `BB04..BB15`
- the wider page still does not stabilize into one clear owner boundary

So `BB00` gave the continuation its cleanest single outside lure and still stayed only a near-miss.

### 4) `BC5C..BC74` was the strongest late local island of the run
The best late local splinter in the continuation showed up on `BC00`:

- `BC5C..BC74`
- score 5
- very low ASCII
- heavy branch density
- return anchor
- multiple stack-ish setup bytes

That is exactly the kind of local island that can fool a sloppy pass into inventing a helper.

It still failed because:
- the only outside pressure on the page is a dirty single hit at `BC1B`
- no caller-backed true start steps forward and owns the splinter
- the page around it still behaves like mixed control, not a recoverable helper lane

So `BC00` was the strongest late local page of the continuation, not a promotion breakthrough.

### 5) `BD12` and the late-page cluster were the cleanest late outside/local near-miss
The late continuation ended with the most balanced outside/local combination on `BD00`.

Outside pressure:
- `BD12` from `C3:389B -> JSR $BD12`
- caller risk = medium
- target risk = medium

Local structure:
- `BDE7..BDF2`
- `BDE7..BDEE`

That is a legitimate near-miss combination.

And it still failed because:
- the cleanest outside hit is still only single-hit
- the page also contains worse false-dawn bait like `BD00` landing on `30` and `BD88` with high/high risk
- the strongest local support is still a tail cluster, not a caller-backed start

So `BD00` ended as the cleanest late outside/local near-miss of the run, still short of honest promotion.

### 6) `BE00` proved the block still had no real breakout
`BE00` is useful because it keeps the continuation honest.

It looks active:
- dirty outside pressure at `BEA2` and `BEF0`
- several local return-anchored pockets
- lots of surface-level motion

But it is still:
- ASCII-heavy
- caller-dirty
- structurally uneven

So the block did not secretly turn the corner at the end.
It stayed mixed.

## Current live seam now
- **`C3:BF00..`**

## Current completion estimate
- **~85.6%**

## No-BS state after this continuation
This was real progress.

But it was still the slow, disciplined kind:
- no giant structural cleanup
- no promotion breakthrough
- just another long stretch where the seam produced a few clean near-misses and several good local splinters that still did not hold up end-to-end

That still matters.
This is exactly where conservative review keeps the repo from filling up with fake helpers and fake owners.

## Recommended next move
Resume at:

- **`C3:BF00..`**

And keep the same standard:
1. reject outside multi-hit pressure unless one landing really owns itself locally
2. reject clean single hits unless the page around them also stabilizes
3. reject strong local splinters unless a caller-backed true start actually steps forward
4. watch whether `BF00+` finally turns this rebound stretch into genuinely recoverable caller-backed code, or whether it keeps producing the same mixed-control near-misses

## Structural truths worth preserving
- `B574` is the strongest early outside multi-hit false dawn of the continuation and still dies immediately on `RTS`
- `B769..B772` and `B994..B9AC` are the strongest early pure local-control splinters and still lack caller-backed ownership
- `BBDA` is the cleanest single outside lure of the continuation and still remains only a near-miss
- `BC5C..BC74` is the strongest late local island of the run and still cannot be promoted honestly
- `BD12` is the cleanest late outside lure, while `BDE7..BDF2` is the strongest late local support; the combination still does not defend a real start
- `BE00` stays ASCII-heavy and caller-dirty despite its local motion
- `B6EF`, `BAB9`, `AC2A`, `AC35`, and `B4A9` remain examples of how tiny `RTL` stubs and landing pads can make these pages feel more executable than they really are

## Files produced in this continuation
- `chrono_trigger_c3_b500_beff_raw_report.md`
- `chrono_trigger_session14_continue_notes_10.md`
