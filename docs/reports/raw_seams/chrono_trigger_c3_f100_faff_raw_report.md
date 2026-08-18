# Chrono Trigger C3 seam raw report — C3:F100..C3:FAFF

## Scope
- Continuation from live seam: `C3:F100..`
- Conservative forward sweep across the next ten pages
- Local toolkit executed from the staged branch copy in the workspace
- Workspace caller anchoring remained conservative because the full pass-manifest history is still not mirrored locally; nothing in this block earned promotion anyway

## Bottom line
- Closed: `C3:F100..C3:FAFF`
- Promotions: **none**
- New live seam: **`C3:FB00..`**

This block produced several believable near-misses:
- a hard-bad early page at `F100`
- a clean single-hit page at `F200`
- a busy mixed false-dawn page at `F400`
- the strongest pure local-control page of the continuation at `F500`
- a three-lure mixed page at `F600`
- a branch-fed page with page-start pressure at `F700`
- the busiest repeated-hit false-dawn page of the continuation at `F800`
- a soft-bad closing-page lure at `F9F0`

None of them defended honest ownership.

---

## Page-by-page triage

### `C3:F100..C3:F1FF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C3:094E -> C3:F1A5` died immediately because the landing byte is **`00`**
- `C3:1825 -> C3:F1AD` was the only surviving lure and still only **weak**
- owner backtrack preferred **`C3:F1A3`** for the bad `F1A5` landing
- strongest local-control pocket was `C3:F17C..C3:F180`

Bottom line:
- early hard-bad false dawn plus one weak survivor; still no promotion

### `C3:F200..C3:F2FF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C3:3D52 -> C3:F2DA` was the only raw lure on the page and stayed **weak**
- owner backtrack preferred **`C3:F2D9`**
- no local islands or merged clusters survived scoring

Bottom line:
- clean single-hit near-miss with no structural support

### `C3:F300..C3:F3FF`
**Page family:** `mixed_command_data`

What mattered:
- no meaningful raw caller traction survived
- no local islands or clusters survived scoring

Bottom line:
- quiet mixed page, seam moved through cleanly

### `C3:F400..C3:F4FF`
**Page family:** `mixed_command_data`

This was the busiest mixed false-dawn page of the continuation.

Main lures:
- `C3:31E3 -> C3:F400` and `C3:51F5 -> C3:F400` both died immediately because the landing byte is **`03`**
- `C3:2BA8 -> C3:F4AC` was the cleanest surviving lure and stayed **weak**
- `C3:4A6D -> C3:F4C0` and `C3:6648 -> C3:F460` both degraded to **suspect**

What mattered:
- owner backtrack preferred:
  - **`C3:F4AB`** for `F4AC`
  - `C3:F4C0` for `F4C0`
  - `C3:F451` for `F460`
- the page produced **no meaningful local clusters**

Bottom line:
- repeated hard-bad pressure plus two dirtier survivors; still no defendable owner boundary

### `C3:F500..C3:F5FF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- no meaningful outside pressure survived on the page
- this was the strongest pure local-control page of the continuation
- strongest local clusters were:
  - **`C3:F56F..C3:F579`**
  - `C3:F586..C3:F58E`
  - `C3:F59B..C3:F5A3`

Bottom line:
- strongest local-only structure of the block, still only structure and not ownership

### `C3:F600..C3:F6FF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C3:0A64 -> C3:F685` was the cleanest weak lure of the page
- `C3:4E2D -> C3:F6A2` also stayed **weak**
- `C3:DF74 -> C3:F618` degraded to **suspect**
- owner backtrack preferred:
  - **`C3:F618`** for `F618`
  - `C3:F685` for `F685`
  - `C3:F69F` for `F6A2`
- strongest local-control pockets were `C3:F6D6..C3:F6DC` and `C3:F6EB..C3:F6F1`, both heavily ASCII-skewed

Bottom line:
- three-lure mixed page, still no owner-backed promotion

### `C3:F700..C3:F7FF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C3:ADA3 -> C3:F700` was the cleanest page-start lure and stayed **weak**
- `C3:6440 -> C3:F708` degraded to **suspect**
- owner backtrack preferred:
  - **`C3:F700`** for `F700`
  - **`C3:F701`** for `F708`
- strongest local clusters were:
  - `C3:F700..C3:F706`
  - `C3:F748..C3:F74E`
  - `C3:F75D..C3:F763`
  - `C3:F772..C3:F778`

Bottom line:
- branch-fed page with one page-start near-miss and strong local structure, still not enough

### `C3:F800..C3:F8FF`
**Page family:** `branch_fed_control_pocket`

This was the busiest repeated-hit false-dawn page of the continuation.

Main lures:
- `C3:E7FD -> C3:F800` and `C3:EF5B -> C3:F800` both died immediately because the landing byte is **`FF`**
- `C3:8622 -> C3:F8BD` died immediately because the landing byte is **`00`**
- `C3:4D05 -> C3:F88E` died as a **soft-bad** landing on `01`
- `C3:20D7 -> C3:F842` was the cleanest surviving lure and still degraded to **suspect**

What mattered:
- owner backtrack preferred **`C3:F8BB`** for `F8BD`
- strongest local-control pocket was `C3:F8CC..C3:F8D2`

Bottom line:
- repeated hard-bad pressure with one soft-bad lure and one surviving near-miss; still no promotion

### `C3:F900..C3:F9FF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C3:14C3 -> C3:F9F0` was the only raw lure on the page
- it died as a **soft-bad** landing on `01`
- owner backtrack preferred **`C3:F9E2`**
- only local support was a tiny pocket at `C3:F908..C3:F90D`

Bottom line:
- single soft-bad closing-page false dawn

### `C3:FA00..C3:FAFF`
**Page family:** `mixed_command_data`

What mattered:
- `C3:55A3 -> C3:FA0C` was the cleanest early lure and stayed **weak**
- `C3:91EB -> C3:FAB0` degraded to **suspect**
- owner backtrack preferred:
  - `C3:FA00` for `FA0C`
  - **`C3:FAA0`** for `FAB0`
- no local islands or clusters survived scoring

Bottom line:
- modest closing page with two weak/suspect lures and no structural ownership

---

## Key truths preserved by this continuation
- `C3:F1A5` is a hard-bad false dawn on `00`
- `C3:F1AD` is the only surviving lure on the first page and still not enough
- `C3:F2DA` is the cleanest single-hit near-miss of the early block and still lacks structural support
- `C3:F400` proves again that repeated outside pressure can land on obvious garbage, here on hard-bad `03`
- `C3:F56F..C3:F579` is the strongest pure local-control cluster of the continuation and still only structure
- `C3:F618`, `C3:F685`, and `C3:F6A2` are all believable mid-block lures and still do not defend ownership
- `C3:F701` is the strongest backtracked owner candidate of the continuation and still not defensible as a promotion
- `C3:F800` and `C3:F8BD` show repeated hard-bad landings on `FF` and `00`
- `C3:F88E` and `C3:F9F0` are soft-bad lures on `01`
- `C3:FA0C` is the cleanest closing-page lure of the block and still falls short of promotion

---

## Result
- Seam advanced from **`C3:F100..`** to **`C3:FB00..`**
- No new labels promoted
- Label space remains clean
