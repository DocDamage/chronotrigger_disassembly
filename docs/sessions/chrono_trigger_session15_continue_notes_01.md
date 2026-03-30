# Chrono Trigger continuation notes after Session 15 handoff

## What was done
- Resumed at the Session-15 live seam `C4:3700..`.
- Swept two 10-page ROM-first seam blocks:
  - `C4:3700..C4:40FF`
  - `C4:4100..C4:4AFF`
- Kept the standard conservative: no code promotion without caller quality + start-byte quality + local structure all agreeing.
- Result: **no new promotions** in these 20 pages.

## Why no promotions were made
- The first block stayed dominated by bad-start collapses, local-control pockets, and one hotter-but-still-shaky run through `C4:3D00..3EFF`.
- `C4:4000..40FF` looked hot on raw hits but also carried a large hard-bad-start load (`12` hard-bad starts, `1` soft-bad start), which is exactly the kind of false dawn the handoff warned about.
- The second block produced a few manual-review pages (`C4:4100..41FF`, `C4:4200..42FF`), but the strongest backtracks still sat inside mixed binary structure rather than clean owner boundaries.
- `C4:4400..45FF` relaxed into mixed-lane-continue posture rather than true owner recovery; isolated weak landings existed, but not enough to justify labels.

## Most important near-miss pages
### Block 1
- `C4:3D00..3DFF` — branch-fed control pocket, 3 effective strong/weak hits, but best backtrack quality still centered on mixed binary pockets like `C4:3D20` and a poor data-like landing at `C4:3DDB..3DF7` for `C4:3DDF`.
- `C4:3E00..3EFF` — manual owner-boundary review, but the best starts (`C4:3EC2`, `C4:3E00`) still looked like interior mixed-content pockets instead of defensible callable owners.
- `C4:4000..40FF` — hottest raw page in the block, but it burned down under bad-start pressure; do **not** overreact to its hit count.

### Block 2
- `C4:4100..41FF` — strongest page of the second block, but still only manual-review quality; candidate starts at `C4:41AE` and `C4:41E0` were not clean enough to promote.
- `C4:4200..42FF` — another manual-review page, but it included a soft-bad landing at `C4:4200` and only one backtrack at score>=3 (`C4:42A0`), again inside mixed material.
- `C4:4400..45FF` — isolated weak hits (`C4:44E3`, `C4:45BA`) without enough supporting structure.

## Byte-level smell check
- Representative hotspots such as `C4:3D00`, `C4:3E00`, `C4:4000`, `C4:4100`, and `C4:42A0` still read like dense mixed binary/data/control material rather than obvious routine lanes.
- This continuation therefore supports the same structural truth preserved by Session 15: **hotter C4 frontier does not automatically mean promotable code**.

## Seam movement
- Previous live seam: `C4:3700..`
- Newly swept through: `C4:4AFF`
- New live seam: **`C4:4B00..`**

## Pass / completion estimate
- Previous latest completed pass: **461**
- New latest completed pass estimate after 20 more pages: **481**
- Previous completion estimate: **~90.4%**
- New rough completion estimate: **~91.2%**

## Recommended next move
1. Continue the same block workflow at `C4:4B00..`.
2. Treat `C4:3D00..3EFF` and `C4:4100..42FF` as preserved near-miss territory only; do not label from them unless stronger caller ownership appears from fuller manifest-backed review.
3. Do not let `C4:4000..40FF` bait a promotion just because it is hot.
