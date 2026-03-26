# Chrono Trigger (USA) — Labels Added / Strengthened in Pass 34

This file contains labels newly added or materially strengthened in pass 34.

Status tags:
- **[strong]** = safe to carry forward unless contradicted by later control-flow proof
- **[provisional]** = useful working label, but still open to rename/refinement
- **[alias]** = intentional alias/stub label for a table entry landing in shared code or wrapper logic

## Group-2 labels upgraded in this pass

```text
C1:99BE  ct_c1_g2_op01_seed_single_from_5e15_finalize        [strong]
         Seeds a one-entry list from $5E15[$AEC8], sets B1FC bit 1,
         captures two inline params into AEE4/AEE5, optionally derives
         B18C for operand-1==1, calls unique long helper FD:AB01,
         then finalizes through AC89/ACCE and returns with B3B8 = 0.

C1:9A39  ct_c1_g2_op02_wrapper_jsr_9a3d                      [strong]
         Table-entry wrapper only: JSR $9A3D ; RTS.

C1:9A3D  ct_c1_g2_op02_seed_from_b16e_validate_commit        [strong]
         Seeds a one-entry list from $B16E[$AEC8], clears B1FC bit 1,
         optionally resolves up to two inline selector bytes through AC14,
         validates through C1DD, then commits through AD09/AD35/FDAAD2/
         AC89/ACCE and returns with B3B8 = 0.
```

## Helper labels strengthened in this pass

```text
FD:AB01  ct_fd_op01_unique_long_helper                        [provisional]
         Unique long helper reached by group-2 opcode 0x01 after the
         one-entry seed + AEE4/AEE5/B18C setup. Do not over-name yet.

C1:9B3B  ct_c1_g2_validation_fail_set_af24_2                 [strong]
         Shared local failure site used by the opcode-0x02 validation path:
         sets AF24 = 2 and then returns through the normal B3B8 = 0 tail.
```

## State labels newly worth carrying forward

```text
7E:AEE5  ct_c1_op01_param2_or_submode                         [provisional]
7E:B18C  ct_c1_primary_seed_or_mode_value                     [provisional]
```

## State notes strengthened in this pass

```text
7E:B1FC bit 1                                                 [provisional]
         Deliberately split by the early group-2 pair:
         set by opcode 0x01, cleared by opcode 0x02.
         Treat as an opcode-mode control bit until helper/caller proof
         gives a safer gameplay-facing name.
```

## Notes for next pass
- Tighten `C1:C1DD`, `C1:AC89`, and `C1:ACCE` before renaming their state outputs aggressively.
- Do not assign gameplay meanings to `$5E15[$AEC8]` or `$B16E[$AEC8]` yet; only their use as distinct one-entry seed sources is proven.
- Do not claim `FD:AB01` is ordinary 65816 code without stronger entry/exit proof.
