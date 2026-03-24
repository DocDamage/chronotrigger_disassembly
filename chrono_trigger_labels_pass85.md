# Chrono Trigger Labels — Pass 85

## Purpose
This file records the label upgrades justified by pass 85.

Pass 84 froze the `CFFF` writer at auxiliary token `0xE6`,
but the neighboring late auxiliary tail at `0xE0..0xE8` was still only partly mapped.

Pass 85 closes most of that tail as exact handlers:

- `0xE8`, `0xE7`, and `0xE0` are now exact wrappers into D1
- `0xE5` is an exact indexed increment helper over `5D80 + index`
- `0xE4` is an exact immediate stage + `5DA0`-index snapshot helper
- `0xE3` is an exact indexed six-byte snapshot/copy helper from `5DA0..5DA5` into `CAEA..CAF5`
- `0xE2` and `0xE1` are exact immediate writes to `CD2E` and `CD2D`

I am still keeping the final gameplay-facing nouns of the `5D80`, `5DA0..5DA5`, and `CAEA..CAF5` families one notch below frozen.

---

## Strengthened helper labels

### CD:1874..CD:1878  ct_cd_auxiliary_token_e8_call_d1_fb72   [strong]
- Exact body: `JSL D1:FB72 ; RTS`.
- Strongest safe reading: wrapper token into the D1-side helper at `FB72`.

### CD:1879..CD:187D  ct_cd_auxiliary_token_e7_call_d1_fb68   [strong]
- Exact body: `JSL D1:FB68 ; RTS`.
- Strongest safe reading: wrapper token into the D1-side helper at `FB68`.

### CD:18C8..CD:18CE  ct_cd_auxiliary_token_e5_increment_indexed_5d80_byte   [strong structural]
- Exact body: `LDA [$40] ; TAX ; INC $5D80,X ; RTS`.
- Strongest safe reading: indexed byte-strip increment helper over the `5D80` family.

### CD:18CF..CD:18DE  ct_cd_auxiliary_token_e4_store_immediate_to_cd24_snapshot_5da0_index_to_cd25_and_increment_cd23   [strong structural]
- Exact body stores one immediate byte to `CD24`, copies current `5DA0` into `X` and `CD25`, then increments `CD23`.
- Strongest safe reading: local immediate-stage plus current-index snapshot/count helper.

### CD:18DF..CD:1906  ct_cd_auxiliary_token_e3_copy_current_5da0_5da5_sixbyte_vector_into_indexed_caea_record   [strong structural]
- Exact body copies `5DA0/5DA2/5DA4/5DA1/5DA3/5DA5` into `CAEA/CAEE/CAF2/CAEC/CAF0/CAF4` using the immediate byte as X index.
- Strongest safe reading: indexed six-byte snapshot/copy helper from the current live `5DA0..5DA5` vector family.

### CD:1907..CD:190C  ct_cd_auxiliary_token_e2_store_immediate_to_cd2e   [strong]
- Exact body: `LDA [$40] ; STA $CD2E ; RTS`.
- Strongest safe reading: direct immediate store token for `CD2E`.

### CD:190D..CD:1912  ct_cd_auxiliary_token_e1_store_immediate_to_cd2d   [strong]
- Exact body: `LDA [$40] ; STA $CD2D ; RTS`.
- Strongest safe reading: direct immediate store token for `CD2D`.

### CD:1913..CD:1917  ct_cd_auxiliary_token_e0_call_d1_f47c   [strong]
- Exact body: `JSL D1:F47C ; RTS`.
- Strongest safe reading: wrapper token into the D1-side helper at `F47C`.

---

## Strengthened RAM/state labels

### 7E:CD23  ct_cd_auxiliary_5da0_snapshot_stage_count_byte   [stronger structural]
- Incremented by auxiliary token `0xE4` after mirroring the current `5DA0` byte into `CD25`.
- Strongest safe reading: local count/state byte for the `E4` snapshot-stage helper family.

### 7E:CD24  ct_cd_auxiliary_immediate_stage_selector_byte   [stronger structural]
- Written directly by auxiliary token `0xE4` from the following stream byte.
- Strongest safe reading: local immediate selector/control byte for the same snapshot-stage helper family.

### 7E:CD25  ct_cd_auxiliary_snapshot_of_current_5da0_index_byte   [stronger structural]
- Written by auxiliary token `0xE4` from the current live byte at `5DA0`.
- Strongest safe reading: mirrored current-index byte for the same local stage family.

### 7E:CD2D  ct_cd_auxiliary_immediate_control_byte_e1   [stronger structural]
- Written directly by auxiliary token `0xE1` from the stream.
- Final higher-level noun remains open.

### 7E:CD2E  ct_cd_auxiliary_immediate_control_byte_e2   [stronger structural]
- Written directly by auxiliary token `0xE2` from the stream.
- Final higher-level noun remains open.

### 7E:CAEA..7E:CAF5  ct_cd_auxiliary_indexed_sixbyte_snapshot_records_from_5da0_vector   [strong structural]
- Auxiliary token `0xE3` copies the current `5DA0..5DA5` six-byte live vector into one indexed destination record rooted here.
- Exact write pattern is interleaved: `CAEA/CAEC/CAEE/CAF0/CAF2/CAF4`.
- Strongest safe reading: indexed destination record family for six-byte snapshots of the current `5DA0` live vector.

### 7E:5D80..7E:5DFF  ct_cd_auxiliary_indexed_byte_counter_strip   [provisional strengthened]
- Auxiliary token `0xE5` increments one byte in this strip using the immediate operand as index.
- Final gameplay-facing noun remains open, but this is clearly an indexed byte strip actively mutated by the auxiliary VM.

### 7E:5DA0..7E:5DA5  ct_cd_auxiliary_current_sixbyte_live_vector   [strong structural]
- Auxiliary token `0xE3` snapshots these six live bytes outward into the indexed `CAEA..CAF5` record family.
- Auxiliary token `0xE4` reads `5DA0` specifically as the current index/selector byte mirrored into `CD25`.
- Strongest safe reading: current six-byte live vector family consumed by the late auxiliary token cluster.

---

## Honest caution
Even after this pass:

- I have **not** frozen the final gameplay-facing noun of the `5D80` strip.
- I have **not** frozen the final noun of the `5DA0..5DA5` live vector family.
- I have **not** frozen the final noun of the indexed destination record family at `CAEA..CAF5`.
- I have **not** yet tied this `0xE0..0xE8` control family all the way into the final presentation/system noun.
- I have **not** yet frozen the first exact external reader(s) of `CDC8` and `CE0F`.
