# Chrono Trigger C3 seam raw report — C3:C900..C3:D2FF

## Scope
- Continuation from live seam: `C3:C900..`
- Conservative forward sweep across the next ten pages
- Source of truth remained the ROM bytes plus the live branch standards from the Session 14 handoff

## Bottom line
- Closed: `C3:C900..C3:D2FF`
- Promotions: **none**
- New live seam: **`C3:D300..`**

This block was not empty. It produced several genuine-looking near-misses:
- a candidate-code rebound page at `C900`
- a two-lure branch-fed pocket at `CB00`
- a two-hit lure at `CCD0`
- a text-heavy false-dawn page at `D000`
- a broad late local-control cluster at `D1CA..D1EB`

None of them earned honest ownership.

---

## Page-by-page triage

### `C3:C900..C3:C9FF`
**Page family:** `candidate_code_lane`

What mattered:
- `C3:D9BE -> C3:C928` was the only raw hit on the page and remained only a weak near-miss
- owner backtrack stayed pinned directly on `C3:C928` and still scored poorly
- strongest local pockets were `C3:C98B..C3:C998` and `C3:C9EE..C3:C9FA`

Why it failed:
- the page looked cleaner than average, but the only hit did not land on a defensible owner boundary
- the best local pocket on the page was already too ASCII-heavy to rescue ownership by structure alone

Bottom line:
- early rebound page, still no promotion

### `C3:CA00..C3:CAFF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- no meaningful raw caller traction survived on the page
- strongest local-control pocket was `C3:CAB2..C3:CABE`
- `C3:CA21` was the only notable backtracked start and still scored negatively

Bottom line:
- local-control-only page, not owner-backed

### `C3:CB00..C3:CBFF`
**Page family:** `branch_fed_control_pocket`

This was one of the strongest pages of the continuation.

Main lures:
- `C3:D68B -> C3:CB08` stayed weak
- `C3:28E9 -> C3:CB4C` stayed weak

What mattered:
- owner backtrack preferred `C3:CB47` for the `CB4C` landing
- `C3:CB08` also looked superficially plausible at byte level
- strongest local cluster was `C3:CB8E..C3:CBA4`, followed by `C3:CB78..C3:CB8A`

Why it failed:
- both hits were still only raw weak pressure
- the backtracked owner at `CB47` looked better than the landing, but still did not gain real ownership support
- the broadest local clusters were noticeably ASCII-heavy and behaved more like internal control structure than caller-backed code ownership

Bottom line:
- strong page, still only a near-miss page

### `C3:CC00..C3:CCFF`
**Page family:** `branch_fed_control_pocket`

What mattered:
- `C3:CCD0` drew the strongest repeated pressure of the continuation with two raw `JSR` hits from `C3:FD31` and `C3:FD8D`
- `C3:CC00` also took a separate raw lure and remained suspect
- owner backtrack split the page between `C3:CC00` and `C3:CCCF`
- strongest local pocket was `C3:CCEC..C3:CCF7`

Why it failed:
- `CCD0` looked like the page’s best outside lure, but still only as weak repeated pressure
- the page never converged on one stable owner boundary that both the landing quality and local structure defended together
- the best local pockets were too small and too disconnected to establish ownership honestly

Bottom line:
- `CCD0` is the strongest repeated-hit lure of this continuation and still not promotable

### `C3:CD00..C3:CDFF`
**Page family:** `mixed_command_data`

What mattered:
- no meaningful raw traction
- no notable backtrack candidates
- no local islands survived scoring

Bottom line:
- dead-feeling mixed page, seam moved cleanly through it

### `C3:CE00..C3:CEFF`
**Page family:** `mixed_command_data`

What mattered:
- `C3:70ED -> C3:CE0F` died immediately as a soft bad-start lure on `09`
- `C3:DE51 -> C3:CEA8` was the page’s only clean-start weak lure
- owner backtrack preferred `C3:CEA2` for the `CEA8` landing
- local clusters `C3:CE76..C3:CE85` and `C3:CE8A..C3:CE96` were heavily ASCII-skewed

Bottom line:
- the page produced one soft-bad false dawn and one cleaner near-miss; neither survived

### `C3:CF00..C3:CFFF`
**Page family:** `mixed_command_data`

What mattered:
- no meaningful raw caller traction
- lone local splinter `C3:CF67..C3:CF6B`

Bottom line:
- another local-control-only page with no ownership

### `C3:D000..C3:D0FF`
**Page family:** `text_ascii_heavy`

This was the dirtiest false-dawn page of the continuation.

What mattered:
- `C3:D000` took **three** raw hits and all three died immediately because the landing byte is `00`
- `C3:D088` looked live at byte level and still degraded under heavy data-side risk
- `C3:24BB -> C3:D0BE` was the cleanest remaining lure and still stayed weak
- strongest local pocket was `C3:D04F..C3:D05B`, but it was extremely ASCII-heavy

Bottom line:
- textbook case of busy page pressure inside text-heavy junk; no promotion survived

### `C3:D100..C3:D1FF`
**Page family:** `mixed_command_data`

What mattered:
- `C3:BA06 -> C3:D105` was the cleanest page lure and still only weak
- `C3:D100` was the preferred backtracked owner for that landing and still not strong enough
- `C3:D1CA..C3:D1EB` was the strongest broad local-control cluster of the continuation

Why it failed:
- the page’s best lure was still only weak raw pressure
- the large late-page cluster looked real as structure, but still did not own itself honestly

Bottom line:
- strongest late local cluster of the block, still not promotable

### `C3:D200..C3:D2FF`
**Page family:** `mixed_command_data`

What mattered:
- `C3:3C4D -> C3:D204` was the cleanest early lure and stayed weak
- `C3:8A1E -> C3:D260` was the cleanest later lure and also stayed weak
- `C3:BD2B -> C3:D220` remained suspect despite a decent byte-level start
- owner backtrack preferred `C3:D202` for `D204`
- strongest local cluster was `C3:D231..C3:D240`

Why it failed:
- the page split into multiple modest near-misses without converging on a defended owner
- the strongest local support stayed structural rather than owning

Bottom line:
- solid closing page, still no honest promotion

---

## Key truths preserved by this continuation
- `C3:C928` is the cleanest early rebound near-miss of the block and still not enough
- `C3:CB47` is the strongest backtracked owner candidate of the continuation and still not defensible as a promotion
- `C3:CCD0` is the strongest repeated-hit lure of the block and still falls short of ownership
- `C3:CE0F` is a soft-bad false dawn on `09`
- `C3:D000` proves raw multi-hit pressure can still land on obvious garbage
- `C3:D1CA..C3:D1EB` is the strongest broad local-control cluster of the continuation and still does not own itself honestly
- `C3:D231..C3:D240` is a real local-control pocket and still not enough to promote code

---

## Result
- Seam advanced from **`C3:C900..`** to **`C3:D300..`**
- No new labels promoted
- Label space remains clean
