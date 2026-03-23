# Chrono Trigger (USA) — Disassembly Pass 32

## Scope
This pass continues directly from pass 31 and stays on the highest-value unresolved target from the master handoff: **bank `C1` group-1 (`B85F`) and group-2 (`B88D`) CC-stream command handlers**.

Pass 31 established that bank `C1` contains four real CC-stream command tables and that `B85F` / `B88D` were still mostly opaque. This pass does not replace the handoff; it extends it.

## Baseline carried forward
- ROM target unchanged: headerless 4 MiB USA HiROM/FastROM build of `Chrono Trigger (USA).sfc`
- Pass 31 remained the prior top-of-stack
- The current high-value target remained group 1 and group 2 command decoding before broader bank splitting

## What was done in this pass
1. Re-opened the group-1 command table at `C1:B85F`
2. Re-opened the group-2 command table at `C1:B88D`
3. Cross-checked dispatch behavior around `C1:8CE7` and `C1:8D88`
4. Pulled the `FD:BA4A` lookup bytes used by the group-1 random-control path
5. Identified which table entries are real bodies vs `RTS` / `STZ $AF24 ; RTS` aliases
6. Isolated the strongest new handler semantics without over-claiming subsystem ownership

## Core results

### 1. `FD:BA4A` is a real opcode-indexed control table for the `0x00..0x16` family
The byte sequence at `FD:BA4A` for the first 23 entries is:

```text
04 04 06 00 FF FF 04 04 04 02 03 05 04 03 02 02 04 0A 10 03 0A 10 0C
```

This table is directly consumed by the random-control path at `C1:98C5` and lines up with the group-1 / group-2 opcode span. It is strongest to keep this as a **command advance / stream-skip control table** for now, not a fully solved universal operand-size table.

### 2. Group 1 is more alias-heavy than it first looked
`C1:B85F` is not 23 independent high-value handlers. A large fraction of entries land in small stub bodies or directly into padding-style `RTS` runs.

#### Group 1 table map (`C1:B85F`)
```text
00 -> C1:9810
01 -> C1:983A
02 -> C1:983A
03 -> C1:98C4
04 -> C1:98C5
05 -> C1:9960
06 -> C1:9961
07 -> C1:9962
08 -> C1:9966
09 -> C1:9967
0A -> C1:9978
0B -> C1:9979
0C -> C1:997D
0D -> C1:997E
0E -> C1:997F
0F -> C1:9980
10 -> C1:9981
11 -> C1:99B4
12 -> C1:99B4
13 -> C1:99B4
14 -> C1:99B4
15 -> C1:99B4
16 -> C1:9981
```

#### Strong alias/stub observations
- `0x03 -> C1:98C4` = `RTS`
- `0x05 -> C1:9960` = `RTS`
- `0x06 -> C1:9961` = `RTS`
- `0x07 -> C1:9962` = `STZ $AF24 ; RTS`
- `0x08 -> C1:9966` = `RTS`
- `0x0A -> C1:9978` = `RTS`
- `0x0B -> C1:9979` = `STZ $AF24 ; RTS`
- `0x0C..0x0F -> C1:997D..9980` = land in `RTS` run
- `0x11..0x15 -> C1:99B4` = shared `STZ $AF24 ; RTS`

So one real advance in this pass is that group 1 is no longer being treated as “23 unknown commands.” It is a much smaller set of meaningful bodies surrounded by explicit no-op / clear-flag exits.

### 3. Group-1 opcode `0x04` is a real random 4-way control-flow command
`C1:98C5` is the strongest semantic win in pass 32.

Observed structure:
- requests a random value with `#$64`
- splits the result into four ranges (`< 0x19`, `< 0x32`, `< 0x4B`, else)
- repeatedly consults `FD:BA4A`
- advances the current command-stream pointer by command-sized boundaries before resuming

Best current name:
- **group-1 opcode `0x04` = random 4-way stream-advance / branch-style command**

That name is still intentionally conservative. It clearly manipulates command-stream control flow; it is not just a small setter.

### 4. Group 2 continuation control is now structurally clearer
The dispatcher tail at and after `C1:8D88` makes two control bytes important:

- `$AF24` = handler short-circuit / abort-style flag
- `$B3B8` = post-handler continuation selector

Current best interpretation of `$B3B8`:
- `0` = take the fuller continuation path
- `1` = take the continuation path that includes the extra helper call before the common tail
- `2` = skip that extra step and fall directly into the common tail

This is a structural result, not a full semantic subsystem label.

### 5. Group 2 now has several concrete handlers pinned

#### Group 2 table map (`C1:B88D`)
```text
00 -> C1:99B8
01 -> C1:99BE
02 -> C1:9A39
03 -> C1:9B46
04 -> C1:9B47
05 -> C1:9B48
06 -> C1:9B8C
07 -> C1:9B8D
08 -> C1:9C6E
09 -> C1:9C6F
0A -> C1:9CB3
0B -> C1:9D1B
0C -> C1:9D72
0D -> C1:9DCE
0E -> C1:9E62
0F -> C1:9E63
10 -> C1:9E78
11 -> C1:9F5A
12 -> C1:9FD2
13 -> C1:A14E
14 -> C1:A188
15 -> C1:A20B
16 -> C1:A396
```

#### Strongest new group-2 identifications
- `0x00 -> C1:99B8`
  - immediate continuation-select return
  - writes `#$02` to `$B3B8`

- `0x03 -> C1:9B46`
  - `RTS` stub

- `0x04 / 0x05 -> C1:9B47 / C1:9B48`
  - shared variable-control family
  - structurally real bodies, not simple fixed-size setters

- `0x0D -> C1:9DCE`
  - bitmask-driven per-slot/global state control
  - operand bits drive a mix of:
    - per-slot state at `$B320,x`
    - per-slot flag bit writes into `$5E4A,x`
    - global clears at `$96F1/$96F2/$96F3`
  - operand 2 can optionally trigger `JSL $CD0033`

- `0x0F -> C1:9E63`
  - minimal wrapper
  - if operand 1 is nonzero, calls `JSL $CD0033`
  - then returns with `$B3B8 = 2`

- `0x13 -> C1:A14E`
  - saturating signed-delta update to `$B158[current]`
  - positive deltas add with clamp at `#$FF`
  - negative deltas subtract with floor at `#$00`

### 6. `C1:A3D1` is a reusable saturating signed byte-adjust helper
This helper takes the signed delta in `$10` and adjusts the byte addressed through `(0E),Y` with floor/clamp behavior.

That matters because:
- `0x14 -> C1:A188`
- `0x15 -> C1:A20B`

both use this helper repeatedly.

So the `0x13 / 0x14 / 0x15` cluster is now best treated as a real family:
- one direct per-slot saturating byte adjust
- then wider multi-target saturating adjust variants

## What changed in the understanding of the table set
Before this pass:
- group 1 and group 2 were “still mostly opaque”

After this pass:
- the alias/stub density in group 1 is now explicit
- one real random stream-control command is identified
- group-2 continuation control via `$AF24` / `$B3B8` is structurally pinned
- one bitmask state-control command is identified
- one optional external-call wrapper is identified
- one direct saturating-delta command is identified
- two wider saturating-adjust family members are structurally identified

That does **not** mean group 1 or group 2 are finished. It means the center of gravity has shifted from “opaque table” to “specific unresolved clusters.”

## Best current unresolved cluster after pass 32
The remaining highest-value unsolved group-2 bodies are now:

```text
0x01 -> C1:99BE
0x02 -> C1:9A39
0x10 -> C1:9E78
0x11 -> C1:9F5A
0x12 -> C1:9FD2
0x16 -> C1:A396
```

These are the best next targets because they appear to sit on the heavier object-selection / pointer-fed mutation side of the interpreter.

## Confidence notes
### Strong enough to keep
- `C1:B85F` and `C1:B88D` full opcode-to-target maps
- alias/stub identification for the obvious `RTS` / `STZ $AF24 ; RTS` entries
- `FD:BA4A` as a real control lookup table used by the group-1 random path
- `C1:98C5` as a random 4-way stream-control command
- `$AF24` as a handler short-circuit flag
- `$B3B8` as a post-handler continuation selector
- `C1:9DCE`, `C1:9E63`, `C1:A14E`, `C1:A3D1` as meaningful solved bodies/helpers

### Still provisional / intentionally not overclaimed
- exact user-facing “opcode names” for most of group 1 / group 2
- exact command encoding rule for every `FD:BA4A` entry
- whether each unresolved handler is map/event/object-side, battle-side, or a shared service wrapper
- higher-level narrative names for the `CD0033` service without caller-side proof

## Recommended next pass from here
Stay in group 2 and attack this order:
1. `C1:9E78`
2. `C1:9F5A`
3. `C1:9FD2`
4. `C1:A396`
5. backfill `C1:99BE` / `C1:9A39`

That keeps the work aligned with the master handoff’s priority order instead of jumping prematurely into source splitting.
