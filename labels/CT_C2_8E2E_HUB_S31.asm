; C2:8E2E-C2:8E82 - ct_c2_8e2e_complex
; Score: 13
; Size: 84 bytes
; Session: 31
;
; C2:8C00-9000 hub region expansion
; 4 internal calls
;
; Characteristics:
; - Part of 8000-region service network
; - Strong function boundaries
; - Hub network connector

ct_c2_8e2e_complex:
    ; Function entry point
    .addr $8E2E

ct_c2_8e2e_complex_end:
    ; Function boundary end
    .addr $8E81
