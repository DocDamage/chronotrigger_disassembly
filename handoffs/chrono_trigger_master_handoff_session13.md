# Chrono Trigger Disassembly — Master Handoff Session 13

## Repo / branch / ROM
- Repo: `DocDamage/chronotrigger_disassembly`
- Working branch: `live-work-from-pass166`
- ROM: `Chrono Trigger (USA).sfc`
- Source of truth: the repo branch plus the ROM bytes

## Current no-BS state
This session pushed the live seam from **`C3:2900..`** through **`C3:5AFF`** and closed **passes 192 through 241**.

That sounds like a lot of range because it was.
It does **not** mean the bank suddenly turned into clean callable code.

The real story of this session is:
- the seam kept moving forward honestly
- the recent `C3` lane stayed mixed-content heavy
- several pages produced convincing false dawns
- none of those false dawns survived caller-quality plus local-structure review together

That is still real progress, because it narrows the executable frontier without polluting the repo with bad labels.

---

## Progress made this session

### Pass span completed
- **192 through 241**

### Seam movement
- started at **`C3:2900..`**
- current live seam is now **`C3:5B00..`**

### Completion estimate
- started around **~79.6%**
- current estimate is **~83.6%**

---

## What happened across the session

### Block 1 — passes 192 through 201 (`C3:2900..32FF`)
Main pattern:
- helper-looking islands ending in `RTS`
- noisy same-bank callers
- interior landings into mixed blobs instead of true starts

Important false dawns:
- `2B06` looked more executable than nearby pages but had an ASCII-heavy caller
- `307F..3087` was a tempting tiny `RTS` helper stub
- `31BF` had some of the strongest caller-side evidence of the block and still failed ownership
- `3200..3216` looked like a short register-write burst ending in `RTI`, but visible support landed inside it rather than at a defendable start

Outcome:
- no defendable owner/helper promotions
- seam advanced to `C3:3300..`

### Block 2 — passes 202 through 211 (`C3:3300..3CFF`)
Main pattern:
- xref-richer pages that still collapsed under byte-level review
- table/command material that looked stronger than it was
- cleaner same-bank hits landing in the wrong place

Important false dawns:
- `33D6` had two same-bank hits and still failed
- `377E` had three same-bank callers and still failed
- `395E`, `39A7`, and `39DE` had the cleanest xref density of the block and still resolved as command/pointer-table style material
- `3C5E` / `3C80` were close to a structured reentry lane, but not enough

Outcome:
- no defendable owner/helper promotions
- seam advanced to `C3:3D00..`

### Block 3 — passes 212 through 221 (`C3:3D00..46FF`)
Main pattern:
- more obvious mixed control/data pages
- one page that finally looked meaningfully executable
- then a hard drop into credits/text-heavy contamination

Important false dawns:
- `3F90` was the cleanest lone external `JSR` landing of the block
- `4309` became the strongest caller-side false dawn of the whole session so far with two clean direct callers
- `4400` proved to be straight credits/text-heavy material
- `4544`, `45DE`, and `4631` looked tempting late, but none survived

Outcome:
- no defendable owner/helper promotions
- seam advanced to `C3:4700..`

### Block 4 — passes 222 through 231 (`C3:4700..50FF`)
Main pattern:
- mixed text-heavy pages
- repeated-value contamination
- one especially strong local-island false dawn

Important false dawns:
- `4BCB` was a comparatively cleaner late landing but still too deep inside mixed material
- `4C3F` plus local island `4C3A..4C49` was the strongest false-dawn combination of the block
- `4D80` was another relatively clean single-hit landing that still failed
- `4A00`, `4B00`, and `4F00` remained heavily contaminated by text-like / repeated-value content

Outcome:
- no defendable owner/helper promotions
- seam advanced to `C3:5100..`

### Block 5 — passes 232 through 241 (`C3:5100..5AFF`)
Main pattern:
- page-top bait
- local branch-fed control traffic
- cleaner-looking pages that still did not show true outside ownership

Important false dawns:
- `5200` was the strongest page-top false dawn of the block
- `54A5` was the strongest true external multi-hit lure and still failed
- `5800` was the cleanest-looking page overall, but behaved more like a self-contained local control blob than a caller-backed routine page
- `5A00` ended cleaner than it began, but still did not cross the threshold into promotable code

Outcome:
- no defendable owner/helper promotions
- seam advanced to **`C3:5B00..`**

---

## Updated toolkit state

### Why the toolkit needed another full upgrade
By the time the seam reached the `5100..5AFF` stretch, the existing toolkit was already good at:
- caller/target neighborhood risk scoring
- return-anchored local island discovery
- one-shot seam triage

But it still left too much manual work around one specific question:

**Is this page receiving true outside ownership, or just branch-fed self-noise that makes it look executable?**

That question kept showing up in pages like:
- `4300`
- `4C00`
- `5200`
- `5400`
- `5800`

### Existing upgraded tools already in place
From the previous session/tooling phase:
- `tools/scripts/score_raw_xref_context_v1.py`
- `tools/scripts/find_local_code_islands_v1.py`
- `tools/scripts/run_c3_candidate_flow_v2.py`
- `tools/docs/seam_shape_triage_upgrade.md`

### New toolkit upgrades completed now
These are the new repo-native additions for this session’s toolkit refresh:

#### `tools/scripts/score_seam_page_ownership_v1.py`
Purpose:
- score whether a page is getting real outside ownership or just same-page branch/control traffic

What it adds:
- separates external direct hits from local branch-fed hits
- flags page-top landings
- penalizes interior landings inside surfaced local islands
- assigns a page class such as:
  - `high_attention_external_owner_candidate`
  - `medium_attention_external_owner_candidate`
  - `local_control_blob`
  - `interior_landing_bait`
  - `mixed_no_owner`

Practical value:
- much faster rejection of pages that only look good because they are self-fed control blobs
- cleaner explanation for why page-top bait still fails
- better ranking of which page in a block deserves the next deep manual read

#### `tools/scripts/run_c3_seam_block_report_v1.py`
Purpose:
- batch-run page-ownership triage across a consecutive block of `C3` pages

What it adds:
- scans every `0x100` page in a requested range
- ranks pages by external-owner signal
- separately ranks pages by local-control density
- gives a fast answer to:
  - which page deserves the next hard read
  - which pages are mostly just local control blobs

Practical value:
- saves manual time before starting a ten-page seam block
- improves handoff quality because block-level comparisons become explicit instead of fuzzy
- helps keep the next passes pointed at the least-bad pages first

#### `tools/scripts/run_c3_candidate_flow_v3.py`
Purpose:
- new default one-shot seam triage wrapper

What it runs:
1. `run_c3_candidate_flow_v2.py`
2. `score_seam_page_ownership_v1.py`

Practical value:
- preserves the earlier seam-shape evidence
- adds page-ownership classification in one command
- should become the default first pass for ugly forward `C3` seams

#### `tools/docs/page_ownership_triage_upgrade.md`
Purpose:
- document the new page-ownership layer, why it exists, and how to use it

### Honest status of the toolkit
The toolkit is materially better now than it was at the start of the session.

It is still **heuristic**, not semantic.
It does **not** prove code automatically.
What it now does better is:
- stop wasting time on local branch-fed bait
- distinguish page-top / interior false dawns from true outside ownership
- rank whole seam blocks before manual page review begins

---

## Current files produced this session

### Continuation / raw seam reports
- `chrono_trigger_session13_continue_notes.md`
- `chrono_trigger_session13_continue_notes_2.md`
- `chrono_trigger_session13_continue_notes_3.md`
- `chrono_trigger_session13_continue_notes_4.md`
- `chrono_trigger_session13_continue_notes_5.md`
- `chrono_trigger_c3_3300_3cff_raw_report.md`
- `chrono_trigger_c3_3d00_46ff_raw_report.md`
- `chrono_trigger_c3_4700_50ff_raw_report.md`
- `chrono_trigger_c3_5100_5aff_raw_report.md`

### Toolkit docs / scripts added in this upgrade
- `tools/scripts/score_seam_page_ownership_v1.py`
- `tools/scripts/run_c3_seam_block_report_v1.py`
- `tools/scripts/run_c3_candidate_flow_v3.py`
- `tools/docs/page_ownership_triage_upgrade.md`

### Docs updated
- `README.md`
- this handoff file

---

## Current structural truths worth preserving

These are the important truths that should survive into future sessions:

1. The seam advanced from `C3:2900..` to `C3:5B00..` **without** finding a trustworthy owner/helper lane in between.
2. `4309`, `4C3F`, `5200`, and `54A5` were some of the strongest false dawns of the session.
3. `4400` is credits/text-heavy material and should not be revisited as a serious code-owner candidate.
4. `5800` is one of the cleanest-looking recent pages, but still behaves more like local control structure than caller-backed ownership.
5. The project is making real progress by refusing bad promotions, not by inflating the label count.

---

## Recommended next-session workflow

1. Stay on `live-work-from-pass166`
2. Read this handoff first
3. Resume from **`C3:5B00..`**
4. Run `run_c3_seam_block_report_v1.py` on the next block before deep-reading pages
5. Use `run_c3_candidate_flow_v3.py` on the strongest-ranked page(s)
6. Only promote code when:
   - caller quality holds up
   - target structure holds up
   - page ownership signal holds up
7. If those three disagree, freeze the page honestly and move the seam

---

## What remains before the disassembly is truly finished

### Immediate remaining work
- continue forward from `C3:5B00..`
- keep resolving the ugly mixed-content `C3` lane without forcing labels
- keep publishing notes/raw reports/handoffs to the repo branch

### Medium-term remaining work
- convert more surviving seams into real owner/helper promotions once a cleaner lane appears
- keep reconciling mixed regions against already known strong labels and frozen post-code/data boundaries
- continue strengthening repo-native tooling so future passes spend less time rediscovering the same false shapes

### Final remaining work for a “completely done” disassembly
- finish all unresolved code/data boundaries across the ROM
- ensure all surviving callable lanes have defendable labels and ownership
- verify mixed-content regions honestly instead of leaving hidden wishful assumptions
- leave the repo in a state where the next person can resume from the branch and reproduce the current understanding without needing chat context

---

## Real next target
- **`C3:5B00..`**

That is still the live seam.
Not the recent page-top bait.
Not the interior landings.
Not the unsupported local islands.
The next page still has to earn executable status the hard way.
