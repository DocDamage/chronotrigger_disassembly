# Chrono Trigger raw seam report — C4:7300..C4:7CFF

Method note:
- ROM-first seam triage run in the current workspace.
- The local environment had the ROM and reconstructed branch-equivalent seam scripts, but not the full checked-out manifest set, so caller ownership stayed conservative.
- Result standard used here: **no promotions unless caller quality, start-byte quality, and local structure still all agree**.

Start seam page: **C4:7300**
Pages swept: **10**
Page-family counts: `{"branch_fed_control_pocket": 3, "mixed_command_data": 2, "candidate_code_lane": 5}`
Review-posture counts: `{"local_control_only": 5, "manual_owner_boundary_review": 2, "mixed_lane_continue": 3}`

## Page summary

### C4:7300..C4:73FF
- family: **branch_fed_control_pocket**
- posture: **local_control_only**
- raw targets: `2` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `1` | tiny veneers: `12` | wrapper bad targets: `0`
- best targets:
  - `C4:7303` | best=`suspect` | hits=`1` | callers=`C4:59BD`
  - `C4:73A6` | best=`suspect` | hits=`1` | callers=`C4:EE26`
- top backtracks:
  - `C4:7303` -> `C4:7300` | score=`2` | dist=`3` | start=`A5` clean_start
  - `C4:73A6` -> `C4:73A2` | score=`2` | dist=`4` | start=`3C` clean_start
- local clusters:
  - `C4:731E..C4:7325` | cluster_score=`3` | children=`1` | width=`8`

### C4:7400..C4:74FF
- family: **mixed_command_data**
- posture: **local_control_only**
- raw targets: `0` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `2` | tiny veneers: `8` | wrapper bad targets: `0`
- local clusters:
  - `C4:741C..C4:7422` | cluster_score=`4` | children=`1` | width=`7`
  - `C4:747F..C4:7486` | cluster_score=`4` | children=`1` | width=`8`

### C4:7500..C4:75FF
- family: **branch_fed_control_pocket**
- posture: **local_control_only**
- raw targets: `0` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `4` | tiny veneers: `3` | wrapper bad targets: `0`
- local clusters:
  - `C4:7512..C4:7518` | cluster_score=`4` | children=`1` | width=`7`
  - `C4:755D..C4:756A` | cluster_score=`4` | children=`1` | width=`14`
  - `C4:75AB..C4:75B4` | cluster_score=`3` | children=`1` | width=`10`
  - `C4:75E5..C4:75EA` | cluster_score=`2` | children=`1` | width=`6`

### C4:7600..C4:76FF
- family: **candidate_code_lane**
- posture: **manual_owner_boundary_review**
- raw targets: `3` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `2` | local clusters: `2` | tiny veneers: `0` | wrapper bad targets: `0`
- best targets:
  - `C4:76B6` | best=`weak` | hits=`1` | callers=`C4:91DB`
  - `C4:76FF` | best=`suspect` | hits=`2` | callers=`C4:2FF4, C4:75E7`
  - `C4:76B8` | best=`suspect` | hits=`1` | callers=`C4:3849`
- top backtracks:
  - `C4:76B6` -> `C4:76AF` | score=`4` | dist=`7` | start=`84` clean_start
  - `C4:76B8` -> `C4:76AF` | score=`4` | dist=`9` | start=`84` clean_start
  - `C4:76FF` -> `C4:76FC` | score=`2` | dist=`3` | start=`4E` clean_start
- local clusters:
  - `C4:76AE..C4:76B9` | cluster_score=`2` | children=`1` | width=`12`
  - `C4:76D4..C4:76D9` | cluster_score=`2` | children=`1` | width=`6`

### C4:7700..C4:77FF
- family: **candidate_code_lane**
- posture: **mixed_lane_continue**
- raw targets: `1` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `4` | tiny veneers: `1` | wrapper bad targets: `0`
- best targets:
  - `C4:7727` | best=`weak` | hits=`1` | callers=`C4:0A1A`
- top backtracks:
  - `C4:7727` -> `C4:7717` | score=`2` | dist=`16` | start=`93` clean_start
- local clusters:
  - `C4:77A6..C4:77AC` | cluster_score=`4` | children=`1` | width=`7`
  - `C4:770F..C4:7717` | cluster_score=`4` | children=`1` | width=`9`
  - `C4:7780..C4:7787` | cluster_score=`2` | children=`1` | width=`8`
  - `C4:77F3..C4:77F9` | cluster_score=`2` | children=`1` | width=`7`

### C4:7800..C4:78FF
- family: **candidate_code_lane**
- posture: **mixed_lane_continue**
- raw targets: `2` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `1` | tiny veneers: `5` | wrapper bad targets: `0`
- best targets:
  - `C4:7844` | best=`weak` | hits=`1` | callers=`C4:35AB`
  - `C4:7878` | best=`suspect` | hits=`1` | callers=`C4:6C14`
- top backtracks:
  - `C4:7844` -> `C4:7844` | score=`1` | dist=`0` | start=`B2` clean_start
  - `C4:7878` -> `C4:7874` | score=`0` | dist=`4` | start=`2C` clean_start
- local clusters:
  - `C4:7812..C4:781A` | cluster_score=`4` | children=`1` | width=`9`

### C4:7900..C4:79FF
- family: **branch_fed_control_pocket**
- posture: **local_control_only**
- raw targets: `0` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `1` | tiny veneers: `2` | wrapper bad targets: `0`
- local clusters:
  - `C4:79D1..C4:79DA` | cluster_score=`3` | children=`1` | width=`10`

### C4:7A00..C4:7AFF
- family: **candidate_code_lane**
- posture: **mixed_lane_continue**
- raw targets: `1` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `2` | tiny veneers: `4` | wrapper bad targets: `0`
- best targets:
  - `C4:7A5B` | best=`weak` | hits=`1` | callers=`C4:ABC0`
- top backtracks:
  - `C4:7A5B` -> `C4:7A55` | score=`2` | dist=`6` | start=`3E` clean_start
- local clusters:
  - `C4:7A11..C4:7A19` | cluster_score=`3` | children=`1` | width=`9`
  - `C4:7ABF..C4:7AC8` | cluster_score=`2` | children=`1` | width=`10`

### C4:7B00..C4:7BFF
- family: **mixed_command_data**
- posture: **manual_owner_boundary_review**
- raw targets: `2` | strong/weak effective hits: `2` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `1` | tiny veneers: `5` | wrapper bad targets: `0`
- best targets:
  - `C4:7B00` | best=`weak` | hits=`1` | callers=`C4:352B`
  - `C4:7B1C` | best=`weak` | hits=`1` | callers=`C4:8886`
- top backtracks:
  - `C4:7B1C` -> `C4:7B14` | score=`4` | dist=`8` | start=`36` clean_start
  - `C4:7B00` -> `C4:7B00` | score=`1` | dist=`0` | start=`5F` clean_start
- local clusters:
  - `C4:7B79..C4:7B85` | cluster_score=`2` | children=`1` | width=`13`

### C4:7C00..C4:7CFF
- family: **candidate_code_lane**
- posture: **local_control_only**
- raw targets: `1` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `1` | tiny veneers: `6` | wrapper bad targets: `0`
- best targets:
  - `C4:7C69` | best=`suspect` | hits=`1` | callers=`C4:E5BE`
- top backtracks:
  - `C4:7C69` -> `C4:7C60` | score=`2` | dist=`9` | start=`38` clean_start
- local clusters:
  - `C4:7C0D..C4:7C16` | cluster_score=`3` | children=`1` | width=`10`
