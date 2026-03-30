# Chrono Trigger Disassembly — Master Handoff (Session 11)

## Current top-line state
- latest completed pass: `181`
- working branch: `live-work-from-pass166`
- repo: `DocDamage/chronotrigger_disassembly`
- current forward seam: `C3:1C00..`
- completion estimate: `~73.6%`
- source of truth: the repo branch, not chat exports or old toolkit zips

## What changed since Session 10
Session 10 ended at pass `171` with the seam `C3:1318..C3:1816`.
That is no longer current.

After that:
- passes `172` through `181` were added to the repo
- the old `1318..1816` seam was consumed through a series of cautious mixed-content freezes and small executable splits
- the assumed anchor for `C3:17BD` was corrected as invalid
- the xref / anchor-validation toolkit was upgraded
- a root `README.md` was added

## Repo-first rule still in force
- GitHub repo is canonical
- `live-work-from-pass166` is the live branch
- manifests live in `passes/manifests/`
- pass notes live in `passes/disasm/` and `passes/labels/`
- toolkit lives in `tools/`
- handoffs now belong in `handoffs/`

## Toolkit status now
### Existing core still in play
- `find_next_callable_lane_v2.py`
- `classify_c3_ranges_v2.py`
- `build_call_anchor_report_v2.py`
- `validate_labels_v2.py`
- `update_bank_progress_v2.py`
- `publish_pass_bundle_v2.py`

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

### Why these matter
They directly address the recent failure modes:
- fake cross-bank same-bank anchors
- over-trusting callers from unresolved mixed-content regions
- missing tiny wrappers / branch pads / one-byte return stubs
- rejecting low addresses like `C3:1817`
- too much manual seam triage every pass

### Recommended workflow now
1. `detect_tiny_veneers_v1.py`
2. `scan_range_entry_callers_v2.py`
3. `run_c3_candidate_flow_v1.py` if quick triage helps
4. `build_call_anchor_report_v3.py` on the best survivors
5. only promote code when byte structure and caller quality both hold up

## What happened in passes 172–181
### Pass 172
- `C3:1318..13F7` frozen as mixed control/dispatch + DMA/setup blob
- `C3:13F8..13FB` split as tiny `JSR $EB7B ; RTS` veneer

### Pass 173
- `C3:13FC..15E3` frozen as mixed control/table/helper blob
- `C3:15E4..15E8` split as `JSL $C302DD ; RTS`

### Pass 174
- `C3:15E9..16A7` frozen as code-looking mixed blob
- `C3:16A8..16AB` split as `JSR $2629 ; RTS`

### Pass 175
- `C3:16AC..16B9` split as small local looping helper
- `C3:16BA..17BC` frozen as mixed content before the supposedly anchored `17BD` target

### Pass 176
Corrective pass.
- `C3:17BD..1816` frozen as mixed opcode-looking inline blob
- prior `C4:CE36 -> C3:17BD` story was invalidated; it was a same-bank `C4` hit, not real `C3` evidence

### Pass 177
- `C3:1817..1818` split as tiny branch landing pad `BRA $17EF`
- `C3:1819..187F` frozen as mixed content
- `C3:1880..1880` split as one-byte `RTL` stub with same-bank `JMP` caller

### Pass 178
- `C3:1881..18FC` frozen as mixed opcode/register-setup blob

### Pass 179
First pass explicitly led by the upgraded flow.
- `C3:18FD..1A5F` frozen as mixed cluster before `1A60`
- false wrapper at `1989..198C` rejected because it targeted `C3:11BA` inside already-frozen post-marker data

### Pass 180
- `C3:1A60..1AD5` frozen as mixed opcode cluster
- `C3:1AD6..1ADA` split as confirmed `JSL $C30D0E ; RTS` veneer
- `C3:1ADB..1AEF` frozen as table-like data after the veneer

### Pass 181
- `C3:1AF0..1BFF` frozen as mixed opcode cluster with weak `RTL` stub candidate and unstable multi-target pocket
- `1AF0` was not promoted just because it is `RTL`
- `1BF7` was not promoted just because it had multiple raw jumps
- seam advanced to `1C00..`

## Current bank C3 state
Low-bank cluster is still closed through:
- `C3:10C0..10CF` = `CODE END C3`
- `C3:10D0..12FF` = post-marker inline data/padding

Higher lane status now:
- old Session 10 target `C3:1318..1816` has been consumed into smaller closures and corrections
- progress has continued through `1BFF`
- current real forward seam is **`C3:1C00..`**

## Why `C3:1C00..` is the right next seam
Because the bytes before it have now been handled honestly:
- weak `RTL` at `1AF0` was not over-promoted
- noisy `1BF7` pocket was not promoted just because it had raw jump traffic
- `1C00` is the first later target in-order whose local byte structure looks more coherent than the unstable lead-in

Important caution:
`1C00` is better-supported, not yet solved. It still has to earn executable status under the upgraded flow.

## Strong recent labels worth preserving
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

## Known pitfalls
1. Do not trust raw pattern hits by themselves.
2. Same-bank `JSR/JMP` must always be bank-aware.
3. Mixed-content islands are normal in this lane.
4. Tiny executable splinters matter and are often the only honest code claims in a noisy region.

## What the next session should do first
Continue at:
- **`C3:1C00..`**

Recommended order:
1. `detect_tiny_veneers_v1.py` on a conservative opening slice beginning at `1C00`
2. `scan_range_entry_callers_v2.py` on the same slice
3. `run_c3_candidate_flow_v1.py` if quick triage helps
4. `build_call_anchor_report_v3.py` on the strongest-looking survivors
5. only then decide whether `1C00` is a real owner/helper start or just the next mixed-content island

## Remaining toolkit refinement ideas
- replace the stale static `bank_c3_progress.json` / `bank_c3_progress.md` with generated current snapshots in the normal flow
- unify publisher + progress emission more cleanly
- add bank-tuned seam heuristics beyond the generic classifier layer
- strengthen rebuild-readiness checks for eventual assembler output

## Short no-BS summary
Session 10 ended at `C3:1318..1816`.
That is no longer the target.

The project pushed forward through passes `172–181`, corrected a fake anchor at `17BD`, upgraded the toolkit to do bank-aware caller validation, and advanced the real seam to:
- **`C3:1C00..`**
