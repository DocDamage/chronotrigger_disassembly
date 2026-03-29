# Chrono Trigger raw seam report — C4:5F00..C4:68FF

Method note:
- ROM-first seam triage run in the current workspace.
- The local environment had the ROM and reconstructed branch-equivalent seam scripts, but not the full checked-out manifest set, so caller ownership stayed conservative.
- Result standard used here: **no promotions unless caller quality, start-byte quality, and local structure still all agree**.

Start seam page: **C4:5F00**
Pages swept: **10**
Page-family counts: `{"candidate_code_lane": 7, "mixed_command_data": 2, "branch_fed_control_pocket": 1}`
Review-posture counts: `{"bad_start_or_dead_lane_reject": 3, "manual_owner_boundary_review": 3, "local_control_only": 3, "mixed_lane_continue": 1}`

## Page summary

### C4:5F00..C4:5FFF
- family: **candidate_code_lane**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `6` | strong/weak effective hits: `5` | hard-bad starts: `2` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `3` | local clusters: `3` | tiny veneers: `2` | wrapper bad targets: `0`
- best targets:
  - `C4:5F08` | best=`weak` | hits=`2` | callers=`C4:40A2, C4:BFA8`
  - `C4:5F5E` | best=`weak` | hits=`2` | callers=`C4:21F1, C4:68D5`
  - `C4:5FA5` | best=`weak` | hits=`1` | callers=`C4:7A0C`
  - `C4:5FC8` | best=`weak` | hits=`1` | callers=`C4:DC0B`
  - `C4:5F36` | best=`invalid` | hits=`1` | callers=`C4:C5EB`
- top backtracks:
  - `C4:5F7F` -> `C4:5F77` | score=`4` | dist=`8` | start=`34` clean_start
  - `C4:5FC8` -> `C4:5FC0` | score=`4` | dist=`8` | start=`11` clean_start
  - `C4:5F08` -> `C4:5F08` | score=`3` | dist=`0` | start=`65` clean_start
  - `C4:5F36` -> `C4:5F26` | score=`2` | dist=`16` | start=`D0` clean_start
  - `C4:5F5E` -> `C4:5F5C` | score=`2` | dist=`2` | start=`BA` clean_start
- local clusters:
  - `C4:5F10..C4:5F1C` | cluster_score=`4` | children=`1` | width=`13`
  - `C4:5FEA..C4:5FF2` | cluster_score=`4` | children=`1` | width=`9`
  - `C4:5FCC..C4:5FD3` | cluster_score=`2` | children=`1` | width=`8`

### C4:6000..C4:60FF
- family: **candidate_code_lane**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `21` | strong/weak effective hits: `14` | hard-bad starts: `4` | soft-bad starts: `1`
- owner-backtrack candidates (score>=3): `8` | local clusters: `1` | tiny veneers: `8` | wrapper bad targets: `0`
- best targets:
  - `C4:6000` | best=`weak` | hits=`4` | callers=`C4:208B, C4:676F, C4:D56D, C4:E870`
  - `C4:60E0` | best=`weak` | hits=`4` | callers=`C4:7271, C4:1BA7, C4:5BDD, C4:DBC8`
  - `C4:6080` | best=`weak` | hits=`2` | callers=`C4:5B01, C4:901F`
  - `C4:60FD` | best=`weak` | hits=`2` | callers=`C4:238C, C4:6A70`
  - `C4:6005` | best=`weak` | hits=`1` | callers=`C4:807E`
- top backtracks:
  - `C4:6077` -> `C4:6073` | score=`6` | dist=`4` | start=`20` clean_start
  - `C4:6080` -> `C4:607D` | score=`6` | dist=`3` | start=`20` clean_start
  - `C4:6085` -> `C4:607D` | score=`6` | dist=`8` | start=`20` clean_start
  - `C4:603F` -> `C4:603E` | score=`4` | dist=`1` | start=`20` clean_start
  - `C4:6040` -> `C4:603E` | score=`4` | dist=`2` | start=`20` clean_start
- local clusters:
  - `C4:607A..C4:6086` | cluster_score=`5` | children=`2` | width=`13`

### C4:6100..C4:61FF
- family: **candidate_code_lane**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `3` | strong/weak effective hits: `0` | hard-bad starts: `1` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `2` | local clusters: `3` | tiny veneers: `2` | wrapper bad targets: `0`
- best targets:
  - `C4:6121` | best=`suspect` | hits=`1` | callers=`C4:18E4`
  - `C4:6138` | best=`suspect` | hits=`1` | callers=`C4:FE68`
  - `C4:6101` | best=`invalid` | hits=`1` | callers=`C4:D697`
- top backtracks:
  - `C4:6121` -> `C4:6120` | score=`4` | dist=`1` | start=`3E` clean_start
  - `C4:6138` -> `C4:6132` | score=`4` | dist=`6` | start=`3D` clean_start
  - `C4:6101` -> `C4:6100` | score=`-3` | dist=`1` | start=`FF` hard_bad_start
- local clusters:
  - `C4:61E3..C4:61F9` | cluster_score=`4` | children=`1` | width=`23`
  - `C4:61C4..C4:61D3` | cluster_score=`3` | children=`1` | width=`16`
  - `C4:6195..C4:619D` | cluster_score=`2` | children=`1` | width=`9`

### C4:6200..C4:62FF
- family: **candidate_code_lane**
- posture: **manual_owner_boundary_review**
- raw targets: `1` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `4` | tiny veneers: `5` | wrapper bad targets: `0`
- best targets:
  - `C4:62DF` | best=`weak` | hits=`1` | callers=`C4:06CF`
- top backtracks:
  - `C4:62DF` -> `C4:62D7` | score=`4` | dist=`8` | start=`25` clean_start
- local clusters:
  - `C4:620F..C4:6227` | cluster_score=`4` | children=`1` | width=`25`
  - `C4:626D..C4:6273` | cluster_score=`3` | children=`1` | width=`7`
  - `C4:62A4..C4:62AB` | cluster_score=`2` | children=`1` | width=`8`
  - `C4:62F2..C4:62F7` | cluster_score=`2` | children=`1` | width=`6`

### C4:6300..C4:63FF
- family: **candidate_code_lane**
- posture: **manual_owner_boundary_review**
- raw targets: `5` | strong/weak effective hits: `3` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `3` | local clusters: `2` | tiny veneers: `5` | wrapper bad targets: `0`
- best targets:
  - `C4:6330` | best=`weak` | hits=`1` | callers=`C4:164E`
  - `C4:63D8` | best=`weak` | hits=`1` | callers=`C4:5E49`
  - `C4:63DF` | best=`weak` | hits=`1` | callers=`C4:86FC`
  - `C4:6301` | best=`suspect` | hits=`1` | callers=`C4:7598`
  - `C4:63E8` | best=`suspect` | hits=`1` | callers=`C4:3CD6`
- top backtracks:
  - `C4:6330` -> `C4:632B` | score=`6` | dist=`5` | start=`DA` clean_start
  - `C4:63D8` -> `C4:63D0` | score=`6` | dist=`8` | start=`20` clean_start
  - `C4:63DF` -> `C4:63D0` | score=`4` | dist=`15` | start=`20` clean_start
  - `C4:6301` -> `C4:6300` | score=`2` | dist=`1` | start=`37` clean_start
  - `C4:63E8` -> `C4:63E5` | score=`2` | dist=`3` | start=`C1` clean_start
- local clusters:
  - `C4:63CB..C4:63D4` | cluster_score=`5` | children=`1` | width=`10`
  - `C4:63AD..C4:63B5` | cluster_score=`5` | children=`1` | width=`9`

### C4:6400..C4:64FF
- family: **mixed_command_data**
- posture: **manual_owner_boundary_review**
- raw targets: `2` | strong/weak effective hits: `4` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `1` | tiny veneers: `3` | wrapper bad targets: `0`
- best targets:
  - `C4:6411` | best=`weak` | hits=`2` | callers=`C4:25E3, C4:6CC7`
  - `C4:64F3` | best=`weak` | hits=`2` | callers=`C4:329B, C4:7893`
- top backtracks:
  - `C4:6411` -> `C4:6403` | score=`6` | dist=`14` | start=`08` clean_start
  - `C4:64F3` -> `C4:64F3` | score=`-1` | dist=`0` | start=`ED` clean_start
- local clusters:
  - `C4:6402..C4:6407` | cluster_score=`2` | children=`1` | width=`6`

### C4:6500..C4:65FF
- family: **branch_fed_control_pocket**
- posture: **local_control_only**
- raw targets: `0` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `4` | tiny veneers: `13` | wrapper bad targets: `0`
- local clusters:
  - `C4:659D..C4:65A3` | cluster_score=`4` | children=`1` | width=`7`
  - `C4:6546..C4:6556` | cluster_score=`3` | children=`4` | width=`17`
  - `C4:655F..C4:6565` | cluster_score=`2` | children=`1` | width=`7`
  - `C4:65CB..C4:65D0` | cluster_score=`2` | children=`1` | width=`6`

### C4:6600..C4:66FF
- family: **mixed_command_data**
- posture: **mixed_lane_continue**
- raw targets: `1` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `0` | tiny veneers: `1` | wrapper bad targets: `0`
- best targets:
  - `C4:6658` | best=`weak` | hits=`1` | callers=`D0:AE7D`
- top backtracks:
  - `C4:6658` -> `C4:6658` | score=`-1` | dist=`0` | start=`BB` clean_start

### C4:6700..C4:67FF
- family: **candidate_code_lane**
- posture: **local_control_only**
- raw targets: `3` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `3` | tiny veneers: `3` | wrapper bad targets: `0`
- best targets:
  - `C4:6701` | best=`suspect` | hits=`1` | callers=`EE:263C`
  - `C4:6709` | best=`suspect` | hits=`1` | callers=`C4:504F`
  - `C4:67FF` | best=`suspect` | hits=`1` | callers=`C4:0DA6`
- top backtracks:
  - `C4:6709` -> `C4:6706` | score=`4` | dist=`3` | start=`DF` clean_start
  - `C4:6701` -> `C4:6700` | score=`2` | dist=`1` | start=`E1` clean_start
  - `C4:67FF` -> `C4:67F9` | score=`2` | dist=`6` | start=`4A` clean_start
- local clusters:
  - `C4:67C1..C4:67CA` | cluster_score=`2` | children=`1` | width=`10`
  - `C4:676A..C4:676E` | cluster_score=`2` | children=`1` | width=`5`
  - `C4:674A..C4:674E` | cluster_score=`2` | children=`1` | width=`5`

### C4:6800..C4:68FF
- family: **candidate_code_lane**
- posture: **local_control_only**
- raw targets: `1` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `1`
- owner-backtrack candidates (score>=3): `0` | local clusters: `1` | tiny veneers: `2` | wrapper bad targets: `0`
- best targets:
  - `C4:6805` | best=`suspect` | hits=`1` | callers=`C4:3633`
- top backtracks:
  - `C4:6805` -> `C4:6802` | score=`2` | dist=`3` | start=`27` clean_start
- local clusters:
  - `C4:681E..C4:6826` | cluster_score=`2` | children=`1` | width=`9`
