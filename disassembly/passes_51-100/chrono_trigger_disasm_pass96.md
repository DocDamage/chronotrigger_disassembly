# Chrono Trigger Disassembly — Pass 96

## What I targeted
Pass 95 left one very clean C7 seam instead of a broad hunt:

- finish the tail of the negative-`1E05` special path after `037B..04B0`
- tighten the helper trio `0655`, `0734`, `0A39`
- pin the adjacent `0x18..0x3F` packet-family bridge only where the same bytes make it cheap and honest

I stayed on that seam.

---

## Strongest keepable result
This pass closes the remaining C7 helper fog from pass 95.

> `C7:04B1..061B` is now an exact **post-emit special-path tail**: it updates current-slot/latch state, conditionally resends a shared command-`0x03` burst, sends a selector-driven variable-length command-`0x03` burst from `0D18`, then sends a second fixed 12-triplet command-`0x03` burst from `1871 + 36*selector`, terminates with `0xE0`, runs cleanup, and exits.

> `C7:0655..071C` is now an exact **per-slot command-`0x03` stream helper** that refreshes the live `1E40..1E63` strip family from the `0AEA` selector table.

> the “mystery helpers” at `0734` and `0A39` are not mystery helpers anymore:
- `0734` currently collapses to exact `1E00 |= 0x04`
- `0A39` is an exact selector-table-backed APU handshake gate with one fatal negative-status unwind path

That is real closure, not wording polish.

---

## 1. `C7:0734` is a real correction, not just another helper label

This one was worth freezing because it corrects the honest state of the seam.

Exact behavior:
- reads exact opcode byte `1E00`
- if `1E00 >= 0x14`, forces `1E00 |= 0x04` and returns
- otherwise enters a selector-scan loop rooted at `C7:0AD8`
- but the first byte at `C7:0AD8` in the current ROM is exact sentinel `0xFF`
- so the scan exits immediately and the helper also forces `1E00 |= 0x04`

So the strongest safe reading is not “conditional selector helper.”
It is:

> `C7:0734..0754` currently collapses to exact `1E00 |= 0x04`, while retaining a dead/degenerate selector-scan stub rooted at `0AD8`.

That is a real correction from the softer pass-95 wording.

---

## 2. `C7:0A39` is the exact selector-table-backed APU handshake gate

This helper turned out to be much cleaner than pass 95 could honestly claim.

Exact behavior:
- uses `1E01 & 0x7F` as a `*2` index into the table at `C7:241D`
- seeds exact local bytes:
  - `02` from `C7:241E + index`
  - `03` from low nibble of `C7:241D + index`
- if exact nibble `03` differs from exact local byte `F0`, calls exact trim helper `09FD`
- sends the exact 4-byte handshake packet:
  - `$2143 = 03`
  - `$2142 = 02`
  - `$2141 = 1E01`
  - `$2140 = 1E00`
- retries until `$2140` echoes the just-written opcode byte
- then stores exact `84 = ((1E00 + 1) & 0x7F)`
- if exact status byte read back from `$2141` is negative:
  - writes `84` back through `$2140`
  - waits for the decremented echo
  - discards the local return frame
  - jumps straight to common exit `0192`
- otherwise returns normally

So the strongest safe reading is:

> `C7:0A39..0A97` is an exact selector-table-backed APU handshake / gate helper with one fatal negative-status unwind path.

This is one of the main reasons the special path is no longer fuzzy.

---

## 3. `C7:09FD`, `09DA`, and `09EA` are the small support cluster that makes `0A39` honest

I kept these with exact helper nouns because they are directly on the seam and they make `0A39` / `04B1` readable.

### `09DA..09E9`
Exact behavior:
- writes `A` to `$2140`
- spins until `$2140` echoes it
- returns exact `((A + 1) & 0x7F)`

Strongest safe reading:
> exact low-bank APU echo/ack helper that advances the local 7-bit handshake token.

### `09EA..09FC`
Exact behavior:
- writes exact local byte `84` to `$2140`
- waits for echo
- forces `84 = 0xE0`

Strongest safe reading:
> exact low-bank APU reset/normalization helper paired with `09DA`.

### `09FD..0A38`
Exact behavior:
- stores the incoming threshold nibble in `F0`
- derives exact comparison byte `F2`
- scans exact live strip `1E63..` in even steps
- once the threshold rule is met, zeroes trailing live strips from that point onward:
  - `1E20..`
  - `1E40..`
  - `1E62..`

Strongest safe reading:
> exact live-slot trim helper used by the selector-handshake path to clamp the trailing live strips.

That matters because pass 95 only knew that `0A39` existed; pass 96 now makes the control loop around it exact.

---

## 4. `C7:0655..071C` is the per-slot command-`0x03` table-stream helper

This helper is called directly from the live-slot reconcile loop at `034F`, so tightening it materially improves the whole negative-`1E05` path.

Exact behavior:
- reads exact current live-slot index from `1C`
- reads exact current selector from `1E20 + X`
- converts `(selector - 1)` into a `*3` index into the pointer table at `C7:0AEA`
- seeds exact source pointer `12/13/14`
- uses exact per-slot base pair `1E60 + X / 1E61 + X` as the command-`0x03` destination/header pair
- after the command-`0x03` handshake succeeds:
  - reads first stream byte into exact local `0C`, mirrors it into `1E40 + X`, and stores base+that byte into `1E62 + X`
  - reads second stream byte into exact local `0D`, mirrors it into `1E41 + X`, and stores base+that byte into `1E63 + X`
- then treats the first byte as an exact triplet-count and streams the remaining body through `$2141/$2142/$2143`
- resets exact local byte `84` to `0xE0` before returning

So the strongest safe reading is:

> `C7:0655..071C` is the exact per-slot command-`0x03` table-stream helper that refreshes the live selector/base/end strip family at `1E20..1E63`.

That finally makes the `1E40..1E63` family honest.

---

## 5. `C7:04B1..061B` is the real tail after the command-`0x02` staged emit

Pass 95 stopped at `04B0`. Pass 96 closes what happens next.

Exact behavior:
- runs only after the staged command-`0x02` emit phase
- starts with the first candidate value already loaded from `1F00`
- scans backward through live selector strip `1E20..1E3E` and stores exact local slot/index state into `FC`
- updates exact latch bytes `1E10 / 1E11` through the carry/result logic at `04C2..04D2`
- if exact local byte `F3` is nonzero, calls shared helper `0922`

Then it enters the first command-`0x03` burst phase:
- sends exact header:
  - `$2143 = 0x20`
  - `$2142 = 0x00`
  - `$2141 = 0x03`
- selects an exact variable-length triplet stream from the long-pointer table at `C7:0D18` using selector `1E05`
- streams that body through `$2141/$2142/$2143`
- normalizes `84 = 0xE0`

Then it enters the second command-`0x03` burst phase:
- computes exact offset `36 * selector`
- seeds exact source pointer to `C7:1871 + 36*selector`
- sends exact header:
  - `$2143 = 0xF1`
  - `$2142 = 0x20`
  - `$2141 = 0x03`
- streams an exact fixed 12-triplet body through `$2141/$2142/$2143`

Then it finishes exactly:
- writes exact reset/terminator byte `0xE0`
- stores `1E05 = 0xE0`
- calls `0A12`
- exits through common dispatcher exit `0192`

So the strongest safe reading is:

> `C7:04B1..061B` is the exact post-emit tail of the negative-`1E05` special sound-command path, updating latch/current-slot state and then sending two exact command-`0x03` burst phases before cleanup.

That closes the specific seam pass 95 left open.

---

## 6. The adjacent `0x18..0x3F` bridge tightened “for free” from the same bytes

Because the same pocket was open, I also froze the immediate bridge just next to the seam.

### `061C..064F`
Exact behavior:
- sends exact bytes `1E03 / 1E02 / 1E01 / 1E00` through `$2143/$2142/$2141/$2140`
- retries until `$2140` echoes the opcode byte
- if `1E00 == 0xFC`, compares exact selector low nibble `1E01 & 0x0F` against exact local byte `F0` and calls `09FD` when they differ
- exits through common dispatcher exit `0192`

Strongest safe reading:
> exact immediate 4-byte APU packet sender for the `0x18..0x2F` family, with one exact `0xFC` threshold-fixup case.

### `071D..0733`
Exact behavior:
- masks exact opcode byte `1E00` to its low nibble
- multiplies by four and indexes the exact table at `C7:0A98`
- seeds exact packet bytes `1E02` and `1E00` from that table
- tail-jumps back into the shared low-bank send path at `0155`

Strongest safe reading:
> exact table-driven bridge from the `0x30..0x3F` family into the shared low-bank packet-send path.

I am still not claiming the final user-facing noun of every one of those opcodes.
But the bridge shape is now exact.

---

## 7. The live low-bank workspace is tighter now

Pass 95 already proved `1F00..` / `1F20..` / `1F80..` were real.

Pass 96 tightens the live slot side too:
- `1E20..1E3E` = live selector strip
- `1E40..1E41` per slot = exact lower/base pair refreshed by `0655`
- `1E60..1E61` per slot = exact base pair consumed as the command-`0x03` destination/header pair
- `1E62..1E63` per slot = exact base+extent / end pair refreshed by `0655`

So the strongest safe reading is:

> `1E20..1E63` is a real live sound-slot selector/base/end strip family, not generic scratch.

---

## What changed semantically
Before pass 96, the seam still honestly contained this caution:

```text
I have not frozen the exact semantic meaning of helpers 0734, 0A39, 0655,
and the later 04B1..061B tail of the 01A1 path.
```

That caution is no longer true.

After pass 96, the honest wording is:

```text
0734 = exact opcode|=0x04 helper (currently degenerate)
0A39 = exact selector-table-backed APU handshake gate
0655 = exact per-slot command-03 stream helper refreshing 1E40..1E63
04B1..061B = exact post-emit tail with two command-03 burst phases
```

That is the real progress in this pass.

---

## Corrections made this pass
The cleanest correction is `0734`.

Pass 95 only knew it was “a helper called at the top of 01A1.”
Pass 96 proves the stronger truth:

- the scan stub rooted at `0AD8` is currently degenerate in this ROM image
- so the helper currently collapses to exact `1E00 |= 0x04`

That is worth keeping explicit.

---

## Honest caution
I am still keeping a few things below frozen:
- the final user-facing audio noun of every `0x18..0x3F` packet
- the precise gameplay-facing meaning of latch pair `1E10 / 1E11`
- the first exact clean-code external reader of `CE0F`

But the specific helper fog around the negative-`1E05` seam is now gone.

---

## Next recommended target
Do **not** go broad.

The cleanest next move now is:
1. tighten `0155` and the immediate bridge around the `0x18..0x3F` family while the C7 low-bank send path is still warm
2. then go back to the first exact clean-code external reader of `CE0F`
