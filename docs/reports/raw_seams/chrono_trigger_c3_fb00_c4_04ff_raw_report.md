# Chrono Trigger seam raw report — C3:FB00..C4:04FF

## Scope
- Continuation from live seam: `C3:FB00..`
- Conservative forward sweep across the next ten pages, crossing the end of bank `C3` into the opening pages of bank `C4`
- Local toolkit logic was reused with a single indexed raw-caller pass for the whole block
- Caller anchoring in the workspace remained conservative because the full manifest history is still not mirrored locally

## Bottom line
- Closed: `C3:FB00..C3:FFFF` and `C4:0000..C4:04FF`
- Promotions: **none**
- New live seam: **`C4:0500..`**

This continuation did two things at once:
- it finished the remaining five pages of bank `C3`
- it opened the first five pages of bank `C4`

The first half stayed consistent with the late-`C3` pattern: branch-fed pockets, dead-lane tail material, and mixed local-control structure that never defended ownership.

The second half was much hotter. `C4:0000..C4:04FF` produced materially more raw pressure and more code-shaped pages than the late `C3` frontier. Even so, nothing in this opening `C4` block cleared the standard cleanly enough to promote under the current conservative local-anchor posture.

---

## Page-by-page triage

### `C3:FB00..C3:FBFF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C3:680D -> C3:FB00` was the only clean surviving page lure and stayed only **weak**
- `C3:C2C5 -> C3:FB29` died immediately because the landing byte is **`00`**
- owner backtrack stayed pinned directly on **`C3:FB00`**
- strongest local-control cluster was **`C3:FB89..C3:FBBA`**, but it was already ASCII-heavy

Bottom line:
- strongest remaining `C3` opening-page near-miss, still not promotable

### `C3:FC00..C3:FCFF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C3:31A8 -> C3:FC00` was the only raw lure and died as a **soft-bad** landing on `01`
- owner backtrack stayed pinned directly on `C3:FC00`
- strongest local support was `C3:FC34..C3:FC41`

Bottom line:
- single soft-bad false dawn, no owner-backed support

### `C3:FD00..C3:FDFF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C3:616F -> C3:FD00` was the only page lure and stayed **weak**
- owner backtrack stayed pinned directly on **`C3:FD00`**
- strongest local clusters were:
  - **`C3:FD95..C3:FDAB`**
  - `C3:FDB4..C3:FDBC`

Bottom line:
- clean single-hit late-`C3` near-miss with no convergence behind it

### `C3:FE00..C3:FEFF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C3:5B77 -> C3:FE0F` stayed **suspect**
- `C9:9C5C -> C3:FE10` was the cleanest surviving lure and stayed **weak**
- `C3:CAE9 -> C3:FE02` died on hard-bad **`03`**
- owner backtrack preferred:
  - `C3:FE03` for `FE0F`
  - `C3:FE0B` for `FE10`
- strongest local-control cluster was **`C3:FE2C..C3:FE44`**

Bottom line:
- best late-`C3` mixed near-miss page, still no defendable owner boundary

### `C3:FF00..C3:FFFF`
**Page family:** `dead_zero_field`

What mattered:
- the page classified as a dead-tail zero field at the bank boundary
- raw callers still landed into it, but most of the interesting landings were either hard-bad `00` bytes or dirty edge material
- `C3:FF11`, `C3:FF18`, `C3:FF20`, `C3:FF29`, `C3:FF41`, `C3:FFA9`, and `C3:FFE0` all died on **`00`**
- `C3:FF08` and `C3:FF09` were the only superficially livelier tail landings and still degraded under risk

Bottom line:
- the `C3` frontier reaches bank end without a late rescue; seam now moves into `C4`

### `C4:0000..C4:00FF`
**Page family:** `mixed_command_data`

This was the first truly hot page after the bank transition.

Main lures:
- `C4:0000` took **nine** raw hits and remained only a weak/suspect mix
- `C4:0002` also took **nine** raw hits and still only stayed weak/suspect
- `C4:0010` took **eight** raw hits and stayed only weak/suspect
- `C4:00DF` and `C4:00E0` were the cleanest later lures on the page and still only weak near-misses
- `C4:0040` died on hard-bad **`02`**
- `C4:00E6` died on hard-bad **`80`**
- `C4:00F0` died on hard-bad **`00`**

What mattered:
- despite the outside pressure, the page produced only one tiny local cluster: `C4:0090..C4:0099`
- owner backtrack scattered across multiple interiors without converging on one obvious owner

Bottom line:
- bank-opening hot page, but still too fragmented to promote honestly

### `C4:0100..C4:01FF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C4:0100` took **three** raw hits and stayed only weak/suspect
- `C4:01E1` took **two** raw hits and stayed **weak**
- `C4:0180` died immediately on hard-bad **`03`**
- strongest owner-backtrack candidate of the early `C4` opening was **`C4:01D2`** for `C4:01D3`
- strongest local clusters were:
  - `C4:01EC..C4:01F2`
  - `C4:01CA..C4:01D5`

Bottom line:
- first page where a real owner-backtrack candidate showed up cleanly, still not enough to promote

### `C4:0200..C4:02FF`
**Page family:** `candidate_code_lane`

This was the best-looking page family of the continuation.

Main lures:
- `C4:027E` took **three** raw hits and stayed **weak**
- `C4:0220` took **two** raw hits and stayed **suspect**
- `C4:0200` died on hard-bad **`00`**
- `C4:0215` and `C4:021F` died on soft-bad **`01`**

What mattered:
- strongest local-control clusters were:
  - **`C4:0293..C4:029D`**
  - `C4:023A..C4:0240`
- owner backtrack produced several plausible interior starts, but nothing that caller pressure and structure both defended together

Bottom line:
- best-looking early `C4` page, still only a near-miss page under the current standard

### `C4:0300..C4:03FF`
**Page family:** `candidate_code_lane`

What mattered:
- `C4:0300` took **two** raw hits and stayed **weak**
- `C4:0303` also took **two** raw hits and remained mixed weak/suspect
- `C4:0351` was the cleanest later lure and still only **suspect**
- `C4:0355` died on soft-bad **`01`**
- `C4:0380` and `C4:03BE` died on hard-bad **`00`**
- strongest backtracked owner candidate of the whole continuation was **`C4:0347`**

Bottom line:
- candidate-code page with the cleanest owner-backtrack of the block, still not promotable yet

### `C4:0400..C4:04FF`
**Page family:** `candidate_code_lane`

This was the busiest closing page of the continuation.

Main lures:
- `C4:0400` took **three** raw hits and stayed only weak/suspect
- `C4:0408`, `C4:0480`, and `C4:04DF` each took **two** raw hits and still only remained weak/suspect
- `C4:0414` died on soft-bad **`01`**
- `C4:0404` died on hard-bad **`00`**

What mattered:
- strongest owner-backtrack candidate on the page was **`C4:049D`** for `C4:04A4`
- strongest local clusters were:
  - **`C4:0497..C4:04A4`**
  - `C4:0405..C4:0410`
  - `C4:041B..C4:0422`

Why it still failed:
- this page had real pressure and real local structure, but still not one start that caller quality, start quality, and structure all defended together cleanly

Bottom line:
- hottest page of the opening `C4` block, still only a near-miss

---

## Key truths preserved by this continuation
- `C3:FB00` is the cleanest surviving late-`C3` lure and still does not defend ownership
- `C3:FE10` is the cleanest closing-bank `C3` lure and still falls short
- `C3:FF00..FFFF` behaves like dead tail material at the bank edge, not a late hidden rescue lane
- `C4:0000`, `C4:0002`, and `C4:0010` all take heavy raw pressure immediately after the bank transition and still do not converge on one defendable owner
- `C4:0040`, `C4:00E6`, and `C4:00F0` prove that the opening `C4` frontier also contains hard-bad bait on `02`, `80`, and `00`
- `C4:01D2` is the strongest early owner-backtrack candidate of the opening `C4` block and still not enough
- `C4:027E` is the strongest repeated-hit lure on the best-looking early `C4` page and still remains only a near-miss
- `C4:0347` is the strongest owner-backtrack candidate of the continuation and still not defensible as a promotion
- `C4:0400`, `C4:0480`, and `C4:04DF` make `C4:0400..04FF` the hottest page of the continuation and still no start survives promotion cleanly

---

## Result
- Seam advanced from **`C3:FB00..`** to **`C4:0500..`**
- Bank `C3` has now been swept through the end-of-bank boundary under the current conservative seam workflow
- No new labels promoted
- Label space remains clean
