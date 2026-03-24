# Chrono Trigger Disassembly — Pass 94

## What I targeted
Pass 93 finally turned `C2:0003`, `C2:0009`, and `C7:0004` into exact veneers / dispatch stages.

That left two clean follow-ups:

- freeze the first real downstream C2 family instead of leaving `58B2 / 5BF5 / 5C3E / 5C77` as anonymous targets
- freeze the first real C7 packet-family bodies so `C7:0140` stops sounding like a generic low-bank packet router

I stayed on those two seams.

---

## Strongest keepable result
The biggest real upgrade this pass is not just another helper label.

It is this:

> the `C7:0140` packet system is now clearly the **APU / sound-command side**, not a generic low-bank packet system.

That is now justified by exact downstream behavior:

- the `0x70` family at `C7:08E3` performs exact handshake traffic through **`$2140`** and repeated command/data writes through **`$2141/$2142/$2143`**
- the `0x71` family at `C7:0755` also performs repeated exact **`$2141/$2142/$2143`** burst writes and terminates through the same common dispatcher exit
- the `0x10..0x17` gate table at `C7:0AD9` is now exact and no longer abstract

That means the noun upgrade is real:

- `1E00..` is best read as a **sound/APU command packet workspace**
- `C7:0140` is best read as a **sound-command opcode-family dispatcher into APU-port handlers**

This is a semantic step forward, not a cosmetic rewrite.

---

## 1. `C2:584A` is the pre-dispatch substate gate

Pass 93 already proved `C2:5823` calls exact local helper `JSR $584A` before it looks at `0230`.

Pass 94 freezes what `584A` really is.

It does this exactly:

- loads `0215`
- doubles it
- uses exact indexed indirect jump `JMP ($5851,X)`

So `584A` is not a calculation helper.
It is a **pure substate jump gate** driven by `0215`.

The jump table is heavily repetitive and collapses to a small set of exact outcomes:

- `5893` = `SEC ; RTS`
- `5895` = immediate clear-carry continue path (`BRA` into `CLC ; RTS`)
- `5897` / `589B` are two entry points into the same seed/update body that:
  - seeds `0234` with `08` or `14`
  - clears `0217`
  - conditionally subtracts `08` from `0234` when `(0214 & 0x0F) == 0x02`
  - returns with clear carry

So the strongest safe reading is:

> `C2:584A..58B1` is the exact `0215`-driven pre-dispatch substate gate that either exits early via carry or prepares the local `0234/0217` state and returns “continue”.

That tightens the entry contract of `5823` a lot.

---

## 2. `C2:58B2` is the first real stream-token consumer / primary token-family dispatcher

This is the first downstream C2 family worth freezing.

The exact opening behavior is strong:

- reads the next byte through direct-indirect pointer `[0231]`
- increments the live stream pointer at `0231`
- then splits on the token value

The split is exact enough to keep:

### A. `token >= 0xA0`
- stores the token into `0235`
- calls exact local helper `JSR $5DC4`
- decrements `0213`
- loops this path while `0213` remains nonzero
- then sets `0215 = 0x10` and returns

### B. `0x21 <= token < 0xA0`
- stores the raw token into `023B`
- converts `(token - 0x21)` into an index into the exact long table rooted at **`DE:FA00`**
- seeds `0237/0239/023A` from that table family
- sets `0230 = 0x01`
- jumps directly into `5BF5`

### C. `token < 0x21`
- uses the token as a direct local dispatch index
- jumps through the exact local jump table rooted at `5903`

So the strongest safe reading is now:

> `C2:58B2..5902` is the exact primary stream-token consumer that advances `[0231]` and dispatches the next token into three concrete token families: `>=A0`, `0x21..0x9F`, and `0x00..0x20`.

I am still **not** freezing the final gameplay-facing noun of the broader C2 stream language yet.
But `58B2` is no longer anonymous.

---

## 3. `C7:0192` is the common dispatcher exit / cleanup epilogue

The `0x10..0x17` family table made this worth freezing.

`C7:0192..01A0` is now exact:

- `SEP #$20`
- `STZ $00`
- `REP #$20`
- `REP #$10`
- restore `Y`, `X`, `A`, flags, direct page, and bank
- `RTL`

So `0192` is not a real content handler.
It is the common **dispatcher exit / cleanup epilogue**.

That matters because part of the `0x10..0x17` table lands directly here.

---

## 4. `C7:0AD9` is the exact `0x10..0x17` gate table

The first eight 16-bit entries at `C7:0AD9` are now exact and keepable.

They map packet opcodes `0x10..0x17` like this:

- `0x10 -> 01A1`
- `0x11 -> 01A1`
- `0x12 -> 0192`
- `0x13 -> 0192`
- `0x14 -> 01A1`
- `0x15 -> 01A1`
- `0x16 -> 0192`
- `0x17 -> 0192`

That is important because it proves the early family gate is not eight fully distinct handlers.
It is a **two-target gate**:

- active handler path = `01A1`
- immediate cleanup / no-work path = `0192`

That is a real structural closure.

---

## 5. `C7:0755` is an exact table-driven APU triplet burst sender

This is the first exact body behind opcode `0x71`.

I am intentionally not pretending to have the final audio-engine noun yet,
but the hardware-facing behavior is now exact enough to freeze structurally.

Exact keepable behavior:

- checks exact per-slot/state byte at `1E20`
- if that state is active and `1E01 == 0`, exits through `0192`
- otherwise computes `(1E01 - 1) * 3`
- uses that as an index into the exact table rooted at **`C7:0AEA`**
- then performs repeated **three-byte burst writes** through:
  - `$2141`
  - `$2142`
  - `$2143`
- performs exact fixed follow-up command writes including:
  - `2141 = 0x05`
  - later `2141 = 0x02` paired with exact `2142/2143` values
- ends by caching the current `1E01` value into the per-slot strip at `1E20 + X`
- then exits through the common cleanup path at `0192`

So the strongest safe reading is:

> `C7:0755..08E2` is the exact opcode-`0x71` table-driven APU burst sender / uploader over the `1E00..` sound-command workspace.

That is already much stronger than “some low-bank packet body.”

---

## 6. `C7:08E3` is the exact opcode-`0x70` APU handshake + packet sender

This is the second key downstream body.

Again, I am staying one notch below over-claiming the final audio-engine noun.
But the hardware-side behavior is now too concrete to ignore.

Exact keepable behavior:

- reads `1E01`
- compares against the latched pair at `1E10/1E11`
- on mismatch, performs exact handshake traffic through **`$2140`** using `0xFE`
- later uses exact handshake/reset writes through the same port with `0xE0`
- writes repeated command/data triplets through **`$2141/$2142/$2143`**
- selects exact command byte `0x05` when `1E00 == 0x70`
- otherwise uses the alternate command byte `0x03` on the shared internal path
- sources repeated triplet payloads from exact C7 tables rooted at:
  - `C7:430B`
  - `C7:5B0D`
- clears exact local latch byte `F3` before returning in the table-send paths

So the strongest safe reading is:

> `C7:08E3..09D8` is the exact opcode-`0x70` APU handshake / packet-send handler behind the `1E00` sound-command dispatcher.

This is enough to promote the subsystem noun.

---

## 7. What changed semantically

Before pass 94, the C7 side still sounded like this:

```text
low-bank packet dispatcher
```

After pass 94, the safe wording is materially better:

```text
low-bank sound/APU command dispatcher over the 1E00 packet workspace,
with exact downstream APU-port handlers for opcode families 0x70 and 0x71
```

That is not a tiny edit.
It closes an actual ambiguity.

---

## Honest caution
I am still keeping a few things below frozen:

- the final gameplay-facing noun of the broader C2 stream language behind `58B2 / 5BF5 / 5C3E / 5C77`
- the exact end-user meaning of each opcode family in the C7 sound/APU command set
- the first exact clean-code external reader of `CE0F`

But pass 94 absolutely does move the project forward:

- `C2:58B2` is no longer anonymous
- `C7:0140` is no longer “generic packet dispatcher” fog
- the sound/APU side now has exact, hardware-facing proof

---

## Best next seam
The best next move is now:

1. **Finish the C2 downstream family pass cleanly**
   - `5BF5`
   - `5C3E`
   - `5C77`

2. **Tighten the active `0x10/11/14/15` C7 path at `01A1`**
   - it is now isolated from the no-work exit at `0192`

3. **Only then go back to `CE0F`**
   - the engine-facing noun wall is cleaner now than it was before pass 94
