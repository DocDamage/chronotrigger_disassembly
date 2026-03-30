# Chrono Trigger raw seam report — C4:4B00..C4:54FF

Method note:
- ROM-first seam triage run in the current workspace.
- The local environment had the ROM and the public branch scripts, but not the full checked-out manifest set, so caller ownership stayed conservative.
- Result standard used here: **no promotions unless caller quality, start-byte quality, and local structure still all agree**.

Start seam page: **C4:4B00**
Pages swept: **10**
Page-family counts: `{"candidate_code_lane": 6, "mixed_command_data": 2, "branch_fed_control_pocket": 2}`
Review-posture counts: `{"local_control_only": 3, "mixed_lane_continue": 2, "manual_owner_boundary_review": 3, "bad_start_or_dead_lane_reject": 2}`

## Page summary

### C4:4B00..C4:4BFF
- family: **candidate_code_lane**
- posture: **local_control_only**
- raw targets: `0` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `1` | tiny veneers: `5` | wrapper bad targets: `0`
- local clusters:
  - `C4:4B18..C4:4B21` | cluster_score=`3` | children=`1` | width=`10`

### C4:4C00..C4:4CFF
- family: **candidate_code_lane**
- posture: **local_control_only**
- raw targets: `0` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `3` | tiny veneers: `1` | wrapper bad targets: `0`
- local clusters:
  - `C4:4C55..C4:4C5D` | cluster_score=`4` | children=`1` | width=`9`
  - `C4:4C94..C4:4C9E` | cluster_score=`4` | children=`1` | width=`11`
  - `C4:4CE4..C4:4CED` | cluster_score=`3` | children=`1` | width=`10`

### C4:4D00..C4:4DFF
- family: **mixed_command_data**
- posture: **mixed_lane_continue**
- raw targets: `2` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `2` | tiny veneers: `1` | wrapper bad targets: `0`
- best targets:
  - `C4:4D0D` | best=`weak` | hits=`1` | callers=`F1:3D6C`
  - `C4:4D50` | best=`suspect` | hits=`1` | callers=`C4:8BF2`
- top backtracks:
  - `C4:4D0D` -> `C4:4D0D` | score=`1` | dist=`0` | start=`11` clean_start
  - `C4:4D50` -> `C4:4D50` | score=`1` | dist=`0` | start=`E0` clean_start
- local clusters:
  - `C4:4D98..C4:4DA0` | cluster_score=`4` | children=`1` | width=`9`
  - `C4:4DC8..C4:4DD0` | cluster_score=`2` | children=`1` | width=`9`

### C4:4E00..C4:4EFF
- family: **candidate_code_lane**
- posture: **manual_owner_boundary_review**
- raw targets: `2` | strong/weak effective hits: `2` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `1` | tiny veneers: `7` | wrapper bad targets: `0`
- best targets:
  - `C4:4ED0` | best=`weak` | hits=`2` | callers=`C4:CC6F, C4:9FA6`
  - `C4:4E00` | best=`weak` | hits=`1` | callers=`C4:7AD5`
- top backtracks:
  - `C4:4ED0` -> `C4:4ECD` | score=`4` | dist=`3` | start=`FB` clean_start
  - `C4:4E00` -> `C4:4E00` | score=`1` | dist=`0` | start=`90` clean_start
- local clusters:
  - `C4:4ECC..C4:4ED6` | cluster_score=`5` | children=`4` | width=`11`

### C4:4F00..C4:4FFF
- family: **branch_fed_control_pocket**
- posture: **manual_owner_boundary_review**
- raw targets: `1` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `3` | tiny veneers: `1` | wrapper bad targets: `0`
- best targets:
  - `C4:4FB7` | best=`weak` | hits=`1` | callers=`C4:F6AE`
- top backtracks:
  - `C4:4FB7` -> `C4:4FB5` | score=`4` | dist=`2` | start=`28` clean_start
- local clusters:
  - `C4:4FBD..C4:4FCA` | cluster_score=`6` | children=`2` | width=`14`
  - `C4:4F0E..C4:4F12` | cluster_score=`4` | children=`1` | width=`5`
  - `C4:4FD3..C4:4FDF` | cluster_score=`2` | children=`1` | width=`13`

### C4:5000..C4:50FF
- family: **candidate_code_lane**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `7` | strong/weak effective hits: `5` | hard-bad starts: `1` | soft-bad starts: `1`
- owner-backtrack candidates (score>=3): `2` | local clusters: `3` | tiny veneers: `3` | wrapper bad targets: `0`
- best targets:
  - `C4:5000` | best=`weak` | hits=`1` | callers=`C4:3D6D`
  - `C4:500C` | best=`weak` | hits=`1` | callers=`C4:58D5`
  - `C4:5064` | best=`weak` | hits=`1` | callers=`C4:3CD6`
  - `C4:5095` | best=`weak` | hits=`1` | callers=`C4:62B7`
  - `C4:50B0` | best=`weak` | hits=`1` | callers=`C4:CFD9`
- top backtracks:
  - `C4:5059` -> `C4:504E` | score=`6` | dist=`11` | start=`20` clean_start
  - `C4:5064` -> `C4:5060` | score=`4` | dist=`4` | start=`AE` clean_start
  - `C4:500C` -> `C4:5000` | score=`2` | dist=`12` | start=`07` clean_start
  - `C4:5095` -> `C4:5090` | score=`2` | dist=`5` | start=`1B` clean_start
  - `C4:50B0` -> `C4:50AB` | score=`2` | dist=`5` | start=`7F` clean_start
- local clusters:
  - `C4:5025..C4:5039` | cluster_score=`7` | children=`1` | width=`21`
  - `C4:50E1..C4:50F4` | cluster_score=`5` | children=`3` | width=`20`
  - `C4:50C6..C4:50CE` | cluster_score=`4` | children=`1` | width=`9`

### C4:5100..C4:51FF
- family: **mixed_command_data**
- posture: **manual_owner_boundary_review**
- raw targets: `4` | strong/weak effective hits: `2` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `1` | tiny veneers: `1` | wrapper bad targets: `0`
- best targets:
  - `C4:5100` | best=`weak` | hits=`1` | callers=`C4:9BF0`
  - `C4:5161` | best=`weak` | hits=`1` | callers=`C4:8FD6`
  - `C4:5120` | best=`suspect` | hits=`1` | callers=`C4:FE3A`
  - `C4:5140` | best=`suspect` | hits=`1` | callers=`C4:814C`
- top backtracks:
  - `C4:5140` -> `C4:5140` | score=`3` | dist=`0` | start=`04` clean_start
  - `C4:5120` -> `C4:511B` | score=`2` | dist=`5` | start=`EE` clean_start
  - `C4:5161` -> `C4:515C` | score=`2` | dist=`5` | start=`04` clean_start
  - `C4:5100` -> `C4:5100` | score=`1` | dist=`0` | start=`9F` clean_start
- local clusters:
  - `C4:51EC..C4:51F3` | cluster_score=`4` | children=`1` | width=`8`

### C4:5200..C4:52FF
- family: **branch_fed_control_pocket**
- posture: **mixed_lane_continue**
- raw targets: `1` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `2` | tiny veneers: `10` | wrapper bad targets: `0`
- best targets:
  - `C4:52E0` | best=`weak` | hits=`1` | callers=`C4:DB00`
- top backtracks:
  - `C4:52E0` -> `C4:52D8` | score=`2` | dist=`8` | start=`A8` clean_start
- local clusters:
  - `C4:525E..C4:5269` | cluster_score=`4` | children=`1` | width=`12`
  - `C4:52A8..C4:52B1` | cluster_score=`3` | children=`1` | width=`10`

### C4:5300..C4:53FF
- family: **candidate_code_lane**
- posture: **local_control_only**
- raw targets: `1` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `1` | tiny veneers: `3` | wrapper bad targets: `0`
- best targets:
  - `C4:53C0` | best=`suspect` | hits=`1` | callers=`C4:DD1F`
- top backtracks:
  - `C4:53C0` -> `C4:53C0` | score=`1` | dist=`0` | start=`D0` clean_start
- local clusters:
  - `C4:5355..C4:5360` | cluster_score=`4` | children=`1` | width=`12`

### C4:5400..C4:54FF
- family: **candidate_code_lane**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `4` | strong/weak effective hits: `2` | hard-bad starts: `1` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `2` | local clusters: `1` | tiny veneers: `3` | wrapper bad targets: `0`
- best targets:
  - `C4:543C` | best=`weak` | hits=`1` | callers=`C4:D4B7`
  - `C4:5447` | best=`weak` | hits=`1` | callers=`C4:0197`
  - `C4:543E` | best=`suspect` | hits=`1` | callers=`C4:E675`
  - `C4:545F` | best=`invalid` | hits=`1` | callers=`C4:C60A`
- top backtracks:
  - `C4:543E` -> `C4:543D` | score=`4` | dist=`1` | start=`20` clean_start
  - `C4:5447` -> `C4:5442` | score=`4` | dist=`5` | start=`44` clean_start
  - `C4:543C` -> `C4:543C` | score=`1` | dist=`0` | start=`10` clean_start
  - `C4:545F` -> `C4:545F` | score=`-4` | dist=`0` | start=`00` hard_bad_start
- local clusters:
  - `C4:54AD..C4:54B1` | cluster_score=`2` | children=`1` | width=`5`
