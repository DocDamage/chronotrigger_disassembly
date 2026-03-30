# Chrono Trigger C3 seam raw report — C3:DD00..C3:E6FF

## Scope
- Continuation from live seam: `C3:DD00..`
- Conservative forward sweep across the next ten pages
- Local toolkit executed from the staged branch copy in the workspace
- Workspace caller anchoring remained conservative because the full pass-manifest history is still not mirrored locally; nothing in this block earned promotion anyway

## Bottom line
- Closed: `C3:DD00..C3:E6FF`
- Promotions: **none**
- New live seam: **`C3:E700..`**

This block produced several believable near-misses:
- a three-lure mixed page at `DD00`
- a text-heavy local-control page at `DE00`
- a hard-bad outside lure at `DF06`
- the busiest outside-pressure page of the continuation at `E000`
- a five-hit mixed page with one soft-bad lure at `E200`
- a repeated hard-bad page at `E400`
- a double-hit late near-miss at `E5D0`
- a two-hit outside lure at `E6AA`

None of them defended honest ownership.

---

## Page-by-page triage

### `C3:DD00..C3:DDFF`
**Page family:** `mixed_command_data`

What mattered:
- `C3:BA7D -> C3:DD24` was the cleanest raw lure on the page and still only **weak**
- `C3:3DB0 -> C3:DD4C` and `C3:653E -> C3:DD98` were also only **weak**
- owner backtrack preferred:
  - `C3:DD24` for the `DD24` landing
  - `C3:DD92` for `DD98`
- strongest local-control cluster was **`C3:DDB1..C3:DDD7`**

Why it failed:
- the page had real outside motion, but it split across three modest lures with no stable owner boundary
- the strongest local cluster was already too ASCII-skewed to claim ownership on structure alone

Bottom line:
- strongest opening page of the continuation, still not promotable

### `C3:DE00..C3:DEFF`
**Page family:** `text_ascii_heavy`

What mattered:
- `C3:56C2 -> C3:DE27` and `C3:8513 -> C3:DE50` were the only page lures and both degraded to **suspect**
- owner backtrack preferred `C3:DE4D` for `DE50`
- strongest local clusters were:
  - **`C3:DE9F..C3:DEA7`**
  - `C3:DEC8..C3:DED4`

Bottom line:
- text-heavy local-control page with no caller-backed ownership

### `C3:DF00..C3:DFFF`
**Page family:** `mixed_command_data`

What mattered:
- `C3:2AC4 -> C3:DF06` was the only raw hit on the page
- it died immediately because the landing byte at `DF06` is **`00`**
- owner backtrack preferred `C3:DF00`
- strongest local-control cluster was **`C3:DFA6..C3:DFC9`**

Bottom line:
- textbook hard-bad false dawn on `00`

### `C3:E000..C3:E0FF`
**Page family:** `mixed_command_data`

This was the busiest outside-pressure page of the continuation.

Main lures:
- `C3:1612 -> C3:E000` was the cleanest page-start lure and stayed **weak**
- `C3:FC29 -> C3:E001`, `C3:84DD -> C3:E00F`, `C3:89CE -> C3:E033`, and `C3:6FFF -> C3:E03A` all looked live enough at byte level and still remained only near-misses
- `C3:F931` and `C3:F98E` both also landed on `E000`, but each degraded under high risk

What mattered:
- owner backtrack preferred:
  - `C3:E004` for `E00F`
  - `C3:E050` for `E060`
- there were **no meaningful local clusters** on the page

Why it failed:
- the page had lots of raw pressure but no local structure strong enough to defend ownership
- repeated outside attention still did not converge on one promotable owner boundary

Bottom line:
- busiest xref page of the block, still no promotion

### `C3:E100..C3:E1FF`
**Page family:** `mixed_command_data`

What mattered:
- `C3:9363 -> C3:E138` was the only raw lure and stayed **weak**
- owner backtrack preferred `C3:E128`
- strongest local-control cluster was **`C3:E1AD..C3:E1C9`**

Bottom line:
- one weak lure plus one real local cluster, still not enough

### `C3:E200..C3:E2FF`
**Page family:** `mixed_command_data`

This was the broadest mixed near-miss page of the continuation.

Main lures:
- `C3:ACE4 -> C3:E235` stayed **weak**
- `C3:7980 -> C3:E24E` died into a **soft-bad** landing on `01`
- `C3:1619 -> C3:E260` stayed **weak**
- `C3:1A41 -> C3:E27B` degraded to **suspect**
- `C3:FE76 -> C3:E2A0` stayed **weak**

What mattered:
- owner backtrack preferred:
  - `C3:E228` for `E235`
  - `C3:E242` for `E24E`
  - `C3:E2A0` for `E2A0`
- strongest local support was **`C3:E23A..C3:E243`**

Bottom line:
- five-hit mixed page with one soft-bad lure and no defendable owner

### `C3:E300..C3:E3FF`
**Page family:** `mixed_command_data`

What mattered:
- `C3:6572 -> C3:E350` was the only raw lure
- it died immediately because the landing byte at `E350` is **`00`**
- strongest local-control cluster was **`C3:E3E0..C3:E3EE`**

Bottom line:
- another hard-bad false dawn on `00`

### `C3:E400..C3:E4FF`
**Page family:** `mixed_command_data`

This was the dirtiest repeated-pressure page of the continuation.

Main lures:
- `C3:FF06 -> C3:E400` died immediately on **`00`**
- `C3:FE8E -> C3:E4B0` and `C3:FEA6 -> C3:E4C0` were the cleanest surviving lures and still only **weak**
- `C3:FED6 -> C3:E4E0` and `C3:FEBE -> C3:E4D0` also died on **`00`**
- `C3:75D6 -> C3:E4D7` and `C3:FEEE -> C3:E4F0` remained only suspect near-misses

What mattered:
- owner backtrack preferred **`C3:E4EF`** for `E4F0`
- secondary backtracks pointed at `C3:E4B9` and `C3:E4B0`
- strongest local clusters were short patterned pockets like `C3:E4B8..C3:E4C6`

Bottom line:
- repeated outside pressure mixed with multiple hard-bad landings; still no promotion

### `C3:E500..C3:E5FF`
**Page family:** `mixed_command_data`

What mattered:
- `C3:D9CE -> C3:E552` was the page’s single early lure and stayed **suspect**
- `C3:108E` and `C3:10B7` both landed on **`C3:E5D0`**, making it the strongest repeated-hit lure of the late block
- owner backtrack preferred **`C3:E5CF`** for `E5D0`
- strongest local clusters were small patterned pockets like `C3:E538..C3:E546` and `C3:E5D6..C3:E5E4`

Why it failed:
- even the repeated-hit pressure at `E5D0` still did not gain a stable owner that local structure defended honestly
- the page’s structural support stayed fragmented and repetitive

Bottom line:
- strongest late repeated-hit near-miss of the continuation, still not promotable

### `C3:E600..C3:E6FF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C3:4CD2 -> C3:E621` stayed **suspect**
- `C3:0C1A` and `C3:0C42` both landed on **`C3:E6AA`**, making it the cleanest repeated-hit lure on the page
- `C3:34B1 -> C3:E6ED` stayed only **weak**
- owner backtrack preferred `C3:E620` for `E621`
- there were **no meaningful local clusters** on the page

Bottom line:
- branch-fed control page with repeated outside pressure and no structural ownership behind it

---

## Key truths preserved by this continuation
- `C3:DD24`, `C3:DD4C`, and `C3:DD98` are all real-looking opening-page lures and still do not converge on one defendable owner
- `C3:DE9F..C3:DEA7` is the strongest early local-control cluster of the continuation and still only structure
- `C3:DF06` is a hard-bad false dawn on `00`
- `C3:E000` is the busiest outside-pressure page of the block and still does not defend ownership
- `C3:E24E` is a soft-bad lure on `01`
- `C3:E350` is another hard-bad landing on `00`
- `C3:E400`, `C3:E4D0`, and `C3:E4E0` show that repeated outside pressure can still keep landing on obvious garbage
- `C3:E5D0` is the strongest repeated-hit late near-miss of the continuation and still falls short
- `C3:E6AA` is the cleanest repeated-hit lure of the closing page and still lacks structural support

---

## Result
- Seam advanced from **`C3:DD00..`** to **`C3:E700..`**
- No new labels promoted
- Label space remains clean
