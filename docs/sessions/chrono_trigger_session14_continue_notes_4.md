# Chrono Trigger Disassembly — Continuation Notes After C3:7900..

## Scope completed
This continuation closed:

- `C3:7900..C3:82FF`

That corresponds to:

- **passes 272 through 281**

## What actually happened
This continuation split cleanly into two very different halves:

1. `7900` begins as another dirty mixed page
2. `7A00..7FFF` then collapses into an overwhelmingly zero-filled field
3. `8000..82FF` finally returns to more plausible mixed command/control material

That matters because this run was not mainly about finding hidden code.
It was about **proving that a long stretch of raw-caller pressure was fake because it landed inside dead zero space**, and then handling the first post-zero rebound pages without getting baited into bad promotions.

## Most important findings

### 1) `7A00..7FFF` is the structural truth of this continuation
The most important thing this block established is simple:

- `7A00..7FFF` is overwhelmingly zero-filled territory

The page metrics make that plain:
- `7A00` is already 84% zero with extreme repeated-pair suspicion
- `7B00..7FFF` are effectively full zero pages

That means the many raw xrefs landing into this range are not hidden callable code.
They are **false landings into dead zero space**.

### 2) `7C13` was the strongest zero-field multi-hit false dawn
If there was one place this continuation could have gone wrong, it was here.

`7C13` received **five outside `JSR` hits**:
- `C3:8BDB`
- `C3:9827`
- `C3:9FAF`
- `C3:BFCB`
- `C3:C850`

That is real pressure.
And it still means nothing here, because:
- the page is all zeros
- the landing byte is `00`
- the whole neighborhood is dead zero-fill

So `7C13` is the best example in this continuation of why caller density alone cannot own a region.

### 3) `7E4E` and `7F8C` proved the zero-field contamination was broad, not isolated
The block did not just have one bad landing.
It repeated the same pattern across multiple pages:

- `7E4E` with 4 outside `JSR` hits
- `7F8C` with 3 outside `JSR` hits

Both still land inside fully zeroed pages.

That confirms this was not one suspicious pocket.
It was a broader zero-filled lane with widespread raw-caller contamination.

### 4) `8000` was the first real post-zero rebound page
This is the most important seam-development fact after the zero field.

`8000..80FF` is the first page that looks like actual mixed material again.

The strongest lure there was:
- `800C` with 8 outside `JSR` hits

The cleanest-looking lure there was:
- `8089` with 3 hits, best from `C3:1B1D -> JSR $8089`
- caller risk = low
- target risk = low

That is the best-looking single outside lure of this whole continuation.

And it still was not enough.

Why:
- the page still starts on `RTS`
- nearby targets like `8034` still collapse onto `00`
- the whole page still reads more like packed mixed command/control material than a clean owner-backed routine lane

So `8000` is real progress, but not a promotion breakthrough.

### 5) `8207` and `82E0..82EE` were the late-block temptations
The late continuation gave two meaningful temptations:

- `8207` with two outside `JSL` hits from `E5:8EA7` and `EC:3F40`
- `82E0..82EE` as the strongest local island of the run

Those matter because they are the first late-block signs that the post-zero seam may be getting somewhat more structured again.

They still fail for different reasons:
- `8207` still does not sit on a defendable owner boundary
- `8278` nearby is an obvious false landing because it starts on `02`
- `82E0..82EE` is still just a local splinter, not a caller-backed true start

## Current live seam now
- **`C3:8300..`**

## Current completion estimate
- **~84.4%**

## No-BS state after this continuation
This was real progress.

But the progress was mostly **structural cleanup**:
- prove the zero field is really a zero field
- reject the xref contamination honestly
- then test the first rebound pages without forcing routines

That is exactly the kind of pass that keeps the repo from getting poisoned by bad owners.

## Recommended next move
Resume at:

- **`C3:8300..`**

And keep the same standard:
1. treat `7A00..7FFF` as established zero-field / non-owner territory unless some very unusual contrary evidence appears
2. inspect whether `8300+` continues the post-zero rebound into genuinely structured caller-backed code
3. reject page-top and interior-byte starts that still land on barrier/data-style bytes
4. reject local splinters unless a true caller-backed start actually defends them

## Structural truths worth preserving
- `7A00..7FFF` is overwhelmingly zero-filled territory, not hidden callable code
- `7C13` is the strongest zero-field multi-hit false dawn of the continuation and still lands on `00`
- `7E4E` and `7F8C` confirm the zero-field contamination is broad across the lane
- `8000` is the first real post-zero rebound page
- `800C` is the strongest true external multi-hit lure after the zero field
- `8089` is the cleanest-looking outside lure of the continuation and still does not defend a stable owner boundary
- `8207` is the strongest late outside multi-hit lure
- `82E0..82EE` is the strongest local island of the continuation and still lacks a caller-backed true start

## Files produced in this continuation
- `chrono_trigger_c3_7900_82ff_raw_report.md`
- `chrono_trigger_session14_continue_notes_4.md`
