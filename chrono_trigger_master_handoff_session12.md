# Chrono Trigger Disassembly — Master Handoff Session 12

## Repo / branch / ROM
- Repo: `DocDamage/chronotrigger_disassembly`
- Working branch: `live-work-from-pass166`
- ROM: `Chrono Trigger (USA).sfc`
- Source of truth: the repo branch plus the ROM bytes

## Current no-BS state
The recent run from pass 182 through pass 191 kept pushing forward honestly through a brutal high-bank `C3` mixed-content lane.

That lane **did not suddenly turn into clean monolithic code**.
Instead, the work kept doing the right thing:
- reject fake caller support coming from text / table / script-like neighborhoods
- reject interior-byte landings that only look strong because of operand overlap
- reject unsupported helper-looking local islands even when they end in `RTS`
- only advance the seam when the local structure and caller context both fail to justify promotion

This is slower than wishful labeling, but it is the correct path.

---

## Progress made this session

This session completed **passes 182 through 191**.

### Pass 182
Closed:
- `C3:1C00..C3:1FFF`

Treated as:
- `ct_c3_inline_mixed_control_table_false_entry_and_false_wrapper_cluster_before_2000_candidate`

Important outcome:
- `1C00` looked cleaner than the lead-in but still did not earn an owner start
- `1DDF..1DE2` was rejected as a false wrapper because it resolved to `JSR $1150 ; RTL`, and `$1150` falls back into frozen post-marker data
- `1DFD..1E01` was also rejected as a false long-wrapper signature

### Pass 183
Closed:
- `C3:2000..C3:20FF`

Treated as:
- `ct_c3_inline_mixed_control_table_and_false_low_bank_helper_cluster_before_2100_candidate`

Important outcome:
- visible same-bank caller pressure into `20AA`, `20B2`, and `20E6` looked promising
- those targets still failed local byte-level sanity checks and were not promoted

### Pass 184
Closed:
- `C3:2100..C3:21FF`

Treated as:
- `ct_c3_inline_mixed_xref_bait_with_untrusted_single_call_targets_and_unsupported_local_helper_pocket_before_2200_candidate`

Important outcome:
- every visible raw target in the page was only a single-hit target
- the strongest local pocket around `2191..21A8` looked helper-like, but the visible `21A0` target landed inside it instead of at its true start

### Pass 185
Closed:
- `C3:2200..C3:22FF`

Treated as:
- `ct_c3_inline_mixed_false_target_cluster_with_brk_heavy_lead_in_and_unsupported_226f_helper_pocket_before_2300_candidate`

Important outcome:
- the page had many raw targets, but several visible callers lived in text/table/script-style data neighborhoods
- the cleanest local pocket at `226F..227B` stayed unsupported because the visible nearby hit landed on the interior `RTS` at `227B`

### Pass 186
Closed:
- `C3:2300..C3:23FF`

Treated as:
- `ct_c3_inline_mixed_brk_heavy_arithmetic_like_cluster_and_false_table_entry_targets_before_2400_candidate`

Important outcome:
- late targets `2380`, `2386`, `238E`, and `23A3` landed inside an obvious repeated-value table-like cluster
- the apparent `C3:0B27 -> C3:2380` relationship was rejected as an interior-byte false positive
- `2322` looked like a possible one-byte `RTS` stub but did not retain trustworthy caller support

### Pass 187
Closed:
- `C3:2400..C3:24FF`

Treated as:
- `ct_c3_inline_mixed_pointer_table_and_false_interior_target_cluster_with_unsupported_2461_helper_pocket_before_2500_candidate`

Important outcome:
- the page opened in obvious pointer/table-like material
- the best unsupported local pocket was around `2461..2483`, ending in a clean `RTS`, but it still had no caller-backed true start

### Pass 188
Closed:
- `C3:2500..C3:25FF`

Treated as:
- `ct_c3_inline_mixed_weak_single_caller_page_with_unsupported_2523_helper_stub_and_late_pointer_table_cluster_before_2600_candidate`

Important outcome:
- only three visible raw targets landed in the page: `2504`, `2509`, `2520`
- only `C3:5599 -> C3:2504` looked remotely caller-trustworthy
- the cleanest local island was `2523..2529`, but it was unsupported and sat inside mixed content

### Pass 189
Closed:
- `C3:2600..C3:26FF`

Treated as:
- `ct_c3_inline_mixed_multi_target_page_with_false_text_table_callers_and_unsupported_late_rts_island_before_2700_candidate`

Important outcome:
- this page had more raw targets than the immediately previous pages
- some low-bank callers into `2600`, `2629`, and `26D0` looked more code-like than recent junk hits
- even then, the targets themselves still collapsed under local structural review

### Pass 190
Closed:
- `C3:2700..C3:27FF`

Treated as:
- `ct_c3_inline_branch_heavy_mixed_control_arithmetic_blob_with_false_data_side_2709_target_and_no_caller_backed_true_start_before_2800_candidate`

Important outcome:
- the page looked more executable than some pointer-heavy freezes, but only one visible raw target existed: `C3:A1B7 -> C3:2709`
- that caller lived in obvious byte soup / inline-data material
- unsupported `BRA` landings did not rescue the page

### Pass 191
Closed:
- `C3:2800..C3:28FF`

Treated as:
- `ct_c3_inline_branch_heavy_mixed_control_blob_with_double_low_bank_2809_hits_but_no_defendable_true_start_before_2900_candidate`

Important outcome:
- this page had the strongest caller-side evidence in a while
- `2809` received **two** low-bank same-bank `JSR` callers from `C3:0CC9` and `C3:0CF4`
- even so, `2809` still opened into a branch-heavy mixed control blob and did not stabilize into a defensible owner/helper split

---

## Current state now

### Latest completed pass
- **191**

### Current live seam
- **`C3:2900..`**

### Current completion estimate
- **~79.6%**

### What this actually means
The project is still advancing, but the current `C3` lane remains a mixed-content heavy forward seam where the main win is **not lying to ourselves**.

The recent run improved confidence by eliminating bad starts, bad stubs, bad wrappers, and bad interior landings across a long high-bank stretch.
That is real progress.

---

## Toolkit upgrade completed this session

### Why the toolkit needed another upgrade
The last ten forward pages kept repeating the same three review costs:
- caller neighborhoods that looked like code in the xref list but were really text/table/script-like inline data
- unsupported helper-looking local islands ending in `RTS` / `RTL`
- pages that felt more executable than simple pointer data, but still failed because caller quality and local byte structure disagreed

### New toolkit pieces added locally
These were built and validated locally against the ROM during this session:

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
- better separation between real caller-backed starts and xref bait

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
- quicker first-pass triage before deeper manual page inspection
- explicit combined output for raw targets, downgraded xrefs, local islands, and veneer candidates

### Toolkit documentation added
- `tools/docs/seam_shape_triage_upgrade.md`

This upgrade note was successfully written into the repo and describes the new seam-triage helpers and recommended workflow.

### Honest note about write-back status
The connector glitched while writing the new toolkit scripts back into GitHub.
The upgrade logic exists locally and was validated, and the upgrade documentation **did** make it into the repo.
If needed next session, the first housekeeping step should be to write the three new scripts into `tools/scripts/` on the branch if they are still missing there.

Local toolkit files created this session:
- `score_raw_xref_context_v1.py`
- `find_local_code_islands_v1.py`
- `run_c3_candidate_flow_v2.py`

---

## Recommended next-session workflow

1. Confirm the toolkit script write-back state in `tools/scripts/`
2. Resume from **`C3:2900..`**
3. Run the upgraded seam triage flow first
4. Only promote code when caller quality and local structure still agree
5. If they disagree, freeze the page honestly and move the seam

---

## Strong labels and structural truths worth preserving

These remain important to the real story of the bank and should not be lost in future handoffs:

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

---

## Real next target
- **`C3:2900..`**

That is the real seam.
Not the pretty-looking unsupported islands behind it.
Not the recent rejected `2809` control blob.
Not any interior `RTS` byte that only looks attractive in isolation.

The next page still has to earn executable status the hard way.
