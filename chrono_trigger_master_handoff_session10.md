# Chrono Trigger Disassembly — Master Handoff (Session 10)

## What this handoff is

This is the current source-of-truth handoff after the repo-first transition, toolkit restructuring, targeted audit passes, and resumed forward progress through bank `C3`.

This handoff is meant to let the next session continue immediately without re-deriving the project state.

---

## Current top-line state

- **Latest completed pass:** `171`
- **Current working branch:** `live-work-from-pass166`
- **Repo:** `DocDamage/chronotrigger_disassembly`
- **Current forward target:** `C3:1318..C3:1816`
- **Overall completion estimate:** `~71.7%`
- **Label rows:** `1344`
- **Strong labels:** `1026`
- **Toolkit direction:** repo-native, manifest-backed, ROM-aware helper layer in place

---

## Major workflow change now in effect

### Old workflow
- local/zip toolkit
- chat artifacts acting like the main history
- repo sync happening later
- too much stale-state / rebuild friction

### New workflow
- **GitHub repo is the source of truth**
- **working branch is the live workspace**
- toolkit now lives in the repo under `tools/`
- manifests live in `passes/manifests/`
- reports live in `reports/`
- chat files are now snapshots/exports, not the canonical state

### Current working rule
Every pass should be treated as incomplete until the repo-side branch contains the pass state.

---

## Repo-native toolkit status

The toolkit is no longer just a zip bundle. It now has a real repo-side structure.

### Repo toolkit layout now present
- `tools/README.md`
- `tools/requirements.txt`
- `tools/docs/repo_layout.md`
- `tools/docs/workflow.md`
- `tools/docs/confidence_levels.md`
- `tools/config/pass_manifest_schema.json`
- `tools/config/label_validation_rules.yaml`
- `tools/config/next_target_scoring.yaml`
- `tools/config/bank_c3_progress.json`
- `reports/bank_c3_progress.md`
- `reports/toolkit_missing_capabilities.md`

### Repo toolkit scripts now present
- `tools/scripts/snes_utils.py`
- `tools/scripts/publish_pass_bundle.py`
- `tools/scripts/publish_pass_bundle_v2.py`
- `tools/scripts/find_next_callable_lane.py`
- `tools/scripts/find_next_callable_lane_v2.py`
- `tools/scripts/classify_c3_ranges.py`
- `tools/scripts/classify_c3_ranges_v2.py`
- `tools/scripts/build_call_anchor_report.py`
- `tools/scripts/build_call_anchor_report_v2.py`
- `tools/scripts/validate_labels.py`
- `tools/scripts/validate_labels_v2.py`
- `tools/scripts/update_bank_progress.py`
- `tools/scripts/update_bank_progress_v2.py`
- `tools/scripts/check_pass_manifest.py`
- `tools/scripts/audit_pass_manifests_v1.py`
- `tools/scripts/audit_branch_state_v1.py`

### Honest toolkit status
The toolkit is **substantially upgraded** and no longer missing the major categories it was missing earlier.

What is now true:
- repo-native toolkit exists
- pass manifests exist and are backfilled for the recent active run
- bank progress has a tracked index
- ROM-aware helper layer exists
- audit layer exists
- branch-state sanity tooling exists

What is still not fully polished:
- some tools are still lightweight/heuristic rather than full disassembly-database integrations
- the publisher is improved but not yet a one-button everything pipeline with zero manual follow-up
- generated bank progress is present as a direction and partial implementation, but the static and generated sides have not been fully unified yet
- the classifier/xref tools are useful, but still conservative and not omniscient

So the toolkit is no longer half-built, but there is still refinement work available.

---

## Pass manifest status

Recent manifests are present in the repo for:
- `pass163.json`
- `pass164.json`
- `pass165.json`
- `pass166.json`
- `pass167.json`
- `pass168.json`
- `pass169.json`
- `pass170.json`
- `pass171.json`

This means the recent active phase now has a machine-readable trail.

---

## Structured audit work completed

A structured audit sweep was started using the newer toolkit instead of blindly trusting older closures.

### Audit reports added
- `reports/pass_audit_163_168.md`
- `reports/pass_audit_163_169.md`

### What the audit proved
The newer ROM-aware tooling did **not** collapse the recent bank `C3` work. That is a good sign.

The biggest audit outcomes:

#### `C3:09E9..C3:0A8F`
Kept closed.
Still correctly treated as:
- `ct_c3_wram_runtime_code_emitter_writing_generated_stub_bytes_through_2180`

Confirmed again as a shared top-level runtime-code emitter with direct long-call evidence.

#### `C3:0B03..C3:0C91`
Kept closed.
Still correctly treated as:
- `ct_c3_stream_bytecode_interpreter_updating_0920_0940_and_dispatching_apu_command_words`

Also confirmed:
- `0AFF..0B02` remains a real wrapper veneer
- `0CB1..0CB7` remains correctly split because it has an external caller

#### `C3:08A9..C3:08B2`
This one **did change**.
It is **not** an unattached orphan tail.
It is now understood as:
- the attached terminal tail of the helper rooted at `C3:0800`

This matters because it removes one fake unresolved fragment from the revisit backlog.

#### `C3:01E4..C3:0306`
Kept split.
The owner/helper separation remains correct:
- `C3:01E4..C3:02DC`
- `C3:02DD..C3:0306`

The newer caller evidence reinforced that split instead of weakening it.

### Audit conclusion
The base recent `C3` work is holding up.
That means forward progress can continue without feeling like the whole recent lane is suspect.

---

## Bank C3 progress summary

### Low-bank state
The low-bank executable cluster has been driven all the way through the explicit marker:
- `C3:10C0..C3:10CF` = inline ASCII marker `CODE END C3`

Post-marker immediate gap was closed honestly as data:
- `C3:10D0..C3:12FF` = post-marker inline data/padding block

### Current higher-lane state
After that, the project moved into the next higher unresolved callable lane.

Most recent cautious forward closure:
- `C3:1300..C3:1317` = inline control/dispatch data block preceding the higher executable body

### Current live seam
- **`C3:1318..C3:1816`**

This is the real next forward target.

---

## Most important passes in the recent run

### Pass 163
Locked the split:
- `C3:01E4..C3:02DC`
- `C3:02DD..C3:0306`

This established an owner/helper separation that later audit confirmed.

### Pass 164
Closed:
- `C3:0307..C3:0528`

Kept it as one owner instead of forcing a fake split at `034C`.

### Pass 165
Split a fake giant seam into real substructures:
- frame/display service wrapper
- signed math helper
- two `MVN` veneers
- change detector/service trigger
- permutation table
- WRAM runtime-code emitter
- inline Jet Bike Race credits text

### Pass 166
Closed the `0A90..0E38` family as:
- one owner
- one veneer
- helper cluster
- four writer variants
- one tail helper

### Pass 167
Closed:
- `C3:0EFA..C3:1024`
- `C3:1025..C3:10BF`
- `C3:10C0..C3:10CF`

This is where the low-bank executable cluster ran cleanly into `CODE END C3`.

### Pass 168
Closed:
- `C3:10D0..C3:12FF`

Important because it refused to fake code after the marker.

### Pass 169
Targeted audit pass.
Confirmed earlier high-value structural closures instead of changing them.

### Pass 170
Targeted audit pass.
Corrected `08A9..08B2` from “orphan tail” to “attached tail of helper rooted at 0800.”
Also reconfirmed the `01E4 / 02DD` split.

### Pass 171
Forward progress resumed.
Closed:
- `C3:1300..C3:1317`

This preserved the executable body for the next pass instead of forcing a weak giant claim.

---

## Current unresolved forward target

### Next exact target
- **`C3:1318..C3:1816`**

### Why this is the right target
- the post-marker low gap is already frozen as data
- the control/dispatch prefix `1300..1317` is frozen as data
- `1318` is the next bytes that actually look code-like
- `1817` remains intentionally separate as its own externally anchored entry

### Recommended approach for the next pass
Use the repo-native flow and do not skip the toolkit.

Recommended order:
1. derive/confirm the lane with `find_next_callable_lane_v2.py`
2. classify the opening slice with `classify_c3_ranges_v2.py`
3. build xref/call-anchor evidence for likely entries with `build_call_anchor_report_v2.py`
4. close the first honest owner/helper/data split in `1318..1816`
5. write/update manifest
6. validate with `validate_labels_v2.py`
7. refresh progress using `update_bank_progress_v2.py`

### Important caution
Do **not** force `1318..1816` into one monolithic owner just because it is the next wide lane.
The recent `C3` work has repeatedly shown that the honest move is often:
- small data/control prefix
- owner
- helper
- data island
- veneer
- marker/text

Assume mixed content until proven otherwise.

---

## Known strong recent labels worth preserving

These are especially important because they survived later audit or are structurally strong.

- `ct_c3_selected_7e_7f_band_initializer_and_32_step_saturating_add_subtract_wram_stream_worker`
- `ct_c3_external_byte_mix_helper_updating_0386_and_returning_start_byte_for_c0_fe_chained_table_walk`
- `ct_c3_7f_tile_strip_builder_with_regenerate_reuse_blank_fast_paths_and_sampled_byte_to_planar_4bpp_pack_core`
- `ct_c3_wram_runtime_code_emitter_writing_generated_stub_bytes_through_2180`
- `ct_c3_stream_bytecode_interpreter_updating_0920_0940_and_dispatching_apu_command_words`
- `ct_c3_stream_word_fetch_helper_advancing_20_and_caching_fetched_word`
- `ct_c3_selected_bank_four_edge_scanline_owner_ordering_four_xy_pairs_and_materializing_row_spans_to_7e_or_7f`
- `ct_c3_selected_bank_edge_rasterizer_storing_one_x_intercept_byte_per_scanline_with_common_epilogue`
- `ct_c3_inline_ascii_code_end_c3_marker`
- `ct_c3_post_code_end_inline_data_padding_block_with_zero_spacer_and_short_control_tail_before_next_callable_lane`
- `ct_c3_inline_control_dispatch_data_block_preceding_higher_c3_execution_body`
- `ct_c3_attached_terminal_tail_of_helper_rooted_at_0800_pending_full_upstream_closure`

---

## Remaining toolkit refinement ideas

These are no longer emergency missing pieces, but they are still worth doing later.

### Useful future refinements
- unify static and generated bank progress into one authoritative generated-first flow
- make pass publishing fully automatic from manifest + templates
- tighten xref scanning beyond raw pattern matching into richer disassembly-aware reporting
- make the classifier bank-tuned with more project-specific heuristics
- add more bank progress indexes beyond `C3`
- add stronger rebuild-readiness checks tied to eventual assembler output

### Important note
These are refinements, not blockers.
The project is now in a state where forward disassembly can continue without first inventing more infrastructure.

---

## What the next session should do first

### First action
Continue at:
- **`C3:1318..C3:1816`**

### Use this workflow
- stay on `live-work-from-pass166`
- use the repo-native toolkit
- generate/refresh a manifest for the new pass
- treat the repo as the canonical state, not chat

### Do not waste time re-auditing immediately again unless new evidence appears
The recent revisit backlog has already been cleared enough to move forward.

---

## Short no-BS summary

The repo-first transition is done.
The toolkit is substantially upgraded and lives in the repo.
The recent pass history is backfilled with manifests.
The last major revisit candidates were audited.
One of them corrected a real mistake (`08A9..08B2`), and the rest held up.

The project is now ready to continue forward again.

### Next real target
- **`C3:1318..C3:1816`**

