# Chrono Trigger Disassembly Labels — Pass 51

This file contains labels newly added, replaced, or materially strengthened in pass 51.

As in prior passes:
- **strong** = directly supported by control flow and data role in the ROM work of this pass
- **strengthened** = previously useful label materially tightened by new proof
- **provisional** = structurally useful but still not safe as a final frozen name

---

## Strong labels

### FD:B820..FD:B850  ct_fd_seed_visible_lane_readiness_from_speed_like_stat         [strong]
- Iterates selected visible participants.
- Clamps record byte `+0x38` to `0x10`.
- Uses the clamped value to index `CC:2E31`.
- Combines that table value with a `0x69` base and local `$2C` bias term.
- Stores the result to both `B158` and `AFAB`.
- Sets `B03A = 1` for the affected visible lane.
- Strongest safe reading: battle-side visible-lane readiness seed writer keyed by a speed-like stat.

### CC:2E31  ct_cc_speed_like_stat_to_readiness_bonus_table                           [strong]
- 16-byte signed step table:
  `CD D1 D5 D9 DD E1 E5 E9 ED F1 F5 F9 FD 01 05 09`
- Smooth +4-step ladder from negative to small positive bonus.
- Consumed directly by the `FD:B820..B850` readiness seed family.
- Strongest safe reading: speed-like stat -> readiness bonus table.

### C1:B390  ct_c1_seed_lane_gauge_exports_from_b158                                 [strong]
- Directly mirrors `B158,Y` into:
  - `AFAB,Y`
  - `99DD,Y`
  - `9F22,Y`
- Strongest safe reading: direct seed/export mirror from the upstream readiness seed value.

---

## Strengthened labels

### 7E:99DD  ct_c1_lane_active_time_gauge_current_fill_export                        [strengthened]
- `C1:06F0` loads it as the renderer numerator/current-side value.
- Goal-only update families do **not** necessarily overwrite it.
- Snap/full commit families explicitly mirror it equal to `9F22`.
- Replaces the looser “progress export” wording with a harder current-fill role.

### 7E:9F22  ct_c1_lane_active_time_gauge_goal_or_cap_export                         [strengthened]
- `C1:06F0` loads it as the denominator/goal-side value for the gauge math.
- `C1:BE00..BE2A` updates it without also updating `99DD`.
- Equal-write paths force `99DD == 9F22` to export a full/ready bar.
- Replaces the narrower pass-50 “cap export” wording with a harder goal/denominator role.

### C1:06F0  ct_c1_render_lane_active_time_gauge_into_0cc0                          [strengthened]
- Pass 50 already tied it to the readiness gauge.
- Pass 51 tightens the exact consumed pair to:
  - current fill = `99DD`
  - goal/cap = `9F22`
- The human-facing readiness-gauge name holds and the math-side split is now much cleaner.

### 7E:B158  ct_c1_lane_readiness_seed_value                                        [strengthened]
- This pass proves `B158` is a direct upstream seed into the visible lane-gauge branch.
- `C1:B390` mirrors it directly into `AFAB/99DD/9F22`.
- `FD:B820..B850` seeds it from a speed-like stat and bonus table.
- This is a stronger and safer description than the older purely generic scalar wording.

### 7E:AFAB  ct_c1_lane_readiness_work_value                                        [strengthened]
- Receives the same upstream seed as `B158` in the battle-side writer families.
- Is also the working value advanced by the later goal/snap export families.
- Stronger now as the work-value/shadow branch for the lane readiness gauge.

---

## Provisional labels

### 7E:[participant_record + 0x38]  ct_battle_participant_speed_like_stat           [provisional]
- Clamped to `0x10` by `FD:B820..B850` before indexing `CC:2E31`.
- Functionally it behaves like the stat that seeds readiness/initiative gain.
- Final human-facing freeze as exactly “speed” is deferred until the surrounding participant record layout is tighter.

### FD:B8C0..FD:B8E0  ct_fd_seed_visible_lane_readiness_sibling_family              [provisional]
- Structural sibling of `FD:B820..B850`.
- Writes to `B15B/AFAE` and sets `B03D`.
- Almost certainly the adjacent visible-lane seed family, but still worth one more pass before freezing the final name.

### 7E:B03A  ct_c1_visible_lane_readiness_seed_valid_flag                           [provisional]
- Set to `1` by the primary visible-lane seed family at `FD:B820..B850`.
- Strongly looks like a “valid/seeded/armed” lane flag.
- Final freeze deferred until the sibling `B03D` path is fully aligned.

---

## Replaced / retired wording

### 7E:99DD old wording “lane_active_time_gauge_progress_export”                    [replaced]
- Too generic after the renderer-side numerator proof.
- Replaced by `ct_c1_lane_active_time_gauge_current_fill_export`.

### 7E:9F22 old wording “lane_active_time_gauge_cap_export”                         [replaced]
- Too narrow after the goal-only update path at `C1:BE00..BE2A` and the snap/full mirror paths.
- Replaced by `ct_c1_lane_active_time_gauge_goal_or_cap_export`.

### 7E:B158 old wording “lane_base_active_time_increment”                           [soft-replaced]
- Pass 50's increment wording was useful but too narrow.
- Pass 51 proves `B158` is at least a direct upstream seed value for the readiness-gauge branch.
- Soft-replaced by `ct_c1_lane_readiness_seed_value` pending one more pass on exact subroles.

### 7E:AFAB old wording “lane_active_time_increment_shadow”                         [soft-replaced]
- Too narrow after the direct seed/export mirror proof and the later working-value advances.
- Soft-replaced by `ct_c1_lane_readiness_work_value`.

---

## Still intentionally unresolved

### Exact human-facing identity of participant record byte `+0x38`                  [unresolved]
- Functionally it behaves like the speed/readiness stat.
- Final freeze as exactly “speed” is deferred one more step.

### Exact source and meaning of local `$2C` in `FD:B820..B850`                      [unresolved]
- It is clearly part of the readiness seed formula.
- Whether it is randomness, formation bias, or another small adjustment still needs one more direct caller pass.

### Exact final role split between `B158` and `AFAB` across every update family     [unresolved]
- This pass proves both participate in the readiness branch more concretely.
- One more pass is still worth doing before freezing their final long-term names.
