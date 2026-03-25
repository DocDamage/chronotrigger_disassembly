# Chrono Trigger Disassembly Labels — Pass 50

This file contains labels newly added, replaced, or materially strengthened in pass 50.

As in prior passes:
- **strong** = directly supported by control flow and data role in the ROM work of this pass
- **strengthened** = previously useful label materially tightened by new proof
- **provisional** = structurally useful but still not safe as a final frozen name

---

## Strong labels

### C1:BD6F  ct_c1_apply_status_modifiers_to_lane_time_increment         [strong]
- Starts from `AFAB[x]`.
- Halves it when the `5E4D|5E52` status family has bit `0x80` set.
- Doubles it with saturation when `5E4B` bit `0x20` is set.
- Forces a minimum of `1`.
- Mirrors the adjusted value to `99DD/9F22` for visible party lanes.
- Strongest safe reading: shared status-modifier helper for the lane active-time/readiness increment.

### C1:B725  ct_c1_init_lane_active_time_gauge_exports                  [strong]
- Clears the visible lane-progress exports `99DD..99DF`.
- Seeds the visible lane-threshold/cap exports `9F22..9F24` to `0x30`.
- Also resets the nearby pending-lane/FIFO state.
- Strongest safe reading: initialization of the visible active-time/readiness gauge export family.

---

## Strengthened labels

### C1:06F0  ct_c1_render_lane_active_time_gauge_into_0cc0             [strengthened]
- Pass 47 proved this was a scaled segmented bar renderer.
- Pass 50 tightens the gameplay-facing meaning of that bar through the upstream producer family.
- Best reading now: render the party-lane active-time/readiness gauge into the `0CC0` strip.

### 7E:B158  ct_c1_lane_base_active_time_increment                     [strengthened]
- Repeatedly copied into `AFAB` before `BD6F` is applied.
- Feeds the visible lane-bar branch through the status-modified increment family.
- Best reading now: base active-time/readiness increment.

### 7E:AFAB  ct_c1_lane_active_time_increment_shadow                    [strengthened]
- Working shadow derived from `B158`.
- Modified by `BD6F` through slow-like / haste-like status effects.
- Consumed by the gauge-advance families at `BDE0/BE50/BED0`.
- Best reading now: status-adjusted active-time/readiness increment shadow.

### 7E:99DD  ct_c1_lane_active_time_gauge_progress_export              [strengthened]
- Visible lane-bar input used by `C1:06F0`.
- Initialized to zero by `B725`.
- Updated in the readiness-gauge advance families.
- Best reading now: visible active-time/readiness gauge progress export.

### 7E:9F22  ct_c1_lane_active_time_gauge_cap_export                   [strengthened]
- Second visible lane-bar input used by `C1:06F0`.
- Initialized to `0x30` by `B725`.
- Updated by the readiness-gauge advance families.
- Best reading now: visible active-time/readiness gauge threshold/cap export.

### C1:BDE0..C1:BF25  ct_c1_advance_lane_active_time_gauge_and_ready_transition_family [strengthened]
- Three sibling update families that:
  - seed `AFAB` from `B158`
  - apply `BD6F`
  - advance one or both lane-bar exports with saturation
  - set/update lane-ready side effects (`B03A`, `B188`, `93EE`)
- Best reading now: readiness-gauge advance and ready-transition family.

### 7E:0CC0..7E:0E08  ct_c1_companion_paired_byte_strip_buffer         [strengthened]
- Earlier passes had already established HP/max HP/MP numeric content and the segmented bar.
- Pass 50 tightens the bar specifically to the lane active-time/readiness gauge.
- The strip now reads more coherently as a battle-status lane display.

---

## Provisional labels

### 7E:99DE / 7E:99DF  ct_c1_lane_active_time_gauge_progress_export_1_2 [provisional]
### 7E:9F23 / 7E:9F24  ct_c1_lane_active_time_gauge_cap_export_1_2      [provisional]
- `B725` proves these are sibling exports for the other visible lanes.
- Their human-facing meaning matches lane 0 strongly.
- Kept grouped/provisional only because pass 50 focused on the branch semantics more than on per-lane alias cleanup.

### 7E:5E4B.bit5  ct_c1_lane_haste_like_rate_modifier_bit               [provisional]
### 7E:5E4D|7E:5E52 bit7  ct_c1_lane_slow_like_rate_modifier_bit_family [provisional]
- ROM proof is strong for the functional behavior:
  - one family doubles the increment
  - one family halves it
- Exact final human-facing status names are still intentionally kept one step conservative.

---

## Replaced / retired wording

### C1:06F0 old wording “render scaled lane bar into 0CC0”             [replaced]
- Too generic after pass 50.
- The ROM now supports a materially harder gameplay-facing reading: active-time/readiness gauge renderer.

### 7E:99DD old wording “display value for scaled bar”                 [replaced]
- Replaced by `ct_c1_lane_active_time_gauge_progress_export`.

### 7E:9F22 old wording “display divisor or capacity”                  [replaced]
- Replaced by `ct_c1_lane_active_time_gauge_cap_export`.

### 7E:B158 / 7E:AFAB old wording “primary carried scalar/shadow”      [replaced]
- Too abstract after the status-modified gauge-rate proof.
- Replaced by the active-time/readiness increment wording.

---

## Still intentionally unresolved

### Exact per-variant split between `99DD` and `9F22` in every ready-transition path [unresolved]
- The human-facing bar role is now hard enough.
- The exact current/frozen/threshold split per sibling advance variant is still worth tightening before freezing every sublabel.

### Exact actor-stat seed feeding `B158`                                [unresolved]
- `B158` is now materially harder as a base readiness increment.
- The cleanest exact upstream stat source is still a good next target.

### Exact final status names for the `5E4B / 5E4D / 5E52` modifier bits [unresolved]
- Functional behavior is proven.
- Exact status-name freezing is intentionally deferred one step.
