# Chrono Trigger Labels — Pass 161

## Purpose

Pass 161 freezes the exact low-bank `C3` bank-head veneer/data cluster, the exact launcher at `C3:0014`, and the exact temporary exact `C3` RAM-trampoline bodies that launcher installs into exact `0500` and `0504`.

## What this pass closes

### C3:0014..C3:0076  ct_c3_bank_head_launcher_installing_c3_ram_trampolines_staging_fe0003_pointer_unpack_to_7e3000_and_jumping_there   [strong structural]
- Begins exact `SEI ; PHA`.
- Writes exact opcode byte `5C` to exact RAM trampoline heads `0500` and `0504`.
- Writes exact words `0548 -> 0501` and `0529 -> 0505`.
- Writes exact bank byte `C3 -> 0503` and `0507`.
- That installs exact RAM trampolines:
  - exact `0500 = JML C3:0548`
  - exact `0504 = JML C3:0529`
- Stores the restored exact accumulator byte into exact `0384` and branches on exact bit `0x80`.
- When exact bit `0x80` is set, writes exact `0F -> $2100`, clears exact `$420C`, writes exact `A1 -> $4200`, writes exact `00D3 -> $4209`, reads exact `$4211`, and runs exact `CLI`.
- Then runs exact `REP #$20`, loads one exact source word from exact long address `FE:0003 -> 0300`, writes exact destination word `3000 -> 0303`, writes exact source bank byte `C3 -> 0302`, clears exact destination bank byte `0305`, calls exact unpack core `C3:0557`, and exits through exact `JML 7E:3000`.
- Strongest safe reading: exact bank-head launcher that installs temporary exact `C3` RAM interrupt trampolines, conditionally seeds exact display/NMI timing state, stages one exact packed-stream load using the exact source-word slot at `FE:0003`, unpacks to exact WRAM destination `7E:3000`, and transfers control there.

### C3:0529..C3:0547  ct_c3_temporary_ram_trampoline_body_waiting_on_4212_transition_then_forcing_2100_blank_and_rti   [strong structural]
- Begins exact `SEP #$20 ; PHA`.
- Reads exact `$4211`.
- Polls exact `$4212` across one exact bit-`0x40` transition.
- Writes exact `80 -> $2100`.
- Restores exact `A`.
- Exits exact `RTI`.
- Strongest safe reading: exact temporary exact `C3` RAM-trampoline body that waits on exact `$4212` timing state, forces exact display blank through exact `$2100 = 0x80`, and returns via exact `RTI`.

### C3:0548..C3:0556  ct_c3_temporary_ram_trampoline_body_acknowledging_4210_restoring_2100_to_0f_and_rti   [strong structural]
- Begins exact `SEP #$20 ; PHA`.
- Reads exact `$4210`.
- Writes exact `0F -> $2100`.
- Restores exact `A`.
- Exits exact `RTI`.
- Strongest safe reading: exact temporary exact `C3` RAM-trampoline body that acknowledges exact NMI latch `$4210`, restores exact display state through exact `$2100 = 0x0F`, and returns via exact `RTI`.

## Alias / wrapper / caution labels

### C3:0000..C3:0001  ct_c3_bank_head_branch_over_low_bank_veneer_cluster_into_0014_launcher   [alias]
- Exact body is `BRA $0014`.
- Strongest safe reading: exact bank-head branch-over wrapper that skips the exact low-bank entry-veneer/data cluster and lands in the exact launcher body at `0014`.

### C3:0005..C3:0007  ct_c3_embedded_raw_long_pointer_constant_c2dece_between_low_bank_entry_veneers   [caution structural]
- Exact bytes are `CE DE C2`.
- Exact little-endian long value is exact address `C2:DECE`.
- This exact span sits between the exact unpack veneer at `0002` and the exact direct-entry veneer at `0008`.
- Strongest safe reading: exact embedded raw long pointer constant, not one exact balanced code owner.

### C3:0008..C3:000A  ct_c3_low_bank_direct_entry_veneer_jumping_to_0077_worker   [alias]
- Exact body is `JMP $0077`.
- Manual exact ROM-wide byte search finds exact `JSL C3:0008` at **11** call sites.
- Strongest safe reading: exact direct entry veneer landing in the exact downstream worker body at `C3:0077`.

### C3:000B..C3:000D  ct_c3_second_embedded_raw_long_pointer_constant_c2dece_between_low_bank_entry_veneers   [caution structural]
- Exact bytes are `CE DE C2`.
- Exact little-endian long value is exact address `C2:DECE`.
- This exact span sits between the exact direct-entry veneers at `0008` and `000E`.
- Strongest safe reading: exact second embedded raw long pointer constant, not one exact balanced code owner.

### C3:000E..C3:0010  ct_c3_low_bank_direct_entry_veneer_jumping_to_01e4_worker   [alias]
- Exact body is `JMP $01E4`.
- Manual exact ROM-wide byte search finds exact `JSL C3:000E` at **3** call sites.
- Strongest safe reading: exact direct entry veneer landing in the exact downstream worker body at `C3:01E4`.

### C3:0011..C3:0013  ct_c3_low_bank_direct_entry_veneer_jumping_to_0efa_worker   [alias]
- Exact body is `JMP $0EFA`.
- Manual exact ROM-wide byte search finds exact `JSL C3:0011` at **1** call site.
- Strongest safe reading: exact direct entry veneer landing in the exact downstream worker body at `C3:0EFA`.

## Honest remaining gap

- the exact low-bank `C3` bank head is now materially tighter and the exact launcher at `0014` is closed
- the next exact worker body to split is the exact first real downstream worker reached by the exact live entry veneer at `C3:0008`, namely exact `C3:0077..C3:01E3`
- exact `C3:01E4` is already anchored by one exact direct entry veneer and should be treated as the next follow-on owner after that
- toolkit v6.7 still has one exact low-bank inspection blind spot for exact `C3:xxxx` raw/project addresses, so the next pass should keep using one exact manual/raw-byte lane there unless the toolkit is upgraded
