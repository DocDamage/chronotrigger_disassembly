# Session 32 Summary: C3 Low-Bank Forward Seam (C3:2900–C3:2FFF)

## Date: 2026-04-09
## Scope: C3:2900–C3:2FFF (Sequential forward seam continuation from pass 191)

---

## 1. Executive Summary

Continued the sequential C3 low-bank forward seam from pass 191's stopping point at C3:2900. Produced **2 passes** (192–193) covering **1792 bytes** (C3:2900–C3:2FFF). One page received full annotated disassembly (C3:2B00); the remaining 6 pages were frozen as mixed data or structured data tables.

### Key Achievements
- **7 new closed ranges** added to the snapshot (1737 → 1744)
- **2 manifests** created (pass1209, pass1210)
- **1 fully annotated disassembly** of C3:2B00 with hardware register analysis
- **6 data pages frozen** with detailed justification (BRK density, byte-coincidence analysis, invalid bank targets)
- **Closed ranges snapshot** updated to 1744 ranges

---

## 2. Pass 192 — C3:2900..C3:2BFF

### Manifest: `passes/manifests/pass1209_c3_s32.json`

| Range | Classification | Confidence | Key Evidence |
|-------|---------------|------------|--------------|
| C3:2900..C3:29FF | data (frozen) | high | 19 BRK (7.4%), no xref targets, no prologue patterns |
| C3:2A00..C3:2AFF | data (frozen) | high | 17 BRK, 6 unsupported RTS, misaligned HW register fragments |
| C3:2B00..C3:2BFF | owner (annotated) | medium-high | Code score 52, 3 RTL, 9 JSR, HW division/multiplication |

### C3:2B00 Annotated Disassembly Highlights
- **Hardware division**: `STA $4204` at C3:2B7A (CPU Dividend Low register)
- **Hardware multiplication**: `STA $4202` at C3:2BF2 (CPU Multiplicand register, possible misalignment)
- **Cross-bank JSL**: `JSL $C3:0E29` at C3:2BA3 — known utility function
- **9 JSR calls** to C3 low-bank utilities: `$00E2`, `$021B`, `$0C0A`, `$10C2`, `$1310`, `$16B8`, `$8017`, `$F4AC`
- **Table-driven computation**: `$00A9+Y`, `$1446+Y`, `$0E40+X`, `$8290+X`
- **Long data access**: `LDA $FE:A531,X` — fixed ROM bank data table
- **DP variable map**: 18 variables tracked ($04–$FE)
- **Cross-page flow**: `BMI $2C01` at C3:2BF9 (later resolved to data target)

---

## 3. Pass 193 — C3:2C00..C3:2FFF

### Manifest: `passes/manifests/pass1210_c3_s32.json`

| Range | Classification | Confidence | Key Evidence |
|-------|---------------|------------|--------------|
| C3:2C00..C3:2CFF | data (frozen) | high | 0 RTS/RTL, JML to invalid bank $A6, 4 COP opcodes |
| C3:2D00..C3:2DFF | data (frozen) | high | 32 BRK (12.5%), score inflated by byte coincidences |
| C3:2E00..C3:2EFF | data (frozen) | high | 42 BRK (16.4%), 14 RTI coincidences, structured `00 XX` patterns |
| C3:2F00..C3:2FFF | data (frozen) | high | 40 BRK (15.6%), `30 XX 30 YY` tilemap/frame patterns |

### Key Analysis Insights
- **C3:2C00**: The `BMI $2C01` branch from C3:2BF9 resolved to data (`CMP [$08]`), confirming a dead code path or never-taken branch
- **C3:2D00**: Apparent RTL at $2D09 and RTS at $2D3A are byte coincidences — $6B is the high byte of `ROL $6B0A` operand, $60 is the DP operand of `ORA [$60],Y`
- **C3:2E00-2FFF**: Large structured data region containing lookup tables, coordinate pair arrays, and tilemap/animation frame data

---

## 4. Artifacts Produced

| Artifact | Path |
|----------|------|
| Pass 192 disasm note | `passes/disasm/pass192.md` (599 lines) |
| Pass 193 disasm note | `passes/disasm/pass193.md` |
| Pass 192 manifest | `passes/manifests/pass1209_c3_s32.json` |
| Pass 193 manifest | `passes/manifests/pass1210_c3_s32.json` |
| Pass 192 labels | `passes/labels/pass192.md` |
| Pass 193 labels | `passes/labels/pass193.md` |
| Closed ranges update | `tools/cache/closed_ranges_snapshot_v1.json` (1744 ranges) |
| Session plan | `plans/disassembly_session_32_plan.md` |

---

## 5. Methodology Notes

### Byte-Coincidence Detection
A key methodological improvement this session: **byte-coincidence analysis** was applied to distinguish real opcodes from data bytes that happen to match opcode values. Examples:
- $6B (RTL) appearing as the high byte of a `ROL $6B0A` address operand
- $60 (RTS) appearing as the DP operand of `ORA [$60],Y`
- $40 (RTI) appearing 14 times in structured data with `00 XX 00 XX` patterns
- $20 (JSR) appearing frequently as a data value in tabular regions

### Score Deflation
Pages C3:2E00-2FFF had raw code scores of 104-110, but these were entirely inflated by byte coincidences in structured data. After coincidence analysis, the effective code score dropped to near zero. This reinforces the project's policy of requiring **local byte-level sanity checks** alongside raw scoring.

---

## 6. Next Seam

Resume at **C3:3000**. The existing flow analysis report `reports/c3_2900_3058_flow.json` covers up to C3:3058, suggesting the C3:3000+ region has been previously analyzed and may contain callable code. Before proceeding:
1. Check existing manifests for C3:3000+ coverage
2. Review `reports/c3_2900_3058_flow.json` for branch targets and return anchors
3. Verify whether C3:3000 is already closed by a prior manifest
