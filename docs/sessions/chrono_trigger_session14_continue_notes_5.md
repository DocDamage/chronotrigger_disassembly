# Chrono Trigger Disassembly — Continuation Notes After C3:8300..

## Scope completed
This continuation closed:

- `C3:8300..C3:8CFF`

That corresponds to:

- **passes 282 through 291**

## What actually happened
This continuation stayed in real mixed material the whole way.

Unlike the prior run, there was no giant zero-field lane to clear and no dramatic structural break.
Instead, this block was about handling a series of **plausible-looking but still non-defendable lures** across a fairly steady post-zero rebound stretch.

That matters because this kind of block is where label pollution gets easy:
- several pages look cleaner than the earlier dirty seam
- outside pressure is real in multiple places
- local return-anchored islands keep appearing
- tiny wrapper and landing-pad fragments keep making the pages feel more executable than they really are

The right move here was still the conservative one.

## Most important findings

### 1) `8500` was the strongest true external multi-hit false dawn of the continuation
This was the biggest seam temptation in the run.

`8500` received **three outside `JSR` hits**:
- `C3:0520 -> JSR $8500`
- `C3:38D9 -> JSR $8500`
- `C3:4368 -> JSR $8500`

That is real outside pressure.

And it still failed.

Why:
- two of the three callers are still dirty/high-risk
- the target-side bytes begin `DF 12 ED 30 00 ...`
- that byte lane still reads like packed mixed command/data material rather than a stable owner start

So `8500` is a textbook example of a page getting more interesting without actually becoming promotable.

### 2) `87A4..87AE` was the strongest local helper-like island of the continuation
This was the best unsupported local pocket in the run.

Why it mattered:
- best local-island score of the continuation
- low ASCII compared with the surrounding page
- branch activity plus one stack-ish setup byte
- clean `RTS` anchor

Why it still failed:
- there is no caller-backed true start defending it
- the surrounding page still contains noisier fragmented splinters and wrapper-like junk
- it still looks like an internal control pocket, not a real helper that owns itself

So it remains a splinter, not a promotable helper.

### 3) `88AD` was the cleanest-looking outside multi-hit lure in the block
This was the most honest near-miss of the continuation.

`88AD` received two outside `JSR` hits:
- `C3:09A5 -> JSR $88AD`
- `C3:0BE3 -> JSR $88AD`

The second caller is low-risk, and the target-side bytes grade low-risk too.
That is better than most of the seam.

And it still was not enough.

Why:
- the surrounding page remains mixed command/control material
- nearby branch-fed landing pads make the page look more structured than it really is
- the landing still does not defend a clean owner boundary the hard way

So `88AD` is probably the cleanest-looking outside multi-hit lure of this entire continuation, and still not safe to promote.

### 4) `8A00` was the busiest internal-control page of the run
`8A00..8AFF` matters for a different reason.

It did not produce the strongest outside pressure.
What it produced was the densest **local island cluster**:
- `8A10..8A26`
- multiple returns
- multiple branches
- repeated internal control behavior

That makes the page feel executable.

But the key truth is that it still feels executable **locally**, not as a caller-backed owner lane.
The page behaves more like a packed internal control pocket than a stable routine start area.

That distinction is exactly what kept this continuation clean.

### 5) `8BDB..8BDE = JSR $7C13 / RTS` was the best sanity-check wrapper in the block
This tiny wrapper matters because it points backward into a known fake lane:

- `8BDB..8BDE = JSR $7C13 / RTS`

And `7C13` was already proven earlier as one of the strongest zero-field false dawns, landing inside dead zero space.

So this tiny wrapper is useful structural confirmation:
- the old zero-field result still holds
- a neat-looking wrapper does not rehabilitate a dead target
- tiny wrappers can point into garbage and still be real wrappers

That is exactly why wrappers alone cannot own the target lane.

### 6) `8C80` was the cleanest late-block double-hit lure
The end of the continuation stayed interesting.

`8C80` took two outside `JSR` hits:
- `C3:065A -> JSR $8C80`
- `C3:071D -> JSR $8C80`

Both callers are low-risk, and the target side is only medium-risk.
That makes `8C80` the cleanest late-block outside double-hit lure of the run.

And it still failed because:
- the page still does not lock into a clean routine boundary
- nearby targets remain mixed and uneven
- the local pocket at `8C9F..8CA5` is still just a splinter, not support strong enough to rescue the page

## Current live seam now
- **`C3:8D00..`**

## Current completion estimate
- **~84.6%**

## No-BS state after this continuation
This was real progress.

But it was the slower kind of progress:
- no giant contaminated field to dismiss
- no routine breakthrough
- just a long run of plausible bait that still did not quite become code

That still matters.
This is exactly the stretch where a sloppy pass would start inventing owners out of cleaner-looking mixed pages.

The repo stayed clean instead.

## Recommended next move
Resume at:

- **`C3:8D00..`**

And keep the exact same standard:
1. reject multi-hit outside pressure unless the landing owns itself locally
2. reject strong local splinters unless a true caller-backed start exists
3. keep treating tiny wrappers and landing pads as supporting evidence only, never ownership by themselves
4. watch whether `8D00+` finally turns this steadier post-zero material into genuinely recoverable caller-backed code, or just continues the same mixed-control pattern

## Structural truths worth preserving
- `8500` is the strongest true external multi-hit false dawn of the continuation and still resolves as packed mixed command/data material
- `87A4..87AE` is the strongest local helper-like island of the continuation and still lacks a caller-backed true start
- `88AD` is the cleanest-looking outside multi-hit lure in the block and still does not defend a stable owner boundary
- `8A10..8A26` is the densest local-island cluster of the continuation and still behaves like internal control structure rather than owner-backed code
- `8BDB..8BDE = JSR $7C13 / RTS` is a tiny wrapper into the already-proven zero-field false dawn at `7C13`
- `8C80` is the cleanest late-block double-hit lure and still falls short of promotion

## Files produced in this continuation
- `chrono_trigger_c3_8300_8cff_raw_report.md`
- `chrono_trigger_session14_continue_notes_5.md`
