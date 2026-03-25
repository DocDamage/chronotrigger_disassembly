# Chrono Trigger Labels — Pass 91

## Purpose
Pass 90 froze the local D1 caller-side contract, but the three exact downstream follow-up stages were still only named as raw addresses:

- `CE:EE6E`
- `CD:0235`
- `C0:0008`

Pass 91 closes that seam materially.

The strongest keepable result is:

- `CE:EE6E..EF0D` is an exact selector/side-driven **nine-record template seeder** into `C867..C9EC`
- `CD:0235..0238` is an exact veneer, and `CD:0239..025D` is the exact **eight-strip workspace clear** behind it
- `C0:0008..000A` is an exact veneer to `C0:1BAB`
- `C0:1BAB..1BE5` is an exact **conditional one-packet `C7:0004` submit helper** selected by `2A1F.bit6`

I am still keeping the final gameplay-facing noun of the broader lane/raster pipeline one notch below frozen.

---

## Strong labels

### CE:EE6E..CE:EF0D  ct_ce_seed_nine_stride_2d_template_records_into_c867_c9ec_from_selector_offset_table_and_2a21_side_bit   [strong structural]
- Entry `A` is doubled with `ASL A` and used to index the exact 16-bit offset table at `CE:F24E`.
- The fetched word becomes an exact byte offset into the flat source-record family rooted at `CE:F58E`.
- The routine loads 9 exact source offsets from one 10-word source record.
- The seventh copied block is selected from one of two exact record words depending on `2A21.bit0`.
- Uses 9 exact `MVN` copies from bank `CE` to bank `7E`, each with `A = 0x001D`, so each copy is exactly `0x1E` bytes long.
- Exact destination roots are: `C867`, `C894`, `C8C1`, `C8EE`, `C91B`, `C948`, `C975`, `C9A2`, `C9CF`.
- Those roots are spaced by an exact stride of `0x2D` bytes.
- Strongest safe reading: selector/side-driven template-record seeder for the nine-record `C867..C9EC` workspace.

### CD:0235..CD:0238  ct_cd_clear_b400_b7ff_eight_strip_workspace_veneer   [strong]
- Exact body: `JSR $0239 ; RTL`.
- Strongest safe reading: veneer for the exact `B400..B7FF` clear helper immediately upstream of the final low-bank follow-up stage.

### CD:0239..CD:025D  ct_cd_clear_contiguous_b400_b7ff_eight_strip_workspace   [strong structural]
- Exact body begins with `REP #$20 ; TDC ; LDX #$0080`.
- Stores zero words into exact bases `B3FE / B47E / B4FE / B57E / B5FE / B67E / B6FE / B77E` while `X` decrements by 2.
- Exact cleared spans are:
  - `B400..B47F`
  - `B480..B4FF`
  - `B500..B57F`
  - `B580..B5FF`
  - `B600..B67F`
  - `B680..B6FF`
  - `B700..B77F`
  - `B780..B7FF`
- Strongest safe reading: exact clear helper for the contiguous eight-strip `B400..B7FF` workspace.

### C0:0008..C0:000A  ct_c0_branch_long_to_1bab_conditional_c70004_packet_submitter_veneer   [strong]
- Exact body: `BRL $1BA0`.
- Lands at exact target `C0:1BAB`.
- Strongest safe reading: veneer for the conditional packet-submit helper behind the pass-90 follow-up tail.

### C0:1BAB..C0:1BE5  ct_c0_submit_one_of_two_c70004_command_packets_by_2a1f_bit6   [strong structural]
- Saves `B` and `D`, sets `D = 0x0100`, and sets `DB = 0x00`.
- Reads `7E:2A1F` and branches on exact mask `0x40`.
- If `2A1F.bit6 == 0`:
  - writes `1E10 = 0xFF`
  - writes `1E01` from exact direct-page byte `$FA` after `D = 0x0100`
  - writes `1E00 = 0x14`
  - then calls `JSL C7:0004`
- If `2A1F.bit6 != 0`:
  - writes `1E01 = 0x01`
  - writes `1E00 = 0x70`
  - then calls `JSL C7:0004`
- Restores `D` and `B`, then returns with `RTL`.
- Strongest safe reading: conditional one-packet `C7:0004` submit helper behind `C0:0008`.

---

## Strengthened RAM / workspace labels

### 7E:C867..7E:C9EC  ct_ce_nine_stride_2d_template_record_workspace_seeded_by_ee6e   [provisional strengthened]
- Pass 91 proves `CE:EE6E..EF0D` copies exact `0x1E`-byte blocks into 9 exact destination records rooted at `C867 / C894 / C8C1 / C8EE / C91B / C948 / C975 / C9A2 / C9CF`.
- The roots are spaced by an exact stride of `0x2D` bytes.
- Strongest safe reading: nine-record template workspace seeded directly by the first exact CE follow-up stage.

### 7E:B400..7E:B7FF  ct_cd_contiguous_eight_strip_workspace_cleared_by_0239_before_c0_followup   [provisional strengthened]
- Pass 91 proves `CD:0239..025D` clears this exact contiguous `0x0400`-byte span as eight exact `0x80`-byte strips.
- `D1:F331..F410` calls `CD:0235` immediately before `C0:0008`.
- Strongest safe reading: contiguous eight-strip workspace cleared just before the final C0 follow-up stage.

---

## Honest caution kept explicit
Even after this pass:

- I have **not** frozen the final gameplay-facing noun of the broader pass-88/89 lane+raster workspace.
- I have **not** frozen the final gameplay-facing noun of the `C867..C9EC` template-record workspace.
- I have **not** frozen the exact role of `C7:0004`; pass 91 only freezes the exact packet builder / submitter behind `C0:0008`.
- I have **not** returned to the first exact clean-code external reader of `CE0F` yet.
