# Chrono Trigger Disassembly — Session 13 Continuation Notes (Third Continuation)

## Starting point
- Prior live seam: `C3:3D00..`
- Prior latest completed pass: **211**
- Prior estimate: **~81.2%**

## Work completed now
This continuation closed **passes 212 through 221**.

### Pass 212 — `C3:3D00..3DFF`
Mixed branch-heavy control/blob page.
- cleanest external-looking hit: `C3:3E54 -> 3DE5` via cross-page `BRA`
- dirtier external pressure also into `3DF0`, `3DD2`, `3DC9`, `3DB9`
- best local splinters: `3D23..3D2C (RTS)`, `3DE2..3DEA (RTS)`
- result: no caller-backed true start

### Pass 213 — `C3:3E00..3EFF`
Mixed init/control page.
- `3ED3` got two external `JSR` hits (`C3:1C1E`, `C3:597A`), but both callers were dirty
- cleaner single-hit branch bait existed into `3EE5`, `3ECE`, `3ECD`, `3E2F`
- strongest local pocket: `3E5E..3E69 (RTS)`
- result: no stable owner lane

### Pass 214 — `C3:3F00..3FFF`
Most executable-looking early page of the run.
- `3F90` got one comparatively cleaner external `JSR` from `C3:62A5`
- strongest local islands: `3F24..3F43 (RTI)`, `3F57..3F6D (RTI)`, `3F0E..3F20 (RTS)`
- `3F90` still lands mid-blob, not at a defendable owner boundary

### Pass 215 — `C3:4000..40FF`
Xref-saturated dispatch/table-like material.
- heaviest external target field of the continuation: `4000`, `4018`, `4019`, `4008`, `405F`, `40F0`, `40A0`, `4025`
- none had caller support clean enough to justify ownership
- best local island: `4028..4035 (RTS)`
- result: mixed dispatch/data, not a defendable owner routine

### Pass 216 — `C3:4100..41FF`
Mixed control/data page.
- cleanest external hit: `C3:51DF -> 4109`
- noisier external pressure into `4159`, `41B5`, `41A5`, `4181`, `4160`
- strongest local splinter: `41C0..41DF (RTS)`
- result: visible late hits still behave like interior/tail bait

### Pass 217 — `C3:4200..42FF`
Mixed script/command-control page.
- cleanest external hit: `C3:68EF -> 4274`
- `424F` drew two dirty external `JSR` hits from `C3:0E4F` and `C3:0E69`
- best local island: `42C2..42D0 (RTL)`
- result: no owner survives

### Pass 218 — `C3:4300..43FF`
Strongest caller-side false dawn of this continuation.
- `4309` received **two** comparatively clean direct external hits: `C3:2193 JSR $4309` and `C3:24A1 JMP $4309`
- `4300` also received one cleaner external `JSR` from `C3:65B7`
- local byte review still killed the page: `4309` lands inside mixed material, not at a defendable owner start
- later `43B0` zone degrades into obvious name/text-style content

### Pass 219 — `C3:4400..44FF`
Credits/text-heavy material.
- visible external hits included `44A5`, `44C2`, `44B0`, `44AA`, `4441`, `4435`
- `44A5` got two external `JSR` hits, but target-side bytes are obviously text-heavy
- result: no callable owner candidate survived anywhere in the page

### Pass 220 — `C3:4500..45FF`
Mixed command/control page.
- `4544` received three external `JSR` hits from `C3:0EEE`, `C3:442F`, and `C3:72B5`, but caller quality remained too poor
- late `45DE..4607` area looked more executable than the top half of the page
- visible hits into `45DE`, `45E0`, `45EB`, and `45EF` still behaved like branch/tail bait
- strongest local island by shape: `45A2..45C1 (RTS)`

### Pass 221 — `C3:4600..46FF`
Mixed control/script tail page.
- `4631` was the strongest external target on paper because it received two external `JSR` hits from `C3:D828` and `C3:DC30`
- those callers were still dirty enough that the target never earned ownership
- cleaner single-hit branch pressure existed into `461E` and `46E3`, but both remained interior/tail bait
- local return pockets: `46BF..46C6 (RTS)`, `46E3..46F0 (RTI)`

## Current state now
- Latest completed pass: **221**
- Current live seam: **`C3:4700..`**
- Current completion estimate: **~82.0%**

## Biggest takeaways
1. **`3F90`** is the cleanest lone external `JSR` landing of this continuation, but it still lands mid-blob.
2. **`4309`** is the strongest false dawn of the run because it has two clean direct callers and still fails ownership.
3. **`4400`** is overwhelmingly text/credits content and should not be mistaken for recoverable code.
4. **`4544` / `45DE` / `4631`** are the main late-page temptations, but none survive caller-quality plus local-structure review together.

## Real next target
- **`C3:4700..`**
