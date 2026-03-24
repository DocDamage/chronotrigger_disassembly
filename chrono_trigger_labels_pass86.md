# Chrono Trigger Labels — Pass 86

## Purpose
This file records the label upgrades justified by pass 86.

Pass 85 left `5DA0..5DA5` and `CAEA..CAF5` one notch too generic,
and it still lacked the first exact external reader of `CDC8`.

Pass 86 tightens both seams:

- `CE:E18E..E1A4` is now the first exact external reader of `CDC8`
- `CDC8` now has exact nonzero-gated clear behavior over `CD47..CDC6`
- `D1:F5CD..F5F2` is an exact D1-side snapshot helper for the `5DA0 -> CAEA` family
- `D1:EC27..EC5B` and `D1:EDCD..EE95` prove that `5DA0 / 5DA1` behave like a coordinate-style axis pair
- `5DA0..5DA5` can now be tightened from a generic six-byte vector to a stronger **current three-pair point bundle** noun

I am still keeping the final presentation/system noun one notch below frozen.

---

## Strong labels

### CE:E18E..CE:E1A4  ct_ce_clear_cd47_cdc6_work_strip_only_when_cdc8_nonzero   [strong structural]
- Exact body: `LDA $CDC8 ; BEQ return ; TDC ; TAX ; REP #$20 ; STZ $CD47,X ; INX ; INX ; CPX #$0080 ; BNE loop ; TDC ; SEP #$20 ; RTL`.
- Exact behavior: if `CDC8 == 0`, return immediately. If `CDC8 != 0`, clear the exact `0x80`-byte strip `CD47..CDC6`.
- Strongest safe reading: first exact external `CDC8` reader; nonzero-gated clear helper for one D1-adjacent work strip.

### D1:EC27..D1:EC5B  ct_d1_build_four_endpoint_pairs_from_mulhi_and_current_5da0_5da1_pair_then_call_f9af   [strong structural]
- Reads one immediate/index through `[$40]`, transforms the `4217` multiply-result high byte, builds four endpoint pairs in `CD0D..CD1B`, uses `5DA0` with `-0x10/+0x10`, uses `5DA1` as the paired byte for both records, then calls `D1:F9AF`.
- Strongest safe reading: D1 helper that converts the current `5DA0/5DA1` pair plus one transformed multiply-derived byte into four coordinate/endpoint pairs for downstream geometry-style processing.

### D1:EDCD..D1:EE95  ct_d1_expand_current_5da0_5da1_axis_pair_by_cd3a_cd3b_into_four_plane_span_strips   [strong structural]
- Selector `[$40] == 0` path uses `5DA0` and `CD3A`, clamps low/high bounds, and fills one of two four-plane strip families with the computed byte at stride 4.
- Selector `[$40] != 0` path uses `5DA1` and `CD3B`, clamps bounds, and clears one of two corresponding four-plane strip families across the computed span.
- Strongest safe reading: D1 axis-span helper consuming the current `5DA0/5DA1` pair as horizontal/vertical coordinates.

### D1:F5CD..D1:F5F2  ct_d1_snapshot_current_5da0_5da5_three_pair_bundle_into_indexed_caea_record   [strong structural]
- Exact body copies `5DA0/5DA2/5DA4/5DA1/5DA3/5DA5` into `CAEA/CAEE/CAF2/CAEC/CAF0/CAF4` using the immediate byte from `[$40]` as X index.
- Strongest safe reading: D1-side reusable snapshot helper for the current three-pair bundle into one indexed `CAEA..CAF5` record.

---

## Strengthened RAM/state labels

### 7E:CDC8  ct_d1_seed_side_nonzero_gate_for_cdc8_conditioned_work_strip_clear   [stronger structural]
- `D1:E984` increments it during the seed/snapshot half.
- `D1:E97D` clears it during the promote/restore half.
- `CE:E18E..E1A4` is the first exact external reader: nonzero gates clearing of `CD47..CDC6`; zero skips the clear entirely.
- Strongest safe reading: seed-side nonzero gate byte for at least one D1-adjacent work-strip clear path.

### 7E:CD47..7E:CDC6  ct_d1_cdc8_conditioned_0x80byte_work_strip   [strong structural]
- `CE:E18E..E1A4` clears this exact `0x80`-byte range only when `CDC8 != 0`.
- Final higher-level noun remains open, but the clear footprint is exact.

### 7E:5DA0..7E:5DA5  ct_cd_d1_current_three_pair_point_bundle   [strong structural]
- Pass 85 already proved exact snapshot order into `CAEA..CAF5`.
- `D1:EC27..EC5B` proves `5DA0/5DA1` behave as a paired coordinate-like byte pair.
- `D1:EDCD..EE95` proves the same pair drives expanding horizontal/vertical span helpers.
- Strongest safe reading: current three-pair point/coordinate bundle shared by the late auxiliary cluster and D1 helpers.

### 7E:CAEA..7E:CAF5  ct_cd_d1_indexed_snapshot_records_of_current_three_pair_point_bundle   [strong structural]
- Auxiliary token `0xE3` and D1 helper `F5CD..F5F2` both snapshot the current `5DA0..5DA5` bundle into one indexed record rooted here.
- Exact interleaved write pattern remains `CAEA/CAEC/CAEE/CAF0/CAF2/CAF4`.
- Strongest safe reading: indexed snapshot record family for the current three-pair point bundle.

---

## Alias / wrapper / caution labels

### 7E:CDC8  ct_d1_palette_seed_vs_promote_phase_byte   [alias / caution retained]
- Pass 84 already justified this local noun from `E984 <-> E91A`.
- Pass 86 does **not** invalidate that reading; it adds exact external clear-gate behavior.
- Keep both readings in play until a wider cluster noun is frozen.

---

## Honest caution
Even after this pass:

- I have **not** frozen the final gameplay-facing noun of the `5DA0..5DA5` bundle.
- I have **not** proven whether the three pairs are literal vertices, corners, or another nearby geometric/effect record.
- I have **not** frozen the first exact external reader of `CE0F`.
- I have **not** promoted `CD23 / CD24 / CD25` beyond their pass-85 local staging noun, because the remaining valid mapped hits are still not clean enough.
