# Chrono Trigger Labels — Pass 131

## Purpose

Pass 131 closes the downstream callback / dispatch seam at `C2:CED2..C2:CF92` and tightens the immediately-following callable initializer at `C2:CFFB..C2:D048`.

## Strong labels

### C2:CED2..C2:CED3  ct_c2_callback_entry_stub_branching_back_to_cec2   [strong structural]
- Exact bytes decode to `BRA CEC2`.
- This is a real local entry stub immediately after the already-frozen `CEC2` wrapper.
- Strongest safe reading: exact callback entry stub that branches back into the previously-frozen `CEC2` service wrapper.

### C2:CED4..C2:CEDB  ct_c2_local_four_word_dispatch_table_for_ced2_callback_family   [strong]
- Exact little-endian word table following the `CED2` entry stub.
- Exact entries:
  - `CEDC`
  - `CEFD`
  - `CF61`
  - `CF92`
- Strongest safe reading: exact local 4-word dispatch table for the `CED2` callback family.

### C2:CEDC..C2:CEFC  ct_c2_bit6_or_gate_owner_choosing_eacc_or_eac2_then_d0e5   [strong structural]
- ORs exact bytes/words `0D34`, `0294`, `0299`, and `029E`.
- Keeps only exact bit `0x40`.
- Set path clears exact byte `67`, seeds exact byte `68 = 01`, and exits through exact jump `EACC`.
- Clear path runs exact helper `EAC2`, increments exact byte `68`, and exits through exact jump `D0E5`.
- Strongest safe reading: exact bit-6 gate owner that either arms the `67/68` immediate lane into `EACC` or falls through the `EAC2 -> D0E5` counted path.

### C2:CEFD..C2:CF2F  ct_c2_0d1d_gated_dispatcher_with_0d49_slot_test_clear_path_to_cfa2_and_overflow_9a98   [strong structural]
- Begins `JSR E984 ; BIT 0D1D`.
- Negative path indexes exact byte `0D49,X` using exact index `79`.
- When exact byte `0D49[79] != 0`, runs exact helper `EAC2`, mirrors exact byte `54 -> 0F00`, increments exact byte `68`, and exits through exact jump `D4BB`.
- When exact byte `0D49[79] == 0`, runs exact helpers `CF37` and `D32C`, emits exact selector `FC0D` through exact helper `8385`, and tail-emits local selector `CF30` through exact jump `8385`.
- Clear path exits through exact jump `CFA2`.
- Overflow path exits through the exact local jump tail at `CF5E`.
- Strongest safe reading: exact `0D1D`-gated dispatcher with a negative-path slot test on `0D49[79]`, a clear-path handoff into `CFA2`, and an overflow jump to `9A98`.

### C2:CF30..C2:CF36  ct_c2_local_selector_descriptor_packet_for_cefd_zero_slot_path   [strong]
- Exact 7-byte local descriptor packet consumed by the zero-slot negative path in `CEFD`.
- Exact bytes: `00 79 00 70 7E 00 06`.
- Strongest safe reading: exact local selector descriptor packet for the `CEFD` zero-slot negative path.

### C2:CF37..C2:CF5D  ct_c2_immediate_1e00_198a80_packet_emitter_marking_0d49_79_ff_and_running_fff9fb_821e_d19f_821e   [strong structural]
- Seeds exact packet bytes:
  - `1E00 = 19`
  - `1E01 = 8A`
  - `1E02 = 80`
- Runs exact long helper `C7:0004`.
- Uses exact index `79` to set exact byte `0D49[79] = FF`.
- Runs exact long helper `FFF9FB`.
- Runs exact helper chain `821E -> D19F -> 821E`.
- Strongest safe reading: exact immediate `1E00/1E01/1E02` packet emitter plus service tail that marks exact slot `0D49[79] = FF` and then runs the fixed `FFF9FB / 821E / D19F / 821E` chain.

### C2:CF5E..C2:CF60  ct_c2_local_overflow_jump_tail_to_9a98   [strong structural]
- Exact bytes decode to `JMP 9A98`.
- This is the overflow landing pad used by the `CEFD` dispatcher.
- Strongest safe reading: exact local overflow jump tail to `9A98`.

### C2:CF61..C2:CF91  ct_c2_sibling_0d1d_gated_owner_with_54_vs_81_return_path_and_cf37_d4d5_negative_lane   [strong structural]
- Begins `JSR E984 ; BIT 0D1D`.
- Clear/non-overflow path compares exact byte `54` against exact byte `81`; when unequal, runs exact helper `EAC2`, then returns `RTS`.
- Negative path when exact byte `54 == 03` runs exact helper `CF37`, seeds exact byte `68 = 01`, runs exact helper `D4D5`, and exits through exact jump `CF21`.
- All other negative / overflow cases run exact helper `EAC2`, seed exact byte `68 = 01`, and exit through exact jump `D4D5`.
- Strongest safe reading: exact sibling `0D1D`-gated owner that either returns after a `54 vs 81` compare, or routes through the `CF37 / D4D5` negative-family service lane.

### C2:CF92..C2:CFA1  ct_c2_0d9b_decrementing_wrapper_reusing_shared_cf88_negative_overflow_tail   [strong structural]
- Decrements exact byte `0D9B`.
- Runs exact helper `E984` and tests exact status byte `0D1D`.
- When neither negative nor overflow are set, returns immediately.
- When either negative or overflow is active, branches into the exact shared tail at `CF88`.
- Strongest safe reading: exact `0D9B`-decrementing wrapper that conditionally reuses the shared `CF88` negative/overflow service tail.

### C2:CFA2..C2:CFFA  ct_c2_state_refresh_strip_expander_owner_running_cffb_and_emitting_fc0d_fbdc_fc29   [strong structural]
- Mirrors exact byte `54 -> 79`, compares exact byte `54` against exact byte `7F`, then mirrors exact byte `54 -> 7F`.
- When the exact value changed, runs exact helper `EAC2`.
- Runs exact helper `CFFB`.
- In 16-bit mode clears exact word `3200`, performs exact overlapping same-bank block move `3200 -> 3202` for exact length `023E`, then copies exact `0012` bytes into exact destinations `5248` and `5288`.
- In 8-bit mode, when exact byte `0D49[79] != 0`, runs exact helper `D36C`.
- Emits exact selectors `FC0D`, `FBDC`, and `FC29` through exact helper `8385`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact state-refresh / strip-expansion owner that refreshes the `54/79/7F` state, runs exact initializer `CFFB`, expands the exact `3200` work strip into exact downstream buffers `5248/5288`, optionally runs `D36C`, then emits three exact selector packets.

### C2:CFFB..C2:D048  ct_c2_callable_block_template_initializer_copying_d044_d064_into_9720_and_stamping_969d_969e_slot_metadata   [strong structural]
- Direct callable entry used by the newly-frozen `CFA2` owner and other live callers.
- Copies exact `0021` bytes from exact embedded source `C2:D044..C2:D064` into exact WRAM destination `7E:9720`.
- Copies exact `0010` bytes from exact source `7E:9710` into exact destination `7E:969A`.
- Seeds exact words `9694 = 969A`, `9696 = 9300`, and `9698 = 0010`.
- In 8-bit mode derives exact index `X = 7F * 3`.
- Writes exact byte `20` into exact slot `969D,X`.
- Sets exact bits `0xC0` in exact word/byte `0D13`.
- In 16-bit mode writes exact word `9740` into exact slot `969E,X`.
- Exits `PLP ; RTS`.
- Strongest safe reading: exact callable block/template initializer that copies one embedded exact 0x21-byte template into `9720`, mirrors a 16-byte exact WRAM strip into `969A`, seeds exact metadata words `9694/9696/9698`, and stamps a per-slot exact 3-byte descriptor keyed by exact byte `7F` while arming exact bits `0xC0` in `0D13`.

## Alias / wrapper / caution labels

## Honest remaining gap

- broader gameplay-facing nouns are still open for `7E:0F0F`, `7E:0D1F`, and the wider role of `7E:0D8B / 0D8C / 0D90`
- the broader top-level family noun for `C2:A886..C2:AA30` is still not tight enough
- the next real code seam now moves naturally to `C2:D065..C2:D0C5`
