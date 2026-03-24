# Chrono Trigger Labels — Pass 108

## Purpose
This file records the label upgrades justified by pass 108.

Pass 108 closes the paired-builder structure behind `FD:C2C1` far enough to prove that:
- the paired targets are true **double-buffer siblings** writing the same grammars into the two exact `7F` bundle spaces
- `0126` is the exact local **3-way builder-family selector**
- `0127` is the exact local **variable-template parameter byte** for families 1 and 2
- the six builder families themselves do **not** directly write `7E:0128`

---

## Strong labels

### FD:C2EB..FD:C3FF  ct_fd_build_first_7f_hdma_bundle_using_family0_fixed_template_for_0126_eq_0   [strong structural]
- Selected by `FD:C2C1` on the set-side table when `0126 = 0`.
- Writes the family-0 fixed template into the first-bundle WRAM slots rooted at:
  - `0F80`
  - `0FD7`
  - `1085`
  - `10DC`
  - `1133`
  - `118A`
- Its clear-side sibling at `FD:C847..C95B` writes the same grammar to the second-bundle slots at the exact `+0x2B8` offsets.
- Strongest safe reading: exact first-bundle family-0 fixed-template HDMA-table builder for local selector value `0126 = 0`.

### FD:C847..FD:C95B  ct_fd_build_second_7f_hdma_bundle_using_family0_fixed_template_for_0126_eq_0   [strong structural]
- Selected by `FD:C2C1` on the clear-side table when `0126 = 0`.
- Writes the family-0 fixed template into the second-bundle WRAM slots rooted at:
  - `1238`
  - `128F`
  - `133D`
  - `1394`
  - `13EB`
  - `1442`
- This is the exact second-bundle sibling of `FD:C2EB..C3FF`, with every corresponding root shifted by `0x2B8`.
- Strongest safe reading: exact second-bundle family-0 fixed-template HDMA-table builder for local selector value `0126 = 0`.

### FD:C995..FD:CC57  ct_fd_build_first_7f_hdma_bundle_using_family1_variable_chunked_template_from_0127_with_zero_fallback_to_family0   [strong structural]
- Selected by `FD:C2C1` on the set-side table when `0126 = 1`.
- Exact entry gate:
  - `LDA $0127`
  - if zero -> `BRL FD:C2EB`
  - if nonzero -> continue family-1 variable build
- Repeatedly uses exact arithmetic on `0127`, including:
  - `0x29 - 0127`
  - `2 * 0127`
  - `0x64 - 0127`
  - chunked count handling around `0x0A`
- Uses the `CC58/CC5E/CCB2` helper lane to emit variable HDMA entries into the first-bundle variable-table space.
- Strongest safe reading: exact first-bundle family-1 variable/chunked HDMA-table builder driven by `0127`, with zero falling back to family 0.

### FD:CD0C..FD:CFCE  ct_fd_build_second_7f_hdma_bundle_using_family1_variable_chunked_template_from_0127_with_zero_fallback_to_family0   [strong structural]
- Selected by `FD:C2C1` on the clear-side table when `0126 = 1`.
- Exact entry gate:
  - `LDA $0127`
  - if zero -> `BRL FD:C847`
  - if nonzero -> continue family-1 variable build
- This is the second-bundle sibling of `FD:C995..CC57` and writes the same grammar into the second-bundle space using the clear-side helper lane.
- Strongest safe reading: exact second-bundle family-1 variable/chunked HDMA-table builder driven by `0127`, with zero falling back to family 0.

### FD:CFCF..FD:D27C  ct_fd_build_first_7f_hdma_bundle_using_family2_alternate_variable_template_from_0127_with_zero_fallback_to_family0   [strong structural]
- Selected by `FD:C2C1` on the set-side table when `0126 = 2`.
- Exact entry gate:
  - `LDA $0127`
  - if zero -> `BRL FD:C2EB`
  - if nonzero -> continue family-2 variable build
- Repeatedly uses exact arithmetic on `0127`, including:
  - `0x29 - 0127 + 1`
  - `2 * 0127`
  - `0x29 - 0127 - 1`
  - fixed spans including `0x58`, `0x64`, and `0x1D`
- Strongest safe reading: exact first-bundle family-2 alternate variable HDMA-table builder driven by `0127`, with zero falling back to family 0.

### FD:D27E..FD:D52B  ct_fd_build_second_7f_hdma_bundle_using_family2_alternate_variable_template_from_0127_with_zero_fallback_to_family0   [strong structural]
- Selected by `FD:C2C1` on the clear-side table when `0126 = 2`.
- Exact entry gate:
  - `LDA $0127`
  - if zero -> `BRL FD:C847`
  - if nonzero -> continue family-2 variable build
- This is the exact second-bundle sibling of `FD:CFCF..D27C`, writing the same alternate variable grammar into the second-bundle space.
- Strongest safe reading: exact second-bundle family-2 alternate variable HDMA-table builder driven by `0127`, with zero falling back to family 0.

### FD:CC58..FD:CCB7  ct_fd_reset_local_variable_builder_offset_then_emit_chunked_first_bundle_hdma_table_entries   [strong structural]
- Exact init entry at `FD:CC58`:
  - `LDY #$0000`
  - `STY $EE`
  - `RTS`
- Main helper at `FD:CC5E..CCB1`:
  - takes a count in `A`
  - for counts below `0x10`, emits one 3-byte entry into the first-bundle variable table lane
  - for counts `>= 0x10`, emits `0x90` chunks until the remainder drops below `0x10`
  - uses pointer words derived from the first-bundle source lane rooted at `1D27`
- Exact helper at `FD:CCB2..CCB7`:
  - `CLC ; ADC $EE ; STA $EE ; RTS`
- Strongest safe reading: exact first-bundle variable-table helper lane that resets/advances the local builder offset and emits chunked HDMA entries.

### FD:CCB8..FD:CD0B  ct_fd_emit_chunked_second_bundle_hdma_table_entries_as_the_clear_side_sibling_of_cc5e   [strong structural]
- Performs the same chunked entry-emission grammar as `FD:CC5E..CCB1`, but writes into the second-bundle variable-table lane.
- Uses the clear-side sibling pointer base rooted at `1DA7`.
- Strongest safe reading: exact second-bundle sibling helper that emits chunked HDMA entries for the clear-side variable builders.

---

## Caution labels

### 7E:0127  ct_fd_local_variable_hdma_builder_parameter_byte_used_by_family1_and_family2_with_zero_fallback_to_family0   [caution]
- Exact local reader contracts now frozen:
  - `FD:C995` / `FD:CD0C` / `FD:CFCF` / `FD:D27E` all begin with `LDA $0127`
  - zero -> long-branch to the same-side family-0 fixed template
  - nonzero -> stay in the variable family and use `0127` repeatedly in exact arithmetic
- Exact local formulas now seen include:
  - `0x29 - 0127`
  - `2 * 0127`
  - `0x64 - 0127`
  - `0x29 - 0127 + 1`
  - `0x29 - 0127 - 1`
- Strongest safe reading: exact local parameter byte that shapes the nonzero variable HDMA-table grammars in builder families 1 and 2.
- Final broader subsystem noun remains intentionally cautious.

---

## What this pass settles
- The paired targets behind `FD:C2C1` are now proven as **true double-buffer siblings**, not alternate mode families.
- `0126` is now exact enough locally to treat as the 3-way builder-family selector for this HDMA table builder cluster.
- `0127` is no longer anonymous RAM in this pocket; it is the local nonzero parameter byte for the variable builders.
- The `CC58/CC5E/CCB2/CCB8` helper lane is no longer fuzzy; it emits chunked HDMA table entries.
- The direct `7E:0128` producer question is now closed **negatively** for this builder cluster.

---

## Honest caution
- I have **not** yet frozen the broader gameplay/UI noun of `0127`.
- I have **not** yet frozen the broader role of `1DF9`, `1DFD`, or the source-pointer lanes rooted at `1D27` / `1DA7`.
- I have **not** yet closed the true low-bank owner/update lane that finally sets the direct `7E:0128` shadow value.
