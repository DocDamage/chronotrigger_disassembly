# Chrono Trigger Labels — Pass 74

## Purpose
This file records the label upgrades justified by pass 74.

Pass 74 re-opened the late seam left by pass 73:

- globals `91 / 98 / 99`
- shared helper tail:
  - `C1:895B`
  - `C1:AC57`
  - `C1:AC85`
  - `FD:ACEE`
- continuation/materialization state:
  - `B2C0`
  - `AE55`

The main architectural correction is that globals `91` and `99` are **dual-path packet callers** rather than generic geometry/helper seeders:

- they populate transient `AD9C` packet workspace
- they queue a live signed stat-delta packet through `EBF8`
- they run the shared fixed-`7F` follow-up/apply tail
- they clear the transient workspace through `FD:ACEE`

By contrast, global `98` is the stripped-down fast path that directly queues + applies one packet without the transient workspace.

---

## Strengthened global opcode labels

### C1:88C5..C1:8974  ct_global_opcode_91_compute_scaled_lane_delta_queue_live_packet_and_run_followup_7f_tail   [strong structural]
- Uses `B179[1]` or `AEC7` through the `B163` lane mapping.
- Requires `5E4A.bit7` set and `5E4B.bit6` clear for the packet path.
- Sets `AFC1[lane] = 1` and `AF32[lane] = B0DF[lane] + 5E64[lane_block]`.
- Computes a scaled amount through `5E32/33`, a `5E64`-derived scale, and `C92A`.
- Mirrors that amount into transient packet workspace at `AD9C[offset]` with mode `3` in `AD9E[offset]`.
- Clears `B202`, queues the live packet through `EBF8`, then runs `A=0x7F ; JSR 895B ; JSL FD:ACEE`.
- Strongest safe reading: scaled lane-derived dual-path packet caller with shared `7F` follow-up/apply tail.

### C1:8A9F..C1:8B0F  ct_global_opcode_98_capture_lane_b12c_variant_into_af7f_and_optionally_apply_one_point_primary_delta   [strong structural]
- Uses `B179[8]` or `AEC7` through the `B163` lane mapping.
- Captures `B12C[lane] -> AF7F[lane]` with status-based halve/double transforms.
- When `5E4B.bit4` is set, seeds `AD89 = 1`, `B1FD = lane`, `B202 = 0`, then runs `EBF8 -> EC7F` directly.
- Because the packet is primary-route and unsigned, this is the direct one-point primary-stat decrement fast path.

### C1:8B10..C1:8BB8  ct_global_opcode_99_update_lane_b019_b0a8_and_on_expiry_queue_secondary_plus5_packet_with_followup_7f_tail   [strong structural]
- Uses `B179[9]` or `AEC7` through the `B163` lane mapping.
- Updates `B019/AF8A/B0A8` on the mapped lane with the already-proved timer front end.
- On expiry and lane/block gate success, seeds `AD89 = 5`, `B1FD = lane`, mirrors the amount into transient packet workspace mode `2`, sets `B202 = 0xC0`, then runs `EBF8`.
- The `0xC0` flag byte gives the queued live packet signed-negate + secondary-route behavior.
- Finishes through `A=0x7F ; JSR 895B ; JSL FD:ACEE`.
- Strongest safe reading: timed secondary-route packet caller with the same shared `7F` follow-up/apply tail used by global `91`.

---

## New helper labels

### C1:895B..C1:8974  ct_c1_seed_fixed_followup_context_from_a_and_run_ac57_tail   [strong structural]
- Copies incoming `A` into `AE93`.
- Seeds fixed context bytes: `AE91 = 0`, `AE92 = 2`, `AE94 = 0`, `AE95 = 0`, `AE96 = 0x80`.
- Runs `JSR AC57` and returns.
- Used by both globals `91` and `99` with `A = 0x7F`.

### C1:AC57..C1:AC5D  ct_c1_run_common_followup_tail_then_apply_pending_stat_deltas   [strong structural]
- Calls `BFA4` first.
- Then calls `AC85`.
- Structural role: bridge the shared follow-up-context tail into pending stat-delta packet apply.

### C1:AC85..C1:AC88  ct_c1_apply_pending_stat_delta_channels_wrapper   [strong]
- Exact wrapper: `JSR EC7F ; RTS`.

### FD:ACEE..FD:ACFC  ct_fd_clear_ad9b_and_transient_ad9c_packet_workspace   [strong structural]
- Clears `AD9B`.
- Clears exactly `0xB0` bytes starting at `AD9C`.
- This proves the transient packet workspace spans `AD9C..AE4B`.

---

## Strengthened state labels

### 7E:AD89..7E:AD8A  ct_c1_pending_stat_delta_packet_amount_seed   [strong structural]
- 16-bit amount consumed by `EBF8` before queue write.
- Negated first when `B202.bit7` is set.

### 7E:AD9B  ct_c1_transient_packet_workspace_record_index   [strong structural]
- Record selector used by the `0x2C * record + 4 * slot` packet-workspace addressing formula.
- Explicitly cleared by `FD:ACEE`.

### 7E:AD9C..7E:AE4B  ct_c1_transient_packet_workspace_records_4x11x4   [strong structural]
- Transient packet workspace proven by the `0x2C` record stride and the `0xB0`-byte clear size in `FD:ACEE`.
- Strongest safe structure: 4 records × 11 slots × 4 bytes.

### 7E:AE55  ct_c1_materialization_descriptor_option_flags   [provisional strengthened]
- Loaded from table-driven descriptor bytes around `CC:6FCC...`.
- Consumed by the `8CF9` tail.
- Bit `3` suppresses arming the alternate continuation pointer in `B2C0`.
- Other bits still need more proof.

### 7E:B1FD  ct_c1_pending_stat_delta_packet_target_slot   [strong structural]
- Per-slot selector used by packet offset helpers like `E89F` and by `EBF8` queue writes.
- Seeded directly from the mapped lane in globals `98` and `99`.

### 7E:B202  ct_c1_pending_stat_delta_packet_flag_byte   [strong structural]
- Packet flag source mirrored into `B203` by `EBF8`.
- Bit `7` = signed-negate before queue write.
- Bit `6` = secondary-route packet path.
- Bit `5` = persistent / do-not-auto-clear channel behavior.

### 7E:B2C0  ct_c1_alternate_continuation_pointer_armed_flag   [strong structural]
- At `8CF9` entry, chooses the alternate continuation pointer in `B273` when nonzero.
- At `8CF9` tail, armed when the chosen `AECC` is in the nonhead range and `AE55.bit3` does not suppress continuation.

---

## Honest caution
Three things should stay explicit even after this pass:

- the exact human-facing meanings of transient packet workspace modes `2` and `3` are still open
- the exact consumer inside the fixed-`7F` follow-up tail is still not fully locked
- `AE55` is now materially tighter, but only bit `3` is safe to treat as pinned here
