# Chrono Trigger Labels — Pass 104

## Purpose
This file records the label upgrades justified by pass 104.

Pass 103 froze the owner-side helper siblings `CD:0D93` and `CD:0DB1`, but not the higher-level chooser that decides whether either one runs.

Pass 104 closes that chooser seam and proves the local `$47` wait helper through the installed `0501/0503 -> D1:F4C0` RAM-trampoline target.

---

## Strong labels

### CD:0534..CD:053A  ct_cd_return_zero_when_ca1f_is_clear_else_one   [strong]
- Exact body is now frozen:
  - `LDA $CA1F`
  - `BEQ done`
  - `LDA #$01`
  - `RTL`
- Strongest safe reading: tiny exact status probe used as a zero/nonzero predicate on `CA1F`.

### CD:83DA..CD:83ED  ct_cd_wait_until_ca1f_clears_then_stage_ca25_0e_and_increment_ca24_before_helper_choice   [strong structural]
- Exact body is now frozen:
  - `JSR CD:3E7D`
  - `JSL CD:0534`
  - loop until result is zero
  - `LDA #$0E ; STA $CA25`
  - `INC $CA24`
  - `JSR CD:3E7D`
- Strongest safe reading: exact pre-launch wait wrapper that blocks while `CA1F` is nonzero, then advances the local `CA25/CA24` stage markers before entering the helper chooser.

### CD:83EE..CD:840C  ct_cd_choose_between_blocking_helper_0db1_and_0d93_by_2a21_bits_4_0_and_7f01ec_zero_state   [strong structural]
- Exact chooser matrix is now frozen:
  - if `(2A21 & 0x11) == 0`: call neither helper
  - if `2A21.bit0 == 1` and `7F:01EC == 0`: `JSR CD:0DB1`
  - if `2A21.bit0 == 0` but `2A21.bit4 == 1` and `7F:01EC != 0`: `JSR CD:0D93`
  - all other combinations call neither helper
- Strongest safe reading: exact local chooser for the pass-103 helper siblings.
- This settles the old seam directly:
  - `2A21 & 0x11` is the precondition mask that makes this split live at all
  - `7F:01EC` does not choose alone; it only selects inside that tighter local matrix

### CD:840D..CD:8449  ct_cd_stage_ca25_08_install_d1_f4c0_ram_trampoline_wait_on_47_optionally_wait_2141_clear_run_c0_000b_and_wait_again   [strong structural]
- Exact body is now frozen:
  - `LDA #$08 ; STA $CA25 ; INC $CA24 ; JSR CD:3E7D`
  - install exact RAM-trampoline target fields `0501/0503 = D1:F4C0`
  - `LDA $BB00 ; STA $45`
  - `JSR CD:044A`
  - if `2A1F.bit6 == 0`, wait until `$2141 == 0`
  - `STZ $2A21`
  - `JSL C0:000B`
  - `TDC ; JSR CD:044A ; RTL`
- Strongest safe reading: exact post-chooser launch wrapper around the `D1:F4C0` RAM-trampoline target and the already-frozen `C0:000B` submit path.

### CD:044A..CD:0452  ct_cd_wait_for_one_ram_trampoline_nmi_cycle_via_47_latch   [strong structural]
- Exact body is now frozen:
  - `LDA #$01 ; STA $47`
  - loop while `$47 != 0`
  - `RTS`
- Pass 104 also proves the other side of the contract:
  - the wrapper at `CD:8418..8420` installs RAM-trampoline target `D1:F4C0` through `0501/0503`
  - the first live front-edge instructions at `D1:F4C0` include `STZ $47`
- Strongest safe reading: exact one-shot wait helper for one RAM-trampoline / NMI cycle.

### 7E:2A21  ct_cd_transient_side_and_launch_control_mask_byte_with_exact_bit0_bit4_helper_gate_role   [stronger structural]
- Earlier passes already proved bit 0 matters in other selector/side-sensitive paths.
- Pass 104 adds an exact local chooser contract:
  - `CD:83EE` first gates on `2A21 & 0x11`
  - bit 0 then selects which helper branch is even eligible
  - `CD:8438` clears `2A21` after the launch wrapper finishes
- Strongest safe reading now: transient side/control mask byte whose bit 0 and bit 4 jointly gate this launch-time helper chooser.
- Final gameplay-facing noun of bit 4 remains open.

### 7F:01EC  ct_cross_subsystem_special_case_selector_byte_with_local_zero_nonzero_helper_choice_role   [stronger structural]
- Pass 92 already proved an exact-value special case in the C0 packet-submit family.
- Pass 104 adds a second clean consumer:
  - zero permits `CD:0DB1` on the `2A21.bit0 == 1` side
  - nonzero permits `CD:0D93` on the `2A21.bit0 == 0 && bit4 == 1` side
- Strongest safe reading now: cross-subsystem special-case selector byte with both exact-value and zero/nonzero consumers.

### 00:0047  ct_cd_ram_trampoline_cycle_completion_latch   [strong structural]
- `CD:044A` sets `$47 = 1` and waits for it to clear.
- The installed RAM-trampoline target at `D1:F4C0` clears `$47` with exact `STZ $47`.
- Strongest safe reading: one-shot completion latch for the local RAM-trampoline / NMI wait contract.

### 00:0501..00:0503  ct_c0_ram_trampoline_target_pointer_fields_reused_here_for_d1_f4c0   [stronger structural]
- Pass 2 already proved `0500..0503` is the RAM trampoline slot.
- Pass 104 adds a clean new install site:
  - `CD:8418..8420` writes exact target `D1:F4C0` into `0501/0503`
- Strongest safe reading: target pointer fields for the RAM trampoline entry, reused here to point at `D1:F4C0`.

---

## What this pass settles about the old seam
- `CD:83EE..840C` is now exact enough to stop calling it a vague chooser neighborhood.
- `2A21 & 0x11` matters because it is the exact precondition mask for this whole helper split.
- `7F:01EC` does not independently pick `0D93` versus `0DB1`; it only selects inside the tighter `2A21`-gated matrix.
- `CD:044A` is not just a delay helper anymore; it is a real wait-for-one-RAM-trampoline/NMI-cycle helper through `$47`.
- `CD:840D..8449` is now a real post-chooser launch wrapper around `D1:F4C0` and `C0:000B`.

---

## Honest caution
Even after this pass:

- I have **not** frozen the final gameplay-facing noun of `CA1F`, `CA24`, or `CA25`.
- I have **not** frozen the final gameplay-facing noun of `BB00` or the byte forwarded through `$45 -> $2100`.
- I have **not** frozen the full higher-level role of `D1:F4C0`; I only used the exact front-edge proof needed to close the `$47` wait contract.
- I have **not** frozen the final gameplay-facing noun of `2A21.bit4`.
