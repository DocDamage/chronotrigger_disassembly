# Chrono Trigger Disassembly — Continuation Notes After C3:AB00..

## Scope completed
This continuation closed:

- `C3:AB00..C3:B4FF`

That corresponds to:

- **passes 322 through 331**

## What actually happened
This continuation stayed in real mixed material the whole way through.

There was no giant zero-field to dismiss and no clean owner-rich breakout.
Instead, this block behaved like a **mixed-control stretch with several honest near-misses**, especially around `AD00`, `AE00`, `AF00`, and the late `B300` pages.

That matters because this is exactly where the seam starts looking more executable than it really is:
- there are real outside-call lures
- a few pages produce genuinely sharp local splinters
- several starts look cleaner than the earlier dirty seam
- and still none of it locks into one caller-backed owner/helper boundary

The right move here was still the conservative one.

## Most important findings

### 1) `AD21` plus `ADB9..ADCD` were the strongest early outside/local combination
The clearest early near-miss in the continuation was on `AD00`.

Outside pressure:
- `AD21` from `C3:6A66 -> JSR $AD21`
- caller risk = low
- target risk = low

Local structure:
- `ADB9..ADCD`
- score 6
- two calls
- three branches
- two returns
- lower ASCII than the surrounding lane

That is a real near-miss.

It still failed because:
- the clean outside pressure is still only single-hit
- nearby landings like `AD00` and `AD23` collapse onto bad starts (`00` and `02`)
- the page as a whole still behaves like mixed control/data rather than one defended start owning the lane

So `AD00` was the strongest early outside/local pairing of the run, not a breakthrough.

### 2) `AE00` and `AF48` were the main early outside multi-hit false dawns
The early continuation produced two actual multi-hit lures:

- `AE00` with 2 outside `JSR` hits
- `AF48` with 2 outside `JSR` hits

Both mattered because they looked like the seam might finally start consolidating.

They still failed for different reasons:
- `AE00` is still dragged down by dirty/high-risk caller context and a very mixed page
- `AF48` has the cleaner pairing, but the page around it still breaks up into splinters rather than one stable routine boundary

So both are real lures, but neither is honest ownership.

### 3) `AE03..AE10` and `AF57..AF60` showed how strong local splinters can still fail
This continuation had multiple good-looking local pockets:

- `AE03..AE10`
- `AF57..AF60`
- `AF4F..AF55`

These matter because they make the pages feel executable:
- strong branch density
- returns
- some stack-ish setup
- tighter byte lanes than the surrounding mess

And they still failed because:
- none of them are defended by a caller-backed true start
- the pages around them remain mixed and uneven
- they still behave like internal splinters, not recoverable helper/owner starts

So the continuation kept producing sharper local structure without actually crossing the line into promotion.

### 4) `B000` and `B100` were useful sanity-check pages
These two pages mattered for opposite reasons.

`B000` produced:
- one neat low-ASCII local pocket at `B067..B074`
- but only weak outside pressure, and the cleanest outside lure still targeted high-risk bytes

`B100` produced:
- cross-bank attention at `B131`
- one busy local cluster at `B147..B159`
- but also obvious bad-start bait like `B101` landing on `00` and `B170` landing on `09`

Together, they were a good reminder that:
- interesting outside hits do not equal ownership
- nice local islands do not equal ownership
- cross-bank attention does not equal ownership

### 5) `B3BF..B3D7` was the strongest late local island cluster
The best late-block local structure showed up on `B300`:

- `B3BF..B3D7`
- score 5
- one call
- one branch
- one return
- one stack-ish setup byte

It still failed because:
- the outside lures on the page are only middling single hits
- the broader page remains branch-fed and fragmented
- no caller-backed true start actually owns the cluster

So `B300` felt more structured than many earlier pages, but still not honestly promotable.

### 6) `B409 / B414` were the cleanest late single-hit outside lures
The continuation cooled off at `B400`, but it still produced two decent late landings:

- `B409` from `C3:BC42 -> JSR $B409`
- `B414` from `C3:600C -> JSR $B414`

Both were medium/low pairings, which is better than most of the seam.

They still failed because:
- each is still only a single outside hit
- the page offers almost no local support
- there is no stable byte-level boundary around either start that would justify promotion

So `B400` ended as another near-miss page, not an owner lane.

## Current live seam now
- **`C3:B500..`**

## Current completion estimate
- **~85.4%**

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

- **`C3:B500..`**

And keep the same standard:
1. reject outside multi-hit pressure unless one landing really owns itself locally
2. reject clean single hits unless the page around them also stabilizes
3. reject strong local splinters unless a caller-backed true start actually steps forward
4. watch whether `B500+` finally turns this rebound stretch into genuinely recoverable caller-backed code, or whether it keeps producing the same mixed-control near-misses

## Structural truths worth preserving
- `AD21` is the cleanest early outside lure of the continuation, and `ADB9..ADCD` is the strongest early local island; the combination still does not defend a real start
- `AE00` and `AF48` are the main early outside multi-hit false dawns of the continuation
- `AE03..AE10`, `AF57..AF60`, and `AF4F..AF55` are strong local splinters that still lack caller-backed ownership
- `B067..B074` is a neat low-ASCII local pocket with no real outside traction
- `B131` brings cross-bank attention without producing a defendable owner boundary
- `B3BF..B3D7` is the strongest late local island cluster of the continuation and still cannot be promoted honestly
- `B409` and `B414` are the cleanest late single-hit outside lures of the run and still remain only near-misses
- `B4A9` is a tiny `RTL` stub at the tail of the last page, not a promoted wrapper target

## Files produced in this continuation
- `chrono_trigger_c3_ab00_b4ff_raw_report.md`
- `chrono_trigger_session14_continue_notes_9.md`
