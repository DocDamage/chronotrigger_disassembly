# Chrono Trigger Disassembly — Session 13 Continuation Notes (Fourth Continuation)

## Starting point
- Prior live seam: `C3:4700..`
- Prior latest completed pass: **221**
- Prior estimate: **~82.0%**

## Work completed now
This continuation closed **passes 222 through 231**.

### Pass 222 — `C3:4700..47FF`
Treated as sparse mixed page with only four visible targets, all dirty on caller quality, and a late unsupported `RTS` island.

Key outcome:
- visible external targets were `4709`, `4738`, `4788`, and `47B8`
- `4738` had the cleanest target-side neighborhood of the page, but its only visible caller came from a dirty high-risk neighborhood at `C3:DADD`
- `4709` also looked superficially interesting because it lands right on a tiny `RTS` pocket at the top of the page, but both caller and target side read mixed / high-risk
- strongest local splinter was `47D6..47E5` ending in `RTS`, still unsupported

### Pass 223 — `C3:4800..48FF`
Treated as xref-richer mixed page with double-hit `4843` bait and no caller-backed owner.

Key outcome:
- `4843` received **two** external `JSR` hits from `C3:3E95` and `C3:7720`
- both callers were still high-risk and the target neighborhood itself stayed mixed/high-risk
- early targets `4800`, `4802`, `480A`, `480C`, and `4814` all looked more like entry-bait into a noisy blob than defendable starts
- local pockets at `489B..489F` and `487C..4883` were too tiny and too unsupported to promote

### Pass 224 — `C3:4900..49FF`
Treated as text-heavier mixed page with dirty double-hit `4920` bait and no stable boundary.

Key outcome:
- `4920` received **two** external `JSR` hits from `C3:4A16` and `C3:73AF`
- both callers were high-risk and the target side also stayed high-risk
- `494E` had the cleanest target-side look of the page, but still only one dirty caller from `C3:73E2`
- the only surfaced local island, `49BB..49C4`, was weak and unsupported

### Pass 225 — `C3:4A00..4AFF`
Treated as ASCII-heavy mixed page with scattered single-hit targets and deceptive return-anchored islands inside text-like material.

Key outcome:
- the page was one of the more text-heavy seams of the run
- `4AA5` and `4AF0` had the least-awful caller/target risk combination on paper, but both still remained only single-hit targets inside a broader ASCII-heavy blob
- `4A60` and `4A62` also looked tempting because they sit near a busier local pocket, but caller quality was still too poor
- surfaced islands such as `4A34..4A4C`, `4A3B..4A53`, and `4A5F..4A77` were all embedded in high-ASCII mixed material and did not earn ownership

### Pass 226 — `C3:4B00..4BFF`
Treated as mixed text-heavy page with one cleaner late landing at `4BCB`, but still no defendable start.

Key outcome:
- `4BCB` was the most tempting target of the page because its visible caller `C3:28EA -> JMP $4BCB` was only medium-risk and the target side looked comparatively clean
- even so, `4BCB` lands too late and too deep inside mixed material to defend a true owner boundary
- earlier targets `4B00`, `4B30`, and `4B3A` all had dirtier caller support
- local islands `4B20..4B33` and `4BED..4BF1` remained unsupported splinters

### Pass 227 — `C3:4C00..4CFF`
Treated as the strongest local-island page of this continuation, with tempting `4C3F` support that still lands inside a splinter rather than at a true start.

Key outcome:
- `4C3F` got the cleanest caller-side evidence of the continuation from `C3:28F4 -> JSR $4C3F`
- the local page also produced the best return-anchored pocket of this run: `4C3A..4C49` ending in `RTS`
- that same fact is what kills promotion: the visible hit lands at interior `4C3F`, not at the pocket’s true beginning
- `4C00`, `4C50`, `4CA5`, and `4CD0` all stayed weaker or dirtier than `4C3F`

### Pass 228 — `C3:4D00..4DFF`
Treated as mixed command/control page with scattered single-hit bait and one cleaner-looking mid-page landing at `4D80`.

Key outcome:
- `4D80` had the best risk profile of the page because its visible caller `C3:42A4 -> JSR $4D80` and the target neighborhood both came out medium-risk instead of outright high-risk
- that still was not enough to rescue the page because `4D80` does not defend a clean routine boundary
- noisy late targets `4DB5` and `4DC5` had cleaner target neighborhoods but visibly dirty callers
- local pockets `4D49..4D51` (`RTL`) and `4D1C..4D23` (`RTI`) were too small and too ASCII-heavy to promote

### Pass 229 — `C3:4E00..4EFF`
Treated as xref-heavy mixed page with dirty double-hit `4E7D` bait and one unsupported mid-page `RTS` island.

Key outcome:
- `4E7D` received **two** visible hits from the same dirty `2A7x` neighborhood (`C3:2A79` and `C3:2A83`)
- other visible targets such as `4E00`, `4E03`, `4E06`, `4E0D`, `4E12`, `4E41`, `4E45`, `4E49`, and `4E60` were all single-hit and mostly high-risk
- `4EE6` had the cleanest caller-side risk of the page, but the target neighborhood itself was still high-risk
- local island `4E2C..4E36` ending in `RTS` remained unsupported

### Pass 230 — `C3:4F00..4FFF`
Treated as repeated-value mixed page with clustered double-hit bait around `4F41`, `4F46`, and `4F4B`.

Key outcome:
- `4F41`, `4F46`, and `4F4B` each received **two** external `JSR` hits
- all of those callers were still high-risk and the page itself carried elevated zero/repeated-pair density
- late targets `4F52`, `4F53`, `4F57`, and `4F59` looked slightly cleaner on the target side, but not enough to defend ownership
- surfaced local `RTI` pockets at `4F1D..4F2A` and `4F13..4F1B` were extremely ASCII-heavy and non-promotable

### Pass 231 — `C3:5000..50FF`
Treated as lower-ASCII but zero/repeated-pair-heavy mixed page with many single-hit targets and no clean owner boundary.

Key outcome:
- the page looked less text-heavy than `4A00`, `4B00`, or `4F00`, but still read mixed and structurally unstable
- `5016`, `5018`, and `50F1` had the least-awful target-side neighborhoods, but their caller support remained high-risk and single-hit only
- noisy scattered targets also included `5008`, `5028`, `5035`, `503F`, `5047`, `50A5`, `50E1`, and `50E7`
- the only surfaced local island, `50B8..50C3` ending in `RTI`, was too weak to promote

## Current state now
- Latest completed pass: **231**
- Current live seam: **`C3:5100..`**
- Current completion estimate: **~82.8%**

## Honest read of the seam
This continuation did not produce a real owner promotion, but it did expose the next block clearly:
- `4700` and `4900` were sparse mixed pages with only dirty caller support
- `4800`, `4E00`, and `4F00` were xref-richer, but the extra hits were still low-quality bait rather than real ownership
- `4A00`, `4B00`, and `4F00` stayed notably ASCII-heavy / text-like
- `4C00` was the strongest false dawn of the run because it paired the best local island with the cleanest visible caller, and still failed at the owner-boundary test
- `5000` looked less text-heavy but still not code-clean

## Biggest takeaways
1. **`4C3F` / `4C3A..4C49`** are the strongest false-dawn combination of this continuation.
2. **`4BCB`** and **`4D80`** are the next most tempting single-hit landings, but neither defends a true start.
3. **`4A00`, `4B00`, and `4F00`** remain strongly contaminated by text-like / repeated-value mixed content.
4. **No new defendable owner/helper promotions survived passes 222 through 231.**

## Real next target
- **`C3:5100..`**
