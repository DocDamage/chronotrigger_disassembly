# Chrono Trigger Disassembly — Pass 21

This round targeted the `FD00` translation table and the remaining meaning of the chunk headers used by `C0:E534 / C0:E687`.

## Goal

The previous pass established that:

- `C0:E534` copies a 32-byte chunk through a byte-translation table
- `C0:E687` copies a 32-byte chunk directly
- the chunk selector comes from 16-bit header words where:
  - low 11 bits = block index
  - bit `0x4000` = source mode selector

The open question was what that byte-translation table actually *is*.

## High-confidence findings

## The table at ROM offset `0x00FD00` is an exact 8-bit bit-reversal table

The bytes at ROM offset `0x00FD00` begin:

```text
00 80 40 C0 20 A0 60 E0 10 90 50 D0 30 B0 70 F0
08 88 48 C8 28 A8 68 E8 18 98 58 D8 38 B8 78 F8
...
```

That is not a vague lookup table. It is the exact mapping:

- `table[x] = bitreverse8(x)`

for all `0x00..0xFF`.

So the old broad label "`TemplateByteTranslateTable`" can now be replaced with the precise meaning:

- **8-bit bit-reverse lookup table**

## `C0:E534` is a horizontally mirrored 32-byte tile-chunk copier

Because `E534` does:

1. read a byte from the source chunk
2. use that byte as an index into the bit-reverse table
3. write the translated byte to the destination stream

and because the chunk size is **exactly 32 bytes**, this is now a much stronger read:

- a 32-byte chunk matches one **SNES 4bpp 8x8 tile**
- reversing the bits in every byte of such a tile produces a **horizontal mirror** of the tile

So `E534` is no longer best understood as a generic “expand/remap” path.

It is much better named as:

- **copy one 32-byte tile chunk while horizontally flipping it**

## `C0:E687` remains the direct tile-chunk copy path

`E687` still reads the same 32-byte chunk size, but copies the bytes straight through from the selected source bank.

So the header bit split is now much more concrete:

- **bit `0x4000` clear** -> copy the tile chunk with bytewise bit reversal (`E534`)
- **bit `0x4000` set** -> copy the tile chunk directly (`E687`)

This is the strongest current interpretation of that mode bit.

## The header descriptors are now better read as tile-chunk descriptors, not generic template metadata

The builder-side chunk math from earlier passes already showed:

- low 11 bits select a chunk index
- chunk width is `0x20` bytes

Now that the translation path is known to be a bit-reversing tile copy, the 16-bit header words are much less mysterious.

They are best read as:

- **tile-chunk descriptors**
- selecting either:
  - a direct tile copy
  - or a horizontally mirrored tile copy

## The class-sized source blocks line up with 4 tile descriptors per emitted sprite record

From the builder loop counts already established:

- class 0 uses `0x10` descriptor words = **16 tile descriptors**
- class 1 uses `0x20` descriptor words = **32 tile descriptors**
- class 2 uses `0x30` descriptor words = **48 tile descriptors**
- class 3 uses `0x60` descriptor words = **96 tile descriptors**

And from the render-side passes:

- class 0 emits **4** sprite records
- class 1 emits **8**
- class 2 emits **12**
- class 3 emits **24**

That is an exact **4:1 ratio**:

- 16 / 4 = 4
- 32 / 8 = 4
- 48 / 12 = 4
- 96 / 24 = 4

Best current reading:

- each emitted sprite record is backed by **4 tile-chunk descriptors**

That strongly suggests the chunk-descriptor region is selecting per-record tile graphics in a structured 4-chunk layout, rather than carrying arbitrary metadata.

I am keeping that as a strong inference rather than a fully locked fact, but the ratio is too clean to ignore.

## What this changes architecturally

This is the real payoff of the pass:

the builder pipeline is no longer “assembling generic template chunks from a mixed vocabulary.”

It is more concrete than that:

- it is selecting **32-byte tile chunks**
- some are copied directly
- some are copied as **horizontally flipped tile graphics**
- those chunks are being staged in a class-sized graphics/template stream before the later render-cache / OAM-side work

So the old vague wording can now be tightened.

## Best current labels

- `ROM:00FD00 (mirrored in ROM image)  BitReverse8Table`
- `C0:E534  CopyTileChunk32_HFlip_UsingBitReverseTable_ToWramPort`
- `C0:E687  CopyTileChunk32_Direct_FromBankedSource_To7FStaging`

## Open questions

Still worth a later dedicated pass:

1. whether bits `0x0800 / 0x1000 / 0x2000 / 0x8000` in the 16-bit chunk descriptors are consumed anywhere else
2. exact handoff from the `7F:4800`-family tile/template staging into the later prepared render cache
3. whether the 4-chunk-per-record grouping corresponds to:
   - one 16x16 sprite
   - or another fixed metasprite tile arrangement

## Bottom line

This pass converts the `FD00` table from a mystery into a precise technical fact:

- it is a **bit-reverse table**
- `E534` uses it to generate **horizontally mirrored 32-byte tile chunks**
- the header words are therefore best understood as **tile-chunk source descriptors**, not generic metadata
