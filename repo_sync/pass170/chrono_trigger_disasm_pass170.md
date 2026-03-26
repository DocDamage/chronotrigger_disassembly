# Chrono Trigger Disassembly — Pass 170 (Targeted Audit)

## Scope
Pass 170 audits the last two remaining revisit candidates:
- `C3:08A9..C3:08B2`
- `C3:01E4..C3:0306`

## Audit results

### `C3:08A9..C3:08B2`
Prior label:
- `ct_c3_unattached_owner_tail_fragment_ending_in_rtl`

### Audit result
**Correct the interpretation.**

This range should **not** remain classified as an unattached orphan tail.

### New evidence
- raw bytes immediately before the range show uninterrupted executable flow from the upstream helper body through exact `C3:08B2`
- exact same-bank caller evidence exists for the upstream helper entry at:
  - `C3:F1CF -> JSR $0800`
- exact `08A9..08B2` contains only the terminal tail sequence of that helper:
  - local accumulator/store cleanup
  - `PLY/PLX/PLP/PLB/RTL`-style unwind tail ending in exact `RTL`

### Structural conclusion
`C3:08A9..C3:08B2` is the **attached terminal tail of the helper rooted at `C3:0800`**, not a floating orphan owner fragment.

### Correction
- retire the idea that this range is an unattached owner tail
- keep it flagged as pending full upstream closure/relabel of the helper rooted at `C3:0800`

---

### `C3:01E4..C3:0306`
Prior split:
- `C3:01E4..C3:02DC`
- `C3:02DD..C3:0306`

### Audit result
**Keep the split.**

### New evidence
- exact owner entry `C3:01E4` still has distinct external anchors at:
  - `C3:000E -> JMP $01E4`
  - `C3:4021 -> JSL $C3:01E4`
- exact helper entry `C3:02DD` still has distinct callers at:
  - `C3:024A -> JSL $C3:02DD`
  - `C3:15E4 -> JSL $C3:02DD`
- the helper remains separately callable and must not be flattened back into the owner

### Structural conclusion
The pass-163 owner/helper split remains correct and is now better supported than before.

## Resulting state
- revisit candidate `08A9..08B2` is resolved as **attached tail, not orphan**
- revisit candidate `01E4..0306` is resolved as **keep split**
- remaining work shifts back to forward progress in the higher `C3` lane

## Completion snapshot after pass 170
- overall completion estimate: **~71.6%**
- exact label rows: **1343**
- exact strong labels: **1025**
