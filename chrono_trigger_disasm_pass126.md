# Chrono Trigger Disassembly — Pass 126

## Summary

Pass 126 closes the next continuation-family owner chain after the pass-125 bridge and freezes the next post-substitution / descriptor-normalization family under the `C2:C20F` local substitution path.

## What closed this pass

### 1. `C2:B6D3..C2:BA2E` is now a real continuation-family owner chain, not a blob after `B6AE`

This seam breaks cleanly into owner/helper/finalizer pieces.

#### `C2:B6D3..C2:B72E`
- seeds exact compare byte `71 = 0419 + 041A`
- reruns exact service `8820`
- snapshots exact byte `0F4A -> 0DD9`
- nonzero path rewrites exact byte `0D95` through `8BA6`, restores exact byte `0F4A`, runs exact helper chain `BD6B -> 821E`
- zero path reruns `EA53` and conditionally enters exact local guard `B72F`
- always mirrors exact selector byte `54 -> 0F48`
- conditionally reruns `EAC2` when exact byte `54 != 81`
- always exits through exact helper chain `BB1F -> BE01 -> BDEB -> FBE3`

That is not generic glue anymore.
It is the exact owner for the next continuation lane rooted in exact byte `0F4A`.

#### `C2:B72F..C2:B741`
This is a tiny exact local guard:
- returns immediately when exact bytes `54 == 0` and `0F4A == 0`
- otherwise only allows the downstream worker when the exact selector/threshold test passes

#### `C2:B742..C2:B7CB`
This worker is the real `0F4A` adjuster/finalizer:
- exact control bit `5A.bit2` increments or decrements exact byte `0F4A`
- exact byte `0F4C` is built from exact index `54 + 0F4A`
- exact source word `61 = 3424` feeds exact helper `BD99`
- then the lane reruns `EAC2`, enters a 16-bit exact ramp using `0DAB`, `0D22`, `0D24`, and sign-dependent updates of exact word `0D95`
- exact helper `B7CC` finalizes the lane afterward

So this is the exact signed-`0F4A` adjuster feeding the next continuation index and ramp.

#### `C2:B7CC..C2:B822`
This is the exact sign split staging mover:
- nonnegative `0D21` path seeds exact words `63 = 3064`, `65 = 2FE4`, `8C = 0010`, and `8A = 0015`, then runs exact helper `EF2B`
- negative `0D21` path performs repeated exact same-bank block copies with stride `0x0040`
- the negative path finishes with one final exact block copy into exact block `2FC0`

#### `C2:B823..C2:B8D8`
This part closes as the exact probe wrapper + exact probe loop:
- `B823` reruns exact helper `B83E`, then exact service `8820`, then clears exact byte `0DBC` when `9A97 < 0F4F`
- `B83E` recenters exact selector byte `54` from exact bytes `0DBB/73` and exact control bits in `0DBD` and `5A`
- `B870` rebuilds exact byte `0DBC` from two exact compare lanes, effectively turning it into a two-bit result byte

This is the first time the role of exact byte `0DBC` is actually pinned instead of guessed.

#### `C2:B8D9..C2:B95C`
This is the exact packet/import finalizer after the probe passes:
- fixed helper chain `F5A7 -> 821E -> F643 -> BA4F -> B6AE`
- then six exact block copies from bank `FF` into exact WRAM bands `94C0`, `94C8`, `94E0`, `94E8`, `9500`, and `9520`
- then exact byte `0D13 = 01`, exact helper `86DD`, and exact selectors `FBE3` / `FBFF`

#### `C2:B95D..C2:BA2E`
The tail breaks cleanly too:
- `B95D..B977` = short exact `F643/C037/FBE3` wrapper
- `B978..B9E0` = exact overflow tail that reseeds exact selector byte `54 = 0419 + 0B`, increments exact byte `0D15`, writes exact bytes `84 = FF` and `0D78 = FF`, builds mirrored exact `5D44/5DC4` blocks, and jumps exact tail `E923`
- `B9E1..BA08` = exact phase-02 packet prep wrapper
- `BA09..BA2E` = exact local packet-byte loader built from exact byte `9A90`

So the whole `B6D3..BA2E` band is now structurally real.

### 2. `C2:C5C7..C2:C783` is now a real post-substitution / descriptor-normalization family

Pass 123 already proved `C20F` always falls through exact tail `C5C7`.
Pass 126 closes what that tail actually is.

#### `C2:C5C7..C2:C618`
This is the exact six-entry post-substitution descriptor normalizer:
- copies exact block `0408 -> 9890`
- marks one exact staged slot from exact selector `(54 - 0F)` with `FF`
- walks six exact entries backward comparing exact bytes `0F00` against exact staged bytes `9890`
- writes exact descriptor words under `2E02/2E04` using exact destination table `C5A7`
- exact helper `C5B3` is reused when the compared exact byte still represents a valid live descriptor value

That locks `C5C7` as the real descriptor normalizer after the local substitution/reconciliation pass.

#### `C2:C619..C2:C61E`
This is an exact three-word local dispatch table:
- `C627`
- `C65D`
- `C6B9`

#### `C2:C61F..C2:C65C`
This band is the pre-entry wrapper plus exact next-clear-slot helper:
- exact sum `0F0B + 0F0C < 02` clears exact byte `67`, increments exact byte `68`, and exits through exact jump `EACC`
- otherwise exact helper `C649` scans forward until exact byte `0F02[X]` has no high bits set
- the selected exact slot is latched into exact selector byte `54`
- exact bytes `0F00/0F01` are both forced to `FF`
- then the wrapper reruns `EAC2` and jumps exact tail `CAF3`

#### `C2:C65D..C2:C783`
This now resolves into three exact sibling pieces:
- `C65D..C6B8` = exact `0D1D`-gated post-selection owner with a clear-return lane, a negative exact `EF05` staging lane, and an overflow escape to exact jump `9A98`
- `C6B9..C6E6` = exact sibling owner that optionally mirrors exact byte `0F0D -> 0F01`, then enters exact helper `C70C`
- `C6E7..C70B` = exact shared helper that forces exact bytes `0F00/0F01 = FF`, runs exact helper `8255` with `A = 40`, and clears exact byte lane `1811` in exact `0x40` strides
- `C70C..C783` = exact swap/normalizer over exact bytes `0F00/0F01`, followed by exact parameter building and fixed tail `F378 -> FBE3 -> CD2B -> CDE3`
- `C784..` begins the next exact helper seam and is now clearly live

This is enough to stop calling the `C5C7..` band a vague finalizer.
It is a real descriptor-normalization family with dispatch, slot selection, swap logic, and fixed emit tails.

## WRAM progress tightened this pass

### `7E:0F4A`
Now strong enough to describe as the exact signed continuation-delta byte:
- snapshotted into exact byte `0DD9`
- adjusted by the exact `B742` worker
- mirrored forward into exact selector/state paths that feed exact bytes `0F48` and `0F4C`

### `7E:0DBC`
Now strong enough to describe as an exact two-bit probe/result byte:
- rebuilt by exact helper `B870`
- one exact compare contributes `0x02`
- the other exact compare contributes `0x01`
- exact wrapper `B823` can still clear it after the downstream threshold recheck

## Honest remaining gaps after pass 126

The next real seams are now:
- `C2:BA2F..C2:BEE5`
- `C2:C7A6..C2:C8AF`
- broader gameplay-facing nouns for exact bytes `0F0F/0D1F`, the broader gameplay/system role of `0D8B/0D8C/0D90`, and the broader top-level family noun for `C2:A886..AA30`
