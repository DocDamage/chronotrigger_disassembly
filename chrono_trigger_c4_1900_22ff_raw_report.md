# Chrono Trigger seam raw report — C4:1900..C4:22FF

## Scope
- Continuation from live seam: `C4:1900..`
- Conservative forward sweep across the next ten pages of bank `C4`
- Upgraded fast-path seam logic reused for the block sweep
- Caller anchoring remained conservative because the full manifest history is still not mirrored locally

## Bottom line
- Closed: `C4:1900..C4:22FF`
- Promotions: **none**
- New live seam: **`C4:2300..`**

This continuation stayed hot and code-shaped, but it still did not yield a start where caller quality, start-byte quality, and local structure all lined up cleanly enough to promote.

The main patterns were:
- an opening candidate-code page at `C4:1900` whose repeated pressure still sat on a soft-bad start
- two cleaner single-hit candidate-code pages at `C4:1A00` and `C4:1B00`
- a strong repeated-hit candidate-code near-miss page at `C4:1C00`
- a broader candidate-code/local-structure page at `C4:1E00`
- a mixed near-miss page at `C4:1F00`
- the hottest overall page of the continuation at `C4:2000`
- a cleaner candidate-code page at `C4:2100`
- a messy mixed closing page at `C4:2200`

None of them cleared the promotion standard.

---

## Page-by-page triage

### `C4:1900..C4:19FF`
**Page family:** `candidate_code_lane`

What mattered:
- `C4:1900` took **two** raw hits and both degraded because the landing byte is the soft-bad **`01`**
- `C4:1939` was the only clean-start surviving lure and still stayed only **suspect**
- `C4:19C5` died immediately on hard-bad **`00`**
- `C4:19F8` died immediately on hard-bad **`02`**
- strongest owner-backtrack candidate was **`C4:19F5`** for `C4:19F8`
- strongest local-control clusters were:
  - **`C4:1954..C4:1966`**
  - `C4:1969..C4:1982`

Bottom line:
- code-shaped opening page, but the repeated pressure still sat on a soft-bad start and the clean survivor never gained enough support to promote

### `C4:1A00..C4:1AFF`
**Page family:** `candidate_code_lane`

What mattered:
- `C4:1A09` was the only raw lure on the page and stayed **weak**
- strongest owner-backtrack candidate was **`C4:1A05`**
- strongest local-control cluster was **`C4:1A15..C4:1A22`**

Bottom line:
- clean single-hit candidate-code near-miss with no caller-backed convergence behind it

### `C4:1B00..C4:1BFF`
**Page family:** `candidate_code_lane`

What mattered:
- `C4:1B79` was the only raw lure on the page and stayed **weak**
- strongest owner-backtrack candidate was **`C4:1B6E`**
- strongest local-control clusters were:
  - **`C4:1B9B..C4:1BA9`**
  - `C4:1B6D..C4:1B83`
  - `C4:1B49..C4:1B56`

Bottom line:
- code-shaped page with real local structure, but still only one weak outside lure and no defendable owner boundary

### `C4:1C00..C4:1CFF`
**Page family:** `candidate_code_lane`

This was one of the strongest early pages of the continuation.

What mattered:
- `C4:1C07` took **two** raw hits and stayed **weak**
- `C4:1C1C` took **two** raw hits and remained a mixed weak/suspect near-miss
- `C4:1C04`, `C4:1C10`, `C4:1C20`, `C4:1CE0`, and `C4:1CE3` were additional believable single weak lures
- strongest owner-backtrack candidates were:
  - **`C4:1C04`** for `C4:1C07`
  - `C4:1CE1` for `C4:1CE3`
  - `C4:1C17` for `C4:1C1C`
- strongest local-control cluster was **`C4:1CC1..C4:1CCA`**

Bottom line:
- strongest repeated-hit early code-lane page of the block, still no start that all three signals defended together cleanly enough to promote

### `C4:1D00..C4:1DFF`
**Page family:** `mixed_command_data`

What mattered:
- `C4:1D9F` was the only raw lure on the page and stayed **suspect**
- strongest owner-backtrack candidate was **`C4:1D9E`**
- no meaningful local clusters survived scoring

Bottom line:
- thin mixed near-miss page with no structural support behind the lure

### `C4:1E00..C4:1EFF`
**Page family:** `candidate_code_lane`

This was one of the broadest candidate-code near-miss pages of the continuation.

What mattered:
- `C4:1EA2` and `C4:1EC1` were the cleanest surviving lures; `C4:1EC1` stayed **weak** and `C4:1EA2` still degraded to **suspect**
- `C4:1E00`, `C4:1E04`, `C4:1E08`, and `C4:1EED` were additional suspect near-misses
- `C4:1E20` died immediately on hard-bad **`FF`**
- strongest owner-backtrack candidates were:
  - **`C4:1E97`** for `C4:1EA2`
  - **`C4:1EBC`** for `C4:1EC1`
  - `C4:1EE3` for `C4:1EED`
- strongest local-control clusters were:
  - **`C4:1EB9..C4:1EBF`**
  - `C4:1E62..C4:1E72`
  - `C4:1EE2..C4:1EEA`

Bottom line:
- broad candidate-code/local-structure page with believable owner-backtracks, still not enough to promote under the current conservative anchor posture

### `C4:1F00..C4:1FFF`
**Page family:** `mixed_command_data`

What mattered:
- `C4:1F67` was the only surviving **weak** lure
- `C4:1F3F` and `C4:1F60` both degraded to **suspect**
- `C4:1FB5` died immediately on hard-bad **`00`**
- strongest owner-backtrack candidate was **`C4:1FB0`** for `C4:1FB5`
- no meaningful local clusters survived scoring

Bottom line:
- mixed near-miss page with one cleaner survivor and one hard-bad false dawn, still no defendable ownership

### `C4:2000..C4:20FF`
**Page family:** `candidate_code_lane`

This was the hottest overall page of the continuation.

What mattered:
- `C4:20C0` took **five** raw hits and all five died immediately because the landing byte is **`00`**
- `C4:2007` took **four** raw hits and stayed the cleanest repeated-hit surviving lure on the page
- `C4:2000` took **three** raw hits and remained a mixed weak/suspect near-miss
- `C4:20A0` took **three** raw hits and died immediately on hard-bad **`FF`**
- `C4:20E0` and `C4:20F0` each took **three** raw hits and still only remained weak/suspect
- `C4:2010` took **two** raw hits and died immediately on hard-bad **`60`**
- strongest owner-backtrack candidates were:
  - **`C4:2030`**
  - **`C4:205F`**
  - `C4:2005` for `C4:2007`
  - `C4:2000` for `C4:2001/2002`
- strongest local-control pockets were tiny and unconvincing:
  - `C4:20DD..C4:20E6`
  - `C4:20B8..C4:20BC`

Bottom line:
- busiest page of the block by far, but too many repeated hard-bad landings and too little convergent structure to promote anything honestly

### `C4:2100..C4:21FF`
**Page family:** `candidate_code_lane`

What mattered:
- `C4:2117` and `C4:21DE` were the cleanest **weak** lures on the page
- `C4:211E` and `C4:212F` both degraded to **suspect**
- `C4:2131` died immediately on hard-bad **`02`**
- strongest owner-backtrack candidates were:
  - **`C4:212F`**
  - `C4:2115` for `C4:2117`
- strongest local-control cluster was **`C4:213A..C4:2142`**

Bottom line:
- cleaner candidate-code page than the hotter `C4:2000` chaos, still not enough to hand over a defendable owner

### `C4:2200..C4:22FF`
**Page family:** `mixed_command_data`

What mattered:
- `C4:227C` took **two** raw hits and still degraded to **suspect**
- `C4:221D`, `C4:221F`, and `C4:2247` were the cleanest surviving weak lures on the page
- `C4:22BF` died as a soft-bad landing on **`30`**
- `C4:22DD` died immediately on hard-bad **`00`**
- `C4:2231`, `C4:22C2`, `C4:22DF`, and `C4:22FF` were additional suspect near-misses
- strongest owner-backtrack candidates were:
  - **`C4:221E`** for `C4:221F`
  - `C4:2230` for `C4:2231`
  - `C4:22DB` for `C4:22DD`
- strongest local-control clusters were:
  - **`C4:222F..C4:2237`**
  - `C4:221D..C4:2224`
  - `C4:2246..C4:2254`

Bottom line:
- messy mixed closing page with several believable starts, but still no one owner boundary where caller quality, byte quality, and structure all lined up together

---

## Key truths preserved by this continuation
- `C4:1900` is a repeated-hit opening lure that still sits on soft-bad `01`
- `C4:1A09` and `C4:1B79` are clean single-hit candidate-code near-misses and still lack enough support to promote
- `C4:1C00..1CFF` is one of the strongest early code-lane pages of the continuation and still does not hand over one clean caller-backed owner
- `C4:1E97` and `C4:1EBC` are the strongest owner-backtrack candidates of the broader mid-block candidate-code page and still are not defensible as promotions
- `C4:2000..20FF` is the hottest page of the continuation
- `C4:20C0`, `C4:20A0`, and `C4:2010` prove again that repeated outside pressure can keep landing on obvious garbage (`00`, `FF`, and `60`)
- `C4:2007` is the strongest repeated-hit clean-start lure of the continuation and still falls short of ownership
- `C4:2131` is a hard-bad lure on `02`
- `C4:22BF` is a soft-bad lure on `30`
- `C4:222F..2237` is the strongest closing local-control cluster of the block and still only structure

---

## Result
- Seam advanced from **`C4:1900..`** to **`C4:2300..`**
- No new labels promoted
- Label space remains clean
