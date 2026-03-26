# Chrono Trigger (USA) — Disassembly Pass 34

## Scope
This pass continues directly from pass 33 and stays on the last early unresolved **bank `C1` group-2 pair**:

- `0x01 -> C1:99BE`
- `0x02 -> C1:9A39`

The goal of this pass was to replace the remaining generic `body` labels with real structural descriptions and to pin whether these two handlers were siblings, wrappers, or unrelated one-offs.

## Baseline carried forward from pass 33
Pass 33 had already split the later unresolved group-2 cluster into:
- selector/finalizer handlers
- table-selected byte-writer handlers
- fused long-helper wrappers

What was still missing was the earlier pair at `C1:99BE` and `C1:9A39`.

---

## What was done in this pass
1. Fully decoded `C1:99BE`
2. Confirmed that `C1:9A39` is only a wrapper and that the real body is `C1:9A3D`
3. Compared `C1:9A3D` against the already-solved `0x12 -> C1:9FD2` family tail to separate shared commit logic from opcode-specific front-end setup
4. Isolated the state differences between `0x01` and `0x02`, especially:
   - one-entry seed source
   - `B1FC` bit-1 mode behavior
   - whether the handler uses the `C1:C1DD` validation/commit path
   - whether the handler routes through the unique long helper at `FD:AB01`

---

## Core results

### 1. `C1:9A39` is just a wrapper; the real opcode-`0x02` body is `C1:9A3D`
`C1:9A39` contains only:

```text
JSR $9A3D
RTS
```

So the group-2 table target for `0x02` is technically `C1:9A39`, but the actual body worth carrying forward is `C1:9A3D`.

This matters because it lets later passes label the real logic body directly instead of pretending the table entry itself is a meaningful body site.

### 2. Group-2 opcode `0x01` (`C1:99BE`) is a one-entry seeded finalize command with unique long-helper path
This handler is not another generic selector blob. It is compact and structurally distinct.

#### Early setup
At entry it:
- clears `B18C`
- sets bit 1 of `$B1FC` (`ORA #$02`)
- uses current index `$AEC8` to fetch one seed entry from `$5E15[current]`
- stores that same entry into both:
  - `$AD8E`
  - `$AECC`
- sets both saved/current counts to `1`:
  - `$AD8D = 1`
  - `$AECB = 1`
- if the seeded entry is `< 3`, sets `$B3B9 = 1`
- builds the first-selected mask via `JSR $AD09`

So unlike the later multi-entry selector family, opcode `0x01` begins with a **hard-seeded one-entry list**.

#### Parameter capture
It then consumes two inline bytes from the `CC` stream:

- first byte -> `$0E` and `$AEE4`
- second byte -> `$AEE5`

The first byte also controls a special mode:
- if operand 1 is `1`, the handler computes an alternate value for `B18C` from a current-index-derived lookup path through `$5E48,...`
- otherwise `B18C` remains `0` from the entry clear

The safest reading is:
- operand 1 = **mode / primary seed control**
- operand 2 = **secondary mode / subtype parameter**

Do not over-name either yet.

#### Unique helper path
After capturing those bytes the handler calls:

```text
JSL $FDAB01
```

This long helper is currently unique to `0x01` in the solved group-2 set.
It is not shared with the `C1DD` validation/commit family.

#### Final local tail
After `FD:AB01` it runs:
- `JSR $AC89`
- `JSR $ACCE`
- `B3B8 = 0`
- `RTS`

So opcode `0x01` is best treated as:

> **single-entry seeded finalize command with `B1FC.bit1` set and unique `FD:AB01` long-helper path**

That is substantially more precise than the old generic `body` label.

### 3. Group-2 opcode `0x02` (`C1:9A39 -> 9A3D`) is a seeded dual-inline-selector validation/commit command
This opcode is a real sibling of the later validation/commit family, but it has a smaller front end.

#### Early setup
At `C1:9A3D` it:
- clears bit 1 of `$B1FC` (`AND #$FD`)
- consumes one inline byte and stores it into both:
  - `$AEE4`
  - `$B18C`
- seeds the current/saved selected entry from `$B16E[current]` using `$AEC8`
- stores that same entry into both:
  - `$AECC`
  - `$AD8E`
- sets both saved/current counts to `1`:
  - `$AD8D = 1`
  - `$AECB = 1`
- initializes selector results to empty:
  - `$AE97 = $FF`
  - `$AE98 = $FF`

So opcode `0x02` also begins from a **hard-seeded one-entry list**, but it uses a different source table than `0x01`:
- `0x01` seeds from `$5E15[current]`
- `0x02` seeds from `$B16E[current]`

That difference is real and should be preserved.

#### Optional dual-selector phase
It then consumes up to two additional inline bytes.
For each nonzero byte:
- preserves current `$AECC`
- calls `JSR $AC14`
- stores the resolved selection into `$AE97` or `$AE98`
- restores original `$AECC`

This is the same selector-resolution pattern already seen in the heavier `0x12` family, but here there is no front-half writer stage before it.

#### Validation / commit phase
After selector resolution it:
- maps selector results through `$AEFF[...]` into:
  - `$B2EB`
  - `$B2EC`
- stores current selection into `$B2AE`
- calls `JSR $C1DD`

If validation fails (`$AF23 != 0`):
- jumps to the shared failure site at `C1:9B3B`
- sets `$AF24 = 2`
- returns with `$B3B8 = 0`

If validation succeeds:
- restores `$AD8E[] -> $AECC[]`
- restores `$AD8D -> $AECB`
- if first selected entry is `< 3`, sets `$B3B9 = 1`
- rebuilds masks with:
  - `JSR $AD09`
  - `JSR $AD35`
- runs `JSL $FDAAD2`
- runs local follow-up helpers:
  - `JSR $AC89`
  - `JSR $ACCE`
- returns with `$B3B8 = 0`

So opcode `0x02` is best treated as:

> **seeded dual-inline-selector validation/commit command**

### 4. `0x02` is a lighter sibling of `0x12`, not a duplicate
This pass matters because `0x02` and `0x12` looked easy to collapse together, but that would be wrong.

Shared with `0x12`:
- dual optional selector resolution through `AC14`
- validation through `C1DD`
- success tail using `AD09`, `AD35`, `FDAAD2`, `AC89`, `ACCE`
- failure path through `$AF23` / `$AF24`

Not shared with `0x12`:
- no group-base-selected write phase
- no five write-pairs front half
- no `AEE3 = 2` setup before the success tail
- different initial one-entry seed source (`$B16E[current]`)

So `0x02` should be grouped with the validation/commit family, but as a **smaller seeded variant**, not as a synonym for `0x12`.

### 5. `0x01` and `0x02` intentionally split on `B1FC` bit 1 and on seed source
This pass finally makes the early pair readable as a deliberate split rather than two opaque leftovers.

#### `0x01`
- sets `B1FC.bit1`
- seed source = `$5E15[current]`
- captures two inline parameters (`AEE4`, `AEE5`)
- routes through unique long helper `FD:AB01`
- does not locally call `C1DD`

#### `0x02`
- clears `B1FC.bit1`
- seed source = `$B16E[current]`
- captures one direct parameter into `AEE4/B18C`
- optionally resolves two inline selector bytes
- explicitly calls `C1DD` and uses the shared validation/commit tail

This is now strong enough to retire the last generic early group-2 labels.

---

## Working opcode interpretations after this pass

### Group-2 opcode `0x01`
Best current reading:

> **one-entry seeded finalize command (`$5E15[current]`) with `B1FC.bit1` set, two inline params, and unique `FD:AB01` helper path**

### Group-2 opcode `0x02`
Best current reading:

> **one-entry seeded dual-inline-selector validation/commit command (`$B16E[current]`) with `B1FC.bit1` clear**

---

## What changed in the understanding of group 2
Before this pass, the remaining early pair was still effectively:
- `0x01 -> body`
- `0x02 -> body`

After this pass:
- `0x01` is structurally identified as a compact one-entry finalize path with a unique long helper
- `0x02` is structurally identified as a smaller seeded member of the selector/validation/commit family
- the real logic site for `0x02` is pinned at `C1:9A3D`
- the group-2 table is now structurally complete enough that the next value is no longer “find the missing handler bodies,” but rather tighten helper semantics and cross-family naming

---

## Remaining uncertainty / naming guardrails
- Do **not** claim exact gameplay meaning for `$5E15[current]` vs `$B16E[current]` yet; only the distinct seed sources are proven here.
- Do **not** over-name `$AEE4`, `$AEE5`, or `$B18C`; they are clearly control/state inputs, but their gameplay-facing semantics still need caller proof.
- Do **not** pretend `FD:AB01` is ordinary linear code; it is only safe to label it as the long helper uniquely used by `0x01` until more proof exists.
- Do **not** merge `0x02` into `0x12`; they share a tail, but their front halves and state setup are different.

---

## Best next target after pass 34
With the early pair now structurally resolved, the next high-value step is **helper tightening**, not another blind table sweep.

Best targets:
1. `C1:C1DD` — validation gate semantics
2. `C1:AC89` / `C1:ACCE` — commit/finalization state assembly
3. `FD:AB01` — determine whether it is true code, a script/data-driven helper, or an external interpreter entry used only by opcode `0x01`

Those helpers now matter more than table coverage, because group 2 is no longer held back by unidentified opcode bodies.
