; C2:8F56-C2:8F6C - ct_c2_8f56_helper
; Score: 8
; Size: 22 bytes
; Session: 31
;
; C2:8C00-9000 hub region expansion
; 2 internal calls
;
; Characteristics:
; - Part of 8000-region service network
; - Strong function boundaries
; - Hub network connector

ct_c2_8f56_helper:
    ; Function entry point
    .addr $8F56

ct_c2_8f56_helper_end:
    ; Function boundary end
    .addr $8F6B
