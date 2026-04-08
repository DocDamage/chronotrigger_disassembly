# Toolkit Updates Summary

This document summarizes the toolkit updates made during Agent Swarm Sessions 1-9.

## New Tools Added

### 1. `generate_coverage_report_v2.py`
**Purpose**: Fixed coverage calculation with overlap detection and range merging.

**Issues Fixed**:
- Bank C5 showing negative coverage (-2689 bytes)
- Overlapping manifests counting bytes multiple times
- No visibility into range conflicts

**Improvements**:
- Merges overlapping and adjacent ranges
- Reports overlap warnings with pass numbers
- Shows diagnostic info for conflict resolution

**Usage**:
```bash
python tools/generate_coverage_report_v2.py
```

---

### 2. `detect_data_patterns_v1.py`
**Purpose**: Detect data patterns vs code patterns in ROM regions.

**Issues Addressed**:
- C6:CC00-D000 identified as PHP-heavy but actually data-encoded structure
- Zero-filled dead zones not automatically detected
- Jump vector tables (like C4:C0C0) vs code confusion

**Detects**:
- `DATA_ENCODED_CONTROL`: PHP/SED/PLP/BRK structural patterns (bytecode/state machine)
- `DEAD_ZONE`: Zero-filled regions (exclude from mapping)
- `TEXT_DATA`: ASCII text regions
- `VECTOR_TABLE`: Jump vector tables
- `DATA_TABLE`: Low opcode density data
- `CODE_CANDIDATE`: Standard code regions

**Usage**:
```bash
python tools/scripts/detect_data_patterns_v1.py --rom "rom/Chrono Trigger (USA).sfc" --bank C6 --start CC00 --end D000
```

---

### 3. `validate_cross_bank_callers_v1.py`
**Purpose**: Validate cross-bank callers and detect fake same-bank misidentifications.

**Issues Addressed**:
- C4:8010 had 22 "cross-bank" callers that were actually same-bank JSR/JMP
- No automated way to verify anchor validity
- False positives in cross-bank analysis

**Validates**:
- `VALID_CROSS_BANK`: True JSL/JML from different bank
- `VALID_SAME_BANK`: True JSR/JMP within same bank
- `FAKE_CROSS_BANK`: Same-bank instruction misidentified
- `INVALID`: Not a call instruction or target mismatch

**Usage**:
```bash
python tools/scripts/validate_cross_bank_callers_v1.py --rom "rom/Chrono Trigger (USA).sfc" --target C4:8010 --callers C4:7FF5 C4:81CD C7:1234
```

---

## Issues Discovered During Agent Swarm

### 1. Coverage Calculation Bug
**Problem**: Overlapping manifests caused negative coverage in Bank C5.

**Root Cause**: Original tool counted overlapping bytes multiple times.

**Solution**: `generate_coverage_report_v2.py` merges ranges before calculation.

---

### 2. Fake Cross-Bank Callers
**Problem**: 22 "cross-bank" callers to C4:8010 were actually same-bank JSR/JMP.

**Root Cause**: Raw xref index matched instruction bytes that happened to match addresses.

**Solution**: `validate_cross_bank_callers_v1.py` validates actual instruction opcodes.

---

### 3. Data vs Code Misidentification
**Problem**: C6:CC00-D000 flagged as code (99 PHP prologues) but was actually data structure.

**Root Cause**: High PHP count looked like function prologues, but pattern was `08 F8 ... 28 00` repeating.

**Solution**: `detect_data_patterns_v1.py` identifies structural patterns vs organic code.

---

### 4. CF:8000-9000 Misidentification
**Problem**: Initially thought to be dispatch table (score 134), actually moderate code region.

**Root Cause**: "Score 134" was aggregate instruction counts, not unique entry points.

**Solution**: Agent reports now distinguish aggregate counts from unique candidates.

---

## Recommended Toolkit Workflow

1. **Before disassembly**: Run `detect_data_patterns_v1.py` on suspicious regions
2. **After creating manifests**: Run `generate_coverage_report_v2.py` to check overlaps
3. **For cross-bank validation**: Use `validate_cross_bank_callers_v1.py` on high-caller targets
4. **For gap analysis**: Use original `generate_coverage_report.py` for quick stats, v2 for detailed analysis

---

## Future Improvements Needed

1. **Automated dead zone exclusion**: Tool to mark zero-filled regions as data
2. **Dispatch table detector**: Identify jump vector patterns (CF:8000 style)
3. **Score aggregation fix**: Distinguish aggregate instruction density from unique entry points
4. **Range conflict resolver**: Automated tool to resolve overlapping manifests

---

*Last updated: 2026-04-08*
