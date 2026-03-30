# Chrono Trigger Disassembly — Continuation Notes After C3:A100..

## Scope completed
This continuation closed:

- `C3:A100..C3:AAFF`

That corresponds to:

- **passes 312 through 321**

## What actually happened
This continuation stayed in real mixed material the whole way through.

There was no giant contaminated zero-field to dismiss and no routine-rich breakout.
Instead, this block behaved like a long **mixed-control rebound stretch with several cleaner-looking near-misses**.

That matters because this is exactly the kind of run where the seam starts feeling more executable than it really is:
- several pages carry real outside pressure
- some single-hit landings are legitimately clean
- local return-anchored splinters keep getting sharper
- and still none of it quite lines up into a caller-backed owner/helper start

The right move here was still the conservative one.

## Most important findings

### 1) `A28B` and `A28A` were the strongest early outside-call temptations
`A200` was the busiest outside-call page of the continuation.

The strongest raw lure was:
- `A28B` with 3 outside `JSR` hits

The cleaner paired lure on the same page was:
- `A28A` with 2 outside `JSR` hits
- best pairings medium/medium and low/medium

That made `A200` the most tempting early page in the run.

It still failed because:
- the page is still fairly ASCII-heavy and structurally mixed
- the landings sit inside wider packed material rather than a stable routine boundary
- no local island steps forward to rescue ownership

So `A200` was busy, not trustworthy.

### 2) `A3A5 / A3B8` were the cleanest single outside lures of the continuation
The cleanest outside landings in the whole block showed up on `A300`:
- `A3A5` from `C3:6CD1 -> JSR $A3A5`
- `A3B8` from `C3:6864 -> JSR $A3B8`
- `A3BD` from `C3:6867 -> JSR $A3BD`

Those are real near-misses.

And they still failed because:
- each landing is still only single-hit support
- the page remains mixed and branch-fed overall
- the cleanest local pockets are still just splinters, not caller-backed starts

So `A300` was the best single-hit outside-call page of the run, not a code breakthrough.

### 3) `A521` was the first true outside multi-hit lure after the early rebound pages
`A500` was the first page in this continuation where the seam felt like it might start consolidating.

The key lure there was:
- `A521` with 2 outside `JSR` hits

It still failed because:
- one caller is low/high and the other is high/medium
- the landing bytes do not defend a stable start
- the page offers almost no local support strong enough to matter

So `A521` is a real multi-hit lure, but still not one you can promote honestly.

### 4) `A847..A855` was the strongest local helper-like island of the continuation
This was the best local-structure temptation in the whole block.

Why it mattered:
- best local island score of the continuation
- two call opcodes
- two branches
- stack-ish setup
- two returns
- a tighter byte lane than most of the surrounding pages

It still failed because:
- the outside support on the page is still only single-hit
- the cleanest outside lure, `A8A2`, still lands on a `03` start and never becomes a defended true boundary
- the page remains mixed and uneven outside the splinter

So `A847..A855` is the strongest local helper-like false dawn of this continuation.

### 5) `A900` was the busiest late dirty page of the continuation
The late block turned noisy again.

The strongest lure there was:
- `A90B` with 3 outside `JSR` hits

The next one was:
- `A960` with 2 outside `JSR` hits

And it still all failed because:
- target-side bytes stay high-risk
- `A905` shows how bad the page is by landing directly on `00`
- the only surviving local island is tiny and worthless as ownership support

So `A900` is a good reminder that raw xref density still means nothing if the landings are bad.

### 6) `AAA0` was the cleanest late single-hit lure
The continuation cooled off at `AA00`, but it still produced one moderately clean landing:
- `AAA0` from `C3:5B14 -> JSR $AAA0`
- caller risk = medium
- target risk = medium

That is the cleanest late-block landing in the continuation.

It still failed because:
- it is still only single-hit support
- the page’s other visible lures are all high/high junk
- the only local support is a tiny late pocket ending on an `RTL` stub at `AAA2`

So `AA00` ends as another near-miss page, not a promotable owner lane.

## Current live seam now
- **`C3:AB00..`**

## Current completion estimate
- **~85.2%**

## No-BS state after this continuation
This was real progress.

But it was still the slow, disciplined kind:
- no giant structural cleanup
- no promotion breakthrough
- just another long stretch where the seam kept producing interesting bait that still did not hold up end-to-end

That still matters.
This is exactly the kind of continuation where conservative review keeps the repo from filling up with fake helpers and fake owners.

## Recommended next move
Resume at:

- **`C3:AB00..`**

And keep the same standard:
1. reject busy outside-call pages unless one landing actually owns itself locally
2. reject clean single hits unless the page around them also stabilizes
3. reject strong local splinters unless a caller-backed true start really steps forward
4. watch whether `AB00+` finally turns this rebound stretch into genuinely recoverable caller-backed code, or whether it keeps producing the same mixed-control near-misses

## Structural truths worth preserving
- `A28B` is the strongest raw outside multi-hit false dawn of the continuation, while `A28A` is the cleaner paired lure on the same page
- `A3A5 / A3B8 / A3BD` are the cleanest single outside lures of the run and still remain only near-misses
- `A521` is the first true outside multi-hit lure after the early rebound pages and still does not defend a stable boundary
- `A847..A855` is the strongest local helper-like island of the continuation and still lacks caller-backed ownership
- `A8A2` is the cleanest outside lure on the same page and still lands on a weak `03` start
- `A90B` is the busiest late outside-call lure of the continuation and still resolves as dirty false pressure
- `AAA0` is the cleanest late single-hit landing of the run and still falls short of promotion
- `AAA2` is a tiny `RTL` stub at the tail of the last page, not a promoted wrapper target

## Files produced in this continuation
- `chrono_trigger_c3_a100_aaff_raw_report.md`
- `chrono_trigger_session14_continue_notes_8.md`
