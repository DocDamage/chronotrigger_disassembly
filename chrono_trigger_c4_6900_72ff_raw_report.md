# Chrono Trigger raw seam report — C4:6900..C4:72FF

Method note:
- ROM-first seam triage run in the current workspace.
- The local environment had the ROM and reconstructed branch-equivalent seam scripts, but not the full checked-out manifest set, so caller ownership stayed conservative.
- Result standard used here: **no promotions unless caller quality, start-byte quality, and local structure still all agree**.

Start seam page: **C4:6900**
Pages swept: **10**
Page-family counts: `{"mixed_command_data": 5, "candidate_code_lane": 5}`
Review-posture counts: `{"bad_start_or_dead_lane_reject": 2, "local_control_only": 5, "manual_owner_boundary_review": 3}`

## Page summary

### C4:6900..C4:69FF
- family: **mixed_command_data**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `1` | strong/weak effective hits: `0` | hard-bad starts: `1` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `3` | tiny veneers: `5` | wrapper bad targets: `0`
- best targets:
  - `C4:69C4` | best=`invalid` | hits=`1` | callers=`F6:B31A`
- top backtracks:
  - `C4:69C4` -> `C4:69C4` | score=`-4` | dist=`0` | start=`FF` hard_bad_start
- local clusters:
  - `C4:6913..C4:691B` | cluster_score=`4` | children=`1` | width=`9`
  - `C4:6901..C4:6908` | cluster_score=`3` | children=`1` | width=`8`
  - `C4:69DB..C4:69E0` | cluster_score=`2` | children=`1` | width=`6`

### C4:6A00..C4:6AFF
- family: **mixed_command_data**
- posture: **local_control_only**
- raw targets: `1` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `1` | tiny veneers: `3` | wrapper bad targets: `0`
- best targets:
  - `C4:6AD1` | best=`suspect` | hits=`1` | callers=`C4:08FC`
- top backtracks:
  - `C4:6AD1` -> `C4:6ACD` | score=`4` | dist=`4` | start=`8E` clean_start
- local clusters:
  - `C4:6AB3..C4:6AB7` | cluster_score=`3` | children=`1` | width=`5`

### C4:6B00..C4:6BFF
- family: **candidate_code_lane**
- posture: **local_control_only**
- raw targets: `0` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `2` | tiny veneers: `5` | wrapper bad targets: `0`
- local clusters:
  - `C4:6BDA..C4:6BE1` | cluster_score=`6` | children=`1` | width=`8`
  - `C4:6BBE..C4:6BCD` | cluster_score=`4` | children=`1` | width=`16`

### C4:6C00..C4:6CFF
- family: **mixed_command_data**
- posture: **local_control_only**
- raw targets: `0` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `1` | tiny veneers: `2` | wrapper bad targets: `0`
- local clusters:
  - `C4:6CB0..C4:6CBA` | cluster_score=`4` | children=`2` | width=`11`

### C4:6D00..C4:6DFF
- family: **mixed_command_data**
- posture: **manual_owner_boundary_review**
- raw targets: `2` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `4` | tiny veneers: `3` | wrapper bad targets: `0`
- best targets:
  - `C4:6D54` | best=`weak` | hits=`1` | callers=`C4:0694`
  - `C4:6D37` | best=`suspect` | hits=`1` | callers=`C4:066B`
- top backtracks:
  - `C4:6D37` -> `C4:6D28` | score=`4` | dist=`15` | start=`99` clean_start
  - `C4:6D54` -> `C4:6D47` | score=`2` | dist=`13` | start=`BF` clean_start
- local clusters:
  - `C4:6DC1..C4:6DD3` | cluster_score=`3` | children=`1` | width=`19`
  - `C4:6D27..C4:6D2C` | cluster_score=`3` | children=`1` | width=`6`
  - `C4:6D87..C4:6D8F` | cluster_score=`2` | children=`1` | width=`9`
  - `C4:6D55..C4:6D5C` | cluster_score=`2` | children=`1` | width=`8`

### C4:6E00..C4:6EFF
- family: **mixed_command_data**
- posture: **local_control_only**
- raw targets: `0` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `4` | tiny veneers: `4` | wrapper bad targets: `0`
- local clusters:
  - `C4:6EA8..C4:6EB8` | cluster_score=`7` | children=`2` | width=`17`
  - `C4:6E69..C4:6E6F` | cluster_score=`3` | children=`1` | width=`7`
  - `C4:6E47..C4:6E4D` | cluster_score=`2` | children=`1` | width=`7`
  - `C4:6E2F..C4:6E34` | cluster_score=`2` | children=`1` | width=`6`

### C4:6F00..C4:6FFF
- family: **candidate_code_lane**
- posture: **local_control_only**
- raw targets: `0` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `2` | tiny veneers: `5` | wrapper bad targets: `0`
- local clusters:
  - `C4:6F96..C4:6FA7` | cluster_score=`3` | children=`2` | width=`18`
  - `C4:6FC9..C4:6FD0` | cluster_score=`2` | children=`1` | width=`8`

### C4:7000..C4:70FF
- family: **candidate_code_lane**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `10` | strong/weak effective hits: `5` | hard-bad starts: `1` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `4` | local clusters: `3` | tiny veneers: `7` | wrapper bad targets: `0`
- best targets:
  - `C4:70B0` | best=`weak` | hits=`2` | callers=`C4:C387, C4:160D`
  - `C4:7002` | best=`weak` | hits=`1` | callers=`C4:CB38`
  - `C4:7010` | best=`weak` | hits=`1` | callers=`C4:8FCF`
  - `C4:704F` | best=`weak` | hits=`1` | callers=`C4:A076`
  - `C4:70C0` | best=`weak` | hits=`1` | callers=`C4:45D0`
- top backtracks:
  - `C4:704F` -> `C4:703F` | score=`4` | dist=`16` | start=`40` clean_start
  - `C4:70B0` -> `C4:70AC` | score=`4` | dist=`4` | start=`3F` clean_start
  - `C4:70C0` -> `C4:70BE` | score=`4` | dist=`2` | start=`C7` clean_start
  - `C4:70CA` -> `C4:70BC` | score=`4` | dist=`14` | start=`20` clean_start
  - `C4:7002` -> `C4:7000` | score=`2` | dist=`2` | start=`A0` clean_start
- local clusters:
  - `C4:70BD..C4:70C2` | cluster_score=`4` | children=`1` | width=`6`
  - `C4:7037..C4:703F` | cluster_score=`3` | children=`1` | width=`9`
  - `C4:7099..C4:70A1` | cluster_score=`2` | children=`1` | width=`9`

### C4:7100..C4:71FF
- family: **candidate_code_lane**
- posture: **manual_owner_boundary_review**
- raw targets: `4` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `2` | local clusters: `3` | tiny veneers: `4` | wrapper bad targets: `0`
- best targets:
  - `C4:71C6` | best=`weak` | hits=`1` | callers=`C4:FA8A`
  - `C4:7100` | best=`suspect` | hits=`1` | callers=`C4:BEC0`
  - `C4:714F` | best=`suspect` | hits=`1` | callers=`C4:2F9E`
  - `C4:71A6` | best=`suspect` | hits=`1` | callers=`C4:A7D3`
- top backtracks:
  - `C4:714F` -> `C4:713F` | score=`4` | dist=`16` | start=`50` clean_start
  - `C4:71A6` -> `C4:71A3` | score=`4` | dist=`3` | start=`7B` clean_start
  - `C4:7100` -> `C4:7100` | score=`1` | dist=`0` | start=`DF` clean_start
  - `C4:71C6` -> `C4:71B9` | score=`0` | dist=`13` | start=`DD` clean_start
- local clusters:
  - `C4:713D..C4:7156` | cluster_score=`5` | children=`2` | width=`26`
  - `C4:7117..C4:711D` | cluster_score=`3` | children=`1` | width=`7`
  - `C4:71CC..C4:71D4` | cluster_score=`2` | children=`1` | width=`9`

### C4:7200..C4:72FF
- family: **candidate_code_lane**
- posture: **manual_owner_boundary_review**
- raw targets: `1` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `2` | tiny veneers: `8` | wrapper bad targets: `0`
- best targets:
  - `C4:7202` | best=`weak` | hits=`1` | callers=`C4:59B4`
- top backtracks:
  - `C4:7202` -> `C4:7200` | score=`4` | dist=`2` | start=`40` clean_start
- local clusters:
  - `C4:726C..C4:7273` | cluster_score=`3` | children=`1` | width=`8`
  - `C4:7243..C4:7249` | cluster_score=`3` | children=`1` | width=`7`
