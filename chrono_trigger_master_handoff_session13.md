# Chrono Trigger Disassembly — Master Handoff Session 13

## Repo / branch / ROM
- Repo: `DocDamage/chronotrigger_disassembly`
- Working branch: `live-work-from-pass166`
- ROM: `Chrono Trigger (USA).sfc`
- Source of truth: the repo branch plus the ROM bytes

## Current no-BS state
This session continued the conservative forward sweep from the old session-12 seam at `C3:2900..` through the current live seam at **`C3:5B00..`**.

The important truth is the same one that kept the project honest in session 12:
- reject fake caller support coming from text, table, script, or inline-data neighborhoods
- reject interior-byte landings that only look strong because of overlap or control-flow noise
- reject unsupported helper-looking islands even when they end in `RTS`, `RTL`, or `RTI`
- reject pages that feel executable when caller quality and local byte structure still disagree
- only promote code when both the caller side and the local structure actually hold up

This stretch **did not suddenly become clean monolithic code**.
It stayed a long ugly mixed-content `C3` lane.
The real progress was continuing to clear it honestly without poisoning the repo with fake owners.

---

## Progress made this session

This session completed **passes 192 through 241**.

### Block 1 — passes 192 through 201
Closed:
- `C3:2900..C3:32FF`

What mattered:
- `2B00` was the most executable-looking early page in the block, but visible support into `2B06` still came from an ASCII-heavy caller neighborhood
- `3000` produced a tempting tiny helper-like pocket at `307F..3087`, but only as a single-hit unsupported stub
- `3100` had the strongest caller-side evidence in the whole early run; `31BF` received two comparatively clean same-bank callers, but still landed inside a wider mixed blob
- `3200` looked like a short register-write / `RTI` burst, but the cleanest visible hit landed at interior `320D`, not at a true start

Bottom line:
- no defendable owner/helper promotions survived
- the seam advanced to `C3:3300..`

### Block 2 — passes 202 through 211
Closed:
- `C3:3300..C3:3CFF`

What mattered:
- `33D6` got two same-bank hits and still failed because it landed inside mixed control/data material
- `3461` is the clearest example of a non-terrible caller landing whose own bytes immediately expose it as pointer/table material
- `377E` was the strongest multi-caller false landing of the block and still did not defend a true start
- `395E`, `39A7`, and `39DE` had the cleanest xref density of the run, but all resolved as command/pointer-table style material rather than callable starts
- `3C5E` and `3C80` were the closest thing to a structured reentry lane, but still failed ownership

Bottom line:
- no defendable owner/helper promotions survived
- the seam advanced to `C3:3D00..`

### Block 3 — passes 212 through 221
Closed:
- `C3:3D00..C3:46FF`

What mattered:
- `3F90` was the cleanest lone external `JSR` landing of the block, but still landed mid-blob rather than at a defendable owner boundary
- `4309` became the strongest false dawn of this continuation because it had two comparatively clean direct callers (`C3:2193 -> JSR $4309` and `C3:24A1 -> JMP $4309`) and still failed ownership
- `4400` proved to be overwhelmingly credits/text-heavy material and should not be mistaken for recoverable code
- `4544`, `45DE`, and `4631` were the late-page temptations, but none survived caller-quality plus local-structure review together

Bottom line:
- no defendable owner/helper promotions survived
- the seam advanced to `C3:4700..`

### Block 4 — passes 222 through 231
Closed:
- `C3:4700..C3:50FF`

What mattered:
- `4BCB` was a comparatively cleaner late landing, but still too deep inside mixed material to defend a true owner boundary
- `4C3F` plus local island `4C3A..4C49` was the strongest false-dawn combination of the block; the caller looked good, the island looked good, but the visible hit still landed at interior `4C3F`, not at the true beginning of the pocket
- `4D80` was the next cleanest single-hit mid-page landing and still did not earn ownership
- `4A00`, `4B00`, and `4F00` remained strongly contaminated by text-like / repeated-value mixed content
- `5000` looked less text-heavy than the preceding pages, but it was still zero/repeated-pair-heavy and structurally mixed

Bottom line:
- no defendable owner/helper promotions survived
- the seam advanced to `C3:5100..`

### Block 5 — passes 232 through 241
Closed:
- `C3:5100..C3:5AFF`

What mattered:
- `5200` was the strongest page-top false dawn of the block; it got one dirty `JSR` plus a cleaner cross-page `BPL`, but still did not defend a real owner start
- `54A5` was the strongest true external multi-hit lure of the run, with two medium-risk `JSR` callers, and still failed because it landed inside a wider mixed splinter rather than at a defendable top boundary
- `5800` was the cleanest-looking page overall in the whole continuation, but it read as local control structure and branch-fed flow, not caller-backed ownership
- `5A00` ended cleaner than it began, which may hint at a slightly less text-contaminated seam ahead, but it still did not earn a promotion

Bottom line:
- no defendable owner/helper promotions survived
- the seam advanced to **`C3:5B00..`**

---

## Current state now

### Latest completed pass
- **241**

### Current live seam
- **`C3:5B00..`**

### Current completion estimate
- **~83.6%**

### What this actually means
The project is still advancing.
The recent work cleared **fifty more forward pages** of ugly `C3` mixed-content territory without poisoning the label space.

That is real progress.

The absence of new promotions in this stretch is not failure.
It means the review standard held.
A lot of this bank segment still behaves like mixed control, script-like bytecode, table-fed command material, credits/text-heavy content, or local branch-fed splinters rather than clean standalone routines.

---

## Toolkit state now

The seam-triage toolkit upgrade from the earlier session is now part of the working repo state on `live-work-from-pass166`.

### Repo-native seam-triage upgrade present on branch
Documentation:
- `tools/docs/seam_shape_triage_upgrade.md`

Scripts:
- `tools/scripts/score_raw_xref_context_v1.py`
- `tools/scripts/find_local_code_islands_v1.py`
- `tools/scripts/run_c3_candidate_flow_v2.py`

### What these tools do
#### `score_raw_xref_context_v1.py`
Purpose:
- score incoming raw xrefs into a seam using caller-side and target-side neighborhood heuristics

What it adds:
- printable ASCII ratio
- `00` / `FF` density
- repeated little-endian pair score for pointer/table suspicion
- caller-side / target-side risk labels
- downgraded `effective_strength` so apparently interesting xrefs can be demoted when the surrounding bytes still look data-side

Practical value:
- faster rejection of fake text-side and table-side callers
- cleaner separation between real caller-backed starts and xref bait

#### `find_local_code_islands_v1.py`
Purpose:
- surface unsupported return-anchored local islands inside ugly seams

What it adds:
- finds windows ending in `RTS`, `RTL`, or `RTI`
- scores branch density, call density, stack-ish setup bytes, and barrier bytes
- penalizes ASCII-heavy and repeated-pair-heavy neighborhoods

Practical value:
- faster discovery of helper-like or stub-like islands that still lack caller-backed true starts
- cleaner explanation for why a page has a promising splinter but still cannot be promoted

#### `run_c3_candidate_flow_v2.py`
Purpose:
- one-shot seam triage wrapper

What it runs:
1. `detect_tiny_veneers_v1.py`
2. `scan_range_entry_callers_v2.py`
3. `score_raw_xref_context_v1.py`
4. `find_local_code_islands_v1.py`

Practical value:
- fast first-pass triage for shaky `C3` seams before deeper manual inspection
- explicit combined output for raw targets, downgraded xrefs, local islands, and veneer candidates

### Recommended workflow now
For forward pages in this bank:
1. run `run_c3_candidate_flow_v2.py`
2. inspect downgraded xrefs from `score_raw_xref_context_v1.py`
3. inspect surfaced local islands from `find_local_code_islands_v1.py`
4. only promote code when caller quality and local structure still agree
5. if they disagree, freeze the page honestly and move the seam

---

## Session 13 repo artifacts written during this session

These continuation artifacts were written into the working branch during the session:
- `chrono_trigger_session13_continue_notes.md`
- `chrono_trigger_session13_continue_notes_2.md`
- `chrono_trigger_session13_continue_notes_3.md`
- `chrono_trigger_session13_continue_notes_4.md`
- `chrono_trigger_session13_continue_notes_5.md`
- `chrono_trigger_c3_3300_3cff_raw_report.md`
- `chrono_trigger_c3_3d00_46ff_raw_report.md`
- `chrono_trigger_c3_4700_50ff_raw_report.md`
- `chrono_trigger_c3_5100_5aff_raw_report.md`

These files preserve the detailed seam-facing evidence and should be treated as the session-13 trail of record for the branch.

---

## Strong labels and structural truths worth preserving

These labels and structural conclusions remain important and should not be lost in future handoffs:

- `ct_c3_stream_bytecode_interpreter_updating_0920_0940_and_dispatching_apu_command_words`
- `ct_c3_stream_word_fetch_helper_advancing_20_and_caching_fetched_word`
- `ct_c3_wram_data_quad_writer_to_0700_with_duplicated_sample_bytes_and_shift_decay_update`
- `ct_c3_selected_bank_four_edge_scanline_owner_ordering_four_xy_pairs_and_materializing_row_spans_to_7e_or_7f`
- `ct_c3_selected_bank_edge_rasterizer_storing_one_x_intercept_byte_per_scanline_with_common_epilogue`
- `ct_c3_inline_ascii_code_end_c3_marker`
- `ct_c3_post_code_end_inline_data_padding_block_with_zero_spacer_and_short_control_tail_before_next_callable_lane`
- `ct_c3_tiny_long_wrapper_calling_c302dd_then_returning`
- `ct_c3_small_local_looping_helper_returning_after_backward_branch`
- `ct_c3_tiny_long_wrapper_calling_c30d0e_then_returning`

Additional structural truths from this session worth preserving:
- `31BF` had strong caller-side evidence and still failed because it landed inside a wider mixed blob
- `377E` and `395E / 39A7 / 39DE` are classic examples of xref-rich false dawns that still resolve as command/pointer-table style material
- `4309` is the strongest clean-direct-caller false dawn of session 13 and still does not defend a true start
- `4400` is credits/text-heavy material, not recoverable callable code
- `4C3F` is the best example in this session of a good caller plus a good local island still failing because the landing is interior rather than owner-worthy
- `54A5` is the strongest true external multi-hit false dawn in the late session-13 run
- `5800` is the cleanest-looking page overall in the late session-13 run, but it still reads as local control structure rather than caller-backed ownership

---

## Recommended next-session workflow

1. Stay on branch **`live-work-from-pass166`**
2. Resume from **`C3:5B00..`**
3. Run the upgraded seam triage flow first
4. Prefer rejecting false page-top bait over forcing routines
5. Pay special attention to whether the slightly cleaner tail of `5A00` actually continues into better caller-backed structure at `5B00`, or whether it is just another local-control mirage
6. Continue writing every continuation note / raw seam report directly to GitHub during the session

---

## Real next target
- **`C3:5B00..`**

That is the real seam.
Not `5200`, which looked better than it deserved.
Not `54A5`, which had better outside caller support than most of this run and still failed.
Not `5800`, which feels cleaner than nearby pages but still does not own itself.

The next page still has to earn executable status the hard way.
