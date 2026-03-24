# Chrono Trigger Labels — Pass 93

## Purpose
Pass 92 proved the downstream tail is no longer bottlenecked by unnamed local helpers.
The exact external bottleneck was:

- `C2:0003`
- `C2:0009`
- `C7:0004`

Pass 93 closes that seam enough to stop treating those as raw engine-facing addresses.

The strongest keepable result is:

- `C2:0003..0005` is an exact veneer to `C2:57DF`
- `C2:0009..000B` is an exact veneer to `C2:5823`
- `C2:57DF..5822` is an exact **stream-state initializer** behind the `020C..0214` packet workspace
- `C2:5823..5841` is an exact **four-family token/stream dispatcher** over that prepared state
- `C7:0004..0006` is an exact veneer to `C7:0140`
- `C7:0140..019D` is an exact **low-bank packet opcode-family dispatcher** over the `1E00..` command packet workspace

This also resolves the percentage question honestly:
- I am **not** stuck
- the completion script is deliberately blunt right now
- `bank_separation_score` and `rebuild_readiness_score` are still hard-coded constants (`24.0` and `8.0`) inside `scripts/ct_completion_score.py`
- so late semantic passes can move the project forward materially while the top-line percent barely changes

---

## Strong labels

### C2:0003..C2:0005  ct_c2_branch_to_57df_stream_state_initializer_veneer   [strong]
- Exact body: `JMP $57DF`.
- Lands at exact target `C2:57DF`.
- Strongest safe reading: veneer for the stream-state initializer behind the `CD:025E` dual-call tail.

### C2:0009..C2:000B  ct_c2_branch_to_5823_stream_token_dispatch_stage_veneer   [strong]
- Exact body: `JMP $5823`.
- Lands at exact target `C2:5823`.
- Strongest safe reading: veneer for the token/stream dispatch stage immediately following `C2:0003` in the `CD:025E` follow-up chain.

### C2:57DF..C2:5822  ct_c2_init_stream_state_from_020c_0214_packet_workspace   [strong structural]
- Exact prologue saves flags and direct page, then sets `D = 0x0200`.
- Treats `020C` as an index/selector:
  - masks it to `00FF`
  - doubles it
  - uses it as `Y`
- Reads a **16-bit entry** through exact long-indirect pointer `[020D],Y` and stores that into `0231`.
- Copies exact byte `020F -> 0233`.
- Therefore proves the live `020D..020F` packet family is consumed as a long pointer base for the selected stream/table entry.
- Seeds exact local state:
  - `0230 = 00`
  - `0234 = 00` or `08` depending on exact comparison of `0214` with `02`
  - if `0214` is negative, forcibly clears `0234`
  - `0215 = 04`
  - `023D = 0200`
  - `023F = 00`
  - `0217 = 00`
- Returns immediately with `RTL` after the seed.
- Strongest safe reading: exact stream-state initializer behind the `020C..0214` packet/workspace family used by `CD:025E` before `C2:0009` runs.

### C2:5823..C2:5841  ct_c2_dispatch_prepared_stream_state_into_four_handler_families   [strong structural]
- Exact prologue saves flags and direct page, then sets `D = 0x0200`.
- Calls exact local helper `JSR $584A`.
- If that helper returns carry set, exits immediately.
- Otherwise reads exact local mode/state byte `0230`.
- Doubles that byte and dispatches through the exact four-entry table at `5842`:
  - `58B2`
  - `5BF5`
  - `5C3E`
  - `5C77`
- Clears `A` on the common exit path, restores state, then returns with `RTL`.
- Strongest safe reading: exact token/stream dispatch stage over the state seeded by `57DF`, with four concrete downstream handler families.

### C7:0004..C7:0006  ct_c7_branch_to_0140_low_bank_packet_dispatcher_veneer   [strong]
- Exact body: `JMP $0140`.
- Lands at exact target `C7:0140`.
- Strongest safe reading: veneer for the low-bank packet opcode-family dispatcher behind all the `1E00..` command-packet submit helpers.

### C7:0140..C7:019D  ct_c7_dispatch_1e00_packet_opcode_families_into_low_bank_handlers   [strong structural]
- Exact prologue saves `B`, `D`, flags, `A`, `X`, and `Y`.
- Sets exact direct page to `D = 0x1E00`.
- Forces `DB = 0x00`.
- Reads exact packet header bytes from the `1E00..` workspace, including `1E00` and `1E05`.
- If `1E05` is negative, diverts into the special path at `01A1`.
- If `1E00 == 00`, exits immediately.
- Exact opcode-family split from `1E00` is now frozen:
  - `0x10..0x17` -> indexed indirect jump through table `0AD9`
  - `0x18..0x2F` -> `JMP $061C`
  - `0x30..0x3F` -> `JMP $071D`
  - `0x70` -> `JMP $08E3`
  - `0x71` -> `JMP $0755`
- Unsupported / finished paths clear exact byte `1E00` before restoring state and returning with `RTL`.
- Strongest safe reading: exact low-bank packet opcode-family dispatcher over the `1E00..` command packet workspace.

---

## Strengthened RAM / workspace labels

### 7E:020C..7E:0214  ct_cd_shared_c2_dual_call_packet_workspace_seeded_by_025e   [provisional strengthened]
- Pass 92 proved `CD:025E..0295` seeds this exact packet/workspace family before calling `C2:0003` and `C2:0009`.
- Pass 93 now proves more of the exact consumer contract:
  - `020C` is used as a masked/doubled selector index
  - `020D..020F` are consumed as a long pointer base by `C2:57DF`
  - `0214` controls the seed of exact local byte `0234`
- Strongest safe reading: shared C2 dual-call packet workspace whose selector/pointer family is consumed directly by the `57DF -> 5823` chain.

### 00:1E00..00:1E05  ct_c7_low_bank_command_packet_header_workspace   [provisional strengthened]
- Pass 93 proves `C7:0140..019D` sets `D = 0x1E00` and consumes exact header bytes from this low-bank workspace.
- Exact proven fields now include:
  - `1E00` = packet opcode / opcode family selector
  - `1E05` = signed control byte that can divert into the special path at `01A1`
- Strongest safe reading: low-bank command-packet header workspace consumed by the `C7:0004 -> 0140` dispatcher.

---

## Honest caution kept explicit
Even after this pass:

- I have **not** frozen the final high-level noun of the downstream `58B2 / 5BF5 / 5C3E / 5C77` handler families.
- I have **not** frozen the final gameplay-facing noun of the broader pass-88/89 lane+raster workspace.
- I have **not** returned to the first exact clean-code external reader of `CE0F` yet.
- I do now have enough exact structure to stop calling `C2:0003`, `C2:0009`, and `C7:0004` generic mystery addresses.
