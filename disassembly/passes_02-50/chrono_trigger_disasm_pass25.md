# Chrono Trigger Disassembly — Pass 25

This pass targeted the open question from pass 24:

- pass 24 proved that `C0:E12A` is the real **class-3 full-build route**
- but it did **not** prove who populates the per-slot source pointers:
  - `1200/1280`
  - `1300/1380`

## Goal

Trace the code that actually seeds the class-3 source pointers and determine whether they come from:

- fixed preset tables
- dynamic script state
- decompressed stream data
- or some mix of the above

## High-confidence findings

## The long-pointer helper tables are boot-seeded from `E4:FFE0`

The boot/init path at `C0:0BBA..0C0E` does the following:

- `LDA #$E4`
- `STA $B1`
- `STA $B4`
- `STA $B7`
- `STA $BA`

Then, in 16-bit A mode, it loads:

- `E4:FFE0 -> $AF`
- `E4:FFE2 -> $B2`
- `E4:FFE4 -> $B5`
- `E4:FFE6 -> $B8`

And the table at `E4:FFE0` contains:

- `2000`
- `2300`
- `2600`
- `2800`

So the four direct-page long pointers used by the later class-3 setup code are:

- `$AF/$B0/$B1 -> E4:2000`
- `$B2/$B3/$B4 -> E4:2300`
- `$B5/$B6/$B7 -> E4:2600`
- `$B8/$B9/$BA -> E4:2800`

That resolves the source base for the `[$AF]`, `[$B2]`, `[$B5]`, and `[$B8]` reads seen in the class-3 setup logic.

## `C0:4476` is a real class-3 preset loader from `E4:F000`

The routine at `C0:4476` is not random setup code. It is a compact **preset-record loader**.

It does:

1. set:
   - `1100 = 3`
   - `1B01 = 1`
2. read a script byte from `7F:2001`
3. multiply that byte by `5`
4. use the result as an index into `E4:F000`

Then it consumes the resulting 5-byte record like this:

- `F001` -> index into `[$B2]` -> writes:
  - `1380`
  - `1300`
- `F002` -> multiply by `0x18` -> writes:
  - `1400`
- `F003` -> index into `[$B5]` / `[$B8]` -> writes:
  - `1480`
  - `1500`
  - `1580`
- `F004` -> writes:
  - `1201`
- `F000` -> index into `[$AF]` -> writes:
  - `1280`
  - `1200`

So `E4:F000` is a genuine **5-byte class-3 preset table** that seeds both:

- the chunk-source long pointer (`1200/1280`)
- and the descriptor/tail-side pointer and offsets (`1300/1380`, `1400`, `1480/1500/1580`, `1201`)

The first several records in `E4:F000` are exactly 5 bytes wide and read cleanly as repeated identity presets:

- `00 00 00 00 00`
- `01 01 01 01 00`
- `02 02 02 02 00`
- `03 03 03 03 00`
- ...

That is strong confirmation that the record size here is really **5 bytes**.

## `C0:4557` is the common stream-driven class-3 setup prefix

The helper at `C0:4557` is reused by the later class-3 setup routines.

What it does:

- writes the caller-supplied mode byte into `1100`
- reads the next script byte into `1101`
- stores that script byte into the hardware multiplier source (`4202`)
- seeds the chunk-source pointer from:
  - `1280 = $71`
  - `1200 = #$7F`
- sets:
  - `0C00 = #$2020`
  - `1600 = 1`
  - `1680 = 0`
  - `1681 = 0`

So `4557` is not building the final record by itself.
It is a real **common prefix** for class-3 source setup that starts from the current `7F:$71` stream buffer.

## `C0:4590` is a second 5-byte preset loader from `E4:F024`

The routine at `C0:4590` does:

1. `LDA #4`
2. `JSR 4557`
3. set `4203 = 5`
4. read the hardware multiply result into `$BF`

So this is another **5-byte record loader**, but built on top of the `4557` prefix.

It then consumes `E4:F024 + record*5` in the same field pattern seen at `4476`:

- `F024+1` -> `1300/1380`
- `F024+2` -> `1400` via `*0x18`
- `F024+3` -> `1480/1500/1580`
- `F024+4` -> `1201`
- `F024+0` -> stored in `$E3`, then passed into chunk-source resolution logic

The important difference is that this path does **not** blindly seed `1200/1280` from a fixed preset record.
Instead, it resolves the chunk source through:

- `$E3`
- `JSR 5C90`
- and then either:
  - copy a chunk-source pointer from another slot's `1280`
  - or decompress / install a new chunk-source pointer through the `47FE/4845` paths

So `C0:4590` is best understood as a **class-3 preset loader with dynamic chunk-source resolution**.

## `C0:46DF` is the extended class-3 preset loader from `E4:F600`

The routine at `C0:46DF` is a third source-setup family.

It does:

1. `LDA #5`
2. `JSR 4557`
3. set `4203 = #$0A`
4. use the multiply result as an index into `E4:F600`

That means the record size here is **10 bytes**.

This handler directly consumes only the **first 5 bytes** of each 10-byte record in the same general field layout:

- `F601` -> `1300/1380`
- `F602` -> `1400` via `*0x18`
- `F603` -> `1480/1500/1580`
- `F604` -> `1201`
- `F600` -> `$E3`, used to resolve the chunk source

So `E4:F600` is a real **10-byte extended class-3 preset table**.

## The second half of the `E4:F600` records is used elsewhere

The reason `E4:F600` is clearly 10 bytes wide is that other code in bank `CC` reads the later bytes directly:

- `CC:EAE0` reads `E4:F603`
- `CC:EB75` reads `E4:F604`
- `CC:EBB0..EBD5` read:
  - `E4:F605`
  - `E4:F606`
  - `E4:F607`
  - `E4:F608`
  - `E4:F609`

So the `F600` records are definitely not “5-byte records with padding.”
They are true **10-byte shared records**, and the class-3 setup path uses the first half.

That is a useful architectural result even though the exact meaning of bytes `5..9` is still unresolved in this pass.

## `C0:47FE` is the dynamic “decompress chunk source and point at it” path

When the `4590/46DF` family does not reuse an existing source pointer, it can fall into `C0:47FE`.

That path does:

- use `$E3` to select a 3-byte entry from `[$AF]`
- build a source pointer in scratch at `$0300/$0302/$0303/$0305`
- call:
  - `JSL C3:0002`
- add the returned size (`0306`) to `$71`

This is the same decompression core that was identified in pass 4.

So `47FE` is a real **dynamic class-3 chunk-source decompression path**.
It expands a source selected by the `$E3` field and advances the live stream pointer at `$71`.

## `C0:4845` is the dynamic “install chunk-source pointer directly from table” path

The fallback path at `C0:4845` uses the same `$E3` selector, but instead of decompressing:

- it indexes `[$AF]`
- writes the resulting long pointer directly into:
  - `1280`
  - `1200`

Then it branches back into the common class-3 continuation at `4799`.

So `4845` is the direct-pointer sibling of `47FE`.

## What this resolves

The question from pass 24 was: where do `1200/1280` and `1300/1380` actually come from?

The answer is now:

### `1300/1380`
These come from **preset-record fields** that index the `[$B2] -> E4:2300` long-pointer table.

Observed source families:

- `E4:F000 + n*5`
- `E4:F024 + n*5`
- `E4:F600 + n*10`

### `1200/1280`
These can come from multiple sources:

1. **direct preset pointer install** via `E4:F000`
2. **dynamic direct-pointer install** via `4845` and `$E3`
3. **dynamic decompressed stream install** via `47FE` and `$71/$7F`
4. **slot-to-slot reuse** via the `5C90`-success path

That is much better than the earlier vague guess that the class-3 pointers were “probably animation/frame tables.”

They are being seeded by a real mix of:

- fixed preset tables
- dynamic table-selected pointers
- decompressed stream data
- and source-pointer reuse

## Strongest current labels

- `C0:0BBA  Seed_E4_LongPointerBanks_For_AF_B2_B5_B8`
- `E4:FFE0  Boot_LongPointerLowWords_For_E4_2000_2300_2600_2800`
- `C0:4476  SetupClass3_FromE4F000_Record5`
- `E4:F000  Class3PresetTable_Record5`
- `C0:4557  Init_Class3_StreamDrivenSourcePrefix`
- `C0:4590  SetupClass3_FromE4F024_Record5_WithDynamicChunkSource`
- `E4:F024  Class3PresetTable_Record5_B`
- `C0:46DF  SetupClass3_FromE4F600_Record10_WithDynamicChunkSource`
- `E4:F600  Class3PresetTable_Record10_Extended`
- `C0:47FE  Decompress_AndInstall_Class3ChunkSource_FromE3Selector`
- `C0:4845  Install_Class3ChunkSourcePointer_FromE3Selector`

## Honest limit

I have **not** yet pinned the exact semantic meaning of:

- `1400`
- `1480`
- `1500`
- `1580`

beyond the fact that they are seeded from the preset records and are consumed downstream by the class-3 build/render system.

I also have **not** yet decoded the exact meaning of bytes `5..9` in the `E4:F600` extended records.

## Bottom line

This pass resolves the upstream class-3 pointer story.

The slot fields used by the class-3 full-build route are not magical internal state.
They are populated by a real family of preset loaders that pull from fixed `E4` tables and, when needed, switch over to dynamic direct-pointer or decompression-backed chunk-source installation.
