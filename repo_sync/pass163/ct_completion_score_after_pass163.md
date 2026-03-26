# Completion Score

- Latest pass: **163**
- Overall completion estimate: **~70.2%**
- Score source of truth: **`reports/completion/ct_completion_score.json`**

## Weighted components
- Label semantics: **80.4%**
- Opcode coverage: **92.5%**
- Bank separation: **40.5%**
- Rebuild readiness: **37.7%**

## Coverage counts
- Master C1 opcodes: **170/170**
- Selector-control bytes: **83/83**
- Service-7 wrappers: **5/8**
- Banks represented in generated source: **15/66**
- Frozen/stable ranges: **969** (73.7 % of label rows)
- Runtime validation rows: **0/0**
- Runtime linked labels: **0** (0.0 % of label rows)
- Rebuild mode: **starter**

## Interpretation
- This is an evidence-weighted estimate, not a fake “almost done” claim.
- The JSON file under `reports/completion/` is the canonical value; handoff notes should mirror it, not override it.
- Semantic coverage can advance faster than the rebuildable-source layer; the score now reflects that instead of hard-coding those layers flat.
- The expensive endgame is still broad bank separation, decompressor work, and byte-accurate assembler validation.
