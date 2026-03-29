# Chrono Trigger seam raw report — C4:0500..C4:0EFF

## Scope
- Continuation from live seam: `C4:0500..`
- Conservative forward sweep across the next ten pages of bank `C4`
- Upgraded fast-path toolkit logic reused locally for the block sweep
- Caller anchoring in the workspace remained conservative because the full manifest history is still not mirrored locally

## Bottom line
- Closed: `C4:0500..C4:0EFF`
- Promotions: **none**
- New live seam: **`C4:0F00..`**

This continuation stayed hotter than the late `C3` frontier, but it still did not yield a defendable owner.

The main patterns were:
- an opening candidate-code page with a hard-bad repeated lure at `C4:0520`
- a mixed page at `C4:0600` where the cleanest-looking repeated lure still sat next to multiple hard-bad starts
- another busy mixed page at `C4:0700` led by repeated pressure on `C4:070A`
- a strong candidate-code near-miss page at `C4:0800`
- a branch-fed page at `C4:0900` with thin caller pressure and stronger local structure than outside ownership
- the hottest page of the continuation at `C4:0A00`
- a pure local-control pocket at `C4:0B00`
- a broad branch-fed near-miss page at `C4:0C00`
- a quieter mixed page at `C4:0D00`
- a closing candidate-code page at `C4:0E00`

None of them cleared the promotion standard.

---

## Page-by-page triage

### `C4:0500..C4:05FF`
**Page family:** `candidate_code_lane`

What mattered:
- `C4:0520` took **two** raw hits and died immediately because the landing byte is **`02`**
- `C4:0502`, `C4:0551`, and `C4:05F8` were the cleanest surviving lures and each stayed only **weak**
- `C4:057A` and `C4:0582` looked alive at byte level and still degraded to **suspect** under neighborhood risk
- strongest owner-backtrack candidate was **`C4:0575`** for both `C4:057A` and `C4:0582`
- strongest local-control cluster was **`C4:05BD..C4:05C4`**

Bottom line:
- clean-looking opening page with a hard-bad repeated lure and no defendable owner behind the survivors

### `C4:0600..C4:06FF`
**Page family:** `mixed_command_data`

What mattered:
- `C4:0650` took **two** raw hits and stayed only **weak**
- `C4:0660` took **two** raw hits and died immediately on hard-bad **`00`**
- `C4:060B`, `C4:061F`, and `C4:0628` were additional hard-bad false dawns on **`00`**
- strongest owner-backtrack candidate was **`C4:0617`** for `C4:061F`
- strongest local-control cluster was **`C4:06B1..C4:06BC`**

Bottom line:
- messy mixed page where the cleanest repeated lure still sat inside a field full of obvious bad starts

### `C4:0700..C4:07FF`
**Page family:** `mixed_command_data`

What mattered:
- `C4:070A` took **three** raw hits and stayed only **weak**
- `C4:0745`, `C4:0760`, `C4:0780`, and `C4:07EC` were all single weak near-misses
- `C4:0700` and `C4:0714` both died immediately on hard-bad **`00`**
- strongest owner-backtrack candidates were:
  - **`C4:073D`** for `C4:0745`
  - `C4:075B` for `C4:0760`
- strongest local-control cluster was **`C4:073C..C4:074C`**

Bottom line:
- busy mixed page with repeated attention on `C4:070A`, still not enough to defend an owner boundary

### `C4:0800..C4:08FF`
**Page family:** `candidate_code_lane`

This was one of the strongest pages of the continuation.

What mattered:
- `C4:0800` took **four** raw hits and stayed only **weak**
- `C4:0830` took **two** raw hits and also stayed **weak**
- `C4:0848` took **two** raw hits and degraded to **suspect**
- `C4:0818` and `C4:081F` both died on hard-bad starts (`00` and `60`)
- strongest owner-backtrack candidates were:
  - **`C4:0810`** for `C4:0812` and `C4:0818`
  - `C4:085E` for `C4:085F`
  - `C4:08B7` for `C4:08BD` and `C4:08C1`
- strongest local-control clusters were:
  - **`C4:0808..C4:0816`**
  - `C4:0893..C4:08A2`

Bottom line:
- strong candidate-code near-miss page with real local structure, still no caller-backed owner that held cleanly

### `C4:0900..C4:09FF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C4:0920` and `C4:0930` were the only page lures and both stayed **suspect**
- strongest owner-backtrack candidate was **`C4:0920`** for `C4:0930`
- strongest local-control cluster was **`C4:096F..C4:0982`**

Bottom line:
- branch-fed pocket with light outside traction and stronger local structure than ownership evidence

### `C4:0A00..C4:0AFF`
**Page family:** `candidate_code_lane`

This was the hottest page of the continuation.

What mattered:
- `C4:0A00` took **two** raw hits and stayed only **weak**
- `C4:0A5B` and `C4:0AA0` were the cleanest later lures and both stayed **weak**
- `C4:0A50` and `C4:0AE0` were soft-bad false dawns on **`01`**
- `C4:0A01` died immediately on hard-bad **`80`**
- strongest owner-backtrack candidates were:
  - **`C4:0A54`** for `C4:0A5B`
  - **`C4:0A99`** for `C4:0AA0`
  - `C4:0ADB` for `C4:0AE0`
- strongest local-control clusters were:
  - **`C4:0A06..C4:0A24`**
  - `C4:0AEC..C4:0AF4`

Bottom line:
- hottest page of the block, with real structure and several believable lures, still no start survived promotion cleanly

### `C4:0B00..C4:0BFF`
**Page family:** `mixed_command_data`

What mattered:
- no meaningful outside pressure survived on the page
- strongest local-control clusters were:
  - **`C4:0B00..C4:0B12`**
  - `C4:0B32..C4:0B44`
  - `C4:0BCE..C4:0BE7`

Bottom line:
- pure local-control page; structure only, not ownership

### `C4:0C00..C4:0CFF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C4:0C8A` took **two** raw hits and stayed **weak**
- `C4:0C00`, `C4:0C0F`, `C4:0C90`, and `C4:0CE0` were all single weak near-misses
- `C4:0CC6` looked cleaner at byte level and still degraded to **suspect**
- strongest owner-backtrack candidates were:
  - **`C4:0C0B`** for `C4:0C0F`
  - `C4:0CBB` for `C4:0CC6`
  - `C4:0CDA` for `C4:0CE0`
- strongest local-control cluster was **`C4:0CBA..C4:0CC2`**

Bottom line:
- broad branch-fed near-miss page, still no stable owner boundary

### `C4:0D00..C4:0DFF`
**Page family:** `mixed_command_data`

What mattered:
- `C4:0D05` and `C4:0D0F` were single **weak** lures
- `C4:0D20` degraded to **suspect**
- strongest owner-backtrack candidate was **`C4:0D04`** for both `C4:0D05` and `C4:0D0F`
- strongest local-control cluster was **`C4:0D8D..C4:0DA0`**

Bottom line:
- quieter mixed page with a few believable starts, still not enough

### `C4:0E00..C4:0EFF`
**Page family:** `candidate_code_lane`

What mattered:
- `C4:0EC7` took **two** raw hits and stayed **weak**
- `C4:0EA0` was a single later **weak** lure
- `C4:0E10` died immediately on hard-bad **`03`**
- strongest owner-backtrack candidate of the closing page was **`C4:0E91`** for `C4:0EA0`
- strongest local-control clusters were:
  - **`C4:0E7A..C4:0E96`**
  - `C4:0E50..C4:0E6B`

Bottom line:
- strong closing candidate-code page with real structure, still no defensible promotion

---

## Key truths preserved by this continuation
- `C4:0520` is an early repeated hard-bad false dawn on `02`
- `C4:0575` is the strongest owner-backtrack candidate of the opening page and still not enough to promote
- `C4:0650` is the cleanest repeated lure on `C4:0600` and still sits next to multiple hard-bad false dawns
- `C4:070A` is the strongest repeated-hit lure of the early block and still falls short of ownership
- `C4:0800..08FF` is one of the best-looking pages of the continuation and still does not hand over one clean caller-backed owner
- `C4:0A00..0AFF` is the hottest page of the block
- `C4:0A50` and `C4:0AE0` are soft-bad lures on `01`
- `C4:0A54` and `C4:0A99` are the strongest owner-backtrack candidates of the continuation and still not defensible as promotions
- `C4:0B00..0BFF` is pure local-control structure without outside ownership
- `C4:0E7A..0E96` is the strongest closing local-control cluster of the block and still only structure

---

## Result
- Seam advanced from **`C4:0500..`** to **`C4:0F00..`**
- No new labels promoted
- Label space remains clean
