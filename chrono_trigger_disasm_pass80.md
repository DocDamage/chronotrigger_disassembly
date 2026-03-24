# Chrono Trigger Disassembly — Pass 80

## Scope of this pass
This pass continues directly from the pass-79 seam.

Pass 79 proved that the optional `CD:0018` side is not a generic blob at all:

- `CA32..` are two active runtime slots
- `15D5` expands descriptor ids into those slots
- `1609` ticks them and interprets stream bytes
- `16B5..` is the big command-token dispatch table for bytes `>= 0x80`

The ugly gap left open was that the token system still had no concrete sub-families.
This pass closes the first real chunk of that gap.

The honest result is:

> the auxiliary descriptor stream is a **small command VM**,
> not a vague “fragment stage”.
>
> Raw bytes `< 0x7F` feed the late graphics path by deriving a `D0`-side tile-block source pointer,
> `0x7F` is a dedicated advance token,
> and a real set of high tokens now reads cleanly as
> **absolute writes, indexed table-copy, conditional rewind, repeat loops, and paired-delta operators**.

I still do **not** claim the full end-to-end player-facing noun of every emitted object, but the optional auxiliary stage is now much more obviously a scripted graphics/tile-support VM.

---

## 1. `1654` is one-token interpreter logic, not just a fetch helper
Pass 79 already proved that `1654` pulls one byte from the current active slot stream and branches three ways:

- `< 0x7F`
- `== 0x7F`
- `>= 0x80`

This pass tightens all three branches.

### 1a. `0x7F` is an exact one-byte stream-advance token
That branch is tiny and exact:

```text
C2 20
A5 40
1A
9D 35 CA
7B
E2 20
```

So `0x7F` just increments the current slot stream pointer at `CA35,X` by one and returns to the scheduler.
It is not a data-emission token and not a command-dispatch token.
It is a dedicated **advance / skip-next-byte token**.

### 1b. raw data tokens `< 0x7F` derive a `D0`-side tile-block pointer
The raw-data branch does:

```text
CLC
ADC $CA3A,X
REP #$20
XBA
ASL
CLC
ADC #$D000
STA $CA18
...
INC $CA17
```

The safest strong reading is:

- the token value is biased by the slot-local byte at `CA3A,X`
- the result is promoted into a `D0`-side, tile-block-shaped source pointer rooted at `D000`
- that pointer is stored in `CA18`
- and `CA17` is incremented to signal a pending request

I am deliberately stopping one notch below overclaiming the exact final codec noun here.
But the important structural upgrade is clear:

> raw bytes in the auxiliary stream are **not abstract markers**.
> They select a `D0`-side graphics/tile source block for later consumption.

That lines up with the pass-79 proof that the late service-04 seam is tile-oriented.

### 1c. command bytes `>= 0x80` are dispatched by low-7-bit token id
The command path calls `16A6`, whose whole job is:

1. preserve the current slot base in `$43`
2. advance the stream pointer by one byte
3. dispatch through `16B5` using the command byte’s low 7 bits

So `0x80..0xFF` is a **128-command token namespace**, with `0x80` mapped to table index `0`, `0x81` to `1`, and so on.

That turns the optional auxiliary descriptor stage into a real little **stream-script VM**.

---

## 2. `16B5..17A6` is now a real command-token table, not just “big dispatch junk”
Pass 79 already froze the table role.
This pass tightens the first important command families.

### 2a. token `0x80` is a 32-way secondary sub-dispatch
Token `0x80` lands at `2A4A`, whose body is:

```text
LDA [$40]
ASL
TAX
JMP ($2A51,X)
```

So the very first command token is not a single action at all.
It is a **secondary 32-way sub-opcode dispatcher** keyed by the following stream byte.

That is a real architecture clue:

> the auxiliary stream language has at least one “extended/meta” command family,
> not just flat one-command-per-token behavior.

### 2b. token `0x81` is the slot countdown seed token
Token `0x81` lands at `2DCB`:

```text
A6 43
A7 40
9D 38 CA
9D 39 CA
RTS
```

So it writes the same immediate byte into both:

- `CA38,X` = reload value
- `CA39,X` = current countdown

That gives an exact noun:

> token `0x81` seeds the slot’s **reload + current countdown pair**.

### 2c. token `0x82` is an 8-way paired-delta operator over `CA5E/60`
Token `0x82` lands at `2DD6`.
Its immediate byte splits into:

- low 5 bits + 1 = magnitude
- high 3 bits = sub-op selector

and dispatches through the local 8-entry table at `2DEA`.
Those eight sub-ops are exact paired add/subtract variants over the two 16-bit fields at:

- `CA5E,X`
- `CA60,X`

The eight behaviors are the full sign-combination family:

- first `+`, second `-`
- second `-`
- both `-`
- first `+`
- first `-`
- both `+`
- second `+`
- first `-`, second `+`

The safest strong reading is:

> token `0x82` applies one of eight **paired 16-bit delta transforms** to the slot-local `CA5E/60` accumulator pair.

This is one of the best upgrades in the pass because it finally gives a concrete role to part of the old fuzzy `CA52..` family.

### 2d. tokens `0x83/0x84/0x85/0x86` are repeat-loop control
These four tokens form a clean family.

#### token `0x83` at `2EA2`
Seeds:

- `CA72,X` = loop resume pointer
- `CA74,X` = repeat count = immediate + 1

#### token `0x84` at `2EB5`
Decrements `CA74,X` and either:

- rewinds `$40` back to `CA72,X` while repeats remain
- or consumes one extra byte and falls through once the repeat count is exhausted

#### token `0x85` at `2EC8`
Same basic seed as `0x83`, but also clears `CA3A,X`.

#### token `0x86` at `2EDE`
Same basic loop as `0x84`, but while looping it increments `CA3A,X`, and on termination it clears `CA3A,X` before consuming the final trailing byte.

So this family is now exact enough to state plainly:

> `0x83..0x86` are the auxiliary stream’s **repeat/rewind loop-control tokens**,
> with `0x85/0x86` adding an iteration counter or base-bias side effect through `CA3A`.

That is a real VM feature, not just random state mutation.

---

## 3. the high `F*` tokens finally read like real control opcodes
The last chunk of the table is packed with small, exact handlers.
These are now much tighter.

### 3a. token `0xF9` at `17A9` = immediate byte write to absolute target
The body:

1. reads one immediate byte from the stream
2. reads the next two bytes as the absolute destination address
3. writes the immediate byte to that address

So `0xF9` is an exact **write-immediate-byte-to-absolute-target** token.

### 3b. token `0xF8` at `17BE` = indexed 2-word record copy through `$2000/$2200`
This token:

- takes one immediate index byte
- takes one destination index byte
- copies one 2-word record from:
  - `$2000 + 2*src`
  - `$2200 + 2*src`
- into the matching destination index

So `0xF8` is a clean **indexed 2-word pair copy token**.

### 3c. tokens `0xF6` and `0xF2` are conditional rewind-by-immediate controls
These two bodies are structurally the same:

- read an immediate byte
- if the corresponding latch is clear/nonzero as required
- subtract that immediate from the stream pointer
- then clear the latch

The only difference is the latch family:

- `0xF6` uses `CE10`
- `0xF2` uses `CD44`

So these are real **one-shot conditional rewind tokens**.

### 3d. token `0xF3` seeds that rewind latch
Token `0xF3` stores the immediate byte to `CD45` and increments `CD44`.
That makes it the obvious sibling/controller for the `0xF2` rewind path.

### 3e. token `0xF7` and `0xF5` are direct immediate staging writes
These are tiny, exact handlers:

- `0xF7` stores the immediate byte to `CE0E`
- `0xF5` stores the immediate byte to `CD46`

I am intentionally keeping the final gameplay noun of those staging bytes open, but the token mechanics are exact.

### 3f. token `0xF1` writes stage/global byte `5D8F` into the slot-local `CAA4` family
This token is also tiny and exact:

```text
A7 40
TAX
LDA $5D8F
STA $CAA4,X
RTS
```

So `0xF1` copies the current stage/global byte at `5D8F` into one indexed `CAA4` slot-local field.

### 3g. token `0xF0` is an exact JSL wrapper
Token `0xF0` is just:

```text
JSL D1:EFD0
RTS
```

So it is a pure wrapper token that invokes a D1-side helper.
The final noun of that helper is still open, but the token role is exact.

---

## 4. This pass tightens the fuzzy `CA52..` and `CA72..` families
The old caution from pass 79 was that `CA52 / CA72` still had no tight field nouns.
This pass does not solve every byte, but it does solve the first real layer.

### 4a. `CA72 / CA74` are repeat-loop state, not generic scratch
The `0x83..0x86` family proves:

- `CA72,X` = loop resume pointer
- `CA74,X` = repeat countdown

for the active auxiliary runtime slot.

### 4b. `CA5E / CA60` are paired 16-bit auxiliary accumulators
The `0x82` family proves that these are two independent 16-bit fields that the stream can update through signed-style paired add/subtract transforms.

That is not enough to freeze “x/y”, “min/max”, or “left/right” yet.
But it is enough to stop calling them generic scratch bytes.

### 4c. `CA3A` is the bias / iteration side-effect byte for the stream VM
This byte now has two exact uses:

- data tokens `< 0x7F` add it before deriving the `D0`-rooted tile-block pointer
- loop token `0x86` increments it per iteration and clears it on termination

So `CA3A` is not random either.
It is a real **slot-local stream bias / iteration byte**.

### 4d. `CA17 / CA18` are the pending/current auxiliary tile-block request state
Because the raw-data path stores a `D0`-side pointer into `CA18` and increments `CA17`, those bytes are now much tighter as:

- `CA17` = pending auxiliary tile-block request count/flag
- `CA18` = current derived `D0` tile-block source pointer

Again, I am intentionally stopping below a fake-perfect noun.
But this is materially beyond “unknown scratch.”

---

## 5. What changed architecturally
Before this pass, the optional `CD:0018` side could still be mistaken for some vague pre-decode side blob.

That is much harder to justify now.

The optional auxiliary descriptor stage is a real **stream-script VM** with at least these feature classes:

- raw tile-block selection into the `D0` graphics path
- one-byte advance tokens
- repeat/rewind loop control
- absolute memory writes
- indexed table-copy
- paired accumulator transforms
- direct D1-side helper calls
- an extended/meta `0x80` sub-op family

That still does **not** solve every high token and still does **not** fully freeze the final player-facing noun of the downstream `4500.. -> 5D00..` emit family.

But the auxiliary stage is now clearly **scripted graphics/tile support logic**, not generic noise.

---

## 6. Honest remaining gaps
I did **not** finish the whole `0x80..0xFF` table.

Still open after this pass:

- the exact 32 sub-ops under token `0x80`
- the final gameplay-facing noun of the `4500.. -> 5D00.. -> A07B` family
- the exact player-facing noun of the paired `CA5E / CA60` accumulators
- the exact nouns of the `CD44/CD45/CD46` and `CE0E/CE10` latch bytes
- the full role of the D1-side helper calls reached by `0xF0` and `0xF4`

The important part is that the seam is smaller now.
The next good move is not “decode random code somewhere else.”
It is:

1. finish the `0x80` sub-dispatch at `2A51`
2. finish the surrounding `0x88..0x9F` command families
3. then re-open `4943 / 4500 / 5D00 / A07B` with this cleaner auxiliary-script proof in hand
