# Chrono Trigger Labels - Pass 56

## Purpose
This file records the label promotions and semantic upgrades justified by pass 56.

Pass 56 closes the direct producer side for the tail half of the 11-slot occupant-map family.
The main upgrades are:

- freeze `AEFF..AF09` and `AF0A..AF14` as unified contiguous 11-slot map families
- promote `FD:B2A3..B2DD` into the canonical tail-map builder
- strengthen `AEC6`
- strengthen `AF15.bit7`
- harden the tail meaning of `AF02..AF09` and `AF0D..AF14`

---

## Strong labels

### 7E:AEFF..AF09  ct_battle_slot_live_occupant_map                          [strengthened]
- Unified 11-slot live occupant map.
- Slots `0..2` = visible head live occupants.
- Slots `3..10` = tail live/materialized occupants.
- `FF` means unoccupied / not live in this map.

### 7E:AF0A..AF14  ct_battle_slot_canonical_occupant_map                     [strengthened]
- Unified 11-slot canonical/remembered occupant map.
- Head half built from the visible source path.
- Tail half built from the `29C4` source-record family.

### 7E:AEC6        ct_canonical_tail_slot_count                              [strong]
- Reset by the canonical tail-map builder at `FD:B2A3`.
- Incremented once per admitted tail source record.
- Counts populated canonical tail entries, not merely currently live tail occupants.

### 7E:AF02..AF09  ct_tail_live_occupant_submap                              [strong]
- Tail subrange of the unified live occupant map.
- Receives occupant IDs from the `29C4` source family.
- May be forced to `FF` while the canonical tail map still retains the occupant.

### 7E:AF0D..AF14  ct_tail_canonical_occupant_submap                         [strong]
- Tail subrange of the unified canonical/remembered occupant map.
- Always receives the admitted occupant ID when the tail-source gate passes.

### FD:B2A3..B2DD  ct_build_tail_live_and_canonical_occupant_maps            [strong]
- Iterates 8 source records with stride `0x0C` rooted at `29C4`.
- Uses:
  - `29C5 + n*0x0C` as the admit/skip gate
  - `29C4 + n*0x0C` as the copied occupant ID
  - `29C6 + n*0x0C` as the secondary live-withhold gate
- Populates:
  - `AF02..AF09`
  - `AF0D..AF14`
  - `AF15.bit7`
  - `AEC6`

---

## Strong bit-level label upgrades

### 7E:AF15 bit 7  ct_tail_canonical_present_but_not_live_flag               [strengthened]
- Set only when the tail-source builder keeps the canonical occupant (`AF0D`) but forces the live occupant (`AF02`) to `FF`.
- Strong structural meaning: canonical tail entry exists, but it is withheld from the live/materialized tail map.
- Exact gameplay-facing noun remains cautious.

---

## Strengthened interpretive labels from earlier passes

### C1:9E78        ct_g2_cmd10_materialize_tail_slots_from_canonical_map     [strengthened]
- Earlier passes already proved the scan gates:
  - `AF0D[x] != FF`
  - `AF02[x] == FF`
  - `AF15.bit7` clear
- Pass 56 upgrades the noun:
  - this command materializes live tail slots from the canonical tail map,
    rather than merely scanning a vague runtime-slot pool.

---

## Supporting structural notes

### Unified occupant-map geometry
The following contiguous geometry is now strong enough to carry forward:

```text
AEFF..AF09  = 11-slot live occupant map
AF0A..AF14  = 11-slot canonical/remembered occupant map

slots 0..2  = visible head partition
slots 3..10 = runtime tail partition
```

This is no longer a convenient coincidence.
The visible head builder and the tail builder now prove both halves.

---

## Cautions still in force
Do **not** over-freeze the following yet:

1. `29C4..` source family as specifically enemy-only slots
   - the 8-record / 12-byte structure is strong
   - the final gameplay-facing noun still wants more caller proof
2. `AF15.bit7` as a fully flavored term like “reserve” or “hidden”
   - structural meaning is strong
   - flavor meaning still wants more proof
3. the exact higher-level reason `C1:C1DD` type `3` requires `AF15.bit7` for entries `>= 3`

---

## Suggested next seam
The best next continuation point after pass 56 is:

1. the caller/consumer logic that distinguishes tail slots with readiness:
   - `0`
   - `1`
   - `>1`
2. the higher-level caller chain that explains why some canonical tail entries are withheld from the live map (`AF15.bit7` set)
3. stronger proof for the exact gameplay-facing identity of the 8 source records rooted at `29C4`
