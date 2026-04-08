# C5:C000-CFFF New Manifests Summary

## Generated: 2026-04-08
## Total New Manifests: 8

---

## Score-6 (High Confidence) - 4 manifests

| Pass | File | Range | Label | Prologue |
|------|------|-------|-------|----------|
| 710 | manifest_c036.json | C5:C036-C050 | ct_c5_c036_jsr_prologue | JSR (20) |
| 711 | manifest_c0ea.json | C5:C0EA-C10C | ct_c5_c0ea_php_prologue | PHP (08) |
| 712 | manifest_c1e6.json | C5:C1E6-C207 | ct_c5_c1e6_jsr_prologue | JSR (20) |
| 713 | manifest_cef2.json | C5:CEF2-CF18 | ct_c5_cef2_php_prologue | PHP (08) |

---

## Score-5 (Medium-High Confidence) - 2 manifests

| Pass | File | Range | Label | Prologue |
|------|------|-------|-------|----------|
| 714 | manifest_c2fd.json | C5:C2FD-C315 | ct_c5_c2fd_phd_prologue | PHD (0B) |
| 715 | manifest_cd33.json | C5:CD33-CD4B | ct_c5_cd33_ldy_prologue | LDY# (A0) |

---

## Score-4 (Medium Confidence) - 4 manifests

| Pass | File | Range | Label | Prologue |
|------|------|-------|-------|----------|
| 716 | manifest_c617.json | C5:C617-C637 | ct_c5_c617_jsr_prologue | JSR (20) |
| 717 | manifest_c4fa.json | C5:C4FA-C518 | ct_c5_c4fa_php_prologue | PHP (08) |
| 718 | manifest_cb2b.json | C5:CB2B-CB47 | ct_c5_cb2b_entry | AND (39) |
| 719 | manifest_c2a9.json | C5:C2A9-C2C8 | ct_c5_c2a9_phb_prologue | PHB (8B) |

---

## Entry Point Distribution

```
C5:C000 +----------------------------------+
      C030 |########## EXISTING (Pass 577)
      C036 |########## NEW (710) JSR
      C0B7 |########## EXISTING (Pass 578) JSL
      C0EA |########## NEW (711) PHP
C5:C100 +----------------------------------+
      C1E6 |########## NEW (712) JSR
C5:C200 +----------------------------------+
      C2A9 |########## NEW (719) PHB
      C2FD |########## NEW (714) PHD
C5:C400 +----------------------------------+
      C4FA |########## NEW (717) PHP
C5:C600 +----------------------------------+
      C617 |########## NEW (716) JSR
C5:CB00 +----------------------------------+
      CB2B |########## NEW (718) Entry
C5:CD00 +----------------------------------+
      CD33 |########## NEW (715) LDY#
C5:CE00 +----------------------------------+
      CEF2 |########## NEW (713) PHP
C5:D000 +----------------------------------+
```

---

## Prologue Type Summary

| Type | Count | Manifests |
|------|-------|-------------|
| PHP (08) | 3 | 711, 713, 717 |
| JSR (20) | 3 | 710, 712, 716 |
| PHD (0B) | 1 | 714 |
| LDY# (A0) | 1 | 715 |
| PHB (8B) | 1 | 719 |
| AND (39) | 1 | 718 |

---

## Notes

- All manifests use pass numbers 710-719 (reserved for C5:C000-CFFF expansion)
- Score-6 manifests marked with "high" confidence
- Score-4/5 manifests marked with "medium" confidence
- Ranges estimated based on backtrack analysis candidate_range fields
- All candidates verified to have "clean_start" classification

---

## Recommended Next Steps

1. Validate manifests 710-713 (score-6) for immediate promotion
2. Review manifests 714-715 (score-5) for medium priority
3. Consider manifests 716-719 (score-4) for gap filling
4. Run conflict check against existing C5 manifests
5. Generate assembly labels for promoted manifests
