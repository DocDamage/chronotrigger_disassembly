# Chrono Trigger raw seam report — C4:7D00..C4:86FF

Method note:
- ROM-first seam triage run in the current workspace.
- The local environment had the ROM and reconstructed branch-equivalent seam scripts, but not the full checked-out manifest set, so caller ownership stayed conservative.
- Result standard used here: **no promotions unless caller quality, start-byte quality, and local structure still all agree**.

Start seam page: **C4:7D00**
Pages swept: **10**
Page-family counts: `{"candidate_code_lane": 8, "mixed_command_data": 1, "branch_fed_control_pocket": 1}`
Review-posture counts: `{"manual_owner_boundary_review": 5, "local_control_only": 1, "bad_start_or_dead_lane_reject": 3, "mixed_lane_continue": 1}`

## Page summary

### C4:7D00..C4:7DFF
- family: **candidate_code_lane**
- posture: **manual_owner_boundary_review**
- raw targets: `2` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `3` | tiny veneers: `4` | wrapper bad targets: `0`
- best targets:
  - `C4:7D0B` | best=`weak` | hits=`1` | callers=`C4:9471`
  - `C4:7D33` | best=`suspect` | hits=`1` | callers=`C4:D7BE`
- top backtracks:
  - `C4:7D0B` -> `C4:7D0B` | score=`3` | dist=`0` | start=`FD` clean_start
  - `C4:7D33` -> `C4:7D33` | score=`1` | dist=`0` | start=`FA` clean_start
- local clusters:
  - `C4:7DA7..C4:7DB5` | cluster_score=`5` | children=`1` | width=`15`
  - `C4:7D96..C4:7DA0` | cluster_score=`2` | children=`1` | width=`11`
  - `C4:7DCC..C4:7DD1` | cluster_score=`2` | children=`1` | width=`6`

### C4:7E00..C4:7EFF
- family: **candidate_code_lane**
- posture: **local_control_only**
- raw targets: `2` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `2` | local clusters: `4` | tiny veneers: `3` | wrapper bad targets: `0`
- best targets:
  - `C4:7E40` | best=`suspect` | hits=`1` | callers=`C4:3A2D`
  - `C4:7E95` | best=`suspect` | hits=`1` | callers=`C4:5128`
- top backtracks:
  - `C4:7E95` -> `C4:7E90` | score=`4` | dist=`5` | start=`96` clean_start
  - `C4:7E40` -> `C4:7E34` | score=`4` | dist=`12` | start=`6F` clean_start
- local clusters:
  - `C4:7EE4..C4:7EF0` | cluster_score=`5` | children=`1` | width=`13`
  - `C4:7E0A..C4:7E1A` | cluster_score=`5` | children=`1` | width=`17`
  - `C4:7EA3..C4:7EAB` | cluster_score=`3` | children=`1` | width=`9`
  - `C4:7E19..C4:7E26` | cluster_score=`2` | children=`1` | width=`14`

### C4:7F00..C4:7FFF
- family: **candidate_code_lane**
- posture: **manual_owner_boundary_review**
- raw targets: `7` | strong/weak effective hits: `8` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `6` | local clusters: `3` | tiny veneers: `5` | wrapper bad targets: `0`
- best targets:
  - `C4:7F00` | best=`weak` | hits=`2` | callers=`C4:C913, C4:9BAC`
  - `C4:7FFF` | best=`weak` | hits=`2` | callers=`C4:4465, C4:736B`
  - `C4:7F03` | best=`weak` | hits=`1` | callers=`C4:F7E1`
  - `C4:7F15` | best=`weak` | hits=`1` | callers=`C4:C452`
  - `C4:7F1D` | best=`weak` | hits=`1` | callers=`C4:777F`
- top backtracks:
  - `C4:7FFF` -> `C4:7FFF` | score=`5` | dist=`0` | start=`A0` clean_start
  - `C4:7F03` -> `C4:7F00` | score=`4` | dist=`3` | start=`50` clean_start
  - `C4:7F15` -> `C4:7F14` | score=`4` | dist=`1` | start=`40` clean_start
  - `C4:7F1D` -> `C4:7F14` | score=`4` | dist=`9` | start=`40` clean_start
  - `C4:7FB4` -> `C4:7FAB` | score=`4` | dist=`9` | start=`FC` clean_start
- local clusters:
  - `C4:7FAA..C4:7FCA` | cluster_score=`5` | children=`2` | width=`33`
  - `C4:7F8F..C4:7FA7` | cluster_score=`5` | children=`1` | width=`25`
  - `C4:7F13..C4:7F1B` | cluster_score=`4` | children=`1` | width=`9`

### C4:8000..C4:80FF
- family: **candidate_code_lane**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `14` | strong/weak effective hits: `6` | hard-bad starts: `4` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `6` | local clusters: `4` | tiny veneers: `4` | wrapper bad targets: `0`
- best targets:
  - `C4:8012` | best=`weak` | hits=`1` | callers=`C4:7FF5`
  - `C4:8020` | best=`weak` | hits=`1` | callers=`C4:81CD`
  - `C4:80A0` | best=`weak` | hits=`1` | callers=`C4:D6BB`
  - `C4:80AF` | best=`weak` | hits=`1` | callers=`C4:9077`
  - `C4:80B8` | best=`weak` | hits=`1` | callers=`C4:8F91`
- top backtracks:
  - `C4:8012` -> `C4:8010` | score=`6` | dist=`2` | start=`20` clean_start
  - `C4:801F` -> `C4:8010` | score=`6` | dist=`15` | start=`20` clean_start
  - `C4:8020` -> `C4:8010` | score=`6` | dist=`16` | start=`20` clean_start
  - `C4:8002` -> `C4:8000` | score=`4` | dist=`2` | start=`26` clean_start
  - `C4:800F` -> `C4:800C` | score=`4` | dist=`3` | start=`40` clean_start
- local clusters:
  - `C4:807A..C4:8080` | cluster_score=`5` | children=`1` | width=`7`
  - `C4:800B..C4:801D` | cluster_score=`3` | children=`1` | width=`19`
  - `C4:808B..C4:8092` | cluster_score=`3` | children=`1` | width=`8`
  - `C4:805F..C4:8068` | cluster_score=`3` | children=`1` | width=`10`

### C4:8100..C4:81FF
- family: **candidate_code_lane**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `4` | strong/weak effective hits: `2` | hard-bad starts: `2` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `2` | local clusters: `1` | tiny veneers: `7` | wrapper bad targets: `0`
- best targets:
  - `C4:81CD` | best=`weak` | hits=`1` | callers=`C4:DEB8`
  - `C4:81FF` | best=`weak` | hits=`1` | callers=`C4:331B`
  - `C4:8180` | best=`invalid` | hits=`1` | callers=`C4:0DA5`
  - `C4:81A2` | best=`invalid` | hits=`1` | callers=`C4:F8F3`
- top backtracks:
  - `C4:81CD` -> `C4:81CC` | score=`4` | dist=`1` | start=`E7` clean_start
  - `C4:81FF` -> `C4:81FF` | score=`3` | dist=`0` | start=`A2` clean_start
  - `C4:81A2` -> `C4:819C` | score=`2` | dist=`6` | start=`3B` clean_start
  - `C4:8180` -> `C4:817B` | score=`-1` | dist=`5` | start=`80` hard_bad_start
- local clusters:
  - `C4:81AB..C4:81B0` | cluster_score=`2` | children=`1` | width=`6`

### C4:8200..C4:82FF
- family: **mixed_command_data**
- posture: **manual_owner_boundary_review**
- raw targets: `4` | strong/weak effective hits: `5` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `2` | local clusters: `0` | tiny veneers: `1` | wrapper bad targets: `0`
- best targets:
  - `C4:8200` | best=`weak` | hits=`2` | callers=`C4:3735, C4:93B4`
  - `C4:821C` | best=`weak` | hits=`1` | callers=`C4:AD0D`
  - `C4:8263` | best=`weak` | hits=`1` | callers=`C4:85FE`
  - `C4:829D` | best=`weak` | hits=`1` | callers=`C4:C347`
- top backtracks:
  - `C4:821C` -> `C4:821C` | score=`3` | dist=`0` | start=`C3` clean_start
  - `C4:8263` -> `C4:8263` | score=`3` | dist=`0` | start=`3F` clean_start
  - `C4:829D` -> `C4:829C` | score=`2` | dist=`1` | start=`86` clean_start
  - `C4:8200` -> `C4:8200` | score=`1` | dist=`0` | start=`F0` clean_start

### C4:8300..C4:83FF
- family: **candidate_code_lane**
- posture: **mixed_lane_continue**
- raw targets: `2` | strong/weak effective hits: `2` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `0` | tiny veneers: `3` | wrapper bad targets: `0`
- best targets:
  - `C4:831E` | best=`weak` | hits=`1` | callers=`C4:C8A9`
  - `C4:8393` | best=`weak` | hits=`1` | callers=`C4:DE2C`
- top backtracks:
  - `C4:8393` -> `C4:8390` | score=`2` | dist=`3` | start=`EF` clean_start
  - `C4:831E` -> `C4:831D` | score=`0` | dist=`1` | start=`DE` clean_start

### C4:8400..C4:84FF
- family: **candidate_code_lane**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `2` | strong/weak effective hits: `0` | hard-bad starts: `1` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `2` | local clusters: `2` | tiny veneers: `7` | wrapper bad targets: `0`
- best targets:
  - `C4:846D` | best=`suspect` | hits=`1` | callers=`C4:DF96`
  - `C4:8477` | best=`invalid` | hits=`1` | callers=`C4:FEE4`
- top backtracks:
  - `C4:846D` -> `C4:845F` | score=`4` | dist=`14` | start=`A2` clean_start
  - `C4:8477` -> `C4:8470` | score=`4` | dist=`7` | start=`13` clean_start
- local clusters:
  - `C4:8455..C4:845E` | cluster_score=`4` | children=`1` | width=`10`
  - `C4:84A4..C4:84B1` | cluster_score=`4` | children=`1` | width=`14`

### C4:8500..C4:85FF
- family: **branch_fed_control_pocket**
- posture: **manual_owner_boundary_review**
- raw targets: `1` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `3` | tiny veneers: `3` | wrapper bad targets: `0`
- best targets:
  - `C4:85B9` | best=`weak` | hits=`1` | callers=`C4:AAEB`
- top backtracks:
  - `C4:85B9` -> `C4:85AF` | score=`4` | dist=`10` | start=`E1` clean_start
- local clusters:
  - `C4:85CB..C4:85D3` | cluster_score=`3` | children=`2` | width=`9`
  - `C4:857E..C4:8582` | cluster_score=`3` | children=`1` | width=`5`
  - `C4:8547..C4:855C` | cluster_score=`2` | children=`1` | width=`22`

### C4:8600..C4:86FF
- family: **candidate_code_lane**
- posture: **manual_owner_boundary_review**
- raw targets: `1` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `1` | tiny veneers: `5` | wrapper bad targets: `0`
- best targets:
  - `C4:8600` | best=`weak` | hits=`1` | callers=`C4:0124`
- top backtracks:
  - `C4:8600` -> `C4:8600` | score=`3` | dist=`0` | start=`82` clean_start
- local clusters:
  - `C4:86A4..C4:86AC` | cluster_score=`3` | children=`2` | width=`9`
