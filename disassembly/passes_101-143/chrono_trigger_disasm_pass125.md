# Chrono Trigger Disassembly Progress — Pass 125

This pass closed the exact helper chain under `C2:C2FF` and froze the next continuation-family bridge after the pass-124 `FF`-record loader.

## 1. `C2:C43A..C2:C5C6` is now an exact local helper family

`C43A..C455` is the mirror/clear front end:
- exact same-bank copy of `0D86..0D8F -> 0F09..0F12`
- exact tail clears of `0F0D/0F0E/0F0F`

`C456..C494` is the exact three-lane low-3-bit table emitter:
- exact lane 1: base `2EA6`, state byte `0D8B`
- exact lane 2: base `2F66`, state byte `0D90`
- exact lane 3: base `2FE6`, state byte `0D8C`
- final exact lane computes `61 += 2 * (state & 07)` and runs exact helper `ECAC` with exact targets `0C08` and `0001`

`C495..C4F8` is the exact `0417`-indexed window seed / byte loader:
- exact words from `FF:D562 + 2*0417` go to `3446`, `3448`, `3486`, and `3488`
- exact byte `0417` is mirrored into `0DCE`
- exact local tables `C4F9` and `C505` build exact byte `0DCF` from exact source block `0D86..`
- exact tail is fixed helper `F943`

`C511..C548` is the exact `0D8B.high3bit` importer:
- exact source base is `FF:9E10 + 0x0280 * index`
- exact copy length is `0x0281`
- exact destination is `7E:8800`
- fixed tail is `962E`, exact selector/data packet `C548 -> 8385`, then exact helper `ED08`

`C555..C579` and `C57A..C5C6` finish the family:
- exact staging seed `FCA9 -> 2993`
- exact live `0408` override when exact word `0D87 != 0`
- exact six-entry descriptor writer using exact destination table `C5A7`
- exact byte-to-word conversion helper `C5B3` backed by exact table `FF:D554`

That means the whole local chain under `C2:C2FF` is now concrete:
- mirror exact state bytes
- emit exact low-3-bit table lanes
- seed exact indexed words/bytes from `0417`
- optionally import one exact `FF:9E10` block selected by exact `0D8B.high3bit`
- stage exact descriptor bytes at `2993`
- convert six exact staged bytes into six exact descriptor triplets

## 2. `C2:B48E..C2:B6D2` breaks cleanly into bridge, table lane, controller, preset selector, builder, and exporter

`B48E..B4DA` is the exact `0D1D`-gated bridge owner:
- clear exact `0D1D.bits7/6` path returns
- exact bit-6 path reruns `EAC2`, mirrors `0F48 -> 54`, decrements exact byte `68`, reruns `F566`, seeds exact compare byte `71 = 0419 + 041A`, reruns exact helper `8820`, writes exact byte `0D75 = 02`, increments exact byte `D0`, runs exact helper `8255` with `A = 40`, shifts exact `5DE0 -> 5DE2`, and exits through exact selectors `FBE3` and `FC3E`
- exact bit-7 path jumps into `B4DB`

`B4DB..B518` is the exact `0DBC`-gated downstream lane:
- exact zero path exits through `EACC`
- exact live path selects exact byte `19E1 = B519[19C0]`, reruns exact helper chain `822B -> 8F55`, seeds exact compare byte `71 = 0F4D`, reruns exact helper `8820`, subtracts exact byte `0F4F` from exact slot byte `0007,X`, and exits through exact jump `BE79`

`B520..B567` is the exact `0418` controller:
- exact `5A.low2` and exact `5A.bit0` steer a clamped signed update of exact byte `0418` in range `0..2`
- then the routine runs exact helper `EA53`, clears exact byte `0D18`, conditionally enters exact helper `B568`, seeds exact byte `0419 = 54 - 0B`, and runs exact helper chain `BC6F -> B6AE -> BE16`

`B568..B5C7` chooses one of two exact preset packs for `B5C8`:
- clear exact `5A.bit2` path decrements exact byte `041A` and seeds preset pack `22=0003 / 26=2605 / 61=364A / 0D22=FFFC / 24=211F`
- set exact `5A.bit2` path rejects when exact byte `041A + 03 >= 85`, then increments exact byte `041A` and seeds preset pack `22=0004 / 26=2005 / 61=3ACA / 0D22=0004 / 24=20EF`

`B5C8..B6A5` is the big exact builder:
- exact front end: `0D13 = 6B`, exact compare byte `71 = 0419 + 041A`, exact helper `8820`, exact helper `BAFC`, clear exact word `9890`, exact compare gate `BA2F`, exact `EF05` seed, exact helper `EF05`, exact selector `FBEA`
- exact 12-step mirrored strip loop updates exact words `0D30/0DAB/24`, mirrors exact carry through exact word `0D95`, and writes exact word `24` into exact lanes `5D44,X` and `5DC4,X`
- exact refill/finalizer flips exact word `5B` with `EOR #0600`, reruns exact helper `EF05`, writes exact word `21FF` to `5D44`, shifts exact bytes `5D44 -> 5D46`, copies exact bytes `5D44 -> 5DC4`, dispatches exact selector `FC3E`, clears exact word `0D30`, reruns exact helper `F566`, then emits an exact three-row tail through exact helper `BAFC`
- exact tail writes `0D13 = 6D`, decrements exact byte `0D18`, and returns

`B6AE..B6D2` is the exact bottom exporter:
- exact base word `61 = 2EE4`
- exact helper `ECAC` with exact target `150A`
- add exact stride `8 * 0418`
- exact helper `ECAC` with exact target `1102`

## 3. WRAM meanings tightened again

Pass 125 materially strengthens these readings:
- `0D8B` = exact primary three-lane cyclic state byte whose low bits feed `C456` and whose high bits select the imported `FF:9E10` block in `C511`
- `0D8C` = exact tertiary three-lane cyclic state byte shared by `C456` and the earlier `C12C/C164` worker family
- `0D90` = exact secondary three-lane cyclic state byte for the `C456` emitter family
- `0F48` = exact continuation selector byte mirrored into `54` by both the bridge and loader families
- `0F49` = exact nonzero gate byte for the earlier `B365` negative-lane continuation path
- `0F4C` = exact `FF`-record continuation index byte for the `B3E6` loader family
- `0F4D` = exact continuation compare-seed byte built from `0419 + 041A` and reused by the new `B4DB` lane
- `0F4F` = exact threshold/result byte consumed by `B4DB` immediately before exact jump `BE79`

## 4. Real next seam now

The next honest targets are:
- `C2:B6D3..C2:BA2E`
- `C2:C5C7..C2:C67A`
- broader gameplay-facing nouns for `0D8B/0D8C/0D90`
- the still-bigger top-level family noun for `C2:A886..AA30`
