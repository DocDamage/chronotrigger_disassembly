# Chrono Trigger Disassembly — Pass 97

## Scope
Pass 96 closed the negative-`1E05` helper fog, but it still left one exact C7 question worth finishing before going back to `CE0F`:

- what `0155` actually is
- what the `0x30..0x3F` bridge at `071D` really rewrites packets into
- whether `061C` is only the `0x18..0x2F` sender, or a broader shared immediate send path

I stayed on that seam and did not go broad.

## Starting point
- previous top-of-stack: **pass 96**
- current target seam: the shared post-prologue C7 re-entry at `0155`, the `071D` bridge, and the exact table at `0A98`

## Work performed
- decoded the raw bytes at `C7:0140..0191` directly from the ROM instead of relying on older prose
- decoded the full bridge body at `C7:071D..0733`
- decoded the exact table payload at `C7:0A98..0AD7`
- rechecked the dispatcher branch shape to see where negative opcodes and `0x18..0x3F` actually land
- verified the only exact external tail-entry to `0155` is the raw `JMP $0155` at `C7:0731`

## Strongest keepable result
Pass 97 closes the last honest ambiguity in the local C7 bridge logic.

The exact shape is now:

- `0155..0191` is **not** a sender helper
- it is the shared **post-prologue redispatch entry** that re-reads the already-seeded `1E00..1E05` header bytes after the `0140` prologue has already installed `DB = 00` and `D = 1E00`
- `071D..0733` does **not** just “go to the packet sender”
- it rewrites the `0x30..0x3F` family into synthetic packets of the form:
  - `1E00 = 0x10`
  - `1E01 = low nibble of original opcode`
  - `1E02 = 0xFF`
  - `1E03 = 0xFF`
- then it tail-jumps to `0155`
- because `0155` redispatches exact opcode `0x10` through the `0x10..0x17` gate table at `0AD9`, this is an exact bridge into the **`01A1` negative-`1E05` special path**, not a generic sender shortcut

That is a real semantic tightening of the live seam.

## 1. `C7:0155..0191` is the shared post-prologue redispatch entry

The raw bytes make this exact.

At `0140..0154`, the dispatcher prologue has already:
- saved `B`, `D`, flags, `A`, `X`, and `Y`
- forced `DB = 00`
- forced direct page `D = 1E00`

`0155` is where the dispatcher body starts re-reading the live header/workspace bytes.

Exact behavior from `0155..0191`:
- `SEP #$20`
- reads exact control byte `1E05`
- if `1E05` is non-negative, exits through the common epilogue at `0192`
- reads exact opcode byte `1E00`
- if `1E00 == 00`, exits through `0192`
- if `1E00` is negative / signed-high, jumps straight to `061C`
- if `1E00 < 0x10`, exits
- if `0x10..0x17`, dispatches through exact table `0AD9`
- if `0x18..0x2F`, jumps to `061C`
- if `0x30..0x3F`, jumps to `071D`
- if `0x70`, jumps to `08E3`
- if `0x71`, jumps to `0755`
- otherwise exits

So the strongest safe reading is:

> `C7:0155..0191` is the exact shared post-prologue redispatch entry over preseeded low-bank packet header bytes, under the negative-`1E05` control gate.

This matters because it explains exactly what `071D` is reusing.

## 2. `C7:061C..064F` is broader than the pass-96 wording implied

Pass 96 correctly froze the send mechanics, but the branch shape at `0155` tightens the entry conditions.

`061C` is reached by two exact routes from the redispatch body:
- any opcode with bit 7 set (`1E00` negative / signed-high)
- the explicit `0x18..0x2F` band

So the exact safe reading is slightly broader than “the `0x18..0x2F` sender.”

It is:

> the shared exact 4-byte APU packet sender for negative-header opcodes and for the direct `0x18..0x2F` family, with the exact `0xFC` threshold-fixup case.

The send body itself stays the same:
- streams `1E03 / 1E02 / 1E01 / 1E00` through `$2143/$2142/$2141/$2140`
- waits for echo on `$2140`
- if exact opcode `1E00 == 0xFC`, compares `1E01 & 0x0F` against `F0` and calls `09FD` when needed
- exits through `0192`

## 3. `C7:071D..0733` is an exact rewrite bridge into the `01A1` special path

This is the biggest direct upgrade of pass 97.

Exact body:
- masks exact opcode byte `1E00` to its low nibble
- multiplies by four
- uses that as an index into exact table `C7:0A98`
- loads one 16-bit word from `C7:0A98 + index` into `1E00 / 1E01`
- loads one 16-bit word from `C7:0A9A + index` into `1E02 / 1E03`
- tail-jumps to exact redispatch entry `0155`

The table contents are exact, and they are not generic.

For all sixteen entries, the rewritten header is:
- `1E00 = 0x10`
- `1E01 = selector 0x00..0x0F`
- `1E02 = 0xFF`
- `1E03 = 0xFF`

Because `0155` then re-runs the dispatcher body against this rewritten header:
- opcode `0x10` goes through gate table `0AD9`
- `0AD9[0] = 01A1`

So the strongest safe reading is:

> `C7:071D..0733` rewrites the `0x30..0x3F` family into synthetic `{0x10, selector, 0xFF, 0xFF}` packets and redispatches them at `0155`, which lands them in the `01A1` negative-`1E05` special path.

That is tighter and more honest than the softer pass-96 wording.

## 4. `C7:0A98..0AD7` is an exact synthetic-packet rewrite table

This table is now worth freezing directly.

Exact structure:
- 16 entries
- 4 bytes per entry
- entry `n` is exactly:
  - byte 0 = `0x10`
  - byte 1 = `n`
  - byte 2 = `0xFF`
  - byte 3 = `0xFF`

So the exact sequence is:
- `30 -> 10 00 FF FF`
- `31 -> 10 01 FF FF`
- `32 -> 10 02 FF FF`
- ...
- `3F -> 10 0F FF FF`

This is why the bridge is exact instead of vague.

It is not “some packet defaults table.”
It is a concrete packet-rewrite table used only by the `0x30..0x3F` bridge.

## 5. What changed semantically

Before pass 97, the safest wording was still a little loose around the bridge:
- `071D` was described as a table-driven bridge into the shared low-bank send path
- `061C` was described mainly as the `0x18..0x2F` sender
- `0155` itself was still unnamed

That is no longer the honest state.

After pass 97:
- `0155` has a real role
- `071D` is an exact **rewrite + redispatch** bridge into `01A1`
- `0A98` has an exact table noun
- `061C` is correctly broader: shared negative-header + `0x18..0x2F` immediate sender

## Strong labels / semantics added
- `C7:0155..0191` — shared post-prologue redispatch entry under the negative-`1E05` gate
- `C7:0A98..0AD7` — exact synthetic `{0x10, selector, 0xFF, 0xFF}` rewrite table for the `0x30..0x3F` family
- strengthened `C7:071D..0733`
- strengthened `C7:061C..064F`

## Corrections made this pass
- corrected the soft implication that `071D` mainly reuses the direct immediate sender
- corrected the too-narrow reading of `061C` as only the `0x18..0x2F` sender
- pinned `0155` as a real redispatch entry instead of leaving it as an unnamed re-entry address

## Still unresolved
- the final user-facing audio noun of every immediate packet opcode is still not frozen
- `1E10 / 1E11` still need broader subsystem naming beyond their exact control/latch role
- `CE0F` still needs the first clean external reader path that freezes its final noun
- the larger endgame remains unchanged: bank separation, decompressor/data grammar work, runtime-backed WRAM proof, and rebuildability

## Next recommended target
Now that `0155`, `071D`, and `0A98` are exact enough, the C7 bridge is cold enough.

The right next move is:
1. go back to **`CE0F`**
2. trace its first clean external reader path
3. only widen back out after that seam is tightened
