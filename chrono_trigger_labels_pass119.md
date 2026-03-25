# Chrono Trigger Labels — Pass 119

## Purpose

Pass 119 fixes a real bank-ownership mistake around the settlement/search subsystem and closes the sibling bank-`C2` caller cluster rooted at `A1B2`, `A2CE`, and `A321`.

## Strong labels

### C2:8820..C2:991F  ct_c2_dp1d00_current_slot_candidate_offset_settlement_search_pipeline   [strong structural, bank correction]
- This is the exact settlement/search owner band previously carried forward with the wrong `C0:` bank prefix.
- Bank-local absolute `JSR $8820` callsites in bank `C2` target `C2:8820`, not `C0:8820`.
- Direct byte check confirms `C2:8820` and `C0:8820` are different routines.
- Strongest safe reading: exact DP=`$1D00` current-slot candidate-offset settlement/search pipeline in bank `C2`.

### C2:A1B2..C2:A1E8  ct_c2_full_span_linear_settlement_sweep_with_post_result_twin_tail_dispatch   [strong structural]
- Seeds `71 = 0413`, clears `72`, and seeds `61 = 2E00`.
- Repeatedly runs exact settlement/search service `C2:8820`.
- Uses exact post-settlement local byte `51` to choose:
  - `A1E9` when nonzero
  - `A216` when zero
- Advances:
  - `INC 71`
  - `61 += 0x0180`
- Exits when either:
  - `71 >= 85`
  - or `61 >= 3280`
- Strongest safe reading: exact full-span linear settlement sweep with twin post-result tail dispatch.

### C2:A1EF..C2:A215  ct_c2_selector_threshold_gate_for_post_settlement_tail_dispatch   [strong structural]
- Clears `0D5D`.
- Copies low three bits of `9A90` into `0D4D`.
- Doubles that selector and indexes exact compare table `0D38`.
- Compares table-derived word against `9A93`.
- When the table value is not below `9A93`:
  - forces `0D5D = 4`
  - sets bit `0x20` in `0D4D`
- Strongest safe reading: exact selector/threshold gate used by the post-settlement tail family.

### C2:A1E9..C2:A1EE  ct_c2_direct_post_settlement_tail_to_ed31_with_be15_selector   [strong]
- Exact body: `LDX #$BE15 ; JMP $ED31`
- Strongest safe reading: direct post-settlement tail into common service `ED31` with fixed selector `BE15`.

### C2:A216..C2:A21E  ct_c2_gated_post_settlement_tail_to_ed31_with_be0e_selector   [strong]
- Runs exact selector/threshold gate `A1EF`.
- Exact tail: `LDX #$BE0E ; JMP $ED31`
- Strongest safe reading: gated post-settlement tail into common service `ED31` with fixed selector `BE0E`.

### C2:A21F..C2:A22E  ct_c2_wrapper_chaining_one_shot_settlement_materializer_into_a216_tail   [strong structural]
- Runs exact one-shot settlement-driven materializer wrapper `A22F`.
- Resets `61 = 2E00`.
- Then runs exact gated post-settlement tail `A216`.
- Strongest safe reading: wrapper chaining the one-shot materializer into the `A216` tail.

### C2:A2CE..C2:A2EC  ct_c2_one_shot_settlement_tail_fanning_into_a6f0_and_ed31   [strong structural]
- Clears `0D22`.
- Seeds `54 = 0412`.
- Seeds `71 = 0412 + 0413`.
- Runs exact settlement/search service `C2:8820`.
- Runs `A6F0` with `X = 30A2`.
- Runs `ED31` with `X = BDEF`.
- Strongest safe reading: one-shot settlement tail feeding `A6F0` and `ED31`.

### C2:A2ED..C2:A320  ct_c2_static_block_seed_and_common_service_tail_after_a170   [strong structural]
- Runs front helper `A170`.
- Seeds:
  - `9694 = 969A`
  - `9696 = 9300`
  - `9698 = 0013`
- Seeds `5D42 = 61FF`.
- Uses overlapping `MVN` to propagate the fill across `5D42..5D58`.
- Runs exact helper `9E76`.
- Finishes through common service call `8385` with `X = FBE3`.
- Strongest safe reading: static block-seed and common-service tail after `A170`.

### C2:A321..C2:A38A  ct_c2_settlement_driven_quad_block_materializer_with_three_service_fanout   [strong structural]
- Runs `ED31` with `X = BE6D`.
- Seeds `71 = (0412 + 0413) & 00FF`.
- Runs exact settlement/search service `C2:8820`.
- Resets `61 = 2E00`.
- Runs exact gated post-settlement tail `A216`.
- Seeds `5CC2 = 40FF` and propagates that fill across `5CC2..5CD8` via overlapping `MVN`.
- Seeds:
  - `9694 = 969A`
  - `9696 = 9300`
  - `9698 = 0025`
- Clears `54`, then runs exact helper `A38B`.
- Updates:
  - `INC 0D15`
  - `DEC 0D9A`
  - `0D13 = C5`
- Fans out through exact service calls:
  - `8385` with `X = FBE3`
  - `8385` with `X = FBFF`
  - `8385` with `X = FC45`
- Strongest safe reading: settlement-driven quad-block materializer with three-service fanout.

### C2:A38B..C2:A3B8  ct_c2_selector_indexed_table_loader_and_3040_to_3840_block_copy_helper   [strong structural]
- Latches selector `54 -> 77`.
- Computes exact selector entry base `A3BA + 10*54`.
- Clears `7D`.
- Runs exact helper `EF65` with:
  - `X = 3086`
  - `A = C20A`
  - selector-derived `Y`
- Copies exact `0x80`-byte block from `3040` to `3840`.
- Strongest safe reading: selector-indexed table loader and `3040 -> 3840` block copy helper.

### C2:A3BA..C2:A3E1  ct_c2_four_entry_selector_table_for_a38b_block_loader   [strong]
- Exact table entry count = 4.
- Exact entry size = `0x0A` bytes.
- Selected by exact formula `A3BA + 10*54`.
- Strongest safe reading: four-entry selector table used by `A38B`.

### C2:A3E2..C2:A418  ct_c2_four_band_marker_writer_using_latched_selector_77   [strong structural]
- Starts with `61 = 3062`.
- Walks four exact `0x80`-spaced bands.
- Writes default word `1C0B` through `ECAC`.
- For the single selector-matched band (`02 == 77`) writes exact override word `000B`.
- Strongest safe reading: four-band marker writer keyed by latched selector `77`.

## Caution-strengthened outputs

### 7E:0D4D  ct_c2_selector_low3bits_and_post_threshold_flag_word_for_a1ef_tail_gate   [caution strengthened]
- Seeded from `9A90 & 0x0007`.
- `A1EF` sets bit `0x20` when selector-derived table value `0D38,X` is not below `9A93`.
- Strongest safe reading: selector low-bits plus post-threshold flag word for the `A1EF` gate.

### 7E:0D5D  ct_c2_post_threshold_result_word_for_a1ef_tail_gate   [caution strengthened]
- Cleared at the front of `A1EF`.
- Forced to `0004` when selector-derived compare table value is not below `9A93`.
- Strongest safe reading: post-threshold result word for the `A1EF` tail gate.

### 7E:0077  ct_c2_latched_selector_byte_for_a38b_a3ed_helper_cluster   [caution strengthened]
- `A38B` stores `54 -> 77`.
- `A3ED` reads `77` to choose which of four `0x80`-spaced bands gets override word `000B`.
- Strongest safe reading: latched selector byte shared by the `A38B/A3ED` helper cluster.

## Honest remaining gap

- The structural work from passes 115–118 survives, but the carry-forward bank prefix must now be read as `C2`, not `C0`.
- The old “outer-bank caller” seam suggested from raw absolute-xref output is no longer safe.
- The real next seam is still same-bank:
  - `C2:9DB9..9ED0`
  - `C2:A046..A0BA`
  - `C2:A886..`
  - `C2:B002`
  - `C2:BA32`
  - `C2:BEEF`
