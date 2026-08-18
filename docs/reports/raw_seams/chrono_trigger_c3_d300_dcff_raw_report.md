# Chrono Trigger C3 seam raw report — C3:D300..C3:DCFF

## Scope
- Continuation from live seam: `C3:D300..`
- Conservative forward sweep across the next ten pages
- Local toolkit executed from the staged branch copy in the workspace
- Caller anchoring in the workspace remained conservative because the full pass-manifest history is not mirrored locally; nothing in this block earned promotion anyway

## Bottom line
- Closed: `C3:D300..C3:DCFF`
- Promotions: **none**
- New live seam: **`C3:DD00..`**

This block produced a few real-looking near-misses:
- a hard-bad outside lure at `D480`
- a candidate-code rebound page at `D600`
- a text-heavy double-hit false-dawn page at `D800`
- the cleanest single-hit outside lure of the continuation at `D900`
- the busiest outside-pressure page of the continuation at `DA00`
- the strongest broad local-control cluster of the block at `DB64..DB88`

None of them defended honest ownership.

---

## Page-by-page triage

### `C3:D300..C3:D3FF`
**Page family:** `mixed_command_data`

What mattered:
- no meaningful raw caller traction survived on the page
- strongest local pocket was `C3:D3A1..C3:D3AC`
- secondary pocket `C3:D3B4..C3:D3C2` was wider but already ASCII-heavy

Bottom line:
- structure only, no caller-backed ownership

### `C3:D400..C3:D4FF`
**Page family:** `mixed_command_data`

What mattered:
- `C3:177D -> C3:D480` was the only raw hit on the page
- it died immediately because the landing byte at `D480` is **`00`**
- strongest local pocket was only `C3:D4D1..C3:D4D7`
- owner backtrack preferred `C3:D47D` and still did not rescue the page

Bottom line:
- textbook hard-bad false dawn on `00`

### `C3:D500..C3:D5FF`
**Page family:** `mixed_command_data`

What mattered:
- no meaningful outside pressure
- no local islands survived scoring

Bottom line:
- quiet mixed page, seam moved through cleanly

### `C3:D600..C3:D6FF`
**Page family:** `candidate_code_lane`

This was the cleanest-looking page family of the continuation.

What mattered:
- `C3:1C51 -> C3:D604` was the only raw lure
- the landing byte at `D604` was clean, but both caller and target neighborhoods still graded high-risk
- strongest local support was `C3:D6DB..C3:D6F0`, but it was heavily ASCII-skewed

Why it failed:
- the page looked better than average, but the only outside lure still degraded to **suspect**
- local structure never defended a real owner boundary

Bottom line:
- candidate-code rebound page, still no promotion

### `C3:D700..C3:D7FF`
**Page family:** `mixed_command_data`

What mattered:
- no meaningful raw caller traction survived
- strongest local clusters were:
  - `C3:D7A0..C3:D7B8`
  - `C3:D766..C3:D776`
- both stayed too ASCII-heavy to claim ownership by local structure alone

Bottom line:
- local-control-only page

### `C3:D800..C3:D8FF`
**Page family:** `text_ascii_heavy`

This was one of the busiest outside-pressure pages of the continuation.

Main lures:
- `C3:8A67 -> C3:D804` was the cleanest page lure and stayed only **weak**
- `C3:86BF -> C3:D802` added second-hit pressure and still degraded to **suspect**

What mattered:
- owner backtrack for both `D802` and `D804` preferred **`C3:D800`**
- strongest local pockets were `C3:D88C..C3:D897` and `C3:D8E0..C3:D8E6`
- the whole page stayed text-heavy despite the outside motion

Bottom line:
- double-hit false dawn inside an ASCII-heavy lane; still not enough

### `C3:D900..C3:D9FF`
**Page family:** `mixed_command_data`

What mattered:
- `C3:64EE -> C3:D900` was the cleanest single outside lure of the continuation
- start byte `B2` is clean enough at byte level
- owner backtrack stayed pinned directly on `C3:D900`
- only local support was a tiny and fully ASCII pocket at `C3:D984..C3:D988`

Why it failed:
- outside pressure was still only a single weak hit
- the page had no meaningful structural support behind the landing

Bottom line:
- cleanest single-hit near-miss of the block, still not promotable

### `C3:DA00..C3:DAFF`
**Page family:** `mixed_command_data`

This was the busiest xref page of the continuation.

Main lures:
- `C3:8AE3 -> C3:DA02` was the cleanest landing and stayed **weak**
- `C3:4A76 -> C3:DA60` and `C3:4B0D -> C3:DA68` both degraded to **suspect**

What mattered:
- owner backtrack preferred:
  - `C3:DA00` for `DA02`
  - `C3:DA5E` for `DA60`
  - `C3:DA67` for `DA68`
- strongest local support was only `C3:DAEB..C3:DAF1`, and it was already very ASCII-heavy

Bottom line:
- busiest outside-call page of the block, still no defendable owner boundary

### `C3:DB00..C3:DBFF`
**Page family:** `text_ascii_heavy`

What mattered:
- no meaningful raw caller traction survived
- strongest broad local-control cluster of the continuation was **`C3:DB64..C3:DB88`**
- that cluster merged three overlapping return-anchored windows and still stayed heavily ASCII-skewed

Bottom line:
- strongest local-only structure of the block, still not ownership

### `C3:DC00..C3:DCFF`
**Page family:** `mixed_command_data`

What mattered:
- `C3:2630 -> C3:DCE0` was the only raw outside lure and stayed **weak**
- owner backtrack preferred `C3:DCDD`
- strongest local cluster was `C3:DC3A..C3:DC44`

Why it failed:
- the outside lure never rose above a single weak hit
- local support stayed small and disconnected from defendable ownership

Bottom line:
- solid closing near-miss page, still no promotion

---

## Key truths preserved by this continuation
- `C3:D480` is a hard-bad false dawn that dies immediately on `00`
- `C3:D604` is the best-looking rebound landing on the candidate-code page and still degrades under risk
- `C3:D800` is the owner-backtrack preference for the `D802/D804` double-hit page and still not enough
- `C3:D900` is the cleanest single-hit outside lure of the continuation and still lacks structural support
- `C3:DA02` is the cleanest landing on the busiest xref page of the block and still only a near-miss
- `C3:DB64..C3:DB88` is the strongest broad local-control cluster of the continuation and still does **not** own itself honestly
- `C3:DCE0` is the cleanest late closing-page lure and still falls short of promotion

---

## Result
- Seam advanced from **`C3:D300..`** to **`C3:DD00..`**
- No new labels promoted
- Label space remains clean
