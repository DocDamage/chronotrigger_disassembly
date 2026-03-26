# Chrono Trigger Disassembly — Pass 171

## Scope
Pass 171 makes cautious forward progress in the next higher `C3` lane by closing the first small, defensible non-owner slice before the larger unresolved body.

## Closed span
- `C3:1300..C3:1317` — inline control/dispatch data block immediately preceding the higher executable body that begins at `C3:1318`

## Why this closure is safe
- bytes at `C3:1300..C3:1317` do not present a credible normal routine prologue
- the sequence is compact, low-structure control-like data with multiple small literal values and no clean owner boundary behavior
- the first bytes at `C3:1318` are much more code-like:
  - immediate state load from exact `0384`
  - mask/shift setup
  - exact indexed dispatch (`FC 43 30`) into a jump-style control path
- freezing `1300..1317` as data avoids forcing a fake monolithic owner across a table/control prefix

## Structural reading
Strongest safe interpretation:
- `1300..1317` is one inline control/dispatch table or parameter block
- it belongs to the surrounding higher `C3` control lane
- the real executable body worth attacking next begins at `C3:1318`

## Strong label added
- `C3:1300..C3:1317` — `ct_c3_inline_control_dispatch_data_block_preceding_higher_c3_execution_body`

## Resulting next target
- **`C3:1318..C3:1816`**

## Completion snapshot after pass 171
- overall completion estimate: **~71.7%**
- exact label rows: **1344**
- exact strong labels: **1026**
