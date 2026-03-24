# Chrono Trigger Disassembly — Pass 111

## Scope of this pass
Pass 110 closed the `ED15` vs `FD:E022` transfer-method split, but it left the honest upstream questions open:

1. who actually fills `7E:05B0..05EB` and the helper tables that `FD:E022` consumes?
2. what exact job does the optional `C0:F05E` prelude do before `ED15` runs?

This pass closes both of those with byte-level evidence.

---

## 1. `FD:FFFA` is the exact veneer into the descriptor/helper-table builder

Raw bytes:

```text
FD:FFF8  9C E3 4C 98 DE 4C 22 E0
```

So the exact local bodies are now:

- `FD:FFF7 -> JMP $E39C`
- `FD:FFFA -> JMP $DE98`
- `FD:FFFD -> JMP $E022`

That makes `FD:FFFA` the exact bank-local veneer for the still-unlabeled builder body at `FD:DE98`.

### Confirmed external caller
Raw startup-chain bytes:

```text
C0:00F4  20 2B 09 20 53 1B 20 60 09 20 CF 6D 20 84 70 20
C0:0104  7E 7F 20 3B A3 20 DD 09 20 14 0A 20 D4 56 22 FA
C0:0114  FF FD 22 F4 FF FD 60
```

So the early low-bank init chain really does include:

```asm
C0:0112  JSL FD:FFFA
C0:0116  JSL FD:FFF4
```

That earlier pass-2/3 startup observation now has an exact target on the FD side.

---

## 2. `FD:DE98..E01D` is the script-driven builder for the `05B0..05EB` workspace and the `7F:0400/0410` helper tables

Entry bytes:

```text
FD:DE98  08 0B 8B A9 00 48 AB C2 10 E2 20 A2 00 05 DA 2B
FD:DEA8  A9 00 EB AE FE 01 BF 01 00 F6 29 3F 0A AA C2 20
FD:DEB8  BF 90 F2 FD AA A9 00 04 8D 81 21 A9 0C 00 85 18
FD:DEC8  E2 20 A9 7F 8D 83 21 A0 00 00 BF 10 F3 FD E8 C9
FD:DED8  80 D0 08 A9 80 99 B3 05 4C 0B E0 99 B0 05 BF 10
FD:DEE8  F3 FD 99 B2 05 E8 BF 10 F3 FD 99 B3 05 E8 A9 7F
FD:DEF8  99 B4 05 B9 B0 05 C9 02 D0 63 A9 00 99 B0 05 99
FD:DF08  B1 05 A9 04 85 10 C2 20 BF 10 F3 FD 29 FF 00 0A
FD:DF18  0A EB 8D 7F 21 EB 8D 7F
```

### Exact setup
The body at `DE98`:

- saves `P`, `D`, and `B`
- forces `DB = 0`
- sets `D = 0x0500`
- reads `X = 7E:01FE`
- reads selector byte `F6:0001,X`
- masks it with `0x3F`, doubles it, and uses that as an index into the exact pointer table at `FD:F290`
- loads the resulting stream pointer from `FD:F290,X`
- seeds WRAM-port address `$7F:0400` through `$2181/$2183`
- seeds local counter `7E:0518 = 0x000C`
- starts with `Y = 0`

### What it builds
For each iteration, the routine consumes bytes from the compact stream rooted at `FD:F310 + pointer_from_F290`.

It writes one 5-byte descriptor lane per iteration into:

- `7E:05B0 + Y`
- `7E:05B1 + Y`
- `7E:05B2 + Y`
- `7E:05B3 + Y`
- `7E:05B4 + Y`

and then advances `Y += 5`.

It repeats until `0518` counts down from `0x0C` to zero, so the builder fills **12 exact 5-byte lanes** in one pass:

- `05B0..05B4`
- `05B5..05B9`
- `05BA..05BE`
- `05BF..05C3`
- `05C4..05C8`
- `05C9..05CD`
- `05CE..05D2`
- `05D3..05D7`
- `05D8..05DC`
- `05DD..05E1`
- `05E2..05E6`
- `05E7..05EB`

That is the exact upstream producer family that pass 110 left open.

### Exact per-record behavior
The first compact byte controls the path:

#### Case A — `0x80`
When the first fetched compact byte is `0x80`, the routine does:

```asm
LDA #$80
STA $05B3,Y
JMP $E00B
```

So `05B3` is the exact negative/sentinel kill byte used by the later `FD:E022` consumer to skip that lane.

#### Case B — general 3-byte lane
Otherwise the builder first stores:

- compact byte 0 -> `05B0,Y`
- compact byte 1 -> `05B2,Y`
- compact byte 2 -> `05B3,Y`
- constant `0x7F` -> `05B4,Y`

Then it branches by the new `05B0,Y` value.

#### Case C — type `0x02`
For `05B0,Y == 0x02`, it zeroes `05B0,Y` and `05B1,Y`, then writes:

- 16 expanded bytes into the WRAM helper area starting at `7F:0400`
- 16 raw bytes into the WRAM helper area starting at `7F:0410`

using the WRAM port at `$2180..$2183`.

#### Case D — type `0x04`
For `05B0,Y == 0x04`, it also zeroes `05B0,Y` and `05B1,Y`, but uses the longer 8-step variant:

- 32 expanded bytes into `7F:0400`
- 16 raw bytes into `7F:0410`

and then advances the compact-stream cursor by the extra consumed bytes.

#### Case E — other non-`0x80`, non-`0x02`, non-`0x04` type
The fallback special path also zeroes `05B0,Y` and `05B1,Y`, then emits:

- 16 bytes into `7F:0400`
- 16 bytes into `7F:0410`

with a different packing grammar from the `0x02` and `0x04` cases.

### Strongest safe reading
`FD:DE98..E01D` is:

> **the exact script-driven startup/refresh builder that materializes all twelve `7E:05B0..05EB` 5-byte descriptor lanes plus the `7F:0400/0410` helper tables later consumed by `FD:E022`.**

This closes the biggest open upstream producer seam left by pass 110.

---

## 3. `C0:F05E` is an exact four-band VRAM prelude keyed by local state byte `63`

Entry bytes:

```text
C0:F05E  0B C2 20 A9 00 21 5B E2 20 A9 80 85 15 AD 63 01
C0:F06E  F0 1B 3A F0 7D 3A F0 5A 3A F0 32 20 59 F1 20 42
C0:F07E  F1 20 2B F1 20 10 F1 2B A9 80 85 63 60 20 42 F1
```

Pass 110 had already proved the caller condition:

```text
C0:ED08  22 FD FF FD C2 30 AB 2B 7A FA 68 40 60 C2 20 A9
C0:ED18  00 01 5B E2 20 A5 63 30 03 20 5E F0 A5 5F 89 10
```

So `ED15` only calls `F05E` when `63` is **not negative**.

### Exact setup
`F05E`:

- saves `D`
- sets `D = 0x2100`
- sets `$2115 = 0x80`
- reads local state byte `7E:0163`

Then it dispatches on the exact values:

- `63 == 0`
- `63 == 1`
- `63 == 2`
- `63 == 3`
- default / other nonnegative values

### Fixed helper leaves
The four helper leaves are exact fixed VRAM writers through `$2116/$2118`:

- `F159` writes fixed pairs at VRAM addresses `1C02` and `1C22`
- `F142` writes fixed pairs at `1C42` and `1C62`
- `F12B` writes fixed pairs at `1C82` and `1CA2`
- `F110` writes fixed pairs at `1CC2` and `1CE2`

The byte patterns are exact:

```text
F110 -> 1CC2/1CE2 with data pairs from 29C2/29D2
F12B -> 1C82/1CA2 with data pairs from 2982/2992
F142 -> 1C42/1C62 with data pairs from 2942/2952
F159 -> 1C02/1C22 with data pairs from 2902/2912
```

### Exact selector behavior
The dispatcher chooses which three default helper leaves to run, then overwrites the remaining band with the special `28FC..28FF` values.

#### `63 == 0`
Runs:
- `F142`
- `F12B`
- `F110`

Then writes special values into:
- `1C02` with `28FC/28FD`
- `1C22` with `28FE/28FF`

#### `63 == 1`
Runs:
- `F159`
- `F12B`
- `F110`

Then writes special values into:
- `1C42` with `28FC/28FD`
- `1C62` with `28FE/28FF`

#### `63 == 2`
Runs:
- `F159`
- `F142`
- `F110`

Then writes special values into:
- `1C82` with `28FC/28FD`
- `1CA2` with `28FE/28FF`

#### `63 == 3`
Runs:
- `F159`
- `F142`
- `F12B`

Then writes special values into:
- `1CC2` with `28FC/28FD`
- `1CE2` with `28FE/28FF`

#### default / other nonnegative values
Runs all four default helper leaves:

- `F159`
- `F142`
- `F12B`
- `F110`

Then restores `63 = 0x80` and returns.

### Strongest safe reading
`C0:F05E` is:

> **an exact four-band immediate-VRAM prelude that restores three fixed bands from the `29xx` default tile pairs and overwrites the selected fourth band with the special `28FC..28FF` tile pair set, keyed by local selector byte `63`.**

Important detail:
- the `0..3` cases do **not** force `63 = 0x80` here
- only the default/non-`0..3` path does that

So `63` is not just a yes/no gate. It is an exact **4-way band selector plus default-restore state byte** for this prelude.

---

## 4. What is now closed vs what is still live

### Closed by pass 111
- `FD:FFFA` exact veneer target
- `FD:DE98..E01D` as the exact upstream builder for:
  - `7E:05B0..05EB`
  - `7F:0400..041F` and related helper-table materialization
- `C0:F05E..F16F` as the exact `63`-driven four-band immediate-VRAM prelude
- `63` is now stronger locally:
  - not just “optional prelude enable”
  - exact 4-way prelude selector + default-restore state

### Still live after pass 111
1. who writes `63` to the exact `0..3` selector values before `ED15` runs?
2. is `FD:DE98` only the startup/descriptor-load path behind `C0:0112`, or are there additional higher-level refresh owners outside the already-known veneer?
3. what broader subsystem noun safely covers the `1C02..1CE2` / `29xx` / `28FC..28FF` VRAM band family?

---

## 5. Conservative completion estimate after pass 111

New estimate: **69.0%**

Why it went up:
- pass 110 left the descriptor/helper-table producer seam open; pass 111 closes it
- `F05E` is no longer vague “optional prelude work”; it is an exact selector-driven VRAM prelude with frozen address/data grammars

Why it did not jump harder:
- the ownership/writer side of selector byte `63` is still open
- the broader subsystem noun behind the four fixed VRAM bands is still intentionally cautious
- this still improves structure and local semantics more than total-bank coverage

---

## 6. Best next seam
The honest next pass should trace the writers/owners of `63` and the broader owner chain of the `F05E` bands.

### Best immediate targets
- search writers of `7E:0163`
- search nearby owners of the `1C02/1C22/1C42/1C62/1C82/1CA2/1CC2/1CE2` VRAM band family
- determine whether the `28FC..28FF` vs `29xx` pair sets correspond to a known UI/map-overlay/subscreen tile family

Second-best fallback:
- widen the `FD:DE98` caller/owner chain beyond `C0:0112`
- freeze whether there are any non-startup refresh paths that rebuild `05B0..05EB`
