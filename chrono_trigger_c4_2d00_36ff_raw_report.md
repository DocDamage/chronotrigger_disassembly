# Chrono Trigger seam raw report — C4:2D00..C4:36FF

## Scope
- Continuation from live seam: `C4:2D00..`
- Conservative forward sweep across the next ten pages of bank `C4`
- Rebuilt local fast-path seam logic reused for the block sweep after the workspace cache dropped out
- Caller anchoring remained conservative because the full manifest history is still not mirrored locally

## Bottom line
- Closed: `C4:2D00..C4:36FF`
- Promotions: **none**
- New live seam: **`C4:3700..`**

This continuation was a little cooler than the hotter `C4:1900..2CFF` stretch, but it still produced several believable near-misses:
- a hottest repeated-hit page at `C4:3000`
- a cleaner repeated-hit page at `C4:3400`
- thin mixed pages at `C4:3200`, `C4:3300`, and `C4:3600`
- multiple dead-feeling pages with essentially no outside traction

None of it cleared the promotion standard.

---

## Page-by-page triage

### `C4:2D00..C4:2DFF`
**Page family:** `mixed_command_data`

What mattered:
- no meaningful raw caller traction survived on the page
- no meaningful local clusters survived scoring

Bottom line:
- quiet mixed page, seam moved through cleanly

### `C4:2E00..C4:2EFF`
**Page family:** `mixed_command_data`

What mattered:
- no meaningful raw caller traction survived on the page
- no meaningful local clusters survived scoring

Bottom line:
- another quiet mixed page with no outside ownership pressure

### `C4:2F00..C4:2FFF`
**Page family:** `mixed_command_data`

What mattered:
- `C4:2FF7` was the only raw lure on the page
- it died immediately because the landing byte is hard-bad **`FF`**
- no meaningful local clusters survived scoring

Bottom line:
- thin page with a single hard-bad false dawn

### `C4:3000..C4:30FF`
**Page family:** `mixed_command_data`

This was the hottest page of the continuation.

What mattered:
- `C4:3000` took **three** raw hits and stayed the cleanest repeated-hit lure on the page
- `C4:3004` took **two** raw hits and died immediately on hard-bad **`FF`**
- `C4:3020` took **two** raw hits and stayed a clean-start near-miss
- `C4:30CF` took **two** raw hits and died immediately on hard-bad **`00`**
- `C4:30DF` took **two** raw hits and stayed a clean-start near-miss
- `C4:309C`, `C4:3047`, `C4:3007`, and `C4:303B` were additional hard-bad false dawns on **`02`** and **`FF`**
- strongest owner-backtrack candidates stayed scattered across the page rather than converging on one stable owner boundary
- the page produced no local structure strong enough to rescue ownership

Bottom line:
- busiest page of the block, but too fragmented and too dirty to justify a promotion

### `C4:3100..C4:31FF`
**Page family:** `mixed_command_data`

What mattered:
- no meaningful raw caller traction survived on the page
- no meaningful local clusters survived scoring

Bottom line:
- dead-feeling mixed page with no outside traction

### `C4:3200..C4:32FF`
**Page family:** `mixed_command_data`

What mattered:
- `C4:3200` was the only clean surviving lure and stayed a single weak near-miss
- `C4:32B7` died immediately on hard-bad **`00`**
- no meaningful local clusters survived scoring

Bottom line:
- thin mixed page with one cleaner survivor sitting next to one obvious hard-bad false dawn

### `C4:3300..C4:33FF`
**Page family:** `mixed_command_data`

What mattered:
- `C4:3300` died immediately on hard-bad **`FF`**
- `C4:33C5` was the only surviving clean-start lure and still remained a single weak near-miss
- no meaningful local clusters survived scoring

Bottom line:
- mixed page with one hard-bad lure and one thin clean-start survivor

### `C4:3400..C4:34FF`
**Page family:** `candidate_code_lane`

This was the cleanest repeated-hit page of the continuation.

What mattered:
- `C4:347C` took **two** raw hits and stayed the strongest repeated-hit clean-start lure of the block
- `C4:34C2`, `C4:3429`, and `C4:3405` were additional single clean-start near-misses
- strongest owner-backtrack candidates stayed split across the page instead of converging behind `C4:347C`
- the page still did not produce one local-control pocket that clearly defended a true owner boundary

Bottom line:
- best-looking page of the block, still not enough to promote under the current conservative anchor posture

### `C4:3500..C4:35FF`
**Page family:** `mixed_command_data`

What mattered:
- no meaningful raw caller traction survived on the page
- no meaningful local clusters survived scoring

Bottom line:
- quiet mixed page, seam moved through cleanly

### `C4:3600..C4:36FF`
**Page family:** `mixed_command_data`

What mattered:
- `C4:3606` died immediately because the landing byte is hard-bad **`60`**
- `C4:3608` and `C4:3689` were the only surviving clean-start lures and both stayed single weak near-misses
- no meaningful local clusters survived scoring

Bottom line:
- modest closing page with one hard-bad false dawn and two thin clean-start survivors

---

## Key truths preserved by this continuation
- `C4:2FF7` is a hard-bad lure on `FF`
- `C4:3000..30FF` is the hottest page of the continuation
- `C4:3000` is the busiest repeated-hit clean-start lure of the block and still does not defend ownership
- `C4:3004`, `C4:30CF`, `C4:309C`, `C4:3047`, `C4:3007`, and `C4:303B` prove again that repeated outside pressure can keep landing on obvious garbage
- `C4:3200` and `C4:33C5` are thin clean-start survivors on otherwise dirty mixed pages
- `C4:347C` is the strongest repeated-hit clean-start lure of the continuation and still falls short of promotion
- `C4:3606` is a hard-bad lure on `60`
- `C4:3608` and `C4:3689` are the cleanest closing lures of the block and still lack enough convergent support to promote

---

## Result
- Seam advanced from **`C4:2D00..`** to **`C4:3700..`**
- No new labels promoted
- Label space remains clean
