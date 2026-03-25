# Chrono Trigger Disassembly — Pass 127

## Scope
- close the post-substitution / descriptor-normalization seam at `C2:C7A6..C2:C946`
- strengthen the continuation-family helper chain at `C2:BB1F..C2:BC70`

## Starting point
- previous top-of-stack: pass 126 froze `C2:B6D3..C2:BA2E` and `C2:C5C7..C2:C783`
- current target seam: `C2:C7A6..C2:C8AF`, with follow-through into the newly proven shared builder at `C2:C8BA..C2:C946`

## Work performed
- proved that `C2:C7A6..C2:C7AB` is data, not code: it is a 3-word local dispatch table pointing at `C7AC`, `C7E0`, and `C6B9`
- reconstructed `C2:C7AC..C2:C7DF` as a real prep owner with a fixed `CB8B -> C9E5 -> C649 -> CAF3 -> CE86` loop before it signals through `9689` and jumps `83B2`
- reconstructed `C2:C7E0..C2:C804` as the next exact `0D1D`-gated sibling dispatcher above `C805`
- reconstructed `C2:C805..C2:C8B9` as two exact reseed/helper lanes (`C85B`, `C88D`) feeding one shared staged builder at `C8BA`
- extended the closure through `C2:C8BA..C2:C946` because the target seam ended in the middle of that shared worker
- used the proven continuation-family xrefs into `BB1F`, `BBD6`, and `BC22` to close the first helper chain behind the new `B6D3` owner

## Findings

### 1. `C2:C7A6..C2:C7AB` is the exact 3-word dispatch root for the local post-substitution family
The bytes are exact little-endian words:
- `C7AC`
- `C7E0`
- `C6B9`

So the unresolved seam did not begin with live code. It begins with a compact local dispatch table that selects between the new prep owner at `C7AC`, the new `0D1D`-gated dispatcher at `C7E0`, and the already-closed sibling owner at `C6B9`.

### 2. `C2:C7AC..C2:C7DF` is an exact prep/scan owner that loops until `00C0` clears
This routine:
- mirrors exact byte `71` into exact bytes `0D36/0D37`
- runs exact helper chain `CB8B -> C9E5`
- forces 8-bit A/X, seeds exact index `X = 00`, and runs exact helper `C649`
- returns to 16-bit X, then loops exact helper chain `CAF3 -> CE86`
- tests exact word `00C0`; when nonzero, reruns exact helper `821E` and loops back into `CAF3`
- once the exact word clears, writes exact byte `9689 = 17`, runs exact helper `CE9D`, and exits through exact jump `83B2`

So this is the exact local prep owner that selects the next clear slot, repeatedly advances the shared descriptor/packet machinery until `00C0` clears, then signals completion through `9689`.

### 3. `C2:C7E0..C2:C804` is the next exact `0D1D`-gated dispatcher above `C805`
This routine:
- runs exact helper `E984`
- tests exact status byte `0D1D`
- clear path runs exact helper `C805`; when exact byte `81 != 54`, reruns exact helper `EAC2`; otherwise returns
- negative path tests exact byte `0F0D`; when exact bit `0x40` is set, returns immediately; otherwise jumps exact helper/owner `C674`
- overflow path runs exact helper `CC0E` and exits through exact jump `82B2`

So it is the real sibling dispatcher above the already-proven `C805` path, splitting into a clear `C805` lane, a negative-latched `C674` lane, and an overflow escape through `CC0E/82B2`.

### 4. `C2:C805..C2:C85A` is the exact post-selection normalization owner above the new reseed helpers
This routine:
- saves flags and forces 8-bit A/X
- clears exact word/byte `0D9E`
- tests exact byte `0F0C`; when `0F0C >= 05` and exact control byte `5A` is negative, runs exact local helper `C85B`
- tests exact OR-combine `0F0B | 0F0C`
- when that exact OR-combine is zero, clears exact selector byte `54` and seeds exact mode byte `80 = 40`
- otherwise builds exact index `X = 54` (or `54 + 80` when `54 >= 03`), tests exact byte `0F02,X & C0`, and when the exact high bits are set, reruns exact helper `C9AE` until the selected lane clears
- stores the exact selected high-bit state into exact byte `0F0D`
- runs exact helper `C973`
- clears exact bit `0x04` in exact word/byte `0D13`
- clears exact byte `56`, mirrors exact selector `54 -> 7F`, and when `54 >= 03`, increments exact byte `56`
- restores flags and exits through exact selector `FC37 -> 8385`

So this is the exact normalization/selection owner that prepares the post-substitution state, optionally recenters it through `C85B`, waits for a clear `0F02` lane, then packages the result for the shared `8385` selector path.

### 5. `C2:C85B..C2:C88C` and `C2:C88D..C2:C8B9` are two exact reseed helpers feeding the same staged builder
#### `C2:C85B..C2:C88C`
This routine:
- requires exact control bit `5A.bit3`
- seeds exact selector byte `54 = 03`
- when exact byte `80 != 00`, decrements exact byte `80`
- writes exact byte `0D9E = D0`
- in 16-bit mode seeds exact word `24 = 2613`, exact word `0D22 = FFF8`, and exact word `22 = 000E`
- runs exact shared helper `C8BA`

#### `C2:C88D..C2:C8B9`
This routine:
- computes exact threshold byte `00 = 0F0C - 03`
- seeds exact selector byte `54 = 06`
- repeatedly increments exact byte `80` until `80 + 1 >= 0F0C - 03`
- writes exact byte `0D9E = 30`
- in 16-bit mode seeds exact word `24 = 2013`, exact word `0D22 = 0008`, and exact word `22 = 0010`
- runs exact shared helper `C8BA`

So both helpers are exact reseed/setup lanes that differ only in how they adjust the selector/count state and in the exact signed step parameters they hand to the shared `C8BA` builder.

### 6. `C2:C8BA..C2:C946` is the exact shared staged builder/finalizer for the new `C805` family
This routine:
- saves flags and forces 8-bit A/X
- computes exact compare byte `71 = (54 - 03) + 80 + 73`
- runs exact settlement/search helper `8820`
- runs exact helper `CD9B`
- sets exact bit `0x04` in exact word/byte `0D13`
- in 16-bit mode seeds exact `EF05` parameter words:
  - `61 = 2E00`
  - `5B = 0213`
  - `5D = 24`
  - `5F = 180A`
- runs exact helper `EF05`
- clears exact word `0DAB`
- seeds exact loop word `0D24 = 0006`
- adjusts exact byte/word `25` from the sign of exact word `0D22`
- subtracts exact signed step word `0D22` from exact word `0D9E`, and when the subtract borrows, net-decrements exact word `0D95`
- runs exact helper `C949`
- reseeds exact `EF05` parameters as `61 = 2E00`, `5B = 24`, `5D = 0213`, then reruns exact helper `EF05`
- emits exact selector `FBE3 -> 8385`
- decrements exact loop word `0D24`; when nonzero, reruns exact helper `821E` and loops
- when the exact loop completes, clears exact words `0D9E` and `0D22`, runs exact helpers `CDE3` and `EAC2`, restores flags, and returns

So this is the real shared staged builder/finalizer for the `C805` family: it seeds the compare lane, runs the shared search/build machinery, then iterates a 6-step exact signed adjustment loop through `0D9E/0D95` and `C949` before clearing the state.

### 7. `C2:BB1F..C2:BBCF` is the exact three-row continuation packet owner feeding `BAFC/BA2F`
Entry is at `BB1F`; the preceding byte `BB1E = C8` is not externally called.

This owner:
- saves flags and immediately runs exact helpers `BBD6` and `BC22`
- mirrors the resulting exact threshold/value byte `X -> 0F6F`
- clears exact byte `7E`, compares exact byte `9A97` against exact word/byte `9890`, and when `9A97 < 9890`, writes exact byte `7E = 04`
- in 16-bit mode copies exact `0x0019` bytes from exact source block `2F9A` into exact destination block `9890` through exact helper `F114`
- seeds exact row counter `71 = 0001`
- the exact `71 = 0001` entry path branches into the shared loop body after the hardware-math setup lane
- the exact setup lane writes exact values to `$4204/$4205`, rewrites exact words `0D95/0D94` through exact helper `8BA6` using exact bytes `0F4A/0F49`, seeds exact word `0D92 = 32E8`, reruns exact helper `BBD6`, then seeds exact packet base `61 = 2ECA`, exact byte `0F51 = 17`, and clears exact byte `7D`
- the exact row loop loads exact byte `16,X`; negative entries emit exact selector packet `C030 -> ED31`, while nonnegative entries run exact helper `8816`, load exact byte `9A90`, run exact helper `BAFC`, rerun exact helper `BC22`, mirror the result into exact byte lane `0F6F[X]`, and run exact compare gate `BA2F`
- after every row, advances exact packet base `61 += 0180`, increments exact row counter `71`, and continues while `71 < 0003`
- finishes through exact selector `FBE3 -> 8385`

So this is the exact three-row continuation packet owner behind the `BB1F` helper slot consumed by the new `B6D3` owner.

### 8. `C2:BBD6..C2:BC20`, `C2:BC22..C2:BC58`, and `C2:BC59..C2:BC70` are the first exact helpers behind `BB1F`
#### `C2:BBD6..C2:BC20`
This helper:
- seeds exact word `17 = FFFF`
- runs exact helper `F566`
- builds exact index `X = 0F48 + 0F4A`
- loads exact byte `0F00[X] -> 0F4C`
- uses exact byte `0F30[X]` to index exact table `CC:2963`
- combines exact bytes `0419 + 041A` with exact table `0D5F`
- uses exact table `FF:F9BB` as a bitmask, repeatedly shifts it through exact local byte `00`, and writes exact incrementing byte indices into exact byte lane `17,X` whenever a mask bit is set

So it is the exact continuation helper that derives `0F4C`, selects one exact mask byte from the `FF:F9BB` table family, and expands that mask into the live exact row-index list at `17..`.

#### `C2:BC22..C2:BC58`
This helper:
- in the `0418 == 00` lane, uses exact byte `0F4C` directly as its base index
- otherwise uses exact high nibble `9A8F & 0F00`, shifts it down, combines it with exact byte `0F4C` through the stack, then uses exact table `1607` to derive a second index
- loads one exact value from exact table `CC:253B`, runs exact helper `BC59`, and writes the result to exact word/byte `9890`

So it is the exact threshold/value lookup helper consumed by `BB1F`, `B427`, and `BE8B`.

#### `C2:BC59..C2:BC70`
This helper:
- tests exact byte `9ABA`
- when `9ABA` is exact `A2` or exact `A3`, quarter-scales the exact accumulator through two rounds of `LSR` with carry compensation
- otherwise returns the exact accumulator unchanged

So it is the exact conditional quarter-round-up helper applied to the threshold/value byte produced by `BC22`.

## Strong labels / semantics added
- exact dispatch-table root for `C7AC/C7E0/C6B9`
- exact prep/scan owner at `C7AC`
- exact `0D1D`-gated sibling dispatcher at `C7E0`
- exact normalization owner at `C805`
- exact reseed helpers at `C85B` and `C88D`
- exact shared staged builder/finalizer at `C8BA`
- exact three-row continuation packet owner at `BB1F`
- exact mask-expander / threshold lookup / quarter-round helper chain at `BBD6/BC22/BC59`

## Corrections made this pass
- corrected the live seam so it no longer treats `C2:C7A6` as code; the first six bytes are data words, not opcodes
- extended the `C7A6..C8AF` target through `C946` because the target seam previously stopped in the middle of the shared `C8BA` routine
- corrected the continuation-family helper entry to `C2:BB1F`; the preceding byte at `BB1E` is not the called entry point

## Still unresolved
- the wider continuation-family seam remains open after the newly closed helper root, especially beyond `C2:BC71..C2:BEE5`
- the next post-substitution/helper seam remains open after the newly closed staged builder, especially beyond `C2:C947..C2:CAxx`
- broader gameplay/system nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B/0D8C/0D90`
- the broader top-level family noun for `C2:A886..AA30` is still not tight enough

## Next recommended target
- `C2:BC71..C2:BEE5`
- `C2:C947..C2:CA40`
- broader nouns for `7E:0F0F`, `7E:0D1F`, and the `0D8B/0D8C/0D90` family
