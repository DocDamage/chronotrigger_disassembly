# Chrono Trigger Labels — Pass 101

## Purpose
This file records the label upgrades justified by pass 101.

Pass 100 froze the D1 palette-transition semantics, but it still left `D1:EB4C..EB6F` below a keepable noun.

Pass 101 closes that exact seam and also anchors the first clean external caller chain for `D1:EA4B`.

The two durable upgrades are:

- `D1:EB4C..EB6F` is not a hidden selector helper; it is a **dead-output timing / cycle-burn prelude** keyed by the local `5FB0 / 5FB2` ratio
- `CD:8985` (PC `0x0D0985`) is the first clean external `JSL D1:EA4B` caller currently anchored in mapped code

---

## Strong labels

### D1:EB4C..D1:EB6F  ct_d1_burn_quantized_timing_cycles_from_5fb0_against_eighths_of_5fb2_before_selector_rebuild   [strong structural]
- Exact body:
  - `LDX #$0001`
  - `REP #$20`
  - `LDA $5FB2 ; LSR ; LSR ; LSR`
  - store that base value to `$45` and `$47`
  - repeatedly compare `5FB0` against the current threshold at `$45`
  - while `5FB0 >= threshold`, add another copy of the base step from `$47` into `$45`
  - stop once `5FB0 < threshold` or after 8 buckets
- Exact negative proof now matters too:
  - `EB70` immediately overwrites `A`
  - `EB70` immediately overwrites `X`
  - `$45 / $47` are only local scratch for the loop
  - no selector/profile/palette state survives from this prelude into `EB70`
- Strongest safe reading: quantized timing/cycle-burn prelude placed only on the `CE0A == 0` branch before the selector/profile rebuild.

### CD:8985  ct_cd_clean_external_jsl_to_d1_palette_profile_maintenance_tick   [strong structural]
- Clean mapped-code `JSL $D1EA4B` at PC `0x0D0985` (mirrored CPU view `CD:8985`).
- This is the first honest external caller anchor currently frozen for the `D1:EA4B` palette-maintenance entry.
- Strongest safe reading: clean CD-side callsite into the D1 palette-profile maintenance tick.

### CD:8978..CD:89CB  ct_cd_driver_block_that_gates_d1_palette_profile_maintenance_then_runs_neighbor_control_tail   [strong structural, cautious noun]
- Exact local facts currently frozen:
  - optional early call to `CE:E18E`
  - gate on `CE13` before `JSL D1:EA4B`
  - later exact calls include `CD:1609` and `D1:F426`
  - later tail also calls `FD:FFF7` and `C2:8002`
- Strongest safe reading: clean surrounding CD-side driver block that owns at least one real call into the D1 palette-maintenance cluster.
- Final higher-level subsystem noun is still intentionally cautious.

---

## Strengthened helper readings

### D1:EA4B..D1:EA5E  ct_d1_guard_palette_profile_maintenance_tick_on_aux_stage_and_slot_activity_then_branch_by_ce0a   [strong structural, caller-chain support strengthened]
- Pass 100 already froze the exact guard body.
- Pass 101 adds the first clean external mapped-code caller at `CD:8985` / PC `0x0D0985`.
- This moves the block from “exact local controller” to “exact local controller with one honest external driver anchor”.

### 7E:CE0A  ct_d1_active_palette_profile_convergence_latch   [support unchanged, branch interpretation strengthened]
- The `CE0A == 0` branch is now tightened further:
  - it does **not** enter another hidden selector calculator before `EB70`
  - it enters only the timing prelude at `EB4C..EB6F`, then the selector/profile rebuild proper at `EB70`
- This sharpens the branch meaning without changing the core noun.

---

## Honest caution
Even after this pass:

- I have **not** frozen the final gameplay-facing noun of `5FB0 / 5FB2`.
- I have **not** frozen the exact noun of `CE13`, `A028`, `A013`, or `CD29` inside the caller block.
- I have **not** frozen a clean direct static reader of `CE0F`.
- I am **not** claiming that `CD:8978..89CB` is fully decoded end-to-end yet; only the D1 caller anchor and its immediate local control facts are frozen.
