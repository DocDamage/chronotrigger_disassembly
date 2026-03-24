# Chrono Trigger Disassembly — Pass 77

## Scope of this pass
This pass continues directly from the pass-76 seam.

Pass 76 proved the big architectural point:

- service `04` is a real local mode dispatcher keyed by `AE92`
- mode `1` is the current-context/current-tail profile-loader front end
- mode `2` is the fixed-follow-up profile-loader front end
- both active modes converge into the same shared runner at `4833`

But four useful gaps were still open:

1. mode `0` and mode `3` were still unresolved
2. `48EC` was only labeled as a vague parser helper
3. `4943` was only labeled as a vague batch builder
4. pass 76 overstated the final `5D00..` record shape as “six-byte” records when the index math really says otherwise

This pass closes those specific gaps.

The biggest honest upgrade is:

> service-04 mode `0` is just a no-op,
> mode `3` is a third fixed-profile front end,
> `48EC` is a segmented CE-stream parser,
> and `4943` is a packed fragment/quad batch decoder.

That does **not** fully freeze the final gameplay-facing noun of the emitted thing, but it makes the output side much less fuzzy.

---

## 1. Service-04 mode `0` is exact no-op, and mode `3` is a third fixed-profile family
Pass 76 already proved that the service-04 mode jump table is:

- mode `0` -> `475A`
- mode `1` -> `432C`
- mode `2` -> `45A0`
- mode `3` -> `475B`

### 1a. `C1:475A` is just `RTS`
Direct bytes:

```text
C1:475A  60
```

So mode `0` is not “light setup” or “default output.”
It is exact **no-op / do nothing** service-04 behavior.

That matters because it means `AE92 >= 4` truly falls back to “nothing happens” rather than some hidden minimal emitter path.

### 1b. `C1:475B..4832` is the missing mode-3 front end
Direct front-half bytes:

```text
C1:475B  38
C1:475C  AD 93 AE
C1:475F  E9 BC
C1:4761  C2 20
C1:4763  85 80
C1:4765  0A 0A 0A
C1:4768  38
C1:4769  E5 80
C1:476B  AA
```

This is exact arithmetic for:

```text
X = 7 * (AE93 - 0xBC)
```

Then mode `3` loads a 7-byte profile record from:

- `CD:5C26 + 7*(AE93 - 0xBC)`

into the same working-byte neighborhood used by mode `2`:

- `9877`
- `987A`
- `987B`
- `987E`
- `9881`
- `9884`
- `987C`

After that it runs the same shared derivation chain as mode `2`:

- `D1:0060` through `987E -> 987F`
- `CD:6C2C` through `9881 -> 9882`
- `CD:656E` through `9884 -> 9885`
- `CD:63F0` through `9877 -> 9878`
- then `22 15 00 CD`
- then `22 2A 00 CD`
- then the same `4833` common output runner

So mode `3` is **not** a new output subsystem.
It is the missing sibling of mode `2`: another fixed-profile front end, but using the high-range profile family rooted at `CD:5C26` and indexing it by `AE93 - 0xBC`.

Safest upgraded reading:

> `C1:475B..4832` = **service-04 mode-3 high-range fixed-follow-up profile loader and common emit-tail runner**

This also explains why the two visible mode-3 seed sites at `BADA` and `BB15` both force:

- `AE92 = 3`
- `AE93` into the `0xBC+` neighborhood

Those callers are selecting the mode-3 high-range profile set on purpose, not accidentally falling into some weird leftover branch.

---

## 2. `C1:48EC` is not a vague parser — it parses a segmented CE stream into per-group start pointers and per-group counts
Direct bytes:

```text
C1:48EC  AE 85 98      LDX $9885
C1:48EF  8E 80 A2      STX $A280
C1:48F2  7B            TDC
C1:48F3  A8            TAY
C1:48F4  84 80         STY $80
C1:48F6  84 82         STY $82
C1:48F8  BF 00 00 CE   LDA CE:0000,X
C1:48FC  29 E0         AND #$E0
C1:48FE  F0 3A         BEQ $493A
C1:4900  30 1F         BMI $4921
C1:4902  29 40         AND #$40
C1:4904  D0 09         BNE $490F
```

The top bits of the CE stream byte are the control class.
The code behavior breaks cleanly like this:

### class A: `00` high bits -> end of stream
If `(byte & 0xE0) == 0`, the routine returns immediately.

So `0x00..0x1F` here are not normal entries.
At this layer they mean **stream end / no more groups**.

### class B: `80..FF` -> start a new group and seed its first counted 4-byte unit
When bit `7` is set, control goes to `4921`.
That path:

- advances `X` by 4
- increments the group index at `$82`
- stores the new stream start pointer into `A280[group]`
- clears the per-group count scratch `$80`
- advances `X` by another 4
- increments `$80`
- loops

That is a real structure.
It means the negative/high-bit CE tokens are **group-start markers**.
They open a new group and immediately count the first following 4-byte unit.

### class C: `0x20` -> group boundary with zero count
If the byte is nonzero in the top bits but does **not** have bit `6` set, the routine stores zero into:

- `A2A0[current_group]`

and then takes the same group-advance path.

So this is a **group delimiter whose accumulated unit count is zero**.

### class D: `0x40` or `0x60` -> group boundary with the accumulated count
If bit `6` is set, control goes through `490F`.
That path:

- advances `X` by 4
- increments the running unit count `$80`
- writes `$80` into `A2A0[current_group]`
- clears `$80`
- loops

So these tokens terminate the current group **and commit its accumulated 4-byte-unit count**.

### structural result
At routine entry:

- `A280[0] = 9885`
- `$82 = 0`
- `$80 = 0`

As parsing proceeds, the routine builds:

- `A280[group]` = start pointer for that CE group
- `A2A0[group]` = counted 4-byte-unit size for that group

up to `0x10` groups.

That is much stronger than the pass-76 wording.

Safest upgraded reading:

> `C1:48EC` = **parse segmented CE fragment-group stream into `A280` start pointers and `A2A0` per-group 4-byte-unit counts**

This also makes the data at `CE:0000..` look much less like a raw “profile blob” and much more like a **grouped frame/fragment stream language**.

---

## 3. `C1:4943` is a packed fragment/quad batch decoder, not just a generic batch builder
Pass 76 already proved that `4943` is called exactly eight times from the `4833` shared runner.

What this pass tightens is **what it is decoding**.

Direct front-half bytes:

```text
C1:4943  60 20 7E 00   JSR $007E
C1:4947  20 FA 10      JSR $10FA
C1:494A  64 8C         STZ $8C
C1:494C  C2 20         REP #$20
C1:494E  AD 50 A6      LDA $A650
C1:4951  0A            ASL A
C1:4952  AA            TAX
C1:4953  BF C0 F7 CC   LDA CC:F7C0,X
C1:4957  85 84         STA $84
C1:4959  7B            TDC
C1:495A  E2 20         SEP #$20
C1:495C  AE 50 A6      LDX $A650
C1:495F  9E 5B A0      STZ $A05B,X
C1:4962  AE 52 A6      LDX $A652
C1:4965  BD 00 2D      LDA $2D00,X
C1:4968  D0 03         BNE $496D
C1:496A  4C FE 49      JMP $49FE
```

This proves several exact things.

### 3a. `A650` selects the current output row/base, and `CC:F7C0` gives that row’s destination base
`A650` is doubled and used to pull a 16-bit value from:

- `CC:F7C0`

into `$84`.

That `$84` value is later used as the destination base for the working `4500..` records.

So `A650` is not random scratch.
It is the **current output-row / fragment-row selector**, and `CC:F7C0` is its base-offset table.

### 3b. `A652` is the current cursor into the packed `2D00..` stream
The routine loads `X = A652`, reads `2D00,X`, and later writes the advanced `X` back into `A652` repeatedly.

So `A652` is the real **cursor into the packed fragment script/materialized stream** produced earlier through `C3:0002`.

### 3c. the first control byte is a real packed header
When the control byte is nonzero, the routine splits it into:

- low nibble -> `$81` and `$82`
- high nibble -> `$80`

Then it copies the next low-nibble-count bytes into `A2D3..`.

So the stream format is not “just raw records.”
It begins with a real packed header that controls how many compact fragment bytes are pulled into the local decode buffer.

### 3d. shifted `A2D3` bytes drive conditional 4-byte record emission into the `4500..` workspace
The decode loop does this for each copied byte:

1. load `A2D3[index]`
2. `ASL` it and write it back
3. if carry is clear, skip direct record emission
4. if carry is set, emit one 4-byte record into `4500 + base`

The emitted 4-byte record is assembled from:

- two bytes read directly from the `2D00..` cursor stream
- one lookup byte from `CC:F820[index]`
- one lookup byte from `CC:F820[produced_count]`

and each emitted record increments:

- `A05B[current_row]`

So `A05B[row]` is clearly a **produced-record count** for the current row.

That is not a vague “batch builder.”
It is a real compact-fragment decoder that conditionally emits 4-byte output records.

### 3e. one call to `4943` processes four subpasses
At the tail:

```text
INC $8C
LDA $8C
CMP #$04
F0 03
JMP $494B
RTS
```

So one `4943` call runs this subpass loop exactly **four** times before returning.

Combined with the eight fixed calls from `4833`, that makes `4943` a multi-stage builder, not a single tiny entry writer.

Safest upgraded reading:

> `C1:4943` = **decode one packed fragment batch from `2D00..` into `A2D3` and emit conditional 4-byte quad/fragment records into the `4500..` workspace, tracking per-row output counts in `A05B`**

This is still structural rather than fully player-facing, but it is a much tighter noun than pass 76 had.

---

## 4. Correction: `4833` seeds sixteen **8-byte-stride** output slots, not “six-byte records”
Pass 76 described the final `5D00..` loop as emitting sixteen 6-byte records.
That was wrong.

The exact stride helper is:

```text
C1:0112  0A 0A 0A 60
```

That is three `ASL`s, i.e. multiply by `8`.

So the late loop at `48B7..48E5` is indexing:

- `5D00 + 8*slot`

not `5D00 + 6*slot`.

What the loop provably does is:

- clear the first two bytes of each output slot
- seed bytes `+2` and `+3` from the `D1:50A2 / D1:50A3` table family
- set `A07B[slot] = 1`
- do this for sixteen slots

So the strongest safe correction is:

> `4833` seeds sixteen **8-byte-stride output-slot records** in the `5D00..` family and marks their corresponding `A07B` active flags.

This is a meaningful cleanup because “8-byte slot records” is a much more believable render/output workspace shape than the old mistaken 6-byte description.

---

## 5. Upgraded interpretation after this pass
The service-04 output side is now materially tighter:

- mode `0` = exact no-op
- mode `1` = current-context profile front end
- mode `2` = fixed-follow-up profile front end
- mode `3` = high-range fixed-follow-up profile front end
- `48EC` = segmented CE fragment-group parser
- `4943` = packed fragment/quad batch decoder
- `4833` = shared output runner that seeds sixteen 8-byte-stride output slots

So the output family is no longer best described as “mysterious common tail.”
It now looks like a real **profile-driven fragment/sprite-piece assembly pipeline**:

1. choose a profile family through service-04 mode
2. derive working profile bytes into `9877..9885`
3. parse a segmented CE stream into group starts/counts
4. materialize a packed intermediate stream at `2D00..`
5. decode that stream into 4-byte fragment records in the `4500..` workspace
6. seed sixteen 8-byte output slots in `5D00..` and mark them active

I am still keeping the final user-facing noun one notch below “fully frozen.”
The code is now strongly pointing at a sprite-piece / fragment assembly subsystem, but I have **not** yet proved whether the thing being assembled should be named as:

- sprite pieces
- subsprites
- effect quads
- animation cells
- or some more specific battle/output object noun

So the labels stay structural where they need to.

---

## Honest caution
I am **not** claiming any of these are final when the proof is not there yet:

1. I have **not** fully named the final gameplay-facing object emitted through `4500.. -> 5D00..`.
2. I have **not** decoded `C3:0002`, which still matters because it materializes the packed `2D00..` stream that `4943` consumes.
3. I have **not** decoded the exact meanings of the individual 7-byte mode-2/mode-3 profile fields.
4. I have **not** frozen whether `A05B` is strictly “quad count,” “fragment count,” or a slightly more specific row-local render count.

But this pass absolutely does close the mode map and substantially tightens the output builder seam.

---

## Best next seam after pass 77
The next best move is now much cleaner than before:

1. decode `C3:0002` so the packed `2D00..` stream gets a real noun
2. crack `CD:0015 / CD:0018 / CD:002A` so the optional pre-parse stages stop being black boxes
3. tighten the final noun of the `4500.. / 5D00.. / A07B` output-slot family
4. re-open the mode-3 callers at `BADA` / `BB15` now that mode `3` is grounded
