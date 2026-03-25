# Chrono Trigger Disassembly — Pass 102

## Scope
Pass 101 found the first honest external caller anchor for `D1:EA4B`, but the surrounding CD-side driver block at `CD:8978..89CB` was still being described too loosely.

This pass stayed on that caller chain and froze the exact local control contract around:

- `CE13`
- `CD29`
- `CD2D`
- `CD2E`
- `A028`
- the raster wait helper at `CD:3B82`

## Starting point
- previous top-of-stack: **pass 101**
- live seam from the note: **`CD:8978..89CB`**

## Work performed
- decoded `CD:8978..89CB` instruction-for-instruction from the ROM bytes
- rechecked the only local readers/writers of `CD29 / CD2D / CD2E / A028 / CE13` in mapped CD-bank code
- disassembled `CD:1918..191D` to close the missing immediate-token sibling after `0xE0`
- decoded `CD:3B82..3BA5` exactly to remove the last fuzzy helper in the gated pre-tail path
- cross-checked the other clean `A028` reader at PC `0x014269`

## 1. `CD:8978..89CB` is now an exact staged tail driver
The exact body is:

```text
CD:8978  BEQ +0F
CD:897A  JSL CE:E18E

CD:897E  LDA $7C
CD:8980  AND $CE13
CD:8983  BNE +04
CD:8985  JSL D1:EA4B

CD:8989  LDA $CD2D
CD:898C  BNE +09
CD:898E  LDA $A028
CD:8991  BNE +04
CD:8993  JSL CE:F066

CD:8997  JSL C1:000C

CD:899B  LDA $CD2E
CD:899E  BNE +0F
CD:89A0  LDA $A013
CD:89A3  BEQ +0A
CD:89A5  LDA $A028
CD:89A8  BNE +05
CD:89AA  LDA #$40
CD:89AC  JSR $3B82

CD:89AF  JSR $1609
CD:89B2  LDA $CD29
CD:89B5  STA $A028
CD:89B8  JSR $0B1E
CD:89BB  JSL D1:F426
CD:89BF  JSL FD:FFF7
CD:89C3  JSR $0ADE
CD:89C6  JSL C2:8002
CD:89CA  JSR $0340
CD:89CD  RTS
```

That means the block is no longer just “caller neighborhood.”
It is an exact linear tail driver with:

1. optional early `CE:E18E` clear
2. bitmask-gated `D1:EA4B` palette-maintenance tick
3. first optional helper gate through `CD2D` and `A028`
4. unconditional `C1:000C`
5. second optional helper gate through `CD2E`, `A013`, and `A028`
6. fixed post-gate tail:
   - `CD:1609`
   - `CD29 -> A028`
   - `CD:0B1E`
   - `D1:F426`
   - `FD:FFF7`
   - `CD:0ADE`
   - `C2:8002`
   - `CD:0340`

## 2. `CE13` is now exact enough to stop calling it a generic unknown byte
Pass 101 only knew that `CE13` gated the D1 call somehow.
This pass freezes the exact local contract:

```text
LDA $7C
AND $CE13
BNE skip_D1_EA4B
```

And the other clean write in this subsystem still stands:

```text
A9 #$03
STA $CE13
```

So the strongest safe reading is now:

> `CE13` is the exact mask byte that suppresses the D1 palette-maintenance tick whenever the currently active low bits in `7C` overlap that mask.

I am still not claiming the broader gameplay-facing noun of the full `7C` state byte from this pass alone.
But the local gate meaning of `CE13` is now exact.

## 3. `CD2D` and `CD2E` are no longer just anonymous immediate bytes
Pass 85 proved tokens `0xE1` and `0xE2` write them directly.
Pass 102 closes their first exact clean-code consumer roles.

### `CD2D`
The gate is:

```text
LDA $CD2D
BNE skip_CE_F066
LDA $A028
BNE skip_CE_F066
JSL CE:F066
```

So `CD2D` is now exact enough to read as:

> immediate inhibit/skip byte for the `CE:F066` pre-tail helper.

### `CD2E`
The gate is:

```text
LDA $CD2E
BNE skip_wait
LDA $A013
BEQ skip_wait
LDA $A028
BNE skip_wait
LDA #$40
JSR $3B82
```

So `CD2E` is now exact enough to read as:

> immediate inhibit/skip byte for the gated raster/beam wait helper at `CD:3B82`.

These are materially stronger than the old “neighboring immediate control bytes” wording.

## 4. `CD:1918..191D` closes the missing immediate-token sibling
The bytes immediately after the already-frozen `0xE0` wrapper are:

```text
A7 40
8D 29 CD
60
```

So `CD:1918..191D` is exact:

```text
LDA [$40]
STA $CD29
RTS
```

Given the contiguous table order in the `0xE0..0xE8` family, this is the natural missing sibling token immediately following `0xE0`.

Strongest safe reading:

> direct immediate store token for `CD29`.

## 5. `CD29 -> A028` is now a frozen mirror/latch contract
This is the biggest RAM-side closure of the pass.

Inside `CD:8978..89CB`:

```text
LDA $CD29
STA $A028
```

And earlier in the same block, both optional helper gates test `A028` and skip their calls when it is nonzero.

The other clean mapped-code reader at PC `0x014269` also busy-waits until `A028 == 0` before continuing.

That is enough to freeze the exact structural reading:

- `CD29` is the immediate/staged source byte
- `A028` is its mirrored live latch / holdoff byte
- nonzero `A028` suppresses both optional pre-tail helpers in `CD:8978..89CB`
- another clean code site later polls `A028` until it returns to zero

This is a real local control contract now, not a loose coincidence.

## 6. `CD:3B82..3BA5` is an exact raster/beam wait helper
The exact body is:

```text
STA $45
loop:
  LDA $4212
  BMI loop
wait_hblank_set:
  LDA $4212
  AND #$40
  BEQ wait_hblank_set
wait_hblank_clear:
  LDA $4212
  AND #$40
  BNE wait_hblank_clear
  LDA $2137
  LDA $213F
  LDA $213D
  CMP $45
  BCC loop
RTS
```

Strongest safe reading:

> exact hardware-status wait helper that latches the PPU beam counters and loops until the latched counter byte read through the `2137/213F/213D` sequence reaches or passes the caller-supplied threshold in `A`.

That is why `CD:89AA` loads `#0x40` before calling it.

## 7. what changed semantically
Before pass 102:

- `CD:8978..89CB` was only a cautiously described caller block
- `CD29` had no frozen token writer
- `A028` was not yet pinned as the mirrored live latch from `CD29`
- `CE13`, `CD2D`, and `CD2E` were still below exact local nouns

After pass 102:

- `CD:8978..89CB` is an exact staged tail driver
- `CE13` is now an exact D1 palette-maintenance suppress mask against `7C`
- `CD2D` is the exact inhibit byte for `CE:F066`
- `CD2E` is the exact inhibit byte for the `CD:3B82` raster wait
- `CD:1918..191D` is the missing direct-immediate token for `CD29`
- `CD29 -> A028` is now a frozen staged-source -> live-latch contract

## Strongest keepable conclusions
1. The CD-side caller chain behind `D1:EA4B` is now exact enough to treat as one real tail driver, not a vague neighborhood.
2. `CE13` is a true mask byte controlling whether the D1 palette-maintenance tick is skipped for the current `7C` state.
3. `CD2D` and `CD2E` are no longer just script-written bytes; they now have exact clean-code inhibit roles.
4. `CD29` is written by a direct immediate auxiliary token and mirrored into `A028` during the tail.
5. `A028` is now a real live holdoff/latch byte used as a zero-gate before both optional helpers in the driver block.

## Honest caution
Even after this pass:

- I have **not** frozen the final higher-level subsystem noun of `CE:F066`.
- I have **not** frozen the final gameplay-facing noun of `A013`.
- I have **not** frozen the exact higher-level noun of the full `7C` state byte beyond already-proven local uses.
- I have **not** frozen a clean direct static reader of `CE0F`.

## Next recommended target
The cleanest next static move is now:

1. stay in the same local CD/CE seam
2. decode the exact contract around `CD:0DB1..0DFB`
3. specifically freeze:
   - why that block seeds `CE13 = 0x03`
   - why it seeds `CE0E = 0x80`
   - how the quiescence loop over `CE0A | CCEA | A013 | 5D9B` relates to the already-frozen tail driver at `CD:8978`

That should turn the current local tail driver into an actual owner chain instead of stopping at the first stable caller.

## Completion estimate after pass 102
Conservative project completion estimate: **~68.5%**
