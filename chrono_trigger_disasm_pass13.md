# Chrono Trigger (USA) — Disassembly Pass 13

## What this pass focused on

This round decoded the previously identified high-opcode VM cluster around:

- `0x84`
- `0x87`
- `0x89..0x92`

The goal was to answer whether this block was still mostly **palette/appearance work**, or whether it actually pivoted into another subsystem.

---

## Biggest conclusion

## The `0x89..0x92` cluster is primarily a **movement / placement control block**, not a pure visual-state block

That is the major correction from this pass.

The cluster still sits right next to palette-related handlers (`0x88` in particular), but once execution moves past the palette parser the code is mostly about:

- movement magnitude / speed bytes
- current-slot coordinate writes
- coordinate writes from variables
- mode/state bytes tied to map/tile refresh
- movement-init flags
- target-follow / directed movement setup

So the high-opcode area is better described as a **slot state + placement + motion setup zone**.

---

## Hard handler findings

## opcode `0x84` -> `C0:4867`
### `Set_CurrentSlot_1B01_FromImm8`

This is very small and direct:

- consumes one immediate byte from `7F:2001`
- stores it to `1B01,X`

From other code already known in the VM/runtime, `1B01` bit `0` is checked by logic around `C0:5BDB`, strongly suggesting it is some kind of **slot behavior / participation / collision-search flag byte**, not random scratch state.

I am intentionally not over-naming it further yet.

---

## opcode `0x87` -> `C0:4876`
### `Set_CurrentSlot_Paired1000_1001_FromImmPlus1_PreserveBit7`

This one:

- reads one immediate byte
- increments it
- preserves bit `7` from the current `1000,X`
- writes the merged value to both:
  - `1000,X`
  - `1001,X`

This is clearly a **paired state-byte write**, but the exact gameplay meaning is still not locked.

What is solid:

- low 7 bits come from script byte + 1
- bit 7 is preserved from previous state
- the value is mirrored into both `1000` and `1001`

So this is not palette work. It is slot-state setup.

---

## opcode `0x89` -> `C0:4B49`
### `Set_CurrentSlot_1A00_FromImm8`

- consumes one immediate byte
- stores it to `1A00,X`

## opcode `0x8A` -> `C0:4B58`
### `Set_CurrentSlot_1A00_FromVarByte`

- consumes one variable index byte
- loads a byte from `7F:0200`
- stores it to `1A00,X`

These two handlers are a matched pair.

The important structural point is what later code does with `1A00`:

- routines like `C0:AC69` use `1A00,X` as the multiplicand for direction-table math
- that produces signed per-axis motion values into `1900/1980`

So `1A00` is now strongly best understood as a **movement magnitude / speed byte**.

That is a real upgrade from the earlier “unknown movement-related state” bucket.

---

## opcode `0x8B` -> `C0:4B74`
### `Set_CurrentSlot_Coords8_Immediate_AndMaybeRefreshTileAttrs`

This handler consumes two immediate bytes and writes:

- first byte -> `1801,X`
- second byte -> `1881,X`

It also seeds:

- `1800,X = 0x80`
- `1880,X = 0xFF`

So this is not writing arbitrary bytes. It is constructing two 16-bit slot position words with fixed low-byte defaults.

That means:

- `1800/1801`
- `1880/1881`

are strongly a **pair of 16-bit position words**, and the script is here supplying the coarse/high-byte components while low bytes are seeded to defaults.

If `0F80,X` is negative, the routine also recomputes `0C00/0C01` using the table at:

- `7E:7000`
- `7E:7040`

through the composite index formed from `1881:1801`.

So this handler is best described as:

- write 8-bit coarse coordinates
- seed fine bytes to defaults
- maybe refresh tile/placement side data

---

## opcode `0x8C` -> `C0:4BC3`
### `Set_CurrentSlot_Coords8_FromVars_AndMaybeRefreshTileAttrs`

This is the variable-table counterpart to `0x8B`.

It:

- consumes two variable indices
- fetches two bytes from `7F:0200`
- writes them to `1801,X` and `1881,X`
- seeds `1800/1880` exactly like `0x8B`
- conditionally refreshes `0C00/0C01` the same way

So `0x8B` and `0x8C` are a clean immediate/variable pair.

---

## opcode `0x8D` -> `C0:4C27`
### `Set_CurrentSlot_Coords16_Immediate_AndMaybeRefreshTileAttrs`

This is the 16-bit counterpart.

It consumes two 16-bit words from the stream and writes them directly to:

- `1800,X`
- `1880,X`

Unlike `0x8B/0x8C`, there is no default low-byte seeding because the full words are already supplied by script.

Then, if `0F80,X` is negative, it recomputes the same `0C00/0C01` side state using the high-byte pair (`1881:1801`) as the lookup index.

So the position-field model is now much stronger:

- `1800/1880` are full 16-bit coordinate words
- `1801/1881` are the coarse/high-byte components used by map/tile side logic
- `0x8B`, `0x8C`, and `0x8D` are the main script-side coordinate setters

---

## opcode `0x8E` -> `C0:4C74`
### `Set_CurrentSlot_0F80_Mode_AndRefreshTileAttrs`

This handler writes one immediate byte to `0F80,X`.

Then it does one of two things:

### If bit 7 is set:
- it recomputes `0C00/0C01` from the `7E:7000 / 7E:7040` tables using current coarse position
- it sets `0F01 = 0xFF`
- it clears `1601`

### If bit 7 is clear:
- it derives `0C00/0C01` directly from bits `4-5` of the mode byte
- it still sets `0F01 = 0xFF`
- it still clears `1601`

So `0F80` is clearly not just a cosmetic byte.

It is a **placement/render/tile-mode control byte** that influences how side state is refreshed.

I am still intentionally avoiding a fake-precise name like “facing byte” or “terrain byte,” because the code supports a broader interpretation than that.

---

## opcode `0x90` -> `C0:4CD5`
### `Set_CurrentSlot_1A81_Positive`

This simply stores:

- `1A81,X = 0x01`

## opcode `0x91` -> `C0:4CE0`
### `Clear_CurrentSlot_1A81`

This simply stores:

- `1A81,X = 0x00`

From wider engine usage already visible elsewhere:

- many routines skip behavior when `1A81 <= 0`
- negative values take a special path in a few places
- positive values participate in world/update logic

So the grounded read is:

`1A81` is some kind of **slot activity/update-participation mode byte**, and `0x90/0x91` are direct script toggles for it.

---

## opcode `0x8F` -> `C0:5429`
### `Start_MoveTowardMappedTargetSlot_WithCollisionFallback` (strong provisional)

This is the most important handler of the pass.

What is solid:

- it consumes one byte argument
- maps it through `$97`
- loads another slot
- compares current-slot and target-slot coarse position (`1801/1881`)
- computes a direction via `C0:ABA2`
- uses the facing table at `F700`
- may run `C0:5B95` and choose an alternate direction if blocked
- stores movement-init state into:
  - `1600`
  - `1A01`
  - `7F:0B00`
- calls `C0:ACFD`
- calls `C0:5614`

This is very clearly **movement initialization toward another slot / mapped target**, not palette work.

What is still provisional is the exact high-level gameplay wording:

- chase
- approach
- face-and-move
- follow target slot

The strongest honest wording right now is:

### `Start_MoveTowardMappedTargetSlot_WithCollisionFallback`

because that matches the code behavior without pretending I know the exact script-language designer intent.

---

## opcode `0x92` -> `C0:4E73`
### `Start_DirectionalMove_ImmediateDir_ImmediateDuration` (strong provisional)

This handler now reads cleanly:

- it guards against already-active motion via `1A80`
- reads one immediate byte -> direction index
- uses that as an index into `F700` -> writes `1600`
- reads one immediate byte -> writes `1A01`
- sets `7F:0B00 = 0x80`
- increments `1A80`
- calls `C0:ACFD`
- calls `C0:5614`

That is a very strong movement-init signature.

Best current read:

- first arg = direction / heading selector
- second arg = duration / count / step budget
- `1A80` = motion active flag
- `1A01` = motion count / duration field

So the strongest honest name is:

### `Start_DirectionalMove_ImmediateDir_ImmediateDuration`

There are nearby sibling routines that clearly do related work from variable-table inputs, but `0x92` itself is the immediate-byte version.

---

## Important field upgrades from this pass

## `1A00` is strongly a movement magnitude / speed byte

This is now well supported by the math routines that multiply it by direction-table values to derive per-axis motion.

## `1800/1880` are coordinate words

The script-side coordinate setters make this much clearer now:

- `0x8B/0x8C` seed them from coarse bytes plus fixed low-byte defaults
- `0x8D` writes full 16-bit values directly

## `1A80` is a movement-active flag / in-progress state byte

Multiple movement-init and movement-wait patterns use it exactly this way.

## `1A01` is a movement count / duration / remaining-step field

The exact semantic label is still slightly provisional, but it is clearly the main countdown/amount field for these movement-init commands.

---

## Biggest architectural correction

Earlier I described `0x87..0x92` as probably a broad appearance / palette / slot-visual-state cluster.

That is now too vague and partly wrong.

The better breakdown is:

- `0x88` = palette command parser
- `0x89..0x92` = mostly **motion / placement / activity state** control

So this part of the VM is not “visual-only.”
It is a blended **slot state transition zone** where the engine moves from palette handling into movement/placement control.

---

## Best next target

The best next move is to chase the **movement-update consumers** of:

- `1A80`
- `1A01`
- `1A00`
- `1600`
- `1900/1980`

That should let the current provisional names for the movement-init commands become exact ones.
