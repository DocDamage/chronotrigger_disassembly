# Chrono Trigger continuation notes after Session 15 handoff — pass set 10

## What was done
- Resumed at the live seam **`C4:EB00..`**.
- Swept two additional 10-page ROM-first seam blocks:
  - `C4:EB00..C4:F4FF`
  - `C4:F500..C4:FEFF`
- Kept the same conservative rule: no code promotion without caller quality, start-byte quality, and local structure all converging.
- Result: **no new promotions** in these 20 pages.

## Why no promotions were made
- This continuation was not a quiet mixed stretch. It was a **dense reject belt**.
- Every page across both blocks stayed in **bad_start_or_dead_lane_reject** posture under the current ROM-first triage.
- The first block (`EB00..F4FF`) was active almost everywhere:
  - `C4:EB00..EBFF`, `C4:ED00..EDFF`, and `C4:EE00..EEFF` all carried strong clean-hit pressure,
  - but each of them still mixed that pressure with enough hard-bad starts to block honest promotion.
- `C4:F000..F0FF` was the hottest page of block one, but it was also obviously trap-heavy, with eight hard-bad starts buried inside the traffic.
- The second block (`F500..FEFF`) got even louder.
- `C4:F600..F6FF` was the cleanest page of the entire continuation: lots of clean weak hits, only two hard-bad starts, and several plausible backtracks. It is the **strongest honest near-miss** of this pass.
- `C4:F800..F8FF` was the hottest page of the continuation by clean-hit pressure, but it still mixed in heavy bad-start pollution and stayed nonpromotable.
- `C4:FD00..FDFF` was the dirtiest page of the continuation by far, with a huge poison load (`17` hard-bad starts and `21` soft-bad starts). That page is not a near-miss — it is a warning sign.
- `C4:FB00..FBFF` and `C4:FE00..FEFF` also looked hotter than average, but both still failed convergence under the current standard.

## Most important near-miss / trap pages
### First block
- `C4:EB00..EBFF` — strongest early hot near-miss page.
- `C4:ED00..EDFF` — cleanest low-noise near-miss page of block one.
- `C4:EE00..EEFF` — broad repeated-hit page, still dirty.
- `C4:F000..F0FF` — hottest trap page of block one.

### Second block
- `C4:F600..F6FF` — **strongest honest near-miss page of the continuation**.
- `C4:F800..F8FF` — **hottest trap page of the continuation**.
- `C4:FB00..FBFF` — very hot, still not convergent.
- `C4:FD00..FDFF` — dirtiest poison field of the continuation.
- `C4:FE00..FEFF` — very hot closing page, still too dirty to trust.

## Structural read
- This continuation did not reveal a rescue lane.
- It revealed that the seam has entered another **high-pressure mixed-content belt**.
- The honest keepers from this pass are:
  - **`C4:F600..F6FF`** — strongest clean near-miss
  - **`C4:F800..F8FF`** — hottest trap page
  - **`C4:FD00..FDFF`** — dirtiest poison page
- The correct move is still the same: preserve those pages as reference territory only and keep the seam moving.

## Seam movement
- Previous live seam: `C4:EB00..`
- Newly swept through: `C4:FEFF`
- New live seam: **`C4:FF00..`**

## Pass / completion estimate
- Previous latest completed pass estimate: **641**
- New latest completed pass estimate: **661**
- Previous completion estimate: **~97.6%**
- New rough completion estimate: **~98.4%**

## Recommended next move
1. Continue the block workflow at `C4:FF00..`.
2. Preserve **`C4:F600..F6FF`**, **`C4:F800..F8FF`**, and **`C4:FD00..FDFF`** as reference territory only.
3. Do not let the heat in the `C4:F000..F8FF` belt force an early promotion.
