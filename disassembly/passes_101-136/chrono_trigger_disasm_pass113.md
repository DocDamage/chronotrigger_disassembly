# Chrono Trigger Disassembly — Pass 113

## Purpose

Pass 112 froze the local writer mechanics for `7E:0163/0164/0165/0166`, but it still left two honest gaps:

1. the exact caller/entry chain that seeds `64/65` from the packed `7F:2001+X` stream byte
2. the first exact consumer path of saved byte `66`

This pass stayed on that seam and only promoted what the bytes justify.

---

## 1. `3643 / 36AA / 36DD` are real VM opcode entries, not random local helpers

The main low-bank VM table rooted at `C0:5D6E` contains these exact entries:

- opcode `0xC0` -> `C0:3643`
- opcode `0xC3` -> `C0:36AA`
- opcode `0xC4` -> `C0:36DD`

The same local cluster also contains nearby exact sibling entries:

- opcode `0xBB` -> `C0:3570`
- opcode `0xC1` -> `C0:35B5`
- opcode `0xC2` -> `C0:35FC`

So the `36xx` seam is no longer just “some nearby local state helper band.”
It lives inside the same `7F:2001` slot/object VM already proven in earlier passes.

That closes the caller/entry side cleanly enough to promote.

---

## 2. `C0:3674..36A8` is the exact shared two-byte initializer reached from opcodes `0xC0 / 0xC3 / 0xC4`

The body is now exact:

```text
C0:3674  A9 01
C0:3676  9F 00 0A 7F
C0:367A  BB
C0:367B  E8
C0:367C  BF 01 20 7F
C0:3680  85 2A
C0:3682  E8
C0:3683  BF 01 20 7F
C0:3687  85 D9
C0:3689  29 03
C0:368B  85 65
C0:368D  A5 D9
C0:368F  4A
C0:3690  4A
C0:3691  29 03
C0:3693  85 64
C0:3695  A9 01
C0:3697  85 62
C0:3699  A5 6D
C0:369B  85 2E
C0:369D  64 32
C0:369F  A9 01
C0:36A1  85 29
C0:36A3  A9 20
C0:36A5  14 54
C0:36A7  BB
C0:36A8  18
C0:36A9  60
```

Exact behavior:

1. writes `01` to exact long slot byte `7F:0A00,X`
2. treats `Y` as the script-stream cursor (`TYX`), then consumes **two successive bytes** from `7F:2001+X`
3. first stream byte -> local `2A`
4. second stream byte -> local scratch `D9`
5. exact packed split from that second byte:
   - `65 = (byte & 0x03)`
   - `64 = ((byte >> 2) & 0x03)`
6. sets `62 = 1`
7. copies `6D -> 2E`
8. clears `32`
9. sets `29 = 1`
10. sets bit `0x20` in local byte `54`
11. returns through `TYX ; CLC ; RTS`

The strongest safe reading is:

> **`C0:3674..36A8` is the exact shared two-byte VM stream initializer for the `0xC0 / 0xC3 / 0xC4` handler family. It arms the local `62/64/65` state from two immediate stream bytes and marks one exact `7F:0A00+slot` byte active.**

---

## 3. Strong correction to pass 112: the packed-byte split is `bits0..1 -> 65` and `bits2..3 -> 64`

Pass 112 correctly identified the packed-byte materialization site, but the wording was slightly too loose.

The exact extraction is:

- `65 = packed & 0x03`
- `64 = (packed >> 2) & 0x03`

So `64` is **not** “the high 2 bits of the full byte.”
It is the **next 2-bit field** (`bits 2..3`) of the same packed byte.

That correction matters because it is now byte-exact enough to freeze the stream format honestly.

---

## 4. `C0:3643..3670`, `C0:36AA..36DC`, and `C0:36DD..370D` are three exact overwrite/retire-or-init variants with mode bytes `0 / 1 / 2`

These three opcode handlers have the same core shape.

### A. Common front gate

Each begins by reading local `2D`:

```text
A5 2D
D0 06
A2 E0 7F
82 ....
```

So the local path is taken only when `2D != 0`.
When `2D == 0`, control diverts to an earlier external helper via `LDX #$7FE0 ; BRL ...`.

### B. Local fast-exit gate

Each then checks local `29` and returns early when it is already nonzero.

### C. Vacant-slot path

If local `29 == 0`, the handler loads exact slot index `X = 6D` and inspects `7F:0A00,X`.
When that slot byte is zero, the handlers do this:

- `3643` -> set `30 = 0`, then branch into shared initializer `3674`
- `36AA` -> set `30 = 1`, then branch into shared initializer `3674`
- `36DD` -> set `30 = 2`, then branch into shared initializer `3674`

So these are not three unrelated bodies.
They are exact mode variants feeding the same shared two-byte initializer.

### D. Occupied-slot retire / overwrite path

When `7F:0A00,X` is already nonzero, all three handlers follow the same exact overwrite tail:

```text
A9 00
9F 00 0A 7F
A5 66
9F 80 0A 7F
64 62
BB
E8
E8
E8
38
60
```

Exact behavior:

1. clears exact long slot byte `7F:0A00,X`
2. writes saved local byte `66 -> 7F:0A80,X`
3. clears `62`
4. returns through `TYX ; INX ; INX ; INX ; SEC ; RTS`

That is the first exact consumer side of `66`.

The strongest safe reading is:

> **opcodes `0xC0 / 0xC3 / 0xC4` are exact three-mode overwrite/retire-or-init handlers. On a vacant slot they seed mode `30 = 0/1/2` and enter shared initializer `3674`; on an occupied slot they retire the current state by clearing `7F:0A00+slot`, persisting `66` into `7F:0A80+slot`, clearing `62`, and returning with carry set.**

---

## 5. `66` is now proven to be persisted outward, not just saved locally

Pass 112 froze the save side:

- `1AFB..1B18` saves prior live `63 -> 66` before forcing `63 = 4`

This pass closes the first exact downstream consumer edge:

- the occupied-slot overwrite tails in `3643 / 36AA / 36DD` write `66 -> 7F:0A80,X`

So the honest upgrade is:

- `66` is not just a temporary local save byte
- it is a saved selector value that is later **persisted back out into exact slot state** on the overwrite/retire path

I am still **not** claiming the full high-level subsystem noun of that `7F:0A00/0A80` slot pair yet, because earlier render/anchor evidence in that neighborhood still deserves caution.
But the local consumer edge for `66` is now exact.

---

## 6. `62` is now tight enough to strengthen, but not fully rename

This pass adds exact state transitions for local byte `62`:

- shared initializer `3674` forces `62 = 1`
- occupied-slot overwrite tails force `62 = 0`
- earlier pass-112 context already showed an exact `62 = 3` writer at `1AF8`

So `62` is no longer “mystery nearby local.”
It is clearly a **multi-state local control byte** inside the same `62/63/64/65/66` family.

What I still did **not** freeze:
- the cleanest final human-readable subsystem noun for `62`
- whether state `3` is best described as suspend, forced-default, or some narrower mode name

---

## What this pass materially changes

This pass does three real things:

1. it proves the `64/65` packed-byte seeding path belongs to exact VM opcodes `0xC0 / 0xC3 / 0xC4`
2. it corrects the packed-field wording from pass 112 into a byte-exact split
3. it closes the first exact external persistence/consumer edge for saved byte `66`

That is enough to move this seam from “tight local mechanics” to “tight local mechanics with exact VM ownership and one exact downstream persistence path.”
