# Chrono Trigger (USA) — Disassembly Pass 9

## What this pass focused on

This round stayed on the palette/effect system and pushed from “this is palette math” to a much more concrete result:

- the `0520` table now has a **usable field map**
- the high nibble in `0520` is now a real **effect family selector**
- several families are now identifiable as:
  - palette animation frame copy
  - palette segment rotate left/right
  - timed darken/scale transforms
  - timed brighten/complement transforms

This is the first pass where the descriptor table is starting to look like a real subsystem spec instead of a pile of addresses.

---

## Biggest new conclusion

## The `0520 + n*0C` record is a family-based palette effect descriptor

The update loop in bank `FD` iterates the same `0x0C`-byte records allocated earlier in bank `C0`.

The core updater starts at:

**`FD:E3AC`**

It walks records in `0x0C`-byte steps and dispatches by the **high nibble** of `0520`.

That gives a real family map.

---

## New core routine

## `FD:E3AC` — update one 12-byte palette effect descriptor

This routine does the following:

1. increments `0524`
2. compares `0524` against `0525`
3. when equal, resets `0524` to zero and advances the record
4. reads `0520`
5. uses the **high nibble** as the effect family

That makes `0524/0525` a timing pair:

- `0524` = frame counter / divider counter
- `0525` = divider period or timed-control byte  
  (its sign bit is also tested by some families, so this field is not just a pure delay value)

Best current name:

**`Update_0520PaletteFxDescriptor`**

---

## The effect family map is now much clearer

After the timing gate, `FD:E3AC` dispatches on `0520 >> 4`.

### Family map

- `0x1x` → `FD:E437`
- `0x2x` → `FD:E532`
- `0x3x` → `FD:E4E8`
- `0x4x` → `FD:E82C`
- `0x5x` → `FD:E5A4`
- `0x6x` → `FD:E807`
- `0x7x` → `FD:E57C`
- `0x8x` → `FD:E485`

That is a real family table, not a guess.

---

## `0x1x` family — animated palette-frame copy from bank `F6`

## `FD:E437`

This family computes a source frame offset like this:

- multiplier input A = `0523`
- multiplier input B = `0522 * 2`
- add `0526`
- result becomes source offset in bank `F6`

Then it copies `0522` colors into the destination segment in WRAM.

Concrete implications:

- `0521` = destination start color index
- `0522` = color count
- `0523` = frame index
- `0526` = base source offset inside the preset table

Best current name:

**`Apply_PaletteAnimFrame_FromF6PresetTable`**

This is a palette animation sequence player.

---

## `0x8x` family — animated palette-frame copy from descriptor-supplied long pointer

## `FD:E485`

This is the same basic frame-copy idea as `E437`, but the source base is not fixed to bank `F6`.

It uses:

- `0529` as source pointer low
- `052B` as source bank
- `0523` as frame index
- `0522` as colors-per-frame

Then it copies the selected frame into the WRAM destination segment.

Best current name:

**`Apply_PaletteAnimFrame_FromLongPtr`**

This makes the low nibble behavior much more believable:

for `0x1x` and `0x8x`, the update loop auto-increments `0523` and wraps it by the low nibble of `0520`.

So for those families:

- high nibble = animation family
- low nibble = frame-count-minus-one / wrap control

That is a strong and useful result.

---

## `0x2x` family — rotate palette segment left by one color

## `FD:E532`

This routine:

- computes the start/end of the palette segment from `0521` and `0522`
- saves the first color from `7E:2000` and `7E:2200`
- shifts following colors down into the current position
- writes the saved first color into the last slot

That is a classic rotate-left over a color segment.

Best current name:

**`Rotate_PaletteSegmentLeft_2000_2200`**

---

## `0x3x` family — rotate palette segment right by one color

## `FD:E4E8`

This is the mirror image of `E532`.

It:

- saves the last color in the segment
- shifts previous colors upward into the current slot
- writes the saved last color into the first slot

Best current name:

**`Rotate_PaletteSegmentRight_2000_2200`**

So the `0x2x / 0x3x` families are now firmly identifiable as palette rotation effects.

---

## `0x5x` and `0x7x` families — darken/scale transform group

## `FD:E5A4`

This routine uses:

- `0527` as the current transform amount
- `0528` as a bound/limit
- `0526` as an inner mode selector
- `0521/0522` to locate the affected palette segment

It then dispatches to the darken/scale inner transform set:

- `E64F`
- `E6A1`
- `E6D1`
- `E708`
- `E737`
- `E779`
- `E7C0`

These routines all operate on the `7E:2000` source palette and write transformed output to `7E:2200`.

This is the **scale/darken** family.

Best current name:

**`Apply_PaletteScaleTransform_Family5x`**

## `FD:E57C`

This is the stepped controller around that transform group.

It updates `0527` using `0523`, compares/clamps against `0528`, and then feeds the result into the same transform path.

Best current name:

**`Step_PaletteScaleTransform_Family7x`**

So:

- `0x5x` = direct/current-amount scale transform
- `0x7x` = stepped or ramped scale transform

That is the strongest current interpretation.

---

## `0x4x` and `0x6x` families — brighten/complement transform group

## `FD:E82C`

This is the companion dispatcher for the other color-math family.

It uses the same descriptor style as `E5A4`, but calls the complementary inner routines:

- `E8D7`
- `E935`
- `E962`
- `E98F`
- `E9CA`
- `EA11`
- `EA5C`

These routines use complement-style math against the channel maxima before blending the result back, which makes them a much better fit for **brighten / approach-max / inverse-blend** effects than for simple darkening.

Best current name:

**`Apply_PaletteBrightenTransform_Family4x`**

## `FD:E807`

This is the stepped/ramped controller for that family.

Best current name:

**`Step_PaletteBrightenTransform_Family6x`**

So:

- `0x4x` = direct/current-amount brighten transform
- `0x6x` = stepped or ramped brighten transform

---

## Descriptor field map — current best interpretation

This is now strong enough to write down as a working field map.

### Common fields

For record base `R = 0520 + slot*0C`:

- `R+0` (`0520`) = family/type byte
  - high nibble = effect family
  - low nibble = family-dependent parameter  
    especially frame-wrap control for `0x1x` / `0x8x`
- `R+1` (`0521`) = start color index in the palette bank
- `R+2` (`0522`) = number of colors in the segment
- `R+4` (`0524`) = frame/divider counter
- `R+5` (`0525`) = divider/mode byte (sign bit is meaningful for timed transform families)

### Family-dependent payload

#### `0x1x / 0x8x`
- `R+3` (`0523`) = current frame index
- `R+6` (`0526`) = base source offset (preset-table family) or family-specific data
- `R+9` (`0529`) = source pointer low (long-pointer family)
- `R+11` (`052B`) = source bank (long-pointer family)

#### `0x2x / 0x3x`
- `R+1` = segment start color
- `R+2` = segment length

#### `0x4x / 0x5x / 0x6x / 0x7x`
- `R+3` (`0523`) = per-step delta / rate
- `R+6` (`0526`) = inner transform mode selector
- `R+7` (`0527`) = current amount / progress / intensity
- `R+8` (`0528`) = target/bound/limit

I am still keeping this as a **working** spec, not a final one, but it is much stronger than before.

---

## Palette bank roles are also tighter now

This pass reinforces the split we were already seeing:

- `7E:2000` = source/current palette bank
- `7E:2200` = transformed/working destination bank

The `0x2x/0x3x` rotation families operate on both banks together, and the transform families consistently read from `2000` and write into `2200`.

That makes the `2000 -> 2200` relationship real and repeatable.

I still have not fully pinned down the exact runtime roles of `7E:2100` and `7E:2300`, but they remain strongly associated with the template-install paths in bank `C0`.

---

## Honest status after this pass

What is now strong:

- descriptor size = `0x0C`
- `FD:E3AC` is the main descriptor updater
- `0520` high nibble is the family selector
- `0x1x` / `0x8x` are palette animation frame players
- `0x2x` / `0x3x` are palette segment rotators
- `0x4x` / `0x6x` are brighten-style transform families
- `0x5x` / `0x7x` are darken/scale transform families
- `0521/0522` really are segment start/count
- `0527/0528` really behave like current amount / limit

What is still not locked:

- the exact semantic meaning of every `0526` inner mode
- the full meaning of the sign bit in `0525`
- the exact runtime role split between `2100` and `2300`

But this pass turns the palette/effect system into a much more usable implementation target.

---

## Best next target

The next clean move is to map the **inner mode selector** in `0526`.

That should let me turn:

- “darken family”
- “brighten family”

into:

- scale all channels
- scale only one channel
- scale two channels
- complement-blend one/two/all channels
- etc.

That would finish the per-effect-family spec instead of stopping at the family dispatcher level.
