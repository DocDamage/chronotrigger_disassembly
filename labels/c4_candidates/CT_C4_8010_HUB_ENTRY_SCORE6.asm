; C4:8010..C4:8038 - High confidence hub entry (Score-6 trio)
ct_c4_8010_hub_entry:
; Score: 6 (all three targets)
; Targets: C4:8012 (distance 2), C4:801F (distance 15), C4:8020 (distance 16)
; Start byte: 20 (JSR) - clean_start
; Internal callers: C4:7FF5 (to C4:8012), C4:81CD (to C4:8020)
; Cross-bank callers: 22 fake (same-bank misidentification)
; Evidence: Multi-entry hub with internal validation
; Confidence: HIGH
