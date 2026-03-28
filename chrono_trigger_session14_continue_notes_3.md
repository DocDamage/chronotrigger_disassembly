# Chrono Trigger Disassembly — Continuation Notes After C3:6F00..

## Scope completed
This continuation closed:

- `C3:6F00..C3:78FF`

That corresponds to:

- **passes 262 through 271**

## What actually happened
The seam kept moving forward, but this stretch did **not** improve into a cleaner callable lane.

In fact, after the relatively lower-ASCII look of parts of the earlier run, this continuation swung back toward more obviously mixed and ASCII-heavy material across much of `7200..78FF`.

That matters because it killed several tempting lures the right way:
- a carried-over wrapper target at `6F50`
- a busier raw-xref page at `7000`
- the strongest outside multi-hit lure at `7420`
- the strongest local helper-like splinter at `771C..7734`

## Most important findings
### 1) `6F50` was a useful carry-over sanity check
From the prior continuation, `6697..669A` already looked like a tiny `JSR $6F50 / RTS` wrapper.

So `6F50` mattered immediately in this block.

It still failed to become a real owner because:
- it only had that carried-over wrapper-style support
- the target-side bytes never stabilized into a routine boundary
- the surrounding page stayed mixed rather than executable-looking in a durable way

That is exactly the kind of bait that can trick a continuation if the seam is evaluated too hopefully.

### 2) `7000` was the busiest raw-xref page of the continuation and still went nowhere
`7000..70FF` produced the most visible outside-call traffic in the block.

The catch:
- every visible landing was only single-hit outside pressure
- the cleaner target-side pockets still had dirty callers
- page-top bait at `7000` stayed high-risk on both sides

So the page looked busy, not trustworthy.

### 3) `7420` was the strongest true external multi-hit false dawn
This was the most important hard rejection in the continuation.

`7420` received two outside `JSR` hits:
- `C3:2E32 -> JSR $7420`
- `C3:4B6C -> JSR $7420`

That would be dangerous label-poison bait if accepted lazily.

It still fails instantly because:
- the landing byte at `7420` is `01`
- the page itself is heavily ASCII-contaminated
- the nearby local islands do not rescue it into a real owner boundary

So even the best outside pressure in the block still did not survive first contact with the bytes.

### 4) `724E` was the cleanest-looking single-hit outside lure on a dirty page
`724E` came from:
- `C3:A8C5 -> JSR $724E`

Caller risk stayed medium, target risk stayed low, which is better than most of the seam.

It still failed because the page around it is strongly ASCII-heavy mixed material. In other words, the landing looked cleaner than the neighborhood deserved.

That is a classic false-dawn pattern for this bank.

### 5) `771C..7734` was the strongest local helper-like island of the continuation
This was the best unsupported local pocket in the block:
- highest local-island score of the run
- multiple call opcodes
- multiple branch opcodes
- stack-ish setup bytes
- clean return anchor

And it still failed for the same reason the honest splinters keep failing:
- no caller-backed true start
- page-level ASCII contamination is extremely high
- the surrounding lane still reads as mixed material, not stable standalone code

So it remains a splinter, not a promotable helper.

## Current live seam now
- **`C3:7900..`**

## Current completion estimate
- **~84.2%**

## No-BS state after this continuation
This was still real progress.

But this block was **more about rejecting contaminated bait cleanly** than about discovering new executable territory.

The most important outcome is that the repo did not get polluted by:
- the carried-over `6F50` wrapper target
- the busy but weak `7000` page
- the double-`JSR` bait at `7420`
- the high-scoring but still contaminated local island at `771C..7734`

## Recommended next move
Resume at:

- **`C3:7900..`**

And keep the exact same standard:
1. reject page-top or interior-byte starts that land on obvious barrier/data-style bytes
2. reject single-hit cleanliness when the surrounding page is still mixed or ASCII-heavy
3. reject strong local splinters unless a real caller-backed start exists
4. watch whether `7900+` finally exits this dirtier mixed lane, or whether the seam is still in another long contaminated stretch

## Structural truths worth preserving
- `6F50` is the carried-over tiny-wrapper target from the prior block and still does not defend a real start
- `7000` is the busiest raw-xref page of this continuation and still has no defendable owner boundary
- `724E` is the cleanest-looking single-hit outside lure of the continuation and still resolves as false-dawn bait inside a dirty page
- `7420` is the strongest true external multi-hit false dawn of the continuation and dies immediately because the landing byte is `01`
- `771C..7734` is the strongest local helper-like island of the continuation and still lacks a caller-backed true start
- `78F0` is a late false landing that takes outside pressure and still lands on `FF`

## Files produced in this continuation
- `chrono_trigger_c3_6f00_78ff_raw_report.md`
- `chrono_trigger_session14_continue_notes_3.md`
