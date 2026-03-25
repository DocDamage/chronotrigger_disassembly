# Chrono Trigger (USA) SNES ROM — Master Session Handoff

## Purpose of this handoff

This file is the **master handoff for the entire reverse-engineering/disassembly session** on the uploaded ROM:

- `Chrono Trigger (USA).sfc`

It is meant to let a future session pick up cold without losing context, repeating solved work, or hallucinating subsystem names that were not actually proven.

This handoff covers:

1. the ROM identity and starting assumptions,
2. the external research baseline used for context,
3. everything actually accomplished this session,
4. the current architectural understanding of the ROM,
5. the labels and subsystem mappings that are strong enough to keep,
6. what is still unresolved,
7. the concrete work still required to complete a serious disassembly of this ROM,
8. the artifact files generated during this session.

---

## Session stance / methodology

The approach used in this session was:

- use **public Chrono Trigger research/docs only as context anchors**
- keep all real conclusions grounded in the uploaded ROM
- avoid inventing subsystem names unless the code path justified them
- correct earlier assumptions when control flow or dataflow disproved them
- preserve uncertainty explicitly instead of papering over gaps

That matters because this session did **not** produce a fake “complete disassembly.”
It produced a growing body of **verified subsystem-level reverse-engineering** and a much stronger map of the ROM.

---

## ROM identity

### Uploaded ROM
- `Chrono Trigger (USA).sfc`

### Verified fingerprint
- Size: `4194304` bytes (`0x400000`)
- CRC32: `2D206BF7`
- MD5: `a2bc447961e52fd2227baed164f729dc`

### ROM profile used throughout the session
- Headerless
- 4 MiB
- HiROM
- FastROM
- USA SNES build

That fingerprint was used as the fixed reference point for all later address work.

---

## External research baseline used this session

Public references were used only as **context anchors**, not as substitutes for ROM analysis.

The main contextual sources used were:

- **Chrono Compendium** modding / utility documentation
- **Data Crystal** technical profile / RAM-map / text-table references
- the general Chrono Trigger hacking ecosystem around **Temporal Flux**, **Geiger docs**, and related utilities

These references were useful for:
- confirming the ROM profile,
- confirming that Chrono Trigger already has a mature hacking scene,
- checking whether a full public disassembly already exists,
- avoiding rediscovery of already-documented basics.

The actual subsystem conclusions below came from the ROM itself.

---

## Executive summary of what this session accomplished

By the end of this session, the reverse-engineering state moved from:

- “known ROM, unknown codebase”

to:

- a **confirmed boot chain**
- a **confirmed descriptor-driven init/decompress path**
- a **confirmed 7F:2000 slot/object script VM**
- a **confirmed palette/effect subsystem tied directly into that VM**
- a **confirmed movement / facing / motion-integrator layer**
- a **confirmed camera-relative bucket system feeding render traversal**
- a **confirmed OAM/metasprite cache pipeline**
- a **partially decoded template/chunk/metasprite source system**
- a **confirmed bank-C1 relation-query service**
- a **confirmed bank-C1 multi-table CC-stream command interpreter**

That is a major jump in real understanding, even though the ROM is **not yet fully disassembled**.

---

## Current high-confidence architecture map

## 1. Boot / hardware / early init

### Confirmed chain
- `00:FF00` → reset stub
- `FD:C000` → low-level hardware bootstrap
- `C0:000E` → first main boot stage

### Strong boot/init labels
- `C0:0B4E` = disable display / interrupts / DMA / HDMA
- `C0:0B64` = install NMI RAM trampoline at `00:0500`
- `C0:0B75` = install IRQ RAM trampoline at `00:0504`
- `C0:0B86` = main runtime state reset/seed
- `C0:092B` = select 14-byte init descriptor
- `C0:00F4` = descriptor-driven init loader group
- `C0:2DF1` = WRAM zero-fill via DMA using Mode-7 multiplier result register as constant-zero source
- `C0:2E1F` = boot error / color hang path
- `C0:B1B2` = VRAM DMA queue processing
- `C0:EA63` = native NMI handler entry
- `C0:ECCC` = native IRQ handler entry

### What this means
The startup path is not opaque anymore. It is a layered boot sequence that:
- installs interrupt trampolines,
- resets direct-page/global state,
- selects descriptor records,
- loads/decompresses startup data,
- initializes rendering-related tables and VRAM work queues.

---

## 2. Descriptor-driven load/decompress path

### Core result
`C3:0002` / `C3:0557` is the main **WRAM decompression engine**.

### Strong labels
- `C3:0002` = decompression entry
- `C3:0557` = decompression core
- `C3:08A4` = decompressor return-length epilogue

### What is proven
- writes through SNES WRAM ports (`2180-2183`)
- consumes command/control bytes
- performs same-bank backreference copies
- is an LZ-style expansion path, not memcpy

### Main descriptor-driven load sites confirmed this session
- `C0:6DCF` = descriptor-selected decompress to `7F:5000`
- `C0:A33B` = descriptor-selected decompress to `7E:B500`, then display/BG-config parse
- `C0:56D4` = descriptor-selected decompress to `7F:2000`, then runtime build/orchestration

---

## 3. 7F:2000 subsystem — slot/object script VM

### Core result
The `7F:2000` path is not a generic blob loader.
It is a **slot/object script VM + scheduler + state-builder**.

### Strong labels
- `C0:56A6` = build runtime slots from `7F:2000`
- `C0:5709` = initialize slot work tables from `7F:2000` slot count
- `C0:58DE` = build slot command state from primary stream
- `C0:595C` = run secondary `7F:2000` command stream
- `C0:59D9` = refresh runnable slot linked list
- `C0:5A46` = time-budgeted slot scheduler
- `C0:5A93` = bounded slot command burst
- `C0:5CC7` = validate `7F:2000` header/size
- `C0:5CED` = initialize `7F:3700` template blocks
- `C0:5D6E` = slot VM opcode table
- `C0:5F6E` = fatal invalid opcode path
- `C0:6240 / 624B / 6254` = set busy / clear busy / terminate slot

### What is proven
- `7F:2000` begins with slot-counted/runtime-driving data
- per-slot work tables are built from it
- command streams are parsed from it
- scheduler-linked lists are built from it
- it is a scriptable object/slot runtime, not just static init data

---

## 4. Palette/effect subsystem

### Core result
A substantial palette/effect system hangs directly off the object VM.

### Strong labels / findings
- `C0:4892` = palette command parser (primary/stream-fed)
- `C0:4A4E` = palette command parser (runtime/absolute)
- `C0:4B2C` = find free 0520 descriptor slot
- `FD:E2C0` = preset palette descriptor seeder
- `FD:E3AC` = palette descriptor updater
- `FD:E437` = animation frame copy from F6 preset table
- `FD:E485` = animation frame copy from long pointer
- `FD:E4E8` / `FD:E532` = rotate palette segment right / left
- `FD:E64F` = palette scale/darken family path
- `FD:E8D7` = palette brighten/blend family path

### Descriptor findings
`0520 + n*0C` records are real 12-byte palette/effect descriptors.

Strong field meanings:
- high nibble of `0520` = effect family
- `0521` = start color index
- `0522` = segment color count
- `0524` = timer/cadence
- `0525` = period/delay
- `0526` = family-local inner transform selector
- `0527/0528` = progress/target-like or step/ramp-related state
- `0523` = family-local state (frame index for anim families; step/ramp seed for transform families)

### Effect-family map (strong enough to keep)
- `1x` = preset-table palette animation frame copy
- `8x` = long-pointer palette animation frame copy
- `2x` = rotate-left segment
- `3x` = rotate-right segment
- `5x / 7x` = darken/scale families
- `4x / 6x` = brighten/complement/brighten-like families

### Architectural consequence
Palette/effect behavior is not an isolated renderer utility.
It is **driven directly by the object VM command streams**.

---

## 5. Movement / placement / facing / integrator layer

### Core result
The object VM directly owns a real movement layer with:
- speed/magnitude,
- per-slot movement state,
- signed motion deltas,
- angle-derived facing,
- multiple movement update paths.

### Strong labels / state meanings
- `1A01` = active movement timer / remaining-step count
- `1A80` = movement-in-progress state
- `1B80` = movement integrator/update mode selector
- `1A00` = movement magnitude / speed byte
- `1900/1980` = signed motion-vector components
- `1600` = coarse 4-way facing
- `0F80` = per-slot mode/control byte set by one of the movement opcodes

### Strong routines
- `C0:ABA2` = compute 8-bit angle index from target/current coarse coords
- `C0:AC69` = convert angle index + speed to signed motion deltas
- `C0:AA07` = active movement update path with clamp/wrap behavior
- `C0:AAC7` = alternate / fractional movement integrator
- `C0:AAFD` = signed-delta-to-position update path

### Architectural consequence
This is not “just 4-way JRPG movement.”
The engine is synthesizing motion from an **8-bit angle index plus lookup tables** and then deriving coarser/final state from that.

---

## 6. Camera-relative spatial buckets and render traversal

### Core result
After movement updates, active slots are **rebucketed into camera-relative spatial linked lists**, and those lists are later traversed for rendering.

### Strong labels / meanings
- `C0:A88D` = active-region membership updater
- `C0:A947` = lighter region test
- `C0:A98A` = bucket remove
- `C0:A9CD` = bucket insert
- `0F00` = active-region flag
- `0E00` = bucket head table
- `0E80` = prev-link table
- `0E81` = next-link table
- `0E01` = membership sentinel-like state

### Render handoff proof
- `C0:B2A0` walks the 64 bucket heads
- follows `0E81` links
- hands each live slot to `C0:B309`
- unused output records get hidden with OAM-style `$E0` Y fill

### Architectural consequence
The spatial buckets are not generic bookkeeping.
They directly feed the sprite/OAM build stage.

---

## 7. Metasprite / OAM cache pipeline

### Core result
The renderer is now understood as a **prepared-cache metasprite system**, not ad-hoc OAM writes.

### Metasprite class selector
`1201 & 3` selects fixed metasprite-size classes:

- class 0 = 4 low-OAM entries
- class 1 = 8
- class 2 = 12
- class 3 = 24

### Strong labels
- `C0:B329` = emit class-0 metasprite
- `C0:B3DF` = emit class-1 metasprite
- `C0:B4B8` = emit class-2 metasprite
- `C0:B5AF` = emit class-3 metasprite
- `C0:B701` = class-aware render-prep / gate

### Cache/materializer paths
- `C0:B8CA` = full class-0 materializer
- `C0:BCDC` = full class-1 materializer
- `C0:C2BF` = full class-2 materializer
- `C0:C73E` / `C0:C73A` = class-3 cache builder / re-anchor-side support
- `C0:C6E7` = 4-sprite X packer / OAM high-byte builder

### Important render buffers
- `7F:4BC0` = low-OAM cache records
- `7F:4F00 / 4F01 / 4B40 / 4B41 / 4F80 / 4F81` = packed OAM high-table bytes
- `1700,X` = per-slot low-OAM cache offset
- `0F80 & 0x0C` = OAM band / sub-buffer selector

### Two confirmed renderer modes
1. **Full materializer path**
   - build/update prepared cache from upstream staging data
2. **Cache re-anchor path**
   - reuse already-prepared cache, recompute anchored X/Y and OAM high bytes only

That split matters because later work should not assume every frame rebuilds from upstream templates.

---

## 8. Template/chunk/metasprite source system

### Core result
Classes 0/1/2 use staged template/frame-block sources; class 3 uses its own source path.

### For classes 0/1/2
- `7F:4800` is **template staging**, not final low-OAM cache
- source frame blocks use class-specific sizes:
  - `0x28`
  - `0x50`
  - `0x78`
- blocks split into:
  - header/chunk-descriptor region
  - signed XY tail

### Chunk helper results
- `C0:E534` = 32-byte chunk copier through `FD:0000`
- `C0:E687` = direct 32-byte chunk copy to `7F`
- `FD:0000` = exact 8-bit bit-reversal table

### Consequence of `FD:0000`
`C0:E534` is a **horizontal tile-flip chunk copier** for 32-byte SNES 4bpp tile chunks.

### Header-descriptor result
Chunk descriptors are 16-bit words using:
- low 11 bits = 32-byte chunk index
- bit `0x4000` = direct-copy vs horizontally-flipped-copy mode

### For class 3
- `C0:E12A` = full class-3 build path
- class 3 does **not** use the `7F:4800 -> 4BC0` materializer path
- class 3 uses:
  - `1200/1280` as class-3 chunk-source pointer sets
  - `1300/1380` as descriptor-tail/source pointer sets
- class-3 cache payload includes:
  - relative XY fields
  - fixed tile bytes
  - fixed attr bytes (`#$22` observed in one builder path)
- class-3 tile layout was observed as a fixed `3 x 8` grid in the solved full-build path

---

## 9. Class-3 preset / source loading

### Core result
Class-3 source pointers can be installed several different ways.

### Strong labels / behavior
- `C0:4476` = 5-byte class-3 preset loader from `E4:F000`
- `C0:4590` = 5-byte preset loader from `E4:F024` with dynamic chunk-source resolution
- `C0:46DF` = 10-byte extended preset loader from `E4:F600`
- `C0:47FE` = decompress-and-install chunk source
- `C0:4845` = direct-install chunk source pointer

### Source-pointer result
- `1300/1380` are seeded from preset-record fields that index the `E4:2300` long-pointer table
- `1200/1280` can come from:
  - fixed preset data
  - direct pointers
  - decompressed installs
  - slot reuse

This is a good place to continue later because it is now obvious that class 3 has a richer content-install path than the smaller metasprite classes.

---

## 10. E4:F600 extended records and downstream timing/state

### Core result
The `E4:F600` 10-byte records are not just setup records for one build call.
Their back half seeds real live runtime state.

### Proven fields / meanings
- `F604` = flags byte
- `F605..F608` = copied into dedicated per-slot arrays
- `F609` = packed timing/phase descriptor

### Strong labels
- `CC:EA5B` = install 10-byte extended-slot records
- `CC:F544` = packed-nibble to phase/reload table helper
- `FF:F97A` = live phase countdown tick
- `C1:3719` = reload countdown tick

### Strong array meanings
- `7E:9700` = flags from `F604`
- `7E:9742` = phase-countdown reload
- `7E:9819` = live phase countdown
- `7E:98C2` = phase step amount
- `7E:989F` = reload countdown seed
- `7E:9897` = live reload countdown

### Important unresolved arrays still alive
- `970B`
- `9716`
- `9721`
- `972C`

These were kept unresolved on purpose where proof was weak.

---

## 11. Geometry / bounds / overlap / local collision

### Core result
A geometry layer was partially mapped from neighboring `97xx` tables and the bounds consumers.

### Strong field meanings
- `9708` = signed X offset table
- `9713` = signed Y offset table
- `971E` = half-width / X extent table
- `9729` = half-height / Y extent table

### Strong routine
- `C1:285A` = build bounds from center + half-extents

### Bounds outputs
- `975A` = min X
- `9770` = max X
- `9765` = min Y
- `977B` = max / terminal Y

### First direct bounds consumers
- `C1:28B0` = active-object rectangle overlap scan, returns classified overlap code (`0`, `0x80`, `0x81`)
- `C1:2926` = object-bounds vs local 16x16 collision-flag-grid test

This means the geometry side is no longer theoretical.
It already feeds overlap and collision decisions.

---

## 12. C1 relation-query subsystem

### Core result
There is a real **mode-dispatched relation/query service** in bank `C1`.

### Strong labels
- `C1:2986` = prepare relation-query workspace and dispatch
- `C1:2D81` = relation-query jump table
- `986E` = query mode
- `986F` = subject slot
- `9870` = arg slot A
- `9871` = arg slot B
- `9872` = flag result
- `9873` = value result

### Solved query handlers
- nearest/farthest slot searches over explicit ranges
- squared-distance metric
- absolute distance-difference metric

### Higher-layer conclusion
This is not raw movement logic.
It is a shared **predicate / target-selection / relation-query** service used by higher-level command wrappers.

---

## 13. C1 function-dispatch veneer and CC-stream command interpreter

### Core result
Bank `C1` is not a loose bag of helpers.
It contains:
- a function-dispatch veneer, and
- a real **multi-table CC-stream command interpreter**.

### Bank-C1 function dispatch
- `C1:0003` / `C1:0045` dispatch by A-register selector
- selector `A=#05` routes into the relation-query block

### Four confirmed CC-stream command tables
- `C1:B80D` = group 0 command table (`0x00..0x28`)
- `C1:B85F` = group 1 command table (`0x00..0x16`)
- `C1:B88D` = group 2 command table (`0x00..0x16`)
- `C1:B8BB` = group 3 command table (`0x00..0x1B`)

### Confirmed dispatch sites
- `C1:874E -> JSR ($B80D,X)`
- `C1:8CE7 -> JSR ($B85F,X)`
- `C1:8D88 -> JSR ($B88D,X)`
- `C1:AC2E -> JSR ($B8BB,X)`

### Confirmed relation-query opcode embeddings
Group 0:
- `0x0C -> 925D`
- `0x0D -> 92A3`
- `0x0E -> 9314`
- `0x0F -> 938D`
- `0x10 -> 93E6`
- `0x11 -> 942A`
- `0x1F -> 9765`

Group 3:
- `0x06 -> A4AF`
- `0x07 -> A4E0`
- `0x17 -> A709`
- `0x18 -> A737`

### Consequence
The relation-query service is not a side utility.
It is embedded directly into the object/command layer as real opcode handlers.

---

## Session chronology by pass

Below is the condensed per-pass progression for this session.

- **Pass 2** — Fingerprinted the ROM, confirmed headerless 4 MiB USA HiROM/FastROM build, mapped reset -> FD:C000 -> C0:000E boot chain, identified NMI/IRQ RAM trampolines, named C0:2DF1 as WRAM zero-fill via DMA, and identified early VRAM DMA queue processing.
- **Pass 3** — Pushed boot/init deeper: identified C0:0B86 as main runtime state reset, C0:092B as 14-byte descriptor selector, C0:00F4 as descriptor-driven init loader group, and C0:B1B2 as VRAM DMA queue processing.
- **Pass 4** — Proved C3:0002/C3:0557 is the core WRAM decompression engine with LZ-style backreferences and WRAM-port writes, not a generic memcpy.
- **Pass 5** — Corrected C0:56D4 control flow, confirmed decompressor length return, identified 7F:2000 validation/header check path, and reclassified C0:A33B as display/BG-config decompress+parse instead of a generic parser.
- **Pass 6** — Stayed on the 7F:2000 lane and showed it builds slot work tables and a time-budgeted scheduler from a slot-counted blob. Named the main slot/scheduler infrastructure and tied it to 7F:2000-derived runtime state.
- **Pass 7** — Mapped the 7F:2000 subsystem far enough to call it a slot/object script VM instead of a generic scheduler. Established var/predicate/slot-control foundations and started decoding opcode-table behavior.
- **Pass 8** — Followed external handlers and discovered a palette/effect subsystem hanging off the VM. Proved 0520+n*0C records are palette-effect descriptors and tied FD bank routines to BGR555 palette math.
- **Pass 9** — Decoded palette descriptor families: animation-copy, rotate-left/right, darken/scale, brighten/complement. Identified 0521/0522 as palette segment start/count and 0527/0528 as progress/target-like fields.
- **Pass 10** — Cracked 0526 as an inner, family-local transform selector. Mapped scale/darken vs brighten families to channel-mask transforms and confirmed mode numbering is family-local, not universal.
- **Pass 11** — Moved upstream into descriptor builders. Identified parser/build routines in C0 that construct palette descriptors from command streams, including actor-relative and runtime/absolute variants.
- **Pass 12** — Proved the palette parsers are direct handlers inside the 7F:2000 slot VM opcode table, tying palette behavior into object/event script execution rather than a separate render-only engine.
- **Pass 13** — Decoded opcode cluster 0x89..0x92 and reclassified it as mostly movement/placement/activity-state commands, with 0x88 remaining palette-related.
- **Pass 14** — Mapped movement internals: 1A01 as active movement timer/steps, 1A80 as movement-in-progress state, 1B80 as movement integrator selector, 1900/1980 as signed deltas, and 1600 as coarse facing derived from an 8-bit angle index.
- **Pass 15** — Followed movement completion/spatial maintenance and found rebucketing logic: active slots are removed/reinserted into camera-relative coarse-cell linked lists after motion updates.
- **Pass 16** — Answered what the movement buckets feed: C0:B2A0/B309 traverse the 0E00 bucket heads and emit sprite/OAM shadow entries, proving the buckets drive render traversal/order.
- **Pass 17** — Decoded render classes: 1201&3 selects fixed metasprite size classes (4/8/12/24 low-OAM entries) and identified class-aware cache builders and OAM band selection.
- **Pass 18** — Resolved class-3 cache support and showed C0:C6E7 packs 4-sprite X MSBs/OAM high bytes, tightening the low-cache/high-cache record understanding.
- **Pass 19** — Shifted to template/source blocks and proved class-local frame-block formats with header regions and signed XY tails feeding 7F:4800 staging.
- **Pass 20** — Cracked E534/E687: header words are 16-bit chunk descriptors with low 11 bits as 32-byte tile-chunk index and bit 0x4000 selecting flipped vs direct chunk copy.
- **Pass 21** — Solved FD:0000 as an exact 8-bit bit-reversal table, proving E534 is a horizontal tile-flip copier for 32-byte SNES 4bpp chunks.
- **Pass 22** — Bridged classes 0/1/2 completely: 7F:4800 is the upstream template staging table that materializes into the 7F:4BC0 prepared render cache and packed OAM-high bytes.
- **Pass 23** — Separated full materializer vs cache-reanchor render paths and showed class-3 runtime emission uses a prepared-cache reuse path rather than a 4800 materializer.
- **Pass 24** — Found the missing full class-3 build path at C0:E12A. Showed class 3 has its own source format, tile upload path, and direct 4BC0 cache construction.
- **Pass 25** — Traced the upstream class-3 source pointers: 1300/1380 are seeded from E4:2300 long-pointer tables, while 1200/1280 can come from presets, direct pointers, decompressed installs, or reused pointers. Identified several preset loaders.
- **Pass 26** — Proved bytes 5..9 of the E4:F600 10-byte extended records are live runtime control/timing data, seeding phase/reload state and downstream timers rather than padding.
- **Pass 27** — Mapped neighboring geometry/profile tables: 9708/9713 as signed X/Y offsets and 971E/9729 as half-extents/radii used to build bounds rectangles at 975A/9765/9770/977B. Kept unresolved extended-slot arrays honest.
- **Pass 28** — Found the first concrete bounds consumers: active-object rectangle overlap classification and local 16x16 collision-flag-grid testing.
- **Pass 29** — Moved one layer up and identified a mode-dispatched relation/query subsystem in C1. Corrected routine starts, proved squared-distance math, and established 986E..9873 as relation-query registers/results.
- **Pass 30** — Traced who seeds the relation-query registers: a bank-C1 object-command/predicate wrapper layer using the C1 bank function-dispatch veneer, with wrappers around query/target-selection use cases.
- **Pass 31** — Closed the loop by finding four explicit C1 CC-stream command jump tables and placing the relation-query/target-selection wrappers as real opcode handlers inside those tables.


---

## Current state: what is actually “done” vs “not done”

## Done enough to trust
These areas are now strong enough to be treated as established working knowledge:

- ROM fingerprint / build identity
- reset and early boot chain
- interrupt trampoline installation
- descriptor-driven init/decompress pipeline
- existence and role of the WRAM decompressor
- `7F:2000` slot/object VM + scheduler existence
- palette/effect descriptor families and much of their runtime/update logic
- direct integration of palette commands into the object VM
- movement magnitude/timer/state/facing/integrator layer
- camera-relative bucket maintenance
- bucket traversal feeding OAM/metasprite emission
- metasprite class sizes and the split between materializer vs re-anchor paths
- class-3 full-build path
- chunk/template source system basics for render assets
- existence and role of the C1 relation-query service
- existence and structure of the C1 CC-stream command tables

## Not done / still incomplete
The ROM is **not yet completely disassembled** in any serious “finished project” sense.

What is still missing includes:

- full code/data separation bank-by-bank
- a rebuildable source tree
- complete opcode specs for the object VM
- complete opcode specs for the C1 CC-stream command groups
- full meaning of all template/chunk header bits
- complete source/content format specs for all metasprite classes
- fully resolved meanings for all extended record tail arrays
- exact decompressor command grammar and compressor counterpart
- fully mapped data tables, script banks, content banks, and subsystem ownership boundaries
- battle-specific vs map/event-specific subsystem separation
- a build pipeline capable of reproducing the original ROM layout

---

## Highest-value unresolved questions

These are the biggest unresolved items left by the end of the session.

## A. Group-1 and group-2 C1 command tables are still mostly opaque
The interpreter skeleton is solved, but:
- group 1 (`B85F`)
- group 2 (`B88D`)
still need handler-by-handler work.

This is one of the most valuable next targets because the command-layer skeleton is now proven.

## B. Most group-0 / group-3 handlers are still unnamed
Only selected relation-query / target-selection handlers are pinned.
The rest of the tables still need semantic decoding.

## C. The full 7F:2000 VM opcode spec is not complete
The VM is real and many handlers are mapped, but the table is not yet fully documented end-to-end.

## D. Template header high bits besides `0x4000` remain unresolved
`0x4000` is solved as flipped-vs-direct chunk mode, but the roles of the other high bits are still not nailed down.

## E. The exact upstream frame/content formats are still incomplete
For classes 0/1/2:
- header-region semantics still need more work

For class 3:
- source pointer installation is better understood, but the content format is not fully specified

## F. The exact meanings of the copied extended-slot arrays are still unresolved
The arrays:
- `970B`
- `9716`
- `9721`
- `972C`
are definitely live, but their exact gameplay/render meaning is not yet proven.

## G. The decompressor is identified functionally, but not fully specified as a file format
The engine role is solved.
The exact token grammar and a rebuild-safe compressor/decompressor spec are still unfinished.

## H. The ROM is not yet split into clean bank-local code/data/source files
This remains a major step before any real “projectized disassembly” can be claimed.

---

## What still needs to be done to complete the disassembly

This section is the straight no-BS completion checklist.

## Phase 1 — stabilize and consolidate the work already done
1. Merge all surviving labels into a single master label database.
2. Normalize address naming style across passes.
3. Re-run entry-point sanity checks so no labels point into the middle of instructions.
4. Build a single “known subsystems” map from the solved passes.

### Deliverables
- master labels file
- bank map
- subsystem map
- corrected entry-point list

---

## Phase 2 — finish the command interpreters
1. Fully decode the `7F:2000` slot/object VM opcode table.
2. Fully decode C1 group 0, 1, 2, 3 command tables.
3. Identify command stream encoding rules and operand conventions.
4. Separate:
   - predicate logic
   - target-selection logic
   - movement logic
   - palette/effect logic
   - render/appearance logic
   - object lifecycle / state logic

### Deliverables
- complete opcode docs
- argument-size/operand-size table
- command family map

---

## Phase 3 — finish the renderer/content side
1. Resolve the remaining template/chunk descriptor bits.
2. Fully document class-0/1/2 frame-block header semantics.
3. Fully document class-3 source record semantics.
4. Identify where prepared render caches are invalidated vs reused.
5. Map all tile-upload and VRAM upload relationships to render classes.

### Deliverables
- metasprite/frame source spec
- tile chunk spec
- render invalidation/rebuild spec
- OAM cache format doc

---

## Phase 4 — finish the movement/geometry/query side
1. Resolve the remaining extended-slot arrays and tie them to live consumers.
2. Finish collision/overlap result consumers.
3. Decode the remaining relation-query modes.
4. Separate map/event/object AI logic from generic geometry services.

### Deliverables
- movement state spec
- geometry/collision spec
- relation-query mode reference
- object-selection / target-selection spec

---

## Phase 5 — classify the whole ROM by subsystem and content type
1. Identify code banks vs data banks vs script banks vs content banks.
2. Separate:
   - render assets
   - metasprite templates
   - palette tables
   - object command streams
   - preset records
   - decompressed-runtime-only structures
3. Tag reused helper banks (e.g. `FD`, `C1`, `C3`) cleanly.

### Deliverables
- bank classification sheet
- code/data ownership map
- content-bank directory

---

## Phase 6 — produce a real assembler project skeleton
1. Choose assembler/toolchain.
2. Split known code into banked source files.
3. Convert proven tables into include/data files.
4. Stub unresolved data as binary includes instead of mis-disassembling it.
5. Add comments referencing solved subsystem behavior.
6. Attempt partial or full rebuilds only after bank ownership is stable.

### Deliverables
- repo skeleton
- banked ASM source tree
- labels / constants includes
- build notes
- partial-rebuild validation plan

---

## Phase 7 — verify and iterate
1. Validate labels against emulation traces.
2. Confirm VM/command handlers with runtime test cases.
3. Confirm render-class assumptions with visual toggles/logging if emulator tooling is used.
4. Confirm collision/query behavior against live object scenarios.
5. Refine names where behavior proves them wrong.

### Deliverables
- verification notes
- corrected labels
- emulator-trace-backed docs

---

## Recommended next-session starting point

If continuing from this session, the highest-value order is:

1. **Finish C1 group-1 and group-2 command tables**
2. **Finish the remaining group-0 / group-3 command handlers**
3. **Close the remaining 7F:2000 VM opcode gaps**
4. **Resolve the unresolved extended-slot arrays**
5. **Finish template-header bit semantics**
6. **Start bank-by-bank source splitting**

That order is better than randomly chasing more helpers because the command/VM layers now form the main semantic spine of the reverse-engineering.

---

## Suggested repo / project structure for the next stage

A practical project layout for continuing this work:

```text
chrono-trigger-disasm/
  README.md
  HANDOFFS/
    chrono_trigger_master_handoff_session1.md
  ROM_INFO/
    checksums.md
    bank_map.md
  LABELS/
    master_labels.txt
    labels_boot.txt
    labels_vm.txt
    labels_palette.txt
    labels_render.txt
    labels_c1_commands.txt
  DOCS/
    boot_init.md
    decompressor.md
    slot_vm.md
    palette_fx.md
    movement.md
    render_oam.md
    class3_sources.md
    relation_query.md
    c1_command_tables.md
  ASM/
    bank_c0.asm
    bank_c1.asm
    bank_c3.asm
    bank_cc.asm
    bank_fd.asm
    bank_ff.asm
  DATA/
    raw_tables/
    unresolved_bins/
    descriptor_tables/
  TOOLS/
    trace_notes/
    scripts/
```

---

## Ground rules for the next session

These rules should be followed so the project does not drift into fake certainty.

1. **Do not relabel unresolved tables just because nearby data looks suggestive.**
2. **Prefer “still unresolved” over bad certainty.**
3. **Keep code/data separation conservative.**
4. **Do not assume battle/map/event ownership without caller proof.**
5. **Preserve corrections when later passes disprove earlier assumptions.**
6. **Treat pass 31 as the current top-of-stack, not any single earlier pass.**

---

## Artifact inventory from this session

These files were generated during the session and should be treated as working materials:

- `chrono_trigger_disasm_pass10.md`
- `chrono_trigger_disasm_pass11.md`
- `chrono_trigger_disasm_pass12.md`
- `chrono_trigger_disasm_pass13.md`
- `chrono_trigger_disasm_pass14.md`
- `chrono_trigger_disasm_pass15.md`
- `chrono_trigger_disasm_pass16.md`
- `chrono_trigger_disasm_pass17.md`
- `chrono_trigger_disasm_pass18.md`
- `chrono_trigger_disasm_pass19.md`
- `chrono_trigger_disasm_pass2.md`
- `chrono_trigger_disasm_pass20.md`
- `chrono_trigger_disasm_pass21.md`
- `chrono_trigger_disasm_pass22.md`
- `chrono_trigger_disasm_pass23.md`
- `chrono_trigger_disasm_pass24.md`
- `chrono_trigger_disasm_pass25.md`
- `chrono_trigger_disasm_pass26.md`
- `chrono_trigger_disasm_pass27.md`
- `chrono_trigger_disasm_pass28.md`
- `chrono_trigger_disasm_pass29.md`
- `chrono_trigger_disasm_pass3.md`
- `chrono_trigger_disasm_pass30.md`
- `chrono_trigger_disasm_pass31.md`
- `chrono_trigger_disasm_pass4.md`
- `chrono_trigger_disasm_pass5.md`
- `chrono_trigger_disasm_pass6.md`
- `chrono_trigger_disasm_pass7.md`
- `chrono_trigger_disasm_pass8.md`
- `chrono_trigger_disasm_pass9.md`
- `chrono_trigger_initial_labels.txt`
- `chrono_trigger_labels_pass10.txt`
- `chrono_trigger_labels_pass11.txt`
- `chrono_trigger_labels_pass12.txt`
- `chrono_trigger_labels_pass13.txt`
- `chrono_trigger_labels_pass14.txt`
- `chrono_trigger_labels_pass15.txt`
- `chrono_trigger_labels_pass16.txt`
- `chrono_trigger_labels_pass17.txt`
- `chrono_trigger_labels_pass18.txt`
- `chrono_trigger_labels_pass19.txt`
- `chrono_trigger_labels_pass2.txt`
- `chrono_trigger_labels_pass20.txt`
- `chrono_trigger_labels_pass21.txt`
- `chrono_trigger_labels_pass22.txt`
- `chrono_trigger_labels_pass23.txt`
- `chrono_trigger_labels_pass24.txt`
- `chrono_trigger_labels_pass25.txt`
- `chrono_trigger_labels_pass26.txt`
- `chrono_trigger_labels_pass27.txt`
- `chrono_trigger_labels_pass28.txt`
- `chrono_trigger_labels_pass29.txt`
- `chrono_trigger_labels_pass3.txt`
- `chrono_trigger_labels_pass30.txt`
- `chrono_trigger_labels_pass31.txt`
- `chrono_trigger_labels_pass4.txt`
- `chrono_trigger_labels_pass5.txt`
- `chrono_trigger_labels_pass6.txt`
- `chrono_trigger_labels_pass7.txt`
- `chrono_trigger_labels_pass8.txt`
- `chrono_trigger_labels_pass9.txt`
- `chrono_trigger_research_and_disasm_start.md`

---

## Best single-file summary of current position

If another session needs the shortest honest state description, it is this:

- the ROM is identified and boot/init are meaningfully mapped
- the main decompressor is identified
- `7F:2000` is a slot/object script VM with a scheduler
- palette/effect logic is directly embedded in that VM
- movement, spatial rebucketing, and render traversal are linked
- metasprite class sizes and cache/materializer flows are substantially understood
- class 3 has its own full-build/render path
- bank `C1` contains a relation-query subsystem and a multi-table command interpreter
- the project is **well past “blind poking”**
- but still **well short of a complete rebuildable disassembly**

---

## Final no-BS status

This session produced **real reverse-engineering progress** and a usable architectural map.

It did **not** finish the disassembly.

The next session should treat this handoff as the canonical summary, then use the existing per-pass reports and labels as the detailed trail behind it.
