# Current Seam Candidate Starts

- Latest pass: **143**
- Target seam: **`C2:E60B..C2:E760`**
- Candidate count: **9**

## Top candidates
- `C2:E743` | score=9.0 | offset=+0x0138 | calls=3 | seed=no | prev_byte=83
  - head bytes: `08 E2 30 A6 54 BD 49 0D D0 10`
  - incoming ops: `{"JSR abs": 3}`
  - sample callers: `[{"caller": "C2:E63A", "op": "JSR abs"}, {"caller": "C2:E6B8", "op": "JSR abs"}, {"caller": "C2:E7F3", "op": "JSR abs"}]`
- `C2:E683` | score=6.0 | offset=+0x0078 | calls=1 | seed=no | after RTS
  - head bytes: `A2 00 BD 49 0D F0 07 E8 E0 03`
  - incoming ops: `{"JMP abs": 1}`
  - sample callers: `[{"caller": "C2:E6D0", "op": "JMP abs"}]`
- `C2:E60B` | score=5.0 | offset=+0x0000 | calls=0 | seed=no | after RTS
  - head bytes: `13 E6 1B E6 AE E6 05 E7 20 C3`
  - nearby labels:
    - pass 143 [strong] `C2:E5CC..C2:E60A` :: ct_c2_54_plus_1_change_handler_refreshing_0d77_020c_5248_6a20_cf3b_0200_then_fa49
  - note mentions: `["chrono_trigger_disasm_pass143.md", "chrono_trigger_labels_pass143.md"]`
- `C2:E61B` | score=5.0 | offset=+0x0010 | calls=0 | seed=yes | prev_byte=83
  - head bytes: `AD 20 04 C9 30 D0 10 A5 54 C9`
- `C2:E6AE` | score=5.0 | offset=+0x00A3 | calls=0 | seed=yes | prev_byte=83
  - head bytes: `20 84 E9 2C 1D 0D 30 0F 70 27`
- `C2:E705` | score=5.0 | offset=+0x00FA | calls=0 | seed=yes | prev_byte=83
  - head bytes: `20 84 E9 2C 1D 0D 30 10 70 0A`
- `C2:E73F` | score=5.0 | offset=+0x0134 | calls=0 | seed=yes | prev_byte=0D
  - head bytes: `FC 4C 85 83 08 E2 30 A6 54 BD`
- `C2:E694` | score=3.0 | offset=+0x0089 | calls=1 | seed=no | prev_byte=04
  - head bytes: `A9 F3 8D 00 1E AD 90 29 29 08`
  - incoming ops: `{"JMP abs": 1}`
  - sample callers: `[{"caller": "C2:E6DC", "op": "JMP abs"}]`
- `C2:E6DD` | score=3.0 | offset=+0x00D2 | calls=1 | seed=no | prev_byte=4C
  - head bytes: `94 E6 20 C2 EA C6 68 CE 4C 0D`
  - incoming ops: `{"JSR abs": 1}`
  - sample callers: `[{"caller": "C2:DD0D", "op": "JSR abs"}]`
