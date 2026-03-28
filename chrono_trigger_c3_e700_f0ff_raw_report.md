# Chrono Trigger C3 seam raw report — C3:E700..C3:F0FF

## Scope
- Continuation from live seam: `C3:E700..`
- Conservative forward sweep across the next ten pages
- Local toolkit executed from the staged branch copy in the workspace
- Workspace caller anchoring remained conservative because the full pass-manifest history is still not mirrored locally; nothing in this block earned promotion anyway

## Bottom line
- Closed: `C3:E700..C3:F0FF`
- Promotions: **none**
- New live seam: **`C3:F100..`**

This block produced several believable near-misses:
- a three-lure mixed page at `E800`
- the busiest early outside-pressure page of the continuation at `E900`
- a pure local-control page at `EA00`
- a broad mixed false-dawn page at `EB00`
- a hard-bad branch-fed page at `EE00`
- the strongest local-only structure of the continuation at `EF00`
- the busiest overall xref page of the block at `F000`

None of them defended honest ownership.

---

## Page-by-page triage

### `C3:E700..C3:E7FF`
**Page family:** `mixed_command_data`

What mattered:
- no meaningful raw caller traction survived on the page
- no local islands or merged clusters survived scoring

Bottom line:
- quiet mixed page, seam moved through cleanly

### `C3:E800..C3:E8FF`
**Page family:** `mixed_command_data`

What mattered:
- `C3:80D2 -> C3:E800` was the cleanest page-start lure and still only **weak**
- `C3:8F4E -> C3:E810` and `C3:D4EA -> C3:E818` were also only **weak**
- owner backtrack stayed pinned directly on `C3:E800`
- the late page never produced any meaningful local clusters

Why it failed:
- the page split into three modest weak lures with no structural ownership behind any of them
- even the cleanest page-start landing at `E800` still carried high target-side noise

Bottom line:
- three-lure mixed page, still no promotion

### `C3:E900..C3:E9FF`
**Page family:** `mixed_command_data`

This was the busiest early outside-pressure page of the continuation.

Main lures:
- `C3:D525 -> C3:E928` was the cleanest page lure and stayed **weak**
- `C3:9DA2 -> C3:E92E` died as a **soft-bad** landing on `01`
- `C3:DB2C`, `C3:DBD3`, and `C3:DC7F` all landed on **`C3:E938`**, making it the strongest repeated-hit lure of the early block, and it still stayed only **suspect**
- `C3:73D1 -> C3:E910` also remained only **suspect**

What mattered:
- owner backtrack preferred `C3:E927` for both `E928` and `E92E`
- owner backtrack preferred `C3:E90B` for the `E910` landing
- the page produced **no meaningful local clusters**

Bottom line:
- strongest early repeated-hit page of the block, still no defendable owner boundary

### `C3:EA00..C3:EAFF`
**Page family:** `mixed_command_data`

What mattered:
- no meaningful outside pressure survived on the page
- strongest local-control cluster was **`C3:EAA8..C3:EAC0`**

Bottom line:
- pure local-control page; structure only, not ownership

### `C3:EB00..C3:EBFF`
**Page family:** `mixed_command_data`

This was the broadest mixed false-dawn page of the middle block.

Main lures:
- `C8:F967 -> C3:EB10` was the cleanest lure on the page and still only **weak**
- `C3:4F62 -> C3:EB00` also stayed **weak**
- `C3:4B59 -> C3:EB00` degraded to **suspect**
- `C3:13F8` and `C3:15ED` both landed on **`C3:EB7B`**, and both remained only **suspect**

What mattered:
- owner backtrack stayed pinned directly on `C3:EB00`
- owner backtrack preferred `C3:EB79` for `EB7B`
- the page produced **no meaningful local clusters**

Bottom line:
- several believable mixed lures, still no owner-backed promotion

### `C3:EC00..C3:ECFF`
**Page family:** `mixed_command_data`

What mattered:
- `C3:0A42 -> C3:EC10` was the only raw lure on the page and stayed **suspect**
- owner backtrack preferred `C3:EC0E`
- no local islands or clusters survived scoring

Bottom line:
- one weak page lure with no structural support

### `C3:ED00..C3:EDFF`
**Page family:** `mixed_command_data`

What mattered:
- no meaningful raw caller traction survived on the page
- no local islands or merged clusters survived scoring

Bottom line:
- another quiet mixed page, seam moved through cleanly

### `C3:EE00..C3:EEFF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C3:3B95 -> C3:EE0A` died immediately because the landing byte is **`00`**
- `C3:6A33 -> C3:EE60` died immediately because the landing byte is **`80`**
- `C3:D7F1 -> C3:EE0C` was the only surviving page lure and still stayed only **suspect**
- owner backtrack preferred `C3:EE5E` for `EE60`, but that still did not rescue ownership
- the page produced **no meaningful local clusters**

Bottom line:
- branch-fed page with two hard-bad landings and one suspect survivor; still no promotion

### `C3:EF00..C3:EFFF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- no meaningful outside pressure survived on the page
- this was the strongest local-only structure page of the continuation
- strongest local clusters were:
  - **`C3:EFC8..C3:EFD2`**
  - `C3:EFE0..C3:EFEA`
  - `C3:EFB3..C3:EFB9`

Why it failed:
- all of the motion on the page remained purely local
- even the strongest cluster stayed only structure without caller-backed ownership

Bottom line:
- strongest local-only page of the block, still not promotable

### `C3:F000..C3:F0FF`
**Page family:** `branch_fed_control_pocket`

This was the busiest overall xref page of the continuation.

Main lures:
- `C3:F001` drew **nine** raw hits and was the busiest non-garbage landing on the page; it still remained only a weak/suspect near-miss mix
- `C3:F040` drew **seven** raw hits and died immediately because the landing byte is **`00`**
- `C3:F009` took three raw hits and still only stayed **weak**
- `C3:F064` took three raw hits and still only stayed weak/suspect
- `C3:F0A4`, `C3:F0A5`, and `C3:F0A6` were the cleanest late clean-start lures of the page and still remained only **weak**
- `C3:F058`, `C3:F070`, and `C3:F0C5` were additional hard-bad landings on **`00`**

What mattered:
- owner backtrack preferred:
  - `C3:F01D` for `F01D`
  - `C3:F01C` for `F020`
  - `C3:F08B` for both `F08D` and `F092`
  - `C3:F0DF` for `F0E0`
- strongest local-control clusters were:
  - **`C3:F07A..C3:F084`**
  - `C3:F0DF..C3:F0F7`
  - `C3:F062..C3:F06C`

Why it failed:
- the page mixed real outside pressure with multiple repeated hard-bad zero landings
- the cleanest late lures at `F0A4..F0A6` still had only weak caller support
- the strongest local clusters did not converge with the outside pressure into one defendable owner boundary

Bottom line:
- busiest page of the block, still no honest promotion

---

## Key truths preserved by this continuation
- `C3:E800`, `C3:E810`, and `C3:E818` are all real-looking opening-page lures and still do not defend ownership
- `C3:E928` is the cleanest early lure of the continuation and still only a near-miss
- `C3:E92E` is a soft-bad lure on `01`
- `C3:E938` is the strongest repeated-hit early lure of the block and still not enough
- `C3:EAA8..C3:EAC0` is the strongest pure local-control cluster of the mid block and still only structure
- `C3:EE0A` and `C3:EE60` show another pair of hard-bad false dawns on `00` and `80`
- `C3:EFC8..C3:EFD2` is the strongest local-only cluster of the continuation and still does **not** own itself honestly
- `C3:F040` proves again that repeated outside pressure can keep landing on obvious garbage
- `C3:F001` is the busiest non-garbage landing of the continuation and still falls short of promotion
- `C3:F0A4..C3:F0A6` are the cleanest late clean-start lures on the busiest page and still lack real ownership support

---

## Result
- Seam advanced from **`C3:E700..`** to **`C3:F100..`**
- No new labels promoted
- Label space remains clean
