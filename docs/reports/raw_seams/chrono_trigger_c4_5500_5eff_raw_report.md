# Chrono Trigger raw seam report — C4:5500..C4:5EFF

Method note:
- ROM-first seam triage run in the current workspace.
- The local environment had the ROM and the public branch scripts, but not the full checked-out manifest set, so caller ownership stayed conservative.
- Result standard used here: **no promotions unless caller quality, start-byte quality, and local structure still all agree**.

Start seam page: **C4:5500**
Pages swept: **10**
Page-family counts: `{"candidate_code_lane": 7, "branch_fed_control_pocket": 1, "mixed_command_data": 2}`
Review-posture counts: `{"local_control_only": 4, "mixed_lane_continue": 2, "bad_start_or_dead_lane_reject": 1, "manual_owner_boundary_review": 3}`

## Page summary

### C4:5500..C4:55FF
- family: **candidate_code_lane**
- posture: **local_control_only**
- raw targets: `0` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `2` | tiny veneers: `3` | wrapper bad targets: `0`
- local clusters:
  - `C4:552D..C4:5535` | cluster_score=`4` | children=`1` | width=`9`
  - `C4:5599..C4:55A5` | cluster_score=`3` | children=`1` | width=`13`

### C4:5600..C4:56FF
- family: **branch_fed_control_pocket**
- posture: **mixed_lane_continue**
- raw targets: `2` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `3` | tiny veneers: `16` | wrapper bad targets: `0`
- best targets:
  - `C4:565F` | best=`weak` | hits=`1` | callers=`C4:491D`
  - `C4:567A` | best=`suspect` | hits=`1` | callers=`C4:E0CD`
- top backtracks:
  - `C4:567A` -> `C4:5678` | score=`2` | dist=`2` | start=`23` clean_start
  - `C4:565F` -> `C4:565F` | score=`1` | dist=`0` | start=`08` clean_start
- local clusters:
  - `C4:568E..C4:5699` | cluster_score=`4` | children=`1` | width=`12`
  - `C4:56E0..C4:56EB` | cluster_score=`4` | children=`1` | width=`12`
  - `C4:563D..C4:5643` | cluster_score=`4` | children=`1` | width=`7`

### C4:5700..C4:57FF
- family: **candidate_code_lane**
- posture: **bad_start_or_dead_lane_reject**
- raw targets: `4` | strong/weak effective hits: `0` | hard-bad starts: `3` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `3` | local clusters: `3` | tiny veneers: `5` | wrapper bad targets: `0`
- best targets:
  - `C4:5720` | best=`suspect` | hits=`1` | callers=`C4:0DCD`
  - `C4:5757` | best=`invalid` | hits=`1` | callers=`C4:0DCE`
  - `C4:57A8` | best=`invalid` | hits=`1` | callers=`C4:4F93`
  - `C4:57DF` | best=`invalid` | hits=`1` | callers=`C4:0640`
- top backtracks:
  - `C4:5757` -> `C4:5753` | score=`4` | dist=`4` | start=`21` clean_start
  - `C4:57A8` -> `C4:57A7` | score=`4` | dist=`1` | start=`04` clean_start
  - `C4:57DF` -> `C4:57D8` | score=`4` | dist=`7` | start=`06` clean_start
  - `C4:5720` -> `C4:571C` | score=`2` | dist=`4` | start=`CC` clean_start
- local clusters:
  - `C4:5740..C4:574A` | cluster_score=`5` | children=`1` | width=`11`
  - `C4:5752..C4:5759` | cluster_score=`3` | children=`2` | width=`8`
  - `C4:5795..C4:579D` | cluster_score=`2` | children=`1` | width=`9`

### C4:5800..C4:58FF
- family: **candidate_code_lane**
- posture: **manual_owner_boundary_review**
- raw targets: `2` | strong/weak effective hits: `2` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `2` | local clusters: `1` | tiny veneers: `6` | wrapper bad targets: `0`
- best targets:
  - `C4:5800` | best=`weak` | hits=`1` | callers=`C4:FDD8`
  - `C4:58AC` | best=`weak` | hits=`1` | callers=`C4:1747`
- top backtracks:
  - `C4:58AC` -> `C4:58A9` | score=`6` | dist=`3` | start=`08` clean_start
  - `C4:5800` -> `C4:5800` | score=`3` | dist=`0` | start=`7C` clean_start
- local clusters:
  - `C4:58EC..C4:58F4` | cluster_score=`2` | children=`1` | width=`9`

### C4:5900..C4:59FF
- family: **candidate_code_lane**
- posture: **local_control_only**
- raw targets: `0` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `1` | tiny veneers: `3` | wrapper bad targets: `0`
- local clusters:
  - `C4:59A0..C4:59A9` | cluster_score=`3` | children=`1` | width=`10`

### C4:5A00..C4:5AFF
- family: **mixed_command_data**
- posture: **mixed_lane_continue**
- raw targets: `1` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `1` | tiny veneers: `4` | wrapper bad targets: `0`
- best targets:
  - `C4:5A0E` | best=`weak` | hits=`1` | callers=`F1:2F2A`
- top backtracks:
  - `C4:5A0E` -> `C4:5A0E` | score=`1` | dist=`0` | start=`EC` clean_start
- local clusters:
  - `C4:5A68..C4:5A72` | cluster_score=`3` | children=`1` | width=`11`

### C4:5B00..C4:5BFF
- family: **candidate_code_lane**
- posture: **local_control_only**
- raw targets: `0` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `0` | local clusters: `2` | tiny veneers: `12` | wrapper bad targets: `0`
- local clusters:
  - `C4:5BC0..C4:5BC9` | cluster_score=`4` | children=`1` | width=`10`
  - `C4:5B31..C4:5B39` | cluster_score=`3` | children=`1` | width=`9`

### C4:5C00..C4:5CFF
- family: **candidate_code_lane**
- posture: **local_control_only**
- raw targets: `2` | strong/weak effective hits: `0` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `4` | tiny veneers: `13` | wrapper bad targets: `0`
- best targets:
  - `C4:5C8B` | best=`suspect` | hits=`1` | callers=`C4:00DF`
  - `C4:5CF9` | best=`suspect` | hits=`1` | callers=`C4:3D75`
- top backtracks:
  - `C4:5C8B` -> `C4:5C89` | score=`6` | dist=`2` | start=`48` clean_start
  - `C4:5CF9` -> `C4:5CF7` | score=`2` | dist=`2` | start=`F6` clean_start
- local clusters:
  - `C4:5C39..C4:5C4B` | cluster_score=`4` | children=`1` | width=`19`
  - `C4:5CAF..C4:5CB4` | cluster_score=`4` | children=`1` | width=`6`
  - `C4:5C7C..C4:5C86` | cluster_score=`3` | children=`1` | width=`11`
  - `C4:5C1C..C4:5C24` | cluster_score=`3` | children=`1` | width=`9`

### C4:5D00..C4:5DFF
- family: **mixed_command_data**
- posture: **manual_owner_boundary_review**
- raw targets: `1` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `1` | tiny veneers: `2` | wrapper bad targets: `0`
- best targets:
  - `C4:5D15` | best=`weak` | hits=`1` | callers=`C4:E011`
- top backtracks:
  - `C4:5D15` -> `C4:5D12` | score=`4` | dist=`3` | start=`E6` clean_start
- local clusters:
  - `C4:5D11..C4:5D1C` | cluster_score=`3` | children=`2` | width=`12`

### C4:5E00..C4:5EFF
- family: **candidate_code_lane**
- posture: **manual_owner_boundary_review**
- raw targets: `2` | strong/weak effective hits: `1` | hard-bad starts: `0` | soft-bad starts: `0`
- owner-backtrack candidates (score>=3): `1` | local clusters: `3` | tiny veneers: `2` | wrapper bad targets: `0`
- best targets:
  - `C4:5E01` | best=`weak` | hits=`1` | callers=`C4:D38B`
  - `C4:5E34` | best=`suspect` | hits=`1` | callers=`C4:CE19`
- top backtracks:
  - `C4:5E01` -> `C4:5E01` | score=`3` | dist=`0` | start=`CF` clean_start
  - `C4:5E34` -> `C4:5E33` | score=`2` | dist=`1` | start=`3F` clean_start
- local clusters:
  - `C4:5E78..C4:5E8B` | cluster_score=`5` | children=`2` | width=`20`
  - `C4:5E11..C4:5E19` | cluster_score=`3` | children=`1` | width=`9`
  - `C4:5EBD..C4:5EC2` | cluster_score=`2` | children=`1` | width=`6`
