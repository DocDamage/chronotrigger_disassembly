# Chrono Trigger Labels — Pass 105

## Purpose
This file records the label upgrades justified by pass 105.

Pass 104 froze the chooser/wrapper that installs `0501/0503 -> D1:F4C0`, but it intentionally stopped before freezing the full role of that installed target.

Pass 105 closes that seam and proves that `D1:F4C0` is the actual installed RAM NMI trampoline body, plus the exact local shadow-byte payloads it flushes.

---

## Strong labels

### D1:F4C0..D1:F55A  ct_d1_installed_ram_nmi_trampoline_body_acknowledge_rearm_interrupt_flush_inidisp_and_bg123_scroll_shadows_then_rti   [strong structural]
- Exact body is now frozen.
- Exact front edge:
  - save `A/X/Y/B/D`
  - set `D = 0`
  - `STA.l $420C` with exact zero
  - `LDA.l $4210`
  - `LDA #$A1 ; STA.l $4200`
  - `STZ $47`
- Exact flush tail:
  - `JSL CD:09CE`
  - `JSL C0:0005`
  - return value from `C0:0005` is written directly to `$420C`
  - `LDA.l $45 ; STA.l $2100`
  - `7E:2C70..2C7B` is flushed into `BG1/BG2/BG3` scroll registers `$210D..$2112`
  - `JSL CD:0C89`
  - `JSL FD:FFF7`
- Exact terminator is `RTI`.
- Strongest safe reading: exact installed RAM NMI trampoline body for this local wrapper contract.

### 00:0045  ct_d1_direct_page_inidisp_shadow_handoff_byte_consumed_by_installed_nmi_trampoline   [strong structural]
- Pass 104 froze the wrapper-side staging:
  - `CD:8423  LDA $BB00`
  - `CD:8426  STA $45`
- Pass 105 freezes the trampoline-side consumer:
  - `D1:F4E9  LDA.l $000045`
  - `D1:F4ED  STA.l $002100`
- Strongest safe reading: direct-page handoff byte consumed by the installed NMI trampoline as the exact source for `$2100`.

### 7E:BB00  ct_cd_staged_inidisp_shadow_source_byte_forwarded_through_dp45_into_ppu_2100   [stronger structural]
- Exact local path is now frozen:
  - `CD:8423  LDA $BB00`
  - `CD:8426  STA $45`
  - `D1:F4E9  LDA.l $45`
  - `D1:F4ED  STA.l $2100`
- Strongest safe reading: staged source byte for the exact `$2100` flush path in this launcher/trampoline chain.
- Final broader gameplay-facing noun remains intentionally cautious.

### 7E:2C70..7E:2C7B  ct_d1_bg1_bg2_bg3_scroll_shadow_byte_band_flushed_to_210d_2112_by_installed_nmi_trampoline   [strong structural]
- Exact write order is frozen:
  - `2C70,2C71 -> $210D,$210D`
  - `2C72,2C73 -> $210E,$210E`
  - `2C74,2C75 -> $210F,$210F`
  - `2C76,2C77 -> $2110,$2110`
  - `2C78,2C79 -> $2111,$2111`
  - `2C7A,2C7B -> $2112,$2112`
- Strongest safe reading: exact 12-byte WRAM shadow band for committed `BG1/BG2/BG3` horizontal/vertical scroll register writes.

### 00:0047  ct_cd_ram_trampoline_cycle_completion_latch   [strengthened]
- Pass 104 proved the waiter side:
  - `CD:044A` sets `$47 = 1` and waits until zero.
- Pass 105 proves the installed interrupt-body side completely:
  - `D1:F4DC  STZ $47`
  - and `D1:F4C0..F55A` is now proven to be the actual installed RAM NMI trampoline body because it ends with `RTI`
- Strongest safe reading: one-shot completion latch for one installed RAM NMI trampoline cycle.

### C0:0005..C0:0007  ct_c0_branch_long_to_0aff_lowbank_helper_returning_byte_consumed_as_420c_mask_by_d1_f4c0   [strong]
- Exact body is now frozen:
  - `BRL $0AF7`
  - lands at exact target `C0:0AFF`
- New exact caller proof from pass 105:
  - `D1:F4E2  JSL C0:0005`
  - `D1:F4E6  STA $420C`
- Strongest safe reading: veneer to the next exact seam, whose return byte is consumed directly as the installed NMI trampoline's `$420C` write value.

---

## What this pass settles
- `D1:F4C0` is no longer “the thing that clears `$47`.”
- It is the actual installed RAM **NMI trampoline body** for this wrapper path.
- `$45 -> $2100` is now exact enough to call a real `INIDISP` shadow flush path.
- `7E:2C70..2C7B` is now an exact BG1/BG2/BG3 scroll-shadow band, not anonymous WRAM.
- The next clean unresolved edge is the return value from `C0:0005 -> C0:0AFF`, because that byte is written directly into `$420C` by the installed trampoline.

---

## Honest caution
Even after this pass:

- I have **not** frozen the exact helper roles of `CD:09CE`, `CD:0C89`, or `FD:FFF7` inside the trampoline tail.
- I have **not** frozen the final broader subsystem noun of `BB00`; only its exact local hardware-facing role in this chain is now pinned.
- I have **not** frozen the exact value semantics returned by `C0:0005 -> C0:0AFF`; only the veneer and the direct `$420C` consumer are now exact.
