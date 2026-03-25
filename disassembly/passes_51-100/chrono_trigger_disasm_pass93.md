# Chrono Trigger Disassembly — Pass 93

## What I targeted
Pass 92 left one clean external bottleneck instead of a fog bank:

- `C2:0003`
- `C2:0009`
- `C7:0004`

I stayed on that seam.

This pass is not fluff.
It freezes those addresses into exact veneers and exact dispatcher roles, and it also explains why the overall percent has looked almost flat for several passes.

---

## Strongest keepable result

The biggest real closure is:

> `C2:0003..0005` is an exact veneer to `C2:57DF`, which initializes the live C2 stream state from the `020C..0214` packet workspace.

> `C2:0009..000B` is an exact veneer to `C2:5823`, which dispatches that prepared state through four exact handler families.

> `C7:0004..0006` is an exact veneer to `C7:0140`, which is the real low-bank `1E00..` packet opcode-family dispatcher.

That means the pass-92 tail is no longer bottlenecked by unnamed engine-facing jump slots.

---

## 1. `C2:0003` and `C2:0009` are just veneers

At bank start:

```text
C2:0003  4C DF 57   JMP $57DF
C2:0009  4C 23 58   JMP $5823
```

So the real bodies are `57DF` and `5823`.

That is already a material cleanup by itself because the pass-92 `CD:025E` chain can now be read as:

```text
seed packet/workspace -> C2:57DF -> C2:5823
```

instead of “call two low-bank externals and hope later.”

---

## 2. `C2:57DF..5822` is an exact stream-state initializer

The body is short and clean enough to freeze structurally.

It does this:

- saves flags and direct page
- sets `D = 0x0200`
- reads `020C`
- masks it to `00FF`
- doubles it
- uses that as `Y`
- reads a **16-bit entry** through exact long-indirect pointer `[020D],Y`
- stores that into `0231`
- copies exact byte `020F -> 0233`

So pass 93 proves something pass 92 could only imply:

- `020D..020F` is not generic scratch
- it is the live long-pointer family consumed by the C2 side of the `CD:025E` packet workspace

Then `57DF` seeds exact local state:

- `0230 = 00`
- `0234 = 00` or `08` depending on exact comparison of `0214` with `02`
- if `0214` is negative, forcibly clears `0234`
- `0215 = 04`
- `023D = 0200`
- `023F = 00`
- `0217 = 00`

Then it returns.

So the strongest safe reading is:

> `57DF` initializes a stream/parser state from the selector + pointer half of the `020C..0214` packet workspace.

I am **not** over-claiming the final subsystem noun of that stream yet.
But the initializer role itself is now exact.

---

## 3. `C2:5823..5841` is an exact four-family dispatcher over that prepared state

`5823` repeats the same direct-page setup (`D = 0x0200`) and then calls local helper `584A`.

If that helper returns carry set, `5823` exits.
If not, it reads exact local mode/state byte `0230`, doubles it, and dispatches through the exact table at `5842`:

- `58B2`
- `5BF5`
- `5C3E`
- `5C77`

Then it clears `A`, restores state, and returns.

That means the safe frozen reading is now:

> `5823` is the token/stream dispatch stage over the state seeded by `57DF`, and it has four concrete downstream handler families.

Again, I am keeping the final subsystem noun one notch below frozen.
But the dispatcher role is now exact.

---

## 4. `C7:0004` is no longer a generic “packet submitter” mystery slot

At bank start:

```text
C7:0004  4C 40 01   JMP $0140
```

So the real body is `C7:0140`.

`0140` does this immediately:

- saves `B`, `D`, flags, `A`, `X`, and `Y`
- sets exact direct page to `D = 0x1E00`
- forces `DB = 0x00`
- reads exact header bytes from the `1E00..` workspace, including `1E00` and `1E05`

Then the packet split is exact:

- if `1E05` is negative, take the special path at `01A1`
- if `1E00 == 00`, exit
- `0x10..0x17` -> indexed indirect jump through table `0AD9`
- `0x18..0x2F` -> `JMP $061C`
- `0x30..0x3F` -> `JMP $071D`
- `0x70` -> `JMP $08E3`
- `0x71` -> `JMP $0755`
- unsupported / finished paths clear exact byte `1E00` before returning

So the strongest safe reading is now:

> `C7:0004 -> 0140` is an exact low-bank packet opcode-family dispatcher over the `1E00..` command-packet workspace.

This is materially better than the previous generic wording.

---

## 5. Why the completion percentage has barely moved

No-BS answer: the score script is part of the reason.

I checked `scripts/ct_completion_score.py`, and right now it still does this:

- `bank_sep_score = 24.0`
- `rebuild_score = 8.0`

Those are hard-coded constants.

So even when the semantic side moves forward, the top-line completion percent is still heavily anchored by two frozen low components.

That means:

- I am **not** stuck
- the recent passes **have** added real exact structure
- the displayed percentage is just a blunt instrument right now

I am leaving the script alone for this pass so the longitudinal numbers stay comparable.
If we want, the next cleanup pass can improve the scoring model itself.

---

## 6. What this pass changes in practice

Before pass 93, the live tail still had this weak spot:

```text
CD:025E -> C2:0003 -> C2:0009 -> ...
C0:*    -> C7:0004 -> ...
```

After pass 93, that tightens to:

```text
CD packet/workspace seed
-> C2:57DF exact stream-state initializer
-> C2:5823 exact four-family dispatcher

C0 packet builders
-> C7:0140 exact 1E00 packet opcode-family dispatcher
```

That is a real closure, not just wording polish.

---

## Honest caution
I am still keeping a few things below frozen:

- the final high-level noun of the `58B2 / 5BF5 / 5C3E / 5C77` handler families
- the final gameplay-facing noun of the broader pass-88/89 lane+raster workspace
- the first exact clean-code external reader of `CE0F`

But `C2:0003`, `C2:0009`, and `C7:0004` are no longer mystery addresses after this pass.

---

## Best next seam
Do **not** go broad.

The cleanest next move now is:

1. **Freeze the four C2 downstream families next**
   - `58B2`
   - `5BF5`
   - `5C3E`
   - `5C77`

2. **Freeze the first real packet-family bodies behind `C7:0140`**
   - especially the `0x70 / 0x71` path and the `0x10..0x17` table gate

3. **Only after that, circle back to `CE0F`**
   - the engine-facing seam is cleaner now than it was before this pass
