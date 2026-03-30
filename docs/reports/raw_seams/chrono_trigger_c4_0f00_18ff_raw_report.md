# Chrono Trigger seam raw report — C4:0F00..C4:18FF

## Scope
- Continuation from live seam: `C4:0F00..`
- Conservative forward sweep across the next ten pages of bank `C4`
- Upgraded fast-path toolkit logic reused locally for the block sweep
- Caller anchoring in the workspace remained conservative because the full manifest history is still not mirrored locally

## Bottom line
- Closed: `C4:0F00..C4:18FF`
- Promotions: **none**
- New live seam: **`C4:1900..`**

This continuation stayed hot and code-shaped, but still did not yield a start that caller quality, start-byte quality, and local structure all defended together cleanly enough to promote.

The main patterns were:
- an opening mixed page at `C4:0F00` with repeated pressure on `C4:0F01`
- the busiest overall xref page of the continuation at `C4:1000`
- a strong candidate-code near-miss page at `C4:1100`
- a thin candidate-code page at `C4:1200`
- a local-structure-heavy candidate-code page at `C4:1300`
- cleaner near-miss pages at `C4:1400`, `C4:1500`, and `C4:1600`
- a dense candidate-code/local-structure page at `C4:1700`
- the strongest closing repeated-hit candidate-code page at `C4:1800`

None of them cleared the promotion standard.

---

## Page-by-page triage

### `C4:0F00..C4:0FFF`
**Page family:** `mixed_command_data`

What mattered:
- `C4:0F01` took **two** raw hits and stayed only **weak**
- `C4:0F00`, `C4:0F02`, and `C4:0F03` were additional single weak near-misses
- `C4:0F56` died immediately because the landing byte is **`00`**
- owner backtrack stayed pinned directly on **`C4:0F00`** for the `0F01/0F02/0F03` cluster
- strongest local-control cluster was **`C4:0FA4..C4:0FAA`**

Bottom line:
- opening mixed page with repeated pressure on a small interior group, still no defendable owner boundary

### `C4:1000..C4:10FF`
**Page family:** `branch_fed_control_pocket`

This was the busiest overall xref page of the continuation.

What mattered:
- `C4:1020` took **three** raw hits and all three died immediately because the landing byte is **`00`**
- `C4:1027` took **two** raw hits and remained only a weak/suspect mix
- `C4:1000` was the cleanest page-start lure and still only **weak**
- `C4:1010` also stayed **weak**, while `C4:1002` degraded to **suspect**
- strongest owner-backtrack candidates were:
  - **`C4:10FE`** for `C4:10FF`
  - `C4:10EC` for `C4:10EC`
  - `C4:100F` for `C4:1010`
- strongest local-control clusters were:
  - **`C4:10B1..C4:10B5`**
  - `C4:10F4..C4:10FF`
  - `C4:1023..C4:1028`

Bottom line:
- hottest page of the block by raw pressure, still too fragmented and too dirty to promote honestly

### `C4:1100..C4:11FF`
**Page family:** `candidate_code_lane`

What mattered:
- `C4:110D` took **two** raw hits and stayed **weak**
- `C4:1116`, `C4:1198`, and `C4:11F4` were all single weak near-misses
- `C4:11F1` died immediately on hard-bad **`02`**
- strongest owner-backtrack candidates were:
  - **`C4:1111`** for `C4:1116`
  - `C4:11EE` for `C4:11F1`
- strongest local-control cluster was **`C4:1159..C4:115F`**

Bottom line:
- strong candidate-code near-miss page, still no start that all three signals defended together

### `C4:1200..C4:12FF`
**Page family:** `candidate_code_lane`

What mattered:
- `C4:1211` died immediately on hard-bad **`03`**
- `C4:1249` was the only surviving clean-start lure and still degraded to **suspect**
- strongest owner-backtrack candidates were:
  - **`C4:1204`** for `C4:1211`
  - `C4:1248` for `C4:1249`
- strongest local-control cluster was **`C4:129A..C4:12A0`**

Bottom line:
- thin candidate-code page with one hard-bad lure and one surviving near-miss, still not enough

### `C4:1300..C4:13FF`
**Page family:** `candidate_code_lane`

What mattered:
- `C4:132C` was the only raw lure on the page and died immediately because the landing byte is **`FF`**
- strongest owner-backtrack candidate was **`C4:131C`**
- strongest local-control clusters were:
  - **`C4:136E..C4:1375`**
  - `C4:13BF..C4:13C8`
  - `C4:138D..C4:1398`

Bottom line:
- code-shaped page with real local structure, but all outside pressure died on hard-bad `FF`

### `C4:1400..C4:14FF`
**Page family:** `candidate_code_lane`

What mattered:
- `C4:1400` was a clean single-hit page-start lure and still only **weak**
- `C4:1488` was the cleanest later lure and also stayed **weak**
- strongest owner-backtrack candidates were:
  - **`C4:1478`** for `C4:1488`
  - `C4:1400` for `C4:1400`
- strongest local-control clusters were:
  - `C4:1415..C4:1421`
  - **`C4:14E4..C4:14EC`**
  - `C4:14C6..C4:14CC`

Bottom line:
- cleaner candidate-code page than most of late `C3`, still no defendable promoted owner

### `C4:1500..C4:15FF`
**Page family:** `candidate_code_lane`

What mattered:
- `C4:151D` and `C4:15D8` were both single **weak** near-misses
- `C4:155F` died immediately on hard-bad **`80`**
- strongest owner-backtrack candidates were:
  - **`C4:1517`** for `C4:151D`
  - `C4:15D8` for `C4:15D8`
- strongest local-control cluster was **`C4:15C1..C4:15D1`**

Bottom line:
- candidate-code page with one hard-bad lure and one strong local cluster, still no caller-backed ownership

### `C4:1600..C4:16FF`
**Page family:** `candidate_code_lane`

What mattered:
- `C4:1606` and `C4:1611` were both single **weak** lures
- `C4:164E` looked cleaner at byte level and still degraded to **suspect**
- strongest owner-backtrack candidate of the continuation was **`C4:160D`** for `C4:1611`
- strongest local-control clusters were:
  - **`C4:16C4..C4:16D2`**
  - `C4:1635..C4:163E`

Bottom line:
- one of the strongest pages of the block, still not enough to justify promotion under the current conservative anchor posture

### `C4:1700..C4:17FF`
**Page family:** `candidate_code_lane`

What mattered:
- `C4:174C` and `C4:17BD` both degraded to **suspect**
- `C4:1773` died immediately on hard-bad **`03`**
- strongest owner-backtrack candidates were:
  - **`C4:1748`** for `C4:174C`
  - `C4:176C` for `C4:1773`
- strongest local-control clusters were:
  - **`C4:1701..C4:1717`**
  - `C4:1730..C4:1738`
  - `C4:1750..C4:1754`

Bottom line:
- dense candidate-code/local-structure page, still no outside/local convergence that held cleanly enough to promote

### `C4:1800..C4:18FF`
**Page family:** `candidate_code_lane`

This was the strongest closing repeated-hit page of the continuation.

What mattered:
- `C4:1802` took **two** raw hits and stayed **weak**
- `C4:183C` and `C4:18F2` degraded to **suspect**
- `C4:186C` was the cleanest later weak lure
- strongest owner-backtrack candidates were:
  - **`C4:1838`** for `C4:183C`
  - **`C4:185C`** for `C4:186C`
  - `C4:18EE` for `C4:18F2`
- strongest local-control clusters were:
  - **`C4:1857..C4:1865`**
  - `C4:1847..C4:184D`

Bottom line:
- best closing candidate-code page of the block, still no start where caller pressure, start quality, and structure all lined up cleanly enough to promote

---

## Key truths preserved by this continuation
- `C4:0F01` is the strongest repeated-hit lure of the opening page and still does not defend ownership
- `C4:1000..10FF` is the busiest page of the continuation, and `C4:1020` proves repeated outside pressure can still land on obvious garbage
- `C4:1100..11FF` is a strong candidate-code near-miss page and still does not hand over one clean caller-backed owner
- `C4:1211` and `C4:1773` are hard-bad lures on `03`
- `C4:132C` dies on hard-bad `FF`
- `C4:155F` is a hard-bad lure on `80`
- `C4:160D` is the strongest owner-backtrack candidate of the continuation and still not defensible as a promotion
- `C4:1701..1717` is the strongest broad local-control cluster of the continuation and still only structure
- `C4:1802` is the strongest repeated-hit clean-start lure of the closing page and still falls short of ownership

---

## Result
- Seam advanced from **`C4:0F00..`** to **`C4:1900..`**
- No new labels promoted
- Label space remains clean
