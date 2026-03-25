# Chrono Trigger Disassembly — Pass 62

## Scope of this pass
This pass continued the exact live seam left by pass 61:

1. stay inside the **early global opcode band** of the master `C1:B80D` table
2. prioritize the pack-fed observed opcodes from pass 61
3. determine whether the early entries are real mutators or mostly gate/control wrappers
4. tighten the success/failure contract around `8C3E` and `AF24`

The highest-value result of this pass is that a meaningful chunk of the early global opcode band is now much less mysterious:

> several early global opcodes are **gate wrappers into the tail replay/controller layer**.
>
> Their common shape is:
>
> - **success** -> `JSR $8C3E`
> - **failure** -> `LDA #$01 / STA $AF24 / RTS`
>
> So these are not opaque “do anything” commands.
> A real subset of the early pack-fed opcode band is now structurally pinned as **boolean gate/control flow over tail replay**.

That is a useful architectural upgrade because it narrows what the remaining unsolved early handlers can be.

---

## Method
1. Re-opened the master-table early targets proved in pass 61:
   - `00 -> 8EA7`
   - `05 -> 9013`
   - `06 -> 9045`
   - `07 -> 9082`
   - `20 -> 97AB`
2. Decoded the handlers directly from ROM bytes rather than reusing the older pass-31 table story.
3. Checked each handler for:
   - parameter fetch shape from `CC:[B1D2 + n]`
   - success path
   - failure path
   - interaction with `8C3E`
   - interaction with `AF24`
4. Cross-checked the results against the already-solved deferred-tail/live-tail model from passes 57 and 61.

---

## 1. Global opcode `00` is an unconditional replay/controller step
Handler bytes:

```text
C1:8EA7  20 3E 8C
C1:8EAA  60
```

That is simply:

```text
JSR $8C3E
RTS
```

### What this proves
Global opcode `00` is not a data-mutating body and not a private mini-op.
It is a **direct unconditional handoff** into the already-proved tail replay/controller block at `8C3E`.

### Strongest safe interpretation
This is best carried forward as:

> **unconditional tail replay/controller step**

That fits pass 61 cleanly, because `8C3E..8CF7` is the layer that:
- records the just-executed opcode
- scans to the next `FE` boundary
- updates replay pointer state
- resumes execution through the shared opcode machinery

So opcode `00` is effectively a “continue/replay now” control step.

---

## 2. Global opcode `05` is the pass-57 tail-count gate, now pinned to a concrete opcode
Handler bytes:

```text
C1:9013  AE D2 B1
C1:9016  BF 01 00 CC 85 08
C1:901C  7B AA 86 0A
C1:9020  BD 02 AF C9 FF F0 07
C1:9027  BD 15 AF D0 02
C1:902C  E6 0A
C1:902E  E8 E0 08 00 90 EC
C1:9034  A5 08 C5 0A 90 05
C1:903A  20 3E 8C
C1:903D  80 05
C1:903F  A9 01 8D 24 AF
C1:9043  60
```

### What it does
1. loads one immediate operand byte from `CC:[B1D2 + 1]` into `$08`
2. scans all 8 tail slots
3. increments the local count `$0A` only when:
   - `AF02[x] != FF`
   - and `AF15[x] == 0`
4. compares the immediate operand against the live count
5. on success calls `JSR $8C3E`
6. on failure sets `AF24 = 1`

### Important compare-direction correction
This pass makes the branch direction concrete.
The success path is taken when:

> **live unwithheld tail count <= immediate operand**

because the failure branch is the `BCC` after `CMP count`.
So this opcode is not just a vague “count gate.”
It is specifically an **upper-bound gate** on the number of currently live, unwithheld tail entries.

### Strongest safe interpretation
Global opcode `05` is best carried forward as:

> **gate tail replay when live-unwithheld-tail-count is at or below an immediate maximum**

This strengthens pass 57 by pinning that count gate to a real master-table opcode.

---

## 3. Global opcode `06` is a lexicographic 24-bit gate against `96F1..96F3`
Handler bytes:

```text
C1:9045  AE D2 B1
C1:9048  BF 01 00 CC 85 08
C1:904E  BF 02 00 CC 85 09
C1:9054  BF 03 00 CC 85 0A
C1:905A  AD F3 96 C5 0A 90 1B F0 02 80 12
C1:9065  AD F2 96 C5 09 90 10 F0 02 80 07
C1:9070  AD F1 96 C5 08 90 05
C1:9077  20 3E 8C
C1:907A  80 05
C1:907C  A9 01 8D 24 AF
C1:9081  60
```

### What it does
This handler reads three immediate bytes from the CC stream and compares them lexicographically against the current WRAM triplet:

- low  -> `$08`
- mid  -> `$09`
- high -> `$0A`

with the current state bytes at:

- `96F1`
- `96F2`
- `96F3`

The compare order is high, then middle, then low.
That means it is a standard lexicographic compare of a 24-bit value.

### Success condition
The success path is taken when:

> **current `96F1..96F3` value >= immediate 24-bit operand**

Otherwise the handler sets `AF24 = 1`.

### Strongest safe interpretation
Global opcode `06` is best carried forward as:

> **gate tail replay when the current WRAM 24-bit triplet is at or above an immediate 24-bit threshold**

I am intentionally not freezing a gameplay-facing noun for `96F1..96F3` yet.
But mechanically this compare is no longer ambiguous.

---

## 4. Global opcode `07` is a comparator gate on `B320[current]`, with the second operand selecting the compare direction
Handler bytes:

```text
C1:9082  AE D2 B1
C1:9085  BF 01 00 CC 85 08
C1:908B  BF 02 00 CC 85 0A
C1:9091  C9 01 F0 0E
C1:9095  7B AD 52 B2 AA BD 20 B3 C5 08 B0 12
C1:90A1  80 15
C1:90A3  7B AD 52 B2 AA BD 20 B3 C5 08 F0 04 90 02
C1:90B1  80 05
C1:90B3  20 3E 8C
C1:90B6  80 05
C1:90B8  A9 01 8D 24 AF
C1:90BD  60
```

### What it does
This handler reads:
- compare byte -> `$08`
- mode byte    -> `$0A`

Then it uses the current slot index in `B252` to read the byte at:

- `B320[B252]`

### Compare behavior
Two modes are directly proved:

#### mode byte `!= 1`
Success when:

> `B320[current] >= operand1`

#### mode byte `== 1`
Success when:

> `B320[current] <= operand1`

On success it enters `8C3E`.
On failure it sets `AF24 = 1`.

### Strongest safe interpretation
Global opcode `07` is best carried forward as:

> **mode-controlled comparator gate on the current `B320` byte**

I am intentionally keeping the human-facing noun for `B320[x]` open.
But the compare mechanics themselves are now solid.

---

## 5. Global opcode `20` is a nonzero gate on the current `AEB3` byte
Handler bytes:

```text
C1:97AB  7B AD 52 B2 AA BD B3 AE F0 05
C1:97B5  20 3E 8C
C1:97B8  80 05
C1:97BA  A9 01 8D 24 AF
C1:97BF  60
```

### What it does
1. loads the current tail/local slot index from `B252`
2. reads `AEB3[B252]`
3. if nonzero -> `JSR $8C3E`
4. if zero -> `AF24 = 1`

### Strongest safe interpretation
Global opcode `20` is best carried forward as:

> **nonzero gate on the current `AEB3` state byte**

I am not freezing a gameplay-facing noun for `AEB3[x]` yet.
But the gate mechanics are direct and clean.

---

## 6. Adjacent sibling: global opcode `21` is the same gate shape over `AF15[current] == 0`
The immediately adjacent handler at `97C0` is structurally useful even though it was not one of the pack-fed observed bytes carried by pass 61.

Bytes:

```text
C1:97C0  7B AD 52 B2 AA BD 15 AF F0 05
C1:97CA  20 3E 8C
C1:97CD  80 05
C1:97CF  A9 01 8D 24 AF
C1:97D4  60
```

This proves the same exact gate skeleton over a different state byte:

> success only when `AF15[current] == 0`

This matters because it strengthens the idea that the early opcode band contains a real **replay gate family**, not isolated one-offs.

---

## 7. Architectural consequence: an early global replay-gate family now exists
The solved handlers above all share the same high-level success/failure contract:

### Degenerate unconditional form
- `00 -> always JSR 8C3E`

### Conditional forms
- `05 -> if live-unwithheld-tail-count <= immediate`
- `06 -> if current 24-bit triplet >= immediate 24-bit value`
- `07 -> if current B320 byte satisfies mode-selected compare`
- `20 -> if current AEB3 byte != 0`
- `21 -> if current AF15 byte == 0`

### Shared failure contract
- `AF24 = 1`

### Why this matters
This means at least part of the early global opcode band is not best read as “effect logic.”
It is better read as:

> **predicate/gate control over whether the replay/controller layer continues**

That narrows the space of plausible semantics for the remaining unsolved early entries.

---

## 8. Corrections tightened by this pass
### A. pass-57 count gate is now less vague
Pass 57 correctly identified the live-unwithheld tail count gate at `9012..9043`, but the exact compare direction was still easy to phrase loosely.

Pass 62 pins the concrete success condition for the master-table opcode:

> **opcode `05` succeeds when current live-unwithheld-tail-count does not exceed the immediate operand**

### B. early master-table work should stop treating all unknown entries as likely “mutators”
For the solved subset here, the stronger read is control/predicate gating into replay.
That is a real narrowing of the remaining search space.

---

## Still unresolved
1. global opcodes `01` and `02` still look like heavier selector/filter bodies rather than simple gates
2. the gameplay-facing nouns for:
   - `96F1..96F3`
   - `B320[x]`
   - `AEB3[x]`
   still want broader caller proof
3. the exact family boundary between:
   - selector/filter bodies
   - replay-gate bodies
   - relation-query wrappers
   inside the early master band still needs one more pass
4. I have not yet re-opened pack-fed observed opcodes:
   - `09`
   - `0A`
   - `0B`
   - `0F`
   - `12`
   from the same corrected master-table framing

---

## Best next target from here
The best continuation after this pass is:

1. stay in the same early global master-table band
2. attack `01` and `02` as the likely selector/filter siblings sitting next to the solved gate wrappers
3. then reopen `09/0A/0B/0F/12` to see whether they form:
   - more replay gates,
   - relation-query wrappers,
   - or a separate selected-list mutation family

If runtime confirmation is needed, these are now good trace candidates specifically because the newly solved handlers establish a much clearer pass/fail contract around `AF24` and `8C3E`.
