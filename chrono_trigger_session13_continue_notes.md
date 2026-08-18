# Chrono Trigger Disassembly — Session 13 Continuation Notes

## Starting point
- Prior live seam: `C3:2900..`
- Prior latest completed pass: **191**
- Prior estimate: **~79.6%**

## Work completed now
This continuation closed **passes 192 through 201**.

### Pass 192 — `C3:2900..29FF`
Treated as mixed compare/branch/arithmetic blob with false single-hit targets and unsupported `298D` RTS-island bait.

Key outcome:
- visible raw targets included `2900`, `290C`, `2920`, `2938`, `298D`, `29F3`
- `298D..29AF` was the cleanest late local island and does end in `RTS`
- it still only had a weak same-bank hit from `C3:18DA` and never stabilized into a defendable owner start
- `29F3` also opened into ASCII-heavy mixed material instead of callable structure

### Pass 193 — `C3:2A00..2AFF`
Treated as mixed single-hit helper bait with false `2A40` tiny-RTS stub and untrusted `2A8D` control lane.

Key outcome:
- `2A40..2A4F` looked like a helper ending in `RTS`
- the only backing caller sat in obvious table-like material around `C3:32A3`
- `2A8D` looked more executable and even carries a `JSL` into bank `C3`, but still had only one noisy caller

### Pass 194 — `C3:2B00..2BFF`
Treated as mostly executable-looking mixed page with ASCII-heavy `2B06` caller and false interior-`RTI` bait at `2B4B`.

Key outcome:
- this was the most code-like page in the run
- `2B06` unfolds into a long helper-like lane with calls and a return near `2B51`
- the only visible external hit into `2B06` came from ASCII-heavy neighborhood `C3:C1EA`
- `2B4B` resolved as interior-byte `RTI` bait, not a real start

### Pass 195 — `C3:2C00..2CFF`
Treated as dense raw-target page with mixed-control lead-in and unsupported late `2CC1` code pocket.

Key outcome:
- crowded target field: `2C09`, `2C26`, `2C29`, `2C37`, `2C4C`, `2C53`, `2C98`, `2CC1`
- most early hits landed inside inline-control/table soup
- the best late pocket was around `2CC1..`, but still had only one medium-quality caller and no defendable owner boundary

### Pass 196 — `C3:2D00..2DFF`
Treated as text-contaminated mixed page with false ASCII-side `2D2D` hit and failed `2DB1` jump target.

Key outcome:
- visible `2D2D` caller from `C3:0E47` lived in blatant text-like material
- `2D40` did not survive review
- `2DB1` had the cleanest caller-side setup because `C3:164F` jumps there directly, but still opened inside mixed bytes and did not defend a true start

### Pass 197 — `C3:2E00..2EFF`
Treated as mixed multi-target page with unsupported `2E30` RTS stub and false late `2E86` tail.

Key outcome:
- visible targets: `2E30`, `2E3D`, `2E52`, `2E58`, `2E86`
- `2E30..2E3A` was the cleanest tiny `RTS` pocket in the page
- every visible target still had only one caller, and most caller neighborhoods were too noisy to trust

### Pass 198 — `C3:2F00..2FFF`
Treated as repeated-value command-stream page with false `2F09` and unsupported late return islands.

Key outcome:
- `2F09` had a comparatively cleaner caller from `C3:17EA`
- the target neighborhood was still ASCII/repeated-value contaminated and behaved more like inline command data than a defendable start
- late `2F72` and `2F80` pockets were visible but unsupported

### Pass 199 — `C3:3000..30FF`
Treated as mixed reentry page with small real-looking PPU-write stub at `307F`, but no caller-backed owner.

Key outcome:
- this page felt more executable than the previous few pages
- `307F..3087` was the cleanest tiny pocket and ends in `RTS`
- it did get a relatively cleaner same-bank caller from `C3:3318`, but only as a single-hit stub embedded in mixed bytes
- `3063` also looked helper-like but still did not earn defendable ownership

### Pass 200 — `C3:3100..31FF`
Treated as mixed high-confidence-caller page with double-supported `31BF` interior landing and no stable owner start.

Key outcome:
- strongest caller-side evidence of the run
- `31BF` received two comparatively clean same-bank callers from `C3:15B0` and `C3:2BD1`
- `31B0` also received multiple hits including a cleaner low-bank caller from `C3:4684`
- both still land inside a wider mixed blob with table-ish / padding-heavy lead-in bytes

### Pass 201 — `C3:3200..32FF`
Treated as mixed register-write / `RTI` tail page with interior `320D` hit, false `3287` long-wrapper, and tail-bait `32FF`.

Key outcome:
- `3200..3216` looked like a short register-write burst terminating in `RTI`
- the cleaner visible hit was into interior `320D`, not the true top of the burst
- `3287..328D` formed a tiny `JSR $290C ; ... ; RTL` shape, but only as a small unsupported wrapper pocket
- `32FF` was false tail bait and not a real callable owner

## Current state now
- Latest completed pass: **201**
- Current live seam: **`C3:3300..`**
- Current completion estimate: **~80.4%**

## Seam read
The run got less uniformly ugly after `3000`, but the recurring failure mode did not change:
- cleaner callers that still are not decisive
- landings into the middle of wider mixed blobs instead of true starts
- tiny return-anchored pockets that look good in isolation but do not own the page

## Biggest takeaways
1. **Pass 194 (`2B00`)** was the most executable-looking page of this run, but still failed because the visible `2B06` caller came from an ASCII-heavy neighborhood.
2. **Pass 199 (`3000`)** showed a tempting same-bank `RTS` helper at `307F..3087`, but only as a single-hit unsupported stub.
3. **Pass 200 (`3100`)** had the strongest caller-side evidence of the run, especially the double-supported `31BF` landing, yet that target still landed inside mixed material rather than at a defendable owner start.
4. **Pass 201 (`3200`)** suggests the seam may be nearing a more structured lane, but visible hits are still catching interior entrypoints and wrappers rather than true owners.

## Real next target
- **`C3:3300..`**
