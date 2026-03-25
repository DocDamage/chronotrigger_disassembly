# Chrono Trigger Labels — Pass 102

## Purpose
This file records the label upgrades justified by pass 102.

Pass 101 found the first clean external caller anchor for `D1:EA4B`, but the surrounding CD-side driver block was still too vague.

Pass 102 turns that caller block into an exact staged tail driver and closes the local control-byte contracts around `CE13`, `CD29`, `CD2D`, `CD2E`, and `A028`.

---

## Strong labels

### CD:8978..CD:89CB  ct_cd_tick_optional_auxiliary_tail_with_masked_d1_palette_maintenance_and_scripted_holdoffs   [strong structural]
- Exact linear flow is now frozen:
  - conditional skip or call to `CE:E18E`
  - `LDA $7C ; AND $CE13` gate before `JSL D1:EA4B`
  - optional `JSL CE:F066` only when `CD2D == 0` and `A028 == 0`
  - unconditional `JSL C1:000C`
  - optional `LDA #$40 ; JSR $3B82` only when `CD2E == 0`, `A013 != 0`, and `A028 == 0`
  - fixed tail:
    - `JSR CD:1609`
    - `LDA $CD29 ; STA $A028`
    - `JSR CD:0B1E`
    - `JSL D1:F426`
    - `JSL FD:FFF7`
    - `JSR CD:0ADE`
    - `JSL C2:8002`
    - `JSR CD:0340`
- Strongest safe reading: exact staged CD-side tail driver that conditionally runs D1 palette maintenance and two optional pre-tail helpers under script-written holdoff bytes before entering the fixed auxiliary/runtime tail.

### CD:1918..CD:191D  ct_cd_auxiliary_token_df_store_immediate_to_cd29   [strong]
- Exact body: `LDA [$40] ; STA $CD29 ; RTS`.
- This closes the previously unlabeled immediate-token sibling directly after the already-frozen `0xE0` wrapper at `CD:1913`.
- Strongest safe reading: direct immediate store token for `CD29`.

### CD:3B82..CD:3BA5  ct_cd_wait_for_latched_ppu_counter_byte_to_reach_or_pass_a_after_hblank_transition   [strong structural]
- Exact body:
  - saves caller `A` to `$45`
  - spins on `$4212` until out of vblank
  - waits for hblank set, then hblank clear
  - reads the exact latch/status/counter sequence `$2137 -> $213F -> $213D`
  - compares the resulting byte against the saved threshold
  - repeats until the latched byte is `>=` the caller threshold
- Strongest safe reading: exact raster/beam wait helper keyed by the caller threshold in `A`.

### 7E:CE13  ct_cd_mask_byte_that_suppresses_d1_palette_maintenance_when_7c_overlap_is_nonzero   [strong structural]
- Exact local consumer contract is now frozen:
  - `LDA $7C ; AND $CE13 ; BNE skip_D1_EA4B`
- Exact clean local write still stands:
  - `A9 #$03 ; STA $CE13`
- Strongest safe reading: mask byte that suppresses the D1 palette-maintenance tick when the current active `7C` bits overlap the stored mask.

### 7E:CD29  ct_cd_auxiliary_immediate_control_byte_df_mirrored_into_a028   [strong structural]
- Pass 102 freezes both ends of the contract:
  - token `CD:1918..191D` writes it directly from the stream
  - `CD:89B2..89B5` mirrors it directly into `A028`
- Strongest safe reading: staged/immediate auxiliary control byte whose live effect is mirrored into `A028` by the CD tail driver.

### 7E:A028  ct_cd_live_holdoff_latch_mirrored_from_cd29_and_used_to_skip_optional_pre_tail_helpers   [strong structural]
- `CD:8978..89CB` tests `A028` before both optional helpers and skips them whenever the byte is nonzero.
- The same block then performs the exact mirror `CD29 -> A028`.
- Another clean mapped-code reader at PC `0x014269` busy-waits until `A028 == 0`.
- Strongest safe reading: live holdoff/latch byte mirrored from `CD29` and used as a zero-gate for optional helper work.

---

## Strengthened helper readings

### CD:8985  ct_cd_clean_external_jsl_to_d1_palette_profile_maintenance_tick   [strong structural, caller context materially strengthened]
- Pass 101 froze this as the first clean external mapped-code caller of `D1:EA4B`.
- Pass 102 now freezes the full local control contract around it:
  - exact `CE13` mask gate before the call
  - exact later fixed tail after the call
- This is no longer just an isolated anchor; it sits inside an exact staged tail driver.

### 7E:CD2D  ct_cd_auxiliary_immediate_control_byte_e1   [stronger structural]
- Pass 85 froze the direct stream writer token.
- Pass 102 adds the first exact clean-code consumer contract:
  - if `CD2D != 0`, `CD:8978..89CB` skips `JSL CE:F066`
- Strongest safe reading now: immediate inhibit/skip byte for the `CE:F066` pre-tail helper.

### 7E:CD2E  ct_cd_auxiliary_immediate_control_byte_e2   [stronger structural]
- Pass 85 froze the direct stream writer token.
- Pass 102 adds the first exact clean-code consumer contract:
  - if `CD2E != 0`, `CD:8978..89CB` skips the `LDA #$40 ; JSR $3B82` raster-wait path
- Strongest safe reading now: immediate inhibit/skip byte for the gated raster/beam wait helper.

### D1:EA4B..D1:EA5E  ct_d1_guard_palette_profile_maintenance_tick_on_aux_stage_and_slot_activity_then_branch_by_ce0a   [strong structural, caller contract strengthened again]
- Pass 100 froze the exact local guard body.
- Pass 101 found the first clean external caller at `CD:8985`.
- Pass 102 now freezes the exact CD-side gating logic around that call through `CE13`.
- This materially strengthens the caller-side contract without changing the core D1 noun.

---

## Honest caution
Even after this pass:

- I have **not** frozen the final higher-level subsystem noun of `CE:F066`.
- I have **not** frozen the final gameplay-facing noun of `A013`.
- I have **not** frozen the exact higher-level noun of the full `7C` state byte.
- I have **not** frozen a clean direct static reader of `CE0F`.
