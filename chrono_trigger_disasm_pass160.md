# Chrono Trigger Disassembly — Pass 160

## Purpose

Pass 160 closes the exact unresolved bank-end tail at exact `C2:FFEE..C2:FFFF` honestly instead of pretending the final exact 18 bytes of bank `C2` form one more clean callable owner.

## What this pass actually proved

### 1) `C2:FFEE..C2:FFFF` is not a new balanced owner head

Exact bytes:

`95 A9 05 00 54 7E D1 A2 BA 95 A0 3A 96 A9 05 00 54 7E`

This exact sequence does **not** begin with one exact sane routine prologue. Instead, it begins mid-body and matches the exact interior import/mirror pattern already proven earlier in the exact helper family around exact `C2:FF87..C2:FFA3`:

- exact `A9 05 00 ; 54 7E D1 ; A2 BA 95 ; A0 3A 96 ; A9 05 00 ; 54 7E ...`
- exact `FFEE..FFFF` preserves that exact structural pattern, but the bank ends before one exact full second `MVN` pair / increment / exit can complete

Strongest safe reading:
- exact bank-end truncated duplicate / overlap tail from the exact `FF87` import-and-mirror helper family
- **not** one exact independently callable owner
- **not** one exact balanced helper entry
- **not** one exact new dispatch head

### 2) no exact direct caller proof appeared for `FFEE`

Toolkit inspection still shows no exact cached hot xrefs landing inside exact `C2:FFEE..C2:FFFF`.

That matters because the exact bytes already fail the normal structural-owner smell test, so without one exact caller anchor there is no good reason to promote exact `FFEE` into code ownership.

### 3) the exact safest closure is a bank-end overlap/tail label

The correct thing here is to freeze the exact span as one exact caution/overlap tail and stop pretending there is one more clean owner at the bank cliff.

## Exact closure frozen this pass

- `C2:FFEE..C2:FFFF`
  - exact bank-end truncated duplicate tail of the exact `FF87` import/mirror helper family
  - begins in the middle of the exact established `95BA/963A` import-and-copy byte pattern
  - runs out of bank before one exact balanced standalone stream can complete

## What this pass deliberately did **not** claim

- it did **not** claim exact `FFEE` is one exact callable routine head
- it did **not** merge exact `FFEE..FFFF` into exact `FFE0..FFED` as though the whole bank end were one exact clean owner
- it did **not** invent one exact synthetic top-level function just because the bank had bytes remaining

## Best next move after bank `C2` is now honestly closed

The next high-value target is the raw low-bank startup cluster immediately after the bank boundary:

- raw/project address convention: exact `C3:0000..C3:0013`
- known facts already visible in the exact bytes:
  - exact `C3:0000` begins `BRA $0014`, skipping the exact startup table/veneer area
  - exact `C3:0002..C3:0004` is already proven as the exact unpack veneer (`JMP $0557`)
  - exact `C3:0014` begins one exact real hardware/setup-looking owner (`SEI ; PHA ; LDA #$5C ; STA $0500 ; ...`)

## Honest tooling caveat

The shipped inspector/dump scripts in toolkit v6.7 still assume exact HiROM CPU ROM addresses with exact offsets `>= $8000`, so raw low-bank project addresses like exact `C3:0000` need one exact manual/raw-byte inspection lane for now.

That is one exact toolkit limitation, not proof that the exact low-bank startup bytes are unimportant.
