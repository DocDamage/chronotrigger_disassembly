# Priority-region pre-disassembly review — 2026-08-18

This report records the instruction-aligned re-review of the Phase 2 regions requested for C3, C4, C2, and C1. Historical scores were treated as leads. No candidate was promoted unless it also had a defensible entry boundary, internal control flow, regional support, and no conflict with neighboring data.

## Outcome

- New executable owners promoted: **0**
- Historical executable claims corrected to data: **4**
- Historical owner windows corrected to reviewed mid-function fragments: **7 active residual ranges**, with four overlapping provenance records explicitly superseded
- Candidates rejected without changing canonical ownership: **4**
- Candidates initially deferred, then resolved by bank-wide review: **4**
- Unique covered bytes: **59,050 before and after**
- Executable bytes: **38,079 → 37,888**
- Classified-data bytes: **20,971 → 21,162**
- Ownership conflicts after correction: **0**

The unchanged unique-byte total is intentional: this batch corrected classification and ownership claims rather than claiming newly closed ROM space.

## Region results

### C3:8800–8FFF

The repaired primary seam pipeline was rerun across the region. The apparent high code density in the historical score output was not supported by aligned control flow.

| Candidate | Disposition | Evidence summary |
|---|---|---|
| C3:8912 | Reclassified as structured data | `PHP; RTL` is unbalanced, no incoming target reaches the claimed entry, and repeating record data follows. |
| C3:8C8E | Reclassified as command data | Repeating short records cross the window; apparent calls and returns occur at record-field offsets. |
| C3:8A10 | Rejected | Overlapping return-anchored windows and an RTI/RTS proximity signature do not form aligned execution. |
| C3:8937 | Rejected | Below threshold and inside the same disproven mixed-data lane as C3:8912. |

### C4:6800–6FFF and C4:772E

The 6800–6FFF scan produced no new candidate satisfying the promotion standard. The historical C4:772E “supercluster” was separately reviewed because it was a named priority.

| Candidate | Disposition | Evidence summary |
|---|---|---|
| C4:6BDA | Reclassified as patterned data | The apparent `JML` is embedded in a repeating table and has no incoming caller. |
| C4:6805 | Rejected | Bank-wide review places the bytes in the same packed-asset lane; no aligned caller exists. |
| C4:6D54 | Rejected | The weak raw target is an opcode-valued asset field, not an entry boundary. |
| C4:772E / 7730 / 7732 | Reclassified as graphics bitplane data | Three sliding windows sample the same plane/mask patterns; none has aligned caller support. |

### C2 score-14 region

The required C2 addresses were inspected with neighboring bytes and raw reference context rather than accepting the score-fourteen windows.

| Candidate | Disposition | Evidence summary |
|---|---|---|
| C2:8C08 | Rejected as an owner | Mid-function `PHP` in execution already underway at C2:8C00; no incoming target. |
| C2:8DA3 | Rejected as an owner | Mid-function `REP` reached by direct fall-through; no incoming target. |
| C2:8F6D | Executable fragment | Real code follows C2:8F6C, but the historical window has no independent entry and includes the next routine at C2:8FCB. |

C2:8F6D was not promoted speculatively; its bytes are retained as non-owning executable context for later source reconstruction.

### C1 candidate pool

The C1:434A mega-cluster contains real executable bytes, but its historical children are sliding mid-function windows rather than independent functions. Aligned execution begins at C1:432D. Its far boundary and caller remain unresolved, so the reviewed canonical pieces are retained as `tail_fragment` records rather than promoted owners. C1:431B was similarly corrected to a fragment of C1:4310–432C. C1:4744 remains deferred pending a verified caller or table entry.

The historical C1 mega-cluster reports also contain an instruction-boundary error: C1:432C is `RTS`; the following routine begins at C1:432D. C1:4744 was likewise finalized as a non-owning executable fragment because no caller establishes an entry. The historical files remain intact, and this report supplies the correction.

## Durable evidence and reproducibility

- Candidate decisions are recorded in `tools/config/candidate_dispositions.json`.
- Post-migration factual corrections are recorded in `tools/config/manifest_corrections.json` and reapplied by `migrate_manifests.py`.
- Baseline conservation recognizes a correction only when both its original identity and corrected canonical identity are present in the reviewed correction ledger.
- Canonical cross-reference indexing now excludes superseded claims and treats pending code as weak evidence rather than a resolved caller.

## Validation

After these corrections:

- 961/961 canonical manifests validate;
- 1,105/1,105 historical ranges are conserved, including reviewed corrections;
- 1,289 canonical range records have zero ownership conflicts;
- 48 tests pass;
- toolkit doctor passes 9/9 checks;
- strict acceptance passes 12/12 steps;
- binary/cache and artifact policy checks pass.

No ROM, archive, seam-cache, or backup-bundle artifact was added or removed.
