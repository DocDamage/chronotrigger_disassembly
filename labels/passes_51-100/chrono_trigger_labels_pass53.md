# Chrono Trigger Disassembly Labels — Pass 53

This file contains labels newly added, replaced, or materially strengthened in pass 53.

As in prior passes:
- **strong** = directly supported by control flow and data role in the ROM work of this pass
- **strengthened** = previously useful label materially tightened by new proof
- **provisional** = structurally useful but still not safe as a final frozen name

---

## Strong labels

### 7E:B158..7E:B162  ct_battle_slot_readiness_seed_array                         [strong]
- Contiguous 11-byte readiness/base array.
- Proven by the 11-entry bulk writer at `FD:B4E0..B54D`.
- Head partition = `B158..B15A`.
- Tail partition = `B15B..B162`.

### 7E:AFAB..7E:AFB5  ct_battle_slot_readiness_work_array                         [strong]
- Contiguous 11-byte readiness/work array.
- Hard-proved by the init block at `C1:80FD..811D`:
  - `AFAB..AFAD = 01`
  - `AFAE..AFB5 = FF`
- Head partition is directly exported to visible gauge buffers at `FD:B93B..B94F`.

### 7E:B03A..7E:B044  ct_battle_slot_readiness_dirty_array                        [strong]
- Contiguous 11-byte readiness update/valid array.
- Head seeder writes the first 3 entries through `B03A,X`.
- Tail seeder writes the later entries through `B03D,X = B03A + 3 + X`.

### FD:B800..FD:B94F  ct_fd_seed_battle_slot_readiness_head_and_tail_partitions   [strong]
- Unified seed routine for the contiguous readiness arrays.
- Fixed head loop seeds slots `0..2`.
- Tail loop seeds the later runtime-slot partition starting at slot `3`.
- Ends by exporting only head work values (`AFAB..AFAD`) to the visible buffers.

---

## Strengthened labels

### 7E:B158..7E:B15A  ct_visible_head_lane_readiness_seed_array                   [strengthened]
- Previously treated as a standalone “primary pair”.
- This pass proves it is the fixed 3-entry head partition of the larger 11-slot seed array.
- These are the entries directly tied to the visible export path.

### 7E:AFAB..7E:AFAD  ct_visible_head_lane_readiness_work_array                   [strengthened]
- Head partition of `AFAB..AFB5`.
- Directly copied to:
  - `99DD..99DF`
  - `9F22..9F24`
- Strongest safe reading: the visible panel/gauge-facing work values.

### 7E:B03A..7E:B03C  ct_visible_head_lane_readiness_dirty_array                  [strengthened]
- Head partition of the contiguous readiness dirty/update array.
- Asserted directly by the head seeder.

### 7E:B15B..7E:B162  ct_runtime_tail_slot_readiness_seed_array                   [strengthened]
- Previously labeled as a separate “sibling” seed pair.
- This pass proves it is the tail partition of the same contiguous seed array rooted at `B158`.
- Seeded by the same config/speed formula as the head partition.

### 7E:AFAE..7E:AFB5  ct_runtime_tail_slot_readiness_work_array                   [strengthened]
- Tail partition of the contiguous work array rooted at `AFAB`.
- Initialized to `FF` in the startup block.
- Participates in the selector/materializer logic from `C1:9E78`.

### 7E:B03D..7E:B044  ct_runtime_tail_slot_readiness_dirty_array                  [strengthened]
- Tail partition of the contiguous readiness dirty array rooted at `B03A`.
- Set by the tail seeder only under the extra `AF02 != FF` gate.

### 7E:AEC6  ct_runtime_tail_slot_count                                           [strengthened]
- Used as the bound for the tail seeder loop in `FD:B867..B8EC`.
- Best current reading: live/populated tail-slot count rather than total capacity.

---

## Provisional labels

### FD:A811  ct_fd_runtime_tail_slot_record_ptr_table                             [provisional]
- Indexed by the tail seeder through a 16-bit table lookup.
- Supplies the record source used to read at least:
  - byte `+0x38` (effective speed in pass 52)
  - byte `+0x0A` (source of the tail-only `AF15.bit6` side effect)
- Exact record family name still wants one more pass.

### 7E:AF15 bit 6  ct_runtime_tail_slot_seed_side_effect_flag                     [provisional]
- Set only by the tail seeder when source record byte `+0x0A` has bit 0 set.
- Real and structurally isolated, but final gameplay-facing meaning is still unresolved.

### FD:B8F5..FD:B93A  ct_fd_normalize_head_readiness_work_before_visible_export    [provisional]
- This is the shared normalization/pre-export tail before the copy into `99DD..99DF` and `9F22..9F24`.
- Clearly head-export facing.
- Exact minimum/subtractive semantics still deserve one dedicated pass before freezing the name harder.

---

## Replaced / retired wording

### `ct_fd_seed_primary_visible_lane_readiness_from_config_and_speed`             [soft-replaced]
- Too narrow after the head/tail partition proof.
- Replaced by:
  - `ct_fd_seed_battle_slot_readiness_head_and_tail_partitions`

### `ct_fd_seed_sibling_visible_lane_readiness_from_config_and_speed`             [retired]
- “sibling visible lane” is no longer the right model.
- Replaced by the tail-partition reading inside the unified array family.

### `ct_c1_primary_lane_readiness_seed_value` / `ct_c1_sibling_lane_readiness_seed_value` [soft-replaced]
- Useful stepping-stones, but too fragmented now.
- Replaced by the unified array labels plus head/tail partition labels.

### `ct_c1_primary_lane_readiness_work_value` / `ct_c1_sibling_lane_readiness_work_value` [soft-replaced]
- Same issue: too fragmented after the unified-array proof.

### `ct_c1_primary_visible_lane_readiness_seed_valid_flag` / `ct_c1_sibling_visible_lane_readiness_seed_valid_flag` [soft-replaced]
- Replaced by the unified dirty-array family plus head/tail partition labels.

---

## Exact structural model now safe to carry forward

Unified readiness families:

```text
seed/base  : B158..B162   (11 entries)
work/value : AFAB..AFB5   (11 entries)
dirty/flag : B03A..B044   (11 entries)
```

Partition split:

```text
head slots 0..2   -> visible head/panel-facing partition
tail slots 3..10  -> runtime tail partition
```

Hard proof points:
- `C1:80FD..811D` initializes the work array as `3 + 8`
- `FD:B4E0..B54D` bulk-writes the seed array across 11 entries
- `FD:B800..B8EC` seeds head then tail using the same config/speed formula family
- `FD:B93B..B94F` exports only the head work values to visible buffers

---

## Still intentionally unresolved

### Exact gameplay-facing identity of the tail partition                          [unresolved]
- It is clearly runtime-slot facing
- It is clearly not exported to the 3 visible panel lanes here
- Final freeze as enemy-side/materialized reserve/etc. wants one more pass

### Exact meaning of `AF15.bit6` in the tail seeder                              [unresolved]
- Real side effect
- Not yet safe to freeze

### Exact normalization semantics of `FD:B8F5..FD:B93A`                          [unresolved]
- Strongly looks like a pre-export normalization pass
- Still wants one clean dedicated decode pass
