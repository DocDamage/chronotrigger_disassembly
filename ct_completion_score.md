# Completion Score

- Latest pass: **95**
- Overall completion estimate: **~68.1%**

## Weighted components
- Label semantics: **76.6%**
- Opcode coverage: **92.5%**
- Bank separation: **38.0%**
- Rebuild readiness: **34.1%**

## Coverage counts
- Master C1 opcodes: **170/170**
- Selector-control bytes: **83/83**
- Service-7 wrappers: **5/8**
- Banks represented in generated source: **15/66**
- Frozen/stable ranges: **437** (66.3 % of label rows)
- Runtime validation rows: **0/0**
- Rebuild mode: **scaffold**

## Interpretation
- This is an evidence-weighted estimate, not a fake “almost done” claim.
- Semantic coverage can advance faster than the rebuildable-source layer; the score now reflects that instead of hard-coding those layers flat.
- The expensive endgame is still broad bank separation, decompressor work, and byte-accurate assembler validation.
