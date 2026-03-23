# Chrono Trigger Labels — Pass 73

## Purpose
This file records the label upgrades justified by pass 73.

Pass 73 re-opened the helper/controller seam left by pass 72:

- global `9C`
- selector-control local `45`
- helper chain around:
  - `C1:8CF9`
  - `C1:E89F`
  - `C1:EBF8`
  - `C1:EC7F`

The main architectural correction is that the `AD9C/AD9E/EBF8/EC7F` family is now best read as a concrete **pending signed stat-delta packet system**, not vague lane-geometry glue.

---

## Strong helper labels

### C1:E89F..C1:E8BE  ct_c1_compute_ad9c_packet_offset_from_ad9b_and_b1fd   [strong]
- Computes `DP0E = 0x2C * AD9B + 4 * B1FD`.
- Uses the already-locked `C90B` 16-bit multiply helper.
- This is the exact packet-slot offset calculator for one 4-byte entry inside a `0x2C`-byte record family.

### C1:E8C0..C1:E8E0  ct_c1_compute_ad9c_packet_offset_from_ad9b_and_b18b   [strong]
- Computes `DP10 = 0x2C * AD9B + 4 * B18B`.
- Companion packet-slot offset calculator using `B18B` instead of `B1FD`.

### C1:EBF8..C1:EC38  ct_c1_queue_signed_pending_stat_delta_packet_into_b328_family   [strong structural]
- Mirrors `B202 -> B203` and negates `AD89` when `B202.bit7` is set.
- Computes a 4-byte packet slot offset from `B2C7` and the `0x2C` record stride.
- Writes the signed 16-bit amount into `B328[offset]` and the packet flag byte into `B32B[offset]`.
- Strongest safe reading: queue one signed pending HP/secondary-stat delta packet.

### C1:EC39..C1:EC7E  ct_c1_clear_nonpersistent_pending_stat_delta_channels   [strong structural]
- Scans the three parallel packet families rooted at `B328`, `B354`, and `B380`.
- If none of the corresponding flag bytes carry bit `0x20`, clears the channel data.
- Also clears associated scratch/export bytes such as `AEB2`, `AEB0`, and `AE82` on the loop tail.

### C1:EC7F..C1:ED87  ct_c1_apply_pending_stat_delta_channels_and_clamp_lane_currents   [strong structural]
- Calls the non-persistent channel clearer first.
- Applies queued signed packet amounts into `5E30/5E32` for the primary current/cap pair.
- Applies queued signed packet amounts into the parallel `5E34/5E36` pair for packets on the secondary-stat route.
- Clamps the resulting current values and performs lane refresh side effects such as `5E4A.bit7` handling and `FD:ABA2` calls when needed.

### C1:8CF9..C1:8EA6  ct_c1_run_tail_lane_selector_control_stream_and_materialize_head_state   [strong structural]
- Initializes current-tail context from `AEC8`, `B252`, and `B18B` and clears selection/result scratch.
- Chooses the command-stream pointer from the saved per-tail pointer pair `B1D4/B1E4` or the continuation pointer in `B273`.
- Fetches the current `CC` byte into `AEE3` and dispatches through the selector-control table at `B88D`.
- Uses `AD8E/AECC/AECB/AE91` and visible-head vacancy scans to materialize or update head-slot assignment/state.
- Maintains saved continuation state such as `B1D4`, `B2C0`, and `AE55`.

---

## Strengthened global label

### C1:8461..C1:883B  ct_global_opcode_9C_service7_tail_lane_admission_reseat_and_readiness_refresh_controller   [strong structural]
- Walks the tail-lane band through `B315/B252/B18B` and the `B179/B163` mapping.
- Services eligible occupied tail lanes, invoking `8CF9` to run the tail selector-control/materialization stream.
- On the follow-up path mirrors `B158 -> AFAB`, applies `BD6F` readiness modifiers, and sets `B03A = 1`.
- Then runs canonical/head-visible reconciliation and readiness-gauge export refresh through helpers such as `B575` and `B725`.
- Strongest safe reading: service-7 tail-lane admission/reseat plus readiness-refresh controller.

---

## Strengthened promoted selector-control local

### C1:8461..C1:883B  ct_service7_tail_lane_admission_reseat_and_readiness_refresh_controller   [strong structural]
- Local selector-control ownership of global `9C`.
- Carries the same upgraded reading: outer controller for eligible tail-lane admission/reseat, readiness-shadow refresh, and downstream canonical/head-visible reconciliation.

---

## Honest caution
Three things should stay explicit even after this pass:

- the fourth byte in each 4-byte packet record remains unresolved here
- the final gameplay-facing noun of the `5E34/5E36` pair is still slightly below fully frozen
- `8CF9` is now structurally strong, but some continuation/result fields like `B242` and `AE55` still want a tighter pass
