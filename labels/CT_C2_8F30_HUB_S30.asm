; C2:8F30-C2:8F8E - ct_c2_8f30_routine_s30
; Score: 9
; Size: 94 bytes
; Session: 30
;
; C2:8000-9000 hub region expansion
; 6 internal calls
;
; Characteristics:
; - Part of 8000-region service network
; - Strong function boundaries
; - Call-rich handler

ct_c2_8f30_routine_s30:
    ; Function entry point
    .addr $8F30

ct_c2_8f30_routine_s30_end:
    ; Function boundary end
    .addr $8F8D
