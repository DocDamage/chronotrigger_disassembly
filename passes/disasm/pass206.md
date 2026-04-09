# Pass 206: C3:6800-6FFF Disassembly Notes

**Date:** 2026-04-09
**Session:** 40
**Seam Range:** C3:6800..C3:6FFF

## Candidates Examined

### C3:6A29 (Score 6) - REJECTED

**Candidate Range:** C3:6A29..C3:6A47
**Target Entry:** C3:6A2F
**Caller:** C3:86EE (JSR $6A2F)

```hex
C3:6A20: 8E 1A 20 8D 5A 00 20 AD 1C 20 AE 5C 20 8E 00 1C
C3:6A30: 20 8D 5C 20 60 EE 0E 02 00 03 10 02 0A 60 A5 7B
```

**Analysis:**
- Caller at C3:86EE context shows data-heavy region
- Bytes 8600-8700 contain many ASCII-range values (0x60-0x7F)
- Target sequence `1C 20 8D 5C 20 60` does not form valid 65816 code
- Distance from candidate start (6A29) to target (6A2F) = 6 bytes

**Decision:** Reject - caller in suspicious data context

---

### C3:6ACB (Score 6) - REJECTED

**Candidate Range:** C3:6ACB..C3:6AE5
**Target Entry:** C3:6ACD

```hex
C3:6ACB: 08 73 00 A5 09 05 10 02 8D 10 0D 21 A5 03 05 10
C3:6ADB: 04 8D 0E 08 21 A5 05 05 00 60 20
```

**Analysis:**
- Start byte 0x08 = PHP (valid)
- Second byte 0x73 = Invalid 65816 opcode
- Byte sequence cannot be decoded as valid instruction stream
- No verified caller for this specific target

**Decision:** Reject - invalid opcode sequence

---

### C3:6C11 (Score 6) - REJECTED

**Candidate Range:** C3:6C11..C3:6C38
**Target Entry:** C3:6C20

```hex
C3:6C11: 22 10 38 40 05 A2 41 3F 8E 39 4C 24 3B 05 22 20
C3:6C21: 3D 22 10 08 0B 35 91 2C 10 A0 57 0B 35 03 00 91
C3:6C31: 1C A0 00 00 E0 E2 E4 E6
```

**Analysis:**
- Start byte 0x22 = JSL (Jump to Subroutine Long)
- Target: $403810 (cross-bank to bank $40)
- High ASCII ratio (42.5%) in candidate region
- No clean return context established

**Decision:** Reject - cross-bank jump without verified context

---

### C3:6B12 (Score 4) - NOT PROMOTED

**Candidate Range:** C3:6B12..C3:6B2D
**Target Entry:** C3:6B15
**Caller:** C3:AD34

**Analysis:**
- Score below threshold (4 < 6)
- Weak caller evidence
- Not promoted per conservative policy

---

## Cross-Bank References

| Source | Instruction | Target Bank | Notes |
|--------|-------------|-------------|-------|
| C3:6C11 | JSL $403810 | $40 | Target outside C3, insufficient context |

## 65816 Mode Usage

No REP/SEP instructions detected in examined candidates.
Processor status manipulation (PHP/PLP) present at 6ACB but context invalid.

## Summary

- **Score-6+ candidates examined:** 3
- **Promotions:** 0
- **All pages frozen as data**

No coherent code sequences identified in this seam block.
