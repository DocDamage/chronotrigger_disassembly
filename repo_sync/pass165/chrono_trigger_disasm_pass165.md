# Chrono Trigger Disassembly — Pass 165

## Scope
Pass 165 splits the front half of the live seam `C3:08A9..C3:0EF9` into honest owners/helpers/data instead of treating it as one monolithic routine.

## Closed spans
- **`C3:08A9..C3:08B2`** — exact unattached tail fragment ending in exact `RTL`
- **`C3:08B3..C3:0943`** — exact frame/display service wrapper with local setup helper and branch-selected external worker call
- **`C3:0944..C3:099C`** — exact signed multiply / accumulate helper using `4202/4203` and `4216`
- **`C3:099D..C3:09A0`** — exact `FE -> 7E` block-move veneer (`MVN` + `RTL`)
- **`C3:09A1..C3:09A4`** — exact `FE -> 7F` block-move veneer (`MVN` + `RTL`)
- **`C3:09A5..C3:09D8`** — exact change detector / service trigger for state rooted at `0388/0389/038A`
- **`C3:09D9..C3:09E8`** — exact eight-word permutation / index table
- **`C3:09E9..C3:0A8F`** — exact WRAM runtime-code emitter writing a generated stub through `$2180`
- **`C3:0E39..C3:0EF9`** — exact inline ASCII credits text block for Jet Bike Race graphic/design staff

## Why these splits are real
The old seam was hiding several true routine/data boundaries:
- exact `C3:08B2`, `C3:0943`, `C3:099C`, `C3:09A0`, `C3:09A4`, and `C3:0A8F` are real terminal boundaries
- exact `C3:09D9..C3:09E8` is data, not executable flow
- exact `C3:0E39..C3:0EF9` is plain readable staff text, not code

## Findings

### `C3:08A9..C3:08B2`
This is not a clean new callable owner. It is one short orphaned tail fragment ending in exact `RTL`, very likely the back edge of the previous owner. It was frozen as a cautionary fragment so the true routines after it can be split honestly.

### `C3:08B3..C3:0943`
This is one exact frame/display service wrapper. It:
- enters with a real prologue
- calls the local helper at exact `C3:08D0`
- checks state rooted at exact `0392/038C/038D`
- selects one of two external workers (`7E:39BE` vs `7E:398A`)
- finishes by restoring exact `0501` and returning via exact `RTL`

The local sub-body at exact `C3:08D0` waits on PPU/NMI status, updates exact `420C`, manipulates display state through exact `2100`, and performs a short exact `MVN` copy before returning to the wrapper.

### `C3:0944..C3:099C`
This is a compact signed math helper. It:
- samples exact hardware status through `4211`
- writes multiplicands to exact `4202/4203`
- reads the exact product from `4216`
- applies sign correction using exact `F0..F6`
- returns one corrected result via exact `RTL`

### `C3:099D..C3:09A4`
These are two tiny real veneers:
- `099D..09A0` = exact `MVN FE->7E ; RTL`
- `09A1..09A4` = exact `MVN FE->7F ; RTL`

### `C3:09A5..C3:09D8`
This routine watches state at exact `0388/0389/038A`, suppresses redundant work when the tracked value has not changed, and when needed writes a small request block to exact `1E00..1E02` before dispatching the external worker at exact `C7:0004`.

### `C3:09D9..C3:09E8`
This is one exact eight-word ordering table:
- `0000, 0002, 0001, 0003, 0004, 0006, 0005, 0007`

### `C3:09E9..C3:0A8F`
This is the most important closure this pass. It is one exact runtime-code / command-stub emitter that writes bytes through exact `$2180` into WRAM. It:
- seeds exact working accumulators from the eight-word table at `09D9`
- emits literal opcode bytes like exact `A9`, exact `5B`, exact `AD`, exact `85`, and final exact `60`
- advances exact `F2/F4/F6/F8` to synthesize the generated stream
- is externally called from at least exact `C3:1CF3` and exact `C3:4D67`

So this is not a dead helper blob; it is a shared WRAM stub builder.

### `C3:0E39..C3:0EF9`
This is inline ASCII data, not executable logic. It contains Jet Bike Race staff/thank-you text including lines for bike object, road, background, and panel/font credits.

## Strong labels / semantics added
- `C3:08A9..C3:08B2`  `ct_c3_unattached_owner_tail_fragment_ending_in_rtl`
- `C3:08B3..C3:0943`  `ct_c3_frame_display_service_wrapper_with_local_setup_and_branch_selected_external_worker`
- `C3:0944..C3:099C`  `ct_c3_signed_ppu_math_helper_using_4202_4203_and_4216`
- `C3:099D..C3:09A0`  `ct_c3_mvn_fe_to_7e_veneer`
- `C3:09A1..C3:09A4`  `ct_c3_mvn_fe_to_7f_veneer`
- `C3:09A5..C3:09D8`  `ct_c3_change_detector_and_c70004_service_trigger_for_0388_038a_state`
- `C3:09D9..C3:09E8`  `ct_c3_eight_word_permutation_table_0000_0002_0001_0003_0004_0006_0005_0007`
- `C3:09E9..C3:0A8F`  `ct_c3_wram_runtime_code_emitter_writing_generated_stub_bytes_through_2180`
- `C3:0E39..C3:0EF9`  `ct_c3_jet_bike_race_inline_ascii_graphic_design_staff_text_block`

## Corrections made this pass
- corrected the idea that `C3:08A9..C3:0EF9` should be attacked as one single owner
- split real code from inline data and from the two one-instruction `MVN` veneers
- preserved the short leading orphan tail separately instead of forcing it into the next wrapper

## Still unresolved
- **`C3:0A90..C3:0E38`** remains the next real unresolved code body in this family
- the short tail `C3:08A9..C3:08B2` still needs eventual backward attachment to its true previous owner

## Next recommended target
- inspect and close **`C3:0A90..C3:0E38`** next
