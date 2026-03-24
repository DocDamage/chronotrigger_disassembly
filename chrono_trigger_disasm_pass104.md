# Chrono Trigger Disassembly — Pass 104

## Scope
Pass 103 froze the local CD/CE owner helper family around `CD:0D62..0E22`, but the higher-level chooser contract that decides whether `CD:0D93` or `CD:0DB1` runs was still open.

This pass stayed on that exact seam and decoded the caller/chooser wrapper around:

- `CD:83DA..8449`
- `CD:044A..0452`
- `CD:0534..053A`

It also used the newly exposed `0501/0503 -> D1:F4C0` install to prove what the `$47` wait helper is actually waiting for.

## Starting point
- previous top-of-stack: **pass 103**
- live seam from the note: **`CD:83ED..840D`**

## Work performed
- decoded the exact instruction stream from PC `0x0D03DA..0x0D0449`
- separated the pre-launch wait at `83DA` from the chooser core at `83EE`
- decoded the tiny local helpers at `044A` and `0534`
- used the already-known `0500` NMI RAM trampoline contract plus the first instructions of `D1:F4C0` to prove the `$47` handshake instead of leaving `044A` as a generic spin helper
- tightened the local roles of `2A21`, `7F:01EC`, and the `0501/0503` trampoline target in this one caller chain

## 1. `CD:0534..053A` is an exact status probe for `CA1F`
The exact body is:

```text
CD:0534  LDA $CA1F
CD:0537  BEQ done
CD:0539  LDA #$01
done:
CD:053A  RTL
```

So this helper returns:
- `A = 0` when `CA1F == 0`
- `A = 1` when `CA1F != 0`

That matters because the front of the chooser wrapper uses it as the exact loop predicate.

## 2. `CD:83DA..83ED` is the pre-launch wait and stage-marker prelude
The exact body is:

```text
wait_ca1f_clear:
CD:83DA  JSR $3E7D
CD:83DD  JSL $CD0534
CD:83E1  BNE wait_ca1f_clear
CD:83E3  LDA #$0E
CD:83E5  STA $CA25
CD:83E8  INC $CA24
CD:83EB  JSR $3E7D
```

That means this block:
1. services the local idle/wait helper `3E7D`
2. loops until `CA1F == 0`
3. then stages exact marker/state values `CA25 = 0x0E` and `CA24++`
4. then burns one more exact `3E7D` service tick before the chooser runs

So the strongest safe reading is:

> exact pre-launch wait wrapper that refuses to proceed while `CA1F` is nonzero, then advances the local `CA25/CA24` stage markers before entering the helper chooser.

## 3. `CD:83EE..840C` is the exact chooser for the pass-103 blocking helper siblings
The exact body is:

```text
CD:83EE  LDA $2A21
CD:83F1  AND #$11
CD:83F3  BEQ skip_helpers
CD:83F5  AND #$01
CD:83F7  BEQ bit0_clear_path

; bit0 set path
CD:83F9  LDA.l $7F01EC
CD:83FD  BNE skip_helpers
CD:83FF  JSR $0DB1
CD:8402  BRA skip_helpers

; bit0 clear path
bit0_clear_path:
CD:8404  LDA.l $7F01EC
CD:8408  BEQ skip_helpers
CD:840A  JSR $0D93
```

This is the exact chooser matrix:

- if `(2A21 & 0x11) == 0`: call **neither** helper
- if `2A21.bit0 == 1` and `7F:01EC == 0`: call **`CD:0DB1`**
- if `2A21.bit0 == 1` and `7F:01EC != 0`: call neither helper
- if `2A21.bit0 == 0` but `2A21.bit4 == 1` and `7F:01EC != 0`: call **`CD:0D93`**
- if `2A21.bit0 == 0` and `7F:01EC == 0`: call neither helper

This settles the old seam question cleanly:
- `7F:01EC` is **not** choosing between `0D93` and `0DB1` by itself
- it only matters inside a tighter local contract gated first by `2A21 & 0x11`
- `2A21.bit0` selects which side of the split is even eligible
- `2A21.bit4` only matters by keeping the whole chooser live when bit 0 is clear

So the strongest safe reading is:

> exact local helper chooser that uses the combined `2A21.bit4/bit0` precondition mask and the zero/nonzero state of `7F:01EC` to decide whether to run the owner transition helper `0DB1`, the simpler selector-`0x87` helper `0D93`, or neither.

## 4. `CD:840D..8449` is the exact post-chooser launch wrapper
The exact body is:

```text
skip_helpers:
CD:840D  LDA #$08
CD:840F  STA $CA25
CD:8412  INC $CA24
CD:8415  JSR $3E7D
CD:8418  LDA #$D1
CD:841A  STA $0503
CD:841D  LDX #$F4C0
CD:8420  STX $0501
CD:8423  LDA $BB00
CD:8426  STA $45
CD:8428  JSR $044A
CD:842B  LDA $2A1F
CD:842E  AND #$40
CD:8430  BNE skip_2141_wait
wait_2141_clear:
CD:8432  LDA.l $002141
CD:8436  BNE wait_2141_clear
skip_2141_wait:
CD:8438  STZ $2A21
CD:843B  PHB
CD:843C  PHD
CD:843D  PHP
CD:843E  JSL $C0000B
CD:8442  PLP
CD:8443  PLD
CD:8444  PLB
CD:8445  TDC
CD:8446  JSR $044A
CD:8449  RTL
```

This is a much stronger result than the old vague “chooser neighborhood” wording:

- it stages another exact marker step: `CA25 = 0x08`, `CA24++`
- it installs exact RAM-trampoline target fields `0501/0503 = D1:F4C0`
- it copies `BB00 -> $45`
- it calls the wait helper at `044A`
- it conditionally waits for `$2141 == 0` unless `2A1F.bit6` is set
- it clears `2A21`
- it runs the already-frozen low-bank packet submit veneer at `C0:000B`
- it waits through `044A` again, then returns

So the strongest safe reading is:

> exact launch wrapper that, after the optional `0D93/0DB1` preconditioning helper, stages the next `CA25/CA24` phase, installs `D1:F4C0` as the active RAM-trampoline target, waits for one trampoline cycle, conditionally waits for `$2141` idleness, clears the local `2A21` control byte, runs `C0:000B`, waits for one more trampoline cycle, and returns.

## 5. `CD:044A..0452` is no longer a generic spin helper; it is an exact RAM-trampoline / NMI wait helper
The exact body is:

```text
CD:044A  LDA #$01
CD:044C  STA $47
wait:
CD:044E  LDA $47
CD:0450  BNE wait
CD:0452  RTS
```

By itself that only proves a latch wait.

But pass 104 can now pin the other side of the contract too:
- this wrapper installs `0501/0503 = D1:F4C0`
- pass 2 already proved `0500..0503` is the RAM NMI trampoline target slot
- the first live instructions at `D1:F4C0` include:

```text
D1:F4CC  A9 A1
D1:F4CF  STA.l $004200
D1:F4D3  STZ $47
D1:F4D5  JSL $CD09CE
D1:F4D9  JSL $C00005
D1:F4E0  LDA.l $000045
D1:F4E4  STA.l $002100
```

That is enough to settle the helper honestly:
- `044A` sets `$47 = 1` and waits
- the installed `D1:F4C0` trampoline target clears `$47`
- the same target also consumes `$45` and writes it to `$2100`

So the strongest safe reading is:

> exact wait-for-one-RAM-trampoline/NMI-cycle helper, with `$47` as the one-shot completion latch and `$45` as one byte forwarded into the installed `D1:F4C0` target.

## 6. What this pass changes about the key local bytes
### `7E:2A21`
Pass 91 and pass 90 already proved bit 0 matters as a side-sensitive selector in other subsystems.

Pass 104 adds a clean new local contract:
- `83EE` first gates on `2A21 & 0x11`
- bit 0 then selects which helper branch is even eligible
- `8438` clears `2A21` after the launch wrapper finishes

So `2A21` is now stronger locally as:

> transient local side/control mask byte whose bit 0 and bit 4 jointly gate this launch-time helper chooser.

I am still **not** claiming the final gameplay-facing noun of bit 4.

### `7F:01EC`
Pass 92 proved this byte selects a special-case path in the C0 packet-submit family when its exact value is `1`.

Pass 104 adds a second, independent clean usage:
- in this CD launch wrapper it is treated purely as a zero/nonzero selector
- zero permits `0DB1` on the bit-0-set side
- nonzero permits `0D93` on the bit-0-clear side

So the strongest safe reading now is:

> cross-subsystem special-case selector byte with both exact-value and zero/nonzero local consumers, not just a one-off C0 submit quirk.

## Main conclusions from pass 104
1. `CD:83EE..840C` is now an exact chooser, not a fuzzy caller neighborhood.
2. `2A21 & 0x11` matters because it is the exact precondition mask that decides whether this helper split is live at all.
3. `7F:01EC` does not choose between `0D93` and `0DB1` alone; it only selects within the tighter `2A21`-gated matrix.
4. `CD:044A` is now an exact wait-for-one-RAM-trampoline/NMI-cycle helper through `$47`, not generic delay noise.
5. `CD:840D..8449` is now exact enough to read as a real launch wrapper for the `0501/0503 -> D1:F4C0 -> C0:000B` chain.

## Honest caution
What this pass does **not** claim:

1. I have **not** frozen the final gameplay-facing noun of `CA1F`, `CA24`, or `CA25`.
2. I have **not** frozen the final gameplay-facing noun of `BB00` or the byte forwarded through `$45 -> $2100`.
3. I have **not** frozen the full higher-level role of `D1:F4C0`; I only used the exact front-edge proof that it clears `$47` and consumes `$45`.
4. I have **not** frozen the final gameplay-facing noun of `2A21.bit4`.

## Next best seam after pass 104
The cleanest next move is now:

1. stay on the exact wrapper we just froze
2. follow the installed RAM-trampoline target at **`D1:F4C0..`**
3. specifically freeze:
   - the exact front-edge role of `D1:F4C0`
   - why it clears `$47`
   - what `$45 -> $2100` means in this local launch chain
   - how that routine relates to the `C0:000B` submit path the wrapper immediately surrounds
