# Chrono Trigger Disassembly — Master Handoff (Session 11)

## What this handoff is

This is the updated source-of-truth handoff after the post-session-10 forward run, the xref/anchor-validation toolkit upgrade, the new repo README, and continued cautious disassembly through bank `C3`.

This file is meant to let the next session continue immediately without re-deriving the project state.

---

## Current top-line state

- **Latest completed pass:** `181`
- **Current working branch:** `live-work-from-pass166`
- **Repo:** `DocDamage/chronotrigger_disassembly`
- **Current forward target:** `C3:1C00..`
- **Overall completion estimate:** `~73.6%`
- **Source of truth:** the GitHub repo branch, not chat exports or old toolkit zips
- **Current toolkit direction:** repo-native, manifest-backed, bank-aware xref validation now in place

---

## Biggest changes since Session 10

Session 10 ended with:
- latest pass `171`
- live seam `C3:1318..C3:1816`
- completion `~71.7%`

That state is no longer current.

What happened after that:
- passes `172` through `181` were added to the repo
- the entire `C3:1318..C3:1BFF` forward lane was advanced via a long series of cautious mixed-content closures and tiny executable splits
- the earlier assumed anchor for `C3:17BD` was **corrected as invalid**
- the toolkit was upgraded to stop bank-mismatch xref mistakes and to rank caller evidence by quality
- a root `README.md` was added to the repo

---

## Repo-first rule still in force

### Canonical workflow
- **GitHub repo is the source of truth**
- **`live-work-from-pass166` is the live working branch**
- toolkit lives in `tools/`
- manifests live in `passes/manifests/`
- per-pass notes live in `passes/disasm/` and `passes/labels/`
- handoffs now belong in `handoffs/`
- chat files are snapshots only

### Working rule
A pass is not real until the repo branch contains the pass files.

---

## Current toolkit status

The toolkit is stronger than it was in Session 10.

### Existing repo-native toolkit core still present
- `tools/README.md`
- `tools/docs/repo_layout.md`
- `tools/docs/workflow.md`
- `tools/docs/confidence_levels.md`
- `tools/config/pass_manifest_schema.json`
- `tools/config/label_validation_rules.yaml`
- `tools/config/next_target_scoring.yaml`
- `tools/config/bank_c3_progress.json` *(older static snapshot; do not treat it as current by itself)*
- `reports/bank_c3_progress.md` *(older static snapshot; useful history, not current truth by itself)*

### Key older toolkit scripts still in play
- `tools/scripts/find_next_callable_lane_v2.py`
- `tools/scripts/classify_c3_ranges_v2.py`
- `tools/scripts/build_call_anchor_report_v2.py`
- `tools/scripts/validate_labels_v2.py`
- `tools/scripts/update_bank_progress_v2.py`
- `tools/scripts/publish_pass_bundle_v2.py`
- `tools/scripts/audit_pass_manifests_v1.py`
- `tools/scripts/audit_branch_state_v1.py`

### New toolkit upgrades added this session
- `tools/scripts/snes_utils_hirom_v2.py`
- `tools/scripts/manifest_xref_utils.py`
- `tools/scripts/build_call_anchor_report_v3.py`
- `tools/scripts/scan_range_entry_callers_v2.py`
- `tools/scripts/detect_tiny_veneers_v1.py`
- `tools/scripts/run_c3_candidate_flow_v1.py`
- `tools/scripts/emit_bank_c3_progress_v1.py`
- `tools/docs/xref_anchor_validation_upgrade.md`
- root `README.md`

### Why these upgrades matter
They directly address the exact failure modes that showed up during passes `176+`:
- fake cross-bank same-bank anchors
- over-trusting callers that live in unresolved mixed-content regions
- missing tiny executable splinters like wrappers, branch pads, and one-byte return stubs
- rejecting low addresses like `C3:1817` because of an overly strict mapper
- wasting time manually stitching the new seam workflow together every pass

### New practical workflow for shaky seams
1. run `detect_tiny_veneers_v1.py`
2. run `scan_range_entry_callers_v2.py`
3. run `run_c3_candidate_flow_v1.py` for one-shot triage if needed
4. run `build_call_anchor_report_v3.py` on the strongest-looking survivors
5. only promote code when both byte structure and caller quality hold up

### Honest toolkit status now
The toolkit is good enough to keep moving.
It is **better than Session 10**, but it is still heuristic rather than a full disassembly database / assembler-backed system.

Still true:
- the project can continue forward without a giant infrastructure detour
- the new xref flow is worth using on every mixed-content seam

---

## Pass manifest status now

Recent manifests present in the repo:
- `pass163.json` through `pass181.json`

That means the active repo-first phase is now machine-readable through the current pass.

---

## What happened in passes 172–181

### Pass 172
Closed:
- `C3:1318..C3:13F7` as mixed control/dispatch + DMA/setup blob
- `C3:13F8..C3:13FB` as tiny wrapper `JSR $EB7B ; RTS`

### Pass 173
Closed:
- `C3:13FC..C3:15E3` as mixed control/table/helper blob
- `C3:15E4..C3:15E8` as tiny wrapper `JSL $C302DD ; RTS`

### Pass 174
Closed:
- `C3:15E9..C3:16A7` as code-looking mixed blob
- `C3:16A8..C3:16AB` as tiny wrapper `JSR $2629 ; RTS`

### Pass 175
Closed:
- `C3:16AC..C3:16B9` as small local looping helper
- `C3:16BA..C3:17BC` as mixed content before the supposedly anchored `17BD` target

Important outcome:
- this pass originally handed the seam to `17BD` because of a claimed caller

### Pass 176
Corrective pass.
Closed:
- `C3:17BD..C3:1816` as mixed opcode-looking inline blob

Important correction:
- the supposed `C4:CE36 -> C3:17BD` anchor was **wrong**
- it was a same-bank `JSR $17BD` inside bank `C4`, so it targeted `C4:17BD`, not `C3:17BD`

This is one of the main reasons the toolkit upgrade was needed.

### Pass 177
Closed:
- `C3:1817..C3:1818` as tiny branch landing pad `BRA $17EF`
- `C3:1819..C3:187F` as mixed content
- `C3:1880..C3:1880` as one-byte `RTL` stub with same-bank `JMP` caller

Important outcome:
- `1817` is real executable bytes, but **not** a normal owner start

### Pass 178
Closed:
- `C3:1881..C3:18FC` as mixed opcode/register-setup blob

Important outcome:
- multiple tempting targets in the `1880s` failed caller-quality review

### Pass 179
First pass explicitly led by the upgraded flow.
Closed:
- `C3:18FD..C3:1A5F` as mixed cluster before `1A60`

Important outcome:
- a pretty `JSR ... ; RTS` pattern at `1989..198C` was rejected because it pointed into the already-frozen post-marker data block at `C3:11BA`
- this is exactly the kind of false-positive the new workflow is meant to catch

### Pass 180
Closed:
- `C3:1A60..C3:1AD5` as mixed opcode cluster
- `C3:1AD6..C3:1ADA` as confirmed veneer `JSL $C30D0E ; RTS`
- `C3:1ADB..C3:1AEF` as table-like inline data after the veneer

Important outcome:
- `C3:1AD6..1ADA` is one of the strongest small executable splits in the recent lane because it targets the already-closed `C3:0D0D..C3:0D5B` owner

### Pass 181
Closed:
- `C3:1AF0..C3:1BFF` as mixed opcode cluster with weak `RTL` stub candidate and unstable multi-target pocket

Important outcome:
- `1AF0` was **not** promoted just because it is `RTL`
- `1BF7` was **not** promoted just because it had multiple raw jumps
- `1C00` is now the next better seam because its local bytes look more coherent than the noisy lead-in

---

## Current bank C3 state

### Low-bank state
Still closed through the explicit marker and immediate post-marker gap:
- `C3:10C0..C3:10CF` = `CODE END C3`
- `C3:10D0..C3:12FF` = post-marker inline data/padding

### Higher-lane state now
The old Session 10 target:
- `C3:1318..C3:1816`

has now been consumed into a sequence of smaller closures, corrections, and executable splinters.

Since then, progress continued through:
- `1817..1880`
- `1881..18FC`
- `18FD..1A5F`
- `1A60..1AEF`
- `1AF0..1BFF`

### Current live seam
- **`C3:1C00..`**

This is the real next forward target.

---

## Why `C3:1C00..` is the right next seam

Because the bytes before it have now been handled honestly:
- weak `RTL` at `1AF0` was not over-promoted
- noisy `1BF7` pocket was not promoted just because it had raw jump traffic
- `1C00` is the first later in-order target in this pocket whose local byte structure looks more coherent than the unstable lead-in

Important caution:
`1C00` is **better-supported**, not yet “solved.”
It still has to earn executable status under the upgraded flow.

---

## Strong recent labels worth preserving

These remain structurally important in the current forward story:

- `ct_c3_stream_bytecode_interpreter_updating_0920_0940_and_dispatching_apu_command_words`
- `ct_c3_stream_word_fetch_helper_advancing_20_and_caching_fetched_word`
- `ct_c3_wram_data_quad_writer_to_0700_with_duplicated_sample_bytes_and_shift_decay_update`
- `ct_c3_selected_bank_four_edge_scanline_owner_ordering_four_xy_pairs_and_materializing_row_spans_to_7e_or_7f`
- `ct_c3_selected_bank_edge_rasterizer_storing_one_x_intercept_byte_per_scanline_with_common_epilogue`
- `ct_c3_inline_ascii_code_end_c3_marker`
- `ct_c3_post_code_end_inline_data_padding_block_with_zero_spacer_and_short_control_tail_before_next_callable_lane`
- `ct_c3_tiny_long_wrapper_calling_c302dd_then_returning`
- `ct_c3_small_local_looping_helper_returning_after_backward_branch`
- `ct_c3_tiny_branch_landing_pad_redirecting_execution_back_to_17ef`
- `ct_c3_single_byte_rtl_return_stub_reached_via_local_jump`
- `ct_c3_tiny_long_wrapper_calling_c30d0e_then_returning`

---

## Current known pitfalls

### 1. Do not trust raw pattern hits by themselves
This is the biggest lesson of the recent run.

Examples:
- bogus `17BD` caller story
- false wrapper signature at `1989..198C`
- weak `RTL` at `1AF0`
- noisy multi-hit pocket at `1BF7`

### 2. Same-bank `JSR/JMP` must always be bank-aware
A same-bank opcode in bank `C4` is not evidence for bank `C3`.

### 3. Mixed-content islands are normal in this lane
The honest shape has repeatedly been:
- mixed lead-in
- tiny executable splinter
- table/data block
- weak candidate seam

Do not force big monolithic owners just because the lane is wide.

### 4. Tiny executable splinters matter
The upgraded workflow is especially good at finding:
- `JSR/JSL ... ; RTS` wrappers
- one-byte `RTL` stubs
- `BRA` landing pads

These are often the only honest code claims inside a noisy region.

---

## What the next session should do first

### First action
Continue at:
- **`C3:1C00..`**

### Recommended workflow
Use the upgraded flow, in this order:

1. `detect_tiny_veneers_v1.py` on a conservative opening slice beginning at `1C00`
2. `scan_range_entry_callers_v2.py` on the same slice
3. `run_c3_candidate_flow_v1.py` if a quick triage summary would help
4. `build_call_anchor_report_v3.py` on the strongest-looking survivors
5. only then decide whether `1C00` is a real owner/helper start or just the next mixed-content island

### Good default approach
- keep the opening slice small
- assume mixed content until caller quality and byte structure both agree
- peel out small wrappers/helpers if they are real
- do **not** promote `1C00` just because it looks better than `1BF7`

---

## Remaining toolkit refinement ideas

These are not blockers, but they are still worth doing later.

### Useful future refinements
- update or replace the old static `bank_c3_progress.json` / `bank_c3_progress.md` with generated current snapshots as part of the standard flow
- unify publisher + progress emission into one cleaner repo-native publish command
- add bank-tuned seam heuristics beyond the current generic classifier layer
- strengthen rebuild-readiness checks for eventual assembler output
- add similar generated progress views for banks beyond `C3`

### Important note
These are refinements, not immediate blockers.
The project can continue forward now.

---

## Short no-BS summary

Session 10 ended at `C3:1318..1816`.
That is no longer the target.

The project pushed forward through passes `172–181`, corrected a fake anchor at `17BD`, upgraded the toolkit to do bank-aware caller validation, and advanced the real forward seam to:
- **`C3:1C00..`**

The current lane is still mixed-content heavy.
The upgraded workflow is now the right way to work it.

### Next real target
- **`C3:1C00..`**
