# Chrono Trigger raw seam report — C4:3700..C4:40FF

Method note:
- ROM-first seam triage run in the current workspace.
- The local environment had the ROM and the public branch scripts, but not the full checked-out manifest set, so caller ownership stayed conservative.
- Result standard used here: **no promotions unless caller quality, start-byte quality, and local structure still all agree**.

Start seam page: **C4:3700**
Pages swept: **10**
Page-family counts: `{"branch_fed_control_pocket": 1, "candidate_code_lane": 8, "mixed_command_data": 1}`
Review-posture counts: `{"bad_start_or_dead_lane_reject": 6, "local_control_only": 2, "manual_owner_boundary_review": 2}`

## Page summary

### C4:3700..C4:37FF
- family: **candidate_code_lane**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `3` | strong/weak effective hits: `1` | hard-bad starts: `1` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `4` | tiny veneers: `4` | wrapper bad targets: `0`
- best targets:
  - `C4:37EF` | best=`weak` | hits=`1` | callers=`C4:E5B3`
  - `C4:37D6` | best=`suspect` | hits=`1` | callers=`C4:C45D`
  - `C4:370A` | best=`invalid` | hits=`1` | callers=`C4:60DB`
- top backtracks:
  - `C4:37D6` -> `C4:37D4` | score=`4` | dist=`2` | start=`04` clean_start
  - `C4:37EF` -> `C4:37E8` | score=`2` | dist=`7` | start=`EB` clean_start
  - `C4:370A` -> `C4:370A` | score=`-6` | dist=`0` | start=`02` hard_bad_start
- local clusters:
  - `C4:37B9..C4:37C7` | cluster_score=`3` | children=`1` | width=`15`
  - `C4:37A8..C4:37B5` | cluster_score=`3` | children=`2` | width=`14`
  - `C4:37DC..C4:37E3` | cluster_score=`2` | children=`1` | width=`8`
  - `C4:3725..C4:372A` | cluster_score=`2` | children=`1` | width=`6`

### C4:3800..C4:38FF
- family: **candidate_code_lane**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `4` | strong/weak effective hits: `1` | hard-bad starts: `1` | soft-bad starts: `1`
- owner-backtrack candidates (score>=3): `2` | local clusters: `3` | tiny veneers: `6` | wrapper bad targets: `0`
- best targets:
  - `C4:38D7` | best=`weak` | hits=`1` | callers=`C4:7D8D`
  - `C4:3802` | best=`suspect` | hits=`1` | callers=`C4:574B`
  - `C4:38E1` | best=`suspect` | hits=`1` | callers=`C4:15CA`
  - `C4:38FF` | best=`suspect` | hits=`1` | callers=`C4:FB10`
- top backtracks:
  - `C4:38D7` -> `C4:38D3` | score=`3` | dist=`4` | start=`9A` clean_start
  - `C4:38E1` -> `C4:38D6` | score=`3` | dist=`11` | start=`A0` clean_start
  - `C4:38FF` -> `C4:38F3` | score=`2` | dist=`12` | start=`8F` clean_start
  - `C4:3802` -> `C4:3802` | score=`-1` | dist=`0` | start=`09` soft_bad_start
- local clusters:
  - `C4:3897..C4:38A1` | cluster_score=`3` | children=`1` | width=`11`
  - `C4:3858..C4:3861` | cluster_score=`2` | children=`1` | width=`10`
  - `C4:3876..C4:387E` | cluster_score=`2` | children=`1` | width=`9`

### C4:3900..C4:39FF
- family: **candidate_code_lane**
- posture: **local_control_only**
- raw targets: `0` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `4` | tiny veneers: `8` | wrapper bad targets: `0`
- local clusters:
  - `C4:39B9..C4:39C0` | cluster_score=`5` | children=`1` | width=`8`
  - `C4:3920..C4:392B` | cluster_score=`3` | children=`1` | width=`12`
  - `C4:3980..C4:3987` | cluster_score=`2` | children=`1` | width=`8`
  - `C4:39C8..C4:39CF` | cluster_score=`2` | children=`1` | width=`8`

### C4:3A00..C4:3AFF
- family: **candidate_code_lane**
- posture: **local_control_only**
- raw targets: `0` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `4` | tiny veneers: `6` | wrapper bad targets: `0`
- local clusters:
  - `C4:3AC7..C4:3ACD` | cluster_score=`4` | children=`1` | width=`7`
  - `C4:3A87..C4:3A8E` | cluster_score=`3` | children=`1` | width=`8`
  - `C4:3A0D..C4:3A13` | cluster_score=`2` | children=`1` | width=`7`
  - `C4:3A31..C4:3A39` | cluster_score=`2` | children=`1` | width=`9`

### C4:3B00..C4:3BFF
- family: **candidate_code_lane**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `4` | strong/weak effective hits: `1` | hard-bad starts: `1` | soft-bad starts: `1`
- owner-backtrack candidates (score>=3): `2` | local clusters: `4` | tiny veneers: `13` | wrapper bad targets: `0`
- best targets:
  - `C4:3B7E` | best=`weak` | hits=`1` | callers=`C4:8F43`
  - `C4:3B6D` | best=`suspect` | hits=`1` | callers=`C4:9147`
  - `C4:3B9C` | best=`suspect` | hits=`1` | callers=`C4:624B`
  - `C4:3BFB` | best=`suspect` | hits=`1` | callers=`C4:BB2D`
- top backtracks:
  - `C4:3B7E` -> `C4:3B6F` | score=`3` | dist=`15` | start=`A2` clean_start
  - `C4:3B9C` -> `C4:3B8E` | score=`3` | dist=`14` | start=`4F` clean_start
  - `C4:3B6D` -> `C4:3B6D` | score=`-1` | dist=`0` | start=`30` soft_bad_start
  - `C4:3BFB` -> `C4:3BFB` | score=`-6` | dist=`0` | start=`00` hard_bad_start
- local clusters:
  - `C4:3B2E..C4:3B3F` | cluster_score=`4` | children=`2` | width=`18`
  - `C4:3B60..C4:3B67` | cluster_score=`3` | children=`1` | width=`8`
  - `C4:3B42..C4:3B4A` | cluster_score=`2` | children=`1` | width=`9`
  - `C4:3BD8..C4:3BDD` | cluster_score=`2` | children=`1` | width=`6`

### C4:3C00..C4:3CFF
- family: **candidate_code_lane**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `2` | strong/weak effective hits: `0` | hard-bad starts: `2` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `2` | local clusters: `5` | tiny veneers: `6` | wrapper bad targets: `0`
- best targets:
  - `C4:3C5C` | best=`suspect` | hits=`1` | callers=`C4:5244`
  - `C4:3C88` | best=`invalid` | hits=`2` | callers=`C5:4DAB, C5:4DAC`
- top backtracks:
  - `C4:3C5C` -> `C4:3C4C` | score=`4` | dist=`16` | start=`63` clean_start
  - `C4:3C88` -> `C4:3C7A` | score=`3` | dist=`14` | start=`20` clean_start
- local clusters:
  - `C4:3C02..C4:3C20` | cluster_score=`5` | children=`3` | width=`31`
  - `C4:3C8A..C4:3C94` | cluster_score=`4` | children=`1` | width=`11`
  - `C4:3CA4..C4:3CAD` | cluster_score=`3` | children=`2` | width=`10`
  - `C4:3CD6..C4:3CDF` | cluster_score=`3` | children=`1` | width=`10`

### C4:3D00..C4:3DFF
- family: **branch_fed_control_pocket**
- posture: **manual_owner_boundary_review**
- raw targets: `4` | strong/weak effective hits: `3` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `3` | tiny veneers: `9` | wrapper bad targets: `0`
- best targets:
  - `C4:3DDF` | best=`weak` | hits=`2` | callers=`C4:2455, C4:6B39`
  - `C4:3D00` | best=`weak` | hits=`1` | callers=`CA:8592`
  - `C4:3D08` | best=`suspect` | hits=`1` | callers=`C4:0B39`
  - `C4:3D24` | best=`suspect` | hits=`1` | callers=`C4:0AC3`
- top backtracks:
  - `C4:3D24` -> `C4:3D20` | score=`4` | dist=`4` | start=`E3` clean_start
  - `C4:3D08` -> `C4:3D05` | score=`2` | dist=`3` | start=`0E` clean_start
  - `C4:3D00` -> `C4:3D00` | score=`1` | dist=`0` | start=`E0` clean_start
  - `C4:3DDF` -> `C4:3DDB` | score=`0` | dist=`4` | start=`7B` clean_start
- local clusters:
  - `C4:3D5F..C4:3D65` | cluster_score=`5` | children=`1` | width=`7`
  - `C4:3DA4..C4:3DAA` | cluster_score=`4` | children=`1` | width=`7`
  - `C4:3D4D..C4:3D59` | cluster_score=`2` | children=`1` | width=`13`

### C4:3E00..C4:3EFF
- family: **mixed_command_data**
- posture: **manual_owner_boundary_review**
- raw targets: `2` | strong/weak effective hits: `2` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `2` | local clusters: `2` | tiny veneers: `1` | wrapper bad targets: `0`
- best targets:
  - `C4:3E00` | best=`weak` | hits=`1` | callers=`C4:55D5`
  - `C4:3EC7` | best=`weak` | hits=`1` | callers=`C4:8680`
- top backtracks:
  - `C4:3EC7` -> `C4:3EC2` | score=`4` | dist=`5` | start=`20` clean_start
  - `C4:3E00` -> `C4:3E00` | score=`3` | dist=`0` | start=`20` clean_start
- local clusters:
  - `C4:3E37..C4:3E40` | cluster_score=`3` | children=`1` | width=`10`
  - `C4:3E9F..C4:3EA7` | cluster_score=`2` | children=`1` | width=`9`

### C4:3F00..C4:3FFF
- family: **candidate_code_lane**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `7` | strong/weak effective hits: `2` | hard-bad starts: `1` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `4` | local clusters: `4` | tiny veneers: `4` | wrapper bad targets: `0`
- best targets:
  - `C4:3F00` | best=`weak` | hits=`2` | callers=`C4:A1B7, C4:1B5B`
  - `C4:3F80` | best=`weak` | hits=`1` | callers=`C4:4620`
  - `C4:3F40` | best=`suspect` | hits=`1` | callers=`C4:595E`
  - `C4:3F5D` | best=`suspect` | hits=`1` | callers=`C4:9988`
  - `C4:3FDB` | best=`suspect` | hits=`1` | callers=`C4:60AA`
- top backtracks:
  - `C4:3F00` -> `C4:3F00` | score=`4` | dist=`0` | start=`08` clean_start
  - `C4:3F40` -> `C4:3F30` | score=`4` | dist=`16` | start=`22` clean_start
  - `C4:3F5D` -> `C4:3F4D` | score=`4` | dist=`16` | start=`08` clean_start
  - `C4:3FDB` -> `C4:3FCB` | score=`4` | dist=`16` | start=`91` clean_start
  - `C4:3F80` -> `C4:3F70` | score=`4` | dist=`16` | start=`89` clean_start
- local clusters:
  - `C4:3F0A..C4:3F13` | cluster_score=`4` | children=`1` | width=`10`
  - `C4:3F60..C4:3F69` | cluster_score=`3` | children=`1` | width=`10`
  - `C4:3F25..C4:3F2D` | cluster_score=`2` | children=`1` | width=`9`
  - `C4:3FA8..C4:3FAD` | cluster_score=`2` | children=`1` | width=`6`

### C4:4000..C4:40FF
- family: **candidate_code_lane**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `23` | strong/weak effective hits: `10` | hard-bad starts: `12` | soft-bad starts: `1`
- owner-backtrack candidates (score>=3): `4` | local clusters: `0` | tiny veneers: `11` | wrapper bad targets: `0`
- best targets:
  - `C4:4010` | best=`weak` | hits=`2` | callers=`C4:01EE, C4:C06C`
  - `C4:401F` | best=`weak` | hits=`2` | callers=`C4:51F1, C4:4421`
  - `C4:4098` | best=`weak` | hits=`2` | callers=`C4:3A88, C4:8037`
  - `C4:4020` | best=`weak` | hits=`1` | callers=`C4:8090`
  - `C4:403F` | best=`weak` | hits=`1` | callers=`C4:1752`
- top backtracks:
  - `C4:401F` -> `C4:4015` | score=`4` | dist=`10` | start=`98` clean_start
  - `C4:4020` -> `C4:4015` | score=`4` | dist=`11` | start=`98` clean_start
  - `C4:4088` -> `C4:4078` | score=`4` | dist=`16` | start=`C8` clean_start
  - `C4:40C0` -> `C4:40C0` | score=`3` | dist=`0` | start=`A0` clean_start
  - `C4:4001` -> `C4:4000` | score=`2` | dist=`1` | start=`D0` clean_start
