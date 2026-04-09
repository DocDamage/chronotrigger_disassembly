# Pass 197: C3:3F00 Fragment Analysis

## Overview
Mixed command/data page with hardware register access patterns. No promotable functions identified.

## Range
- **C3:3F00..C3:3FFF** (256 bytes)

## Key Observations

### Hardware Register Access
- **$211B** at C3:3F24 - Mode 7 Matrix A register (16-bit write)
- **$2123** at C3:3F9E - Window Mask Settings register
- **$038C** at C3:3FC3 - Unknown (likely WRAM mirror)

### Long Addressing to WRAM
- **STA $7E6A5F** at C3:3FB0 - Store to WRAM bank $7E
- **$7E6A7E**, **$7E2006** references in C3:3FBB-3FB8 region

### Code Fragments

#### C3:3F20 - Small routine
```
C3:3F20: RTS
C3:3F21: LDA #$01
C3:3F23: CLC
C3:3F24: STZ $211B     ; Clear Mode 7 matrix register
C3:3F27: DEC $0A
C3:3F29: LDA $1C04,Y   ; Table lookup
```

#### C3:3F4E - RTL return
```
C3:3F4E: RTL            ; Return from long call
```

#### C3:3F99 - JSR to known function
```
C3:3F99: JSR $36CC      ; Call to C3:36CC (known utility)
C3:3F9C: LDA #$33
C3:3F9E: STA $2123      ; Window mask settings
```

#### C3:3FB0 - WRAM long store
```
C3:3FB0: STA $7E6A5F    ; Store A to WRAM (16-bit)
C3:3FB4: LDA #$08
C3:3FB6: PHP            ; Push processor status
C3:3FB7: STA $7E2006    ; Store to WRAM
```

## Analysis
This page contains scattered code fragments related to:
1. Mode 7 matrix manipulation (SNES background mode)
2. Window mask configuration
3. WRAM data structures in bank $7E

## Why Not Promoted
- No clean entry points with verified caller chains
- Fragmented execution flow with data interspersed
- Local clusters lack sufficient return anchoring
- Byte-coincidence patterns suggest data/table regions

## Labels (Tentative)
- `ct_c3_3f20_mode7_fragment` - Mode 7 register setup
- `ct_c3_3f99_window_mask_call` - Window settings JSR
- `ct_c3_3fb0_wram_store` - WRAM long address store
