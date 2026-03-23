# Chrono Trigger Disassembly Labels — Pass 42

This file contains labels newly added or materially strengthened in pass 42.

As in prior passes:
- **strong** = control flow and data role are directly supported by the ROM work in this pass
- **provisional** = structurally useful but still not safe as a final gameplay-facing name

---

## Strong labels

### C1:B575  ct_c1_service7_reconcile_canonical_record_lane_pairs          [strong]
- Initializes `B3EB..B3F3` to `FF`, seeds root lane IDs `0/1/2`,
  then reads the packed category bytes from `93F3 / 93FA / 9401`
  and reconciles them into lane-family scratch arrays plus the
  final enabled-lane mask in `B3E7..B3E9`.
- This is the concrete front-end of the downstream `93F3` family.

### 7E:B3E7  ct_c1_service7_enabled_lane0_flag                            [strong]
### 7E:B3E8  ct_c1_service7_enabled_lane1_flag                            [strong]
### 7E:B3E9  ct_c1_service7_enabled_lane2_flag                            [strong]
- Final enabled-lane flags derived from the canonical trio’s lane-ID pairs
  plus the lane-block eligibility test at `FD:A8A5`.

### FD:A8A5  ct_fd_service7_lane_block_is_eligible                        [strong]
- Tests one of three `0x80`-spaced WRAM lane blocks selected by lane ID
  `0/1/2`.
- Uses:
  - `5E4A + lane*0x80`, bit 7
  - `5E4E + lane*0x80` OR `5E53 + lane*0x80`, bit 7
  - `5E4B + lane*0x80`, bits `7/2/1` (`#86`)
- Sets `B3EA = 1` on any qualifying hit.

### 7E:B3EA  ct_fd_service7_lane_eligibility_hit                          [strong]
- Scratch result written by `FD:A8A5`.
- Nonzero means the currently tested lane family has a qualifying lane block.

### FD:A93C  ct_fd_service7_dispatch_enabled_lane_clear_phase            [strong]
- Iterates enabled lanes in `B3E7..B3E9`.
- Calls `FD:A8CE` for each enabled lane.

### FD:A8CE  ct_fd_service7_clear_canonical_record_lane                  [strong]
- Computes `X = lane * 7`.
- Clears canonical fixed-record fields:
  - `93EE + X`
  - `93EF + X`
  - `93F3 + X = FF`
- Then resets matching lane-carried state via `B158/AFAB/99DD/9F22/B188/B03A`.

### FD:A95F  ct_fd_service7_dispatch_enabled_lane_refresh_phase          [strong]
- Iterates enabled lanes in `B3E7..B3E9`.
- Calls `FD:A8FE` for each enabled lane.

### FD:A8FE  ct_fd_service7_clear_occupied_lane_and_refresh_service2     [strong]
- Checks `B188[lane]`.
- If the lane is marked/occupied, performs the same canonical-record clear
  and lane-state reset as `FD:A8CE`, then invokes `C1:B961`.

### C1:B961  ct_c1_local_service2_wrapper                                [strong]
- Exact wrapper:
  - `LDA #$02`
  - `JSR $0003`
  - `RTL`
- Invokes local service 2 through the bank-C1 dispatcher.

---

## Strengthened existing labels

### 7E:93F3  ct_c1_service7_record_lane_pair                             [strong]
- Stronger than pass 41.
- The packed byte is no longer just “small dispatch categories.”
- It is now best read as a packed pair of **lane IDs** for the canonical
  fixed records, with observed values:
  - `0`
  - `1`
  - `2`
  - `F` = none / disabled

### 7E:93EE  ct_c1_service7_record_status_flags                           [strong]
- Strengthened by `FD:A8CE` / `FD:A8FE`, which explicitly clear this field
  when a canonical record lane is reset.

### 7E:93EF  ct_c1_service7_record_aux_flags                              [strong]
- Strengthened by `FD:A8CE` / `FD:A8FE`, which explicitly clear this field
  when a canonical record lane is reset.

---

## Provisional labels

### 7E:B158  ct_c1_service7_lane_carried_value                            [provisional]
- Copied into `AFAB`, `99DD`, and `9F22` during lane clear/reset.
- Structural role is real; gameplay-facing meaning is still unresolved.

### 7E:B188  ct_c1_service7_lane_occupied_or_latched_flag                 [provisional]
- Gates the extra refresh path in `FD:A8FE`.
- Strongly looks like a lane-occupied / lane-latched byte, but still needs
  a cleaner subsystem-level proof.

### 7E:AFAB  ct_c1_service7_lane_shadow_value_0                           [provisional]
### 7E:99DD  ct_c1_service7_lane_shadow_value_1                           [provisional]
### 7E:9F22  ct_c1_service7_lane_shadow_value_2                           [provisional]
- Three destinations that receive `B158[lane]` during lane clear/reset.
- Their exact downstream semantics are still open.

### 7E:B03A  ct_c1_service7_lane_aux_reset_field                          [provisional]
- Cleared during both lane-reset helpers.
- Real reset role is proven; human-facing meaning is still open.

### 7E:9F38  ct_c1_service7_slot_aux_flags_for_emitted_records            [provisional]
- Carried forward from pass 41.
- Still a valid sink-side label because its low bits feed `93EF` on emit,
  but pass 42 did not pin a trustworthy producer path.

---

## Notes
- Pass 42 materially tightened the downstream `93F3` family: the nibble
  values now look like **lane IDs `0/1/2` plus `F = none`**, not arbitrary
  tiny dispatch values.
- The main unresolved seam has shifted again:
  1. service 2 in the contexts reached from `FD:A8FE`
  2. the carried-state bytes `B158/B188/AFAB/99DD/9F22/B03A`
  3. the upstream producer path for `9F38[x]`
