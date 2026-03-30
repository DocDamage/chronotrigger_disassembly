# Chrono Trigger Revisit Backlog From Session-15 Continuation Notes

## Purpose
This is the short backlog extracted from older note-backed seam work so nobody has to reread dozens of continuation notes looking for the same near-miss pages.

This is **not** a “reopen everything” list.
These pages should only be revisited if new caller-quality evidence appears.

Latest tighter audit:
- `docs/reports/chrono_trigger_tier1_revisit_audit_2026-03-30.md`

Current audit result:
- no Tier-1 page earned reopening
- repaired caller-context scoring downgraded every caller-backed Tier-1 target to **suspect / resolved_data**
- exact unsupported islands (`C5:4387..438E`, `C5:4821..482A`) still have zero direct callers

---

## Tier 1: Highest-Value Revisit Candidates

### `C5:4200..42FF`
- Source: `docs/sessions/chrono_trigger_session15_continue_notes_14.md`
- Why it matters: strongest honest near-miss of that block; score-6 backtrack; two caller-backed targets; manual owner-boundary review posture
- Why it still failed: `4200` opens with ORA long, `4208` opens with BEQ, and the score-6 body never stabilized into a defensible owner
- Revisit trigger: a resolved caller into `4208` or nearby ownership bytes

### `C5:4387..438E`
- Source: `docs/sessions/chrono_trigger_session15_continue_notes_14.md`
- Why it matters: only structurally coherent unsupported JSR+body+RTS island in that sweep
- Why it still failed: no external caller support
- Revisit trigger: any resolved caller into the pocket or a nearby entry byte

### `C5:4C00..4CFF`
- Source: `docs/sessions/chrono_trigger_session15_continue_notes_15.md`
- Why it matters: strongest honest near-miss of that block; branch-fed control pocket with clean metrics
- Why it still failed: RTI+RTS appear inside the first 9 bytes, killing the entry claim
- Revisit trigger: resolved branch-side caller evidence

### `C5:4821..482A`
- Source: `docs/sessions/chrono_trigger_session15_continue_notes_15.md`
- Why it matters: structurally correct PHP+body+RTS unsupported island
- Why it still failed: zero external caller support
- Revisit trigger: resolved caller from later `C5` work into that pocket or a neighboring start

### `C5:5400..54FF`
- Source: `docs/sessions/chrono_trigger_session15_continue_notes_16.md`
- Why it matters: strongest honest near-miss of that block; zero bad starts; zero clusters; three score-4 backtracks
- Why it still failed: all candidate bytes collapsed at byte level (`54FF` boundary bait, `54C0` STA-at-entry, `543F` suspect PEI)
- Revisit trigger: future resolved callers into `54C0`, `54FF`, or nearby bytes that materially change ownership confidence

### `C5:3600..36FF`
- Source: `docs/sessions/chrono_trigger_session15_continue_notes_13.md`
- Why it matters: strongest honest near-miss of the mid-`C5` belt
- Why it still failed: page never escaped mixed-content pressure strongly enough for promotion
- Revisit trigger: caller-quality improvement from adjacent resolved work

---

## Tier 2: Useful Older Reference Candidates

### `C5:1800..18FF`
- Source: `docs/sessions/chrono_trigger_session15_continue_notes_12.md`
- Why it matters: strongest honest near-miss in the earlier `C5:1300..26FF` belt
- Revisit trigger: materially stronger caller context than the note had

### `C5:0700..07FF`
- Source: `docs/sessions/chrono_trigger_session15_continue_notes_11.md`
- Why it matters: strongest honest near-miss in the bank-opening `C5` belt
- Revisit trigger: new resolved callers from later nearby closures

### `C4:F600..F6FF`
- Source: `docs/sessions/chrono_trigger_session15_continue_notes_10.md`
- Why it matters: strongest honest near-miss of that late-`C4` pressure belt
- Revisit trigger: only if cross-bank historical review becomes necessary; not on the critical path now

---

## Trap Pages To Avoid Reopening Prematurely

These pages were loud, tempting, and specifically called out as trap territory:
- `C5:4000..40FF` — huge traffic density, no defensible start
- `C5:4E00..4EFF` — score-4 with weak JSR callers, still failed at the byte level
- `C5:5800..58FF` — score-6 trap; target byte was still wrong
- `C5:3800..38FF` — hottest trap page of the mid-`C5` belt
- `C5:2000..20FF` — hottest trap page of the early `C5` belt
- `C5:0000..00FF` — loud early-bank trap page
- `C4:F800..F8FF` — hottest trap page of the late `C4` belt

Rule:
- heat alone is not revisit evidence
- backtrack score alone is not revisit evidence
- only new caller-quality evidence justifies reopening these

---

## Not Backlog

Do **not** treat these as current tasks:
- broad old-bank rereads
- reopening pages just because they were “the cleanest” in a bad block
- revisiting unsupported islands without new inbound caller evidence

Current priority remains the live seam at `C7:0800..`.
