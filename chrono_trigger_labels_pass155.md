# Chrono Trigger Labels — Pass 155

## Purpose

Pass 155 closes the former exact `C2:F75C` live seam and splits it into one exact local row materializer helper, one exact direct-page-derived descriptor builder, and one exact alias/shared packet-submit pair.

## Strong labels

### C2:F75C..C2:F870  ct_c2_9890_word_driven_32byte_row_materializer_with_optional_c0_fd00_translation_then_9a88_submit_tail   [strong structural]
- Real exact caller is exact `C2:F74D` from the downstream exact `F6E0` submit tail.
- Begins `PHP ; SEP #$30`, mirrors exact byte `06 -> 9692`, then widens through exact `REP #$31`.
- Derives exact word `9A8A = 8000 + ((0D72 << 1) & FF00)` and uses that exact word as the running exact destination in `Y`.
- Derives exact loop bound word `0002 = ((01 & 0F00) >> 3)`.
- Walks exact words `9890,X` in exact two-byte steps.
- On exact zero exact selector word, clears one exact `0x20`-byte row at exact `Y` across offsets `0000..001E`.
- On exact nonzero exact selector word, derives exact source index `04 + 0x20*(9890[X] & 07FF)`, runs exact `JSL 7E:9690` with exact `A = 001F`, and when the original exact selector word has its exact `V` bit set remaps the produced exact `0x20` bytes through exact long table `C0:FD00`.
- After the row loop seeds exact submit-state bytes/words `9A88/9A8C/9A8D/9A8E`, advances exact global byte `0D73 += 02`, and chooses between one exact `JSR 838E` or two exact `JSR 838E` submits depending on the exact parity of byte `02`.
- Strongest safe reading: exact `9890`-driven row materializer/helper that clears or materializes exact `0x20`-byte rows, optionally remaps those bytes through exact `C0:FD00`, then seeds exact `9A88`-family submit state and runs exact `838E`.

### C2:F871..C2:F904  ct_c2_direct_page_row_descriptor_builder_writing_0800_quads_and_0910_bits_from_dp_base_02_0e_0f_19_22_23_0d2e_0d30   [strong structural]
- Real exact caller is exact `C2:F687` from the exact persistent eight-row direct-page service loop.
- Begins `PHP ; REP #$20 ; TDC`, so it derives part of its exact output base directly from the caller’s current exact direct-page base.
- From that exact direct-page base derives one exact descriptor/output offset in `Y` and one exact group byte in exact `0002`.
- In exact widened mode derives exact loop bound word `0004 = 8 * (02 & 000F)`, clears exact word `0008`, and seeds exact byte/word `0006 = 0F + 0D2E`.
- Rotates exact byte `0007` through exact `LSR` / `ROR` before entering the exact descriptor loop.
- On each exact `X += 2` loop writes one exact four-byte descriptor into exact `0800,Y`: exact byte `0800 = 0006 + 22,X`, exact byte `0801 = 0E + 23,X + 0D30`, and exact word `0802 = 0008 + 19`.
- Uses the exact sign/parity test rooted at exact `ROR A`, exact `EOR 22,X`, and exact `EOR 0007` to decide when to set one exact bit in exact table byte `0910[group]` via exact bitmask byte `0000`.
- Advances exact `Y += 4`, mutates exact byte `0008` through the exact lane `((0008 | 10) + 2) & EF`, shifts exact bitmask byte `0000` left twice, and repeats while exact `X < 0004`.
- Strongest safe reading: exact direct-page-row-derived descriptor builder that writes exact four-byte records into exact `0800` and accumulates exact group bits into exact `0910`.

### C2:F90C..C2:F942  ct_c2_shared_dual_packet_submitter_seeding_0210_0212_0213_0214_then_running_c2_0003_c2_0009_and_looping_on_0215_eq_05   [strong structural]
- Has real outside callers at exact `C2:D2BF`, `C2:D2F0`, `C2:D3DF`, `C2:E4E6`, and exact `C2:E85F`.
- Shared body begins `PHP ; SEP #$20 ; LDA #$80`.
- Seeds exact packet workspace `0214 = 80` for the shared entry or exact `0214 = 81` when entered through exact alias `F905`.
- Mirrors exact word `0DC5 -> 0210` and exact literal byte `7E -> 0212`.
- Runs exact `JSL C2:0003`.
- Seeds exact byte `0213 = 20` and runs exact `JSL C2:0009`.
- Checks exact result/status byte `0215`; when exact `0215 == 05`, advances exact byte/word `0211 += 4` and repeats the exact `0213 / C2:0009 / 0215` lane.
- Exits through exact `PLP ; RTS` when exact `0215 != 05`.
- Strongest safe reading: exact shared packet submitter that seeds exact `0210..0214`, runs exact `C2:0003` then exact `C2:0009`, and on exact result `0215 == 05` repeatedly advances exact `0211` by four before retrying the exact second-call lane.

## Alias / wrapper / caution labels

### C2:F905..C2:F90B  ct_c2_seed_0214_81_alias_entry_into_f90c_shared_dual_packet_submitter   [alias wrapper]
- Exact body: `PHP ; SEP #$20 ; LDA #$81 ; BRA $F911`.
- Real exact caller is exact `C2:CA8F`.
- Strongest safe reading: exact wrapper entry that selects exact packet mode byte `0214 = 81` before joining the downstream exact shared packet submit body at exact `F90C`.

## Honest remaining gap

- exact `C2:F75C..C2:F942` is now honestly split and closed
- the next clearly live callable/helper band begins at exact `C2:F943`
- that next owner family should be taken as the forward seam rather than guessed from the middle
