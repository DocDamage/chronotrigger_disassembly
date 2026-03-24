# Chrono Trigger Labels — Pass 84

## Purpose
This file records the label upgrades justified by pass 84.

Pass 83 proved the local gate behavior of `D1:F426 / F431 / F457`,
but the actual writers for `7E:CFFF` were still open.

Pass 84 closes that external control seam:

- auxiliary token `0xE6` at `CD:18C2..18C7` is now exact as the direct immediate-write token for `CFFF`
- the older primary slot-script VM has exact hard set / hard clear helpers at `C1:58DB` and `C1:58E4`
- `CFFF` can now be tightened from vague selector to a stronger **zero/nonzero suspend/restore mode byte**
- `CDC8` can now be tightened locally as the seed-vs-promote phase-side byte of the `E984 <-> E91A` half-cycle
- `CE0F` can now be tightened locally as a seed-side arm/epoch byte
- the D1 reset cluster explicitly clears `CFFF / CE0F / CE12`

I am still keeping the final gameplay-facing nouns of the palette-band pages and the exact reader(s) of `CDC8 / CE0F` one notch below frozen.

---

## Strengthened helper labels

### CD:18C2..CD:18C7  ct_cd_auxiliary_token_e6_store_immediate_to_cfff   [strong]
- Exact body: `LDA [$40] ; STA $CFFF ; RTS`.
- Table decode from `CD:16B5` proves this is auxiliary token `0xE6`.
- Strongest safe reading: direct stream-write token for the D1 suspend/restore mode byte.

### C1:58DB..C1:58E3  ct_c1_primary_slot_vm_force_cfff_nonzero_and_return_success   [strong]
- Exact body: `LDA #$01 ; STA $CFFF ; JMP $75BB`.
- Strongest safe reading: primary-script convenience helper that forces the D1 gate into nonzero/suspend mode.

### C1:58E4..C1:58EB  ct_c1_primary_slot_vm_clear_cfff_and_return_success   [strong]
- Exact body: `STZ $CFFF ; LDA #$01 ; JMP $75BB`.
- Strongest safe reading: primary-script convenience helper that forces the D1 gate into zero/restore mode.

### D1:F260..D1:F297  ct_d1_reset_control_cluster_state_including_ce0f_ce12_and_cfff   [strong structural]
- Exact writes in this subsection clear `CE0E / CE0F / CE10 / CE12 / CFFF` and seed neighboring D1 control bytes.
- Strongest safe reading: local reset/init subsection for the D1 palette/control cluster.

---

## Strengthened RAM/state labels

### 7E:CFFF  ct_d1_palette_descriptor_suspend_restore_mode_byte   [strong structural]
- Local D1 consumer at `D1:F426` tests only zero vs nonzero.
- `00` selects the restore path at `D1:F457`.
- Any nonzero value selects the suspend path at `D1:F431`.
- Written directly by auxiliary token `0xE6` at `CD:18C2`.
- Also forced to `1` or `0` by primary-slot helpers at `C1:58DB` and `C1:58E4`.
- Cleared by the D1 reset subsection at `D1:F295`.
- Strongest safe reading: externally writable zero/nonzero mode byte for the D1 descriptor-header suspend/restore gate.

### 7E:CDC8  ct_d1_palette_seed_vs_promote_phase_byte   [stronger support]
- `D1:E984` increments it during the seed/snapshot half.
- `D1:E97D` clears it during the promote/restore half.
- No exact external reader is frozen yet.
- Strongest safe reading: local phase-side byte for the `E984 <-> E91A` first-band seed/promote cycle.

### 7E:CE0F  ct_d1_palette_seed_side_arm_or_epoch_byte   [stronger support]
- `D1:E987` increments it during the seed/snapshot half.
- `D1:F26E` clears it in the D1 reset subsection.
- No exact reader is frozen yet.
- Strongest safe reading: seed-side arm/epoch byte in the same D1 control cluster.

### 7E:CE12  ct_d1_palette_suspend_restore_gate_latch_or_pending_count   [stronger local reset support]
- Pass 83 already proved the local one-shot gate behavior at `D1:F431 / F457`.
- Pass 84 adds explicit reset proof: `D1:F277` clears it in the D1 reset subsection.
- Strongest safe reading remains: local suspend/restore gate latch with wider pending-count caution still allowed outside the local pair.

---

## Honest caution
Even after this pass:

- I have **not** proven that nonzero `CFFF` values carry distinct live meanings beyond the local zero/nonzero branch.
- I have **not** frozen the final gameplay-facing noun of the `2040/20A0/2120/21A0/2240/22A0/2320/23A0` palette-band families.
- I have **not** frozen the exact external reader(s) of `CDC8` or `CE0F`.
- I have **not** yet explained why the suspend path clears positive `0x1x` descriptor headers while sparing the signed `0x8x` family.
