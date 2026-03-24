# Chrono Trigger Disassembly — Pass 114

## Purpose

Pass 113 froze the exact VM ownership of the `0xC0 / 0xC3 / 0xC4` two-byte initializer family, but it still left three honest gaps:

1. the exact earlier sibling family at opcodes `0xBB / 0xC1 / 0xC2`
2. the exact stream-loader feeding local bytes `2B / 2C / 2D`
3. the first exact downstream consumer edge for the locally seeded `2A / 2B / 2D` state

This pass stayed on that seam and only promoted what the bytes justify.

---

## 1. `0xB8`, `0xBB`, `0xC1`, and `0xC2` are exact VM opcode entries in the same local family

The same master VM table rooted at `C0:5D6E` contains these exact entries:

- opcode `0xB8` -> `C0:3557`
- opcode `0xBB` -> `C0:3570`
- opcode `0xC1` -> `C0:35B5`
- opcode `0xC2` -> `C0:35FC`

So the `3557..3642` neighborhood is not “adjacent helper fog.”
It is an exact earlier sibling band of the same VM family already proven for `0xC0 / 0xC3 / 0xC4`.

That closes the entry side cleanly enough to promote.

---

## 2. `C0:3557..356F` is the exact three-byte VM stream loader for local `2B / 2C / 2D`

The body is byte-exact:

```text
C0:3557  BB
C0:3558  E8
C0:3559  BF 01 20 7F
C0:355D  85 2B
C0:355F  E8
C0:3560  BF 01 20 7F
C0:3564  85 2C
C0:3566  E8
C0:3567  BF 01 20 7F
C0:356B  85 2D
C0:356D  BB
C0:356E  38
C0:356F  60
```

Exact behavior:

1. treats `Y` as the script-stream cursor through `TYX`
2. reads three successive bytes from `7F:2001+X`
3. stores them exactly as:
   - first byte -> local `2B`
   - second byte -> local `2C`
   - third byte -> local `2D`
4. returns through `TYX ; SEC ; RTS`

This pass does **not** overclaim the final human-facing noun of that three-byte triplet.
But it now proves the exact ownership and write order cleanly.

The strongest safe reading is:

> **`C0:3557..356F` is the exact three-byte VM stream loader for the local `2B / 2C / 2D` triplet that later gates and parameterizes the same `0xBB / 0xC1 / 0xC2 / 0xC0 / 0xC3 / 0xC4` family.**

---

## 3. `C0:3570..35B4`, `C0:35B5..35FB`, and `C0:35FC..3642` are exact one-byte mode-`0 / 1 / 2` siblings of the later two-byte family

These three handlers have the same front shape as the pass-113 `0xC0 / 0xC3 / 0xC4` bodies.

### A. Common front gate

All three begin by reading local `2D` and taking the local path only when it is nonzero:

```text
A5 2D
D0 06
A2 E0 7F
82 ....   -> exact target C0:2E1E
```

So all three share the same exact external fallback target:
- when `2D == 0` -> branch to `C0:2E1E`
- when `2D != 0` -> continue locally

### B. Local fast-exit gate

All three then check local `29` and return early when it is already nonzero.

### C. Vacant-slot path

If local `29 == 0`, the handler loads slot index `X = 6D` and inspects exact long byte `7F:0A00,X`.

When that slot byte is zero, the three handlers do this:

- `3570`:
  - write `01` to `7F:0A00,X`
  - first stream byte -> `2A`
  - `2E = 6D`
  - `32 = 0`
  - `29 = 1`
  - `30 = 0`
  - `54 |= 0x20`
  - return with carry clear

- `35B5`:
  - same exact body, except `30 = 1`

- `35FC`:
  - same exact body, except `30 = 2`

The exact byte bodies prove this is a **one-byte** sibling family:
they seed `2A` from one stream byte and do **not** touch the pass-113 `62 / 64 / 65 / 66` lane.

### D. Occupied-slot retire path

When `7F:0A00,X` is already nonzero, all three follow the same smaller retire path:

```text
A9 00
9F 00 0A 7F
BB
E8
E8
38
60
```

Exact behavior:

1. clears exact long slot byte `7F:0A00,X`
2. returns through `TYX ; INX ; INX ; SEC ; RTS`

This pass intentionally does **not** promote a broader noun for that slot byte yet.

The strongest safe reading is:

> **opcodes `0xBB / 0xC1 / 0xC2` are exact one-byte mode-`0 / 1 / 2` overwrite-or-vacant-slot handlers. They are the narrower siblings of pass 113’s two-byte `0xC0 / 0xC3 / 0xC4` family: same gate shape, same mode byte `30 = 0/1/2`, but only one stream parameter byte (`2A`) and no `62/64/65/66` materialization.**

---

## 4. `C0:20F0..2126` is the first exact downstream packet builder consuming `2A / 2B / 2D`

This is the strongest new consumer edge in the pass.

The byte body is:

```text
C0:20F0  20 60 A5
C0:20F3  A5 2A
C0:20F5  8D 0C 02
C0:20F8  A5 54
C0:20FA  89 20
C0:20FC  F0 0A
C0:20FE  A2 00 FF
C0:2101  8E 0D 02
C0:2104  A9 DE
C0:2106  80 07
C0:2108  A6 2B
C0:210A  8E 0D 02
C0:210D  A5 2D
C0:210F  8D 0F 02
C0:2112  A2 00 F0
C0:2115  8E 10 02
C0:2118  A9 7E
C0:211A  8D 12 02
C0:211D  A9 00
C0:211F  8D 14 02
C0:2122  22 03 00 C2
C0:2126  60
```

Exact behavior after the front `JSR $A560`:

1. copies local `2A -> 020C`
2. tests local `54.bit5` (`BIT #$20`)
3. if `54.bit5 == 1`:
   - writes `FF00 -> 020D`
   - writes `DE -> 020F`
4. if `54.bit5 == 0`:
   - writes local `2B -> 020D`
   - writes local `2D -> 020F`
5. writes the fixed pointer half:
   - `0210 = F000`
   - `0212 = 7E`
   - `0214 = 00`
6. calls exact external veneer `JSL C2:0003`
7. returns

That ties this local VM family directly into the already-frozen pass-92/pass-93 `020C..0214 -> C2:0003` stream-state initializer lane.

The strongest safe reading is:

> **`C0:20F0..2126` is an exact local packet builder that turns the family’s seeded local bytes into the `020C..0214` C2 stream-init packet. It always copies `2A -> 020C`, conditionally uses either `2B/2D` or the exact forced override pair `FF00 / DE`, then launches the known `C2:0003` stream-state initializer veneer.**

---

## 5. What materially changed in this pass

This pass does four real things:

1. it proves `0xB8` is the exact triplet loader for `2B / 2C / 2D`
2. it closes `0xBB / 0xC1 / 0xC2` as the **one-byte** siblings of the pass-113 two-byte family
3. it proves all six handlers share the same exact external fallback target `C0:2E1E` when `2D == 0`
4. it closes the first exact downstream consumer edge for the family’s locally seeded operand bytes through `C0:20F0..2126`

What it still does **not** do:

- freeze the first exact consumer of local mode byte `30`
- freeze the final noun of `7F:0A00/0A80`
- freeze the exact role of `2C` beyond “middle byte of the exact `3557` stream triplet”

Those are still live seams.

---

## Honest next seam after this pass

The cleanest continuation target is now:

1. the exact external fallback body at `C0:2E1E..`
2. the first exact reader/consumer of local `30`
3. the first exact consumer edge of local `2C`

That is a smaller, more honest seam than what pass 113 started with.
