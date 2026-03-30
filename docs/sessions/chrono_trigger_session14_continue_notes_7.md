# Chrono Trigger Disassembly — Continuation Notes After C3:9700..

## Scope completed
This continuation closed:

- `C3:9700..C3:A0FF`

That corresponds to:

- **passes 302 through 311**

## What actually happened
This continuation stayed in real mixed material the whole way through.

There was no giant zero-field to dismiss and no sudden routine-rich breakout.
Instead, this block behaved like a long **post-zero mixed-control stretch with several cleaner-looking near-misses**.

That matters because this is exactly the kind of run where a sloppy pass starts inventing code just because the pages feel more structured than the uglier seam behind them.

The right move here was still the conservative one.

## Most important findings

### 1) `97B5` plus `97B1..97C9` were the strongest early outside/local combination
The most interesting early page was `9700`.

Outside pressure:
- `97B5` from `C3:64CB -> JSR $97B5`
- caller risk = low
- target risk = low

Local structure:
- `97B1..97C9`
- strongest local island on the page
- score 7
- low-ish ASCII
- two calls, three branches, one return, two stack-ish setup bytes

That is a real near-miss.

And it still failed because:
- the outside pressure is still only single-hit
- the local island does not get defended by a caller-backed true start
- the page as a whole still reads like mixed control material rather than one routine owning itself cleanly

So `9700` was the strongest early near-miss of the continuation, not a breakthrough.

### 2) `9900` was the first true outside multi-hit false dawn of the block
`9900` received two outside `JSR` hits:
- `C3:627D -> JSR $9900`
- `C3:6C91 -> JSR $9900`

That makes it the first real multi-hit lure in the continuation.

It still failed because:
- the landing byte is `09`
- target-side bytes still grade high-risk
- the page’s local structure never resolves into a defendable owner boundary

So it is real pressure, but still not honest ownership.

### 3) `9B80` and `9B76..9B80` were the best mid-block outside/local pairing
The cleanest mid-block combination showed up in `9B00`.

Outside pressure:
- `9B80` from `C3:6671 -> JMP $9B80`
- caller risk = low
- target risk = medium

Local structure:
- `9B76..9B80`
- score 5
- two calls, one branch, one return, one stack-ish byte

That is a good pairing.

It still failed because:
- there is still only one outside landing
- the local pocket stays just a splinter instead of a defended start
- the wider page remains mixed and branch-fed

So `9B00` felt promising, but still did not earn promotion honestly.

### 4) `9E1C` was the cleanest single outside lure in the whole continuation
This was probably the cleanest single caller-backed landing in the run:
- `9E1C` from `C3:4510 -> JSR $9E1C`
- caller risk = low
- target risk = low

That is better than most of the seam.

And it still was not enough.

Why:
- it is still only a single outside hit
- the page around it stays mixed and branch-fed
- the strong support on the page comes from local control behavior, not a defendable owner boundary

So `9E1C` is a great example of why “clean single hit” still is not the same thing as promotable code.

### 5) `9C00` was a useful sanity-check false-dawn page
`9C00..9CFF` mattered for the opposite reason.

It looked busy, but the busyness was trashy:
- `9C00` got two outside `JSR` hits and still landed on `00`
- `9C2C` and `9C18` were both dirty on caller and target side
- the page only produced noisy internal pockets, not a defendable start

That makes `9C00` a good reminder that raw xref density still means nothing if the landings are bad.

### 6) `A03D` was the cleanest late-block outside multi-hit lure
The late continuation ended with the strongest outside-call page of the run.

The most important target there was:
- `A03D` with 2 outside hits
  - `C3:68BB -> JSR $A03D`
  - `C3:6963 -> JMP $A03D`

That is the cleanest late-block outside multi-hit lure in the continuation.

It still failed because:
- target-side bytes only hold up as medium-risk
- the page still contains nearby bad-start bait like `A05A` landing on `01`
- the strongest local pocket at `A0ED..A0FB` is still a late splinter, not support strong enough to rescue ownership

So `A000` ended active and interesting, but still not owner-worthy.

## Current live seam now
- **`C3:A100..`**

## Current completion estimate
- **~85.0%**

## No-BS state after this continuation
This was real progress.

But it was the slow, disciplined kind again:
- several pages looked cleaner
- a few outside-call targets looked legitimately interesting
- multiple local islands looked sharper than the earlier seam
- and still none of it quite crossed the line into a defendable owner/helper promotion

That still matters.
This is exactly where conservative review keeps the repo clean.

## Recommended next move
Resume at:

- **`C3:A100..`**

And keep the same standard:
1. reject clean single outside hits unless the landing also owns itself locally
2. reject multi-hit outside pressure unless the start is truly defendable at the byte level
3. reject strong local splinters unless a caller-backed true start actually steps forward
4. watch whether `A100+` finally turns this steadier post-zero rebound into genuinely recoverable caller-backed code, or whether it keeps producing the same mixed-control near-misses

## Structural truths worth preserving
- `97B5` is the cleanest early outside lure of the continuation, and `97B1..97C9` is the strongest early local island; the combination still does not defend a real start
- `9900` is the first true outside multi-hit false dawn of the continuation and still fails on byte-level boundary quality
- `9B80` plus `9B76..9B80` form the best mid-block outside/local pairing and still do not justify promotion
- `9C00` is a busy dirty false-dawn page whose multi-hit pressure still lands on `00`
- `9E1C` is the cleanest single outside lure in the continuation and still remains only a near-miss
- `A03D` is the cleanest late-block outside multi-hit lure of the run and still falls short of a defendable owner boundary
- `A0ED..A0FB` is the strongest late local splinter of the continuation and still lacks caller-backed ownership

## Files produced in this continuation
- `chrono_trigger_c3_9700_a0ff_raw_report.md`
- `chrono_trigger_session14_continue_notes_7.md`
