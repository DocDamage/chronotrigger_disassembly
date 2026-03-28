# Chrono Trigger Disassembly — Session 13 Continuation Notes (Fifth Continuation)

## Starting point
- Prior live seam: `C3:5100..`
- Prior latest completed pass: **231**
- Prior estimate: **~82.8%**

## Work completed now
This continuation closed **passes 232 through 241**.

### Pass 232 — `C3:5100..51FF`
Treated as mixed control page with a tempting late pocket, but no caller-backed owner start.

Key outcome:
- the strongest visible target on paper was **`5196`** because it drew two branch-fed hits and the target neighborhood itself came out low-risk
- that still was not enough to rescue the page, because both hits were local/control-style branches inside the same mixed blob, not defendable external ownership
- the strongest true outside pressure was a dirty double-`JSR` into **`5100`** from `C3:2C08` and `C3:5B7D`, which still fails immediately on caller quality
- late pocket **`51E8..51F0`** ending in `RTI` was the best local island of the page, but it remained unsupported

### Pass 233 — `C3:5200..52FF`
Treated as the strongest page-top false dawn of the continuation: clean-looking `5200` bait, but still no defendable start.

Key outcome:
- **`5200`** received two visible hits: a dirty `JSR` from `C3:3E86` and a much cleaner cross-page `BPL` from `C3:51FE`
- the page also produced several low-risk branch-fed landings like `520A`, `5213`, and `52BE`, which makes it look more stable than it really is
- local splinter **`5221..5226`** ending in `RTS` and broader pocket **`5273..5284`** both read like unsupported local control fragments rather than true owners
- result: best early page-top bait of the run, still not promotable

### Pass 234 — `C3:5300..53FF`
Treated as sparse mixed branch/control page with mostly self-fed local traffic and no credible outside ownership.

Key outcome:
- visible targets were light and almost entirely branch-fed from within or immediately around the same mixed blob
- **`534E`** and **`534F`** looked cleanest on paper, but only as local branch landings, not callable starts
- strongest local island **`5364..5375`** had two returns inside it, which makes it look structured, but still only as a local splinter with no defendable owner boundary
- page stayed too ASCII/zero-heavy overall to promote anything

### Pass 235 — `C3:5400..54FF`
Treated as xref-heavier mixed page with a real-looking double-`JSR` false dawn at `54A5`.

Key outcome:
- **`54A5`** was the strongest true external target of the page because it received two `JSR` hits from `C3:009D` and `C3:026D`, both only medium-risk
- that still was not enough to rescue the page because `54A5` lands inside a wider mixed return-anchored splinter rather than at a defendable top boundary
- `5445`, `544C`, `545E`, and `5462` all had more xref noise, but the caller/target mix stayed too dirty
- page looked active, but not trustworthy

### Pass 236 — `C3:5500..55FF`
Treated as mixed branch-heavy page with one medium-quality local cluster and no stable external owner.

Key outcome:
- **`557B`** got two medium-risk branch-fed hits and was the least-awful visible landing in the page
- that support was still local control traffic rather than real outside ownership
- stronger-looking outside pressure like the double-`JSR` into **`55A5`** from `C3:1002` and `C3:105E` failed immediately because both callers were high-risk
- strongest local pocket **`559F..55B1`** ending in `RTS` stayed unsupported

### Pass 237 — `C3:5600..56FF`
Treated as mixed command/control page with ugly page-level density but one clean late branch-fed lure.

Key outcome:
- page metrics were among the worst of the continuation (`ascii=0.36`, `zero=0.21`, `repeated_pair=0.20`)
- **`56DD`** had the cleanest individual risk pairing of the page thanks to `C3:5757 -> BMI $56DD`, both low-risk
- even so, that landing sits late in the page and behaves like branch-fed interior bait, not a defendable owner start
- no local islands survived scoring strongly enough to matter

### Pass 238 — `C3:5700..57FF`
Treated as mixed control page with clustered late-page traffic and one broad unsupported local island.

Key outcome:
- **`57FF`** and **`57C5`** both drew two visible hits, but the support was still branch-fed local/control traffic rather than clean ownership
- strongest outside `JSR` pressure landed at **`5777`**, but that target stayed high-risk and failed caller-quality review
- local splinter **`57BF..57D7`** ending in `RTI` was the broadest page island, but it still read like internal control flow rather than a callable start
- no promotion survived

### Pass 239 — `C3:5800..58FF`
Treated as the cleanest-looking page of the continuation, but still only as a local control blob rather than a caller-backed routine.

Key outcome:
- page metrics were the best of the run (`ascii=0.25`, `zero=0.05`, `repeated_pair=0.00`)
- several targets such as `581C`, `581D`, `5827`, `587E`, and `5890` looked clean on both caller and target risk, but nearly all of that support was self-contained branch traffic
- **`5872`** was the busiest visible landing with two hits, yet still only medium-grade and not ownership-worthy
- local islands **`582B..5840`** and **`587A..5886`** made the page feel executable, but not enough to defend a true external owner start

### Pass 240 — `C3:5900..59FF`
Treated as sparse mixed page with one cleaner mid-page lure and otherwise dirty tail traffic.

Key outcome:
- **`596F`** had the cleanest target-side profile of the page because `C3:5958 -> BVS $596F` only came out medium/low risk
- that still remained branch-fed local bait inside a mixed page, not a defendable start
- late **`59DA`** drew two hits, but both caller and target neighborhoods were high-risk
- only surfaced island **`59D0..59D5`** was too tiny and too ASCII-heavy to matter

### Pass 241 — `C3:5A00..5AFF`
Treated as mixed page with dirty clustered early bait and a cleaner late branch-fed tail that still does not own the page.

Key outcome:
- early targets **`5A1D`** and **`5A4C`** both drew two hits, but those hits were uniformly high-risk
- late tail landings **`5AAA`** and **`5ABA`** looked much cleaner, but only as local branch-fed control endpoints rather than routine starts
- local island **`5A67..5A75`** ending in `RTS` gave the page a slightly more structured feel late, but still without caller-backed ownership
- result: page ends cleaner than it begins, but still not promotable

## Current state now
- Latest completed pass: **241**
- Current live seam: **`C3:5B00..`**
- Current completion estimate: **~83.6%**

## Honest read of the seam
This continuation still did not produce a real owner/helper promotion, but it narrowed the next block clearly:
- `5200` was the strongest page-top false dawn of the run
- `5400` provided the strongest true external multi-hit landing at `54A5`, and it still failed
- `5800` was the cleanest-looking page overall, but mostly from local branch/control structure rather than true caller-backed ownership
- `5A00` ended cleaner than it began, hinting at a somewhat less text-contaminated seam ahead, but still not enough to promote yet

## Biggest takeaways
1. **`5200`** is the strongest page-top bait of this continuation and still fails ownership.
2. **`54A5`** is the strongest true external multi-hit false dawn of the run.
3. **`5800`** is the cleanest-looking page overall, but still reads as local control structure, not a defendable owner.
4. **No new defendable owner/helper promotions survived passes 232 through 241.**

## Real next target
- **`C3:5B00..`**
