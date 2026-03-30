# Chrono Trigger C3 seam raw report — C3:BF00..C3:C8FF

## Scope
- Continuation from Session 14 live seam: `C3:BF00..`
- Conservative ROM-first seam triage using the Session 14 v5 heuristics mirrored locally from the branch toolkit
- Local repo checkout / manifests were not present in the workspace, so caller anchor status was treated conservatively unless raw evidence invalidated the landing directly

## Bottom line
- Closed: `C3:BF00..C3:C8FF`
- Promotions: **none**
- New live seam: **`C3:C900..`**
- Rationale: this block produced repeated **branch-fed control pockets, local splinters, and interior-hit bait**, but no page where caller quality, start-byte quality, and local ownership all aligned strongly enough to justify a code promotion

---

## Page-by-page triage

### `C3:BF00..C3:BFFF`
**Page family:** `branch_fed_control_pocket`

Raw caller pressure exists, but it is shallow:
- `C3:6985 -> C3:BF00` was the only landing at the page start and remained only a **weak** hit
- `C3:4A66 -> C3:BFAA` was a single-hit interior lure; best owner backtrack was only `C3:BFA9`
- `C3:DE02 -> C3:BF88` degraded to **suspect** due to high caller/target data-side risk

What mattered:
- No local return-anchored cluster survived scoring on the page
- `BF00` itself stayed exposed as a page-start near-miss, not a defendable owner
- `BFAA` and `BF88` looked like isolated interiors, not true routine boundaries

Bottom line:
- no owner/helper promotion survived

### `C3:C000..C3:C0FF`
**Page family:** `candidate_code_lane`

This was the liveliest page of the block, but still not enough to promote honestly.

Main lures:
- `C3:5352 -> C3:C0A9` was the cleanest raw hit on the page and stayed only **weak**
- `C3:8530 -> C3:C0A8` died immediately because the landing byte is **`00`**
- `C3:5C9C -> C3:C017` degraded because the landing byte is soft-bad **`09`**
- `C3:906C -> C3:C022` and `C3:DFD8 -> C3:C004` remained **suspect**

Strongest local structure:
- owner backtrack repeatedly preferred **`C3:C09E`** for the `C0A8/C0A9` pair
- strongest local cluster was **`C3:C096..C3:C0A4`**

Why it still failed:
- the best outside pressure lands **inside** the `C096..C0A4` pocket, not on a defended owner boundary
- one paired landing is hard-bad (`C0A8 = 00`)
- the page behaves like a control pocket with interior-fed entries, not a clean callable lane

Bottom line:
- strongest near-miss of the continuation so far, but still not promotable

### `C3:C100..C3:C1FF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- no meaningful raw caller traction survived on the page
- strongest local cluster was **`C3:C120..C3:C129`**
- secondary pocket `C3:C1DC..C3:C1E3` scored well structurally but was ASCII-heavy and caller-free

Bottom line:
- local-control-only page; no caller-backed ownership

### `C3:C200..C3:C2FF`
**Page family:** `branch_fed_control_pocket`

This page had the strongest broad local structure of the block.

Main lures:
- `C3:0C62 -> C3:C248` stayed **suspect**
- `C3:FD20 -> C3:C2D0` stayed **suspect**

Strongest local structure:
- owner backtrack preferred **`C3:C244`** for `C248`
- owner backtrack preferred **`C3:C2C2`** for `C2D0`
- strongest merged local cluster was **`C3:C2BA..C3:C2F2`**

Why it still failed:
- both raw caller neighborhoods and target neighborhoods scored high-risk
- the big local cluster is real as structure, but it still does not own itself honestly
- no target gained clean caller-backed executable status

Bottom line:
- strongest local-control page of the continuation, still not enough

### `C3:C300..C3:C3FF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C3:419A -> C3:C3C6` was the cleanest page lure and still only **weak**
- owner backtrack preferred **`C3:C3BE`**
- strongest cluster was **`C3:C3B9..C3:C3D1`**

Why it failed:
- the cluster is ASCII-heavy (`~0.52`)
- no stable caller-backed owner boundary emerged

Bottom line:
- local splinter only

### `C3:C400..C3:C4FF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C3:B160 -> C3:C410` was the only meaningful raw lure and stayed **suspect**
- owner backtrack preferred **`C3:C40E`**
- only tiny local pockets survived scoring: `C3:C425..C3:C42D` and `C3:C481..C3:C485`

Bottom line:
- single-hit false dawn with only tiny unsupported pockets behind it

### `C3:C500..C3:C5FF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C3:D80F -> C3:C500` was the page-start lure and still only **suspect**
- strongest local cluster was **`C3:C5B5..C3:C5C6`**
- secondary cluster `C3:C5C9..C3:C5D1` was even more ASCII-heavy

Bottom line:
- page-start pressure existed, but the page never defended code ownership

### `C3:C600..C3:C6FF`
**Page family:** `mixed_command_data`

What mattered:
- `C3:AE62 -> C3:C6F6` was the only raw hit and remained **weak**
- owner backtrack preferred **`C3:C6F2`**
- strongest local cluster was **`C3:C6D7..C3:C6F8`**

Why it failed:
- the whole late-page pocket is very ASCII-heavy (`~0.647`)
- this looks like mixed command/data with an attractive late interior, not a callable owner

Bottom line:
- no promotion survived

### `C3:C700..C3:C7FF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- no meaningful raw caller traction survived
- strongest clusters were:
  - **`C3:C7B1..C3:C7C7`**
  - `C3:C77B..C3:C78B`
  - `C3:C79B..C3:C7AD`

Bottom line:
- multiple local splinters, no caller-backed start

### `C3:C800..C3:C8FF`
**Page family:** `branch_fed_control_pocket`

Main lures:
- `C3:6D0B -> C3:C850` stayed **suspect**
- one raw landing at **`C3:C8D0 = 00`** died immediately on hard-bad start quality
- strongest owner-backtrack late-page near-miss was **`C3:C8F0 -> C3:C8F1`**

Strongest local structure:
- **`C3:C8F3..C3:C8FE`**

Why it failed:
- the page mixes another hard-bad landing with a late local splinter
- nothing on the page gained defendable caller-backed ownership

Bottom line:
- no promotion survived

---

## Key truths preserved by this continuation
- `C3:BF00` had real raw pressure and still did **not** earn ownership
- `C3:C000` is the strongest near-miss page of this block; `C3:C09E..C3:C0A4` is structural, but still not an honest promoted owner
- `C3:C100` and `C3:C700` are local-control-only pages in this continuation
- `C3:C2BA..C3:C2F2` is a strong local-control cluster and still does **not** own itself honestly
- `C3:C6D7..C3:C6F8` is a classic late-page attractive interior inside a mixed lane, not a defendable owner
- `C3:C8D0` is a hard-bad landing on `00`

---

## Result
- Seam advanced from **`C3:BF00..`** to **`C3:C900..`**
- No new labels promoted
- Repo label space stays clean
