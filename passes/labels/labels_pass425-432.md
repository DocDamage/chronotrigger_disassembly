# Labels for Passes 425-432

## Bank C0 Script/Event Engine Functions

### C0:C000 Region
| Address | Label | Pass | Callers | Notes |
|---------|-------|------|---------|-------|
| $C0:C000 | `C0_C000_Entry_6Callers` | 425 | 6 (JSL from D1) | Cross-bank entry point |
| $C0:C09D | `C0_C09D_Utility_13Callers` | 426 | 13 (JSR) | Utility function, no overlap with pass276 |

### C0:C200 Region - Major Script Functions
| Address | Label | Pass | Callers | Notes |
|---------|-------|------|---------|-------|
| $C0:C260 | `C0_C260_Helper_20Callers` | 427 | 20 (JSR) | Event/script helper |
| $C0:C27F | `C0_C27F_MajorDispatcher_65Callers` | 428 | 65 (JSR/JMP) | **MAJOR** script/event dispatcher, highest caller count in region |

### C0:C800 Region
| Address | Label | Pass | Callers | Notes |
|---------|-------|------|---------|-------|
| $C0:C87F | `C0_C87F_ScriptEngine_46Callers` | 429 | 46 (JSR/JMP) | **MAJOR** script engine function |

### C0:9000-A000 Region - Event/Script Utilities
| Address | Label | Pass | Callers | Notes |
|---------|-------|------|---------|-------|
| $C0:97A6 | `C0_97A6_Utility_7Callers` | 430 | 7 (JSR) | Event utility |
| $C0:9923 | `C0_9923_Helper_8Callers` | 431 | 8 (JSR) | Script helper |
| $C0:9F7F | `C0_9F7F_JumpDispatcher_21Callers` | 432 | 21 (JMP) | Jump table dispatcher |

---

## Summary
- **Total new functions identified:** 8
- **Pass numbers created:** 425-432
- **Major high-caller functions:** C0:C27F (65 callers), C0:C87F (46 callers)
- **Overlap verification:** C0:C09D does NOT overlap pass276 (24 byte gap)
