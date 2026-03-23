# Chrono Trigger Labels — Pass 64

## Purpose
This file records the label upgrades and corrections justified by pass 64.

The biggest result is that `AE21` is no longer a vague helper.
It is the reducer that collapses marked selected entries down to one chosen entry or raises `AF24`.

That forces a cleanup in how the surrounding early global opcodes are named.

---

## Strong labels

### C1:AE21..C1:AE6F  ct_reduce_marked_selected_entries_to_single_choice_or_fail   [strong structural]
- Empty input selection increments `AF24` and returns.
- Requires a bit-7-marked chosen entry to succeed.
- On success:
  - strips bit 7
  - writes the chosen entry into `AECC[0]`
  - writes `AECB = 1`
- On failure increments `AF24`.
- Multi-entry path uses a low-nibble comparison against the `C1:B163` byte stream before accepting a marked entry.
- Exact higher-level ranking noun is still open, but the reducer contract itself is now strong.

### C1:90BE..C1:912F  ct_global_opcode_08_mark_selected_entries_by_fd_record_word3_le_immediate_then_reduce   [strong structural]
- Calls `AC14`.
- Empty selection -> failure.
- Reads a 16-bit immediate threshold.
- For each selected entry:
  - resolves the `FD:A80B` record base
  - reads the 16-bit field at record offset `+3`
  - marks the entry in `AECC` with bit 7 when `record_word_+3 <= immediate_word`
- Stores the number of marked entries in `AECB`.
- Then calls `AE21`, `AEFD`, and `8C3E` on success.

### C1:918E..C1:91F8  ct_global_opcode_0A_gate_tail_replay_on_priority_selected_entry_record_mask_clear   [strong structural]
- Calls `AC14`.
- Empty selection -> failure.
- If only one entry is selected, uses it directly.
- If multiple entries are selected, reduces them to one chosen entry using WRAM vector `B23A[0..7]`.
- Operand `+1` is a record-byte offset.
- Operand `+2` is an immediate mask.
- Succeeds only when the chosen entry's `FD:A80B` record byte at that offset has no overlapping bits with the mask.
- Success goes directly to `8C3E`.
- Failure sets `AF24 = 1`.

---

## Provisional structural labels

### C1:9130..C1:918D  ct_global_opcode_09_scan_selected_entries_for_fd_record_byte_offset_gte_immediate_then_reduce   [provisional structural]
- Calls `AC14`.
- Empty selection -> failure.
- Operand `+1` is a byte offset inside the `FD:A80B` record.
- Operand `+2` is the compare byte.
- Scans the selected entries and breaks to `AE21` on the first entry where:
  - `record_byte >= immediate`
- Fails if the scan completes with no hit.
- This body does **not** mark `AECC` entries itself before calling `AE21`, so the precise final selected-entry effect should remain open.

### C1:91F9..C1:925C  ct_global_opcode_0B_scan_selected_entries_for_fd_record_byte_offset_lte_immediate_then_reduce   [provisional structural]
- Calls `AC14`.
- Empty selection -> failure.
- Operand `+1` is a byte offset inside the `FD:A80B` record.
- Operand `+2` is the compare byte.
- Scans the selected entries and breaks to `AE21` on the first entry where:
  - `record_byte <= immediate`
- Fails if the scan completes with no hit.
- Like opcode `09`, this body does not mark `AECC` entries itself before `AE21`.

---

## Important corrections

### retire the old “generic finalize helper” wording for `AE21`
Keep the stronger wording instead:

> **reduce marked selected entries to one chosen entry or fail**

### retire the old “increments selected entries in place” wording for the OR-`0x80` writes
Those writes are candidate-mark operations for `AE21`, not arithmetic increments.

This correction directly sharpens the already-solved caller family:
- opcode `01`
- opcode `02`
- opcode `03`
- opcode `08`

---

## Carry-forward family cleanup

### marked-candidate reducer family
These now belong together:

- `01`
- `02`
- `03`
- `08`

They:
- start from `AC14`
- mark candidate entries with bit 7
- call `AE21`
- continue through `AEFD` and `8C3E` if `AF24 == 0`

### direct chosen-entry gate
Opcode `0A` is not part of that family.
It reduces to one chosen entry itself and then performs a direct bit-clear replay gate.

### scan-into-reducer wrappers
Opcodes `09` and `0B` are adjacent but slightly different:
- they scan selected entries for a compare hit
- they hand off to `AE21`
- but they do not themselves mark `AECC` entries in the visible body

That distinction should be preserved until a later pass fully resolves their incoming mark-state assumptions.
