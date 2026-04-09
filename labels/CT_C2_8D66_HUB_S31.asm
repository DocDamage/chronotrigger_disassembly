; C2:8D66-C2:8D8F - ct_c2_8d66_helper
; Score: 12
; Size: 41 bytes
; Session: 31
;
; C2:8C00-9000 hub region expansion
; 3 internal calls
;
; Characteristics:
; - Part of 8000-region service network
; - Strong function boundaries
; - Hub network connector

ct_c2_8d66_helper:
    ; Function entry point
    .addr $8D66

ct_c2_8d66_helper_end:
    ; Function boundary end
    .addr $8D8E
