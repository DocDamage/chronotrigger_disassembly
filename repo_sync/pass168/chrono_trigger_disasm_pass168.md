# Chrono Trigger Disassembly — Pass 168

## Scope
Pass 168 closes the immediate post-marker gap after the low-bank `C3` executable cluster by freezing the bytes after exact `CODE END C3` as inline data, not latent executable code.

## Closed span
- `C3:10D0..C3:12FF` — post-`CODE END C3` inline data/padding block with long zero-filled spacer and compact nonzero control/bitmask tail ending just before the next higher callable candidate lane at `C3:1300`

## Why this closure is real
- pass 167 already proved `C3:10C0..C3:10CF` is the inline ASCII marker `CODE END C3`
- the exact bytes immediately after that marker do **not** present a credible continuation of the low-bank executable flow
- seam-candidate scoring for `C3:10D0..C3:12FF` only surfaced weak starts dominated by zero bytes
- the first materially interesting higher callable candidate in this neighborhood is `C3:1300`, not anything inside the exact `10D0..12FF` gap

## Findings

### `C3:10D0..C3:12DF`
This subrange is dominated by a long zero-filled spacer / padding field. It does not behave like active owner code, and there are no strong exact call anchors into the middle of it.

### `C3:12E0..C3:12FF`
The last exact 32 bytes before `C3:1300` are not all zero, but they still read as compact inline data rather than executable logic. Strongest safe reading: one short post-padding control/bitmask tail that belongs to the surrounding bank-local data lane, not one callable owner.

## Strong label added
- `C3:10D0..C3:12FF` — `ct_c3_post_code_end_inline_data_padding_block_with_zero_spacer_and_short_control_tail_before_next_callable_lane`

## Important correction/state change
- do **not** keep hunting for executable low-bank `C3` code immediately after `CODE END C3`
- the correct next move is to jump to the next higher unresolved callable lane instead of treating the post-marker padding/data as a seam

## Resulting next target
- **`C3:1300..C3:1816`** — next higher unresolved bank-`C3` callable lane to inspect before the already externally anchored exact entry at `C3:1817`

## Completion snapshot after pass 168
- overall completion estimate: **~71.4%**
- exact label rows: **1343**
- exact strong labels: **1025**
