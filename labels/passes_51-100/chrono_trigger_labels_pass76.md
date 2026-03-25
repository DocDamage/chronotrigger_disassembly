# Chrono Trigger Labels — Pass 76

## Purpose
This file records the label upgrades justified by pass 76.

Pass 75 proved that the late fixed follow-up tail enters service `04`, but it still left service `04` itself too vague.

Pass 76 closes that gap by proving:

- `AE92` is the service-04 mode byte
- `431D` is the local service-04 mode dispatcher
- the two already-proved late callers split into different service-04 modes:
  - `BFAA` -> mode `1`
  - `895B` -> mode `2`
- both active modes converge into the same shared output/materialization runner at `4833`

This is the first pass where service `04` can be described as a real local subsystem rather than a generic hook.

---

## Strengthened helper labels

### C1:431D..C1:432A  ct_c1_service04_mode_dispatcher_by_ae92   [strong]
- Loads `AE92`, clamps any value `>= 4` to mode `0`, then dispatches through the jump table at `C1:7A63`.
- Proven table entries:
  - mode `0` -> `475A`
  - mode `1` -> `432C`
  - mode `2` -> `45A0`
  - mode `3` -> `475B`
- This is the real local mode dispatcher behind service `04`.

### C1:432C..C1:459F  ct_c1_service04_mode1_load_current_context_profiles_by_source_slot_and_run_common_emit_tail   [strong structural]
- Mode-1 front end reached when `AE92 = 1`.
- Splits immediately on `AE91 < 3` vs `AE91 >= 3`.
- Head-slot branch uses transformed slot state plus parallel bank-`CD` table families around `4000/4007/400E` and `4015/401A/401F`.
- Tail-slot branch reduces `AE91 - 3`, uses `9853[tail_local]`, and loads tail-family profiles from `CD:4926...` or `CD:4F26...` depending on `AE93`.
- Both branches populate the `9877 / 987A / 987B / 987E / 9881 / 9884` working neighborhood and converge into `4833`.
- Strongest safe reading: service-04 mode-1 current-context profile loader/emitter front end.

### C1:45A0..C1:4758  ct_c1_service04_mode2_load_fixed_followup_profiles_by_source_slot_and_run_common_emit_tail   [strong structural]
- Mode-2 front end reached when `AE92 = 2`.
- This is the exact service-04 mode used by `895B`, and therefore by the fixed-`7F` follow-up path already proved in passes 74–75.
- Head-slot branch loads a 7-byte record from `CD:45A6 + 7*AE93` into the `9877..9884` working bytes plus `987C`.
- Tail-slot branch loads the matching 7-byte record family from `CD:5526 + 7*AE93`.
- Both branches converge into `4833` after the shared bank-`D1/CD/CE` derivation chain.
- Strongest safe reading: service-04 mode-2 fixed-follow-up profile loader/emitter front end.

### C1:4833..C1:48E7  ct_c1_service04_common_output_materialization_and_emit_finalize_runner   [strong structural]
- Shared convergence tail used by both active service-04 modes proved in this seam.
- Consumes the working bytes built in the `9877..9885` neighborhood.
- Runs `JSL CD:0015` and `JSL CD:002A` unconditionally.
- Runs `JSL CD:0018` only when `AE93 != 0x37`, `AE94 == 0`, and `987C != 0xFF`.
- Calls `48EC`, prepares the `7E:2D00..` workspace for a `C3:0002` call, then runs `4943` eight times.
- Emits sixteen 6-byte output records into the `5D00..` family while setting `A07B[...] = 1`.
- Final gameplay-facing noun for the emitted thing remains open, but the common output/materialization role is now strong.

### C1:48EC..C1:493F  ct_c1_service04_parse_ce_profile_stream_into_a280_a2a0_work_vectors   [provisional strengthened]
- Consumes `9885` as the source index.
- Walks a bank-`CE` byte stream and partitions entries into the `A280..` and `A2A0..` work-vector families.
- This is clearly a service-04-local stream/parser helper for the shared output tail, not unrelated scratch logic.

### C1:4943..C1:49FD  ct_c1_service04_build_one_output_record_batch_into_a2d3_and_a45x_workspace   [provisional strengthened]
- Consumed exactly eight times from the shared `4833` runner.
- Builds one intermediate output batch into the `A2D3..` / `4500..` workspace neighborhood before final emission into `5D00..`.
- Final emitted-object noun still needs one more pass, so the label stays structural.

---

## Strengthened state labels

### 7E:AE91  ct_c1_service04_source_or_current_slot_selector   [strong structural]
- Service-04 modes `1` and `2` immediately branch on whether `AE91 < 3` or `AE91 >= 3`.
- This byte selects the source/current slot family for the active service-04 profile loader.

### 7E:AE92  ct_c1_service04_mode_selector   [strong]
- Directly consumed by `431D`.
- Values `0..3` select service-04 mode handlers through the `7A63` table.
- Values `>=4` fall back to mode `0`.

### 7E:AE93  ct_c1_service04_profile_or_pattern_index   [strong structural]
- Used directly as the record selector in service-04 mode `2` via `X = 7 * AE93`.
- Also gates family selection inside mode `1` and suppresses/permits parts of the shared `4833` tail.
- This is no longer generic follow-up scratch; it is a real service-04 profile/pattern index.

### 7E:AE94  ct_c1_service04_optional_cd0018_stage_suppress_or_override_flag   [provisional strengthened]
- The shared `4833` runner only enters the optional `JSL CD:0018` stage when `AE94 == 0`.
- Strongest safe reading so far: suppress/override flag for one optional service-04 substage.

### 7E:9877..7E:9885  ct_c1_service04_working_profile_and_derived_output_bytes   [provisional strengthened]
- Modes `1` and `2` both populate this neighborhood before entering the shared `4833` runner.
- The bytes are then consumed by the bank-`CD/D1/CE` derivation chain and the output/materialization tail.
- Exact per-byte nouns remain open, but this is now clearly a service-04 working-profile/output buffer family.

---

## Honest caution
Even after this pass:

- service-04 modes `0` and `3` at `475A / 475B` are still open
- the final gameplay-facing noun for the `4833 / 48EC / 4943` output is still not frozen
- the 17-byte `CC:213F -> AEE6..AEF6` descriptor fields still want a dedicated pass now that the service-04 mode picture is cleaner
