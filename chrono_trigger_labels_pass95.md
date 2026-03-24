# Chrono Trigger Labels — Pass 95

## Purpose
Pass 94 isolated two still-open seams cleanly:

- the downstream C2 family cluster at `5BF5 / 5C3E / 5C77`
- the active C7 `0x10/11/14/15` path at `01A1`

Pass 95 closes both structurally enough to stop treating them as anonymous branches.

The strongest keepable result is:

- the three downstream C2 families are now an exact **chained three-family long-stream stage** over `[0237]` with counter-driven exits keyed by `023A` and `0213`
- the `C7:01A1` side is now a real **negative-`1E05` special path** with exact internal phase boundaries:
  - candidate rebuild / staging at `01A1..0216`
  - live-slot reconcile / migration at `0217..0325`
  - staged command-`0x02` emit at `037B..04B0`

That is a real noun upgrade, not wording polish.

---

## Strong labels

### C2:5BF5..C2:5C3D  ct_c2_consume_first_downstream_long_stream_family_into_0235_then_route_by_023a_0213_exhaustion   [strong structural]
- Consumes the active long-pointer stream through exact direct-page indirect-long reads from `[0237]`.
- Advances the live pointer by exact `INC 0237` steps.
- Materializes the consumed entry into exact local word `0235`.
- Calls exact shared helper `JSR $5DC4`.
- Decrements exact counters `023A` and `0213`.
- Reduces their post-decrement zero/nonzero state to a four-way indexed jump through the exact table at `5C28`.
- Exact four-way outcomes now frozen:
  - both exhausted -> force `0215 = 0x10`, return
  - `023A` remains but `0213` exhausted -> store the live tail state directly into `0215`, return
  - `023A` exhausted but `0213` remains -> jump back to `58B2`
  - both remain -> enter the next downstream family at `5C3C/5C3E`
- Strongest safe reading: first downstream long-stream family behind `58B2`, routing by the exact exhaustion state of `023A` and `0213`.

### C2:5C3E..C2:5C76  ct_c2_consume_second_downstream_long_stream_family_with_exact_c2d4_rebase_before_shared_materializer   [strong structural]
- Consumes the next entry from the same exact long pointer `[0237]`.
- Adds exact base `C2:D4` before storing the word into `0235`.
- Calls the same exact shared helper `JSR $5DC4`.
- Decrements the same exact counters `023A` and `0213`.
- Dispatches through the exact four-entry jump table at `5C61`.
- Exact outcomes now frozen:
  - case 0 -> clears `0230`, forces `0215 = 0x10`, returns
  - case 1 -> forces `0215 = 0x10`, returns
  - case 2 -> clears `0230`, jumps back to `58B2`
  - case 3 -> branches directly into the third family at `5C77`
- Strongest safe reading: second downstream long-stream family with an exact `+C2D4` rebasing step before the shared materializer runs.

### C2:5C77..C2:5CBF  ct_c2_consume_terminal_downstream_long_stream_family_and_self_loop_while_both_counters_remain_live   [strong structural]
- Reuses the same exact long pointer `[0237]`, exact `0235` materialization, exact `JSR $5DC4`, and exact decrement pair `023A` / `0213`.
- Dispatches through the exact four-entry jump table at `5CAA`.
- Exact outcomes now frozen:
  - case 0 -> clears `0230`, forces `0215 = 0x10`, returns
  - case 1 -> forces `0215 = 0x10`, returns
  - case 2 -> clears `0230`, jumps back to `58B2`
  - case 3 -> branches back into `5C77` itself
- Strongest safe reading: terminal self-looping downstream family in the chained C2 long-stream stage.

### C2:5D1D..C2:5D55  ct_c2_scan_active_long_stream_for_exact_ef_or_00_sentinels_with_bounded_lengths   [strong]
- Contains three exact bounded scanners over `[0237],Y`:
  - scan for `0xEF` up to `Y == 0x000A`
  - scan for `0xEF` up to `Y == 0x000B`
  - scan for `0x00` up to `Y == 0x0005`
- Each returns the exact `Y` position.
- Strongest safe reading: local bounded sentinel-scan helper cluster used to derive inner counts from the active long stream.

### C7:01A1..C7:0216  ct_c7_negative_1e05_special_path_rebuild_candidate_slot_strips_at_1f00_and_1f20_before_reconcile   [strong structural]
- Validates exact selector byte `1E01` against exact long value at `C7:0AE9`.
- Calls exact local helpers `0734` and `0A39`.
- Copies `1E01 -> 1E05`.
- Clears two exact 0x20-byte strips through the loop over `1EFE..1F1E` and `1F1E..1F3E`.
- Scans backward through exact live strip `1E20..1E3E` to seed the last-active index in `0C`.
- Seeds exact staging pointers:
  - `12 = 1F00`
  - `14 = 1F20`
- Walks the exact long table rooted at `C7:0E11`:
  - writes nonzero entries into `[12]` / `1F00..`
  - writes entries not already present in `1E20..1E3E` into `[14]` / `1F20..`
- If `1F20 == 0`, jumps directly to `037B`.
- Strongest safe reading: candidate rebuild / staging gate for the negative-`1E05` special sound-command path.

### C7:0217..C7:0325  ct_c7_reconcile_unmatched_1f20_candidates_into_live_1e20_1e40_1e60_slot_state_using_apu_command_07   [strong structural]
- Prunes dead entries from live `1E20..1E3E` if absent from the candidate strip at `1F00..1F1E`.
- Finds the first open live slot and the last occupied live slot.
- If those are equal, jumps directly to `0326`.
- Otherwise sends exact APU command byte `0x07` through `$2141`.
- Iterates over unmatched/new strip `1F20..1F3E`.
- Migrates/mirrors exact values into the live strips `1E20..`, `1E40..`, and `1E62..` while writing exact triplets through `$2142/$2143`.
- Updates exact local byte `84` through repeated calls to `09DA`.
- On the no-free-slot path, sends exact zero payload through `$2142/$2143` and rebuilds `1EFE..1F7E` from exact table `C7:0E0F`.
- Strongest safe reading: live-slot reconcile / migration phase of the negative-`1E05` path using APU command `0x07`.

### C7:037B..C7:04B0  ct_c7_emit_staged_special_path_blocks_from_1f80_with_apu_command_02   [strong structural]
- Seeds exact pointer `12 = 1F80`.
- Walks candidate strip `1F00..1F1E` and writes paired output words into `1F80..`.
- Uses exact long table `C7:0BA4` for the paired-output build when entries are already present in live `1E20..`.
- Sends an exact command-`0x02` block header through APU ports:
  - `$2143 = 0x1E`
  - `$2142 = 0x80`
  - `$2141 = 0x02`
- Streams the exact staged `1F80..1FBF` block.
- Sends two more exact command-`0x02` blocks rooted at:
  - `1F40..` using exact table `C7:0C20`
  - `1FC0..` using exact table `C7:0C9C`
- Repeatedly updates exact local byte `84` through `JSR 09DA` and normalizes it back to `0xE0`.
- Strongest safe reading: staged command-`0x02` emit phase of the negative-`1E05` special sound-command path.

---

## Strengthened RAM / workspace labels

### 7E:0237..7E:023A  ct_c2_active_long_stream_cursor_and_inner_counter_family_for_downstream_chained_handlers   [provisional strengthened]
- Pass 94 already proved `58B2` seeds this family from the exact table rooted at `DE:FA00`.
- Pass 95 proves more of the exact consumer contract:
  - `0237..0239` is the active long stream cursor consumed by `5BF5 / 5C3E / 5C77`
  - `023A` is decremented by all three downstream families and participates in the exact four-way tail routing
- Strongest safe reading: active long stream cursor + inner counter family for the chained downstream C2 handlers.

### 00:1F00..00:1FC0  ct_c7_negative_1e05_special_path_candidate_unmatched_and_emit_staging_strips   [provisional strengthened]
- Pass 95 proves this low-bank workspace is not generic scratch.
- Exact proven roles now include:
  - `1F00..1F1E` = candidate strip rebuilt from exact table `C7:0E11`
  - `1F20..1F3E` = unmatched/new candidate strip not already present in live `1E20..`
  - `1F80..1FBF` = staged paired output block later sent with exact APU command `0x02`
  - `1FC0..` = later exact command-`0x02` table-backed emit source
- Strongest safe reading: candidate/unmatched/emit staging workspace for the negative-`1E05` special sound-command path.

---

## Honest caution kept explicit
Even after this pass:

- I have **not** frozen the final gameplay-facing noun of the broader C2 stream language behind `58B2 / 5BF5 / 5C3E / 5C77`.
- I have **not** frozen the exact semantic meaning of helpers `0734`, `0A39`, `0655`, and the later `04B1..061B` tail of the `01A1` path.
- I have **not** returned to the first exact clean-code external reader of `CE0F` yet.
- I **have** crossed an important structural threshold: the `01A1` side is no longer honestly describable as just “the active branch of the early C7 gate”.
