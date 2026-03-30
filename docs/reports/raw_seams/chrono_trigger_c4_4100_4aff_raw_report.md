# Chrono Trigger raw seam report — C4:4100..C4:4AFF

Method note:
- ROM-first seam triage run in the current workspace.
- The local environment had the ROM and the public branch scripts, but not the full checked-out manifest set, so caller ownership stayed conservative.
- Result standard used here: **no promotions unless caller quality, start-byte quality, and local structure still all agree**.

Start seam page: **C4:4100**
Pages swept: **10**
Page-family counts: `{"branch_fed_control_pocket": 2, "candidate_code_lane": 6, "mixed_command_data": 2}`
Review-posture counts: `{"bad_start_or_dead_lane_reject": 4, "local_control_only": 2, "manual_owner_boundary_review": 2, "mixed_lane_continue": 2}`

## Page summary

### C4:4100..C4:41FF
- family: **candidate_code_lane**
- posture: **manual_owner_boundary_review**
- raw targets: `4` | strong/weak effective hits: `4` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `2` | local clusters: `2` | tiny veneers: `0` | wrapper bad targets: `0`
- best targets:
  - `C4:4101` | best=`weak` | hits=`1` | callers=`C4:EBB2`
  - `C4:41BE` | best=`weak` | hits=`1` | callers=`C4:BC34`
  - `C4:41E0` | best=`weak` | hits=`1` | callers=`C4:806E`
  - `C4:41F8` | best=`weak` | hits=`1` | callers=`C4:D683`
- top backtracks:
  - `C4:41BE` -> `C4:41AE` | score=`4` | dist=`16` | start=`A3` clean_start
  - `C4:41E0` -> `C4:41E0` | score=`3` | dist=`0` | start=`A0` clean_start
  - `C4:41F8` -> `C4:41F5` | score=`2` | dist=`3` | start=`B8` clean_start
  - `C4:4101` -> `C4:4101` | score=`1` | dist=`0` | start=`28` clean_start
- local clusters:
  - `C4:419F..C4:41B9` | cluster_score=`8` | children=`2` | width=`27`
  - `C4:4159..C4:4161` | cluster_score=`2` | children=`1` | width=`9`

### C4:4200..C4:42FF
- family: **candidate_code_lane**
- posture: **manual_owner_boundary_review**
- raw targets: `5` | strong/weak effective hits: `2` | hard-bad starts: `0` | soft-bad starts: `1`
- owner-backtrack candidates (score>=3): `1` | local clusters: `1` | tiny veneers: `4` | wrapper bad targets: `0`
- best targets:
  - `C4:4290` | best=`weak` | hits=`1` | callers=`C4:9DCE`
  - `C4:42DE` | best=`weak` | hits=`1` | callers=`C4:03C5`
  - `C4:4200` | best=`suspect` | hits=`1` | callers=`C4:0DD6`
  - `C4:42A0` | best=`suspect` | hits=`1` | callers=`C4:82CE`
  - `C4:42DF` | best=`suspect` | hits=`1` | callers=`C4:0DE4`
- top backtracks:
  - `C4:42A0` -> `C4:42A0` | score=`3` | dist=`0` | start=`73` clean_start
  - `C4:42DE` -> `C4:42D5` | score=`2` | dist=`9` | start=`3F` clean_start
  - `C4:42DF` -> `C4:42D5` | score=`2` | dist=`10` | start=`3F` clean_start
  - `C4:4290` -> `C4:4290` | score=`1` | dist=`0` | start=`63` clean_start
  - `C4:4200` -> `C4:4200` | score=`-2` | dist=`0` | start=`30` soft_bad_start
- local clusters:
  - `C4:42C2..C4:42D2` | cluster_score=`2` | children=`2` | width=`17`

### C4:4300..C4:43FF
- family: **mixed_command_data**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `2` | strong/weak effective hits: `1` | hard-bad starts: `1` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `3` | tiny veneers: `9` | wrapper bad targets: `0`
- best targets:
  - `C4:43BE` | best=`weak` | hits=`1` | callers=`C4:9E19`
  - `C4:43F0` | best=`suspect` | hits=`1` | callers=`C4:93DF`
- top backtracks:
  - `C4:43BE` -> `C4:43B0` | score=`3` | dist=`14` | start=`8A` clean_start
  - `C4:43F0` -> `C4:43F0` | score=`-6` | dist=`0` | start=`00` hard_bad_start
- local clusters:
  - `C4:4390..C4:4397` | cluster_score=`4` | children=`1` | width=`8`
  - `C4:4345..C4:434A` | cluster_score=`3` | children=`1` | width=`6`
  - `C4:43D8..C4:43DE` | cluster_score=`2` | children=`1` | width=`7`

### C4:4400..C4:44FF
- family: **candidate_code_lane**
- posture: **mixed_lane_continue**
- raw targets: `1` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `2` | tiny veneers: `3` | wrapper bad targets: `0`
- best targets:
  - `C4:44E3` | best=`weak` | hits=`1` | callers=`C4:1A86`
- top backtracks:
  - `C4:44E3` -> `C4:44DF` | score=`2` | dist=`4` | start=`5F` clean_start
- local clusters:
  - `C4:441C..C4:4423` | cluster_score=`4` | children=`1` | width=`8`
  - `C4:44AF..C4:44B5` | cluster_score=`3` | children=`1` | width=`7`

### C4:4500..C4:45FF
- family: **mixed_command_data**
- posture: **mixed_lane_continue**
- raw targets: `1` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `3` | tiny veneers: `4` | wrapper bad targets: `0`
- best targets:
  - `C4:45BA` | best=`weak` | hits=`1` | callers=`C4:F1EA`
- top backtracks:
  - `C4:45BA` -> `C4:45B9` | score=`2` | dist=`1` | start=`4A` clean_start
- local clusters:
  - `C4:45F2..C4:45F8` | cluster_score=`3` | children=`1` | width=`7`
  - `C4:4514..C4:451E` | cluster_score=`2` | children=`1` | width=`11`
  - `C4:4527..C4:452C` | cluster_score=`2` | children=`1` | width=`6`

### C4:4600..C4:46FF
- family: **candidate_code_lane**
- posture: **local_control_only**
- raw targets: `1` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `4` | tiny veneers: `3` | wrapper bad targets: `0`
- best targets:
  - `C4:46C0` | best=`suspect` | hits=`1` | callers=`C4:2848`
- top backtracks:
  - `C4:46C0` -> `C4:46B0` | score=`3` | dist=`16` | start=`08` clean_start
- local clusters:
  - `C4:4604..C4:4612` | cluster_score=`4` | children=`2` | width=`15`
  - `C4:465A..C4:4665` | cluster_score=`3` | children=`1` | width=`12`
  - `C4:46AE..C4:46B5` | cluster_score=`3` | children=`1` | width=`8`
  - `C4:46DB..C4:46E4` | cluster_score=`3` | children=`1` | width=`10`

### C4:4700..C4:47FF
- family: **candidate_code_lane**
- posture: **local_control_only**
- raw targets: `0` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `2` | tiny veneers: `4` | wrapper bad targets: `0`
- local clusters:
  - `C4:4727..C4:4731` | cluster_score=`3` | children=`1` | width=`11`
  - `C4:47B8..C4:47C1` | cluster_score=`2` | children=`1` | width=`10`

### C4:4800..C4:48FF
- family: **branch_fed_control_pocket**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `3` | strong/weak effective hits: `0` | hard-bad starts: `1` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `2` | local clusters: `1` | tiny veneers: `3` | wrapper bad targets: `0`
- best targets:
  - `C4:48A5` | best=`suspect` | hits=`1` | callers=`C4:AA10`
  - `C4:48DF` | best=`suspect` | hits=`1` | callers=`C4:AA1B`
  - `C4:48F0` | best=`invalid` | hits=`1` | callers=`C5:54E0`
- top backtracks:
  - `C4:48A5` -> `C4:4898` | score=`3` | dist=`13` | start=`08` clean_start
  - `C4:48DF` -> `C4:48CE` | score=`3` | dist=`17` | start=`08` clean_start
  - `C4:48F0` -> `C4:48F0` | score=`-6` | dist=`0` | start=`00` hard_bad_start
- local clusters:
  - `C4:487B..C4:4882` | cluster_score=`3` | children=`1` | width=`8`

### C4:4900..C4:49FF
- family: **candidate_code_lane**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `3` | strong/weak effective hits: `0` | hard-bad starts: `1` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `2` | tiny veneers: `2` | wrapper bad targets: `0`
- best targets:
  - `C4:49A0` | best=`suspect` | hits=`1` | callers=`C4:8221`
  - `C4:49C0` | best=`suspect` | hits=`1` | callers=`C4:EAB4`
  - `C4:49F0` | best=`suspect` | hits=`1` | callers=`C4:D41D`
- top backtracks:
  - `C4:49A0` -> `C4:4990` | score=`3` | dist=`16` | start=`20` clean_start
  - `C4:49C0` -> `C4:49B8` | score=`2` | dist=`8` | start=`1C` clean_start
  - `C4:49F0` -> `C4:49F0` | score=`-6` | dist=`0` | start=`00` hard_bad_start
- local clusters:
  - `C4:4906..C4:4912` | cluster_score=`3` | children=`1` | width=`13`
  - `C4:4987..C4:498C` | cluster_score=`2` | children=`1` | width=`6`

### C4:4A00..C4:4AFF
- family: **branch_fed_control_pocket**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `2` | strong/weak effective hits: `1` | hard-bad starts: `1` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `2` | tiny veneers: `4` | wrapper bad targets: `0`
- best targets:
  - `C4:4A63` | best=`weak` | hits=`1` | callers=`C4:9AF2`
  - `C4:4AF2` | best=`suspect` | hits=`1` | callers=`C4:E8A1`
- top backtracks:
  - `C4:4A63` -> `C4:4A53` | score=`4` | dist=`16` | start=`5A` clean_start
  - `C4:4AF2` -> `C4:4AF2` | score=`-6` | dist=`0` | start=`00` hard_bad_start
- local clusters:
  - `C4:4A3B..C4:4A41` | cluster_score=`4` | children=`1` | width=`7`
  - `C4:4AA8..C4:4AB4` | cluster_score=`4` | children=`1` | width=`13`
