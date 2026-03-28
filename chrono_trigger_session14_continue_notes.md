# Chrono Trigger Disassembly — Continuation Notes After Session 13

## Scope completed
This continuation closed:

- `C3:5B00..C3:64FF`

That corresponds to:

- **passes 242 through 251**

## What actually happened
The seam kept moving forward honestly, but it did **not** suddenly break into a clean routine-rich lane.

This ten-page stretch stayed mostly consistent with the session-13 truth:
- mixed command/table/control material can still throw off strong-looking raw callers
- low-ascii pages are not automatically code pages
- interior-byte landings can still look great on the caller side and still fail instantly on local structure
- short return-anchored splinters can exist without earning owner or helper promotion

## Most important findings
### 1) `5E3C` was the strongest early-block false dawn
`5E3C` took two outside `JSR` hits and looked like the next plausible owner candidate early in the run.

It still failed because:
- caller quality stayed dirty/high-risk
- the landing sits inside a wider mixed command-style lane
- the surrounding page never stabilized into a defendable routine boundary

### 2) `60AB` was the strongest true external multi-hit lure of the continuation
This is the most important seam fact in the block.

`60AB` received **two low-risk outside `JSR` callers**:
- `C3:30BC -> JSR $60AB`
- `C3:591D -> JSR $60AB`

That looks good on paper.

It still dies immediately because the first landing byte at `60AB` is **`02`**, which makes it barrier-style garbage as a callable owner start.

So this page is a perfect example of why caller support alone is not enough.

### 3) `6010` was the next-cleanest outside-call lure
`6010` took:
- `C3:2F41 -> JSR $6010`
- `C3:68CE -> JMP $6010`

That is real outside pressure.

It still did not survive because the local byte lane around the landing still reads like packed command/table material instead of a stable routine boundary.

### 4) `6334..6345` was the strongest local island of the run
This block finally produced the best unsupported local helper-like splinter since the session-13 seam:
- `C3:6334..C3:6345`

Why it mattered:
- strongest island score in the continuation
- low ascii
- one call opcode plus multiple branch opcodes
- clear return anchor

Why it still failed:
- it is still embedded inside a wider mixed page
- no caller-backed true start defends it cleanly
- promoting it would still overclaim ownership

### 5) `6400` stayed tempting without becoming real code
The late block produced several outside lures:
- `64AD`
- `64CA`
- `64DD`

But:
- `64CA` starts on `02`
- the page still contains mixed material around the tempting splinters
- the code-looking pocket around `6430..643F` never became a defendable owner boundary

## Current live seam now
- **`C3:6500..`**

## Current completion estimate
- **~83.8%**

## No-BS state after this continuation
This was real progress.

But it was **cleanup progress**, not a code-promotion breakthrough.

The seam is getting somewhat less ASCII-heavy in places from `5F00` onward, but the block is still full of mixed command/table/control structure. The cleanest outside-call lures still keep landing on bad starts, interior bytes, or tiny return stubs.

That means the standard held.

## Recommended next move
Resume at:

- **`C3:6500..`**

And keep doing the same thing:
1. prefer raw-caller plus local-structure agreement over wishful pattern matching
2. reject interior-byte starts even when outside callers look unusually clean
3. watch for whether the lower-ascii feel from `5F00..64FF` turns into real routine boundaries at `6500+`, or whether it stays another mixed-control mirage

## Structural truths worth preserving
- `60AB` is the strongest true external multi-hit false dawn of this continuation and still fails immediately because the landing byte is `02`
- `6010` is the next-cleanest outside-call lure and still resolves as mixed command/table material
- `62D1` is a one-hit `JSR` landing directly on `RTS`, making it classic return-stub bait
- `6334..6345` is the strongest local helper-like island of the continuation and still does not defend a real owner/helper start
- `6400` contains tempting internal splinters but still does not own itself as code

## Files produced in this continuation
- `chrono_trigger_c3_5b00_64ff_raw_report.md`
- `chrono_trigger_session14_continue_notes.md`
