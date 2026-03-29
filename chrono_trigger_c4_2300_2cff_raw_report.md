# Chrono Trigger seam raw report — C4:2300..C4:2CFF

## Scope
- Continuation from live seam: `C4:2300..`
- Conservative forward sweep across the next ten pages of bank `C4`
- Rebuilt local fast-path seam logic reused for the block sweep after the workspace cache dropped out
- Caller anchoring remained conservative because the full manifest history is still not mirrored locally

## Bottom line
- Closed: `C4:2300..C4:2CFF`
- Promotions: **none**
- New live seam: **`C4:2D00..`**

This continuation stayed active, but it was a step down from the hotter `C4:1900..22FF` block.

The main patterns were:
- an opening mixed page at `C4:2300` with several single-hit clean-start lures and no real structural ownership
- the busiest page of the continuation at `C4:2400`, led by repeated pressure on `C4:2400`
- two dead-feeling pages at `C4:2500` and `C4:2A00` with no meaningful outside traction
- a mixed page at `C4:2600` where the cleanest survivor sat next to hard-bad `00` landings
- the strongest repeated-hit near-miss page of the block at `C4:2700`
- a branch-fed page at `C4:2800` with one hard-bad lure on `02`
- a mixed page at `C4:2900` with one hard-bad `RTS` landing on `60`
- a thin branch-fed page at `C4:2B00`
- a cleaner closing mixed page at `C4:2C00`

None of them cleared the promotion standard.

---

## Page-by-page triage

### `C4:2300..C4:23FF`
**Page family:** `mixed_command_data`

What mattered:
- `C4:2300`, `C4:2302`, `C4:2367`, `C4:23A2`, and `C4:23C4` all took single raw hits and all five were clean-start near-misses
- strongest owner-backtrack candidate was **`C4:2360`** for `C4:2367`
- the page produced **no meaningful local clusters**

Bottom line:
- several believable clean-start lures, but no repeated pressure and no structural ownership behind them

### `C4:2400..C4:24FF`
**Page family:** `branch_fed_control_pocket`

This was the busiest page of the continuation.

What mattered:
- `C4:2400` took **two** raw hits and stayed the cleanest repeated-hit lure on the page
- `C4:2401`, `C4:2411`, `C4:241D`, `C4:24B0`, and `C4:24F4` were all additional single clean-start near-misses
- strongest owner-backtrack candidates were:
  - **`C4:2400`** for `C4:2401`
  - `C4:240F` for `C4:2411`
  - `C4:24AB` for `C4:24B0`
  - `C4:24EE` for `C4:24F4`
- the page produced **no meaningful local clusters**

Bottom line:
- hottest page of the block by raw pressure, still too thin structurally to hand over a defendable owner

### `C4:2500..C4:25FF`
**Page family:** `mixed_command_data`

What mattered:
- no meaningful raw caller traction survived on the page
- no local islands or merged clusters survived scoring

Bottom line:
- quiet mixed page, seam moved through cleanly

### `C4:2600..C4:26FF`
**Page family:** `mixed_command_data`

What mattered:
- `C4:263B` was the cleanest surviving lure and stayed **clean-start**
- `C4:2610` was another single clean-start near-miss
- `C4:2630` and `C4:269C` both died immediately because the landing byte is **`00`**
- strongest owner-backtrack candidates were:
  - **`C4:262F`** for `C4:2630`
  - `C4:263B` for `C4:263B`
- strongest local-control cluster was **`C4:2643..C4:2648`**

Bottom line:
- mixed page with one cleaner survivor sitting next to two obvious hard-bad false dawns

### `C4:2700..C4:27FF`
**Page family:** `mixed_command_data`

This was the strongest repeated-hit near-miss page of the continuation.

What mattered:
- `C4:2738` took **two** raw hits and stayed the cleanest repeated-hit lure of the block
- `C4:271B` and `C4:273F` were additional single clean-start near-misses
- strongest owner-backtrack candidate was **`C4:2716`** for `C4:271B`
- strongest local-control cluster was **`C4:27C3..C4:27D4`**

Bottom line:
- strongest repeated-hit page of the block, still no start where caller pressure and local structure lined up cleanly enough to promote

### `C4:2800..C4:28FF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C4:2815` and `C4:2820` were single clean-start weak near-misses
- `C4:28DC` died immediately on hard-bad **`02`**
- strongest owner-backtrack candidate was **`C4:281E`** for `C4:2820`
- only surviving local-control cluster was **`C4:28BA..C4:28BF`**

Bottom line:
- branch-fed page with thin outside traction and one obvious hard-bad lure

### `C4:2900..C4:29FF`
**Page family:** `mixed_command_data`

What mattered:
- `C4:2900` and `C4:29F6` were the cleanest surviving lures and both stayed **clean-start**
- `C4:2960` died immediately because the landing byte is hard-bad **`60`**
- strongest owner-backtrack candidates were:
  - **`C4:29F3`** for `C4:29F6`
  - `C4:295E` for `C4:2960`
- the page produced **no meaningful local clusters**

Bottom line:
- mixed page with one cleaner late lure and one hard-bad RTS landing on `60`

### `C4:2A00..C4:2AFF`
**Page family:** `mixed_command_data`

What mattered:
- no meaningful raw caller traction survived on the page
- strongest local-control cluster was **`C4:2A88..C4:2A91`**

Bottom line:
- dead-feeling mixed page with only light local structure

### `C4:2B00..C4:2BFF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C4:2BEC` was the only raw lure on the page and stayed **clean-start**
- strongest owner-backtrack candidate stayed pinned directly on **`C4:2BEC`**
- strongest local-control cluster was **`C4:2BDB..C4:2BE4`**, but it was extremely ASCII-skewed

Bottom line:
- thin branch-fed near-miss page with one weak lure and no believable supporting ownership

### `C4:2C00..C4:2CFF`
**Page family:** `mixed_command_data`

What mattered:
- `C4:2C4F` was the cleanest lure of the closing page and looked like the cleanest direct start of the whole continuation
- `C4:2C52` was another single clean-start weak near-miss
- `C4:2CD8` died immediately on hard-bad **`02`**
- strongest owner-backtrack candidate stayed pinned directly on **`C4:2C4F`**
- the page produced **no meaningful local clusters**

Bottom line:
- cleaner closing page than most of the block, still not enough to justify a promotion under the current conservative anchor posture

---

## Key truths preserved by this continuation
- `C4:2400` is the busiest repeated-hit lure of the continuation and still does not defend ownership
- `C4:2500..25FF` and `C4:2A00..2AFF` both read as quieter mixed territory with little or no outside traction
- `C4:2630` and `C4:269C` are hard-bad false dawns on `00`
- `C4:2738` is the strongest repeated-hit clean-start lure of the block and still falls short of promotion
- `C4:28DC` and `C4:2CD8` are hard-bad lures on `02`
- `C4:2960` is a hard-bad lure on `60`
- `C4:2716` and `C4:29F3` are the strongest owner-backtrack candidates of the continuation and still are not defensible as promotions
- `C4:2C4F` is the cleanest direct-start closing lure of the block and still lacks enough convergent support to promote
- `C4:27C3..27D4` is the strongest local-control cluster of the continuation and still only structure

---

## Result
- Seam advanced from **`C4:2300..`** to **`C4:2D00..`**
- No new labels promoted
- Label space remains clean
