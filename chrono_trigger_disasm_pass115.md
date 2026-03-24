# Chrono Trigger Disassembly — Pass 115

## Purpose

Pass 114 finished the exact `0xB8 / 0xBB / 0xC1 / 0xC2` VM family edges, but it still left three honest gaps:

1. the exact external fallback body at `C0:2E1E..`
2. the first exact downstream reader of local `30`
3. the first exact downstream role of local `2C`

This pass stayed on that seam and only promoted what the raw bytes justify.

---

## 1. `C0:2E1E..2E65` is the exact forced-blank error-color hang path used by the VM family’s invalid fallback

Pass 114 already proved that all six related handlers branch to the same exact target when local `2D == 0`:

- `C0:3577 -> BRL C0:2E1E`
- `C0:35BC -> BRL C0:2E1E`
- `C0:3603 -> BRL C0:2E1E`
- `C0:364A -> BRL C0:2E1E`
- `C0:36B1 -> BRL C0:2E1E`
- the same family shape continues in the nearby two-byte siblings

What this pass froze is the body itself.

The byte body is:

```text
C0:2E1E  78
C0:2E1F  A9 00
C0:2E21  48
C0:2E22  AB
C0:2E23  A9 80
C0:2E25  8D 00 21
C0:2E28  A9 00
C0:2E2A  8D 00 42
C0:2E2D  8D 0B 42
C0:2E30  8D 0C 42
C0:2E33  8D 28 01
C0:2E36  8D 2C 21
C0:2E39  8D 2D 21
C0:2E3C  8D 21 21
C0:2E3F  C2 20
C0:2E41  8A
C0:2E42  E2 20
C0:2E44  8D 22 21
C0:2E47  EB
C0:2E48  8D 22 21
C0:2E4B  A9 40
C0:2E4D  8D 04 05
C0:2E50  A9 40
C0:2E52  8D 00 05
C0:2E55  A9 0F
C0:2E57  8D 19 01
C0:2E5A  A9 81
C0:2E5C  8D 00 42
C0:2E5F  A9 0F
C0:2E61  8D 00 21
C0:2E64  58
C0:2E65  80 FE
```

Exact behavior:

1. `SEI`
2. force DBR to bank `00`
3. write `0x80 -> $2100` to force blank
4. zero:
   - `$4200`
   - `$420B`
   - `$420C`
   - exact mirror byte `0128`
   - `$212C`
   - `$212D`
   - `$2121`
5. copy 16-bit `X` into CGRAM data port `$2122/$2122`
6. write `0x40 -> 0504`
7. write `0x40 -> 0500`
8. write `0x0F -> 0119`
9. write `0x81 -> $4200`
10. write `0x0F -> $2100`
11. `CLI`
12. spin forever through `BRA $FE`

That exact body matches the much older pass-2 boot-side fatal color hang reading, but now it is frozen as the **shared invalid fallback actually reached by the VM family**.

One sharper detail matters:
all six family entries load `X = 0x7FE0` before branching here, so this is not a generic panic path. It is a fixed-color, force-blank hard-stop.

The strongest safe reading is:

> **`C0:2E1E..2E65` is the exact forced-blank error-color hang body used as the shared invalid fallback when the local family gate byte `2D` is zero.**

---

## 2. `C0:88E5..88EC` is the first exact downstream transfer of the family’s local seed bytes into a working pair

This tiny body is byte-exact:

```text
C0:88E5  A5 2A
C0:88E7  85 2E
C0:88E9  A5 2B
C0:88EB  85 30
C0:88ED  60
```

Exact behavior:

- local `2A -> 2E`
- local `2B -> 30`
- return

That is the first exact downstream handoff from the pass-114 seed family into a different working lane.

This pass does **not** overclaim the final player-facing noun of `2E/30`.
But it does prove that `30` is no longer only a vague “mode byte” in the abstract.
Inside this later chain it is an exact working-byte copy sourced from the earlier family’s local parameters.

The strongest safe reading is:

> **`C0:88E5..88EC` is the exact local transfer body that copies the family’s parameter bytes `2A/2B` into the later working pair `2E/30`.**

---

## 3. `C0:88ED..8A69` is an exact template-dispatch lane that seeds local step bytes `2C/2D` and shifts working pair `2E/30`

The front dispatcher at `88ED` is now tight enough to promote.

The body:

```text
C0:88ED  AD 38 01
C0:88F0  D0 0E
C0:88F2  AD F9 00
C0:88F5  29 0F
C0:88F7  0A
C0:88F8  E2 10
C0:88FA  AA
C0:88FB  FC 02 89
C0:88FE  C2 10
C0:8900  60
```

Exact behavior:

1. tests `0138`
2. when `0138 != 0`, returns through the short `REP #$10 ; RTS` tail
3. otherwise reads `00F9 & 0x0F`
4. doubles that nibble
5. uses it to dispatch through the inline target table beside `8900`

The unique live helper bodies reached from that table are:

- `C0:8924` — no-op return
- `C0:8925..8943`
- `C0:8944..8962`
- `C0:8963..8981`
- `C0:8982..89A0`
- `C0:89A1..89D1`
- `C0:89D2..8A06`
- `C0:8A07..8A3B`
- `C0:8A3C..8A69`

### Exact helper semantics

These bodies are byte-regular enough to freeze their shared mechanics.

Common pattern:
- test `00F8.bit1`
- choose coarse step `0x20 / 0xE0` when set
- choose fine step `0x10 / 0xF0` when clear
- write exact step bytes into local `2C` and/or `2D`
- add or subtract the same exact step from working pair `2E` and/or `30`

The bodies break down like this:

- `8925..8943`
  - writes positive X-like step into `2C`
  - adds that step to `2E`

- `8944..8962`
  - writes negative X-like step into `2C`
  - subtracts that step from `2E`

- `8963..8981`
  - writes negative Y-like step into `2D`
  - subtracts that step from `30`

- `8982..89A0`
  - writes positive Y-like step into `2D`
  - adds that step to `30`

- `89A1..89D1`
  - writes matching positive steps into both `2C` and `2D`
  - adds that step to both `2E` and `30`

- `89D2..8A06`
  - writes negative step to `2C`
  - subtracts from `2E`
  - writes positive step to `2D`
  - adds to `30`

- `8A07..8A3B`
  - writes positive step to `2C`
  - adds to `2E`
  - writes negative step to `2D`
  - subtracts from `30`

- `8A3C..8A69`
  - writes matching negative steps into both `2C` and `2D`
  - subtracts that step from both `2E` and `30`

This is the first exact downstream role freeze for local `2C`:
not yet a final global noun, but no longer anonymous.

The strongest safe reading is:

> **`C0:88ED..8A69` is an exact template-dispatch lane that uses a low-nibble selector from `00F9` to choose one of several signed step templates, writes those exact step bytes into local `2C/2D`, and shifts the working pair `2E/30` by coarse (`0x20`) or fine (`0x10`) signed steps according to `00F8.bit1`.**

---

## 4. `C0:8A6C..8A9D` is the first exact reader of local `30`

Pass 114 explicitly left “first exact consumer of `30`” open.

That edge is now closed.

The body starts:

```text
C0:8A6C  A5 30
C0:8A6E  F0 11
C0:8A70  30 1C
...
C0:8A72  A5 2E
C0:8A74  F0 08
C0:8A76  30 03
C0:8A78  82 20 06
C0:8A7B  82 42 05
C0:8A7E  82 8F 02
...
```

and continues through the same shape for the other sign/zero cases.

Exact behavior:
- reads local `30`
- splits first on `zero / negative / positive`
- then reads local `2E`
- splits again on `zero / negative / positive`
- long-branches into one of these exact downstream bodies:
  - `C0:909C`
  - `C0:8FC1`
  - `C0:8D11`
  - `C0:8AB5`
  - `C0:8BC4`
  - `C0:8E21`
  - `C0:8EF1`
  - `C0:8BF9`

This is the first exact place where `30` is not merely seeded or carried.
It is directly read and used as the top-level branch discriminator.

The strongest safe reading is:

> **`C0:8A6C..8A9D` is the first exact downstream reader of local `30`: a sign/zero dispatcher over the working pair `2E/30` that selects one of eight later branch bodies.**

---

## 5. What materially changed in this pass

This pass does four real things:

1. closes the external fallback target `C0:2E1E..2E65` as the exact forced-blank error-color hang body
2. proves the earlier seed bytes `2A/2B` are copied into a later working pair `2E/30`
3. freezes the first exact downstream role of local `2C` as a signed step byte written by the template helpers
4. closes the first exact downstream reader of local `30` through the sign/zero dispatcher at `8A6C..8A9D`

What it still does **not** do:

- freeze the final player-facing noun of the `2E/30` working pair
- freeze the final global noun of `2C/2D`
- decode the eight downstream branch bodies at:
  - `8AB5`
  - `8BC4`
  - `8BF9`
  - `8D11`
  - `8E21`
  - `8EF1`
  - `8FC1`
  - `909C`

Those are now the real next seam.

---

## Honest next seam after this pass

The cleanest continuation target is now:

1. the eight-way downstream branch family selected by `8A6C..8A9D`
2. whichever of those bodies first proves the final human-facing noun of the working pair `2E/30`
3. whichever of those bodies first proves the later exact consumer of template step bytes `2C/2D`

That is the smallest honest seam left open by this pass.
