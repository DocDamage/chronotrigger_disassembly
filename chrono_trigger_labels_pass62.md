# Chrono Trigger Labels — Pass 62

## Purpose
This file records the new global-opcode mappings justified by pass 62.

The main result is that several early entries in the corrected master `C1:B80D` opcode space are now proved to be **replay/control-flow gates** rather than opaque effect bodies.

Their shared contract is:
- success -> `JSR $8C3E`
- failure -> `LDA #$01 / STA $AF24 / RTS`

---

## Strong labels

### C1:8EA7..C1:8EAA  ct_global_opcode_00_unconditional_tail_replay_step                [strong]
- Direct body is only: `JSR $8C3E ; RTS`.
- Global opcode `00` is therefore an unconditional handoff into the tail replay/controller layer.
- This is a master-table opcode mapping, not a standalone subsystem root.

### C1:9013..C1:9043  ct_global_opcode_05_gate_tail_replay_by_live_unwithheld_tail_count_max [strong]
- Reads one immediate operand byte from `CC:[B1D2 + 1]`.
- Counts tail entries where:
  - `AF02[x] != FF`
  - and `AF15[x] == 0`
- Success path is taken when the resulting count is **less than or equal to** the immediate operand.
- Success -> `JSR $8C3E`
- Failure -> `AF24 = 1`
- This strengthens the old pass-57 count gate by pinning the compare direction.

### C1:9045..C1:9081  ct_global_opcode_06_gate_tail_replay_when_96f1_96f3_triplet_gte_immediate [strong structural]
- Reads a 3-byte immediate operand from `CC:[B1D2 + 1..3]`.
- Compares that operand lexicographically against current WRAM bytes:
  - `96F1`
  - `96F2`
  - `96F3`
- Success when current triplet >= immediate triplet.
- Success -> `JSR $8C3E`
- Failure -> `AF24 = 1`
- Gameplay-facing noun for `96F1..96F3` remains intentionally open.

### C1:9082..C1:90BD  ct_global_opcode_07_gate_tail_replay_on_current_b320_compare_mode [strong structural]
- Reads compare byte from `CC:[B1D2 + 1]` and mode byte from `CC:[B1D2 + 2]`.
- Uses current slot index `B252` to read `B320[B252]`.
- Proven compare modes:
  - mode `!= 1` -> success when `B320[current] >= operand1`
  - mode `== 1` -> success when `B320[current] <= operand1`
- Success -> `JSR $8C3E`
- Failure -> `AF24 = 1`
- Final gameplay-facing noun for `B320[x]` still wants more caller proof.

### C1:97AB..C1:97BF  ct_global_opcode_20_gate_tail_replay_on_current_aeb3_nonzero      [strong structural]
- Uses current index `B252`.
- Reads `AEB3[B252]`.
- Success only when that byte is nonzero.
- Success -> `JSR $8C3E`
- Failure -> `AF24 = 1`
- Final gameplay-facing noun for `AEB3[x]` is still intentionally open.

### C1:97C0..C1:97D4  ct_global_opcode_21_gate_tail_replay_on_current_af15_zero         [strong structural]
- Immediate adjacent sibling of opcode `20`.
- Uses current index `B252`.
- Success only when `AF15[B252] == 0`.
- Success -> `JSR $8C3E`
- Failure -> `AF24 = 1`
- Useful carry-forward proof that opcode `20` is part of a real replay-gate family.

---

## Provisional labels

### 7E:96F1..7E:96F3  ct_c1_global_24bit_replay_gate_triplet_state                       [provisional]
- Pass 62 proves these three bytes are compared lexicographically against the immediate operand in global opcode `06`.
- Earlier work already showed they are globally cleared by another command family.
- The mechanical role is now real.
- The gameplay/system-facing noun still wants more caller-side proof.

---

## Important carry-forward notes

### Do not over-globalize the gate-family result yet
Pass 62 proves a real replay/control subset in the early master-table band.
That does **not** mean every early opcode is a gate.
`01` and `02` still look like heavier selector/filter bodies.

### Do not freeze gameplay nouns for `96F1..96F3`, `B320[x]`, or `AEB3[x]` yet
The byte-level mechanics are now strong.
The higher-level subsystem nouns remain open.

### Do keep the new success/failure contract in mind
For the solved subset here, the important pattern is:
- success -> replay/controller continuation through `8C3E`
- failure -> `AF24 = 1`

That is the cleanest architectural carry-forward from pass 62.
