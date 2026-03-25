# Chrono Trigger Disassembly Pass 43

## Scope of this pass
This pass continued directly from pass 42’s live seam:

- decode local **service 2** in the exact contexts reached from `FD:A8FE`
- explain the small controller state around `A6D9 / A6DD / A6DE / A6DF / 95D6..95DA`
- tighten the structural meaning of the carried-state bytes reset by the lane-clear helpers
- re-check the producer side of `9F38[x]` without forcing a fake positive-writer label

This pass did **not** try to rename the entire gameplay subsystem.
It stayed on the exact roster/refresh controller that pass 42 exposed.

---

## Method
1. Re-traced local services `1` and `2` from the bank-`C1` dispatcher table established in pass 37.
2. Decoded the contiguous helper band at:
   - `C1:1B19`
   - `C1:1B69`
   - `C1:1BAA`
   - `C1:1C3A`
3. Cross-checked the same state bytes in the caller/consumer band around:
   - `C1:11D6..123A`
   - `C1:16DA..1768`
   - `C1:B3F4..B441`
   - `FD:A8CE..A95F`
4. Re-scanned direct accesses to `7E:9F38` to separate proven behavior from still-unresolved behavior.

---

## Starting point from pass 42
Pass 42 had already proven:

- `FD:A8FE` clears an occupied lane and then invokes local **service 2** through `C1:B961`
- the downstream lane clear/reset helpers touch exactly this carried-state bundle:
  - `B158`
  - `AFAB`
  - `99DD`
  - `9F22`
  - `B188`
  - `B03A`
- `93F3` resolves as a packed pair of lane IDs `0/1/2` plus `F = none`
- the positive producer path for `9F38[x]` was still unresolved

The exact ambiguity was therefore no longer in the lane clear helpers themselves.
It was in the **controller they call back into**.

---

## 1. Local service 2 at `C1:1BAA` is a **lane-roster removal / refresh service** over exactly three lanes
This pass materially tightens what service 2 is doing.

The key structural fact is that the code paths centered on `1B69` and `1BAA` only scan and compact a **3-entry lane controller**, not an arbitrary object-slot list.
The proof is direct:

- pending queue scans use `CPX #$0003`
- active-roster rescans also use `CPX #$0003`
- the same lane IDs `0/1/2` already proved in pass 42 line up with the surrounding helper calls

### Core service-2 behavior
At `C1:1BAA`, the input lane is taken from direct-page state (`A1`) and handled in two distinct cases.

#### Case A: the lane is **not** active in `A6D9[x]`
Service 2 scans the pending queue at `95D6..95D8`.
If the lane is found there, the queue is compacted left and the pending count at `95DA` is decremented.
If the lane is not found, service 2 simply returns.

So service 2 is **not** “active-only.”
It can also delete a lane that is still waiting in the small pending-admission queue.

#### Case B: the lane **is** active in `A6D9[x]`
Service 2:

- clears the lane’s active marker in `A6D9[x]`
- decrements `A6DE`
- writes `FEh` into `A6DF`
- then branches depending on whether the removed lane matches `A6DD`

If the removed lane is **not** the current active lane, the service ends after the delete path and workspace reset tail.

If the removed lane **is** the current active lane, the service performs a much bigger reseat/reset sequence:

- conditionally folds back `A86B -> 95DB` and clears `A86B` / `A09A`
- clears:
  - `9609`
  - `960E`
  - `9614`
  - `95DB`
  - `99E0`
- clears the removed lane’s `A6D9[x]` marker
- rescans the 3-lane active roster for the next live lane and writes it into:
  - `A6DD`
  - `95D5`
- falls through to `1C3A`

That makes the safest strong reading:

> `C1:1BAA` = **remove a lane from the pending/active roster and reseat the current lane plus outer selection state when needed**

This is substantially stronger than the pass-42 wording of “refresh service 2.”

---

## 2. `C1:1C3A` is the common **workspace reset tail** used by service 2
The tail reached from service 2 is simple but important:

```text
C1:1C3A  TDC
C1:1C3B  TAX
loop:
C1:1C3C  LDA $D1:5800,X
C1:1C40  STA $0B40,X
C1:1C43  INX
C1:1C44  CPX #$0180
C1:1C47  BNE loop
C1:1C49  RTS
```

So service 2 does not just delete a lane and stop.
It always ends through a **copy/reset of a 0x180-byte workspace image** from `D1:5800` into WRAM rooted at `0B40`.

Safest reading:

> `C1:1C3A` = **service-2 workspace template restore**

The exact human-facing meaning of the `0B40` workspace is still open, but its role as a reset image is now direct ROM proof.

---

## 3. The companion routines at `1B19` and `1B69` complete the same 3-lane roster controller
Service 2 makes a lot more sense once the two adjacent local routines are read with it.

### `C1:1B19` = enqueue lane + set record active bit
This routine:

- checks `A6D9[current_lane]`
- if the lane is not already active, it:
  - maps the lane through `CC:FAF0`
  - sets bit 7 in the record status byte at `93EE + record_offset`
  - appends the lane to `95D6 + pending_count`
  - seeds per-lane local state at `95DC[current_lane]`
  - increments `95DA`

So this is not a random helper.
It is the **admission/enqueue side** of the same 3-lane controller.

### `C1:1B69` = promote head of pending queue into active roster
This routine:

- reads the head of the pending queue at `95D6`
- if a pending lane exists:
  - clears `9F38[lane]`
  - copies two small per-lane bytes into `95DF[lane]` and `95EB[lane]`
  - writes the lane into `A6D9[lane]`
  - compacts `95D6..95D8`
  - decrements `95DA`
  - increments `A6DE`
  - if `A6DD < 0`, seeds `A6DD` with this new active lane

That gives a clean three-part controller picture:

- `1B19` = admit/enqueue a lane
- `1B69` = promote the queue head into the active roster
- `1BAA` = remove a lane from pending/active state and reseat the current lane if necessary

This is the strongest new structural result of the pass.

---

## 4. The small state block around `A6D9 / A6DD / A6DE / 95D6..95DA` is now materially tighter
The surrounding controller code no longer supports vague wording here.

### Strong readings
- `A6D9[0..2]` is a **per-lane active-roster membership marker**
  - `FF` means absent/inactive
  - nonnegative means the lane is active in the local 3-lane roster
- `A6DE` is the **active-lane count**
- `A6DD` is the **current active lane** used by the outer controller
- `95D6..95D8` is a **3-entry pending-admission queue of lane IDs**
- `95DA` is the **pending-admission count**

### Useful but still provisional
- `A6DF` is a **roster-change / invalidation sentinel** forced to `FEh` in both promotion/removal paths
  - structurally real
  - exact downstream meaning still needs more proof

This aligns cleanly with the pass-40/41/42 lane-controller work instead of fighting it.

---

## 5. The carried-state bundle reset by `FD:A8CE / A8FE` is now stronger as a **per-lane carried-state group**, not generic scratch
Pass 42 already showed that lane clear/reset touches:

- `B158`
- `AFAB`
- `99DD`
- `9F22`
- `B188`
- `B03A`

This pass tightens the grouping.

### What is now strong
The reset path is lane-indexed and runs immediately beside the canonical-record clear.
That means these bytes are **not** unrelated globals.
They are a compact **per-lane carried-state bundle** tied to the same lane IDs `0/1/2`.

### Best structural reading so far
- `B158[lane]` is the **primary carried scalar** for that lane
- `AFAB[lane]` is a **shadow / mirrored copy** of that scalar
- `99DD[lane]` and `9F22[lane]` are **export mirrors** updated from the same source in the clear/update families
- `B188[lane]` is an **occupied / refresh-required latch**
  - this is the byte that gates whether `FD:A8FE` escalates into local service 2
- `B03A[lane]` is a **secondary per-lane change/dirty latch**
  - still provisional as a final name, but clearly not unrelated scratch

So the strongest safe upgrade is:

> this 6-byte family is a **lane-carried state block** maintained alongside the canonical-record lane system

That is enough to keep future passes from treating these bytes as anonymous glue.

---

## 6. `9F38[x]` remains only partially solved: the negative proof got stronger, but the positive writer still is **not** pinned
This pass re-checked the direct accesses to `9F38`.

What is directly proved:

- `C1:16F7` ORs `9F38[current_lane]` into emitted record aux state at `93EF + record_offset`
- `C1:1B6D` clears `9F38[lane]` when a pending lane is promoted into the active roster

What is **not** yet proved:

- a trustworthy positive writer in the currently traced bank-`C1` / bank-`FD` controller band

So the safest wording is still:

> `9F38[x]` contributes lane-side aux bits into emitted record state, but its positive producer path remains unresolved

This pass therefore does **not** promote `9F38` beyond a provisional structural label.

---

## Net result of pass 43
Pass 42 had already decoded the downstream canonical-record lane reconciler.
This pass closes the loop on the **upstream local roster controller** that those helpers call back into.

The controller picture is now materially cleaner:

- a 3-lane pending-admission queue at `95D6..95D8`
- a 3-lane active roster tracked through `A6D9`
- a current active-lane cursor at `A6DD`
- service 1 to admit/enqueue lanes
- `1B69` to promote a queued lane into active state
- service 2 to remove a lane and reseat/reset the controller when necessary
- a lane-carried state bundle (`B158 / AFAB / 99DD / 9F22 / B188 / B03A`) maintained beside that roster

The abstraction gap moved again.
The next clean seam is now:

1. the exact downstream meaning of the `0B40` workspace restored by `1C3A`
2. the remaining outer-controller consumers of `A6DD / A6DE / A6DF`
3. and a stronger search for the positive writer(s) of `9F38[x]`

