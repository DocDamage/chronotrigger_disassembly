# Chrono Trigger Disassembly — Continuation Notes After C3:6500..

## Scope completed
This continuation closed:

- `C3:6500..C3:6EFF`

That corresponds to:

- **passes 252 through 261**

## What actually happened
The seam kept moving forward, but it still did **not** break into a clean owner-rich lane.

This block was more interesting than the immediately preceding one because it produced:
- the strongest local helper-like island of the continuation at `6641..6649`
- the busiest xref page of the run at `6A00`
- a late double-`JSR` false dawn at `6E1B`

Even with those temptations, the same rule held:
- raw outside pressure is not enough
- cleaner page metrics are not enough
- local return-anchored splinters are not enough
- a page only becomes recoverable code when caller quality and local structure agree at the same true start

## Most important findings
### 1) `66B0` was the strongest true external multi-hit lure early in the block
`66B0` took two outside `JSR` hits:
- `C3:3B44 -> JSR $66B0`
- `C3:577B -> JSR $66B0`

That sounds good until you look at the caller side.

Both callers still grade high-risk, and the landing is still embedded inside a wider mixed page.
So it stays a false dawn.

### 2) `6641..6649` was the strongest local helper-like island of the continuation
This was the best unsupported local pocket of the whole run:
- low-ish ASCII
- one call opcode
- one branch opcode
- clean `RTS` anchor
- highest local-island score in the continuation

It still failed because there is no caller-backed true start defending it as a real helper/owner.
It is still a splinter, not a stable routine boundary.

### 3) `6A00` was the busiest page of the continuation
This page matters because it looked more executable than most of the surrounding block.

The cleanest-looking outside callable lures were:
- `6A95` from `C3:89E8 -> JMP $6A95`
- `6AAB` from `C3:3FBA -> JSR $6AAB`

Both were medium-risk caller / low-risk target combinations.

That is better than most of the seam.

And it still was not enough.
The page stayed mixed and xref-busy, with nearby landings like `6A45` starting on `02`, and the full page still reading more like packed command/control material than a defendable callable lane.

### 4) `6D00` proved the block had not really turned the corner
`6D00` is the clearest reminder not to overread the cleaner pages around it.

Metrics there spike hard:
- very high ASCII
- elevated zero density
- elevated repeated-pair suspicion

So even though the continuation had cleaner-looking pages around `6800`, `6A00`, and `6C00`, the underlying seam still had obvious mixed-content contamination.

### 5) `6E1B` was the strongest late-block false dawn
`6E1B` received two outside `JSR` hits:
- `C3:DB25 -> JSR $6E1B`
- `C3:DC78 -> JSR $6E1B`

That made it the strongest late-block lure.

It still failed because:
- both callers are high-risk
- the landing still does not sit on a defendable owner boundary
- the page produced no strong supporting local island to rescue it

## Current live seam now
- **`C3:6F00..`**

## Current completion estimate
- **~84.0%**

## No-BS state after this continuation
This was still real progress.

But again, it was **cleanup progress**, not a code-promotion breakthrough.

The main gain is that the project pushed ten more pages forward while keeping the label space clean.
That matters because pages like `66B0`, `6A95`, `6AAB`, and `6E1B` are exactly the kind of bait that can poison the repo if the standard gets sloppy.

## Recommended next move
Resume at:

- **`C3:6F00..`**

And keep the same conservative workflow:
1. reject single-hit cleanliness unless the local start also stabilizes
2. reject multi-hit landings when the callers stay dirty
3. reject strong local islands unless a true caller-backed start exists
4. watch whether `6F00+` becomes a genuinely better caller-backed lane, or just another low-ASCII mirage

## Structural truths worth preserving
- `66B0` is the strongest true external multi-hit false dawn early in this continuation and still does not own itself
- `6641..6649` is the strongest local helper-like island of the continuation and still lacks a caller-backed true start
- `6A00` is the busiest xref page of the continuation and still resolves as mixed command/control material rather than stable code
- `6A45` is an obvious false landing because it starts on `02`
- `6D00` is heavily contaminated and should not be mistaken for a code breakout
- `6E1B` is the strongest late-block multi-hit false dawn and still fails ownership

## Files produced in this continuation
- `chrono_trigger_c3_6500_6eff_raw_report.md`
- `chrono_trigger_session14_continue_notes_2.md`
