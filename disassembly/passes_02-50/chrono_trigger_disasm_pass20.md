# Chrono Trigger Disassembly — Pass 20

This round cracked the two header-dispatch helpers at `C0:E534` and `C0:E687`.

## Goal

The previous pass established that the class-sized `7F:4800` builders walk a header/descriptor region and dispatch through:

- `C0:E534`
- `C0:E687`

The open question was what those helpers actually do, and what the 16-bit header words mean.

## High-confidence findings

## The header region is a sequence of 16-bit block descriptors

At the builder call sites (`CC5A`, `CF7A`, `D2EA`, `D356`, `D5A6`, `D5E5`, `D668`, `D6D6`, `D715`, `D783`, `D7C2`, `D82E`, `DAB2`, `DAED`, `E17C`) the code does:

- load a 16-bit word via `B7 D3`
- test it with `BIT #$4000`
- call `E687` when bit `0x4000` is set
- call `E534` when bit `0x4000` is clear

Both callees mask with `AND #$07FF` and then shift left 5 times, so both interpret:

- **low 11 bits** = block index
- **bit 14 (`0x4000`)** = source mode selector
- **bits 11-13 and bit 15** = still unresolved here

Because of the `<< 5`, each indexed block is **32 bytes** wide.

That fits perfectly with the pass-19 result that the builder is generating one **4-sprite / 0x20-byte template chunk** at a time.

## `C0:E534` = expand a 32-byte template block through the `FD:0000` byte-translation table

`E534` does this shape:

1. mask header word to 11-bit block index
2. multiply by `0x20`
3. use the result as `Y`
4. in 8-bit A mode, repeat 32 times:
   - `LDA [$CD],Y`
   - `TAX`
   - `LDA $FD00,X`
   - `STA $2180`
   - `INY`
5. restore 16-bit A and return

So `E534` is not a direct copier. It is a **32-byte indexed expansion/remap path**:

- source: long indirect pointer at `$CD/$CF`
- lookup table: `FD:0000`
- destination: WRAM via `$2180`

The important honest limit:

I have **not** fully decoded the semantic meaning of the `FD:0000` translation table yet.  
But the execution model is clear: this is a **1-byte in -> table lookup -> 1-byte out** remap for 32 consecutive bytes.

## `C0:E687` = copy a 32-byte template block directly into `7F` staging

`E687` does the same initial `((header & 0x07FF) << 5)` block-index math, but then:

- adds the builder base offset in `$CD`
- uses `$CF` as the **source bank selector**
- loads `Y` from `$D0` as the **destination offset**
- copies **16 words / 32 bytes** directly into bank `7F`
- then updates `$2181` to `Y + 0x20` so the WRAM-port destination stays synchronized with the direct-copy path

The source-bank dispatch is real and explicit:

- `$CF == 0x7F` -> direct indexed copy from current bank-local source
- `$CF == 0xD2` -> copy from `D2:0000,X`
- `$CF == 0xD3` -> copy from `D3:0000,X`
- `$CF == 0xD4` -> copy from `D4:0000,X`
- otherwise -> copy from `D5:0000,X`

So `E687` is the **direct 32-byte template-block copy path**.

## `E534` and `E687` are interchangeable chunk writers for the same builder pipeline

This is the architectural payoff:

- `E534` writes its 32-byte result through the WRAM data port at `$2180`
- `E687` writes its 32-byte result directly into bank `7F`, then advances `$2181` by `0x20`

That means both helpers are designed to feed the **same `7F:4800`-family staging stream**.
They differ only in how the chunk is sourced:

- **bit `0x4000` clear** -> remap/expand source bytes through `FD:0000`
- **bit `0x4000` set** -> direct-copy a 32-byte template block from source bank `7F/D2/D3/D4/D5`

## The builder-side source pointer state is now clearer

In the class-3 builder region (`D4F8+`) the code explicitly seeds:

- `$CF` from `1200,X`
- `$CD` from `1280,X`

So the helper pair is not freelancing. They are consuming a real per-slot / per-frame source pointer pair.

This lines up with the pass-19 conclusion that the source-side frame blocks have a real class-local format.

## What this means now

The metasprite-template frame format is cleaner than before:

- frame blocks are broken into 32-byte chunks
- each chunk is selected by a 16-bit header word
- the chunk can be:
  - **direct-copied** from banks `7F/D2/D3/D4/D5`
  - or **expanded/remapped** through the `FD:0000` table
- those chunks feed the `7F:4800` template staging family
- the XY tails are still copied separately by the class-sized tail builders (`CCC0 / CFE0 / D890`)

So the header words are not just “template metadata.”
They are real **template-chunk source descriptors**.

## Best current labels

- `C0:E534  ExpandTemplateChunk32_FromIndirectSource_ThroughFDTable_ToWramPort`
- `C0:E687  CopyTemplateChunk32_FromBankedSource_To7FStaging`
- `FD:0000  TemplateByteTranslateTable`

## Open questions

Still unresolved, and worth a dedicated next pass:

1. what `FD:0000` semantically represents
   - tile remap table?
   - attribute expansion table?
   - packed-template decode table?
2. whether bits `0x0800/0x1000/0x2000/0x8000` in the 16-bit header words are used by other code
3. exact handoff from `7F:4800` template chunks into the later `7F:4BC0` prepared render cache

## Bottom line

This pass turns `E534 / E687` from “mystery helper pair” into a real source-mode system for metasprite template chunks.

That is enough to say the class builders are assembling frame data from a **mixed template vocabulary**:
some chunks are copied directly from prebuilt banks, and some chunks are expanded through a translation table.
