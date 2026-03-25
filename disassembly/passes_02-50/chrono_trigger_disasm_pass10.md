# Chrono Trigger (USA) — Disassembly Pass 10

## What this pass focused on

This round stayed on the palette/effect system and drilled into the last big unknown from pass 9:

- the **`0526` inner mode byte**
- the exact inner transform targets behind the `5x/7x` scale families
- the exact inner transform targets behind the `4x/6x` brighten families
- the stepped-family prelude in `FD:E57C` / `FD:E807`

This pass turns `0526` from “some inner selector” into a real implementation table.

---

## Biggest conclusion

## `0526` is a family-local inner transform selector

The transform families all route through the same outer pattern:

1. timing gate / amount preparation
2. `0521 * 2 -> X` for color-word offset
3. `0522 -> Y` for color count
4. dispatch on `0526`

What matters is that `0526` is **not just a generic strength byte**.

It is the **mode selector for which color-field combination gets transformed**.

The evidence is in the dispatch chains at:

- `FD:E5ED..E623` for the scale/darken family
- `FD:E875..E8AB` for the brighten family

---

## The common setup before inner dispatch

Both outer dispatchers do the same important setup just before reading `0526`:

- `0521` is doubled and moved into `X`
- `0522` becomes the loop count
- the effective transform amount is already sitting in `$4202`

That means the inner routines are pure “apply transform to selected field mask(s)” workers.

This is why the inner mode table is now safe to write down.

---

## `5x / 7x` scale-family inner mode table

The scale/darken family eventually jumps through this chain:

- mode `00` -> `FD:E64F`
- mode `01` -> `FD:E7C0`
- mode `02` -> `FD:E737`
- mode `03` -> `FD:E6A1`
- mode `04` -> `FD:E779`
- mode `05` -> `FD:E6D1`
- mode `06` (and fallthrough/default) -> `FD:E708`

### What each inner routine really does

These are field-based transforms over the SNES 15-bit color word:

- **high field** = bits `10-14` (`0x7C00`)
- **mid field** = bits `5-9` (`0x03E0`)
- **low field** = bits `0-4` (`0x001F`)

### Scale-family mapping

- `00` -> scale **all three fields** -> `FD:E64F`
- `01` -> scale **high + mid** -> `FD:E7C0`
- `02` -> scale **high + low** -> `FD:E737`
- `03` -> scale **high only** -> `FD:E6A1`
- `04` -> scale **low + mid** -> `FD:E779`
- `05` -> scale **mid only** -> `FD:E6D1`
- `06` -> scale **low only** -> `FD:E708`

That gives a real per-mode table for the `5x/7x` family.

---

## Why those scale mappings are solid

### `FD:E64F` — all fields
This routine individually scales:

- `0x7C00`
- `0x03E0`
- `0x001F`

and recombines them into `7E:2200,X`.

### `FD:E6A1` — high field only
This routine scales only the high field and preserves the remaining `0x03FF` bits.

### `FD:E6D1` — mid field only
This routine preserves `0x7C1F` and only scales the `0x03E0` field.

### `FD:E708` — low field only
This routine preserves `0x7FE0` and only scales the `0x001F` field.

### `FD:E737` — high + low
This routine scales the high field, scales the low field, preserves the mid field.

### `FD:E779` — low + mid
This routine preserves the high field, scales the low field, scales the mid field.

### `FD:E7C0` — high + mid
This routine scales the high field, preserves the low field, scales the mid field.

So the mode table is not guesswork anymore.

---

## `4x / 6x` brighten-family inner mode table

The brighten/complement family uses a different dispatch order:

- mode `00` -> `FD:E8D7`
- mode `01` -> `FD:E962`
- mode `02` -> `FD:E98F`
- mode `03` -> `FD:EA5C`
- mode `04` -> `FD:E935`
- mode `05` -> `FD:E9CA`
- mode `06` (and fallthrough/default) -> `FD:EA11`

### Brighten-family mapping

- `00` -> brighten **all three fields** -> `FD:E8D7`
- `01` -> brighten **low only** -> `FD:E962`
- `02` -> brighten **mid only** -> `FD:E98F`
- `03` -> brighten **low + mid** -> `FD:EA5C`
- `04` -> brighten **high only** -> `FD:E935`
- `05` -> brighten **high + low** -> `FD:E9CA`
- `06` -> brighten **high + mid** -> `FD:EA11`

Important: this is a **different numeric ordering** from the scale family.

So the honest conclusion is:

**`0526` is family-local, not globally normalized across all transform families.**

That matters for any future editor/spec.

---

## Why the brighten mappings are solid

These routines all use the same complement-style pattern:

1. isolate one or more fields
2. XOR against the field maximum (`0x1F`, `0x7C`, or `0xF8`)
3. multiply by the prepared amount
4. add the original field back in
5. write the recombined result into `7E:2200`

That is why these are brighten/approach-max transforms rather than scale-down paths.

Per-routine proof pattern:

- `FD:E935` updates only the high field in `7E:2201`
- `FD:E962` updates only the low field in the color word
- `FD:E98F` updates only the mid field
- `FD:E9CA`, `FD:EA11`, `FD:EA5C` update the corresponding two-field combinations
- `FD:E8D7` updates all three

---

## The stepped-family prelude is now much clearer too

## `FD:E57C` — stepped scale-family controller (`7x`)

This prelude does:

- `0527 += 0523`
- take the absolute value of `0527`
- multiply by `0528`
- invert the result before loading `$4202`
- branch into the same inner dispatch tail used by `FD:E5A4`

That makes this routine look like a **signed phase/ramp controller** that converts phase into a darken/scale amount.

Best current interpretation:

- `0523` = signed delta / step rate
- `0527` = signed phase/progress accumulator
- `0528` = peak intensity / bound
- effective scale amount is derived from `abs(phase) * peak`, then inverted for darkening

## `FD:E807` — stepped brighten-family controller (`6x`)

This is the brighten companion.

It does the same signed-accumulator style setup, but **does not invert** the multiplier result before entering the brighten inner dispatch tail.

That fits a stepped brighten ramp:

- `0527 += 0523`
- `abs(phase) * peak` becomes the effective brighten amount
- then `0526` selects which field mask(s) to brighten

So pass 9’s “stepped family” reading is now much stronger.

---

## What this changes about the descriptor spec

The working spec for transform families is now much better:

### `4x / 5x`
direct transform families

- `0523` = direct step amount / delta
- `0526` = family-local inner mode selector
- `0527` = current transform amount
- `0528` = bound / target

### `6x / 7x`
stepped phase-driven families

- `0523` = signed phase delta
- `0526` = family-local inner mode selector
- `0527` = signed phase/progress accumulator
- `0528` = peak intensity

I am still avoiding a final claim about the exact meaning of the sign bit in `0525`, but `0526` is now pinned down enough that the transform subsystem is genuinely spec-worthy.

---

## Honest status after this pass

What is now strong:

- `0526` is the inner transform selector
- the scale-family mode table is known
- the brighten-family mode table is known
- the stepped-family prelude behavior is much clearer
- the numeric mode order is **not identical** between scale and brighten families

What is still not fully locked:

- the full authoring-side meaning of `0525`
- where each family/mode combination is created upstream in content data
- the exact runtime role split of WRAM palette banks `2100` and `2300`

But this pass closes the biggest remaining gap inside the palette-effect system.

---

## Best next target

The next clean move is upstream, not downstream:

- trace where the `4x/5x/6x/7x` descriptors are built
- identify what source data chooses `0526`
- map whether content uses named effect presets or raw per-record fields

That is the shortest path from “reverse-engineered runtime” to “editable palette-effect spec.”
