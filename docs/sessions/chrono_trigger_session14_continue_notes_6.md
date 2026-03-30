# Chrono Trigger Disassembly — Continuation Notes After C3:8D00..

## Scope completed
This continuation closed:

- `C3:8D00..C3:96FF`

That corresponds to:

- **passes 292 through 301**

## What actually happened
This continuation stayed in real mixed material all the way through.

There was no giant zero-field to clear and no sudden owner-rich breakout.
Instead, this block behaved like a long **mixed-control seam with recurring outside-call bait plus increasingly convincing local splinters**.

That matters because this is exactly the kind of stretch where sloppy review starts inventing helpers and owners that the bytes do not really support.

The right move here was still the conservative one.

## Most important findings

### 1) `8D80` was the cleanest early double-hit outside lure
The first important seam temptation came right away.

`8D80` received two outside `JSR` hits:
- `C3:07DF -> JSR $8D80`
- `C3:08A1 -> JSR $8D80`

That made it the cleanest early outside multi-hit target of the continuation.

It still failed because:
- target-side bytes only held up as medium-risk, not truly clean
- the surrounding page never stabilized into a defendable routine boundary
- the page had no supporting local island strong enough to rescue ownership

So it stayed a real lure, not a promotable start.

### 2) `9000` was the busiest outside-call page of the continuation
`9000..90FF` was the most xref-active page in the whole run.

The strongest lure there was:
- `90A7` with 2 outside `JSR` hits

The page also carried multiple additional outside landings:
- `9000`
- `90FC`
- `9079`
- `90AA`
- `90AD`

That made it feel executable.

And it still failed for the same old reason:
- caller pressure existed, but the landings were still uneven
- the page stayed visibly mixed
- the best support was still page-level busyness rather than one clean owner-backed start

So `9000` was active, not trustworthy.

### 3) `9199..91B1` and `91E0..91F7` were the strongest internal-control cluster of the continuation
`9100..91FF` was the most important page in the block from a local-structure point of view.

It barely had any outside-call support.
But it produced the strongest cluster of local islands:
- `9199..91B1`
- `91E0..91F7`

That combination matters because it makes the page look more executable than almost anything around it.

Why it still failed:
- the page’s structure is mostly self-contained
- the outside-call support is too thin and too weak
- no caller-backed true start steps forward and owns the cluster

So this was a strong internal-control page, not a recoverable owner/helper page.

### 4) `9200` and `9400` were good sanity-check pages
These two pages were useful for opposite reasons.

`9200` mattered because:
- no outside callable landings survived into it
- no local islands survived strongly enough either

So it is a clean reminder that some of this seam is just mixed command/control material with no traction at all.

`9400` mattered because:
- it had no outside-call support
- but it still produced one very clean local pocket at `94BA..94C4`

That is a useful sanity check:
a neat local splinter by itself still does not justify promotion.

### 5) `957B..958B` was the strongest local helper-like island of the run
This was the biggest local-structure temptation in the whole continuation.

`957B..958B` scored the highest local-island score of the run and looked genuinely good:
- low-ish ASCII
- one call opcode
- two branch opcodes
- two returns
- a tighter byte lane than most nearby pages

It still failed because:
- all outside lures on the page were only single-hit
- none of those callers defended this island as a true start
- the page’s best evidence stayed local, not caller-backed

So `957B..958B` is the strongest local helper-like false dawn of this continuation.

### 6) `960A` plus `960C..9624` were the cleanest late-block combination
The late continuation ended with the most interesting outside/local pairing in the block.

Outside pressure:
- `960A` with 2 outside `JSR` hits

Local structure:
- `960C..9624`, a strong return-anchored island with low ASCII, one call, three branches, and two returns

That is the best combined late-block evidence in the run.

And it still was not enough.

Why:
- the outside pressure is real but not decisive
- nearby landings such as `9618` still collapse on bad starts like `01`
- the page still does not resolve into one clear owner-backed boundary that actually earns promotion

So it remains the cleanest late-block near-miss, not a breakthrough.

## Current live seam now
- **`C3:9700..`**

## Current completion estimate
- **~84.8%**

## No-BS state after this continuation
This was real progress.

But it was the slow, disciplined kind:
- no zero-field cleanup
- no code breakthrough
- just a long stretch of mixed material where several pages looked tempting without quite becoming code

That still matters.
This is exactly where conservative review protects the repo from fake helpers and fake owners.

## Recommended next move
Resume at:

- **`C3:9700..`**

And keep the same standard:
1. reject outside multi-hit pressure unless the landing owns itself locally
2. reject strong local splinters unless a caller-backed true start actually defends them
3. treat busy xref pages as interesting, not trustworthy
4. watch whether `9700+` finally turns this steadier post-zero rebound into genuinely recoverable caller-backed code, or whether it keeps producing the same mixed-control near-misses

## Structural truths worth preserving
- `8D80` is the cleanest early double-hit outside lure of the continuation and still does not defend a stable owner boundary
- `90A7` is the strongest lure on the busiest outside-call page of the run and still fails ownership
- `9199..91B1` plus `91E0..91F7` form the strongest internal-control island cluster of the continuation and still lack a caller-backed true start
- `9200` has no meaningful outside or local traction and should stay treated as mixed command/control material
- `94BA..94C4` is a clean isolated local pocket with no caller-backed support
- `957B..958B` is the strongest local helper-like island of the continuation and still cannot be promoted honestly
- `960A` is the strongest late-block outside multi-hit lure
- `960C..9624` is the strongest late-block local island cluster, and the combination still falls short of promotion

## Files produced in this continuation
- `chrono_trigger_c3_8d00_96ff_raw_report.md`
- `chrono_trigger_session14_continue_notes_6.md`
