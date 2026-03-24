# Chrono Trigger Labels — Pass 92

## Purpose
Pass 91 froze the downstream tail enough to stop treating it like three raw addresses, but the next exact helper pair was still open:

- `CD:025E..`
- `C0:000B / C0:1BE6..`

Pass 92 closes that seam materially.

The strongest keepable result is:

- `CD:025E..0295` is an exact shared **selector/workspace setup helper** for the `020C..0214` packet plus the `0239 -> C2:0003 -> C2:0009` follow-up chain
- `C0:000B..000D` is an exact veneer to `C0:1BE6`
- `C0:1BE6..1CFB` is an exact gated **multi-packet `C7:0004` submit helper** with one alternate second-packet path selected only when `7F:01EC == 1` and `2A1F.bit5` is clear; if `2A1F.bit6` is set it collapses to the same one-packet `0x70` path already seen at `1BAB`

I am still keeping the final engine-facing noun of `C2:0003`, `C2:0009`, and `C7:0004` one notch below frozen.

---

## Strong labels

### CD:025E..CD:0295  ct_cd_seed_020c_0214_call_packet_clear_b400_b7ff_and_run_c2_dual_call_tail   [strong structural]
- Entry writes exact local packet/workspace fields:
  - caller `A` into `020C`
  - clears `CCED`
  - clears `02A1`
  - seeds `0210 = B400`
  - seeds `0212 = 007E`
  - clears `0214`
- Then runs exact clear helper `JSR $0239`.
- Then calls exact external helper `JSL C2:0003`.
- Then seeds exact `0213 = 0x6040`.
- Then calls exact external helper `JSL C2:0009`.
- Then runs exact local tail `JSR $3E7D ; JSR $3E7D ; LDA #$0010 ; STA $CCEC ; INC $CA24 ; RTS`.
- Clean in-bank shared callsites include `CD:01D2`, `CD:0222`, `CD:02AD`, `CD:02FF`, and `CD:032F`.
- Strongest safe reading: shared selector/workspace setup helper for the `020C..0214` packet plus the `0239 -> C2:0003 -> C2:0009` follow-up chain.

### C0:000B..C0:000D  ct_c0_branch_long_to_1be6_gated_multi_packet_c70004_submitter_veneer   [strong]
- Exact body: `BRL $1BD8`.
- Lands at exact target `C0:1BE6`.
- Strongest safe reading: veneer for the sibling gated multi-packet submit helper in the same low-bank packet/submit cluster as `0008 -> 1BAB`.

### C0:1BE6..C0:1CFB  ct_c0_submit_gated_multi_packet_c70004_sequence_by_7f01ec_and_2a1f_bits   [strong structural]
- Saves `B` and `D`, sets `D = 0x0100`, and sets `DB = 0x00`.
- Reads exact byte `7F:01EC` and only treats exact value `1` specially.
- The alternate long-branch packet body at `1C90` is selected **only when** `7F:01EC == 1` and `2A1F.bit5 == 0`.
- Otherwise control continues to the default path at `1C09`.
- The default path branches on exact mask `2A1F.bit6`.
- If `2A1F.bit6 != 0`, it collapses to the exact one-packet path:
  - `1E01 = 0x00`
  - `1E00 = 0x70`
  - `JSL C7:0004`
- If `2A1F.bit6 == 0`, the default path submits the following exact 5-packet sequence through repeated `JSL C7:0004`:
  1. `1E10=00, 1E01=00, 1E02=00, 1E03=FF, 1E00=81`
  2. `1E01=[7E:29AE], 1E00=11`
  3. `1E01=40, 1E02=FF, 1E03=FF, 1E00=81`
  4. `1E01=00, 1E02=FF, 1E00=82`
  5. `1E01=00, 1E02=FF, 1E00=83`
- The alternate path at `1C90` preserves the same surrounding structure but changes the second packet to:
  - `1E01=26, 1E00=14`
  and uses `1E01=80` instead of `40` in the following `0x81` packet.
- Restores `D` and `B`, then returns with `RTL`.
- Strongest safe reading: gated multi-packet `C7:0004` submit helper with one exact alternate second-packet path selected by `7F:01EC` and `2A1F.bit5`, plus the same `2A1F.bit6` one-packet collapse already seen at `1BAB`.

---

## Strengthened RAM / workspace labels

### 7E:020C..7E:0214  ct_cd_shared_c2_dual_call_packet_workspace_seeded_by_025e   [provisional strengthened]
- Pass 92 proves `CD:025E..0295` seeds this exact packet/workspace family before calling `C2:0003` and `C2:0009`.
- Exact seeded members include:
  - caller `A` into `020C`
  - `0210 = B400`
  - `0212 = 007E`
  - `0213 = 0x6040`
  - `0214` cleared before the pair runs
- Strongest safe reading: shared packet/workspace family for the exact `C2:0003 -> C2:0009` follow-up chain.

### 7F:01EC  ct_c0_multi_packet_submit_special_case_selector_byte   [provisional strengthened]
- Pass 92 proves `C0:1BE6..1CFB` only treats exact value `1` specially.
- That exact special case then still requires `2A1F.bit5 == 0` before selecting the alternate packet body at `1C90`.
- Strongest safe reading: special-case selector byte for the sibling gated multi-packet submit helper.

### 7E:29AE  ct_c0_multi_packet_submit_default_second_packet_byte   [provisional strengthened]
- Pass 92 proves the default `bit6 == 0` packet sequence at `C0:1BE6` reads this exact byte into `1E01` before submitting packet `1E00 = 0x11`.
- Strongest safe reading: live byte consumed as the default second-packet payload in the sibling multi-packet submit path.

---

## Honest caution kept explicit
Even after this pass:

- I have **not** frozen the final engine-facing noun of `C2:0003`.
- I have **not** frozen the final engine-facing noun of `C2:0009`.
- I have **not** frozen the final engine-facing noun of `C7:0004`; pass 91 + pass 92 now freeze multiple exact local packet builders and submit sequences around it, not the final subsystem name.
- I have **not** frozen the final gameplay-facing noun of the broader pass-88/89 lane+raster workspace.
- I have **not** returned to the first exact clean-code external reader of `CE0F` yet.
