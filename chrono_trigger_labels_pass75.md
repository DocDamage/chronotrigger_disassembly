# Chrono Trigger Labels — Pass 75

## Purpose
This file records the label upgrades justified by pass 75.

Pass 75 cleaned up the fixed-`7F` follow-up seam left open by pass 74.

The biggest correction is direct:

- `C1:BFA4` is not unresolved
- it is an exact `LDA #$04 ; JSR $0003 ; RTS` wrapper

That sharpens the shared tail behind globals `91` and `99`:

- `895B` seeds the fixed follow-up context
- `AC57` runs the local service-`04` hook
- `AC85 -> EC7F` applies pending stat-delta channels

Pass 75 also promoted the nearby current-tail runner and two downstream queue/accumulator helpers.

---

## Strengthened helper labels

### C1:BFA4..C1:BFA9  ct_c1_invoke_local_service_04_wrapper   [strong]
- Exact bytes: `LDA #$04 ; JSR $0003 ; RTS`.
- This is no longer a fuzzy helper blob.
- Structural role: tiny wrapper into the local service/dispatcher family with service id `04`.

### C1:BF7F..C1:BFA0  ct_c1_copy_17_byte_followup_descriptor_profile_from_cc213f_by_b18c   [strong structural]
- Computes `0x11 * B18C`.
- Copies `0x11` bytes from `CC:213F + 0x11*B18C` into `AEE6..AEF6`.
- Strongest safe reading: load the current follow-up/descriptor profile record selected by `B18C`.

### C1:BFAA..C1:C029  ct_c1_initialize_current_tail_followup_context_load_current_descriptor_and_run_common_tail   [strong structural]
- Sets `B1FC.bit1` on entry and clears it on exit.
- Clears `AE93/AE94/AE95/AE96/AE99/AE9A/AE9B`, sets `AE97=AE98=0xFF`, seeds `AE90=0`, `AE91=B18B`, `AE92=1`.
- Seeds single-entry selection state through `AECC=AD8E`, `AECB=1`, and `AE94=AD09()`.
- If `AEFF[B18B] != 0xFF`, resolves `CC:2583[occupant] -> B18C`, loads the 17-byte descriptor/profile through `BF7F`, and checks `AF23`.
- On success runs `AC57`, optionally arms `B2C0` when `AECC>=3`, clears transient packet workspace through `FD:ACEE`, clears `B1FC.bit1`, and returns.

### C1:AC57..C1:AC5D  ct_c1_run_service_04_hook_then_apply_pending_stat_deltas   [strong correction]
- Exact body: `JSR BFA4 ; JSR AC85 ; RTS`.
- Because `BFA4` is now exact, this tail is no longer just a vague bridge.
- Strongest safe reading: run the service-`04` follow-up hook, then apply pending stat-delta channels.

---

## Strengthened downstream helper labels

### FD:ABA2..FD:AC6D  ct_fd_accumulate_slot_descriptor_vectors_and_optional_unique_token_queues   [provisional strengthened]
- Requires `AF12[slot].bit6` clear and `AF0A[slot] != 0xFF`.
- Uses `AF0A[slot]` as an index into a 7-byte descriptor family via `DP28=index ; DP2A=7 ; JSL C1:FDBF`.
- Accumulates record components from `CC:5E00/02/06 + 7*index` into `B28C`, `B2A5`, and `B2DB/B2DD`.
- Under extra gates, inserts unique 8-bit tokens into the first free entries of `B2A7..B2A9` and `B2AA..B2AC`, setting `B2AF.bit5` when it does so.
- Final gameplay-facing nouns for those accumulators and token queues remain open.

### FD:AC6E..FD:ACEE  ct_fd_consume_pending_slot_queue_and_attempt_admission_materialization   [provisional strengthened]
- Uses `B3B9` as a nonzero queue gate/cursor seed and mirrors it into `B315`.
- Pulls pending slot ids from `B3AC[B315]` until exhausted or rejected.
- Validates pending slots against lane/block flags in the `5E4A/5E4B/5E78/5E7A/5E7B` neighborhood.
- On accepted slots may set `AFAB[slot]=1`, seeds `B18B=slot` and `AD8E=selected value`, then dispatches the downstream materialization/helper path through `C1:FDC7`.
- Clears `B3B9` when the queue walk finishes.
- Exact queue owner noun still wants one more pass.

---

## Strengthened RAM/state labels

### 7E:AEE6..7E:AEF6  ct_c1_current_followup_descriptor_profile_record_17bytes   [strong structural]
- Destination of the `BF7F` copy.
- Holds the currently loaded 17-byte follow-up/descriptor profile selected by `B18C`.

### 7E:B1FC  ct_c1_followup_context_flags   [provisional strengthened]
- `BFAA` sets bit `0x02` on entry and clears it before return.
- Strongest safe reading so far: this byte carries active/in-progress follow-up-context flags rather than being generic scratch.

---

## Honest caution
Even after this pass:

- `AEE6..AEF6` is structurally a descriptor/profile record, but the per-byte field nouns are still open.
- `FD:ABA2`'s accumulators and token queues are real, but not yet frozen to final gameplay-facing names.
- `FD:AC6E` is clearly a queue-consumer / admission runner, but the owning subsystem noun still needs one more tightening pass.
