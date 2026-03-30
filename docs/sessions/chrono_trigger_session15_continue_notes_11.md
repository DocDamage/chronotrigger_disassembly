# Chrono Trigger continuation notes after Session 15 handoff — pass set 11

## What was done
- Resumed at the live seam **`C4:FF00..`**.
- Swept two additional 10-page ROM-first seam blocks:
  - `C4:FF00..C5:08FF`
  - `C5:0900..C5:12FF`
- Crossed the bank boundary cleanly from late `C4` into early `C5`.
- Kept the same conservative rule: no code promotion without caller quality, start-byte quality, and local structure all converging.
- Result: **no new promotions** in these 20 pages.

## Method note
- No manifest-backed workspace was recovered in this session, so caller ownership stayed conservative.
- This continuation used a local fixed-target control-flow/xref scan over static calls, jumps, and branches.
- That was enough to keep seam movement honest, but not enough to justify aggressive owner inflation.

## Why no promotions were made
- The first block opened with a nasty bank-edge carryover at `C4:FF00..FFFF`, then immediately rolled into an even hotter early-`C5` belt.
- `C5:0000..00FF` was the hottest page of the entire continuation by raw pressure and effective hits. It also carried an enormous bad-start burden, which kept it squarely in trap territory instead of promotable-owner territory.
- `C5:0100..06FF` stayed consistently active, but every page still mixed believable clean starts with enough hard-bad or soft-bad bait to fail the standard.
- `C5:0700..07FF` was the cleanest page of block one. It had the best balance between clean-hit pressure and bad-start load, which makes it the **strongest honest near-miss** of this continuation.
- `C5:0800..08FF` stayed quieter and did not reopen promotion pressure before the second block.
- The second block remained fully reject posture, but it was less chaotic than the bank-opening burst.
- `C5:0900..0E00` formed a broad branch-fed control belt: active, structured, still not convergent.
- `C5:0F00..0FFF` was the hottest late trap page of the continuation and the strongest false dawn of block two.
- `C5:1000..10FF` was the cleanest second-block candidate-code page, but it still carried too much poison to promote honestly.
- `C5:1200..12FF` closed the continuation by proving the later belt had still not cleaned up.

## Most important near-miss / trap pages
### First block
- `C4:FF00..FFFF` — dirtiest bank-edge carryover page of the continuation.
- `C5:0000..00FF` — **hottest trap page of the continuation**.
- `C5:0300..03FF` and `C5:0400..04FF` — early cleaner candidate-code near-miss pages.
- `C5:0700..07FF` — **strongest honest near-miss page of the continuation**.
- `C5:0500..06FF` — branch-fed dirty belt, still not promotable.

### Second block
- `C5:0900..0E00` — broad branch-fed control belt; active but still reject posture.
- `C5:0F00..0FFF` — hottest late trap page.
- `C5:1000..10FF` — cleanest second-block candidate-code near-miss page.
- `C5:1100..11FF` — quieter follow-on page, still nonconvergent.
- `C5:1200..12FF` — dirty closing page with no rescue lane.

## Structural read
- This continuation did not reveal a hidden callable lane at the end of bank `C4`.
- It revealed a **hot early-`C5` mixed-content belt** with one very loud trap page at `C5:0000..00FF`.
- The honest keepers from this pass are:
  - **`C5:0700..07FF`** — strongest clean near-miss
  - **`C5:0000..00FF`** — hottest trap page
  - **`C4:FF00..FFFF`** — dirtiest carryover bank-edge page
- The correct move is still the same: preserve these as reference territory only and keep the seam moving.

## Seam movement
- Previous live seam: `C4:FF00..`
- Newly swept through: `C5:12FF`
- New live seam: **`C5:1300..`**

## Pass / completion estimate
- Previous latest completed pass estimate: **661**
- New latest completed pass estimate: **681**
- Previous completion estimate: **~98.4%**
- New rough completion estimate: **~99.2%**

## Recommended next move
1. Continue the block workflow at `C5:1300..`.
2. Preserve **`C5:0700..07FF`**, **`C5:0000..00FF`**, and **`C4:FF00..FFFF`** as reference territory only.
3. Do not let the bank-opening heat in early `C5` force an early promotion.
