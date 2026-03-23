# Chrono Trigger Disassembly — Pass 30

This pass followed the exact open question from pass 29:

- who actually seeds `986E/986F/9870/9871`
- and what kind of higher-level code is doing it

The answer is cleaner than “some random callers set them.”

The relation-query block is being driven by a **bank-C1 object-command / predicate layer** that sits above the raw geometry code and consumes the results through `AE/AF` work registers.

## Correction to pass 29

Pass 29 understated the live mode range for the relation-query jump table.

I now have hard caller evidence for relation-query modes:

- `00`
- `01`
- `02`
- `03`
- `04`
- `05`
- `06`
- `08`
- `09`
- `0A`
- `0B`
- `0C`
- `0E`

So the jump table at `C1:2D81` is live **at least through mode `0E`**.
The “14-entry” description from pass 29 was too small.

## `C1:0003 / C1:0045` are the bank-C1 function dispatch veneer

The low-bank stub at `C1:0003` is just:

- `JMP $0045`

And `C1:0045` is a real A-register function dispatcher:

- saves `A/X/Y`
- doubles `A`
- uses `JSR ($0051,X)`
- restores registers
- returns

That means the very common sequence:

- `LDA #$05`
- `JSR $0003`

is not arbitrary.
It is a real call into the bank-C1 function table, and selector `5` lands in the relation-query dispatcher at `C1:2986`.

### Best-fit names

- `C1:0003 = Dispatch_BankC1_FunctionByA`
- `C1:0045 = Dispatch_BankC1_FunctionTableCore`

## Caller cluster 1: `C1:9260..977D` is a predicate-style relation-query wrapper block

A dense group of routines in this region all follow the same higher-level pattern:

1. call a common setup/helper (`JSR $AC14`)
2. read and write `AE/AF` work registers
3. seed `986E..9871`
4. invoke the relation-query block with `LDA #$05 / JSR $0003`
5. consume `9872` or `9873`
6. update `AECC / AECB / AF24`

That is exactly what a **command/predicate wrapper layer** looks like.

## Common subject-slot source: `B252 + 3`

Multiple wrappers seed `986F` with the same sequence:

- `LDA $B252`
- `CLC`
- `ADC #$03`
- `STA $986F`

So `986F` is very often being loaded from a single “current object / current command owner” style slot source rather than from a transient local loop variable.

I am intentionally keeping the label conservative here.
What is safe to say is:

- `B252` behaves like a current active object / interpreter-owned slot base
- `+3` is the normalized slot index fed into the relation-query layer

## Predicate wrappers now pinned down

### `C1:9260`

Seeds:

- `986F <- B252 + 3`
- `986E <- 04`
- `9870 <- AECC`

Then dispatches through `0003`, checks `9872`, and updates `AECB / AF24`.

### Best-fit name

- `C1:9260 = ObjectCmd_RunRelationQuery_Mode04_WithAECC`

### `C1:92A3`

Seeds:

- `986F <- B252 + 3`
- `986E <- 05`

Then loops candidate values through `9870`, dispatches, and consumes `9872`.

### Best-fit name

- `C1:92A3 = ObjectCmd_RunRelationQuery_Mode05_OverCandidateList`

### `C1:9313`

Seeds:

- `986F <- B252 + 3`
- `986E <- 06`

It is structurally the sibling of `92A3`, with the same list-style candidate walk and `9872` consumption.

### Best-fit name

- `C1:9313 = ObjectCmd_RunRelationQuery_Mode06_OverCandidateList`

### `C1:9390`

Seeds:

- `986F <- B252 + 3`
- `986E <- 08`
- `9870 <- AECC`
- `9871 <- packed/derived arg from the `CC` bank table`

Then dispatches and consumes both `9872` and surrounding command state.

### Best-fit name

- `C1:9390 = ObjectCmd_RunRelationQuery_Mode08_WithDualArgs`

### `C1:9400`

Selects one of several relation modes before dispatch:

- `09`
- `0A`
- `0B`
- `0C`

Then seeds `986F <- B252 + 3`, runs the dispatcher, and consumes the returned state through the same `AE/AF` work bytes.

### Best-fit name

- `C1:9400 = ObjectCmd_RunRelationQuery_Mode09to0C_SelectedByPreset`

### `C1:9765`

Seeds:

- `986F <- B252 + 3`
- `986E <- 0E`
- `9870 <- AECC`

Then dispatches and consumes `9872`.

This is the clean proof that the relation-query mode range extends beyond `0D`.

### Best-fit name

- `C1:9765 = ObjectCmd_RunRelationQuery_Mode0E_WithAECC`

## Caller cluster 2: `C1:A4AA..A75F` is a target-selection wrapper block

A second dense block uses the same relation-query service, but the post-call behavior is different:

- the returned `9873` value is treated as a chosen slot
- that slot is written back into `AECC`
- failure/sentinel cases clear or gate the same command-state bytes

These wrappers are best understood as **target-selection commands**.

### `C1:A4AA`

Seeds:

- `986F <- B252 + 3`
- `986E <- 00`

Runs the dispatcher and consumes `9873` as a selected slot/result.

### Best-fit name

- `C1:A4AA = ObjectCmd_SelectTarget_Mode00`

### `C1:A4E0`

Seeds mode `01`.

### Best-fit name

- `C1:A4E0 = ObjectCmd_SelectTarget_Mode01`

### `C1:A70A`

Seeds mode `02`.

### Best-fit name

- `C1:A70A = ObjectCmd_SelectTarget_Mode02`

### `C1:A73A`

Seeds mode `03`.

### Best-fit name

- `C1:A73A = ObjectCmd_SelectTarget_Mode03`

## Direct client outside the wrapper pattern

One useful structural detail showed up at `C1:4A00`:

that code seeds `986F/9870`, builds projected-position work in `D3..D6`, and then calls `C1:2AE3` directly instead of going through `2986`.

That proves the relation-query routines are not only reachable through the bank-C1 mode dispatcher.
They also exist as **direct reusable helpers**.

## What this pass proves

### It **does** prove

- the relation-query block is not being driven primarily by the movement integrator itself
- it is being consumed by a higher-level bank-C1 wrapper layer that reads and writes `AE/AF` command-state registers
- there are two clear client families:
  - **predicate-style wrappers** (`9260..977D`)
  - **target-selection wrappers** (`A4AA..A75F`)
- `B252 + 3` is a common subject-slot source for these calls
- the live relation-query mode range extends to **at least `0E`**

### It **does not** prove yet

- the exact user-facing script/opcode names of those wrappers
- whether the wrapper bank is best described as “AI”, “event actor logic”, or a shared object-command VM
- the exact semantics of every relation-query mode above the already decoded nearest/farthest/distance group

## Best-fit architectural conclusion

The cleanest current read is:

**`C1:2986` and friends form a shared object-relation query service, and the primary live callers are bank-C1 object-command / predicate wrappers that use it for target selection and condition testing.**

That is a much stronger answer than “some code sets 986E.”

## Best next target

The best next move is to decode the higher-level wrapper bank itself:

- identify the jump tables or command tables that enter `9260..977D` and `A4AA..A75F`
- then map those wrappers back to concrete object-command semantics
- or, alternatively, finish the undecoded relation-query modes `08..0E` from the bottom up
