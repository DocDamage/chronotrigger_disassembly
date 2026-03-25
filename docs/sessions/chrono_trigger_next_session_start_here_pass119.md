# Chrono Trigger — Next Session Start Here (Pass 119)

## What pass 119 actually closed

Pass 119 fixed a real bank-ownership bug and then closed the sibling bank-`C2` caller cluster around the settlement/search subsystem.

### Exact correction now frozen

The settlement/search owner band is:

- `C2:8820..C2:991F`

not:

- `C0:8820..C0:991F`

Why this is frozen:

- bank-`C2` callsites use plain absolute `JSR $8820`
- on 65816 that is bank-local
- therefore:
  - `C2:8E5D`
  - `C2:8F99`
  - `C2:A1C3`
  - `C2:A244`
  - `C2:A2DE`
  - `C2:A336`
  target `C2:8820`
- direct byte check confirms `C0:8820` and `C2:8820` are different routines

So the structural work from passes 115–118 survives, but the bank prefix must be corrected moving forward.

---

## New exact closures from pass 119

### `C2:A1B2..A1E8`
- exact full-span linear settlement sweep
- seeds:
  - `71 = 0413`
  - `72 = 0`
  - `61 = 2E00`
- repeatedly runs exact settlement/search service `C2:8820`
- chooses twin post-settlement tail by local `51`
- advances:
  - `INC 71`
  - `61 += 0x0180`
- exits when:
  - `71 >= 85`
  - or `61 >= 3280`

### `C2:A1EF..A215`
- exact selector/threshold gate for the post-settlement tail family
- seeds `0D4D = 9A90 & 7`
- compares selector-derived `0D38,X` against `9A93`
- when table value is not below `9A93`:
  - `0D5D = 4`
  - sets bit `0x20` in `0D4D`

### `C2:A1E9..A21E`
- exact twin post-settlement tails into `ED31`
- `A1E9`:
  - `LDX #BE15`
  - `JMP $ED31`
- `A216`:
  - runs `A1EF`
  - `LDX #BE0E`
  - `JMP $ED31`

### `C2:A21F..A22E`
- exact wrapper chaining:
  - one-shot settlement materializer `A22F`
  - then `61 = 2E00`
  - then `A216`

### `C2:A2CE..A2EC`
- exact one-shot settlement tail
- clears `0D22`
- seeds:
  - `54 = 0412`
  - `71 = 0412 + 0413`
- runs `C2:8820`
- then:
  - `A6F0` with `X = 30A2`
  - `ED31` with `X = BDEF`

### `C2:A2ED..A320`
- exact static block-seed/common-service tail after `A170`
- seeds:
  - `9694 = 969A`
  - `9696 = 9300`
  - `9698 = 0013`
- propagates `61FF` fill across `5D42..5D58`
- runs `9E76`
- finishes through `8385` with `X = FBE3`

### `C2:A321..A38A`
- exact settlement-driven quad-block materializer with three-service fanout
- runs:
  - `ED31` with `X = BE6D`
  - `C2:8820`
  - `A216`
  - `A38B`
- propagates `40FF` fill across `5CC2..5CD8`
- seeds:
  - `9694 = 969A`
  - `9696 = 9300`
  - `9698 = 0025`
- updates:
  - `INC 0D15`
  - `DEC 0D9A`
  - `0D13 = C5`
- fans out through `8385` with:
  - `FBE3`
  - `FBFF`
  - `FC45`

### `C2:A38B..A418`
- exact selector-indexed helper cluster behind `A321`
- `A38B`:
  - `54 -> 77`
  - exact table entry base `A3BA + 10*54`
  - runs `EF65`
  - copies `0x80` bytes from `3040` to `3840`
- `A3BA..A3E1`:
  - exact four-entry table
  - entry size `0x0A`
- `A3E2..A418`:
  - exact four-band marker writer
  - default word `1C0B`
  - selector-matched override word `000B`

---

## What **not** to reopen

Do **not** reopen these as if they belong to bank `C0`:

- `8820..991F`
- `88E5`
- `88ED..8A69`
- `8A6C..8A9D`
- `8AB5..916F`
- `9175..91AB`
- `91AC..93E0`
- `93E1..991F`
- `99DE..9A1E`

Carry them forward as bank-`C2`, not bank-`C0`.

Also do **not** use raw absolute-xref hits in other banks as proof of cross-bank callers for this subsystem.

---

## The real next seam now

Best next targets are same-bank and bank-correct:

1. broader same-bank caller family:
   - `C2:9DB9..9ED0`
   - `C2:A046..A0BA`
   - `C2:A886..`
   - `C2:B002`
   - `C2:BA32`
   - `C2:BEEF`

2. carry-forward cleanup:
   - relabel old pass wording from `C0:8820..991F` to `C2:8820..991F`
   - correct any handoff/dashboard text that still says the settlement/search owner is bank `C0`

3. downstream noun hunt:
   - identify the larger gameplay/system-facing family that owns:
     - `0D4D`
     - `0D5D`
     - `0077`
     - `5CC2..5CD8`
     - `5D42..5D58`

---

## Important carry-forward wording

Carry this exact wording forward:

- `C2:8820..C2:991F` = exact DP=`$1D00` current-slot candidate-offset settlement/search pipeline
- `C2:A1B2..A1E8` = exact full-span linear settlement sweep with post-result twin tail dispatch
- `C2:A1EF..A215` = exact selector/threshold gate for the post-settlement tail family
- `C2:A2CE..A2EC` = exact one-shot settlement tail fanning into `A6F0` and `ED31`
- `C2:A321..A38A` = exact settlement-driven quad-block materializer with three-service fanout
- `C2:A38B..A418` = exact selector-indexed helper cluster behind `A321`
