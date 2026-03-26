# Chrono Trigger Disassembly — Pass 169 (Targeted Audit)

## Scope
Pass 169 is a targeted audit pass using the newer repo-native, ROM-aware toolkit flow.
It revisits two high-value earlier closures:
- `C3:09E9..C3:0A8F`
- `C3:0B03..C3:0C91`

The goal was to confirm or overturn earlier structural claims, not to force a new closure for its own sake.

## Audited ranges

### `C3:09E9..C3:0A8F`
Prior label:
- `ct_c3_wram_runtime_code_emitter_writing_generated_stub_bytes_through_2180`

### Audit result
**Keep the closure and keep the label.**

### New evidence
- raw bytes still show literal emitted opcode stream bytes including exact `A9`, exact `5B`, exact `AD`, exact `85`, and exact terminal exact `60`
- exact emitted bytes are written through exact `$2180`, confirming generated WRAM code / command-stub materialization behavior rather than one normal inline worker
- direct long-call hits into exact `C3:09E9` still exist from:
  - exact `C3:1CF3`
  - exact `C3:4D67`

### Structural conclusion
This routine remains a **shared top-level runtime-code emitter**, not one buried helper and not one false data classification.

### Confidence update
- structural confidence upgraded from **medium-high** to **high**
- semantic confidence remains **medium-high**

---

### `C3:0B03..C3:0C91`
Prior label:
- `ct_c3_stream_bytecode_interpreter_updating_0920_0940_and_dispatching_apu_command_words`

### Audit result
**Keep the closure and keep the split.**

### New evidence
- exact `C3:0AFF..C3:0B02` remains a real wrapper veneer: exact `JSR $0B03 ; RTL`
- internal jump-style entries into exact `0B03` family remain consistent with one jump-table-driven interpreter body, not multiple separate public owners
- exact helper `C3:0CB1..C3:0CB7` still has a real same-bank external caller at:
  - exact `C3:C8FD`

### Structural conclusion
The original pass-166 split was correct:
- `0B03..0C91` should remain the main interpreter owner
- `0CB1..0CB7` must remain a separate helper because it is externally called

### Confidence update
- structural confidence upgraded from **medium-high** to **high**
- semantic confidence remains **medium-high**

## What did *not* change
- no range boundaries changed this pass
- no labels were renamed this pass
- no new code/data reclassification was needed for these two targets

## Why this audit still matters
This pass reduces the risk that earlier closures were only “good enough at the time.”
The newer ROM-aware xref pass supports the earlier structural calls instead of exposing a hidden split mistake.

## Resulting state
- audited earlier closures now have stronger structural support
- next unresolved forward-disassembly lane is still:
  - **`C3:1300..C3:1816`**

## Completion snapshot after pass 169
- overall completion estimate: **~71.5%**
- exact label rows: **1343**
- exact strong labels: **1025**
