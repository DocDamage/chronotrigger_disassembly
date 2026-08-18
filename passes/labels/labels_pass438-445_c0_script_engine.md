# Labels for Passes 438-445: C0 Script/Event Engine Functions

## Summary
- **Total new functions identified:** 8
- **Pass numbers created:** 438-445
- **Regions covered:** C0:C000-C800 (script engine), C0:9000-A000 (event utilities)

---

## Bank C0:C000-C800 Region - Script Engine Core

| Address | Label | Pass | Callers | Notes |
|---------|-------|------|---------|-------|
| $C0:C000 | `C0_C000_Entry_6Callers` | 444 | 6 (JSL from D1) | Cross-bank entry point |
| $C0:C09D | `C0_C09D_Utility_13Callers` | 445 | 13 (JSR) | Utility function, **24-byte gap** before pass276 |
| $C0:C260 | `C0_C260_Helper_20Callers` | 438 | 20 (JSR) | Event/script helper, related to C0:C27F |
| $C0:C27F | `C0_C27F_MajorDispatcher_65Callers` | 439 | **65 (JSR/JMP)** | **MAJOR** script/event dispatcher, highest caller count in region |
| $C0:C87F | `C0_C87F_ScriptEngine_46Callers` | 440 | **46 (JSR/JMP)** | **MAJOR** script engine function, second highest caller count |

---

## Bank C0:9000-A000 Region - Event/Script Utilities

| Address | Label | Pass | Callers | Notes |
|---------|-------|------|---------|-------|
| $C0:97A6 | `C0_97A6_Utility_7Callers` | 441 | 7 (JSR) | Event utility function, adjusted to C0:97C0 to avoid pass326 |
| $C0:9923 | `C0_9923_Helper_8Callers` | 442 | 8 (JSR) | Script helper function |
| $C0:9F7F | `C0_9F7F_JumpDispatcher_21Callers` | 443 | 21 (JMP) | Jump table dispatcher |

---

## Major High-Caller Functions Status

| Function | Address | Callers | Pass | Status |
|----------|---------|---------|------|--------|
| **Script Dispatcher** | C0:C27F | 65 | 439 | ✅ NEW - Highest caller count in C0:C000-C800 |
| **Script Engine** | C0:C87F | 46 | 440 | ✅ NEW - Second highest caller count |
| **Jump Dispatcher** | C0:9F7F | 21 | 443 | ✅ NEW - Jump table target |
| **Script Helper** | C0:C260 | 20 | 438 | ✅ NEW - Related to C0:C27F |
| **Utility** | C0:C09D | 13 | 445 | ✅ NEW - No overlap with pass276 |
| **Entry Point** | C0:C000 | 6 | 444 | ✅ NEW - Cross-bank entry |

---

## Overlap Verification

### C0:C09D vs pass276
- **C0:C09D:** 0xC09D (49309) - Pass 445: C0:C09D..C0:C0B4
- **pass276:** C0:C0B5..C0:C110 (49333-49424)
- **Gap:** 24 bytes (C0:C09D-C0:C0B4 ends at 0xC0B4 = 49332, pass276 starts at 0xC0B5 = 49333)
- **Result:** ✅ NO OVERLAP

---

## Coverage Impact

### Before This Scan:
- C0:C000-C800: pass276 (C0:C0B5..C0:C110), pass342-346, pass417-418 only
- C0:9000-A000: pass419 (C0:997F..C0:998A) only

### After This Scan:
- **8 new functions documented** in C0:C000-C800 and C0:9000-A000
- Major script engine entry points identified (C0:C27F, C0:C87F)
- No overlaps with existing passes
