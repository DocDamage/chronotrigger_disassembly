# Chrono Trigger Labels — Pass 103

## Purpose
This file records the label upgrades justified by pass 103.

Pass 102 froze the late CD-side tail driver at `CD:8978..89CB`, but the owner block that seeds `CE13 = 0x03` and `CE0E = 0x80` was still too vague.

Pass 103 closes that owner-side seam and turns `CD:0D62..0E22` into exact blocking helper structure instead of “mystery setup around the D1 call.”

---

## Strong labels

### CD:0D62..CD:0D92  ct_cd_submit_exact_c7_sound_packets_80_ff_and_10_3a_then_reinit_auxiliary_stage_by_x_selector_and_mark_active   [strong structural]
- Exact body is now frozen:
  - `PHX`
  - submit exact packet `{ 80, 00, FF }` through `1E00..1E02` and `JSL C7:0004`
  - `JSR CD:3E7D`
  - submit exact packet `{ 10, 3A }` through `1E00..1E01` and `JSL C7:0004`
  - `PLX`
  - `JSR CD:0EBD`
  - `STZ $5D9B`
  - `JSR CD:0D33`
  - `INC $5D9B`
  - `RTS`
- Strongest safe reading: exact restart/reinit helper that submits two fixed low-bank sound/APU packets, reinitializes the auxiliary stage from the caller-supplied selector in `X`, rebuilds the descriptor work tables, and leaves the stage active.

### CD:0D93..CD:0DB0  ct_cd_clear_99d2_wait_for_apu_port_2141_idle_then_run_selector_87_auxiliary_stage_until_5d9b_clears   [strong structural]
- Exact body is now frozen:
  - `STZ $99D2`
  - loop: `JSR CD:039E ; JSR CD:3E7D ; LDA.l $002141 ; BNE loop`
  - `LDX #$0087 ; JSR CD:0D62`
  - loop: `JSR CD:3E7D ; LDA $5D9B ; BNE loop`
  - `RTS`
- Strongest safe reading: exact blocking owner helper that waits for the sound/APU side to go idle, launches auxiliary-stage selector `0x87`, then waits until the stage active flag clears.

### CD:0DB1..CD:0DD7  ct_cd_wait_for_apu_port_2141_idle_seed_ce13_03_and_ce0e_80_drain_owner_quiescence_delay_80_ticks_then_start_selector_84_auxiliary_stage   [strong structural]
- Exact linear flow is now frozen:
  - loop: `JSR CD:039E ; JSR CD:3E7D ; LDA.l $002141 ; BNE loop`
  - `LDA #$03 ; STA $CE13`
  - `LDA #$80 ; STA $CE0E`
  - `JSR CD:0DD8`
  - exact `0x80`-iteration delay loop over `JSR CD:3E7D`
  - `LDX #$0084 ; JSR CD:0D62`
  - falls directly into the shared blocking helper at `CD:0DD8`
- This is the pass that finally ties the earlier `CE13` and `CE0E` writes to a real local owner block instead of leaving them as isolated write sites.
- Strongest safe reading: exact owner-side transition helper that first forces the CD/D1 control bytes into a known masked signed-target state, drains current work to quiescence, burns a fixed delay, then launches auxiliary-stage selector `0x84` and continues blocking through the shared drain loop.

### CD:0DD8..CD:0DFF  ct_cd_service_cd04aa_until_ce0b_is_below_02_and_ce0a_ccea_a013_5d9b_are_all_zero   [strong structural]
- Exact body is now frozen:
  - `JSR CD:3E7D`
  - `JSR CD:3E7D`
  - `JSL CD:04AA`
  - `LDA $CE0B ; CMP #$02 ; BCS repeat`
  - `LDA $CE0A ; ORA $CCEA ; ORA $A013 ; ORA $5D9B ; BNE repeat`
  - `RTS`
- Strongest safe reading: exact blocking drain/quiescence loop for this owner chain. It keeps servicing `CD:04AA` until the D1-side target byte drops below `0x02` and all four local busy/progress bytes are clear.

### CD:0DFA..CD:0E04  ct_cd_wait_until_5d9b_clears_via_cd_3e75   [strong]
- Exact body: `LDA $5D9B ; BEQ done ; JSR CD:3E75 ; BRA repeat ; RTS`.
- Strongest safe reading: tiny busy-wait helper for the auxiliary-stage active flag.

### CD:0E05..CD:0E22  ct_cd_blocking_run_auxiliary_stage_by_a_selector_until_5d9b_clears   [strong structural]
- Exact body is now frozen:
  - `PHA ; JSR CD:0DFA ; PLA ; TAX`
  - `JSR CD:0EBD ; JSR CD:0D33 ; INC $5D9B`
  - loop while `5D9B != 0`: `JSR CD:3E75 ; JSL CD:04AA`
  - `RTL`
- This is the exact blocking sibling of the already-frozen nonblocking coordinator at `CD:0D28`.
- Strongest safe reading: run one auxiliary-stage selector to completion, blocking until the stage active flag clears.

### 7E:5D9B  ct_cd_optional_auxiliary_descriptor_stage_active_flag   [stronger structural]
- Earlier passes already froze it as the stage active flag.
- Pass 103 materially tightens the contract:
  - `CD:0D62` clears it before `0D33`, then increments it to mark the newly rebuilt stage active
  - `CD:0D93`, `CD:0DFA`, and `CD:0E05` busy-wait on it directly
  - `CD:0DD8` ORs it into the owner-side quiescence test before returning
- Strongest safe reading remains: stage active flag for the optional auxiliary descriptor stage, now with exact blocking-owner usage frozen.

### 7E:CCEA  ct_cd_optional_auxiliary_descriptor_stage_progress_byte   [stronger structural]
- Earlier passes only knew this byte blocked certain progression paths.
- Pass 103 adds a clean owner-side consumer:
  - `CD:0DD8` refuses to return while `CCEA != 0`
- Strongest safe reading now: stage progress/busy byte that must be clear before the owner-side blocking helper considers the local auxiliary path quiescent.

### 7E:CE0E  ct_cd_d1_signed_profile_target_selector_byte   [stronger structural]
- Earlier passes froze the D1-side consumption and the direct token `0xF7` writer.
- Pass 103 adds the exact owner-side write:
  - `CD:0DC2..0DC6` seeds `CE0E = 0x80` immediately before the shared blocking drain helper at `CD:0DD8`
- Strongest safe reading now: signed D1 profile-target selector byte that is written both by the old token path and by the clean CD-side owner block before a blocking transition/drain.

---

## What this pass settles about the old seam
- `CE13 = 0x03` is not a stray write anymore; it is part of a real owner-side blocking transition helper.
- `CE0E = 0x80` is not just a token-era staging path anymore; the clean CD owner block seeds it deliberately before draining quiescence.
- the exact `CE0A | CCEA | A013 | 5D9B` loop at `CD:0DD8` is now frozen as the owner-side drain condition that must clear before this helper returns.
- `CD:8978` and `CD:0DB1` now read as two sides of the same local control neighborhood:
  - `CD:0DB1` seeds and blocks on the owner-side state
  - `CD:8978` later consumes that same neighborhood in the staged tail driver

---

## Honest caution
Even after this pass:

- I have **not** frozen the final higher-level noun of `CD:039E`, `CD:04AA`, `CD:3E75`, or `CD:3E7D`.
- I have **not** frozen the final gameplay-facing noun of `A013`.
- I have **not** frozen the exact higher-level noun of the `2A21 / 7F:01EC` chooser block that decides between `CD:0D93` and `CD:0DB1`.
- I have **not** frozen a clean direct static reader of `CE0F`.
