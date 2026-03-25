# Chrono Trigger Labels — Pass 111

## Purpose
Pass 111 closes two upstream seams left by pass 110:

1. the exact producer of the `7E:05B0..05EB` descriptor workspace and the `7F:0400/0410` helper tables
2. the exact role of the optional `C0:F05E` prelude relative to local state byte `63`

---

## Strong labels

### FD:FFFA  ct_fd_bank_local_jump_veneer_to_de98_descriptor_and_helper_table_builder   [strong structural]
- Exact body: `JMP $DE98`
- Strongest safe reading: bank-local veneer used to enter the compact descriptor/helper-table builder behind the startup chain.

### FD:DE98..FD:E01D  ct_fd_build_twelve_5byte_vram_dma_descriptor_lanes_and_7f0400_0410_helper_tables_from_compact_script   [strong structural]
- Exact setup:
  - saves `P/D/B`
  - forces `DB = 0`
  - sets `D = 0x0500`
  - loads selector from `7E:01FE`
  - reads compact selector byte `F6:0001,X`
  - masks with `0x3F`, doubles, and indexes exact pointer table `FD:F290`
  - loads compact stream pointer from `FD:F290`
  - seeds WRAM-port target at `7F:0400`
  - seeds exact local loop count `7E:0518 = 0x000C`
- Exact output contract:
  - fills 12 exact 5-byte lanes covering `7E:05B0..05EB`
  - advances `Y += 5` per lane
- Exact compact-byte paths:
  - `0x80` -> writes `0x80` to `05B3,Y` as the negative/sentinel skip marker
  - other types first store compact bytes into `05B0,Y`, `05B2,Y`, `05B3,Y`, and constant bank `0x7F` into `05B4,Y`
  - `type 0x02` -> zeroes `05B0/05B1` and materializes helper bytes into `7F:0400` and `7F:0410`
  - `type 0x04` -> same basic lane zeroing, but uses the longer 8-step helper-table materializer
  - fallback other type -> same lane zeroing with the third helper-table packing grammar
- Strongest safe reading: exact builder for the descriptor lanes and helper tables later consumed by `FD:E022`.

### C0:F05E..C0:F16F  ct_c0_local_63_driven_four_band_immediate_vram_prelude_with_special_28fc_28ff_override_set   [strong structural]
- Exact setup:
  - saves `D`
  - sets `D = 0x2100`
  - writes `$2115 = 0x80`
  - reads local selector byte `7E:0163`
- Exact selector values:
  - `63 == 0`
  - `63 == 1`
  - `63 == 2`
  - `63 == 3`
  - default / other nonnegative values
- Exact fixed helper leaves:
  - `F159` writes default pairs at `1C02` and `1C22`
  - `F142` writes default pairs at `1C42` and `1C62`
  - `F12B` writes default pairs at `1C82` and `1CA2`
  - `F110` writes default pairs at `1CC2` and `1CE2`
- Exact selector actions:
  - `0` -> run `F142/F12B/F110`, then overwrite `1C02/1C22` with `28FC/28FD` and `28FE/28FF`
  - `1` -> run `F159/F12B/F110`, then overwrite `1C42/1C62` with `28FC/28FD` and `28FE/28FF`
  - `2` -> run `F159/F142/F110`, then overwrite `1C82/1CA2` with `28FC/28FD` and `28FE/28FF`
  - `3` -> run `F159/F142/F12B`, then overwrite `1CC2/1CE2` with `28FC/28FD` and `28FE/28FF`
  - default/non-`0..3` -> run all four default helper leaves, then force `63 = 0x80`
- Strongest safe reading: exact 4-way band selector plus default-restore prelude for this immediate-VRAM band family.

---

## Strengthened local/state labels

### 7E:0518  ct_fd_local_twelve_lane_descriptor_build_countdown_in_de98   [caution]
- Exact local proof:
  - `DE98` seeds `0518 = 0x000C`
  - decrements it once per 5-byte lane
  - exits when it reaches zero
- Strongest safe reading: local countdown for the 12-lane descriptor/helper-table builder.
- Broader subsystem ownership remains open.

### 7E:0163  ct_c0_local_four_band_vram_prelude_selector_and_default_restore_state_byte   [caution strengthened]
- Exact local proof from pass 111:
  - negative -> caller `ED15` skips `F05E`
  - `0..3` -> choose one of four exact band overrides
  - other nonnegative -> default-restore path writes all four normal bands and forces `63 = 0x80`
- Strongest safe reading: local selector/state byte for the `F05E` prelude.
- Broader writer/owner chain remains open.

### 7F:0400..7F:041F  ct_fd_helper_tables_materialized_by_de98_and_consumed_by_e022   [provisional strengthened]
- Pass 110 proved `E022` consumes exact helper tables at `7F:0400` and `7F:0410`.
- Pass 111 proves `DE98` is the materializer that writes those helper tables through the WRAM port.
- Strongest safe reading: helper-table materialization area for the FD-side VRAM DMA descriptor system.

---

## Important negative closure
- `FD:E022` no longer stands alone as an isolated streamer; its upstream builder is now exact.
- `C0:F05E` is not just a generic “do some pre-display work” helper.
- Local state byte `63` is not merely a boolean gate; it is an exact selector over four fixed VRAM bands plus one default-restore state.

---

## Best next seam
- trace the real writers of `7E:0163`
- identify the broader subsystem noun for the `1C02..1CE2` / `29xx` / `28FC..28FF` VRAM band family
- widen owner tracing around `FD:DE98` only if fresh callers beyond `C0:0112` turn up
