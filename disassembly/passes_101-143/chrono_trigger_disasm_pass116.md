# Chrono Trigger Disassembly — Pass 116

## Purpose

Pass 115 froze the downstream sign/zero dispatcher at `C0:8A6C..8A9D`, but the eight selected bodies were still just a list of addresses.

This pass stayed on that exact seam and only promoted what the bytes justify.

---

## Biggest closure

The eight bodies selected by `C0:8A6C..8A9D` are not eight unrelated algorithms.

They are one **mirrored candidate-search system** over the current slot coordinate words, split into:

- **two X-only / `30 == 0` roots**
- **two Y-only / `2E == 0` roots**
- **four full quadrant bodies when both `2E` and `30` are nonzero**

That is the first honest closure that upgrades the working pair `2E/30` from anonymous scratch into an exact **signed candidate-offset pair**.

---

## 1. `C0:8A9E..8AB4` is the shared candidate-validator entry used by all eight branch bodies

This body is now tight enough to promote.

Byte shape:

```text
C0:8A9E  A5 68
C0:8AA0  E2 20
C0:8AA2  A5 67
C0:8AA4  20 A1 9A
C0:8AA7  90 03
C0:8AA9  A9 01
C0:8AAB  60
C0:8AAC  20 D3 9A
C0:8AAF  20 37 9C
C0:8AB2  A9 00
C0:8AB4  60
```

Exact structural behavior:

1. uses the candidate pair already staged in local `66/68` (low bytes read through `67/68`)
2. calls `C0:9AA1`
3. if that helper leaves carry clear, it immediately returns failure
4. otherwise it runs the shared classifier / prep body at `9AD3`
5. then runs the final gate at `9C37`
6. returns with the carry result from that later gate still live

What is exact about `9AA1` now:

- it masks local `67` with `1E`
- uses that as an index into `7E:70C0`
- returns **carry set** when the table byte is nonnegative
- returns **carry clear** when the table byte is negative

So the strongest safe reading is:

> **`C0:8A9E..8AB4` is the shared candidate-validator entry used by all eight later branch bodies, with an early occupancy/class-table gate through `7E:70C0[(67 & 1E)]` before the heavier `9AD3 -> 9C37` path.**

I am intentionally **not** overclaiming the final gameplay noun of the `70C0` table yet.

---

## 2. `C0:9923..99D9` is the shared quick nearby-slot rejection helper over candidate pair `66/68`

This helper is called from the branch roots before the slower shared validator.

What the bytes freeze:

- loads slot-count byte `7F:2000`
- scans slot records backward in 2-byte steps
- skips entries whose `0F00,X` byte is zero
- skips:
  - current slot `0197`
  - exact slots `0199`
  - and `019B`
- checks exact flag bit `1B01,X.bit0`
- compares the absolute deltas against the candidate pair already staged in `66/68`:
  - `abs(1880,X - 68) < 0x00E0`
  - `abs(1800,X - 66) < 0x00E0`

Carry behavior is exact:

- **carry set** when the helper rejects the candidate as too-close / conflicting
- **carry clear** when no such rejecting slot is found

That is enough to promote this helper structurally:

> **`C0:9923..99D9` is the shared quick nearby-slot rejection scan over the candidate coordinate pair in `66/68`, filtering active/exempt slots before the heavier validator path is attempted.**

---

## 3. The eight dispatcher targets collapse into axis-degenerate pairs plus four true quadrant bodies

Pass 115 already froze the dispatcher at `8A6C..8A9D`.

This pass closes the bodies it selects.

### A. `8AB5..8BC3` and `8BC4..8BF8` are the `30 == 0` / X-only families

Shared exact traits:

- start by seeding sign-marker bytes:
  - `8AB5..` clears `2F` and `31`
  - `8BC4..` seeds `2F = 0xFF`, clears `31`
- cache current slot coordinate words from:
  - `1800,X -> 62`
  - `1880,X -> 64`
- build a candidate pair in:
  - `66` on the `1800` side
  - `68` on the `1880` side
- use exact fixed bias constants:
  - `+0x0070`
  - `-0x0040`
- fold signed working byte `2E` into the `66` side
- call `9923` first
- if that quick gate accepts, clear `2E` and return
- otherwise continue through repeated `8A9E` attempts using alternate candidate placements and forced fallback seeds such as:
  - `2E = 0`
  - `30 = -0x0010`
  - `30 = +0x0010`

The cleanest safe reading is:

> these are the two mirrored **X-only candidate-search families** for the `30 == 0` case, differing only by the sign-marker seed and candidate ordering.

### B. `8BF9..8D10` and `8D11..8E20` are the `2E == 0` / Y-only families

Shared exact traits:

- start by seeding sign-marker bytes:
  - `8BF9..` seeds `31 = 0xFF`, clears `2F`
  - `8D11..` clears both `31` and `2F`
- cache current slot coordinate words from the same `1800/1880` pair
- build candidate pair `66/68`
- use fixed bias constants:
  - `-0x0070` on one side or none on the root side
  - `+0x0070` on later retries
- fold signed working byte `30` into the `68` side
- call `9923` first
- if that quick gate accepts, clear `30` and return
- otherwise continue through repeated `8A9E` attempts with alternate candidates and forced fallback seeds such as:
  - `2E = -0x0010`
  - `2E = +0x0010`
  - `30 = 0`

The strongest safe reading is:

> these are the two mirrored **Y-only candidate-search families** for the `2E == 0` case.

### C. `8E21..8EF0`, `8EF1..8FC0`, `8FC1..909B`, and `909C..916F` are the four full quadrant bodies

These are the only four roots that stage **both** working bytes into the initial candidate.

Shared exact traits:

- seed the sign-marker pair `2F/31` as one of the four exact combinations:
  - `00 / FF`
  - `FF / FF`
  - `FF / 00`
  - `00 / 00`
- cache current slot coordinate words from `1800/1880`
- build candidate pair `66/68` using **both** signed working bytes:
  - `2E` folded onto the `1800` side
  - `30` folded onto the `1880` side
- use the same fixed bias vocabulary seen in the axis-only roots:
  - `±0x0070`
  - `-0x0040`
- call `9923` first
- then retry through repeated `8A9E` validations in a mirrored order
- on success, clear the component(s) consumed by the accepted candidate and return

The strongest safe reading is:

> **these four bodies are the exact mirrored quadrant search families for the nonzero/nonzero case, with entry sign markers in `2F/31` telling the downstream shared path which quadrant ordering is active.**

---

## 4. This pass upgrades the noun of `2E/30`

Pass 115 proved:

- `2A -> 2E`
- `2B -> 30`
- later helpers at `88ED..8A69` write signed coarse/fine step values and shift the pair

Pass 116 adds the missing downstream proof:

- the eight search bodies add `2E` on the exact `1800` coordinate side
- and add `30` on the exact `1880` coordinate side
- to build candidate pair `66/68`
- then validate those candidates

That is now enough to upgrade the working-pair read:

> **`2E/30` are not just later working bytes; they are the signed candidate-offset pair used by the exact mirrored candidate-search family selected at `8A6C..8A9D`.**

I am still intentionally avoiding a fake-final noun like “jump vector,” “knockback vector,” or “spawn offset” until the enclosing caller at `8820..8857` and its downstream `9175 / 99DE / 91AC / 93E1` pipeline are frozen.

---

## 5. What this pass does **not** overclaim

I am intentionally **not** freezing:

- the exact gameplay noun of the `7E:70C0` table
- the final player-facing noun of the whole `8820..8857` entry routine
- the final semantics of the sign-marker bytes `2F/31`
- the full meaning of the fixed bias constants `0x70`, `0x40`, and `0x100`

But the branch-family structure itself is no longer fuzzy.

---

## Clean carry-forward wording

Carry this wording forward exactly:

- `C0:8A9E..8AB4` = shared candidate-validator entry with early `7E:70C0[(67 & 1E)]` gate before `9AD3 -> 9C37`
- `C0:9923..99D9` = shared quick nearby-slot rejection scan over candidate pair `66/68`
- `C0:8AB5..916F` = exact mirrored candidate-search family over current slot `1800/1880` coordinates and signed working pair `2E/30`
- `2E/30` = signed candidate-offset pair in the later search lane

---

## Honest next seam

Now that the eight bodies are structurally frozen, the smallest honest live seam is the **whole enclosing solver entry**:

- `C0:8820..8857`
- `C0:9175..91AB`
- `C0:99DE..9A1E`
- `C0:91AC..93E0`
- `C0:93E1..`

That is where the final gameplay-facing noun of this entire lane now lives.
