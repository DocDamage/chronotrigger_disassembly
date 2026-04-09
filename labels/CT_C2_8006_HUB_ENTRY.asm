; C2:8006-8090 - Hub Entry Service
; Score: 6
; Size: 138 bytes
; Session: 29
;
; C2:8000 hub area - Major entry point candidate
; 6 internal calls, cross-bank accessible
;
; Characteristics:
; - Primary hub service function
; - Multiple internal JSR calls
; - Strong function boundaries
; - Part of 8000-region service network

ct_c2_8006_hub_entry_s29:
    ; Entry point for hub service
    .addr $8006
    
ct_c2_8006_service_end:
    ; Function boundary end
    .addr $8090
